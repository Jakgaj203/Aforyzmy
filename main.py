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

from tkinter import *
from time import localtime, strftime
from playsound import playsound
from random import choice


x = localtime()
date_today = strftime("%d.%m.%Y", x)


def sound(func):
    def wrapper(n, list_last_aphorisms):
        playsound('sound_effect.mp3')
        return func(n, list_last_aphorisms)

    return wrapper


@sound
def graphic_design(n, list_last_aphorisms):
    window = Tk()
    window.minsize(width=1000, height=250)
    window.geometry("250x250")

    Label(window, text=date_today + " - " + n, font=("Times", 16), wraplength=1000).pack(fill=BOTH, expand=True)
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
