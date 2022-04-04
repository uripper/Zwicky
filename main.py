import os
from threading import local
from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import *
from tkinter import ttk
import locale


def get_information():
    global ENTRYFIELD, COMBOBOX
    LANGCHOICE = COMBOBOX.get()
    VIDEOID = ENTRYFIELD.get()
    print(LANGCHOICE, VIDEOID)
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
    # elif LANGCHOICE == 'Japanese':
    #     locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    #     local_lang = 'ja'
    # elif LANGCHOICE == 'Korean':
    #     locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
    #     local_lang = 'ko'
    # elif LANGCHOICE == 'Portuguese':
    #     locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')
    #     local_lang = 'pt'
    # elif LANGCHOICE == 'Russian':
    #     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    #     local_lang = 'ru'
    # elif LANGCHOICE == 'Chinese':
    #     locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    #     local_lang = 'zh'
    # elif LANGCHOICE == 'Turkish':
    #     locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
    #     local_lang = 'tr'
    # elif LANGCHOICE == 'Ukrainian':
    #     locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    #     local_lang = 'uk'
    # elif LANGCHOICE == 'Vietnamese':
    #     locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    #     local_lang = 'vi'

    print(local_lang)


language_list = ['English', 'French', 'Spanish', 'German', 'Italian']

root = Tk()


frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Subtitle Frequency Creator").grid(column=1, row=0)
ttk.Label(frm, text="Enter Youtube Video ID").grid(column=0, row=1)
ttk.Label(frm, text="Target Language").grid(column=0, row=2)

COMBOBOX = ttk.Combobox(root, values=language_list, state='readonly')

COMBOBOX.grid(column=1, row=0)

ENTRYFIELD = ttk.Entry(frm, width=10)
ENTRYFIELD.grid(column=1, row=1)
ttk.Button(frm, text="Begin", command=get_information).grid(column=0, row=3)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=3)
root.mainloop()


print(COMBOBOX)
print(ENTRYFIELD)
