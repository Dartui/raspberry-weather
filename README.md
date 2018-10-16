# Raspberry Pi Weather for Waveshare 1.54" e-Paper Screen

Small application written in Python 2 which displays basic forecast from API on e-Paper screen, including:

- weather type icon (sun, cloudy, rain, snow, etc)
- temperature (Celcius unit)
- wind direction icon
- wind speed (km/h unit)
- pressure (hPa unit)
- time of forecast

## Installation

1. Follow this two great tutorials about installing required packages on Raspberry Pi:
   - https://www.waveshare.com/wiki/1.54inch_e-Paper_Module#Working_with_Raspberry_Pi
   - https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi

2. Install git (optional)
```sh
sudo apt-get install git
```

3. Clone this repository
```sh
git clone https://github.com/Dartui/raspberry-weather.git
```

4. Change latitude and longitude in main.py
```python
class Main:
    def __init__(self):
        self.weather = Weather(latitude, longitude)
        
        ...
```

5. Run script
```sh
cd raspberry-weather
python main.py
```

## Automatic screen updates

To automate screen updates you should add cron job to run script every hour (because of API limitations). crontab record should looks like this:

```
0 * * * * python /home/pi/raspberry-weather/main.py 2>&1
```

You can also run script on Raspberry PI startup. Because of delayed time update (about 10-15 seconds from boot) crontab record should looks like this:

```
@reboot sleep 20 && python /home/pi/raspberry-weather/main.py 2>&1
```

## Forecast API

Forecast is getting from https://api.met.no/ free API. It is updated every hour.

## Todo

- add photos
- possibility of changing current location (from CLI parameters?)
- text position (left/right) based on text length
- more weather type icons
- switch between sun and moon icon based on sunrise and sunset
- add different unit handling
- code refactorization
