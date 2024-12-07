from flask import Flask, render_template, request, jsonify
from mysql.connector import connect
import requests
from geopy.distance import geodesic

yhteys = connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='omar',
    password='Amoury123',
    charset='utf8mb4',
    collation='utf8mb4_general_ci',
    autocommit=True
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/get_airports', methods=['GET'])
def get_airports():
    country_code = request.args.get('country_code')
    if not country_code:
        return jsonify({"error": "country_code parameter is required"}), 400

    airports = get_airport_list_with_coords()
    return jsonify(airports)


@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    api_key = "785d33b81003cb7269fa3658e8e8b85f"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    return jsonify(response.json())

def get_airport_list_with_coords():
    sql = """
        SELECT airport.id, airport.name, latitude_deg, longitude_deg 
        FROM airport
        INNER JOIN country ON country.iso_country = airport.iso_country
        WHERE airport.type = "large_airport";
    """
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return [{"id": a[0], "name": a[1], "coords": (a[2], a[3])} for a in result]

if __name__ == '__main__':
    app.run(debug=True)
