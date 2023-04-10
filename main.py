# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 08:38:10 2020

@author: Gfrkad
"""
from tkinter import *

import urllib.request

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

# import mysql.connector as sql

import pyttsx3

import random

from functools import partial

import speech_recognition as sr

# import winsound

import smtplib, ssl




#chrome options
chrome_options = Options()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--incognito')

browser = webdriver.Chrome(options=chrome_options, executable_path=r"reqs/chromedriver")

run = False

global paused
paused = False


def check_con():
    try:
        urllib.request.urlopen('http://google.com')
        tts("connected")
        return True
    except:
        return False


#text to speech
def tts(to_say):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(to_say) 
        engine.runAndWait()
        engine.stop()
    except:
            pass


#if no internet, run this
def no_internet():
    no_internet = Tk()
    tts("no internet")
    no_internet.title("Music.www")
    photo = PhotoImage(file = "reqs/logo.png")
    no_internet.iconphoto(False, photo)
    img = PhotoImage(file = "reqs/no_internet.png")
    panel = Label(no_internet, image = img)
    panel.pack(side = "top", fill = "both", expand = "yes")
    no_internet.mainloop()


#Checking if installed(tables made or not)
with open("reqs/i.txt", "r") as file:
    if "^" not in file.read():
        from install import *
        import install
    else:
        #check if internet connection available
        if check_con():
            run = True
        else:
            no_internet()


#connect to database
with open("user.txt", "r") as file:
    user = file.read()
with open("passw.txt", "r") as file:
    passw = file.read()

host = "localhost"

db = "mwww"

# con = sql.connect(host = host, user = user, passwd = passw, database = db)

# crsr = con.cursor()


def send_mail(msg, receiver_email):
    try:
        port = 465  # For SSL
        
        with open("email.txt", "r") as file:
            sender_email = str(file.read())
        
        with open("email_pass.txt","r") as file:
            password = str(file.read())
        
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg)
    except:
        tts("Failed send the email")


#speech to text
def stt():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        frequency = 400
        duration = 800
        # winsound.Beep(frequency, duration)
        audio = r.listen(source)
        try:
            spoken = r.recognize_google(audio)
            return spoken
        except Exception as e:
            tts("Error :- " + str(e))



#function to find and play song from youtube
def playsong(song_name):
    if  song_name != '':
        main_win.change_state()
        main_win.search.delete(0, END)
        main_win.search.insert(0, song_name)
        tts("Searching for {}".format(song_name))
        
        url = "https://www.youtube.com./"
        browser.get(url)
        browser.implicitly_wait(5)
        
        #search for song
        search_bar = browser.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input')
        search_bar.send_keys(song_name + " song")
        
        #click search
        search_but = browser.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/button')
        search_but.click()
        browser.implicitly_wait(5)
        
        #click video
        song = browser.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a")
        song.click()
        global paused
        paused = False
        
        tts("Here is what I found for {} on youtube.".format(song_name))
    
    elif song_name == '':
        tts('Please enter the name of a song')
    

#function to play or pause
def play_or_pause(event = None):
    try:
        video = browser.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[1]/video")
        video.click()
        global paused
        if not paused:
            paused = True 
        else:  
            paused = False
    except:
        pass


#get song name
def yt_song_name():
    try:
        song_text = browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[7]/div[2]/ytd-video-primary-info-renderer/div/h1').text
        main_win.search.delete(0, END)
        main_win.search.insert(0, song_text)
    except:
        pass

#function to play next song
def next_song():
    tts("Playing the next song")
    next_song = browser.find_element_by_css_selector("#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button")
    next_song.click()
    yt_song_name()
    


#function to mute
def mute_or_unmute():
    mute_but = browser.find_element_by_css_selector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > span > button')
    mute_but.click()


#save to favourites
def favourites_it(song_name):
    tts("Added to favourites")
    fav_play_qry = "SELECT song FROM favourites"
    crsr.execute(fav_play_qry)
    fav_rslt = crsr.fetchall()
    if song_name not in fav_rslt:
        fav_qry = "INSERT INTO favourites (song) values ('{}')".format(song_name)
        crsr.execute(fav_qry)
        con.commit()

#remove from favourites
def unfavourite_it(song_name):
    tts("Removed from favourites")
    unfav_qry = "DELETE FROM favourites where song = '{}'".format(song_name)
    crsr.execute(unfav_qry)
    con.commit()

#play favourites
def play_rand_fav():
    main_win.change_state()
    fav_play_qry = "SELECT song FROM favourites"
    crsr.execute(fav_play_qry)
    fav_rslt = crsr.fetchall()
    while len(fav_rslt) > 1:
        song_to_play = str(random.choice(fav_rslt)[0])
        if song_to_play != main_win.search.get():
            playsong(song_to_play)
            break

#save to recents
def recents_it(song_name):
    rec_qry = "INSERT INTO recents (song) values ('{}')".format(song_name)
    crsr.execute(rec_qry)
    unrecent_it_auto()
    con.commit()

#delete from recents(on every add)
def unrecent_it_auto():
    unrecent_qry = "SELECT song FROM recents"
    crsr.execute(unrecent_qry)
    unrecent_rslt = crsr.fetchall()
    if len(unrecent_rslt) > 20:
        unrecent_internal_qry = "DELETE FROM recents where song = {}".format(unrecent_rslt[0])
        crsr.execute(unrecent_internal_qry)
        con.commit()


#delete from recents
def unrecents_it():
    unrecent_qry = "DELETE FROM recents"
    crsr.execute(unrecent_qry)
    tts("deleted")
    con.commit()


def recents_win():
    # winsound.MessageBeep()
    r_win = Toplevel()
    
    r_win.resizable(False, False)
    
    r_win.iconphoto(False, PhotoImage(file = "reqs/logo.png"))
    
    lb = Listbox(r_win, relief = GROOVE, bg = 'beige', width = 50, bd = 0, fg = 'grey')
    
    recent_qry1 = "SELECT song FROM recents"
    crsr.execute(recent_qry1)
    recents__ = crsr.fetchall()
    
    x = 0
    for i in recents__:
        lb.insert(x, str(i[0]))
        x += 1
    
    lb.pack()
    r_win.mainloop()


#make playlist
def add_to_playlist_main(playlist_number):
    song_name_pl = main_win.search_entry.get()
    if song_name_pl != "Search..." and song_name_pl != "":
        pl_insert_qry = 'INSERT INTO pl{} (song) values("{}")'.format(playlist_number, song_name_pl)
        tts("Ok")
        crsr.execute(pl_insert_qry)
        con.commit()
        

#play playlist
def play_button(playlist_number):
    # winsound.MessageBeep()
    pl_play_qry = "SELECT song FROM pl{}".format(str(playlist_number))
    crsr.execute(pl_play_qry)
    pl_rslt = crsr.fetchall()
    while len(pl_rslt) > 1:
        song_to_play = str(random.choice(pl_rslt)[0])
        if song_to_play != main_win.search.get():
            playsong(song_to_play)
            main_win.change_state()
            break
    

def playlists_win(pl_num):
    # winsound.MessageBeep()
    pl_win = Toplevel()
    
    pl_win.resizable(False, False)
    
    pl_win.iconphoto(False, PhotoImage(file = "reqs/logo.png"))
    
    lb = Listbox(pl_win, relief = GROOVE, bg = 'beige', width = 50, bd = 0, fg = 'grey')
    
    pl_win_qry = "SELECT song FROM pl{}".format(pl_num)
    crsr.execute(pl_win_qry)
    recents__pl = crsr.fetchall()
    
    x = 0
    
    msg = ""
    
    for i in recents__pl:
        song_pl1 = str(i[0])
        lb.insert(x, song_pl1)
        x += 1
        msg += song_pl1
        msg += "\n"
    
    lb.grid(row = 0, column = 0, columnspan = 2)
    
    label_to_pl = Label(pl_win, text = "Email to :- ")
    label_to_pl.grid(row = 1, column = 0)
    
    def sending_of_email(msg):
        reciever_email = reciever_email_var.get()
        send_mail(msg, reciever_email)
    
    reciever_email_var = StringVar()
    reciever_email_entry = Entry(pl_win,textvariable = reciever_email_var, width = 30)
    reciever_email_entry.grid(row = 1, column = 1)
    
    send_playlist = Button(pl_win, text = "Send", command = partial(sending_of_email, msg), relief = GROOVE, cursor = 'hand2')
    
    send_playlist.grid(row = 2, column = 0, columnspan = 2)
    
    label_info_pl = Label(pl_win, text = """You might have to change some settings
