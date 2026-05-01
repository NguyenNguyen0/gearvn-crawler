# Product Service — Model Design & Data Pipeline Plan

---

## Phần 1 — Model Design

### 1.1 Brand

Thêm `parentBrandId` để hỗ trợ brand hierarchy (ASUS → ASUS/ROG, ACER → ACER/Predator) thay vì nối tên bằng dấu `/`.

```java
public class Brand {

    @Id
    private String id;

    private String name;

    private String slug;

    private String parentBrandId;   // NEW — null nếu là brand gốc

    private String logoUrl;

    private boolean active;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
```

> Khi query danh sách brand gốc: `parentBrandId = null`. Sub-brand dùng để filter nâng cao hoặc hiển thị breadcrumb.

---

### 1.2 Category

Giữ nguyên cấu trúc, không thay đổi. Việc cần làm là **clean data**: xóa các node category đang dùng để nhóm brand (Brands → ASUS, ACER…). Brand filter đi qua `brandId` trong Product, không đi qua Category tree.

```java
public class Category {

    @Id
    private String id;

    private String name;

    private String slug;

    private String description;

    private String parentId;        // null nếu là danh mục gốc

    private String imageUrl;

    private int sortOrder;

    private boolean active;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
```

---

### 1.3 Product

Model thay đổi nhiều nhất. Các field mới xuất phát trực tiếp từ data crawl GearVN và nhu cầu thực tế.

```java
public class Product {

    @Id
    private String id;

    @TextIndexed(weight = 5)
    private String name;

    private String slug;

    @TextIndexed(weight = 2)
    private String description;         // plain text — dùng cho full-text search

    private String descriptionHtml;     // NEW — HTML để render, không index

    private BigDecimal price;

    private BigDecimal compareAtPrice;

    @TextIndexed(weight = 3)
    private String sku;

    private String thumbnail;           // NEW — ảnh đại diện trên listing

    private List<String> images;        // ảnh chi tiết

    private String categoryId;

    private String brandId;

    private Map<String, String> specs;  // NEW — thông số kỹ thuật (cpu, ram, ssd…)

    private List<String> tags;          // NEW — new-arrival, hot-deal, gaming…

    private Map<String, String> attributes;  // thuộc tính tùy chọn khác

    private Map<String, String> metadata;   // NEW — source tracking, không thuộc domain
                                            // { source: "gearvn",
                                            //   externalId: "1072890525",
                                            //   sourceUrl: "https://..." }

    private boolean active;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
```

**Lý do tách `description` và `descriptionHtml`:** `description` là plain text để MongoDB text index hoạt động chính xác. `descriptionHtml` lưu nguyên HTML gốc để render phía client — nếu gộp chung thì HTML tags sẽ nhiễu kết quả search.

**Lý do dùng `metadata` thay vì `sourceUrl` + `externalId` riêng lẻ:** Map linh hoạt, không làm phình domain model, dễ thêm key mới khi có nguồn crawl khác. Khi không cần nữa chỉ xóa key, không phải migrate schema.

---

## Phần 2 — Data Pipeline Plan

Pipeline xử lý dữ liệu crawl từ GearVN vào MongoDB theo model mới. Thiết kế **idempotent** — chạy lại nhiều lần không tạo duplicate.

### Tổng quan

```
Raw JSON (GearVN)
      │
      ▼
[1] Validate & clean
      │
      ▼
[2] Resolve Brand  ──────────► brands collection (upsert)
      │
      ▼
[3] Resolve Category ────────► categories collection (upsert)
      │
      ▼
[4] Transform → Product model
      │
      ▼
[5] Upsert MongoDB ──────────► products collection
      │
      ▼
[6] Post-process (slug, indexes)
```

---

### Bước 1 — Validate & clean

**Required fields:** `name`, `price`, `category`, `brand`, `images` (ít nhất 1 phần tử).

**Các transform cần làm:**
- `price`: parse từ string `"NumberInt('13100000')"` hoặc số nguyên thô → `BigDecimal`
- `images`: lọc bỏ URL có khoảng trắng sau `"https: //"` (lỗi phổ biến trong data GearVN), normalize thành `"https://"`
- `thumbnail`: tương tự, normalize URL

**Nếu thiếu required field:** skip record, log warning kèm `raw.id`. Không throw exception để pipeline tiếp tục xử lý các record còn lại.

---

### Bước 2 — Resolve Brand

Xử lý cả trường hợp brand đơn (`"ASUS"`) và sub-brand (`"ASUS / ROG"`).

```
brand string có " / " ?
    ├── YES → split thành [parentName, childName]
    │         └── lookup parentName
    │               ├── không tìm thấy → insert Brand(parentBrandId=null)
    │               └── tìm thấy → lấy parent.id
    │         └── lookup childName với parentBrandId=parent.id
    │               ├── không tìm thấy → insert Brand(parentBrandId=parent.id)
    │               └── tìm thấy → dùng luôn
    │         └── brandId = child.id
    │
    └── NO  → lookup trực tiếp (case-insensitive)
              ├── không tìm thấy → insert Brand(parentBrandId=null)
              └── tìm thấy → dùng luôn
              └── brandId = brand.id
```

