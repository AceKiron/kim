import requests
import bs4
import sys
from urllib.request import urlretrieve

from kimutils import reporthook, getAllEpisodesInCartoon, getEpisode, host

sys.argv = sys.argv[1:]
sys.argc = len(sys.argv)

if sys.argc == 0:
    print("Missing an argument (i.e. \"latest\")")
    quit()

if sys.argv[0] == "latest":
    latest = []

    req = requests.get(host + "/Mobile/SwitchToDesktop")
    soup = bs4.BeautifulSoup(req.text, features="html.parser")

    for child in soup.find("span", {"class": "title-list"}).parent.find("div", {"class": "items"}).find_all("a"):
        latest.append({
            "series": child.find("div", {"class": "item-title"}).contents[0],
            "episode": child.attrs["title"],
            "href": child.attrs["href"]
        })

    for new in latest[::-1]:
        print(new)

if sys.argv[0] == "cartoon":
    episodes = getAllEpisodesInCartoon(sys.argv[1])

    for episode in episodes:
        print(episode)

if sys.argv[0] == "episode":
    files = getEpisode(sys.argv[1])
    file = files["1080p"]

    print("Saving " + sys.argv[1] + " to " + file["filename"])
    urlretrieve(file["url"], file["filename"], reporthook)

if sys.argv[0] == "episode-files":
    print(getEpisode(sys.argv[1]))
