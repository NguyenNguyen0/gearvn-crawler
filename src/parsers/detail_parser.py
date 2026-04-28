from bs4 import BeautifulSoup

BASE_URL = "https:"


def parse_detail(html: str):
    soup = BeautifulSoup(html, "lxml")

    result = {
        "images": [],
        "specs_detail": {},
        "description_html": None,
    }

    image_nodes = soup.select(".product-gallery--photo")

    images = []
    for node in image_nodes:
        img_url = node.get("data-image")

        if img_url:
            if img_url.startswith("//"):
                img_url = BASE_URL + img_url

            images.append(img_url)

    # remove duplicate
    result["images"] = list(dict.fromkeys(images))

    spec_nodes = soup.select(".table-technical ul li")

    specs = {}

    for li in spec_nodes:
        divs = li.find_all("div")

        if len(divs) >= 2:
            key = divs[0].get_text(strip=True)
            value = divs[1].get_text(strip=True)

            if key:
                specs[key] = value

    result["specs_detail"] = specs

    desc = soup.select_one("div.desc-content")

    if desc:
        result["description_html"] = str(desc)

    return result
