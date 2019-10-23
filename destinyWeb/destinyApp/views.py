from django.shortcuts import render
from django.http import HttpResponse
import json,os

from pprint import pprint
# Create your views here.

def index(request):
    jFile = "/Destiny1Grimoire/allies/rasputin"

    cwd = os.getcwd()
    jsonData = []
    with open(str(cwd+jFile + "/grimoireJson.json")) as jsonFile:
        data = json.load(jsonFile)
       
    pprint(data["name"])
            #test = input()
    return HttpResponse("you are at the destiny app index")

def cardHome(request):
    return HttpResponse("you are at the card homepage")

def card(request, cardID):
    return HttpResponse("you are at card ID: %s" % cardID)
    