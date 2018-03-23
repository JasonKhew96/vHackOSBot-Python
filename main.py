"""Main entry point"""
import logging
from distutils.version import StrictVersion
from random import uniform
from time import sleep, time

import requests
from lxml import html

from network import Network
from vhackosapi import VHackOSAPI

VERSION = "0.0.0.7"  # major.minor.build.revision
APP_VER = "1.40"


def getappver():
    """Get vHackOS version from play store."""
    url = 'https://play.google.com/store/apps/details?id=cc.vhack.vhackxtmobile&hl=en'
    response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3378.0 Safari/537.36'})
    html_content = html.fromstring(response.content)
    try:
        version = html_content.xpath('//span[@class="htlgb"]')[3].text.strip()
    except IndexError:
        print("SOMETHING'S HAPPENING!!!")
        exit()
    return version


def mainloop():
    """Main bot loop."""
    network = Network()
    api = VHackOSAPI(network)
    cd_timer = 0
    while True:
        api.update()
        api.attack()
        api.update()
        if time() - cd_timer > 600:  # 10 minutes
            api.withdraw()
            api.update()
            api.collectmining()
            api.update()
            cd_timer = time()
        api.upgradesingle()
        api.update()
        api.printuserinfo()
        mseconds = uniform(60.0, 600.0)
        logging.info('Sleep %i second(s)', round(mseconds))
        sleep(mseconds)


def main():
    """Main entry point."""
    try:
        log_format = "[%(asctime)s][%(module)s][%(funcName)8s][%(levelname)8s] %(message)s"
        # FORMATTER = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%s")

        logging.basicConfig(format=log_format, level=logging.INFO)
        logger = logging.getLogger(__name__)

        # fh = logging.FileHandler('debug.log')
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warn('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
        logger.info('vHackOS-Bot: %s', VERSION)

        newappver = getappver()
        if StrictVersion(newappver) > StrictVersion(APP_VER):
            logger.error(
                '\nNew vHackOS-app detected: %s\nSupported version: %s',
                newappver, APP_VER)
            exit()

        logger.info('vHackOS-app: %s', newappver)
        sleep(10)
        mainloop()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted')
        exit()


if __name__ == '__main__':
    main()
