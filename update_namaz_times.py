import json
from datetime import datetime, timedelta
from praytimes import PrayTimes

# Şehirlerin listesini JSON dosyasından yükle
with open('cities.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

def update_prayer_times():
    # Bugünden itibaren bir yıllık tarih aralığı oluştur
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3650)
    delta = timedelta(days=1)
    
    # Her şehir için namaz vakitlerini hesapla ve kaydet
    for city in cities:
        city_name = city['il_adi']
        latitude = city['lat']
        longitude = city['lon']
        
        prayer_times_list = []
        current_date = start_date
        
        while current_date <= end_date:
            times = calculate_prayer_times(latitude, longitude, current_date)
            times['date'] = current_date.strftime('%Y-%m-%d')
            prayer_times_list.append(times)
            current_date += delta
        
        # Şehir bazında JSON dosyasına kaydet
        with open(f'prayer_times/{city_name}.json', 'w', encoding='utf-8') as f:
            json.dump(prayer_times_list, f, ensure_ascii=False, indent=4)
        print(f"{city_name} için namaz vakitleri güncellendi.")

def calculate_prayer_times(lat, lon, date):
    pt = PrayTimes('Turkey')
    
    # Tarihi yıl, ay, gün olarak parçalıyoruz
    year = date.year
    month = date.month
    day = date.day

    # getTimes fonksiyonuna liste halinde tarih bilgilerini gönderiyoruz
    times = pt.getTimes([year, month, day], (lat, lon), +3)
    return {
        'fajr': times['fajr'],
        'sunrise': times['sunrise'],
        'dhuhr': times['dhuhr'],
        'asr': times['asr'],
        'maghrib': times['maghrib'],
        'isha': times['isha']
    }


if __name__ == '__main__':
    update_prayer_times()
