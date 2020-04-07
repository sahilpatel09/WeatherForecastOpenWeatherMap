from django.shortcuts import render
import requests
import datetime

# Create your views here.

def forcast(request):
    #daily data through API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=831f77dcd47accb0ad81ae949234638f'

    # city variable change it to change the data. For ex. New York
    city = 'Ahmedabad'
    city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types

    #daily weather data
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'temperature_max': city_weather['main']['temp_max'] ,
        'temperature_min':  city_weather['main']['temp_min']  ,
        'feelslike_weather': city_weather['main']['feels_like']

    }

    #forcasted weather data API
    v = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=831f77dcd47accb0ad81ae949234638f'
    a = v.format(city)
    #accessing the API json data
    full = requests.get(a).json()

    # today's date taking as int
    day = datetime.datetime.today()
    today_date = int(day.strftime('%d'))


    forcast_data_list = {} # dictionary to store json data

    #looping to get value and put it in the dictionary
    for c in range(0, full['cnt']):
        date_var1 = full['list'][c]['dt_txt']
        date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
        # print the json data and analyze the data coming to understand the structure. I couldn't find the better way
        # to process date
        if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
            # print(date_time_obj1.strftime('%d %a'))
            if int(date_time_obj1.strftime('%d')) == today_date+1:
                today_date += 1
            forcast_data_list[today_date] = {}
            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
            forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']

            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']

            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']

            today_date += 1
        else:
            pass
    #returning the context with all the data to the index.html
    context = {
        'weather':weather, 'forcast_data_list':forcast_data_list
    }

    return render(request, 'index.html', context)