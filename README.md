<!-- Danh sách sản phẩm (list) -->
<div id="detail-collection" class="collection-layout"> 
    <!-- Thông tin sản phẩm (list item) -->
    <div class="collection-product" data-list-id="Laptop ASUS - Học tập và Làm việc">
        <div class="col-xl-3 col-lg-3 col-6 proloop ajaxloop bg_border loaded"
            data-level="E" data-handle="laptop-asus-expertbook-p1403cva-c3u08-50w"
            data-id="1072890525"
            data-list-items-item_id="LAP-ASUS-EXPERT-P1403CVA-C3U08-50W"
            data-list-items-item_name="Laptop ASUS ExpertBook P1403CVA-C3U08-50W"
            data-list-items-item-price="13100000"
            data-list-items-item-spec_cpu="Intel Core 3 Processor 100U"
            data-list-items-item-spec_bao_mat="Fingerprint sensor intergrated with Touchpad; BIOS Booting User Password Protection; HDD User Password Protection and Security; Trusted Platform Module"
            data-list-items-item-spec_chuan_mau="45% NTSC"
            data-list-items-item-spec_he_dieu_hanh="Windows 11"
            data-list-items-item-spec_pin="50Wh"
            data-list-items-item-spec_dong_san_pham="ExpertBook"
            data-list-items-item-spec_card_do_hoa="Intel UHD Graphics"
            data-list-items-item-spec_kich_thuoc_man_hinh="14"
            data-list-items-item-spec_ram="8GB"
            data-list-items-item-spec_hang="ASUS"
            data-list-items-item-spec_lcd="IPS / FHD"
            data-list-items-item-spec_vga="Intel UHD Graphics"
            data-list-items-item-spec_cong_ket_noi="2 USB-C; 2 USB-A; 1 HDMI; 1 Jack 3.5mm; 1 Ethernet"
            data-list-items-item-spec_do_day="19.7mm"
            data-list-items-item-spec_trong_luong="1.4kg"
            data-list-items-item-spec_nhu_cau_su_dung="Văn phòng"
            data-list-items-item-spec_tan_so_quet="60Hz"
            data-list-items-item-spec_do_phan_giai="FHD (1920 x 1080)"
            data-list-items-item-spec_ssd="512GB">
        </div>
        ...
    </div>
    ...
</div>

dưới đây là phần cấu trúc html cần cào, gồm div#detail-collection chứa các product card có data-list-id và class collection-product. lưu ý data-list-items-item-spec không đồng nhất với nhau chỉ có vài spec là tất cả product đều có như name, id, price

<!-- link chi tiết sản phẩm (không cần selenium): https://gearvn.com/products/{data-handle} -->
<div class="product-gallery--inner sticky-gallery">
											
<div class="product-gallery--slide swiper" id="slideProduct">	
<div class="swiper-wrapper">


<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-1_731bd2b40fba4760aaa43822bd8ab0ad_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-1_731bd2b40fba4760aaa43822bd8ab0ad_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-1_731bd2b40fba4760aaa43822bd8ab0ad_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-2_0e9b4fe2a40744b99167a13d4254edbd_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-2_0e9b4fe2a40744b99167a13d4254edbd_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-2_0e9b4fe2a40744b99167a13d4254edbd_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-3_bb2876892bd6444785e78b25284841dd_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-3_bb2876892bd6444785e78b25284841dd_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-3_bb2876892bd6444785e78b25284841dd_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-4_8bbca19ab2844d40ab2ab6dc3df8f02b_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-4_8bbca19ab2844d40ab2ab6dc3df8f02b_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-4_8bbca19ab2844d40ab2ab6dc3df8f02b_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-5_79f8111ead0444a2849edcf678167fbc_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-5_79f8111ead0444a2849edcf678167fbc_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-5_79f8111ead0444a2849edcf678167fbc_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-6_c80f0c571b4241629b283f1084141b9e_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-6_c80f0c571b4241629b283f1084141b9e_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-6_c80f0c571b4241629b283f1084141b9e_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-7_dca0908f62d24afeb135c403bdae43f4_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-7_dca0908f62d24afeb135c403bdae43f4_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-7_dca0908f62d24afeb135c403bdae43f4_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	
<div class="product-gallery--photo swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-8_be797205a81a417d93b943bc42b0c0a5_master.jpg">
<div class="product-gallery--item boxlazy-img">
    <div class="boxlazy-img--insert lazy-img--prod">
        <a data-fancybox="gallery" class="boxlazy-img--aspect" href="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-8_be797205a81a417d93b943bc42b0c0a5_master.jpg">
            <img src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-8_be797205a81a417d93b943bc42b0c0a5_master.jpg" class="gallery-demo swiper-lazy" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
        </a>
    </div>
