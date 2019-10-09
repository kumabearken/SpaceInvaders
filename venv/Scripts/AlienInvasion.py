import pygame
import os
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from buttons import Buttons
from ship import Ship
from alien import Alien
import game_functions as gf
from bunker import Bunker
from ufo import UFO
from tkinter import *
from PIL import ImageTk
from PIL import Image
from pygame import mixer

#from window import Window
class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master=None)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Space_Invaders")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        lbl = Label(self, text='Space\nInavders',font=("Arial Bold",80))
        lbl.grid(column=50, row =0)

        # creating a button instance
        playButton = Button(self, text="Play", command=run_game)

        # placing the button on my window
        playButton.place(x=350, y=800)

        # creating a button instance
        hsButton = Button(self, text="HighScore", command=highScore)

        # placing the button on my window
        hsButton.place(x=100, y=800)

        width = 100
        height = 100
        self.img1 = Image.open("images/Alien10.png")
        self.img1 = self.img1.resize((width, height), Image.ANTIALIAS)
        self.photoImg1 = ImageTk.PhotoImage(self.img1)
        self.imglabel1 = Label(self, image=self.photoImg1).grid(row=400, column=50)
        lbl1 = Label(self, text='x45',font=("Arial Bold",16))
        lbl1.grid(row=401, column=50)

        self.img2 = Image.open("images/Alien20.png")
        self.img2 = self.img2.resize((width, height), Image.ANTIALIAS)
        self.photoImg2 = ImageTk.PhotoImage(self.img2)
        self.imglabel2 = Label(self, image=self.photoImg2).grid(row=500, column=50)
        lbl2 = Label(self, text='x30',font=("Arial Bold",16))
        lbl2.grid(row=501, column=50)

        self.img3 = Image.open("images/Alien30.png")
        self.img3 = self.img3.resize((width, height), Image.ANTIALIAS)
        self.photoImg3 = ImageTk.PhotoImage(self.img3)
        self.imglabel3 = Label(self, image=self.photoImg3).grid(row=600, column=50)
        lbl3 = Label(self, text='x15',font=("Arial Bold",16))
        lbl3.grid(row=601, column=50)

def run_game():
    # Initialize game and create a screen object.
    window.destroy()
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # Make the Play button.
    play_button = Buttons(ai_settings, screen, "Play:)")

    # Create an instance to store game statistics and create scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship a group of bullets and group of aeins
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = []
    gf.create_fleet(ai_settings, screen,ship, aliens, stats)
    bunkers = Group()
    ufos = Group()

    # Create the fleet of ;aiens
    gf.create_bunkers(ai_settings, screen,bunkers)
    #gf.create_fleet(ai_settings, screen, ship, aliens)
    gf.create_ufo(ai_settings,screen, ufos)
    mixer.init()
    mixer.music.load("sounds\\Hipster Alien.mp3")
    mixer.music.play(-1)
    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers,ufos)
        if stats.game_active:
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,bunkers,ufos)
            ship.update()
            for ufo in ufos:
                ufo.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,bunkers,ufos)
            gf.update_aliens(ai_settings,screen, stats, sb , ship, aliens, bullets, clock)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bunkers,ufos)

def highScore():
    top = Toplevel()
    top.geometry("200x200")
    top.title("High_Score")
    with open("highscore.txt", "r") as file:
        Label(top,text=file.read()).pack()
    file.close()

window = Tk()
window.geometry("500x900")
app = Window(window)
window.mainloop()

