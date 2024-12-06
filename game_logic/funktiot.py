from mysql.connector import connect
from geopy.distance import geodesic
import random
import time

# Database connection
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

def player_exists(name):
    sql = "SELECT COUNT(screen_name) FROM game WHERE screen_name = %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0

def add_player(name):
    if not player_exists(name):
        count = get_count_of_players()
        player_id = count + 1
        sql = """
            INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name, points)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = [player_id, 0, 10000, 'EFHK', name, 0]
        cursor = yhteys.cursor()
        cursor.execute(sql, values)
        yhteys.commit()
        cursor.close()

def get_count_of_players():
    sql = "SELECT COUNT(id) FROM game;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def get_points(name):
    sql = "SELECT points FROM game WHERE screen_name = %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]

def get_location(name):
    sql = """
        SELECT country.name, airport.name, airport.id 
        FROM country 
        INNER JOIN airport ON country.iso_country = airport.iso_country 
        INNER JOIN game ON game.location = airport.gps_code 
        WHERE game.screen_name = %s
    """
    cursor = yhteys.cursor()
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        raise ValueError(f"Player '{name}' does not have a valid location in the database.")
    
    return result
def country_code(name):
    sql = """
        SELECT country.iso_country
        FROM country 
        INNER JOIN airport ON airport.iso_country = country.iso_country 
        INNER JOIN game ON game.location = airport.gps_code
        WHERE game.screen_name = %s
    """
    cursor = yhteys.cursor()
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        return result[0]  # Return the country code
    else:
        raise ValueError(f"Country code not found for player '{name}'")


def get_airport_list(country_code):
    sql = """
        SELECT airport.id, airport.name 
        FROM airport
        INNER JOIN country ON country.iso_country = airport.iso_country
        WHERE country.iso_country = %s AND airport.type = "large_airport";
    """
    cursor = yhteys.cursor()
    cursor.execute(sql, (country_code,))
    result = cursor.fetchall()
    cursor.close()
    return result
def get_airport_list_with_coords(country_code):
    sql = """
        SELECT airport.id, airport.name, latitude_deg, longitude_deg 
        FROM airport
        INNER JOIN country ON country.iso_country = airport.iso_country
        WHERE country.iso_country = %s AND airport.type = "large_airport";
    """
    cursor = yhteys.cursor()
    cursor.execute(sql, (country_code,))
    result = cursor.fetchall()
    cursor.close()
    return [{"id": a[0], "name": a[1], "coords": (a[2], a[3])} for a in result]


def default_settings(name):
    sql = "UPDATE game SET points = 0, co2_consumed = 0, location = 'EFHK' WHERE screen_name = %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (name,))
    yhteys.commit()
    cursor.close()

def get_airport_coordinates(airport_name):
    sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE name = %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (airport_name,))
    coords = cursor.fetchone()
    cursor.close()
    return coords
