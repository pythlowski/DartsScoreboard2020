import tkinter as tk
# import playsound


class Player:
    bgcolor = '#333333'
    fgcolor = 'white'
    active_entry_color = '#f6da63'

    def __init__(self, root, player_name, player_color, position):

        self.root = root
        self.position = position

        self.player_name = tk.StringVar()
        self.player_name.set(player_name)

        self.player_color = player_color

        # statistics
        self.statistics = {
            'pts_overall': 0,
            'darts_thrown': 0,
            'average': 0,
            'count180s': 0,
            'count170plus': 0,
            'count130plus': 0,
            'count90plus': 0,
            'top_checkout': 0,
            'top_throw': 0,
            'ton_plus_checkouts_list': []
        }

        self.legs_won = tk.IntVar()
        self.legs_won.set(0)

        self.sets_won = tk.IntVar()
        self.sets_won.set(0)

        self.SPACE = 0.01
        self.WIDTH2 = (1 - self.SPACE) / 2

        self.score = -1

        if self.position == 0.5:
            self.relx1 = 0
            self.relx2 = 0.51
        else:
            self.relx1 = 0.51 * self.position
            self.relx2 = 0.51 * (not self.position)

        self.frame = tk.Frame(root, bg=self.player_color, bd=10)
        self.frame.place(relx=0.01 + self.position * 0.5, rely=0.05, relwidth=0.485, relheight=0.98)

        self.frame1 = tk.Frame(self.frame, bg=self.player_color)
        self.frame1.place(relwidth=self.WIDTH2, relheight=1)

        self.frame2 = tk.Frame(self.frame, bg=self.player_color)
        self.frame2.place(relx=self.WIDTH2 + self.SPACE, relwidth=self.WIDTH2, relheight=1)

        if self.position == 1:
            tmp = self.frame2
            self.frame2 = self.frame1
            self.frame1 = tmp

        self.checkout_string = ""
        self.checkout_label = tk.Label(self.frame1, font=(None, 22, 'bold'), text=self.checkout_string,
                                       bg=self.fgcolor, fg='red', borderwidth=4, relief="solid")

        # statistics

        self.avg_label = self.statistics_elements("AVG", "---", 0.32)
        self.count180s_label = self.statistics_elements("180s", 0, 0.38)
        self.count170plus_label = self.statistics_elements("170+", 0, 0.44)
        self.count130plus_label = self.statistics_elements("130+", 0, 0.5)
        self.count90plus_label = self.statistics_elements("90+", 0, 0.56)
        self.top_checkout_label = self.statistics_elements("top check", "---", 0.62)
        self.top_throw_label = self.statistics_elements("top throw", "---", 0.68)

        tk.Label(self.frame1, font=(None, 15), text="Ton+ checkouts", bg=self.bgcolor, fg=self.fgcolor) \
            .place(rely=0.74, relwidth=1, relheight=0.05)
        self.ton_plus_checkouts_list_label = tk.Label(self.frame1, font=(None, 15), text="---", bg=self.bgcolor, fg=self.fgcolor)
        self.ton_plus_checkouts_list_label.place(rely=0.8, relwidth=1, relheight=0.07)

        self.scoreboard = tk.Label(self.frame2, font=(None, 50), text=self.score, bg=self.bgcolor, fg=self.fgcolor)
        self.scoreboard.place(rely=0.12, relwidth=1, relheight=0.11)

        ####
        vcmd = root.register(self.callback)
        self.entry = tk.Entry(self.frame1, font=(None, 50),
                              validate='key', validatecommand=(vcmd, '%P'), state=tk.DISABLED)
        self.entry.place(rely=0.12, relwidth=1, relheight=0.11)

        self.entry.bind('<Return>', self.on_score_input)

        tk.Label(self.frame1, font=(None, 30), textvariable=self.player_name, bg=self.bgcolor, fg=self.fgcolor)\
            .place(relwidth=1, relheight=0.11)

        self.turnsFrame = tk.Frame(self.frame, bg=self.player_color)

        if self.position == 0.5:
            relx = self.WIDTH2 + self.SPACE
        else:
            relx = (self.WIDTH2 + self.SPACE) * (not self.position)
        self.turnsFrame.place(rely=0.24, relx=relx, relwidth=self.WIDTH2, relheight=0.72)
        self.turnsLabels = []

        if self.position == 0.5: # trening
            self.legs_label = tk.Label(self.frame, font=(None, 26),
                                       text="PLAYED: 0", bg=self.bgcolor, fg=self.fgcolor)
            self.legs_label.place(relwidth=1, relheight=0.11)
        else:
            self.score_frame = tk.Frame(self.frame2, bg=self.player_color)
            self.score_frame.place(relheight=0.11, relwidth=1)
            self.sets_label = tk.Label(self.score_frame, font=(None, 55),
                                       textvariable=self.sets_won, bg=self.bgcolor, fg=self.fgcolor)

            self.sets_txt = tk.Label(self.score_frame, font=(None, 11, 'bold '),
                                     text="S\nE\nT\nS", bg=self.bgcolor, fg=self.fgcolor)

            self.legs_label = tk.Label(self.score_frame, font=(None, 45),
                                       textvariable=self.legs_won, bg=self.bgcolor, fg=self.fgcolor)

            self.legs_txt = tk.Label(self.score_frame, font=(None, 11, 'bold'),
                                     text="L\nE\nG\nS", bg=self.bgcolor, fg=self.fgcolor)

            self.display_sets_and_legs()

    def callback(self, P):
        if not self.root.controller.suspended and (str.isdigit(P) or P == ""):
            return True
        else:
            return False

    def display_legs_only(self):
        self.sets_label.place_forget()
        self.sets_txt.place_forget()
        self.legs_txt.place(relx=(self.relx1 + self.relx2)/2, relheight=1, relwidth=0.1)
        self.legs_label.place(relx=(self.relx1 + self.relx2)/2 + 0.12, relheight=1, relwidth=0.37)
        self.legs_label.configure(font=(None, 55))

    def display_sets_and_legs(self):
        self.legs_label.configure(font=(None, 45))
        self.sets_label.place(relx=self.relx2 + 0.12, relheight=1, relwidth=0.37)
        self.sets_txt.place(relx=self.relx2, relheight=1, relwidth=0.1)
        self.legs_label.place(relx=self.relx1 + 0.12, relheight=1, relwidth=0.37)
        self.legs_txt.place(relx=self.relx1, relheight=1, relwidth=0.1)

    def statistics_elements(self, text, variable, _rely):
        tk.Label(self.frame1, font=(None, 15), text=text, bg=self.bgcolor, fg=self.fgcolor) \
            .place(rely=_rely, relwidth=self.WIDTH2 - self.SPACE / 2, relheight=0.05)
        label = tk.Label(self.frame1, font=(None, 15), text=variable, bg=self.bgcolor, fg=self.fgcolor)
        label.place(rely=_rely, relx=self.WIDTH2 + 2 * self.SPACE, relwidth=self.WIDTH2 - self.SPACE/2, relheight=0.05)
        return label

    def on_score_input(self, event=None):
        round_score = self.entry_correctness()
        print('Round score: {}'.format(round_score))
        if round_score != -1:
            self.root.move_made = True
            if round_score == 0 or round_score == self.score:
                self.ns_win = self.no_score_window(round_score)
            else:
                self.parse_round_score(round_score)

    def entry_correctness(self):
        entry = self.entry.get()
        if entry and not self.root.controller.suspended:
            entry = int(entry)
            if 0 <= entry <= 180 and entry <= self.score and entry != self.score - 1:
                return entry
        return -1

    def no_score_window(self, score):
        self.root.controller.suspended = True
        win = tk.Frame(self.frame, borderwidth=3, relief="solid")
        win.place(relx=.5, rely=.2, anchor="center")
        message = "How many darts\nhave you thrown in this round?"
        tk.Label(win, font=(None, 18), text=message, height=3).pack()
        tk.Button(win, font=(None, 22), text=1, command=lambda: subf(1), bg='white')\
            .pack(side=tk.LEFT, fill="both", expand=True, padx=20, pady=10)
        tk.Button(win, font=(None, 22),  text=2, command=lambda: subf(2), bg='white')\
            .pack(side=tk.LEFT, fill="both", expand=True, padx=20, pady=10)
        tk.Button(win, font=(None, 22),  text=3, command=lambda: subf(3), bg='white')\
            .pack(side=tk.LEFT, fill="both", expand=True, padx=20, pady=10)
        win.focus_set()
        win.bind('1', lambda x: subf(1))
        win.bind('2', lambda x: subf(2))
        win.bind('3', lambda x: subf(3))

        def subf(count):
            if count == 1:
                self.statistics['darts_thrown'] -= 2
            if count == 2:
                self.statistics['darts_thrown'] -= 1
            win.destroy()
            self.parse_round_score(score)
            self.root.controller.suspended = False
            self.delete_entry()
            self.entry.focus_set()
            try:
                self.root.switch_turn()
            except:
                pass

        return win

    def parse_round_score(self, round_score):
        self.delete_entry()
        self.score -= round_score
        if round_score != 0:
            self.scoreboard.configure(text=self.score)

        self.statistics['darts_thrown'] += 3
        self.statistics['pts_overall'] += round_score
        if round_score == 180:
            self.statistics['count180s'] += 1
            self.count180s_label.configure(text=self.statistics['count180s'])
            # playsound.playsound("180.mp3")
        elif round_score >= 170:
            self.statistics['count170plus'] += 1
            self.count170plus_label.configure(text=self.statistics['count170plus'])
        elif round_score >= 130:
            self.statistics['count130plus'] += 1
            self.count130plus_label.configure(text=self.statistics['count130plus'])
        elif round_score >= 90:
            self.statistics['count90plus'] += 1
            self.count90plus_label.configure(text=self.statistics['count90plus'])

        if round_score >= self.statistics['top_throw']:
            self.statistics['top_throw'] = round_score
            self.top_throw_label.configure(text=round_score)

        self.calc_average()

        tl_len = len(self.turnsLabels)
        if tl_len < 28:
            turn = tk.Label(self.turnsFrame, font=(None, 16), text=round_score, bg='#4c4c4c', fg=self.fgcolor)
            turn.place(rely=tl_len/2 * 0.07, relx=self.relx1, relwidth=0.49, relheight=0.06)

            left = tk.Label(self.turnsFrame, font=(None, 20), text=self.score, bg='#4c4c4c', fg=self.fgcolor)
            left.place(rely=tl_len/2 * 0.07, relx=self.relx2, relwidth=0.49, relheight=0.06)

            self.turnsLabels.append(turn)
            self.turnsLabels.append(left)

        self.checkout_label.place_forget()

        if self.score <= 170:
            self.checkout_string = self.root.controller.checkouts.dict.get(self.score, "")

            if self.checkout_string != "" and self.score > 0:
                self.checkout_label.configure(text=self.checkout_string)
                self.checkout_label.place(rely=0.24, relwidth=1, relheight=0.07)

        if self.score == 0:
            self.parse_checkout(round_score)
            self.reset()

    def calc_average(self):
        avg = 3 * self.statistics['pts_overall'] / self.statistics['darts_thrown']
        self.statistics['average'] = avg
        self.avg_label.configure(text="{:.2f}".format(avg))

    def parse_checkout(self, checkout_score):
        if checkout_score >= self.statistics['top_checkout']:
            self.statistics['top_checkout'] = checkout_score
            self.top_checkout_label.configure(text=checkout_score)

        if checkout_score >= 100:
            ch_list = self.statistics['ton_plus_checkouts_list']
            if len(ch_list) < 8:
                ch_list.append(checkout_score)
            elif checkout_score > ch_list[-1]:
                ch_list[-1] = checkout_score
            ch_list.sort(reverse=True)
            self.ton_plus_checkouts_list_label.configure(text=self.to_string(ch_list))

    def to_string(self, numbers_list):
        ret_str = ""
        for index, number in enumerate(numbers_list):
            if index > 0:
                if len(numbers_list) >= 5 and index == 4:
                    ret_str += "\n"
                else:
                    ret_str += ", "
            ret_str += str(number)
        return ret_str

    def get_entry_focus(self):
        # if self.root.focus_get() != self.entry:
        self.entry.configure(state=tk.NORMAL, bg=Player.active_entry_color)
        self.entry.focus()

    def lose_entry_focus(self):
        # if self.root.focus_get() == self.entry:
        self.entry.configure(state=tk.DISABLED)

    def delete_entry(self):
        if self.entry['state'] == tk.DISABLED:
            self.entry.configure(state=tk.NORMAL)
            self.entry.delete(0, "end")
            self.entry.configure(state=tk.DISABLED)
        else:
            self.entry.delete(0, "end")
            self.entry.delete(0, "end")

    def reset(self):
        if self.score == 0:
            self.root.on_leg_won(self)

        self.checkout_label.place_forget()
        self.checkout_string = ""
        self.delete_entry()
        self.score = self.root.mode.get()
        self.scoreboard.configure(text=self.score)
        for label in self.turnsLabels:
            label.destroy()
        self.turnsLabels = []

        if self.position == 0.5:
            self.legs_label.configure(text="GAMES PLAYED: {}".format(self.legs_won.get()))

    def hard_reset(self):
        self.reset()
        self.legs_won.set(0)
        self.sets_won.set(0)
        self.statistics['pts_overall'] = 0
        self.statistics['darts_thrown'] = 0
        self.statistics['average'] = 0
        self.avg_label.configure(text="---")

        self.statistics['count180s'] = 0
        self.count180s_label.configure(text=0)

        self.statistics['count170plus'] = 0
        self.count170plus_label.configure(text=0)

        self.statistics['count130plus'] = 0
        self.count130plus_label.configure(text=0)

        self.statistics['count90plus'] = 0
        self.count90plus_label.configure(text=0)

        self.statistics['top_checkout'] = 0
        self.top_checkout_label.configure(text="---")

        self.statistics['top_throw'] = 0
        self.top_throw_label.configure(text="---")

        self.statistics['ton_plus_checkouts_list'] = []
        self.ton_plus_checkouts_list_label.configure(text="---")

        try:
            self.ns_win.destroy()
        except:
            pass



