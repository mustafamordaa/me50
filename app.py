import requests
from flask import Flask, render_template, session, request

app = Flask(__name__)


@app.route("/")
def main():

	#REQUEST THE API OF SUMMURY FOR GLOBAL STATUS COVID-19
	res = requests.get("https://api.covid19api.com/summary")
	#REQUEST THE API OF LOCATION DATA
	ip_res = requests.get("https://freegeoip.app/json/")
	#TEST THE CONNECTION
	if res.status_code != 200 or ip_res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
	#STORE THE INFORMATION IN A VARIABLE   
	data = res.json()
	geoIp = ip_res.json()
    #GETTING THE INFORMATION FROM COVED-19 API DATA
	allCases = data["Global"]["TotalConfirmed"]
	allDeaths = data["Global"]["TotalDeaths"]
	allRecover = data["Global"]["TotalRecovered"]
	newCases = data["Global"]["NewConfirmed"]
	newDeaths = data["Global"]["NewDeaths"]
	newRecover = data["Global"]["NewRecovered"]
	#GETTING THE COUNTRY NAME FRM THE LOCATIIN API DATA
	location = geoIp["country_name"]
	#INSERT THE COUNTRY NAME TO THE API URL AND GETTING THE INFORMATION ABOUT COVID-19 STATUS
	myRes = requests.get(f"https://api.covid19api.com/live/country/{ location }/status/confirmed")
	myCasesData = myRes.json()
	length = len(myCasesData)
	lastData = myCasesData[length - 1]
	myConfrim = lastData["Confirmed"]
	myDeaths = lastData["Deaths"]
	myRecover = lastData["Recovered"]
	
		
	return render_template("index.html", allCases = allCases, allDeaths = allDeaths, allRecover = allRecover, newCases = newCases, newDeaths = newDeaths, newRecover = newRecover, location = location, myConfrim = myConfrim, myDeaths = myDeaths, myRecover = myRecover)
@app.route("/search",methods=["POST"])
def index():
	
	if request.method == "POST":
		#GETTING THE CHOOSEN COUNTRY FROM THE FORM IN THE HTML PAGE
		country = request.form.get("country")
		#INSERT THE COUNTRY NAME TO THE API URL AND GETTING THE INFORMATION ABOUT COVID-19 STATUS
		res_country = requests.get(f"https://api.covid19api.com/live/country/{ country }/status/confirmed")
		countryData = res_country.json()
		length = len(countryData)
		lastData = countryData[length - 1]
		contConfrim = lastData["Confirmed"]
		contDeaths = lastData["Deaths"]
		contRecover = lastData["Recovered"]
		
		return render_template("search.html", country = country, contConfrim = contConfrim, contDeaths = contDeaths, contRecover = contRecover)


if __name__ == "__main__":
    main()
