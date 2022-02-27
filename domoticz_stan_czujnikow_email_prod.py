# -*- coding: utf-8 -*-
import json
import urllib.request
import smtplib
import time
import datetime

adres = "http://ip.ip.ip.ip:port/json.htm?type=devices&rid="
czujniki = {"Kuchnia (góra)": 9, 
            "Strych": 10, 
            "Spiżarka (dół)": 11,
            "Kuchnia (dół)": 12,
            "Temp+wilg_Kuchnia (dół)": 13,
            "Temp+wilg_Na_Polu": 14,
            "Boiler CS": 20,
            "Piec": 21,
            "Pokój I (dół)": 22,
            "Na polu": 23,
            "Halogen_Wifi": 35,
            "MQ9_Wifi": 36,
            "Multi_sensors_Wifi": 37,
            "Pokój II (dół)": 42,
            "Spiżarka (góra)": 43,
            "Pokój IV (góra)": 44,
            "Pokój III (góra)": 45,
            "Na polu (W)": 46,
            "Boiler CO": 47,
            "DS18b20_Wifi": 50,
            "Old_Home": 73
}

gmail_user = '@gmail.com'
gmail_password = 'haslo'

sent_from = gmail_user
to = ['@gmail.com']

x = 0
while True:
    for key in czujniki:
        idx = str(czujniki[key])
        url = adres + str(czujniki[key])
        json_text = urllib.request.urlopen(url).read().decode()
        data = json.loads(json_text)
        data2 = data['result']

        for data3 in data2:
            print(data3['LastUpdate'])

        czas_serwera = data['ServerTime']
        czas_aktualizacji = data3['LastUpdate']

        fmt = '%Y-%m-%d %H:%M:%S'
        minuty_aktualizacji = datetime.datetime.strptime(czas_aktualizacji, fmt)
        minuty_serwera = datetime.datetime.strptime(czas_serwera, fmt)
        roznica = minuty_serwera - minuty_aktualizacji
        roznica_minut = (roznica.days * 24 * 60) + (roznica.seconds/60)
        roznica_minut2 = int(roznica_minut)

        tresc_subject = key + ": "
        subject = tresc_subject
        tresc_body = "Czas serwera: " + str(czas_serwera) + " a czas aktualizacji czujnika: " + str(czas_aktualizacji)
        body = tresc_body


        email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (sent_from, to, subject, body)


        if roznica_minut >= 6:
            print('Różnica minut jest więkasza o', roznica_minut,  'minut/e!!!')
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text.encode("utf8"))
                server.close()

                print('Email sent!')
            except:
                print('Something went wrong...')
        else:
            print('Różnica minut jest większa o', roznica_minut,'minut/e ale nie wieksza od 6!!!')

        x = x + 1
        print("petla", x)
        print(email_text)
        time.sleep(5)
