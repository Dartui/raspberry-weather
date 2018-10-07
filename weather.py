import xml.etree.ElementTree as XML
import requests
import os

class Weather:
    def __init__(self, lat, lng):
        self.__lat = lat
        self.__lng = lng

        self.__data = self.__getApiData()

    def getTime(self):
        return self.__data['time']

    def getIcon(self):
        return self.__data['icon']

    def getTemperatureIcon(self):
        return self.__data['temperature']['icon']

    def getTemperatureValue(self):
        return self.__data['temperature']['value']

    def getTemperatureUnit(self):
        return self.__data['temperature']['unit']

    def getPressureValue(self):
        return self.__data['pressure']['value']

    def getPressureUnit(self):
        return self.__data['pressure']['unit']

    def getWindIcon(self):
        return self.__data['wind']['icon']

    def getWindDirection(self):
        return self.__data['wind']['direction']

    def getWindSpeed(self):
        return self.__data['wind']['speed']

    def __getApiData(self):
        url = 'https://api.met.no/weatherapi/locationforecast/1.9/?lat=%f&lon=%f' % (self.__lat, self.__lng)
        response = requests.get(url)
        xml = XML.fromstring(response.content)

        time = xml.find('product/time')
        temperature = xml.find('product/time/location/temperature')
        pressure = xml.find('product/time/location/pressure')
        windDirection = xml.find('product/time/location/windDirection')
        windSpeed = xml.find('product/time/location/windSpeed')

        return {
            'time': time.get('from'),
            'icon': self.__weatherIcon(xml),
            'temperature': {
                'icon': self.__temperatureIcon(temperature.get('value')),
                'value': temperature.get('value'),
                'unit': temperature.get('unit'),
            },
            'pressure': {
                'value': pressure.get('value'),
                'unit': pressure.get('unit'),
            },
            'wind': {
                'icon': self.__windIcon(windDirection.get('name')),
                'direction': windDirection.get('name'),
                'speed': self.__windSpeed(windSpeed.get('mps')),
            },
        }

    def __weatherIcon(self, xml):
        iconId = xml.find('product')[1].find('location/symbol').get('number')
        path = self.__getIconPath('weather/%s.bmp' % (iconId))

        if (os.path.isfile(path)):
            return path

        return self.__getIconPath('unknown.bmp')

    def __temperatureIcon(self, temperature):
        temperature = float(temperature)
        
        if (temperature < 0):
            return self.__getIconPath('temperature/cold.bmp')

        if (temperature > 20):
            return self.__getIconPath('temperature/warm.bmp')

        return self.__getIconPath('temperature/normal.bmp')


    def __windIcon(self, direction):
        return self.__getIconPath('wind/%s.bmp' % (direction))

    def __windSpeed(self, speed):
        speed = float(speed) * 3.6

        return "{0:.1f}".format(speed)

    def __getIconPath(self, path):
        root = os.path.dirname(os.path.realpath(__file__))

        return '%s/icons/%s' % (root, path)