"""
Temat 5: Aforyzmy na każdy dzień

Funkcjonalności:

Baza co najmniej 100 aforyzmów.
Program po uruchomieniu wyświetla jeden aforyzm na dzień.
Program pamięta które aforyzmy wyświetlił, w jaki dzień i nie powtarza wyświetlonych.
System oceny aforyzmu.
Po uruchomieniu program ma zagrać krótką melodyjkę.
Tryb ciemny
Wysyłanie przypomnienia o codziennym aforyzmie na maila (ewentualnie: dostosowanie czcionki w aplikacji)
"""

from random import choice
from time import localtime, strftime
from tkinter import *
from playsound import playsound

import email
import ssl
import smtplib

x = localtime()
date_today = strftime("%d.%m.%Y", x)


def sending_email(email_receiver, aphorism_today):
    email_sender = 'Aforyzmynakazdydzien@gmail.com'
    email_password = 'hgfrxleebcbonmtz'

    subject = 'Aforyzmy na każdy dzień'
    body = f"Aforyzm z dnia {date_today} to : {aphorism_today}"

    em = email.message.EmailMessage()
    em['From'] = email_sender
    em['To'] = email_password
    em['Subject'] = subject
    em.set_content(body)

    contex = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contex) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def sound(func):
    def wrapper(n, list_last_aphorisms):
        playsound('sound_effect.mp3')
        return func(n, list_last_aphorisms)

    return wrapper


@sound
def graphic_design(a, list_last_aphorisms):
    window = Tk()
    window.minsize(width=1000, height=250)
    window.geometry("250x250")

    Label(window, text=date_today + " - " + a, font=("Times", 16), wraplength=1000).pack(fill=BOTH, expand=True)
    Label(window, text="".join(list_last_aphorisms), justify=LEFT, font=("Times", 9), wraplength=1000).pack(fill=BOTH,
                                                                                                            expand=True)
    window.mainloop()

    # window = Tk()
    # w_1 = LabelFrame(window)
    #
    #
    # window.title("Aphorisms for every day")
    # window.geometry("800x700")
    # window.mainloop()

    # suwak i oprawa graficzna

    with open('email.txt', 'r+') as e:
        email_receiver = e.read()
        if len(email_receiver) != 0:
            sending_email(email_receiver, a)
        else:
            email_receiver = input("Podaj email : ")  # uzależnić od interfejsu graficznego
            e.write(email_receiver)
            sending_email(email_receiver, a)


def main():
    filepath_1 = "data_one_hundred_aphorisms.txt"
    filepath_2 = "aphorisms_used_before.txt"

    with open(filepath_1, "r", encoding="UTF-8") as d_1, open(filepath_2, "r+", encoding="UTF-8") as d_2:

        aphorisms = d_1.readlines()
        last_aphorisms = d_2.readlines()

        if date_today != last_aphorisms[-1][:10]:
            while True:
                aphorism_today = choice(aphorisms)
                if (last_aphorisms == []) or (aphorism_today not in [i[13:] for i in last_aphorisms]):
                    break
            d_2.write(date_today + " - " + aphorism_today)
            graphic_design(aphorism_today, last_aphorisms)


main()
