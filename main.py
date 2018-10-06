from weather import Weather
import lib.epd1in54 as epd
import Image
import ImageDraw
import ImageFont
import os
import time

class Main:
    def __init__(self):
        self.weather = Weather(54.456417, 18.535194).getDataFromApi()
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)

        self.initEpd()

    def initEpd(self):
        self.epd = epd.EPD()
        self.epd.init(self.epd.lut_full_update)
        self.epd.clear_frame_memory(0xFF)

    def screenDimension(self):
        return (epd.EPD_WIDTH, epd.EPD_HEIGHT)

    def drawBackground(self):
        image = Image.new('1', self.screenDimension(), 255)

        draw = ImageDraw.Draw(image)


        self.drawImage(image)
        self.drawImage(image)

    def writeData(self):
        image = Image.new('1', self.screenDimension(), 255);
        draw = ImageDraw.Draw(image)

        # background
        draw.line((100, 0, 100, 200), fill = 0)
        draw.line((101, 0, 101, 200), fill = 0)
        draw.line((0, 100, 200, 100), fill = 0)
        draw.line((0, 101, 200, 101), fill = 0)

        # icon
        draw.text((20, 70), time.strftime('%H:%M'), font = self.font, fill = 0)
        weatherImage = Image.open(self.weatherIcon())
        image.paste(weatherImage, (18, 3))

        # temperature
        draw.text((123, 70), self.weather['temperature']['value'], font = self.font, fill = 0)
        temperatureImage = Image.open(self.temperatureIcon())
        image.paste(temperatureImage, (126, 3))

        # wind
        draw.text((33, 171), self.windSpeed(), font = self.font, fill = 0)
        windImage = Image.open(self.windIcon())
        image.paste(windImage, (18, 104))

        # pressure
        draw.text((110, 171), self.weather['pressure']['value'], font = self.font, fill = 0)
        pressureFont = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 36)
        draw.text((120, 120), self.weather['pressure']['unit'], font = pressureFont, fill = 0)

        self.drawImage(image)
        self.drawImage(image)

    def weatherIcon(self):
        iconId = self.weather['icon']
        path = 'icons/weather/%s.bmp' % (iconId)

        if (os.path.isfile(path)):
            return path

        return 'icons/unknown.bmp'


    def temperatureIcon(self):
        temperature = float(self.weather['temperature']['value'])

        if (temperature < 0):
            return 'icons/temperature/cold.bmp'

        if (temperature > 20):
            return 'icons/temperature/warm.bmp'

        return 'icons/temperature/normal.bmp'

    def windIcon(self):
        windDirection = self.weather['wind']['direction']

        return 'icons/wind/%s.bmp' % (windDirection)

    def windSpeed(self):
        speed = float(self.weather['wind']['speed']) * 3.6

        return "{0:.1f}".format(speed)

    def drawImage(self, image, x = 0, y = 0):
        self.epd.set_frame_memory(image, x, y)
        self.epd.display_frame()

    def clearScreen(self):
        image = Image.new('1', self.screenDimension(), 255)

        self.drawImage(image)

main = Main()
main.writeData()