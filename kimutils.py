import sys
import bs4
import requests

host = "https://kimcartoon.li"

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def getAllEpisodesInCartoon(url):
    episodes = []

    for episode in bs4.BeautifulSoup(requests.get(host + url).text, features="html.parser").find("ul", {"class": "list"}).find_all("li"):
        episodes.append({
            "episode": episode.find("span").contents[0],
            "href": episode.find("a").attrs["href"]
        })

    return episodes[::-1]

def getEpisode(url):
    links = {}

    for i in requests.get(host + url).text.replace("\r", "").split("\n"):
        if i.strip().startswith("location"):
            offsiteUrl = bs4.BeautifulSoup(requests.get(i.strip().replace("location.href = '", "").replace("';", ""), headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "kisscenter.net",
                "Referer": "http://ghostthis.review",
                "Sec-GPC": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36"
            }, cookies={
                "snc": "1"
            }).text, features="html.parser").find("iframe", {"id": "my_video_1"}).attrs["src"]

            if offsiteUrl.startswith("https://www.luxubu.review/v/"):
                for file in requests.post("https://www.luxubu.review/api/source/" + offsiteUrl.replace("https://www.luxubu.review/v/", "")).json()["data"]:
                    links[file["label"]] = {
                        "url": file["file"],
                        "filename": url.replace("/", "").replace("-", "").split("?")[0][7:] + "." + file["type"]
                    }

            else:
                print("UNKNOWN PROVIDER: " + offsiteUrl)

    return links
