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
        self.smallFont = ImageFont.truetype('./fonts/FreeMonoBold.ttf', 24)
        self.largeFont = ImageFont.truetype('./fonts/FreeMonoBold.ttf', 36)

        self.initEpd()

    def initEpd(self):
        self.epd = epd.EPD()
        self.epd.init(self.epd.lut_full_update)
        self.epd.clear_frame_memory(0xFF)

    def screenDimension(self):
        return (epd.EPD_WIDTH, epd.EPD_HEIGHT)

    def generate(self):
        image = Image.new('1', self.screenDimension(), 255);
        draw = ImageDraw.Draw(image)

        # background
        draw.line((100, 0, 100, 200), fill = 0)
        draw.line((101, 0, 101, 200), fill = 0)
        draw.line((0, 100, 200, 100), fill = 0)
        draw.line((0, 101, 200, 101), fill = 0)

        # icon
        draw.text((18, 70), time.strftime('%H:%M'), font = self.smallFont, fill = 0)

        weatherImage = Image.open(self.weather.getIcon())
        image.paste(weatherImage, (18, 3))

        # temperature
        draw.text((123, 70), self.weather.getTemperatureValue(), font = self.smallFont, fill = 0)

        temperatureImage = Image.open(self.weather.getTemperatureIcon())
        image.paste(temperatureImage, (126, 3))

        # wind
        draw.text((20, 171), self.weather.getWindSpeed(), font = self.smallFont, fill = 0)

        windImage = Image.open(self.weather.getWindIcon())
        image.paste(windImage, (18, 104))

        # pressure
        draw.text((110, 171), self.weather.getPressureValue(), font = self.smallFont, fill = 0)

        draw.text((120, 120), self.weather.getPressureUnit(), font = self.largeFont, fill = 0)

        return image

    def draw(self):
        image = self.generate()

        self.drawImage(image)
        self.drawImage(image)

    def drawImage(self, image, x = 0, y = 0):
        self.epd.set_frame_memory(image, x, y)
        self.epd.display_frame()

main = Main()
main.draw()