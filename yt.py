import requests
from pprint import pprint
url = "https://youtube-quick-video-downloader.p.rapidapi.com/api/youtube/links"
def youtube_save(link):

    payload = {"url": link}
    headers = {
        "x-rapidapi-key": "4360836b63msh9edf45be1d447e0p105946jsn831c2c920c00",
        "x-rapidapi-host": "youtube-quick-video-downloader.p.rapidapi.com",
        "Content-Type": "application/json",
        "X-Forwarded-For": "70.41.3.18"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()[0]["urls"][0]["url"]