**Performance:** cache `Map<brandName, brandId>` trong session để tránh query MongoDB lặp lại cho cùng một brand.

---

### Bước 3 — Resolve Category

```
lookup category theo raw.category (case-insensitive, trim)
    ├── không tìm thấy → insert Category(parentId=null, sortOrder=0, active=true)
    └── tìm thấy → lấy category.id

nếu raw.sub_category != null:
    lookup sub_category với parentId = category.id
        ├── không tìm thấy → insert Category(parentId=category.id)
        └── tìm thấy → dùng luôn
    categoryId = subCategory.id
else:
    categoryId = category.id
```

**Performance:** tương tự Brand, cache `Map<categoryName, categoryId>` trong session.

---

### Bước 4 — Transform → Product model

```javascript
// Mapping logic
product.name            = raw.name
product.slug            = slugify(raw.name)          // xử lý ở bước 6
product.description     = stripHtml(raw.description_html)
product.descriptionHtml = raw.description_html
product.price           = parsePrice(raw.price)
product.compareAtPrice  = null                        // GearVN không có field này
product.sku             = raw.id                      // dùng externalId làm sku tạm
product.thumbnail       = normalizeUrl(raw.thumbnail)
product.images          = raw.images
                            .map(normalizeUrl)
                            .filter(isValidUrl)
product.categoryId      = <từ bước 3>
product.brandId         = <từ bước 2>
product.specs           = raw.specs                   // Map trực tiếp
product.tags            = []                          // để trống, fill thủ công sau
product.attributes      = {}
product.metadata        = {
                            source:     "gearvn",
                            externalId: raw.id,
                            sourceUrl:  normalizeUrl(raw.url)
                          }
product.active          = true
```

---

### Bước 5 — Upsert MongoDB

Điều kiện match để upsert:

```javascript
filter = {
  "metadata.source":     "gearvn",
  "metadata.externalId": raw.id
}
```

- Dùng `replaceOne(filter, product, { upsert: true })`
- Khi là **update** (document đã tồn tại): preserve `createdAt` — chỉ ghi đè các field khác
- Đếm và log: `inserted` / `updated` / `skipped`

---

### Bước 6 — Post-process

**Slug generation:**
- `slugify(name)`: lowercase, bỏ dấu tiếng Việt, thay space bằng `-`, xóa ký tự đặc biệt
- Ví dụ: `"Laptop ASUS ExpertBook P1403CVA"` → `"laptop-asus-expertbook-p1403cva"`

**Slug uniqueness:**
- Nếu slug đã tồn tại trong collection → thêm suffix: `-2`, `-3`, …
- Update lại document sau khi có slug unique

**Verify indexes** sau khi load xong:

```javascript
// Text index cho search
db.products.createIndex({ name: "text", description: "text", sku: "text" })

// Filter thường dùng
db.products.createIndex({ categoryId: 1, active: 1 })
db.products.createIndex({ brandId: 1, active: 1 })
db.products.createIndex({ slug: 1 }, { unique: true })
db.products.createIndex({ "metadata.externalId": 1, "metadata.source": 1 })
```

---

### Output log mẫu

```
[Pipeline] Start — source: gearvn, total records: 168
[Validate] Skipped: 3 records (missing required fields)
[Brand]    Inserted: 12 | Found existing: 48
[Category] Inserted: 2  | Found existing: 6
[Product]  Inserted: 120 | Updated: 45 | Skipped: 3
[Slug]     Conflicts resolved: 2
[Done]     Elapsed: 4.2s
```

---

## Phần 3 — Lưu ý quan trọng

**Image URL bị lỗi trong data GearVN:** các URL có dạng `"https: //cdn.hstatic.net/..."` (có khoảng trắng). Cần normalize trước khi lưu, không phải filter bỏ.

**`description_html` đang rỗng:** trong data mẫu, field này là `<div class='desc-content'></div>`. Nếu cần mô tả đầy đủ thì phải crawl lại từng trang chi tiết sản phẩm.

**Brand name case không nhất quán:** data có cả `"ACER"` và `"Acer"` tồn tại song song trong brands.json. Lookup brand cần dùng case-insensitive + trim, sau đó normalize về một dạng chuẩn khi insert.

**Batch size:** nếu crawl nhiều record (>1000), chia batch 100–200 records/lần khi upsert để tránh timeout.

---

## Phần 4 — Checklist triển khai

- [ ] Cập nhật 3 model Java theo thiết kế ở Phần 1
- [ ] Tạo/verify MongoDB indexes (Phần 2, Bước 6)
- [ ] Viết pipeline script theo plan Phần 2
- [ ] Chạy thử với tập nhỏ (~10 records) để verify mapping
- [ ] Chạy full với toàn bộ data crawl
- [ ] Kiểm tra brand hierarchy đúng (parentBrandId)
- [ ] Kiểm tra slug unique, images URL valid
- [ ] Clean category data: xóa các node category đang nhóm brand
- [ ] Review `metadata` field của vài product để đảm bảo source tracking đúng