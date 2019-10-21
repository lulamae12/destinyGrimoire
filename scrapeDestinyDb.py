import requests
import urllib.request
from urllib.request import Request
import time,sys
from bs4 import BeautifulSoup
from soupMaker import soupGen



class grimoreScrape():
    def __init__(self,link):
        self.url = link
        self.response = requests.get(self.url)
        print(self.response)
    def makeSoup(self):
        soup = BeautifulSoup(self.response.text,"html.parser")
        soupPretty = soup.prettify()
        #print(soupPretty)
        self.findLoreEntryObjects(soup)
    def formatSubtitle(self,subtitle):
        subtitle = str(subtitle);subtitle = subtitle.strip('<p class="subtitle">');subtitle = subtitle.replace("<b>","");subtitle = subtitle.replace("</b>","");subtitle = subtitle.replace("</","");subtitle = subtitle.replace("\n","")

        #has < or > as special chars idents
        subtitle = subtitle.replace("&lt;","<");subtitle = subtitle.replace("&gt;",">")

        #italics
        subtitle = subtitle.replace("<span><i>","");subtitle = subtitle.replace("i>span>","")

        #print(subtitleSpl)
        if subtitle == "Non":
            #print("NONETYPE FOUND")
            subtitle = "NAN"
        return subtitle

    def getAndFormatDescription(self,soup):
        #print(soup)
        soupContentList = []
        for item in soup:
            
            if str('class="subtitle">') not in str(item).split(): #not subtitle must be desc
                description = item
        
        description = str(description);description = description.replace("<p>","");description = description.replace("</p>","");description = description.replace("<br/>","\n");description = description.replace("\'","'")

        return description
    def findTitle(self,soup):
        soupTitle = BeautifulSoup(str(soup))
        title = soupTitle.find("a").string
        return title

    def getImageUrl(self,soup): #get src attribute from img tag
        imgSrc = soup["src"]
        imgName = soup["alt"];imgName =imgName + ".jpg"
        
        return imgSrc,imgName
    def makeJson(self,Title,Subtitle,Description,ImageName,ImageUrl):
            data = {
                Title:{
                    "Title":Title,
                    "Subtitle":Subtitle,
                    "Description":Description,
                    "ImageName":ImageName,
                    "ImageUrl":ImageUrl
                }
            }
            print(data)
            return data   

    def saveJson(self,jsonDict,jsonInfoTuple):
        print(jsonDict)
    def findLoreEntryObjects(self,soup):
        loreSections = []
        url = self.url
        for section in soup.find_all("div",class_="panel panel-default clearfix grimoire-card"):
            loreSections.append(section)
        #print(loreSections[0])
        for item in loreSections:
            soupSection = BeautifulSoup(str(item))
            
            cardTitle = self.findTitle(soupSection.find("h3",style="margin-top: 0;"))

            cardSubtitle = self.formatSubtitle(soupSection.find("p",class_="subtitle"))

            cardDescription = self.getAndFormatDescription(soupSection.findAll("p"))
            
            cardImageUrl,cardImageName = self.getImageUrl(soupSection.find(class_="card-image"))
            
                    


            
            print("==============")

            print("Title: ",cardTitle)
            print("Subtitle: ",cardSubtitle)
            print("Description: ",cardDescription)
            print("\nImage name: ",cardImageName)
            print("Image url: ",cardImageUrl)
            print("===============")
            data = self.makeJson(cardTitle,cardSubtitle,cardDescription,cardImageName,cardImageUrl)

            #sys.exit()
            
        # maincontent = soup.find("div",class_="panel panel-default clearfix grimoire-card")
        #list1 = str(maincontent).split("</a>")
        #print(maincontent)
        #for i in list1:
         #   print(i)
        #print(list1[0])


            
g= grimoreScrape("https://db.destinytracker.com/d1/grimoire/guardian/ghost")
g.makeSoup()