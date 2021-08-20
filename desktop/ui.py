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
    def __init__(self, root, theme):
        self.root = root
        Frame.__init__(self, root)
        self.text = """
        This is a typing test. Repeat: this is a typing test. Got it? Good. Continue to enter this text. This text determines your future (no it doesn't). Please note that entering this text is vital to success in this typing test, obviously, so keep on typing this text! Come on, just a little more! It won't hurt! You're almost there! Just so much more typing to go! Just a lot! Then you will be done! Isn't that exciting? Closer, closer, closer, closer, closer, and boom, you're so close! Just a little more, just a little. And... you're done!
        """.strip()
        self.theme = theme
        self.displayed_text = """
This is a typing test. Repeat: this is a typing test. Got it? Good. Continue to
enter this text. This text determines your future (no it doesn't). Please note
that entering this text is vital to success in this typing test, obviously, so
keep on typing this text! Come on, just a little more! It won't hurt! You're al
most there! Just so much more typing to go! Just a lot! Then you will be done!
Isn't that exciting? Closer, closer, closer, closer, closer, and boom, you're s
o close! Just a little more, just a little. And... you're done!""".strip()
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
        if self.theme == "azure-dark":
            self.text_widget.config(bg="#333333")

        self.display_t.pack(padx=10, pady=10)
        self.enter_text.pack(padx=10, pady=10)
        self.text_widget.pack(padx=10, pady=10)

    def get(self):
        return self.text_widget.get('1.0', END)

class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Typing Test")
        self.root.tk.call('source', 'theme/azure-dark.tcl')
        self.root.tk.call('source', 'theme/azure.tcl')
        self.style = Style()
        if isDark():
            self.style.theme_use('azure-dark')
            self.theme = "azure-dark"
        else:
            self.style.theme_use('azure')
            self.theme = "azure"

        self.measure = TypingTestResults()
        self.timer = None

        self.open_page = OnOpen(self.root, self.start)
        self.main_page = MainFrame(self.root, self.theme)
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
