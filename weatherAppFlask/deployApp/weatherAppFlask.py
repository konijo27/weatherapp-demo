import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '743976'  # Replace 'your_secret_key' with a random secret key

def get_weather_data(city, api_key):
    url = (
        "https://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&appid="
        + api_key
        + "&units=metric"
    )
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return {}

    json = response.json()

    description = json.get("weather")[0].get("description")
    feels_like = json.get("main").get("feels_like")
    temp_min = json.get("main").get("temp_min")
    temp_max = json.get("main").get("temp_max")

    return {
        "description": description,
        "temp_max": temp_max,
        "temp_min": temp_min,
        "feels_like": feels_like,
    }

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("start"))

@app.route("/api_key", methods=["GET", "POST"]) 
def api_key_input():
    if request.method == "POST":
        api_key = request.form["api_key"]
        session['api_key'] = api_key
        return redirect(url_for("weather"))
    return render_template("apiRequest.html")

@app.route("/start")
def start():
    session.clear()
    return redirect(url_for("api_key_input"))

@app.route("/set_api_key", methods=["POST"])
def set_api_key():
    api_key = request.form["api_key"]
    session['api_key'] = api_key
    return redirect(url_for("weather"))

@app.route("/weather", methods=["GET", "POST"])
def weather():
    if 'api_key' not in session:
        return redirect(url_for("api_key_input"))
    
    if request.method == "POST":
        city = request.form["city"]
        api_key = request.form["api_key"]
        weather_data = get_weather_data(city, api_key)
        if weather_data:
            return render_template("interface.html", city=city, weather=weather_data)
        else:
            flash("Error: City not found or invalid API key. Please try again.")
            return redirect(url_for("weather"))
    return render_template("interface.html")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    app.run(debug=True, host=args.host)
