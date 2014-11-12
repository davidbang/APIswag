from flask import Flask,request,url_for,redirect,render_template
import json, urllib2

app=Flask(__name__)

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
    if (d['query']['results'] == "null"):
        flash ("Invalid Location")
        return redirect ("/")
    d1 = d['query']['results']['channel']
    loadstr= "hi"
    title =  d1['description']
    location = d1['item']['title'] + " located at latitude:" + d1 ['item']['lat'] + " longitude:" + d1 ['item']['long']
    date = d1['item']['condition']['date']
    return render_template ("weather.html", title = title, location = location, date = date)
            
    
if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
