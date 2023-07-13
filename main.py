# Refactored Code

from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import *
from tkinter import ttk
import locale
import tomllib


class Zwicky:
    def __init__(self):
        with open("config.toml", "rb") as f:
            self.config = tomllib.load(f)

        self.locale_codes = self.config["locale_codes"]
        self.language_codes = self.config["language_codes"]

        self.root = Tk()
        self.root.title("Word Frequency Analyzer")
        self.font_general = ("Roboto", 14)
        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.grid()
        self.combobox = ttk.Combobox(
            self.frm, values=self.config["language_list"], state="readonly"
        )
        self.entryfield = ttk.Entry(self.frm, width=10)
        self.filename = ttk.Entry(self.frm, width=25)
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.frm, text="Enter Youtube Video ID").grid(
            column=0, row=1, sticky=W
        )
        ttk.Label(self.frm, text="Target Language").grid(column=0, row=2, sticky=W)
        self.combobox.grid(column=1, row=2, sticky=E)
        self.entryfield.grid(column=1, row=1, sticky=E)
        ttk.Label(self.frm, text="Enter Desired Filename").grid(
            column=0, row=4, sticky=W
        )
        self.filename.grid(column=1, row=4, sticky=E)
        ttk.Button(self.frm, text="Begin", command=self.get_information).grid(
            column=0, row=5, sticky=W
        )
        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(
            column=1, row=5, sticky=E
        )

    def get_transcript(self, video_id, lang):
        return YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

    def clean_transcript(self, transcript):
        cleaned_words = []
        subtitles_parsed = [i["text"] for i in transcript]
        for i in subtitles_parsed:
            i = (
                i.replace("\n", " ")
                .replace(".", " ")
                .replace("(", "")
                .replace(")", "")
                .replace("?", "")
            )
            i = (
                i.replace("!", "")
                .replace(",", "")
                .replace(";", "")
                .replace(":", "")
                .replace('"', "")
                .replace("-", "")
            )
            words = i.split(" ")
            cleaned_words.extend(i.lower() for i in words)
        return cleaned_words

    def compute_word_frequencies(self, words):
        frequency = {}
        for i in words:
            if i == "":
                continue
            elif i in frequency:
                frequency[i] += 1
            else:
                frequency[i] = 1
        return frequency

    def save_frequencies(self, frequency, filename):
        sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        with open(f"{filename}.txt", "w", encoding="utf-8") as f:
            for word, frequencies in sorted_frequency:
                f.write(f"{word}: {str(frequencies)}" + "\n")

    def get_information(self):
        lang_choice = self.combobox.get()
        video_id = self.entryfield.get()
        user_filename = self.filename.get()
        locale.setlocale(locale.LC_ALL, self.locale_codes[lang_choice])
        transcript = self.get_transcript(video_id, self.language_codes[lang_choice])
        cleaned_words = self.clean_transcript(transcript)
        frequency = self.compute_word_frequencies(cleaned_words)
        self.save_frequencies(frequency, user_filename)
        self.root.destroy()

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Zwicky()
    app.main()