</div>					
</div>	


</div>
<div class="swiper-nav swiper-nav-main">
<span class="swiper-button swiper-prev swiper-product-prev">
</span>
<span class="swiper-button swiper-next swiper-product-next">
</span>
</div>
</div>
<div class="product-gallery--thumb swiper" id="slideThumb">
<div class="swiper-wrapper">

<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-1_731bd2b40fba4760aaa43822bd8ab0ad_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-1_731bd2b40fba4760aaa43822bd8ab0ad_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-2_0e9b4fe2a40744b99167a13d4254edbd_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-2_0e9b4fe2a40744b99167a13d4254edbd_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-3_bb2876892bd6444785e78b25284841dd_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-3_bb2876892bd6444785e78b25284841dd_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-4_8bbca19ab2844d40ab2ab6dc3df8f02b_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-4_8bbca19ab2844d40ab2ab6dc3df8f02b_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-5_79f8111ead0444a2849edcf678167fbc_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-5_79f8111ead0444a2849edcf678167fbc_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-6_c80f0c571b4241629b283f1084141b9e_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-6_c80f0c571b4241629b283f1084141b9e_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-7_dca0908f62d24afeb135c403bdae43f4_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-7_dca0908f62d24afeb135c403bdae43f4_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	
<div class="product-thumb swiper-slide" data-image="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-8_be797205a81a417d93b943bc42b0c0a5_compact.jpg">
    <div class="product-thumb--link boxlazy-img">		
        <div class="boxlazy-img--insert lazy-img--prod">
            <span class="boxlazy-img--aspect">
                <img class="product-thumb--photo" src="//cdn.hstatic.net/products/200000722513/laptop-asus-expertbook-p1403cva-c3u08-50w-8_be797205a81a417d93b943bc42b0c0a5_compact.jpg" alt=" Laptop ASUS ExpertBook P1403CVA-C3U08-50W ">
            </span>
        </div>
    </div>					
</div>	

</div>
<div class="swiper-nav swiper-nav-thumb">

</div>
</div>	


</div>

<!-- Thông tin chi tiết -->
<div class="product-inner">
    <div class="product-block product-desc">
        <div class="product-heading"><h2>Thông tin sản phẩm</h2></div>		
        <div class="product-wrap">
            <div class="product-desc--content expandable-toggle opened"> 
                <div class="desc-content">
                    <!-- thông tin chi tiết của sản phẩm được trình bày dưới dạng bài viết có định dạng (ảnh đi kèm, bảng thông số kỹ thuật) -->
                </div>
                <div class="desc-btn">
                    <button class="expandable-btn button">
                        <span class="expandable-toggle--text more">Đọc tiếp bài viết</span>
                        <span class="expandable-toggle--text less">Thu gọn bài viết</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Bảng thông số kỹ thuật -->
