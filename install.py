# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 08:37:44 2020

@author: Gfrkad
"""
import sys

import mysql.connector as sql

from tkinter.ttk import *

from tkinter import *

from time import sleep


class installation_win:
    def __init__(self, master):
        self.master = master
        master.title("Installation")
        master.iconphoto(False, PhotoImage(file = "reqs/logo.png"))
        
        self.Musicwww = Label(master, text = "Music.www",font = ("Courrier",20), bg="#252525", fg = "#c2c2c2")
        self.required = Label(master, text = "Mysql Must be installed", font = ("Courrier", 7), bg="#252525", fg = "#c2c2c2")
        self.mysql_user_label = Label(master, text = "Mysql Username:-", bg="#252525", fg = "#c2c2c2")
        self.mysql_user = Entry(master, relief = RIDGE, bg="#252525", fg = "#c2c2c2")
        self.mysql_pass_label = Label(master, text = "Mysql Password:-", bg="#252525", fg = "#c2c2c2")
        self.mysql_pass = Entry(master, relief = RIDGE, bg="#252525", fg = "#c2c2c2")
        self.email_id_label = Label(master, text = "Email id:-", bg="#252525", fg = "#c2c2c2")
        self.email_id = Entry(master, relief = RIDGE, bg="#252525", fg = "#c2c2c2")
        self.email_pass_label = Label(master, text = "Email password:-", bg="#252525", fg = "#c2c2c2")
        self.email_pass = Entry(master, relief = RIDGE, show = "*", bg="#252525", fg = "#c2c2c2")
        self.submit = Button(master, text ="Next", command = self.on_submit, bg="#252525", fg = "#c2c2c2")
        master.bind("<Return>", self.on_submit)
        
        self.Musicwww.grid(row = 0, column = 0, columnspan = 3)
        self.required.grid(row = 1, column = 0, columnspan = 3)
        self.mysql_user_label.grid(row = 2, column = 0, columnspan = 2)
        self.mysql_user.grid(row = 2, column = 2, columnspan = 1)
        self.mysql_pass_label.grid(row = 3, column = 0, columnspan = 2)
        self.mysql_pass.grid(row = 3, column = 2, columnspan = 1)
        self.email_id_label.grid(row = 4, column = 0, columnspan = 1)
        self.email_id.grid(row = 4, column = 1, columnspan = 2)
        self.email_pass_label.grid(row = 5, column = 0, columnspan = 2)
        self.email_pass.grid(row = 5, column = 2, columnspan = 1)
        self.submit.grid(row = 10, column = 0, columnspan = 3)
    
    def on_submit(self, n = 0):
        global host, user, passw
        host = "localhost"
        user = self.mysql_user.get()
        passw = self.mysql_pass.get()
        email_id = self.email_id.get()
        email_pass = self.email_pass.get()
        self.mysql_user.delete(0, len(user) + 1)
        self.mysql_pass.delete(0, len(passw) + 1)
        self.email_id.delete(0, len(email_id) + 1)
        self.email_pass.delete(0, len(email_pass) + 1)
        root.destroy()
        loading = True
        self.install_pic_win()
        #store user and pass of mysql
        with open("user.txt", "w") as file:
            file.write(user)
        with open("passw.txt", "w") as file:
            file.write(passw)
        #store user and passw of email
        with open("email.txt", "w") as file:
            file.write(email_id)
        with open("email_pass.txt", "w") as file:
            file.write(email_pass)
        
    def install_pic_win(self):
        global progress
        global root2
        root2 = Tk()
        root2.title("Installation")
        root2.iconphoto(False, PhotoImage(file = "reqs/logo.png"))
        img = PhotoImage(file = "reqs/Installation-img.png")
        panel = Label(root2, image = img)
        panel.pack(side = "top", fill = "both", expand = "yes")
        progress = Progressbar(root2, orient = HORIZONTAL, length = 500, mode = 'determinate')
        progress.pack()
        progress['value'] = 20
        self.progress()
        root2.mainloop()
    
    def progress(self):
        global con
        global crsr
        con = sql.connect(host = host, user = user, passwd = passw)
        if con.is_connected():
            progress['value'] = 50
        else:
            sys.exit()
        crsr = con.cursor()
        progress['value'] = 70
        try:
            crsr.execute("DROP DATABASE mwww")
        except:
            pass
        qry = "CREATE DATABASE mwww"
        crsr.execute(qry)
        qry = "USE mwww"
        crsr.execute(qry)
        progress['value'] = 80
        qry = "CREATE TABLE favourites (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, song char(255))"
        crsr.execute(qry)
        qry = "CREATE TABLE recents (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, song char(255))"
        crsr.execute(qry)
        qry = "CREATE TABLE other (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, song char(255))"
        crsr.execute(qry)
        qry = "CREATE TABLE playlists (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, song char(255))"
        crsr.execute(qry)
        for i in ["pl1", "pl2", "pl3", "pl4"]:
            self.create_playlist(i)
        progress['value'] = 90
        progress['value'] = 100
        sleep(1)
        nextt = Button(root2, text = 'Finish', bd = '5', command = self.finish)
        nextt.pack()
    
    
    #create playlist
    def create_playlist(self, name_of_playlist):
        crsr.execute("SELECT song FROM playlists")
        no_of_pl = len(crsr.fetchall())
        
        if no_of_pl < 5:
            #insert into playlists table
            playlists_table_qry = "INSERT INTO playlists (song) values ('{}')".format(name_of_playlist)
            crsr.execute(playlists_table_qry)
            
            #make new playlist table
            playlist_qry = "CREATE TABLE {} (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, song char(255))".format(name_of_playlist)
            
            crsr.execute(playlist_qry)
        else:
            tts("You can only have 4 active playlists")

    
    def finish(self):
        root2.destroy()
        con.close()
        root3 = Tk()
        root3.title("Installation")
        root3.iconphoto(False, PhotoImage(file = "reqs/logo.png"))
        img = PhotoImage(file = "reqs/Finished.png")
        panel = Label(root3, image = img)
        panel.pack(side = "top", fill = "both", expand = "yes")
        root3.after(3000, lambda: root3.destroy())
        root3.mainloop()

        with open("reqs/i.txt", "w") as file:
            file.write("installed^")

root = Tk()
root.configure(bg="#252525")
installation_win = installation_win(root)
root.mainloop() 