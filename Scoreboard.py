from CheckoutDict import CheckoutDict
from Player import Player
import tkinter as tk


class Scoreboard(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Darts Scoreboard by ptl")
        self.geometry("800x700")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.suspended = False
        self.checkouts = CheckoutDict()

        for F in (StartPage, MatchOptionsPage, MatchPage, TrainingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, font=(None, 40), text="Select game mode:").pack()

        tk.Button(self, font=(None, 28), width=20, text="TRAINING 301",
                  command=lambda: self.go_to_training(301)).pack(pady=6)
        tk.Button(self, font=(None, 28), width=20, text="TRAINING 501",
                  command=lambda: self.go_to_training(501)).pack(pady=6)
        tk.Button(self, font=(None, 28), width=20, text="MATCH",
                  command=lambda: controller.show_frame(MatchOptionsPage)).pack(pady=6)
        tk.Button(self, font=(None, 28), width=20, text="EXIT APP",
                  command=lambda: controller.destroy()).pack(pady=30)

    def go_to_training(self, mode):
        frame = self.controller.frames[TrainingPage]
        frame.mode.set(mode)
        frame.player.reset()
        frame.player.entry.focus_set()

        self.controller.show_frame(TrainingPage)


class MatchOptionsPage(tk.Frame):

    ''' contains variables: sets, legs, mode'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.sets = tk.IntVar()
        self.sets.set(1)

        self.legs = tk.IntVar()
        self.legs.set(1)

        self.padx = 20
        self.mode = 0

        self.inside_frame = tk.Frame(self)
        self.inside_frame.place(relx=0.1, relwidth=0.8)

        self.inside_frame.columnconfigure(1, weight=1)
        self.inside_frame.columnconfigure(0, weight=1, pad=20)

        for i in range(7):
            if i != 1:
                self.inside_frame.rowconfigure(i, pad=25)

        tk.Label(self.inside_frame, font=(None, 40), text="Select game options:").grid(row=0, column=0, columnspan=2)
        tk.Label(self.inside_frame, font=(None, 30), text="Player 1 name:").grid(row=1, column=0, sticky="we")
        tk.Label(self.inside_frame, font=(None, 30), text="Player 2 name:").grid(row=1, column=1, sticky="we")

        # players names entries
        self.p1_entry = tk.Entry(self.inside_frame, font=(None, 30))
        self.p1_entry.grid(row=2, column=0, sticky="we", padx=self.padx)
        self.p2_entry = tk.Entry(self.inside_frame, font=(None, 30))
        self.p2_entry.grid(row=2, column=1, sticky="we", padx=self.padx)

        # text labels
        tk.Label(self.inside_frame, font=(None, 30), text="SETS (first to):") \
            .grid(row=3, column=0, sticky="e", padx=self.padx)
        tk.Label(self.inside_frame, font=(None, 30), text="LEGS (first to):") \
            .grid(row=4, column=0, sticky="e", padx=self.padx)

        # # inc and dec buttons to set sets and legs
        tk.Spinbox(self.inside_frame, font=(None, 30), textvariable=self.sets, from_=1, to=99,
                   width=2, state='readonly').grid(row=3, column=1, sticky="w", padx=self.padx)
        tk.Spinbox(self.inside_frame, font=(None, 30), textvariable=self.legs, from_=1, to=99,
                   width=2, state='readonly').grid(row=4, column=1, sticky="w", padx=self.padx)

        # buttons to set the game mode (301 or 501)
        tk.Button(self.inside_frame, font=(None, 25), text="301 GAME", command=lambda: self.set_mode(301))\
            .grid(row=5, column=0, sticky="e", padx=self.padx)
        tk.Button(self.inside_frame, font=(None, 25), text="501 GAME", command=lambda: self.set_mode(501))\
            .grid(row=5, column=1, sticky="w", padx=self.padx)

        # confirm button
        self.confirm = tk.Button(self.inside_frame, font=(None, 30), text="Select mode above", bg='red',
                                 command=lambda: self.on_confirm())
        self.confirm.grid(row=6, column=0, columnspan=2, sticky="we", padx=self.padx)

        #go back button
        tk.Button(self.inside_frame, font=(None, 28), text="Go back",
                  command=lambda: controller.show_frame(StartPage)).grid(row=7, column=1)

    def set_mode(self, value):
        self.mode = value
        self.confirm.configure(text="Play a {} game".format(self.mode), bg='green')

    def on_confirm(self):
        if self.mode != 0:

            # there is no point in playing a few sets with single legs,
            # so we switch legs with sets to make a single set
            if self.sets.get() > 1 and self.legs.get() == 1:
                self.sets, self.legs = self.legs, self.sets

            match_page = self.controller.frames[MatchPage]
            match_page.mode.set(self.mode)
            p1_entry = self.p1_entry.get()
            if p1_entry != "":
                match_page.player1.player_name.set(p1_entry)
            else:
                match_page.player1.player_name.set("Player 1")

            p2_entry = self.p2_entry.get()
            if p2_entry != "":
                match_page.player2.player_name.set(p2_entry)
            else:
                match_page.player2.player_name.set("Player 2")

            match_page.player1.score = self.mode
            match_page.player2.score = self.mode

            match_page.player1.scoreboard.configure(text=self.mode)
            match_page.player2.scoreboard.configure(text=self.mode)

            match_page.legs_first_to = self.legs.get()
            match_page.sets_first_to = self.sets.get()

            match_page.player1.get_entry_focus()
            match_page.player2.lose_entry_focus()


            # info string contains information about game type that is displayed in top banner
            info = "{} GAME".format(self.mode)

            sets = self.sets.get()
            legs = self.legs.get()
            if sets > 1:
                info += ", FIRST TO {} SETS".format(sets)
            else:
                info += ", SINGLE SET"
            if legs > 1:
                info += ", FIRST TO {} LEGS".format(legs)
            else:
                info += ", SINGLE LEG"
            match_page.top_label.configure(text=info)

            print("Confirmuję mecz: sety, legi: ", sets, legs)
            if sets == 1:
                # delete displaying set scores for players
                match_page.player1.display_legs_only()
                match_page.player2.display_legs_only()
            else:
                match_page.player1.display_sets_and_legs()
                match_page.player2.display_sets_and_legs()

            self.controller.show_frame(MatchPage)

    def reset(self):
        self.mode = 0
        self.p1_entry.delete(0, "end")
        self.p2_entry.delete(0, "end")
        self.sets.set(1)
        self.legs.set(1)
        self.confirm.configure(text="Select mode above", bg='red')


class MatchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.mode = tk.IntVar()
        self.mode.set(0)

        self.legs_first_to = -1
        self.sets_first_to = -1

        self.move_made = False
        self.leg_flag = False
        self.set_flag = False

        self.player1 = Player(self, "Player 1", "yellow", 0)
        self.player2 = Player(self, "Player 2", "cyan", 1)

        self.top_label = top_banner(self, "", lambda: warning_window(self))
        self.player1.entry.bind("<Escape>", lambda x: warning_window(self))
        self.player2.entry.bind("<Escape>", lambda x: warning_window(self))

        self.player1.entry.bind("<Return>", lambda x: self.on_entry_input(self.player2), add="+")
        self.player2.entry.bind("<Return>", lambda x: self.on_entry_input(self.player1), add="+")

    def on_entry_input(self, player_to_turn):
        if self.move_made:
            self.switch_turn_to(player_to_turn)
        self.move_made = False

    def on_back(self):
        self.controller.show_frame(StartPage)
        self.player1.hard_reset()
        self.player2.hard_reset()
        try:
            self.win.destroy()
        except:
            pass
        try:
            self.warn_win.destroy()
        except:
            pass
        self.controller.frames[MatchOptionsPage].reset()


    def switch_turn_to(self, player_to_turn):
        if player_to_turn == self.player1:
            self.player1.get_entry_focus()
            self.player2.lose_entry_focus()
        else:
            self.player2.get_entry_focus()
            self.player1.lose_entry_focus()

    def on_leg_won(self, winning_player):
        if winning_player == self.player1:
            losing_player = self.player2
        else:
            losing_player = self.player1
        losing_player.reset()

        winning_player.legs_won.set(winning_player.legs_won.get() + 1)

        # set won
        if winning_player.legs_won.get() == self.legs_first_to:
            self.set_flag = True
            print("Game shot and a set!")
            winning_player.sets_won.set(winning_player.sets_won.get() + 1)

            if winning_player.sets_won.get() == self.sets_first_to:
                self.on_match_won(winning_player.player_name.get())

            if self.sets_first_to != 1:
                winning_player.legs_won.set(0)
                losing_player.legs_won.set(0)

        print("Set, leg =", self.current_set(), self.current_leg())
        set = self.current_set()
        leg = self.current_leg()
        if (set % 2 == 1 and leg % 2 == 1) or (set % 2 == 0 and leg % 2 == 0):
            self.switch_turn_to(self.player1)
            print("Focus powinien mieć p1")
        else:
            self.switch_turn_to(self.player2)
            print("Focus powinien mieć p2")

    def on_match_won(self, player_name):
        self.controller.suspended = True

        self.player1.lose_entry_focus()
        self.player2.lose_entry_focus()

        self.win = tk.Frame(self, borderwidth=3, relief="solid")
        self.win.place(relx=.5, rely=.4, anchor="center")
        message = "Game shot\nand the match,\n{}!".format(player_name)
        tk.Label(self.win, font=(None, 38), text=message).pack()
        tk.Button(self.win, font=(None, 20), text="Play again", command=lambda: on_again(), bg='white', padx=10)\
            .pack(side=tk.LEFT, fill="both", expand=True, padx=20)

        tk.Button(self.win, font=(None, 20), text="Main menu", command=lambda: on_exit(), bg='white', padx=10)\
            .pack(side=tk.LEFT, fill="both", expand=True, padx=20)

        def on_exit():
            self.win.destroy()
            self.on_back()
            self.controller.suspended = False

        def on_again():
            self.win.destroy()
            self.player1.hard_reset()
            self.player2.hard_reset()
            self.player1.get_entry_focus()
            self.controller.suspended = False

    def current_set(self):
        return self.player1.sets_won.get() + self.player2.sets_won.get() + 1

    def current_leg(self):
        return self.player1.legs_won.get() + self.player2.legs_won.get() + 1


class TrainingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = tk.IntVar()
        self.mode.set(0)

        self.player = Player(self, "", "lightgreen", 0.5)
        self.player.get_entry_focus()

        self.top_label = top_banner(self, "TRAINING GAME", lambda: warning_window(self))
        self.player.entry.bind("<Escape>", lambda x: warning_window(self))


    def on_back(self):
        self.controller.show_frame(StartPage)
        self.player.hard_reset()

    def on_leg_won(self, xd):
        self.player.legs_won.set(self.player.legs_won.get() + 1)


def top_banner(parent, text, function):
    top = tk.Frame(parent, bg=Player.bgcolor)
    top.place(relwidth=1, relheight=0.05)
    label = tk.Label(top, font=(None, 16), bg=Player.bgcolor, fg=Player.fgcolor, text=text)
    label.place(relx=.5, rely=.5, anchor="center")
    tk.Button(top, font=(None, 16), text="GO BACK", command=function, width=10).pack(side=tk.RIGHT)
    return label


def warning_window(frame):
    frame.controller.suspended = True
    frame.warn_win = tk.Frame(frame, borderwidth=3, relief="solid")
    frame.warn_win.place(relx=.5, rely=.3, anchor="center")
    message = "Are you sure you want to return to the main menu?\nThis game's stats will be deleted."
    tk.Label(frame.warn_win, font=(None, 20), text=message, height=3, bd=20).pack()
    tk.Button(frame.warn_win, font=(None, 22), text="Yes (Enter)", command=lambda: on_exit(), bg='red', fg='white')\
        .pack(side=tk.LEFT, fill="both", expand=True, padx=30, pady=20)
    tk.Button(frame.warn_win, font=(None, 22),  text="No (Escape)", command=lambda: on_stay(), bg='green', fg='white')\
        .pack(side=tk.LEFT, fill="both", expand=True, padx=30, pady=20)
    previously_focused = frame.focus_get()
    frame.focus_set()
    frame.bind('<Return>', lambda x: on_exit())
    frame.bind('<Escape>', lambda x: on_stay())

    def on_exit():
        frame.warn_win.destroy()
        frame.on_back()
        frame.controller.suspended = False

    def on_stay():
        frame.warn_win.destroy()
        frame.controller.suspended = False
        previously_focused.focus_set()


if __name__ == '__main__':
    Scoreboard()