<div class="modal-body">
<div class="table-technical">
    <ul>
        <li class="5">
            <div>CPU</div>
            <div>Intel Core 3 Processor 100U</div>
        </li>
        <li class="6">
            <div>Bảo mật</div>
            <div>Fingerprint sensor intergrated with Touchpad; BIOS Booting User Password
                Protection; HDD User Password Protection and Security; Trusted Platform Module
            </div>
        </li>
        <li class="7">
            <div>Chuẩn màu</div>
            <div>45% NTSC</div>
        </li>
        <li class="9">
            <div>Dòng sản phẩm</div>
            <div>ExpertBook</div>
        </li>
        <li class="10">
            <div>Pin</div>
            <div>50Wh</div>
        </li>
        <li class="11">
            <div>Hệ điều hành</div>
            <div>Windows 11</div>
        </li>
        <li class="12">
            <div>Card đồ họa</div>
            <div>Intel UHD Graphics</div>
        </li>
        <li class="14">
            <div>RAM</div>
            <div>8GB</div>
        </li>
        <li class="15">
            <div>Kích thước màn hình</div>
            <div>14"</div>
        </li>
        <li class="18">
            <div>LCD</div>
            <div> IPS / FHD</div>
        </li>
        <li class="21">
            <div>Hãng</div>
            <div>ASUS</div>
        </li>
        <li class="22">
            <div>Độ dày</div>
            <div>19.7mm</div>
        </li>
        <li class="23">
            <div>VGA</div>
            <div>Intel UHD Graphics</div>
        </li>
        <li class="24">
            <div>Nhu cầu sử dụng</div>
            <div>Văn phòng</div>
        </li>
        <li class="25">
            <div>Cổng kết nối</div>
            <div>2 USB-C; 2 USB-A; 1 HDMI; 1 Jack 3.5mm; 1 Ethernet</div>
        </li>
        <li class="26">
            <div>Trọng lượng</div>
            <div>1.4kg</div>
        </li>
        <li class="27">
            <div>Tần số quét</div>
            <div>60Hz</div>
        </li>
        <li class="29">
            <div>SSD</div>
            <div>512GB</div>
        </li>
        <li class="30">
            <div>Độ phân giải</div>
            <div>FHD (1920 x 1080)</div>
        </li>
    </ul>
</div>
</div>


Tạo project python cào web gearvn.
hiện tại tôi đã có: 
- file json danh mục và đường link tương ứng để cào danh sách sản phẩm tương ứng với danh mục đó.
- cấu trúc html của 2 trang list và trang detail.
hướng đi:
- 1. app sẽ đọc file gearvn_brands.json và load danh sách link danh mục.
- 2. sử dụng selenium để lấy được trang html -> cào link và thông tin sản phẩm các sản phẩm (có id, tên, giá, ...)
- 3. từ link mỗi sản phẩm -> dùng requests để lấy trang html để cào thêm thông tin:
    + danh sách ảnh minh họa của sản phẩm
    + phần thông tin chi tiết: thường là 1 bài viết review có thể có bảng kỹ thuật đi kèm, hình ảnh minh họa, link video review youtube
    + bảng thông số kỹ thuật
- 4. kết hợp 2 thông tin sản phẩm đã cào ở bước 2, 3 -> lưu vào file json
Lưu ý: do sản phẩm đa dạng nên phần thông tin chi tiết cũng khá đa dạng theo. theo tôi quan sát có 3 dạng chính:
    dạng 1: bài viết review + ảnh minh họa
    dạng 2: bảng thông tin sản phẩm (khác với bảng thông số kỹ thuật)
    dạng 3: Kết hợp cả 2  
dự kiến sẽ cào toàn bộ thông tin phần này và chuyển sang dạng mardown để lưu vào file json.

Giờ hãy lên plan chi tiết cho tôi, bao gồm:
- cấu trúc thư mục
- các file cần thiết
- luồng hoạt động của app
- các thư viện sẽ sử dụng

Tạo phần sườn thư mục và cấu trúc file dựa theo hướng đi trên.
Sau khi lên plan, chúng ta sẽ thực hiện chi tiết từng bước theo plan và tôi sẽ cung cấp thêm thông tin về cấu trúc html, những điểm cần lưu ý trong quá trình cào web.

Nếu có câu hỏi thêm thì hãy hỏi lại, hoặc có đề xuất hay thì báo cho tôi biết.