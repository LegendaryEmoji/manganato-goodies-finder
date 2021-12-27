import requests, json, time, random
from bs4 import BeautifulSoup
from colorama import init, Fore

init()

def main():
    global BASE_URL
    loadConfig()
    if not jsonData["genre"]: return error("Unable to detect the genre!")
    if type(jsonData["minimumViews"]) != int: return error("Unable to detect the minimum views!")
    if jsonData["limit"] == "auto": jsonData["limit"] = 0
    if type(jsonData["limit"]) != int: return error("Unable to detect the limit of pages!")
    BASE_URL = f"https://manganato.com/genre-{jsonData['genre']}/(NUM){'' if not jsonData.get('genreQuery') else jsonData.get('genreQuery')}"
    if jsonData["limit"] == 0: jsonData["limit"] = getTheLimit(BASE_URL.replace("(NUM)", "1"))
    try:
        for i in range(int(jsonData["limit"])):
            print(f"~ Scraping: {i+1}")
            scrapeThePage(requests.get(BASE_URL.replace("(NUM)", f"{i+1}")).text)
    except:
        print(f"{Fore.LIGHTCYAN_EX}~ Stopped the scraper!")
        input("~ Press enter to exit...")
        exit()
    print(f"{Fore.MAGENTA}~ Done!")
    input("~ Press enter to exit...")
    exit()
        

def loadConfig():
    global jsonData
    with open("configurations.json") as fileData:
        jsonData = json.load(fileData)

def error(msg):
    print(f"{Fore.RED}Oops ~ {msg}")
    time.sleep(10)
    exit()

def getTheLimit(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    lastPageNumber = soup.find(class_="page-blue page-last")
    if not lastPageNumber:
        input(f"{Fore.RED}~ Invalid genre provided...")
        exit()
    return lastPageNumber.text.replace("LAST(", "").replace(")", "")


def scrapeThePage(html):
    soup = BeautifulSoup(html, "html.parser")
    mainCollection = soup.find(class_="panel-content-genres")
    for element in mainCollection.children:
        anotherSoup = BeautifulSoup(str(element.encode("utf-8")), "html.parser")
        rating = anotherSoup.find(class_="genres-item-rate")
        if not rating: continue
        rating, views = rating.text, anotherSoup.find(class_="genres-item-view").text.replace(",", "")
        if float(rating) < jsonData["minimumRating"] or int(views) < jsonData["minimumViews"]: continue
        head = anotherSoup.find(class_="genres-item-name text-nowrap a-h")
        if head.attrs["href"].split("manga-")[1] in jsonData["alreadyKnow"]: continue
        latestChapter = anotherSoup.find(class_="genres-item-chap text-nowrap a-h").text.replace("Chapter ", "")
        image, shortDescription = anotherSoup.find(class_="img-loading").attrs["src"], anotherSoup.find(class_="genres-item-description").text.strip()
        print(f"{Fore.__dict__.get(random.choice(jsonData['printingColors']))}[{rating}] ~ {head.text}\nThumbnail - {image}\nLatest chapter ~ {latestChapter}\nViews ~ {views}\nURL - {head.attrs['href']}\nShort Description -\n{shortDescription}\n====================")

if __name__ == "__main__":
    main()