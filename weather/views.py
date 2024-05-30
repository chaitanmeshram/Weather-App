from django.shortcuts import render
import json
import urllib.request
from urllib.parse import quote

def index(request):
    data = {}
    city = ''

    if request.method == "POST":
        city = request.POST['city']

        try:
            # Ensure the city name is URL-encoded to handle spaces and special characters
            city_encoded = quote(city)
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid=fe44a1aa398ab4ff31e1fec97b09ca9f'
            res = urllib.request.urlopen(url).read()
            json_data = json.loads(res)

            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": f"{json_data['coord']['lon']} {json_data['coord']['lat']}",
                "temp": str(round((json_data['main']['temp'] ) - 273.15, 2))  + ' C',
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data['error'] = 'City not found !!'
            else:
                data['error'] = 'An error occurred. Please try again later.'
        except urllib.error.URLError:
            data['error'] = 'Network issue. Please try again later.'
        except Exception as e:
            data['error'] = 'An unexpected error occurred. Please try again later.'


    context = {
        'data': data,
        'city': city,
    }
    
    return render(request, 'index.html', context)


