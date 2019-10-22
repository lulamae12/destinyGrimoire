import requests
import urllib.request
from urllib.request import Request
import time,sys,os,json
from bs4 import BeautifulSoup
from soupMaker import soupGen



class grimoireScrape():
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
        subtitle = str(subtitle);subtitle = subtitle.strip('<p class="subtitle">');subtitle = subtitle.replace("<b>","");subtitle = subtitle.replace("</b>","");subtitle = subtitle.replace("</","");subtitle = subtitle.replace("\n","");subtitle = subtitle.replace('\"',"");subtitle =subtitle.replace("\u2014","-");subtitle =subtitle.replace("\u201d",'"');subtitle =subtitle.replace("\u201c",'"');subtitle =subtitle.replace("<i>",'');subtitle = subtitle.replace("\u2019","'")

        #has < or > as special chars idents
        subtitle = subtitle.replace("&lt;","<");subtitle = subtitle.replace("&gt;",">")

        #italics
        subtitle = subtitle.replace("<span><i>","");subtitle = subtitle.replace("i>span>","");subtitle=subtitle.replace("i>","");subtitle = subtitle.replace("<span>","");subtitle = subtitle.replace("&gt;",">");subtitle=subtitle.replace("</","");subtitle = subtitle.replace("\u00fb","u");subtitle = subtitle.replace("<br/>","")
        
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
        
        description = str(description);description = description.replace("<p>","");description = description.replace("</p>","");description = description.replace("<br/>","\n");description = description.replace("\"","'");description =description.replace("\u2014","-");description =description.replace("\u201d",'"');description =description.replace("\u201c",'"');description =description.replace("<i>",'');description = description.replace("i>span>","")
        description = description.replace("i>","");description = description.replace("<b>","");description = description.replace("\u2019","'");description=description.replace("i>","");description = description.replace("\u2013"," - ");description = description.replace("&gt;",">");description = description.replace("</","");description = description.replace("&lt;","<");description = description.replace("\u00fb","u");description=description.replace("<br/>","")
       
        return description
    def findTitle(self,soup):
        soupTitle = BeautifulSoup(str(soup))
        title = soupTitle.find("a").string
        return title

    def getImageUrl(self,soup): #get src attribute from img tag
        imgSrc = soup["src"]
        imgName = soup["alt"];imgName =imgName + ".jpg"
        imgName = imgName.replace("&#39;","'");imgName = imgName.replace("&lt;","<");imgName=imgName.replace("&gt;",">");imgName = imgName.replace("\u00fb","u")
        
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
            #print(data)
            return data   



    def saveJson(self,jsonDict,fileInfoTuple):
        currentDir = os.getcwd()

        if os.path.exists("Destiny1Grimoire") == False:
            os.makedirs("Destiny1Grimoire")
            print("Directory 'Destiny1Grimoire' created!")
        else:
            pass
        
        
        topPathCat = fileInfoTuple[0]
        bottomPathCat = fileInfoTuple[1]
        currentDir = currentDir + "\\" + "Destiny1Grimoire\\" +topPathCat
        if os.path.exists(currentDir) == False:
            os.makedirs(currentDir)
            print("Directory ",topPathCat," created in :\n",currentDir)
        else:
            pass
        currentDir = currentDir + "\\" +bottomPathCat
        if os.path.exists(currentDir) == False:
            os.makedirs(currentDir)
            print("Directory ",bottomPathCat," created in :\n",currentDir)
        else:
            pass

        


        #print(currentDir)
        

        with open(currentDir + "\grimoireJson.json","a") as jsonFile:
            json.dump(jsonDict,jsonFile,indent=4)
        #print(jsonDict)
        
    def findLoreEntryObjects(self,soup):
        loreSections = []
        #print(url)
        url = self.url
        url = url.replace("https://db.destinytracker.com/d1/grimoire/","")
        urlTuple = url.split("/")
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
            self.saveJson(data,urlTuple)
            #sys.exit()
            
        # maincontent = soup.find("div",class_="panel panel-default clearfix grimoire-card")
        #list1 = str(maincontent).split("</a>")
        #print(maincontent)
        #for i in list1:
         #   print(i)
        #print(list1[0])

