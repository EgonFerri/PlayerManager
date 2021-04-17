from tkinter import Tk, Label, Button, INSERT, Text, Entry, Checkbutton, IntVar
import pickle
import math
import itertools
import random

class SportAlgorithm:
    # Initializations
    
    def __init__(self, master):
        # First page aestethics
        self.master = master
        master.title('Welcome to the Giorno Fisso')
        master.geometry("800x500")
        master.grid_columnconfigure(4, weight=1)
        master.configure(background="moccasin")

        # Load data
        try:
            with open('players.pkl', 'rb') as f:
                self.players = pickle.load(f)
        except:
            self.players = {}

        try:
            with open('reds.pkl', 'rb') as f:
                self.reds = pickle.load(f)
            with open('yellows.pkl', 'rb') as f:
                self.yellows = pickle.load(f)
        except:
            self.reds = set()
            self.yellows = set()

        self.play_list=list(self.players.keys())
        self.playing_players=set()
        self.first_page()

    def clean(self):
        for w in self.master.winfo_children():
            w.destroy()
        button_exit = Button(text='Exit', font=('verdana', 15),
                             command=self.master.destroy, background='palegoldenrod', foreground='Black')
        button_home = Button(text='Home', font=('verdana', 15),
                             command=self.first_page, background='palegoldenrod', foreground='Black')
        button_home.grid(row=30, sticky='SW', padx=10, pady=10)
        button_exit.grid(row=30, column=4, sticky='SE', pady=10, padx=10)

    def first_page(self):
        self.clean()

        welcome_label = Label(self.master,
                              text="Welcome to your sport manager app, what do you want to do?",
                              font=('verdana', 15),
                              background='moccasin',
                              foreground='black')

        button1 = Button(text='Show values', font=('verdana', 15),
                         command=self.show_values, background='palegoldenrod', foreground='Black')

        button2 = Button(text='Make teams', font=('verdana', 15),
                         command=self.player_loader, background='palegoldenrod', foreground='Black')

        button3 = Button(text='Adjust values', font=('verdana', 15),
                         command=self.new_values, background='palegoldenrod', foreground='Black')

        button4 = Button(text='Add players', font=('verdana', 15),
                         command=self.add_players, background='palegoldenrod', foreground='Black')

        button5 = Button(text='Delete players', font=('verdana', 15),
                         command=self.delete_players, background='palegoldenrod', foreground='Black')

        welcome_label.grid(row=0, column=0, sticky='N', padx=20, pady=10, columnspan=5)
        button1.grid(row=2, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
        button2.grid(row=3, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
        button3.grid(row=4, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
        button4.grid(row=5, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
        button5.grid(row=6, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
    
    # Show values
    
    def show_values(self):
        self.clean()
        res = sorted(self.players.items(), key=lambda key_value: key_value[1])
        text = Text()
        for i in res:
            text.insert(INSERT, str(i[0])+' '+str(i[1])+'\t\t')
        text.grid(row=3, column=0, padx=10, pady=30, columnspan=5)
        text.configure(background='moccasin', foreground='black',
                       height=12, font='verdana')
    
    # Generate and save teams

    def save_teams(self):
        with open('reds.pkl', 'wb') as f:
            pickle.dump(self.reds, f, pickle.HIGHEST_PROTOCOL)
        with open('yellows.pkl', 'wb') as f:
            pickle.dump(self.yellows, f, pickle.HIGHEST_PROTOCOL)
        lab = Label(self.master, text=f"SAVED TEAMS!",
                        font=('verdana', 20),
                        background='moccasin',
                        foreground='black')
        lab.grid(column=0,row=6, sticky='s', padx=20, columnspan=5)

    def make_teams(self, var):
        i = 0
        for v in var:
            if v.get() == 1:
                self.playing_players.add(self.play_list[i])
            i += 1
        if len(self.playing_players) != (10 or 16):
            lab = Label(text="Seleziona 10 o 16 giocatori!",
                           font=('verdana', 17),
                           background='moccasin',
                           foreground='darkred')
            lab.grid(row=29, column=0, padx=0, columnspan=5)

        else:
            self.clean()
            squadre = list(itertools.combinations(self.playing_players, int(len(self.playing_players)/2)))
            outcomes = []
            for squad in squadre:
                sq1 = set(squad)
                sq2 = set(self.playing_players)-sq1
                value1 = 0
                for pl in sq1:
                    value1 += self.players[pl]
                value2 = 0
                for pl in sq2:
                    value2 += self.players[pl]
                res = [round(abs(value1-value2), 1), sq1,
                    round(value1, 1), sq2, round(value2, 1)]
                outcomes.append(res)

            trial = random.sample(sorted(outcomes)[0:len(self.playing_players)], 1)
            self.reds = trial[0][1]
            val_reds = trial[0][2]
            self.yellows = trial[0][3]
            val_yellows = trial[0][4]
            text = Text()
            text.insert(INSERT, 'Reds: '+' '.join(self.reds)+' '+str(val_reds)+'\n \n \t \t \t vs \t \t \n \n' +
                        'Yellows: '+' '.join(self.yellows)+' '+str(val_yellows))
            text.grid(row=3, column=0, padx=10, pady=30, columnspan=5)
            text.configure(background='moccasin', foreground='black',
                       height=12, font='verdana')

            button_save = Button(text='save teams', font=('verdana', 15),
                                command=lambda: self.save_teams(), background='palegoldenrod', foreground='Black')
            button_save.grid(row=8, sticky='WE', padx=10, pady=10, columnspan=5)


            button_retry = Button(text='retry', font=('verdana', 15),
                                command=lambda: self.make_teams(var), background='palegoldenrod', foreground='Black')
            button_retry.grid(row=7, sticky='WE', padx=10, pady=10, columnspan=5)
    
    def player_loader(self):
        self.clean()
        row = 1
        col = 0
        var = []
    
        for i in range(len(self.play_list)):
            var.append(IntVar())
            Checkbutton(text=self.play_list[i], variable=var[i],
                        fg='black', bg='moccasin').grid(row=row, column=col, sticky='W')

            row += 1
            if row > math.ceil(len(self.play_list)/4):
                col += 1
                row = 1

        button_save = Button(text='\n\n\nMake teams\n\n\n', font=('verdana', 15),
                             command=lambda: self.make_teams(var), background='palegoldenrod', foreground='Black')
        button_save.grid(row=0,column=col+1, sticky='WE', padx=10, pady=10, columnspan=5, rowspan=10)
    
    # Adjust values
    
    def aggiornator(self, winners):
        if winners == 'reds':
            winners = self.reds
            losers = self.yellows
        else:
            winners = self.yellows
            losers = self.reds

        for c in winners:
            self.players[c] = round(self.players[c]+0.1, 1)
        for c in losers:
            self.players[c] = round(self.players[c]-0.1, 1)
        with open('players.pkl', 'wb') as f:
            pickle.dump(self.players, f, pickle.HIGHEST_PROTOCOL)
        lab = Label(self.master, text="DONE!",
                    font=('verdana', 40),
                    background='moccasin',
                    foreground='black')
        lab.grid(column=0, sticky='s', padx=20, columnspan=5)

    def new_values(self):
        self.clean()
        lab = Label(self.master, text="Who won?",
                    font=('verdana', 15),
                    background='moccasin',
                    foreground='black')

        button_r = Button(text='\n'.join(self.reds), font=('verdana', 15), command=lambda: self.aggiornator("reds"),
                          background='darkred', foreground='peach puff')
        button_y = Button(text='\n'.join(self.yellows), font=('verdana', 15), command=lambda: self.aggiornator("yellows"),
                          background='gold', foreground='DarkOrange4')

        lab.grid(row=0, column=0, sticky='N', padx=20, pady=10, columnspan=5)
        button_r.grid(row=1, column=0, sticky="WE", pady=10, padx=10, columnspan=5)
        button_y.grid(row=2, column=0, sticky="WE", pady=10, padx=10, columnspan=5)

    # Add a player
    
    def save_player(self, player, value):
        self.players[player]=int(value)
        with open('players.pkl', 'wb') as f:
            pickle.dump(self.players, f, pickle.HIGHEST_PROTOCOL)
        lab = Label(self.master, text=f"SAVED {player} with value {value}!",
                        font=('verdana', 20),
                        background='moccasin',
                        foreground='black')
        lab.grid(column=0, sticky='s', padx=20, columnspan=5)
        
    def add_players(self):
        self.clean()
        lab = Label(self.master, text="Add a player",
                    font=('verdana', 15),
                    background='moccasin',
                    foreground='black')
        l1 = Label(self.master, text="Player name:",
                   font=('verdana', 15),
                   background='moccasin',
                   foreground='black')
        l2 = Label(self.master, text="Player first value:",
                   font=('verdana', 15),
                   background='moccasin',
                   foreground='black')

        e1 = Entry(self.master, width=40, bd=3,
                   bg='peach puff', font=('verdana', 15))
        e2 = Entry(self.master, width=40, bd=3,
                   bg='peach puff', font=('verdana', 15))

        lab.grid(row=0, sticky='N', padx=10, pady=10, columnspan=5)
        l1.grid(row=1, sticky="W", pady=10, padx=10, columnspan=5)
        l2.grid(row=2, sticky="W", pady=10, padx=10, columnspan=5)
        e1.grid(row=1, sticky="E", pady=10, padx=10, columnspan=5)
        e2.grid(row=2, sticky="E", pady=10, padx=10, columnspan=5)
        
        button_save = Button(text='Save', font=('verdana', 15),
                             command=lambda: self.save_player(e1.get(), e2.get()), background='palegoldenrod', foreground='Black')
        button_save.grid(row=7, sticky='WE', padx=10, pady=10, columnspan=5)

    # Remove a player

    def savedel_player(self, player):
        del self.players[player]
        with open('players.pkl', 'wb') as f:
            pickle.dump(self.players, f, pickle.HIGHEST_PROTOCOL)
        lab = Label(self.master, text=f"DELETED {player}!",
                        font=('verdana', 40),
                        background='moccasin',
                        foreground='black')
        lab.grid(column=0, sticky='s', padx=20, columnspan=5)
        
    def delete_players(self):
        self.clean()
        lab = Label(self.master, text="Delete a player",
                    font=('verdana', 15),
                    background='moccasin',
                    foreground='black')
        l1 = Label(self.master, text="Player name:",
                   font=('verdana', 15),
                   background='moccasin',
                   foreground='black')

        e1 = Entry(self.master, width=40, bd=3,
                   bg='peach puff', font=('verdana', 15))

        lab.grid(row=0, sticky='N', padx=10, pady=10, columnspan=5)
        l1.grid(row=1, sticky="W", pady=10, padx=10, columnspan=5)
        e1.grid(row=1, sticky="E", pady=10, padx=10, columnspan=5)
        
        button_save = Button(text='Delete', font=('verdana', 15),
                             command=lambda: self.savedel_player(e1.get()), background='palegoldenrod', foreground='Black')
        button_save.grid(row=7, sticky='WE', padx=10, pady=10, columnspan=5)

root = Tk()
my_gui = SportAlgorithm(root)
root.mainloop()
