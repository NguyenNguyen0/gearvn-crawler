from bs4 import BeautifulSoup


BASE_URL = "https://gearvn.com"


def parse_list(html: str):
    soup = BeautifulSoup(html, "lxml")

    products = []

    items = soup.select("div.proloop.ajaxloop")

    for item in items:
        try:
            product = {}
            product_id = item.get("data-id")

            if not product_id:
                handle = item.get("data-handle")
                product_id = handle

            product["id"] = product_id
            product["name"] = item.get("data-list-items-item_name")
            price = item.get("data-list-items-item-price")

            if price:
                product["price"] = int(price)
            else:
                product["price"] = None

            product["handle"] = item.get("data-handle")
            link_tag = item.select_one("a.aspect-ratio")

            if link_tag:
                href = link_tag.get("href")
                if href:
                    product["url"] = BASE_URL + href
                else:
                    product["url"] = None

                # thumbnail
                img = link_tag.select_one("img")
                if img:
                    src = img.get("src") or img.get("data-src")
                    if src and src.startswith("//"):
                        src = "https:" + src
                    product["thumbnail"] = src
                else:
                    product["thumbnail"] = None
            else:
                product["url"] = None
                product["thumbnail"] = None

            specs = {}

            for attr, value in item.attrs.items():
                if attr.startswith("data-list-items-item-spec_"):
                    key = attr.replace("data-list-items-item-spec_", "")
                    specs[key] = value

            product["specs"] = specs

            products.append(product)

        except Exception as e:
            print(f"Error parsing product: {e}")

    return products
