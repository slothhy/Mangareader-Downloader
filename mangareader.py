import os
import img2pdf
import requests
import time
import urllib.request
from natsort import natsorted
from bs4 import BeautifulSoup

def main():
    #if directory doesn't exist, make one
    if os.path.isdir('./onepiece') is False:
        os.mkdir('./onepiece')
    if os.path.isdir('./pdfs') is False:
        os.mkdir('./pdfs')

    project_home = os.getcwd()
    #check how many chapters
    base_url = 'https://www.mangareader.net/one-piece' 
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("table", { "id" : "listing"})
    chapters = 0
    for row in table.findAll("tr"):
        chapters += 1
    
    print(chapters)

    #check if chapter exist, if not download
    for chapter in range(1, chapters + 1):
        if os.path.isdir('./onepiece/' + str(chapter)) is False:
            os.mkdir('./onepiece/' + str(chapter))
            #loop through pages
            page = 0
            while True:
                page += 1
                res = requests.get(base_url + "/" + str(chapter) + "/" + str(page))
                if res.status_code != 200:
                    break
                soup = BeautifulSoup(res.text, "lxml")
                image = soup.find('img')
                print(image['src'])
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(image['src'], './onepiece/' + str(chapter) + "/" + str(page) + ".jpg")

            with open("./pdfs/" + str(chapter) + ".pdf", "wb") as f:
                os.chdir('./onepiece/' + str(chapter))
                filelist = natsorted(os.listdir(os.getcwd()))
                #print(filelist)
                f.write(img2pdf.convert([i for i in filelist]))
                os.chdir(project_home) #workaround



main()