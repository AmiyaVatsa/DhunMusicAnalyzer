import tkinter as tk
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename
from compare_audio import audio_comparator

audio_list = {}

class dhunApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Music Analyzer App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btn_open_file = tk.Button(self, text = "Choose an Audio", command = self.open_file)
        self.audio_names = tk.Label(self, text="Audio Selected:-\n")
        btn_compare = tk.Button(self, text = "Compare Audios", command = lambda: controller.show_frame("ComparePage"))
        btn_extract_notes_one = tk.Button(self, text= "Extract Notes from first audio", command = lambda: controller.show_frame("AudioPageOne")) 
        btn_extract_notes_two = tk.Button(self, text= "Extract Notes from second audio", command = lambda: controller.show_frame("AudioPageTwo")) 
        btn_clear_list = tk.Button(self, text="Clear", command=self.clear)
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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Comparison", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        btn_compare = tk.Button(self, text="Initiate Comparison", command=self.compare)
        self.result = tk.Label(self)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        btn_compare.pack()
        self.result.pack()
    def compare(self):
        temp = list(audio_list.keys())
        file_1 = temp[0]
        file_2 = temp[1]
        self.result["text"] = "The two songs are :" + str(audio_comparator(file_1=file_1, file_2=file_2)) + "%" + " similar.\n"


class AudioPageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class AudioPageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = dhunApp()
    app.mainloop()