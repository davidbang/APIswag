from flask import Flask,request,url_for,redirect,render_template, flash
import json, urllib2

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def index():
    submit = request.args.get("submit")
    if (submit == "Submit"):
        city = request.args.get("city")
        if (city == ""):
            city = "NewYork"
        return redirect("/weather/" + city)
    return render_template("index.html")

@app.route("/weather")
@app.route("/weather/<loc>")
def t(loc= "newyork"):
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22" + loc + "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result)
    if (not d['query']['results']):
        flash ("Invalid Location")
        return redirect ("/")

    d1 = d['query']['results']['channel']
    loadstr= "hi"
    title =  d1['description']
    locationt = d1['item']['title'] 
    location = "Located at latitude: " + d1 ['item']['lat'] + " longitude: " + d1 ['item']['long']
    date = d1['item']['condition']['date']
    units = d1 ['units']
    temp = []
    
    temp.append('Current Temperature: ' +  d1['item'] ['condition']['temp'] + units ['temperature'])
    temp.append('Current Condition: ' + d1 ['item']['condition'] ['text'])
    
    forecast = []
    for r in d1['item'] ['forecast']:
        forecast.append ([r ['day'] + " " +  r ['date'],  "High: " + r ['high'] + units['temperature'],  "Low: "  + r ['low'] + units ['temperature'], "Condition: " + r ['text']] )

    sun = []
    sun.append("Sunrise: " + d1 ['astronomy'] ['sunrise'])
    sun.append("Sunset: " + d1 ['astronomy'] ['sunset'])
    
    wind= []
    wind.append("Wind:")
    wind.append("Wind Chill: " + d1 ['wind']['chill'] + units ['temperature'])
    wind.append("Direction: " + d1['wind']['chill'])
    wind.append("Speed:" + d1['wind']['speed'] + units ['speed'])
    
    tmp = d1 ['atmosphere']
    atmosphere = []
    atmosphere.append("Humidity: " + tmp ['humidity'] + " %")
    atmosphere.append("Pressure: " + tmp['pressure'] + units ['pressure'])
    atmosphere.append("Visibility: " + tmp ['visibility'] + units ['distance'])
    
    
    return render_template ("weather.html", title = title, locationt = locationt,location = location, date = date, temp = temp, forecast = forecast, sun = sun, wind = wind, atmosphere = atmosphere)
            
    
if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
