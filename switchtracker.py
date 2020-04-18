# webtracker.py
# to know when to purchase my beloved switch

# Created by Tyler Ressler, assisted by the RegEx Pro, Matthew W. Mancuso
# April 17, 2020

import re
import requests
import smtplib
import time
from collections import namedtuple

# default email server login
GMAIL_USER = 'myemail@gmail.com'
GMAIL_PASS = 'you-cant-have-my-password'

# init named tuples for email contacts and website search info
Contact = namedtuple('Contact', 'name email')
Website = namedtuple('Website', 'url site_name search_query description')

# responsible for emailing notifications
class EMailer:

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()  # start email server
        self.server.login(GMAIL_USER, GMAIL_PASS)  # email login
        pass

    def send_email(self, contacts, site):
        # iterate through all email contacts to send email
        for contact in contacts:
            fromaddr = GMAIL_USER  # from email address
            toaddrs = [contact.email]  # to email address

            # email body text
            msg = '''
Hi {}!
                
A Switch is now available on {}'s site. See details below.\n

{}
Buy here: {}

                '''.format(contact.name, site.site_name, site.description, site.url)

            self.server.sendmail(fromaddr, toaddrs, msg)  # send email

            # print action of EMailer
            print(
                "Just sent an email to {} about the {} from {}".format(contact.name, site.description, site.site_name))

    def __del__(self):
        self.server.quit()  # shut down email server

# responsible for parsing webpage for change in "Sold Out" or "Not Available" status
class WebsiteParser:
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
        "Referer": "https://www.google.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us"
    }

    # perform search for webpage text
    def search(self, site):
        req = requests.get(site.url, headers=WebsiteParser.header) # request from site
        r = re.findall(site.search_query, req.text) # regex search for query in Website
        return True if r else False # if query is found, output true

# calls all subsequent functions - auto,
class Coordinator:

    def __init__(self, websites, contacts):
        self.websites = websites
        self.contacts = contacts

    # auto run
    def auto(self, wait):
        while True:
            self.caller(self.websites)
            time.sleep(wait)

    def caller(self, websites):
        for website in websites:
            websiteparser = WebsiteParser()
            if websiteparser.search(website):
                emailer = EMailer()
                emailer.send_email(self.contacts, website)


def main():
    # website information
    bestbuy_gray = Website(
        "http://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/6364253.p?skuId=6364253",
        "Best Buy",
        "<button.*?>.*?Sold Out.*?</button>",
        "Nintendo - Switch 32GB Console - Gray Joy-Con")

    bestbuy_neon = Website(
        "http://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255",
        "Best Buy",
        "<button.*?>.*?Sold Out.*?</button>",
        "Nintendo - Switch 32GB Console - Neon Red/Neon Blue Joy-Con")

    bestbuy_ac = Website(
        "http://www.bestbuy.com/site/nintendo-switch-animal-crossing-new-horizons-edition-32gb-console-multi/6401728.p?skuId=6401728",
        "Best Buy",
        "<button.*?>.*?Sold Out.*?</button>",
        "Nintendo - Switch - Animal Crossing: New Horizons Edition 32GB Console - Multi")

    gamestop_gray = Website(
        "http://www.gamestop.com/video-games/switch/consoles/products/nintendo-switch-with-gray-joy-con/10141820.html",
        "GameStop",
        "availability&quot;:&quot;Not Available&quot;",
        "Nintendo Switch with Gray Joy-Con")

    gamestop_neon = Website(
        "http://www.gamestop.com/video-games/switch/consoles/products/nintendo-switch-with-neon-blue-and-neon-red-joy-con/10141887.html",
        "GameStop",
        "availability&quot;:&quot;Not Available&quot;",
        "Nintendo Switch with Neon Blue and Neon Red Joy-Con")

    # contacts
    tyler = Contact("Tyler", GMAIL_USER)

    # website list
    websiteList = [
        # bestbuy_ac,
        # bestbuy_gray,
        # bestbuy_neon,
        gamestop_gray,
        gamestop_neon]
    # websiteList = [gamestop_gray, gamestop_neon]

    # contact list
    contactList = [tyler]

    # call doer function to do
    coordinator = Coordinator(websiteList, contactList)
    coordinator.auto(60)

# we this so if you import this file, main() never gets called
if __name__ == '__main__':
    main()
