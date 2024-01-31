#! /usr/bin/python 
import sys
import os
import getopt
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epaper/pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epaper/lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import date
import panchangam
import json

screen_on = False

class EPanchangamDisplay:

    def __init__(self, argv):

        try:
           logging.info("Initializing epd...")
           self.epd = epd7in5_V2.EPD()
           self.epd.init()
           self.get_user_option(argv)

        except IOError as e:
           logging.info(e)
           exit()


    def get_user_option(self, argv):

        try:
            opts, args = getopt.getopt(argv, "hdc", ["display","clear"])

        except getopt.GetoptError:
            print('cmd.py display | clear')
            sys.exit(2)

        for opt, arg in opts:
             if opt in ('-h', '--help'):
                 print("cmd.py [-d | --display] | [-c | --clear]")
                 sys.exit()
             elif opt in ('-d', '--display'):
                  self.display_current_date_details()
             elif opt in ('-c', '--clear'):
                 self.clear_screen()
             else:
                 print("cmd.py  [-d | --display] | [-c | --clear]")

    def display_current_date_details(self):

        try:

            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            detail_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

            title_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 96)
            subtitle_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)

            self.epd.init_fast()
            Himage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)

            today = date.today()
            json_data = json.loads(panchangam.get_details())

            date_english = json_data['date_text']
            date_tamil = json_data["date_tamil"]
            tamil_date_details = json_data["tamil_date_details"]
            sunrise = json_data["Sunrise"]
            sunset = json_data["Sunset"]
            tithi = json_data["Tithi"]
            nakshathram = json_data["Nakshathram"]
            rahu_kalam = json_data["Rahu Kalam"]
            gulikai_kalam = json_data["Gulikai Kalam"]
            yamaganda = json_data["Yamaganda"]
            last_refresh = json_data["last_refresh"]

            draw.text((10, 0), date_english, font=title_font, fill=0)
            draw.text((10, 150), date_tamil, font=subtitle_font, fill=0)
            draw.text((10, 200), tamil_date_details, font=subtitle_font, fill=0)
            draw.text((10,250), f"Sunrise: {sunrise}", font=detail_font, fill=0)
            draw.text((10,280), f"Sunset : {sunset}", font=detail_font, fill=0)
            draw.text((10,310), f"Tithi  : {tithi}", font=detail_font, fill=0)
            draw.text((10,340), f"Nakshathram: {nakshathram}", font=detail_font, fill=0)
            draw.text((450,250), f"Rahu: {rahu_kalam}", font=detail_font, fill=0)
            draw.text((450,280), f"Guli: {gulikai_kalam}", font=detail_font, fill=0)
            draw.text((450,310), f"Yama: {yamaganda}", font=detail_font, fill=0)
            draw.text((10, 400), f"Last refreshed at {last_refresh}", font=detail_font, fill=0) 

            self.epd.display(self.epd.getbuffer(Himage))


            time.sleep(2)

            self.epd.sleep()

            self.screen_on = True

        except IOError as e:
            logging.info(e)

    def clear_screen(self):

        logging.info("Clear...")
        self.epd.init()
        self.epd.Clear()

        logging.info("Goto Sleep...")
        self.epd.sleep()
        self.screen_on = False

    def main_process(self):
        user_selection = self.get_user_option(argv)


def setup():

    logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    setup()
    argv = sys.argv[1:]
    epdisplay = EPanchangamDisplay(argv)
