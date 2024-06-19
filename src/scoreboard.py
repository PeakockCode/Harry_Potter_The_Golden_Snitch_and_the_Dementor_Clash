import tkinter
import customtkinter


class Scoreboard(customtkinter.CTk):

    def __init__(self, title, geometry, icon_path,
                 text_color, button_color, button_hover_color, txt_file_path, score):
        super().__init__()

        # define window
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.iconbitmap(icon_path)

        # set dark mode
        customtkinter.set_appearance_mode("dark")

        # define fonts, colors, and padding
        self.main_color = text_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.txt_file_path = txt_file_path
        # add score
        self.score = score

        # adding frames
        self.heading_frame = customtkinter.CTkFrame(master=self)
        self.input_frame = customtkinter.CTkFrame(master=self)
        self.warning_frame = customtkinter.CTkFrame(master=self)
        self.results_frame = customtkinter.CTkFrame(master=self)
        self.button_frame = customtkinter.CTkFrame(master=self)

        self.heading_frame.pack(padx=2, pady=2)
        self.input_frame.pack(padx=2, pady=2)
        self.warning_frame.pack(padx=2, pady=4)
        self.results_frame.pack(padx=2, pady=2)
        self.button_frame.pack(padx=2, pady=2)

        # Heading frame - add labels
        self.name_label = customtkinter.CTkLabel(self.heading_frame, width=100, height=13,
                                                 text="Reveal your name for the records...",
                                                 text_color=self.main_color)
        self.name_label.grid(row=0, column=0, padx=(0, 1), pady=2, ipadx=1, sticky="nw")
        self.score_label = customtkinter.CTkLabel(self.heading_frame, text="Score:",
                                                  width=290, height=13, text_color=self.main_color)
        self.score_label.grid(row=0, column=1, padx=(1, 0), pady=2, ipadx=1, sticky="nw")

        # results frame - create results list with scrollbar
        self.results_list = tkinter.Listbox(self.results_frame, width=35, height=13, selectborderwidth=3,
                                            bg="#000000", fg=self.main_color, font=("Verdana", 12))
        self.results_list.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar = customtkinter.CTkScrollbar(self.results_frame,
                                                        command=self.results_list.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_list.configure(yscrollcommand=vertical_scrollbar.set)

        # input frame - name input, score
        self.name_input = customtkinter.CTkEntry(self.input_frame, width=270)
        self.name_input.grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        self.score_label = customtkinter.CTkLabel(self.input_frame, text=self.score, width=120)
        self.score_label.grid(row=0, column=1, padx=4, pady=2, sticky="E")
        self.add_score_button = customtkinter.CTkButton(self.input_frame, text="Add score", width=10,
                                                        fg_color=self.button_color, hover_color=self.button_hover_color,
                                                        border_width=1, command=self.add_score)
        self.add_score_button.grid(row=0, column=2, padx=6, pady=2, ipadx=1, sticky="ne")
        # warning frame - warning info line (show warning when it is necessary)
        self.warning_info = customtkinter.CTkLabel(self.warning_frame, text="", width=478, height=10)
        self.warning_info.grid(row=0, column=0, padx=4, pady=4, ipadx=2, ipady=2, sticky="news")

        # button frame
        # creating buttons: to remove score, to clear the score list, to save score list and to quit the table

        self.remove_score = customtkinter.CTkButton(self.button_frame, text="Remove", width=5, border_width=1,
                                                    fg_color=self.button_color, hover_color=self.button_hover_color,
                                                    command=self.remove_score)
        self.clear_table = customtkinter.CTkButton(self.button_frame, text="Delete All", width=5, border_width=1,
                                                   fg_color=self.button_color, hover_color=self.button_hover_color,
                                                   command=self.delete_all_results)
        self.save_score = customtkinter.CTkButton(self.button_frame, text="Save", width=5, border_width=1,
                                                  fg_color=self.button_color, hover_color=self.button_hover_color,
                                                  command=self.save_results)
        self.quit_table = customtkinter.CTkButton(self.button_frame, text="Quit", width=5, border_width=1,
                                                  fg_color=self.button_color, hover_color=self.button_hover_color,
                                                  command=self.close_scoreboard)
        self.remove_score.grid(row=0, column=0, padx=5, pady=8, ipadx=10)
        self.clear_table.grid(row=0, column=1, padx=5, pady=8, ipadx=10)
        self.save_score.grid(row=0, column=2, padx=5, pady=8, ipadx=10)
        self.quit_table.grid(row=0, column=3, padx=5, pady=8, ipadx=10)

        # load results to the table
        self.after(100, self.load_results())

    def add_score(self):
        # Adds a new player and score to the list
        if self.check_player(self.name_input.get()):
            self.results_list.insert(tkinter.END, f"{self.name_input.get()} : {self.score}\n")
            self.name_input.delete(0, tkinter.END)
            self.score_label.configure(text="")
            self.warning_info.configure(text="")

    def check_player(self, player_name):
        results = self.results_list.get(0, tkinter.END)
        for one_line in results:
            if player_name in one_line:
                self.warning_info.configure(text="Name already used!!! "
                                                 "Remove old records first if you want to save your score.",
                                            text_color="red")
                return False
        self.warning_info.configure(text="")
        return True

    def remove_score(self):
        self.results_list.delete(tkinter.ANCHOR)

    def delete_all_results(self):
        self.results_list.delete(0, tkinter.END)

    def save_results(self):
        with open(self.txt_file_path, "w", encoding="utf8") as results_file:
            results = self.results_list.get(0, tkinter.END)
            for one_result in results:
                if one_result.endswith("\n"):
                    results_file.write(f"{one_result}")
                else:
                    results_file.write(f"{one_result}\n")

    def close_scoreboard(self):
        self.withdraw()
        self.quit()

    def load_results(self):
        # Loads tasks from a text file to show scoreboard
        try:
            with open(self.txt_file_path, "r", encoding="utf8") as results_file:
                for one_line in results_file:
                    self.results_list.insert(tkinter.END, one_line)
        except FileExistsError:
            print("Error. Cannot find file with tasks.")


# SCOREBOARD_TITLE = "Harry Potter: The Golden Snitch and The Dementor Clash"
# SCOREBOARD_GEOMETRY = "550x500+700+250"
# SCOREBOARD_ICON = "../assets/images/icons/hp_icon.ico"
# SCOREBOARD_FONT_TYPE_PATH = "../assets/fonts/Harry.ttf",
# SCOREBOARD_TEXT_COLOR = "#EEBA30"
# SCOREBOARD_BUTTON_COLOR = "#740001"
# SCOREBOARD_HOVER_COLOR = "#AE0001"
# SCOREBOARD_TXT_FILE_PATH = "../results/score.txt"
# scoreboard = Scoreboard(SCOREBOARD_TITLE, SCOREBOARD_GEOMETRY, SCOREBOARD_ICON, SCOREBOARD_TEXT_COLOR,
#                         SCOREBOARD_BUTTON_COLOR, SCOREBOARD_HOVER_COLOR, SCOREBOARD_TXT_FILE_PATH, 2555)
# scoreboard.mainloop()
