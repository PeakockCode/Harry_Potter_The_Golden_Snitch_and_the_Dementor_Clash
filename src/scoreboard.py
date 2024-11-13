# Import necessary modules
import tkinter
import customtkinter


class Scoreboard(customtkinter.CTk):

    def __init__(self, title, geometry, icon_path,
                 text_color, button_color, button_hover_color, txt_file_path, score):
        super().__init__()

        # Initialize the window with a title and geometry
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.iconbitmap(icon_path)

        # Set the appearance mode of the window to dark (using customtkinter)
        customtkinter.set_appearance_mode("dark")

        # Store the parameters for color schemes, text file path, and score
        self.main_color = text_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.txt_file_path = txt_file_path
        # add score
        self.score = score

        # Create frames to organize UI elements
        self.heading_frame = customtkinter.CTkFrame(master=self)
        self.input_frame = customtkinter.CTkFrame(master=self)
        self.warning_frame = customtkinter.CTkFrame(master=self)
        self.results_frame = customtkinter.CTkFrame(master=self)
        self.button_frame = customtkinter.CTkFrame(master=self)

        # Pack frames with some padding
        self.heading_frame.pack(padx=2, pady=2)
        self.input_frame.pack(padx=2, pady=2)
        self.warning_frame.pack(padx=2, pady=4)
        self.results_frame.pack(padx=2, pady=2)
        self.button_frame.pack(padx=2, pady=2)

        # Heading frame - Add labels to show game instructions and score
        self.name_label = customtkinter.CTkLabel(self.heading_frame, width=100, height=13,
                                                 text="Reveal your name for the records...",
                                                 text_color=self.main_color)
        self.name_label.grid(row=0, column=0, padx=(0, 1), pady=2, ipadx=1, sticky="nw")
        self.score_label = customtkinter.CTkLabel(self.heading_frame, text="Score:",
                                                  width=290, height=13, text_color=self.main_color)
        self.score_label.grid(row=0, column=1, padx=(1, 0), pady=2, ipadx=1, sticky="nw")

        # Results frame - Create a listbox with scrollbar to show the scoreboard
        self.results_list = tkinter.Listbox(self.results_frame, width=35, height=13, selectborderwidth=3,
                                            bg="#000000", fg=self.main_color, font=("Verdana", 12))
        self.results_list.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar = customtkinter.CTkScrollbar(self.results_frame,
                                                        command=self.results_list.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_list.configure(yscrollcommand=vertical_scrollbar.set)

        # Input frame - Provide entry field for player name and score display
        self.name_input = customtkinter.CTkEntry(self.input_frame, width=270)
        self.name_input.grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        self.score_label = customtkinter.CTkLabel(self.input_frame, text=self.score, width=120)
        self.score_label.grid(row=0, column=1, padx=4, pady=2, sticky="E")
        self.add_score_button = customtkinter.CTkButton(self.input_frame, text="Add score", width=10,
                                                        fg_color=self.button_color, hover_color=self.button_hover_color,
                                                        border_width=1, command=self.add_score)
        self.add_score_button.grid(row=0, column=2, padx=6, pady=2, ipadx=1, sticky="ne")
        # Warning frame - Display warning if any action is incorrect (e.g., duplicate name)
        self.warning_info = customtkinter.CTkLabel(self.warning_frame, text="", width=478, height=10)
        self.warning_info.grid(row=0, column=0, padx=4, pady=4, ipadx=2, ipady=2, sticky="news")

        # Button frame - Buttons to manage scores: remove, clear, save, and quit
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

        # Load results from the text file into the results list (after 100ms delay)
        self.after(100, self.load_results())

    # Function to add a new player and their score to the scoreboard if the player name is valid.
    def add_score(self):
        # Adds a new player and score to the list
        if self.check_player(self.name_input.get()):
            self.results_list.insert(tkinter.END, f"{self.name_input.get()} : {self.score}\n")
            self.name_input.delete(0, tkinter.END)
            self.score_label.configure(text="")
            self.warning_info.configure(text="")

    # Function to checks if the player name is already in the results list. Show the warning message if the name already exists.
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

    # Function to remove the selected score from the scoreboard.
    def remove_score(self):
        self.results_list.delete(tkinter.ANCHOR)

    # Function to clear all scores from the scoreboard.
    def delete_all_results(self):
        self.results_list.delete(0, tkinter.END)

    # Function to save the current results list to a text file.
    def save_results(self):
        with open(self.txt_file_path, "w", encoding="utf8") as results_file:
            results = self.results_list.get(0, tkinter.END)
            for one_result in results:
                if one_result.endswith("\n"):
                    results_file.write(f"{one_result}")
                else:
                    results_file.write(f"{one_result}\n")

    # Function to close the scoreboard window.
    def close_scoreboard(self):
        self.withdraw()
        self.quit()

    # Function to load the results from a text file and displays them in the scoreboard.
    def load_results(self):
        # Loads tasks from a text file to show scoreboard
        try:
            with open(self.txt_file_path, "r", encoding="utf8") as results_file:
                for one_line in results_file:
                    self.results_list.insert(tkinter.END, one_line)
        except FileExistsError:
            print("Error. Cannot find file with tasks.")
