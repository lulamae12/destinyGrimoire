from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    #http://127.0.0.1:8000/destinyApp/
    path("cardHome/",views.cardHome,name="cardHome"),
    #http://127.0.0.1:8000/destinyApp/cardHome/
    
    path("<int:cardID>/card/",views.card,name="card") #ex destinyApp/5/card where '5' is the card num
]
