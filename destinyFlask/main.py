from flask import Flask,render_template,request
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "you are at the index"

@app.route("/home")
def cardHome():
    return render_template("cardHome.html")







@app.route("/about")
def about():
    if request.method == "POST":
        print(request.form)
        print('hi')
    return render_template("about.html")

@app.route("/aboutButton")
def test():
    print("hello")
    
    
    return render_template("about.html")

@app.route("/card")
def card():
    return render_template("card.html",cardImgPath = "https://www.bungie.net/common/destiny_content/grimoire/hr_images/107010_25097097211250951c97d4a1f97ca0a5.jpg",subStr = "NAN",cardLore = "The legendary Warminds stood watch over our Golden Age colonies: vigilant intelligences stretched across thousands of warsats and hardened installations. When the Collapse struck, the great Warminds fought and died. Rasputin fell with them.\n\n\nOr so history believed. But centuries of explorers' tales spoke of a surviving, elusive Warmind  - a myth substantiated when Guardians exploring the old Cosmodrome made positive contact with Rasputin. A single Warmind still lives, diminished but unbroken.\n\n\nThreatened by a convergence of Fallen and Hive forces, Rasputin exploited the reactivation of the Cosmodrome's Terrestrial-space array to extend itself across the inner solar system. The Guardian Vanguard hoped that Rasputin might make a powerful ally, capable of mapping and reviving Golden Age military assets and recruiting them for the City's defense. But Rasputin has proven recalcitrant and high-handed, unresponsive to the City's outreach.\n\n\nWe cannot characterize Rasputin's strategic objectives and capabilities, cannot define its physical or computational architecture, cannot ascertain its disposition with regard to the City, and cannot be sure it retains memory of events before the Collapse. Perhaps what remains is only an autonomic shell, defending itself by reflex. Or perhaps Rasputin's objectives have changed, transformed by some vital information it obtained during those dark days.\n\n\nRasputin's survival opens the possibility that other Warminds may be revivable, opening weapons systems to aid in City defenses. The Vanguard and the Consensus hope that continued outreach towards Rasputin will develop into a strategic alliance.")
    
    
if __name__ == "__main__":
    app.run(debug=True)