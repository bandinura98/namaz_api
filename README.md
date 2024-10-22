# namaz_api
an api that calculates prayer times and gives them over the internet with requests

to make the calculation

flask, requests and PyPrayTimes libraries must be installed

pip install flask
pip install requests
pip install PyPrayTimes

update_namaz_times.py program calculates prayer times and saves them in prayer_times in a city-by-city format
to calculate the number of days to be calculated

start_date = datetime.now()
end_date = start_date + timedelta(days=3650)
you can edit this code

runner.py program starts serving the api from localhost on port 5000

an example request is shown below:

http://127.0.0.1:5000/api/timesFromCoordinates?lat=39.91987&lng=32.85427&timezoneOffset=180



# namaz_api
 namaz vakitlerini hesaplayıp internet üzerinden requestler ile veren bir api
 hesaplamayı yapmak için

flask, requests ve PyPrayTimes kütüphanelerinin kurulu olması lazım

pip install flask
pip install requests
pip install PyPrayTimes


update_namaz_times.py programı namaz vakitlerini hesaplayıp prayer_timesin içine illere ayrılmış bir biçimde kaydeder
hesaplanacak gün sayısını hesaplamak için 
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3650)
bu kodu editleyebilirsiniz

runner.py programı localhost üzerinden 5000 portundan apiyi sunmaya başlatır

aşağıda örnek bir request gösterilmiştir: 

http://127.0.0.1:5000/api/timesFromCoordinates?lat=39.91987&lng=32.85427&timezoneOffset=180