urlList = [
    "https://db.destinytracker.com/d1/grimoire/guardian/classes",
    "https://db.destinytracker.com/d1/grimoire/guardian/races",
    "https://db.destinytracker.com/d1/grimoire/guardian/ghost",
    "https://db.destinytracker.com/d1/grimoire/guardian/sub-classes",
    "https://db.destinytracker.com/d1/grimoire/guardian/melee-abilities",
    "https://db.destinytracker.com/d1/grimoire/guardian/grenade-abilities",
    "https://db.destinytracker.com/d1/grimoire/guardian/movement-modes",
    "https://db.destinytracker.com/d1/grimoire/guardian/super-abilities",
    "https://db.destinytracker.com/d1/grimoire/inventory/primary-weapons",
    "https://db.destinytracker.com/d1/grimoire/inventory/special-weapons",
    "https://db.destinytracker.com/d1/grimoire/inventory/heavy-weapons",
    "https://db.destinytracker.com/d1/grimoire/inventory/damage-types",
    "https://db.destinytracker.com/d1/grimoire/inventory/guardian-vehicles",
    "https://db.destinytracker.com/d1/grimoire/inventory/economy",
    "https://db.destinytracker.com/d1/grimoire/allies/the-traveler",
    "https://db.destinytracker.com/d1/grimoire/allies/tower-allies",
    "https://db.destinytracker.com/d1/grimoire/allies/city-factions",
    "https://db.destinytracker.com/d1/grimoire/allies/the-exo-stranger",
    "https://db.destinytracker.com/d1/grimoire/allies/the-queen",
    "https://db.destinytracker.com/d1/grimoire/allies/rasputin",
    "https://db.destinytracker.com/d1/grimoire/allies/osiris",
    "https://db.destinytracker.com/d1/grimoire/allies/legends-mysteries",
    "https://db.destinytracker.com/d1/grimoire/allies/iron-lords",
    "https://db.destinytracker.com/d1/grimoire/enemies/fallen",
    "https://db.destinytracker.com/d1/grimoire/enemies/fallen-arsenal",
    "https://db.destinytracker.com/d1/grimoire/enemies/fallen-leadership",
    "https://db.destinytracker.com/d1/grimoire/enemies/fallen-hunted",
    "https://db.destinytracker.com/d1/grimoire/enemies/hive",
    "https://db.destinytracker.com/d1/grimoire/enemies/hive-arsenal",
    "https://db.destinytracker.com/d1/grimoire/enemies/exalted-hive",
    "https://db.destinytracker.com/d1/grimoire/enemies/vex",
    "https://db.destinytracker.com/d1/grimoire/enemies/vex-arsenal",
    "https://db.destinytracker.com/d1/grimoire/enemies/vex-axis-minds",
    "https://db.destinytracker.com/d1/grimoire/enemies/cabal",
    "https://db.destinytracker.com/d1/grimoire/enemies/cabal-arsenal",
    "https://db.destinytracker.com/d1/grimoire/enemies/cabal-command",
    "https://db.destinytracker.com/d1/grimoire/enemies/darkness",
    "https://db.destinytracker.com/d1/grimoire/enemies/books-of-sorrow",
    "https://db.destinytracker.com/d1/grimoire/enemies/the-taken",
    "https://db.destinytracker.com/d1/grimoire/enemies/siva",
    "https://db.destinytracker.com/d1/grimoire/places/mercury",
    "https://db.destinytracker.com/d1/grimoire/places/venus",
    "https://db.destinytracker.com/d1/grimoire/places/earth",
    "https://db.destinytracker.com/d1/grimoire/places/the-city",
    "https://db.destinytracker.com/d1/grimoire/places/moon",
    "https://db.destinytracker.com/d1/grimoire/places/mars",
    "https://db.destinytracker.com/d1/grimoire/places/the-asteroid-belt",
    "https://db.destinytracker.com/d1/grimoire/places/jupiter",
    "https://db.destinytracker.com/d1/grimoire/places/saturn",
    "https://db.destinytracker.com/d1/grimoire/activities/story-earth-old-russia",
    "https://db.destinytracker.com/d1/grimoire/activities/story-moon-ocean-of-storms",
    "https://db.destinytracker.com/d1/grimoire/activities/story-venus-ishtar-sink",
    "https://db.destinytracker.com/d1/grimoire/activities/story-mars-meridian-bay",
    "https://db.destinytracker.com/d1/grimoire/activities/the-dark-below",
    "https://db.destinytracker.com/d1/grimoire/activities/house-of-wolves",
    "https://db.destinytracker.com/d1/grimoire/activities/the-taken-king",
    "https://db.destinytracker.com/d1/grimoire/activities/strikes",
    "https://db.destinytracker.com/d1/grimoire/activities/raids",
    "https://db.destinytracker.com/d1/grimoire/activities/crucible-playlists",
    "https://db.destinytracker.com/d1/grimoire/activities/crucible-arenas",
    "https://db.destinytracker.com/d1/grimoire/activities/other-activities",
    "https://db.destinytracker.com/d1/grimoire/activities/rise-of-iron"
]

for link in urlList:
    grimoire = grimoireScrape(link)
    grimoire.makeSoup()


print("DONE!")