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
def graphic_design(ap_t, list_last_aphorisms):
    window = Tk()
    window.maxsize(width=1280, height=480)
    window.minsize(width=1280, height=480)
    window.geometry('1280x480')

    # Tworzenie Menu
    my_menu = Menu(window)
    window.config(menu=my_menu)

    # Tworzenie tła i wypisywanie aforyzmów
    window.iconbitmap(r'GR_3.ico')

    bg = [PhotoImage(file="image.png"),
          PhotoImage(file="image_dark_mode.png")]

    my_canva = Canvas(window, width=1280, height=480)
    my_canva.pack(fill='both', expand=True)
    my_canva.create_image(0, 0, image=bg[0], anchor="nw")

    my_canva.create_text(640, 80, text=ap_t, font=("Oswald", 25), fill="black", width=1000)
    my_canva.create_text(310, 250, text="".join(list_last_aphorisms), font=("Oswald", 11), fill="black", width=600)

    # Wpisywanie maila i zapisywanie go do pliku tekstowego
    entry = Text(window, height=2, width=30)
    my_canva.create_window(640, 460, window=entry)

    def save_text():
        text_file = open("email.txt", "w")
        text_file.write(entry.get(1.0, END))
        text_file.close()

    button_send = Button(window, text="Wyślij na ten mail", command=save_text)
    my_canva.create_window(840, 460, window=button_send)

    # Opcja dark i light mode
    def night_on():
        my_canva.create_image(0, 0, image=bg[1], anchor="nw")

        my_canva.create_text(640, 80, text=ap_t, font=("Oswald", 25), fill="white", width=1000)
        my_canva.create_text(310, 250, text="".join(list_last_aphorisms), font=("Oswald", 11), fill="white", width=600)

    def night_off():
        my_canva.create_image(0, 0, image=bg[0], anchor="nw")

        my_canva.create_text(640, 80, text=ap_t, font=("Oswald", 25), fill="black", width=1000)
        my_canva.create_text(310, 250, text="".join(list_last_aphorisms), font=("Oswald", 11), fill="black", width=600)

    option_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="Option", menu=option_menu)
    option_menu.add_command(label="Night on", command=night_on)
    option_menu.add_command(label="Night off", command=night_off)

    window.mainloop()

    with open('email.txt', 'r+') as e:
        email_receiver = e.read()
        if len(email_receiver) != 0:
            sending_email(email_receiver, ap_t)
        else:
            email_receiver = input("Podaj email : ")  # uzależnić od interfejsu graficznego
            e.write(email_receiver)
            sending_email(email_receiver, ap_t)


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
