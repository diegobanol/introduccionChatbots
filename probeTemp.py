import pyowm


owm = pyowm.OWM('4bf4d2493999fbf6bf563d1f337f5fd8')
observation = owm.weather_at_place('London,GB')
w = observation.get_weather()
print(w.get_temperature('celsius'))