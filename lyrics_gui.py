import tkinter as tk
import customtkinter as ctk

#from gtts import gTTS 


import time
import os
import re
import random
from pathlib import Path


def next_song(var = None):
    print(song_title_var.get())
    print("next")
    count_var.set(count_var.get()+1)
    song_num_var.set((song_num_var.get() + 1) % 50)
    prev_song_var.set(song_title_var.get())
    lyrics_var.set(songs[song_num_var.get()][1])
    song_title_var.set(songs[song_num_var.get()][0].lower())

def skip_song(var):
    print(song_title_var.get())
    print("skip")
    song_num_var.set((song_num_var.get() + 1) % 50)
    prev_song_var.set(song_title_var.get())
    lyrics_var.set(songs[song_num_var.get()][1])
    song_title_var.set(songs[song_num_var.get()][0].lower())

def check_song(var, index, mode):
    song_guess = song_var.get()
    song_title = song_title_var.get()

    song_guess = song_guess.lower()

    print(re.sub('[\W_]+', '',song_guess))
    print(re.sub('[\W_]+','', song_title))
    if re.sub('[\W_]+','', song_guess) == re.sub('[\W_]+','', song_title):
        next_song()
        song_entry.delete(0, tk.END)
        return True
    else: 
        return False

def switch_mode():
    print("HERE")
    if typing_mode_var.get():
        print("TYPING TRUE")
        app.bind("<Right>",next_song)
        app.bind("<Left>",skip_song)
        song_entry.grid_remove()
        button_var.set("Typing mode")
    
    if not typing_mode_var.get():
        print("TYPING FALSE")
        app.unbind("<Right>")
        app.unbind("<Left>")
        song_entry.grid()
        button_var.set("Training mode")
    
    typing_mode_var.set(not typing_mode_var.get())
        
def update_timer():
    if min_var.get() == 0 and sec_var.get() == 0:
        with open("games.txt", "a+") as games_file:
            print("Added to file")
            games_file.write(f"{count_var.get()}")
        timer_var.set("Done")
        return
    elif sec_var.get() == 0:
        min_var.set(min_var.get()-1)
        sec_var.set(59)
    else:
        sec_var.set(sec_var.get()-1)

    timer_var.set(f"{min_var.get():02d}:{sec_var.get():02d}")
    after_id.set(timer_lbl.after(1000,update_timer))

def reset_game():
    timer_lbl.after_cancel(after_id.get())
    min_var.set("1")
    sec_var.set("0")
    timer_var.set("1:00")
    count_var.set(0)
    song_num_var.set(0)
    random.shuffle(songs)
    lyrics_var.set(songs[song_num_var.get()][1])
    song_title_var.set(songs[song_num_var.get()][0].lower())
    after_id.set(timer_lbl.after(1000,update_timer))


songs = []
for dirname, _, filenames in os.walk('../taylor_swift_lyrics/Top50'):
        for filename in filenames:
            print(filename)
            song = (Path(filename).stem)

            raw_lyrics = ''
            with open(os.path.join(dirname, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    if 'Contributors' in line or line[0] == '(' or line[0] == '[' or line == '\n':
                        continue
                    raw_lyrics = line
                    break

            # Clean up the lyrics by replacing non-standard characters
            raw_lyrics = raw_lyrics.encode('ascii', 'replace').decode().replace('?', ' ')
            raw_lyrics = re.sub('(?!\n)\s+', ' ', raw_lyrics)

            # Remove lyrics header
            raw_lyrics = re.sub('.*Lyrics', '', raw_lyrics)

            # Remove end characters (number + 'Embed' or number + 'KEmbed')
            raw_lyrics = re.sub('[0-9]+KEmbed', '', raw_lyrics)
            raw_lyrics = re.sub('[0-9]+Embed', '', raw_lyrics)

            section_pattern = re.compile(r'(?<!\n\n)\[([^\]]+)\]')
            raw_lyrics = section_pattern.sub(r'\n[\1]', section_pattern.sub(r'\n[\1]', raw_lyrics))

            # Remove firsts empty lines 
            empty_lines = re.compile(r'^\s*')
            raw_lyrics = empty_lines.sub('', raw_lyrics)
            raw_lyrics = raw_lyrics.split()
            lyrics = ""
            count = 0
            for i in raw_lyrics:
                lyrics += i + " "
                count += 1
                if count >= 4:
                    break

            songs.append([song,lyrics])



print(*songs,sep='\n')
random.shuffle(songs)


## GUI
ctk.set_default_color_theme("lover.json")

app = ctk.CTk()
app.geometry("720x480")
app.title("Taylor Swift Trainer")
app.columnconfigure(0, weight=1)

song_num_var = tk.IntVar(value=0)
count_var = tk.IntVar(value=0)
lyrics_var = tk.StringVar(value=songs[count_var.get()][1])
song_var = tk.StringVar()
song_title_var = tk.StringVar(value=songs[count_var.get()][0].lower())
prev_song_var = tk.StringVar()
button_var = tk.StringVar(value="Training Mode")
typing_mode_var = tk.BooleanVar(value=True)
after_id = tk.StringVar()


min_var=tk.IntVar(value="1")
sec_var=tk.IntVar(value="0")
timer_var=tk.StringVar(value="1:00")

timer_lbl = ctk.CTkLabel(app, textvariable=timer_var)
lyric_lbl = ctk.CTkLabel(app, textvariable=lyrics_var, font=ctk.CTkFont(family='AppleGothic', size=25, weight='bold'))
prev_song_lbl = ctk.CTkLabel(app,textvariable=prev_song_var, font=ctk.CTkFont(family='AppleGothic', size=15))
count_lbl = ctk.CTkLabel(app, textvariable=count_var)
typing_btn = ctk.CTkButton(app, text="Switch Mode", command=switch_mode)
timer_btn = ctk.CTkButton(app, text="Reset Game", command=reset_game)
song_entry = ctk.CTkEntry(app, width=350, height = 40, textvariable=song_var)
app.bind("<Left>",skip_song)

lyric_lbl.grid(row=0, pady=10)
song_entry.grid(row=1)
prev_song_lbl.grid(row=2)
count_lbl.grid(row=3)
timer_lbl.grid(row=4)
typing_btn.grid(row=5)
timer_btn.grid(row=6, pady=10)

after_id.set(timer_lbl.after(1000,update_timer))

song_var.trace_add("write", check_song)

app.mainloop()

print("Exited")