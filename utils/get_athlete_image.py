import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup

def get_athlete_image(name):
    name = "-".join(name.lower().split(' ')[::-1])
    url = f"https://www.olympics.com/en/athletes/{name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
    except ConnectionError:
        return None
    except Timeout:
        return None
    except RecursionError:
        return None
    


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