(Check your gmail account)""")
    label_info_pl.grid(row = 3, column = 0, columnspan = 2)
    
    pl_win.mainloop()


def unplaylist_it(pl_num):
    song_name = main_win.search_entry.get()
    tts("Deleting {} from playlist {}".format(song_name, pl_num))
    pl_del_qry = "SELECT song FROM pl{}".format(pl_num)
    crsr.execute(pl_del_qry)
    pl_rslt = crsr.fetchall()
    for i in pl_rslt:
        if i[0] == song_name:
            pl_del_qry = "DELETE FROM pl{} where song = '{}'".format(pl_num, song_name)
            crsr.execute(pl_del_qry)
            con.commit()


#random english yt playlist
def rand_eng_playlist():
    song_name = "English playlist"
    playsong(song_name)


#random hindi yt playlist
def rand_hin_playlist():
    song_name = "Hindi playlist"
    playsong(song_name)


#skip ads
def try_skip():
    try:
        #browser.find_element_by_css_selector('#skip-button\:u > span > button').click()
        browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[15]/div/div[3]/div/div[2]/span/button').click()
    except:
        pass


#copy link to clipboard
def get_link():
    try:
        main_win.link_address_var.set(str(browser.current_url))
        main_win.link_address.config(textvariable = main_win.link_address_var)
        main_win.master.clipboard_clear()
        main_win.master.clipboard_append(str(browser.current_url))
        tts("Link copied to clipboard")
    except:
        pass


#the main window for the app
class main_win:
    def __init__(self, master):
        #title
        self.master = master
        master.title("Music.www")
        #Resizing
        master.resizable(False, False)
        #icon
        self.photo = PhotoImage(file = "reqs/logo.png")
        master.iconphoto(False, self.photo)
        #geometry
        master.geometry("800x400")
        
        master.bind('<Return>', self.get_entry_and_play)
        
        
        
        #widgets
        #Search
        self.search_entry = StringVar(master, value = "Search...")
        self.search = Entry(master,textvariable = self.search_entry, width = 50, state = DISABLED, bg="#252525", fg = "#c2c2c2", disabledbackground = "black")
        self.search.place(x = 10, y = 10)
        self.on_click_id = self.search.bind('<Button-1>', self.focus_on)
        
        #search button
        self.search_button = Button(text = "ɢᴏ",relief = GROOVE, command = self.get_entry_and_play, cursor = 'hand2', state = DISABLED, bg = 'pale green')
        self.search_button.place(x = 317, y = 5)
        # def on_enter_search(self, e = None):
        #     self.search_button['background'] = '#9eb0b0'
        
        # def on_leave_search(self, e = None):
        #     self.search_button['background'] = '#252525'
        
        # self.search_button.bind("<Enter>", on_enter_search)
        # self.search_button.bind("<Leave>", on_leave_search)
        
        
        #pause button
        self.pause_button = Button(master, text = "►/║", relief = GROOVE, command = play_or_pause, state = DISABLED,width = 15, cursor = 'hand2', bg = 'pale green')
        self.pause_button.place(x = 10, y = 50)
        
        master.bind("<space>", play_or_pause)
        
        # def on_enter_pause(self, e = None):
        #     self.pause_button['background'] = '#9eb0b0'
        
        # def on_leave_pause(self, e = None):
        #     self.pause_button['background'] = '#252525'
        
        # self.pause_button.bind("<Enter>", on_enter_pause)
        # self.pause_button.bind("<Leave>", on_leave_pause)
        
        
        #next button
        self.next_button = Button(master, text = " ⊵ ", relief = GROOVE, command = next_song, state = DISABLED, width = 5, cursor = 'hand2', bg = 'sky blue')
        self.next_button.place(x = 130, y = 50)
        
        
        #mute button
        self.mute_button = Button(master, text = " ∅ ", relief = GROOVE, command = mute_or_unmute, state = DISABLED, cursor = 'hand2', bg = 'sky blue')
        self.mute_button.place(x = 180, y = 50)
        
        
        #Random eng 
        self.rand_eng = Button(master, text = " Random English ", relief = GROOVE, command = self.rand_playlist_eng, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.rand_eng.place(x = 10, y = 80)
        
        
        #Random hin 
        self.rand_hin = Button(master, text = " Random Hindi ", relief = GROOVE, command = self.rand_playlist_hin, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.rand_hin.place(x = 118, y = 80)
        
        #play_random_fav
        self.play_rand_fav = Button(master, text = " Play favourite", relief = GROOVE, command = play_rand_fav, width = 16, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.play_rand_fav.place(x = 217, y = 80)
        
        #skip ads
        self.skip_ad = Button(master, text = " Try Skipping Ads ", relief = GROOVE, command = try_skip, state = DISABLED, width = 16, cursor = 'hand2', bg = 'sandy brown')
        self.skip_ad.place(x = 215, y = 50)
        
        #get link
        self.get_link = Button(master, text = " Get link ", relief = GROOVE, command = get_link, width = 8, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.get_link.place(x = 272, y = 110)
        
        
        #add to favourites
        self.add_to_fav = Button(master, text = " Add to favourites ", relief = GROOVE, command = self.add_fav, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.add_to_fav.place(x = 10, y = 110)
        
        #remove from favourites
        self.remove_from_fav = Button(master, text = " Remove from favourites ", relief = GROOVE, command = self.remove_fav, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.remove_from_fav.place(x = 123, y = 110)
        
        #link address entry
        self.link_label = Label(master, text = "Link...", bg="#252525", fg = "#c2c2c2")
        self.link_label.place(x = 10, y = 170 )
        
        self.link_address_var = StringVar(master, value = "None")
        self.link_address = Entry(master, textvariable = self.link_address_var, relief = GROOVE, width = 54, state = 'readonly', justify = CENTER, bg="#252525", fg = "#c2c2c2", readonlybackground = "black")
        self.link_address.place(x = 10, y = 200)
        
        # recents listbox
        self.recents_listbox_button = Button(master, text = "recents", command = recents_win, width = 20, relief = GROOVE, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.recents_listbox_button.place(x = 10, y = 260)
        
        #unreccent
        self.unrecents_button = Button(master, text = "Delete from Recents", command = unrecents_it, relief = GROOVE, width = 23, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.unrecents_button.place(x = 165, y = 260)
        
        
        #Now playing
        self.srch_for_lbl = Label(master, text = "Now Playing...", bg="#252525", fg = "#c2c2c2")
        self.srch_for_lbl.place(x = 10, y = 350)
        
        self.search_for = Label(master, textvariable = self.search_entry, relief = GROOVE, width = 47, bg="#252525", fg = "#c2c2c2")
        self.search_for.place(x = 10, y = 370)
        
        
        #Playlist info label
        self.playlist_name_playlist = Label(master, text = "Playlists", bg="#252525", fg = "#c2c2c2")
        self.playlist_name_playlist.place(x = 550, y = 10)
        
        
        #x and y values
        x = 350
        y = 50 
        
        
        #Playlist no.s
        self.pl_num_label_1 = Label(master, text = "1.", bg="#252525", fg = "#c2c2c2")
        self.pl_num_label_2 = Label(master, text = "2.", bg="#252525", fg = "#c2c2c2")
        self.pl_num_label_3 = Label(master, text = "3.", bg="#252525", fg = "#c2c2c2")
        self.pl_num_label_4 = Label(master, text = "4.", bg="#252525", fg = "#c2c2c2")
        #place
        self.pl_num_label_1.place(x = x, y = y)
        self.pl_num_label_2.place(x = x, y = y + 30)
        self.pl_num_label_3.place(x = x, y = y + 60)
        self.pl_num_label_4.place(x = x, y = y + 90)
        
        
        #playlist play buttons
        self.playlist_1_play = Button(master, text = "Play", command = partial( play_button, "1"), relief = GROOVE, width = 15, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_2_play = Button(master, text = "Play", command = partial( play_button, "2"), relief = GROOVE, width = 15, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_3_play = Button(master, text = "Play", command = partial( play_button, "3"), relief = GROOVE, width = 15, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_4_play = Button(master, text = "Play", command = partial( play_button, "4"), relief = GROOVE, width = 15, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        #place
        x = 380
        self.playlist_1_play.place(x = x, y = y)
        self.playlist_2_play.place(x = x, y = y + 30)
        self.playlist_3_play.place(x = x, y = y + 60)
        self.playlist_4_play.place(x = x, y = y + 90)
        
        
        #playlist show buttons
        self.playlist_1_show = Button(master, text = "Show", command = partial( playlists_win, "1"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_2_show = Button(master, text = "Show", command = partial( playlists_win, "2"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_3_show = Button(master, text = "Show", command = partial( playlists_win, "3"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_4_show = Button(master, text = "Show", command = partial( playlists_win, "4"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        #place
        x = 500
        self.playlist_1_show.place(x = x, y = y)
        self.playlist_2_show.place(x = x, y = y + 30)
        self.playlist_3_show.place(x = x, y = y + 60)
        self.playlist_4_show.place(x = x, y = y + 90)
        
                
        #playlist add buttons
        self.playlist_1_add = Button(master, text = "Add", command = partial(add_to_playlist_main, "1"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_2_add = Button(master, text = "Add", command = partial(add_to_playlist_main, "2"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_3_add = Button(master, text = "Add", command = partial(add_to_playlist_main, "3"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_4_add = Button(master, text = "Add", command = partial(add_to_playlist_main, "4"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        #place
        x = 599
        self.playlist_1_add.place(x = x, y = y)
        self.playlist_2_add.place(x = x, y = y + 30)
        self.playlist_3_add.place(x = x, y = y + 60)
        self.playlist_4_add.place(x = x, y = y + 90)
        
        
        #playlist del buttons
        self.playlist_1_del = Button(master, text = "Delete", command = partial( unplaylist_it, "1"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_2_del = Button(master, text = "Delete", command = partial( unplaylist_it, "2"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_3_del = Button(master, text = "Delete", command = partial( unplaylist_it, "3"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.playlist_4_del = Button(master, text = "Delete", command = partial( unplaylist_it, "4"), relief = GROOVE, width = 12, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        #place
        x = 698
        self.playlist_1_del.place(x = x, y = y)
        self.playlist_2_del.place(x = x, y = y + 30)
        self.playlist_3_del.place(x = x, y = y + 60)
        self.playlist_4_del.place(x = x, y = y + 90)
        
        
        #speech search
        self.speak_instruction = Label(master, text = "Speak after the beep and start with 'play'(slow search)", bg="#252525", fg = "#c2c2c2")
        self.speak_instruction.place(x = 490, y = 280)
        self.speak = Button(master, text = "⦿ Speech Search", command = self.check_spoken, relief = GROOVE, cursor = 'hand2', bg = 'sky blue')
        self.speak.place(x = 380, y = 280)
        
        
        #playlist name entry future v
        self.pne_label = Label(master, text = "Enter name of playlist...", bg="#252525", fg = "#c2c2c2")
        self.playlist_name_entry = Entry(master)
        
        
        #beeper
        self.beep_var = IntVar()
        self.slider = Scale(master, variable = self.beep_var, from_ = 40, to = 20000, orient = HORIZONTAL, length = 350, bg="#252525", fg = "#c2c2c2")#, command = self.win_beep)
        self.slider.place(x = 375, y = 330)
        self.slider.set(2500)
        
        self.beep_button = Button(master, text = "Beep", command = self.win_beep, relief = GROOVE, cursor = 'hand2', bg="#252525", fg = "#c2c2c2")
        self.beep_button.place(x = 745, y = 340)
        self.master.bind("b", self.win_beep)
        
    
        #funcs
    def win_beep(self, event = None):
        winsound.Beep(int(self.beep_var.get()), 300)
    
    def check_spoken(self):
        self.spoken = str(stt())
        if "play" in self.spoken:
            self.spoken = self.spoken[5 :]
            playsong(self.spoken)
    
    def focus_on(self, event):
        self.search_button.configure(state = NORMAL)
        self.search.configure(state = NORMAL)
        self.search.delete(0, END)
        self.master.unbind("<space>")
    
    def get_entry_and_play(self, event = None):
        self.change_state()
        self.search_song_name = str(self.search.get())
        playsong(self.search_song_name)
        recents_it(self.search_song_name)
        self.master.bind("<space>", play_or_pause)
        self.link_label.focus()
    
    def change_state(self):
        self.search.configure(state = NORMAL)
        self.pause_button.configure(state = NORMAL)
        self.next_button.configure(state = NORMAL)
        self.mute_button.configure(state = NORMAL)
        self.skip_ad.configure(state = NORMAL)
    
    def rand_playlist_eng(self):
        self.change_state()
        rand_eng_playlist()
        
    def rand_playlist_hin(self):
        self.change_state()
        rand_hin_playlist()
    
    def add_fav(self):
        self.temp_fav_var = str(self.search.get())
        if self.temp_fav_var != "":
            favourites_it(self.temp_fav_var)
    
    def remove_fav(self):
        unfavourite_it(str(self.search.get()))
        

if run:
    root = Tk()
    root.configure(bg="#252525")
    main_win = main_win(root)
    #root.after(0, yt_song_name)  not working
    root.mainloop()
    con.commit()
    con.close()
    browser.close()