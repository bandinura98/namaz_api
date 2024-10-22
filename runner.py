from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from praytimes import PrayTimes
import json
import os
import math

app = Flask(__name__)

# Şehirlerin listesini JSON dosyasından yükle
with open('cities.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

# Koordinatlara en yakın şehri bulma fonksiyonu
def get_nearest_city(lat, lon):
    min_distance = float('inf')
    nearest_city = None
    for city in cities:
        distance = haversine(lat, lon, city['lat'], city['lon'])
        if distance < min_distance:
            min_distance = distance
            nearest_city = city
    return nearest_city

# Haversine formülü ile iki koordinat arasındaki mesafeyi hesaplama
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Dünya'nın yarıçapı (km)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Namaz vakitlerini hesaplama fonksiyonu
def calculate_prayer_times(lat, lon, date, timezone_offset, method):
    pt = PrayTimes(method)
    times = pt.getTimes(date, (lat, lon), timezone_offset / 60)
    return {
        'fajr': times['fajr'],
        'sunrise': times['sunrise'],
        'dhuhr': times['dhuhr'],
        'asr': times['asr'],
        'maghrib': times['maghrib'],
        'isha': times['isha']
    }

@app.route('/api/timesFromCoordinates', methods=['GET'])
def times_from_coordinates():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    days = request.args.get('days', default=1, type=int)
    timezone_offset = request.args.get('timezoneOffset', default=0, type=int)
    calculation_method = request.args.get('calculationMethod', default='Turkey')

    if lat is None or lon is None:
        return jsonify({'error': 'lat ve lon parametreleri gereklidir.'}), 400

    if days < 1 or days > 1000:
        return jsonify({'error': 'days parametresi [1, 1000] aralığında olmalıdır.'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Geçersiz tarih formatı. YYYY-AA-GG olmalıdır.'}), 400

    # Koordinatlara en yakın şehri bul
    nearest_city = get_nearest_city(lat, lon)

    # Eğer şehir için önceden hesaplanmış veriler varsa, onları kullan
    prayer_times_list = []
    data_available = False
    city_data_path = f'prayer_times/{nearest_city["il_adi"]}.json'
    if os.path.exists(city_data_path):
        data_available = True
        with open(city_data_path, 'r', encoding='utf-8') as f:
            city_prayer_times = json.load(f)
        date_indices = [(date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        for date_index in date_indices:
            times = next((item for item in city_prayer_times if item['date'] == date_index), None)
            if times:
                prayer_times_list.append({'date': date_index, 'times': times})
            else:
                data_available = False
                break

    # Eğer veri yoksa veya eksikse, hesaplama yap
    if not data_available:
        for i in range(days):
            current_date = date + timedelta(days=i)
            times = calculate_prayer_times(lat, lon, current_date, timezone_offset, calculation_method)
            prayer_times_list.append({'date': current_date.strftime('%Y-%m-%d'), 'times': times})

    response = {
        'coordinates': {'latitude': lat, 'longitude': lon},
        'nearest_city': nearest_city['il_adi'],
        'calculation_method': calculation_method,
        'prayer_times': prayer_times_list
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
