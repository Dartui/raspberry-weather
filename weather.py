import xml.etree.ElementTree as XML
import requests

class Weather:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def getDataFromApi(self):
        url = 'https://api.met.no/weatherapi/locationforecast/1.9/?lat=%f&lon=%f' % (self.lat, self.lng)
        response = requests.get(url)

        xml = XML.fromstring(response.content)
        time = xml.find('product/time')
        temperature = xml.find('product/time/location/temperature')
        pressure = xml.find('product/time/location/pressure')
        windDirection = xml.find('product/time/location/windDirection')
        windSpeed = xml.find('product/time/location/windSpeed')

        return {
            'time': time.get('from'),
            'temperature': {
                'value': temperature.get('value'),
                'unit': temperature.get('unit')
            },
            'pressure': {
                'value': pressure.get('value'),
                'unit': pressure.get('unit')
            },
            'wind': {
                'direction': windDirection.get('name'),
                'speed': windSpeed.get('mps')
            },
            'icon': self.getIconId(xml)
        }

    def getIconId(self, xml):
        return xml.find('product')[1].find('location/symbol').get('number')