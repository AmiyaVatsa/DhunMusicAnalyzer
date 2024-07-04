import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from ttkthemes import ThemedTk, ThemedStyle
from tkinter.filedialog import askopenfilename
from compare_audio import audio_comparator
from extract_notes import extractor
from PIL import Image, ImageTk
audio_list = {}
global_image_list = []
class dhunApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        style = ThemedStyle()
        style.theme_use('black')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, ComparePage, AudioPageOne, AudioPageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Music Analyzer App", font=controller.title_font, justify='center')
        label.pack()
        btn_open_file = ttk.Button(self, text = "Choose an Audio", command = self.open_file)
        self.audio_names = ttk.Label(self, text="Audio Selected:-\n")
        btn_compare = ttk.Button(self, text = "Compare Audios", command = lambda: controller.show_frame("ComparePage"))
        btn_extract_notes_one = ttk.Button(self, text= "Extract Notes from first audio", command = lambda: controller.show_frame("AudioPageOne")) 
        btn_extract_notes_two = ttk.Button(self, text= "Extract Notes from second audio", command = lambda: controller.show_frame("AudioPageTwo")) 
        btn_clear_list = ttk.Button(self, text="Clear", command=self.clear)
        btn_open_file.pack()
        btn_compare.pack()
        btn_extract_notes_one.pack()
        btn_extract_notes_two.pack()
        self.audio_names.pack()
        btn_clear_list.pack()
    def clear(self):
        audio_list.clear()
        self.audio_names["text"] = "Audio Selected:-\n"
    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3")]
        )
        path_list = filepath.split("/")
        audio_list[path_list[len(path_list) - 1]] = filepath
        self.audio_names["text"] += path_list[len(path_list) - 1] + "\n"


class ComparePage(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Audio Comparison", font=controller.title_font)
        label.pack()
        btn_compare = ttk.Button(self, text="Initiate Comparison", command=self.compare)
        self.result = ttk.Label(self)
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        btn_compare.pack()
        self.result.pack()
    def compare(self):
        temp = list(audio_list.keys())
        if len(temp) == 1:
            temp.append(temp[0])
        file_1 = temp[0]
        file_2 = temp[1]
        self.result["text"] = "The two songs are :" + str(audio_comparator(file_1=file_1, file_2=file_2)) + "%" + " similar.\n"


class AudioPageOne(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.FRAME_COUNT = 100
        self.cur = 0
        label = ttk.Label(self, text="Frame-Wise Dominant Notes : Audio 1", font=controller.title_font)
        label.pack()
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        btn_extract = ttk.Button(self, text="Initiate Extraction", command = self.extract)
        self.image_label = ttk.Label(self)
        btn_next = ttk.Button(self, text = "Next Image", command = self.next_image)
        btn_prev = ttk.Button(self, text = "Previous Image", command = self.prev_image)
        button.pack()
        btn_extract.pack()
        btn_next.pack()
        btn_prev.pack()
        self.image_label.pack()
    def extract(self):
        temp = list(audio_list.keys())
        file = temp[0]
        self.FRAME_COUNT = extractor(filepath=file)
        self.image_label.config(image=ImageTk.PhotoImage(Image.open("content\\frame0.png")))
        global_image_list.append(ImageTk.PhotoImage(Image.open("content\\frame0.png")))
    def next_image(self):
        if self.cur == self.FRAME_COUNT - 1:
            self.cur = 0
        else:
            self.cur += 1
        im = Image.open(f"content\\frame{self.cur}.png")
        ph = ImageTk.PhotoImage(image = im)
        self.image_label.config(image=ph)
        global_image_list.append(ph)
    def prev_image(self):
        if self.cur == 0:
            self.cur = self.FRAME_COUNT - 1
        else:
            self.cur -= 1
        im = Image.open(f"content\\frame{self.cur}.png")
        ph = ImageTk.PhotoImage(image = im)
        self.image_label.config(image=ph)
        global_image_list.append(ph)

class AudioPageTwo(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.FRAME_COUNT = 100
        self.cur = 0
        label = ttk.Label(self, text="Frame-Wise Dominant Notes : Audio 2", font=controller.title_font)
        label.pack()
        button = ttk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        btn_extract = ttk.Button(self, text="Initiate Extraction", command = self.extract)
        self.image_label = ttk.Label(self)
        btn_next = ttk.Button(self, text = "Next Image", command = self.next_image)
        btn_prev = ttk.Button(self, text = "Previous Image", command = self.prev_image)
        button.pack()
        btn_extract.pack()
        btn_next.pack()
        btn_prev.pack()
        self.image_label.pack()
    def extract(self):
        temp = list(audio_list.keys())
        if len(temp) == 1:
            temp.append(temp[0])
        file = temp[1]
        self.FRAME_COUNT = extractor(filepath=file)
        self.image_label.config(image=ImageTk.PhotoImage(Image.open("content\\frame0.png")))
        global_image_list.append(ImageTk.PhotoImage(Image.open("content\\frame0.png")))
    def next_image(self):
        if self.cur == self.FRAME_COUNT - 1:
            self.cur = 0
        else:
            self.cur += 1
        im = Image.open(f"content\\frame{self.cur}.png")
        ph = ImageTk.PhotoImage(image = im)
        self.image_label.config(image=ph)
        global_image_list.append(ph)
    def prev_image(self):
        if self.cur == 0:
            self.cur = self.FRAME_COUNT - 1
        else:
            self.cur -= 1
        im = Image.open(f"content\\frame{self.cur}.png")
        ph = ImageTk.PhotoImage(image = im)
        self.image_label.config(image=ph)
        global_image_list.append(ph)

if __name__ == "__main__":
    app = dhunApp()
    app.mainloop()