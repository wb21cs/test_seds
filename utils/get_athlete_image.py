import requests
from bs4 import BeautifulSoup

def get_athlete_image(name):
    name = "-".join(name.lower().split(' ')[::-1])
    url = f"https://www.olympics.com/en/athletes/{name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch page")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    picture = soup.find("div", {"data-cy": "athlete-image"})
    
    if not picture:
        print("Image not found")
        return None

    img = picture.find("img")

    if not img or not img.get("src"):
        print("Image src not found")
        return None

    return img["src"]