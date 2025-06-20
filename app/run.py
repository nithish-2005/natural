from flask import Flask, render_template, request, jsonify
import requests
import smtplib
from email.message import EmailMessage
import pyttsx3
import random
from threading import Thread
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.flood_predictor import predict_flood_risk

app = Flask(__name__)

def send_email_alert(subject, body):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    recipient = "recipient_email@gmail.com"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
    except Exception as e:
        print("Email failed:", e)

def voice_alert(message):
from flask import Flask, render_template, request, jsonify
import requests
import smtplib
from email.message import EmailMessage
import pyttsx3
import random
from threading import Thread
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.flood_predictor import predict_flood_risk

app = Flask(__name__)

# Configuration
CONFIG = {
    'email': {
        'sender': 'your_email@gmail.com',
        'password': 'your_app_password',
        'recipient': 'recipient_email@gmail.com'
    },
    'openweathermap': {
        'api_key': 'your_openweathermap_api_key'
    },
    'criticals': {
        'temperature': 40,
        'humidity': 90,
        'uv_index': 8,
        'pressure_low': 980,
        'rain': 80,
        'earthquake_possibility': 0.7
    }
}

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = CONFIG['email']['sender']
    msg['To'] = CONFIG['email']['recipient']

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(CONFIG['email']['sender'], CONFIG['email']['password'])
            smtp.send_message(msg)
    except Exception as e:
        print("Email failed:", e)

