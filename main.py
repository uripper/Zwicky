import contextlib
from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import ttk, filedialog, Tk, Scale, HORIZONTAL, W, E
import locale
import toml
import re


class Zwicky:
    def __init__(self):
        try:
            with open("config.toml", "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            error_message = "Config file not found. Please ensure that config.\
                toml is in the same directory as this program. \
                    This can be downloaded from the Github repository."
            raise FileNotFoundError(error_message)
        try:
            with open("ignored_words.txt", "r") as f:
                self.ignored_words = f.read().splitlines()
        except FileNotFoundError:
            with open("ignored_words.txt", "w") as f:
                f.write("")
                self.ignored_words = []
        self.locale_codes = self.config["locale_codes"]
        self.language_codes = self.config["language_codes"]

        self.root = Tk()
        self.root.title("Zwicky: Word Frequency Analyzer")

        self.font_general = ("Roboto", 14)

        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.grid()

        self.combobox = ttk.Combobox(
            self.frm, values=self.config["language_list"], state="readonly"
        )
        self.entry_field = ttk.Entry(self.frm, width=25)

        self.min_slider = Scale(self.frm, from_=0, to=5, orient=HORIZONTAL)
        self.max_slider = Scale(self.frm, from_=3, to=10, orient=HORIZONTAL)
        self.use_min_slider_box = ttk.Checkbutton(self.frm, text="Use Min Slider")
        self.use_max_slider_box = ttk.Checkbutton(self.frm, text="Use Max Slider")
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.frm, text="Target Language").grid(column=0, row=0, sticky=W)
        self.combobox.grid(column=1, row=0, sticky=E)

        ttk.Label(self.frm, text="Enter Youtube Video URL").grid(
            column=0, row=1, sticky=W
        )
        self.entry_field.grid(column=1, row=1, sticky=E)

        ttk.Label(self.frm, text="Min Word Frequency (%)").grid(
            column=0, row=2, sticky=W
        )
        self.min_slider.grid(column=1, row=2, sticky=E)
        ttk.Label(self.frm, text="Use Min Slider").grid(column=2, row=2, sticky=W)
        self.use_min_slider_box.grid(column=3, row=2, sticky=E)
        self.min_slider.set(0)
        self.use_min_slider_box.state(["selected"])

        ttk.Label(self.frm, text="Max Word Frequency (%)").grid(
            column=0, row=3, sticky=W
        )
        self.max_slider.grid(column=1, row=3, sticky=E)
        self.max_slider.set(10)
        ttk.Label(self.frm, text="Use Max Slider").grid(column=2, row=3, sticky=W)
        self.use_max_slider_box.grid(column=3, row=3, sticky=E)
        self.use_max_slider_box.state(["selected"])

        ttk.Button(self.frm, text="Begin", command=self.get_information).grid(
            column=0, row=4, sticky=W
        )
        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(
            column=1, row=4, sticky=E
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
        total_words = len(words)
        frequency = {}
        for i in words:
            if i == "" or i in self.ignored_words:
                continue
            elif i in frequency:
                frequency[i] += 1
            else:
                frequency[i] = 1

        # Filter words based on min and max frequencies
        min_freq = self.min_slider.get() * total_words / 100
        max_freq = self.max_slider.get() * total_words / 100

        if not self.use_min_slider_box.instate(["selected"]):
            min_freq = 0

        if not self.use_max_slider_box.instate(["selected"]):
            max_freq = total_words

        filtered_frequency = {
            word: count
            for word, count in frequency.items()
            if min_freq <= count <= max_freq
        }
        return filtered_frequency, total_words

    def save_frequencies(self, frequency, total_words, filename):
        sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        with contextlib.suppress(FileNotFoundError):
            with open(filename, "w", encoding="utf-8") as f:
                for word, frequencies in sorted_frequency:
                    percentage = (frequencies / total_words) * 100
                    f.write(f"{word}: {str(frequencies)} ({percentage:.2f}%)" + "\n")

    def get_information(self):
        url = self.entry_field.get()
        video_id = re.findall(r"(?<=v=)[^&#]+", url)[0]
        lang_choice = self.combobox.get()
        locale.setlocale(locale.LC_ALL, self.locale_codes[lang_choice])
        transcript = self.get_transcript(video_id, self.language_codes[lang_choice])
        cleaned_words = self.clean_transcript(transcript)
        frequency, total_words = self.compute_word_frequencies(cleaned_words)
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        self.save_frequencies(frequency, total_words, filename)
        self.root.destroy()

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Zwicky()
    app.main()
