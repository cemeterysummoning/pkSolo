from question import *
import tkinter as tk
import time
import os, sys

class UI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("pkSolo")
        screen_width, screen_height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        #self.window.geometry(f"{screen_width}x{screen_height}+0+0")

        self.color_var = tk.StringVar()
        self.color_var.set("dark")
        self.color_mode = ["black", "white"]

        # setting up environment
        self.question_frame = tk.LabelFrame(self.window, padx=15, 
                                            pady=15, text="question", fg=self.color_mode[1], bg=self.color_mode[0])
        self.question_frame.pack(fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.LabelFrame(self.window, padx=15, pady=15, text="stats", fg="white", bg="black")

        self.buttons_frame.pack(fill=tk.BOTH, expand=True)

        # score label
        tk.Label(self.buttons_frame, text="score:", bg="black", fg="white").grid(row=0, column=0)
        self.score = tk.IntVar()
        self.score.set(5)
        self.scoring = tk.Label(self.buttons_frame, textvariable=self.score, bg="black", fg="white")
        self.scoring.grid(row=0, column=1)

        # question count
        tk.Label(self.buttons_frame, text="\tquestion number:", bg="black", fg="white").grid(row=0, column=2)
        self.q_num = tk.IntVar()
        self.q_num.set(0)
        tk.Label(self.buttons_frame, textvariable=self.q_num, bg="black", fg="white").grid(row=0, column=3)

        tk.Label(self.buttons_frame, text="\n", bg="black").grid(row=1, column=0)

        # get new html
        self.get_html_button = tk.Button(self.buttons_frame,
                                        text="Get new set", command=self.get_html_window, bg="black", fg="white")
        self.get_html_button.grid(row=2, column=0)

        # restart
        self.restart_button = tk.Button(self.buttons_frame, text="Restart with new", 
                                        command=self.restart, bg="black", fg="white")
        self.restart_button.grid(row=2, column=1)

        # place question
        self.canvas = tk.Canvas(self.question_frame, width=screen_width * 9 / 10, height=screen_height * 2 / 5, bg="black")

        self.question_txt = self.canvas.create_text(screen_width * 9 / 20, screen_height / 5,
                                                    text="placeholder", width=1000, fill="white",
                                                    font=("calibri", 15))

        self.canvas.pack()

        # entry
        tk.Label(self.question_frame, text="\n\n", bg="black").pack()

        self.answer_box = tk.Entry(self.question_frame, width=32, borderwidth=5, bg="black", fg="white", insertbackground="white")
        self.answer_box.pack()

        tk.Label(self.question_frame, text="\n", bg="black").pack()

        self.enter_button = tk.Button(self.question_frame, text="enter", padx=5, pady=5, bg="black", fg="white", command=lambda: self.next())
        self.enter_button.pack()

        tk.Label(self.question_frame, text="\n", bg="black").pack()

        self.corrections = tk.StringVar()
        self.corrections.set("\n")
        tk.Label(self.question_frame, textvariable=self.corrections, bg="black", fg="white").pack()

        self.next()

        self.corrections.set("\n")

        self.window.bind("<Return>", self.enter_tobind)
        
        self.window.mainloop()
        
    def get_html_window(self):
        self.window = webdriver.Firefox(executable_path="/home/ace/geckodriver")
        self.window.get('https://www.quizdb.org')

        self.other_userin = tk.Tk()

        self.userin_button = tk.Button(self.other_userin, text="click here to return", 
                command=lambda: [self.get_html_source(), self.window.close(), self.other_userin.destroy()]).pack()

    def get_html_source(self):
        html = self.window.page_source
        with open("html.txt", "w") as ptext:
                ptext.write(html)
        
        self.game.get_qs()
        
    def restart(self):
        os.system("python3 mainUI.py")
        self.window.destroy()

    def enter_tobind(self, e):
        self.next()

    def next(self):
        if self.game.has_next():
            tempscore = 0
            if self.check_answer():
                tempscore = 10
                self.canvas.itemconfigure(self.question_txt, text="correct")
                self.corrections.set("previous: correct")
            elif not self.check_answer():
                tempscore = -5
                self.corrections.set(f"previous: incorrect. answer was {self.game.question_set[self.game.question_index].answer}")


            self.score.set(self.score.get() + tempscore)
            
            self.game.next()

            self.q_num.set(self.q_num.get() + 1)

            self.answer_box.delete(0, tk.END)

            self.display_next_q()
        else:
            self.canvas.itemconfigure(self.question_txt, text="no more questions")

    def display_next_q(self):
        current_q = self.game.question_set[self.game.question_index].contents
        self.canvas.itemconfigure(self.question_txt, text=current_q)

        self.q_words = current_q.split()

        self.iterative(0)

    def iterative(self, i):
        self.canvas.itemconfigure(self.question_txt, text=self.q_words[:i])
        i += 1    
        self.window.after(100, lambda: self.iterative(i))

    def check_answer(self):
        answer = self.answer_box.get()
        
        return self.game.verify(answer)
    

mainGame = MainGame()
main = UI(mainGame)