def voice_alert(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude parameters'}), 400

    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={CONFIG["openweathermap"]["api_key"]}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast_data = [entry['main']['temp'] for entry in data['list'][:24]]
        current = data['list'][0]

        return jsonify({
            'location': f"{data['city']['name']}, {data['city']['country']}",
            'temperature': current['main']['temp'],
            'humidity': current['main']['humidity'],
            'wind_speed': current['wind']['speed'],
            'description': current['weather'][0]['description'],
            'forecast_data': forecast_data
        })
    except requests.exceptions.RequestException as e:
        # Generate random weather data for next 24 hours
        temperature_data = [round(random.uniform(15, 45), 1) for _ in range(24)]
        humidity_data = [round(random.uniform(30, 100), 1) for _ in range(24)]
        rain_data = [round(random.uniform(0, 100), 1) for _ in range(24)]
        uv_index_data = [round(random.uniform(0, 11), 1) for _ in range(24)]
        pressure_data = [round(random.uniform(950, 1050), 1) for _ in range(24)]
        earthquake_possibility_data = [round(random.uniform(0, 1), 2) for _ in range(24)]

        temperature = temperature_data[0]
        humidity = humidity_data[0]
        rain = rain_data[0]
        uv_index = uv_index_data[0]
        pressure = pressure_data[0]
        earthquake_possibility = earthquake_possibility_data[0]

        flood_risk = predict_flood_risk({'rain': rain, 'humidity': humidity})

        alerts = []

        for key, value in CONFIG['criticals'].items():
            if key == 'pressure_low':
                if pressure < value:
                    alerts.append(f"Low Pressure: {pressure} hPa")
            elif key == 'earthquake_possibility':
                if earthquake_possibility > value:
                    alerts.append(f"High Earthquake Possibility: {earthquake_possibility}")
            else:
                if key == 'temperature':
                    if temperature > value:
                        alerts.append(f"High Temperature: {temperature}°C")
                elif key == 'humidity':
                    if humidity > value:
                        alerts.append(f"High Humidity: {humidity}%")
                elif key == 'uv_index':
                    if uv_index > value:
                        alerts.append(f"Critical UV Index: {uv_index}")
                elif key == 'rain':
                    if rain > value:
                        alerts.append(f"Heavy Rainfall: {rain} mm")
                elif key == 'earthquake_possibility':
                    if earthquake_possibility > value:
                        alerts.append(f"High Earthquake Possibility: {earthquake_possibility}")

        if flood_risk == "High":
            alerts.append("High Flood Risk")

        def alert_if_critical():
            if alerts:
                alert_msg = "\n".join(alerts)
                send_email_alert("🚨 Weather Alert", alert_msg)
                voice_alert(alert_msg)

        Thread(target=alert_if_critical).start()

        return jsonify({
            'location': 'Simulated Location',
            'temperature': temperature,
            'humidity': humidity,
            'rain': rain,
            'uv_index': uv_index,
            'pressure': pressure,
            'earthquake_possibility': earthquake_possibility,
            'flood_risk': flood_risk,
            'alerts': alerts,
            'temperature_data': temperature_data,
            'humidity_data': humidity_data,
            'rain_data': rain_data,
            'uv_index_data': uv_index_data,
            'pressure_data': pressure_data,
            'earthquake_possibility_data': earthquake_possibility_data
        })

if __name__ == '__main__':
    app.run(debug=True)    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude parameters'}), 400

    api_key = 'your_openweathermap_api_key'
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast_data = [entry['main']['temp'] for entry in data['list'][:24]]
        current = data['list'][0]

        return jsonify({
            'location': f"{data['city']['name']}, {data['city']['country']}",
            'temperature': current['main']['temp'],
            'humidity': current['main']['humidity'],
            'wind_speed': current['wind']['speed'],
            'description': current['weather'][0]['description'],
            'forecast_data': forecast_data
        })
    except requests.exceptions.RequestException as e:
        # Generate random weather data for next 24 hours
        temperature_data = [round(random.uniform(15, 45), 1) for _ in range(24)]
        humidity_data = [round(random.uniform(30, 100), 1) for _ in range(24)]
        rain_data = [round(random.uniform(0, 100), 1) for _ in range(24)]
        uv_index_data = [round(random.uniform(0, 11), 1) for _ in range(24)]
        pressure_data = [round(random.uniform(950, 1050), 1) for _ in range(24)]
        earthquake_possibility_data = [round(random.uniform(0, 1), 2) for _ in range(24)]

        temperature = temperature_data[0]
        humidity = humidity_data[0]
        rain = rain_data[0]
        uv_index = uv_index_data[0]
        pressure = pressure_data[0]
        earthquake_possibility = earthquake_possibility_data[0]

        flood_risk = predict_flood_risk({'rain': rain, 'humidity': humidity})

        CRITICALS = {
            'temperature': 40,
            'humidity': 90,
            'uv_index': 8,
            'pressure_low': 980,
            'rain': 80,
            'earthquake_possibility': 0.7
        }

        alerts = []

        if temperature > CRITICALS['temperature']:
            alerts.append(f"High Temperature: {temperature}°C")
        if humidity > CRITICALS['humidity']:
            alerts.append(f"High Humidity: {humidity}%")
        if uv_index > CRITICALS['uv_index']:
            alerts.append(f"Critical UV Index: {uv_index}")
        if pressure < CRITICALS['pressure_low']:
            alerts.append(f"Low Pressure: {pressure} hPa")
        if rain > CRITICALS['rain']:
            alerts.append(f"Heavy Rainfall: {rain} mm")
        if flood_risk == "High":
            alerts.append("High Flood Risk")
        if earthquake_possibility > CRITICALS['earthquake_possibility']:
            alerts.append(f"High Earthquake Possibility: {earthquake_possibility}")

        def alert_if_critical():
            if alerts:
                alert_msg = "\n".join(alerts)
                send_email_alert("🚨 Weather Alert", alert_msg)
                voice_alert(alert_msg)

        Thread(target=alert_if_critical).start()

        return jsonify({
            'location': 'Simulated Location',
            'temperature': temperature,
            'humidity': humidity,
            'rain': rain,
            'uv_index': uv_index,
            'pressure': pressure,
            'earthquake_possibility': earthquake_possibility,
            'flood_risk': flood_risk,
            'alerts': alerts,
            'temperature_data': temperature_data,
            'humidity_data': humidity_data,
            'rain_data': rain_data,
            'uv_index_data': uv_index_data,
            'pressure_data': pressure_data,
            'earthquake_possibility_data': earthquake_possibility_data
        })

if __name__ == '__main__':
    app.run(debug=True)
