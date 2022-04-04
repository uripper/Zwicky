import os
from threading import local
from tkinter import font
from numpy import size
from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import *
from tkinter import ttk
import locale


def get_information():
    global ENTRYFIELD, COMBOBOX
    LANGCHOICE = COMBOBOX.get()
    VIDEOID = ENTRYFIELD.get()
    USER_FILENAME = FILENAME.get()
    if LANGCHOICE == 'English':
        locale.setlocale(locale.LC_ALL, 'en_EN.UTF-8')
        local_lang = 'en'
    elif LANGCHOICE == 'French':
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        local_lang = 'fr'
    elif LANGCHOICE == 'Spanish':
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        local_lang = 'es'
    elif LANGCHOICE == 'German':
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        local_lang = 'de'
    elif LANGCHOICE == 'Italian':
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        local_lang = 'it'
    elif LANGCHOICE == 'Japanese':
        locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
        local_lang = 'ja'
    elif LANGCHOICE == 'Korean':
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
        local_lang = 'ko'
    elif LANGCHOICE == 'Portuguese':
        locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')
        local_lang = 'pt'
    elif LANGCHOICE == 'Russian':
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        local_lang = 'ru'
    elif LANGCHOICE == 'Chinese':
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
        local_lang = 'zh'
    elif LANGCHOICE == 'Turkish':
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        local_lang = 'tr'
    elif LANGCHOICE == 'Ukrainian':
        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
        local_lang = 'uk'
    elif LANGCHOICE == 'Vietnamese':
        locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
        local_lang = 'vi'

    subtitles = YouTubeTranscriptApi.get_transcript(
        VIDEOID, languages=[local_lang])
    subtitles_parsed = []
    cleaned_words = []
    usable_words = []
    frequency = {}
    for i in subtitles:
        subtitles_parsed.append(i['text'])
    for i in subtitles_parsed:
        cleaned_words.append(i.replace("\n", " ").replace(".", " ").replace("(", "").replace(")", "").replace("?", "").replace("!", "").replace(
            ",", "").replace(";", "").replace(":", "").replace('"', '').replace("-", ""))
    for i in cleaned_words:
        words = i.split(" ")
        for i in words:
            usable_words.append(i.lower())
    for i in usable_words:
        if i == "":
            continue
        elif i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1
    sorted_frequency = sorted(
        frequency.items(), key=lambda x: x[1], reverse=True)
    with open(f"{USER_FILENAME}.txt", "w", encoding='utf-8') as f:
        for word, frequencies in sorted_frequency:
            f.write(word + ": " + str(frequencies) + "\n")
    root.destroy()


language_list = ['English', 'French', 'Spanish', 'German', 'Italian',
                 'Korean', 'Portuguese', 'Russian', 'Turkish', 'Ukrainian']

root = Tk()
root.title("Word Frequency Analyzer")
font_general = ('Roboto', 14)
frm = ttk.Frame(root, padding=20)
frm.grid()


ttk.Label(frm, text="Enter Youtube Video ID").grid(column=0, row=1, sticky=W)
ttk.Label(frm, text="Target Language").grid(column=0, row=2, sticky=W)

COMBOBOX = ttk.Combobox(frm, values=language_list, state='readonly')

COMBOBOX.grid(column=1, row=2, sticky=E)

ENTRYFIELD = ttk.Entry(frm, width=10)
ENTRYFIELD.grid(column=1, row=1, sticky=E)
ttk.Label(frm, text="Enter Desired Filename").grid(column=0, row=4, sticky=W)
FILENAME = ttk.Entry(frm, width=25)
FILENAME.grid(column=1, row=4, sticky=E)
ttk.Button(frm, text="Begin", command=get_information).grid(
    column=0, row=5, sticky=W)
ttk.Button(frm, text="Quit", command=root.destroy).grid(
    column=1, row=5, sticky=E)
root.mainloop()


print(COMBOBOX)
print(ENTRYFIELD)
