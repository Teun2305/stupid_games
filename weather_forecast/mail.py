# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 20:10:55 2022

@author: teunh
"""
import sys
import schedule
import time
import smtplib
import requests
from datetime import date
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_link():
    """
    Gets the link from darksky.net with for today.
    The location is Nijmegen (NL).

    Returns
    -------
    str
        URL to today's weather via darksky.net

    """
    year, month, day = str(date.today()).split('-')
    return f'https://darksky.net/details/51.8453,5.8676/{year}-{month}-{day}/ca24/en'


def get_data():
    """
    Retrieves the necessary data from darksky.net

    Returns
    -------
    date : str
        Today's date
    summary : str
        Summary of today's weather
    low_temp : str
        Today's lowest temperature
    low_time : str
        Time of today's lowest temperature
    high_temp : str
        Today's highest temperature
    high_time : str
        Time of today's highest temperature
    sun_rise : str
        Time at which the sun rises
    sun_set : str
        Time at which the sun sets
    rain : str
        Amount of rain that will fall (in mm)

    """
    r = requests.get(get_link())
    soup = BeautifulSoup(r.content, 'html.parser')

    date = soup.find('div', class_='date').get_text()

    summary = soup.find('p', id='summary').get_text()

    low_high_temp = soup.find('div', class_='highLowTemp swip').get_text().split('\n')
    for _ in range(6):
        low_high_temp.remove('')
    low_high_temp.remove('→')
    low_temp, low_time, high_temp, high_time = low_high_temp

    sun_times = soup.find('div', class_='sunTimes').get_text().split('\n')
    for _ in range(8):
        sun_times.remove('')
    sun_rise, sun_set = sun_times

    rain = soup.find('div', class_='precipAccum swap').get_text().split('\n')[3]
    return date, summary, low_temp, low_time, high_temp, high_time, sun_rise, sun_set, rain


def message():
    """
    Creates the message and subject for the mail

    Returns
    -------
    str
        MIMEMultipart object containing the subject and message as string

    """
    msg = MIMEMultipart()
    msg['Subject'] = 'Weather forecast for today'

    date, summary, low_temp, low_time, high_temp, high_time, sun_rise, sun_set, rain = get_data()
    text = f'Good morning, the weather forecast for {date} in Nijmegen is: {summary}\n' + \
           f'The lowest temperature of the day will be {low_temp}C at {low_time} ' + \
           f'and the highest will be {high_temp}C at {high_time}.\n' + \
           f'The sun will rise at {sun_rise} and set at {sun_set}.\n' + \
           f'There will be {rain} mm rain today.' + \
           '\n\nThis weather prediction is provided by darksky.net\n\n' + \
           'Have a nice day!!'

    msg.attach(MIMEText(text))
    return msg.as_string()


def get_mail_addresses():
    """
    Reads email addresses from a .csv file

    Returns
    -------
    addresses : list
        List containing the email addresses

    """
    addresses = list()
    try: 
        f = open('addresses.csv', 'r')
        for address in f:
            if '\n' in address:
                address = address.replace('\n', '')
            addresses.append(address)
        f.close()
    except FileNotFoundError:
        print('The file with the addresses has not been found.')
    except Exception as exc:
        print(f'An error occurred: {exc}')

    return addresses


def mail():
    """
    Sends out the mail via ochtendweerbericht@outlook.com to all the adresses
    in the list 'to'

    """
    email = 'ochtendweerbericht@outlook.com'
    smtp = smtplib.SMTP('smtp.office365.com', port=587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, 'password123')
    
    smtp.sendmail(from_addr=email,
                  to_addrs=get_mail_addresses(), msg=message())
    print('Mails sent successfully!!')
    smtp.quit()


if __name__ == '__main__':
    mail()
    time.sleep(3)
    sys.exit(0)
