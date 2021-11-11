from threading import Timer
from darkdetect import isDark
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.ttk import *
from results import *
from tkinter.ttk import *

class ResultsFrame(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)
        self.create_widgets()

    def create_widgets(self):
        self.accuracy_label = Label(self)
        self.wpm_label = Label(self)
        self.errors_label = Label(self)

        self.accuracy_label.pack(padx=10, pady=10)
        self.wpm_label.pack(padx=10, pady=10)
        self.errors_label.pack(padx=20, pady=10)

    def main(self, wpm, accuracy, errors):
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.errors_label.config(text=f"Errors: {errors}")
        self.pack()

class OnOpen(Frame):
    def __init__(self, root, start):
        self.root = root
        self.c_start = start
        Frame.__init__(self, root)
        self.create_widgets()

    def create_widgets(self):
        self.start_button = Button(self, text="Start", command=self.start)
        self.start_button.pack(padx=10, pady=10)

    def start(self):
        self.c_start()

class MainFrame(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)
        self.text = """
    Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then she continued her way. On her way she met a copy. The copy warned the Little Blind Text, that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word "and" and the Little Blind Text should turn around and return to its own, safe country. But nothing the copy said could convince her and so it didn’t take long until a few insidious Copy Writers ambushed her, made her drunk with Longe and Parole and dragged her into their agency, where they abused her.
        """.strip()
        self.displayed_text = """
Far far away, behind the word mountains, far from the countries Vokalia and Cons
onantia, there live the blind texts. Separated they live in Bookmarksgrove righ
t at the coast of the Semantics, a large language ocean. A small river named Du
den flows by their place and supplies it with the necessary regelialia. It is a
 paradisematic country, in which roasted parts of sentences fly into your mouth
. Even the all-powerful Pointing has no control about the blind texts it is an
almost unorthographic life One day however a small line of blind text by the na
me of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox
advised her not to do so, because there were thousands of bad Commas, wild Ques
tion Marks and devious Semikoli, but the Little Blind Text didn’t listen. She p
acked her seven versalia, put her initial into the belt and made herself on the
 way. When she reached the first hills of the Italic Mountains, she had a last
view back on the skyline of her hometown Bookmarksgrove, the headline of Alphab
et Village and the subline of her own road, the Line Lane. Pityful a rethoric q
uestion ran over her cheek, then she continued her way. On her way she met a co
py. The copy warned the Little Blind Text, that where it came from it would hav
e been rewritten a thousand times and everything that was left from its origin
would be the word "and" and the Little Blind Text should turn around and return
 to its own, safe country. But nothing the copy said could convince her and so
it didn’t take long until a few insidious Copy Writers ambushed her, made her d
runk with Longe and Parole and dragged her into their agency, where they abused her.
        """.strip()
        self.text_length = self.get_length(self.text)
        self.create_widgets()

    def get_length(self, string):
        split = string.split(' ')
        length = len(split)
        return length

    def create_widgets(self):
        self.display_t = Label(self, text="Enter below into text box.", font='tahoma 18 bold')
        self.enter_text = Label(self, text=self.displayed_text)
        self.text_widget = ScrolledText(self)

        self.display_t.pack(padx=10, pady=10)
        self.enter_text.pack(padx=10, pady=10)
        self.text_widget.pack(padx=10, pady=10)

    def get(self):
        return self.text_widget.get('1.0', END)

class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Typing Test")

        self.measure = TypingTestResults()
        self.timer = None

        self.open_page = OnOpen(self.root, self.start)
        self.main_page = MainFrame(self.root)
        self.results_page = ResultsFrame(self.root)

        self.open_page.pack()

    def start(self):
        self.timer = Timer(60, self.stop)

        self.open_page.pack_forget()
        self.main_page.pack()

        self.timer.start()

    def stop(self):
        self.timer.cancel()

        content = self.main_page.get()
        c = ""
        for line in content.split('\n'):
            c += line
        content = c
        length = len(content.split(' '))

        orig_text = self.main_page.text
        l = self.main_page.text_length
        time_taken = 1.0 # one minute taken

        wpm = self.measure.wpm(content, time_taken)
        errors = self.measure.errors(orig_text, content)
        accuracy = self.measure.accuracy(length, errors)

        accuracy = accuracy * 100.0
        wpm = int(wpm)

        self.main_page.pack_forget()
        self.results_page.main(wpm, accuracy, errors)

    def main(self):
        self.root.mainloop()
