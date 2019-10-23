from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    
    
    
    return HttpResponse("you are at the destiny app index")

def cardHome(request):
    return HttpResponse("you are at the card homepage")

def card(request, cardID):
    return HttpResponse("you are at card ID: %s" % cardID)
    