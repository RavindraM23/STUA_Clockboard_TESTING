from turtle import color
import pygame
import stua, time
from stua import gtfsSubway
from stua import gtfsBus
#import random
from pygame import freetype
import dotenv, os

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT"))#os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))


pygame.init()
screen = pygame.display.set_mode()
#screen = pygame.display.set_mode((1280, 720))
#pygame.draw.rect(screen, "#888888", (0,70*gwidth,60,70)) #top left coords, width, height
height = screen.get_height()
width = screen.get_width()
#screen = pygame.display.set_mode((width, (5/6)*height))
sectionfactor = 1/6
halfwidth = 0.5*width
bulletfont = freetype.Font("Acta_Symbols_W95_Circles.ttf", int(1.15*sectionfactor*height)) #for a .otf/.ttf font
smallbulletfont = freetype.Font("Acta_Symbols_W95_Circles.ttf", int(0.5*sectionfactor*height))
standardbig = freetype.Font("standard-medium.otf", int(sectionfactor*height*1.15))
standardsmall = freetype.Font("standard-medium.otf", int(sectionfactor*height*0.5)) #for a .otf/.ttf font
standardc = freetype.Font("standard-medium-condensed.otf", int(sectionfactor*height*0.3))
standardcond = freetype.Font("standard-medium-condensed.otf", int(sectionfactor*height*0.5))
#stuashort=stua.gtfsSubway()
#stua.keyMTA("xxxxxx")
routelist = ("1","2","3","4","5","6","7","6X")
bulletlist = ("➊","➋","➌","➍","➎","➏","➐","⑥")

orange = True
barclay = True
counter = 0
loading = True
#LOADING SCREEN
screen.fill("#ffffff")
image = pygame.image.load('logo.png')
image2 = pygame.image.load('SU.png')
#image ratio 1.5625:1, where smaller numbers are bigger sizes
#image = pygame.transform.scale(image, (width/3.125, height/2))
image = pygame.transform.scale(image, (width/(3.5*1.5625), height/3.5))
image2 = pygame.transform.scale(image2, (width/7, height/4))
screen.blit(image, (width*0, height*0.25 - height * 0.25))
screen.blit(image2, (width*0.84, height*0.25 - height * 0.24))
#screen.blit(image, (width*0, height*0.5 - height * 0.25))
#standardbigLOADING = freetype.Font("standard-medium.otf", int(height/17))
#helveticasmallLOADING = freetype.Font("helvetica-light.ttf", int(height/17))
standardbigLOADING = freetype.Font("standard-medium.otf", int(height/25))
helveticasmallLOADING = freetype.Font("helvetica-light.ttf", int(height/25))
#standardbigLOADING.render_to(screen, (width/3.25, height/2.20), "Stuyvesant Transit and Urbanism Association")
#helveticasmallLOADING.render_to(screen, (width/3.25, height/1.90), "Countdown Board Project v1.1.0")
standardbigLOADING.render_to(screen, (width/5.75, height/8.20), "Stuyvesant Transit and Urbanism Association")
helveticasmallLOADING.render_to(screen, (width/5.75, height/6.00), "Countdown Board Project v1.1.0")
#bar = pygame.draw.rect(screen, "#000000", pygame.Rect(width/3.25, width/3.25, height/0.86, height/22), 2)
#standardbigLOADING.render_to(screen, (width/3.25, height/1.96), "Loading Display...")

#RECTANGLES: first two args pos, next two args size
helveticaDAYROTATION = freetype.Font("standard-medium.otf", int(height/3.5))
helveticaSCHEDULEROTATION = freetype.Font("standard-medium.otf", int(height/9.5))

DAYROTATION = pygame.draw.rect(screen, "#000000", pygame.Rect(width/10.7, width/5.00, height/2.75, height/2.75), border_radius=20)
helveticaDAYROTATION.render_to(screen, (width/8, height/2.3), "B1", "#ffffff")
#pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
SCHEDULEROTATION = pygame.draw.rect(screen, "#f00000", pygame.Rect(width/1.85, width/5.00, height/1.90, height/6.75), border_radius=20)
helveticaSCHEDULEROTATION.render_to(screen, (width/1.69, height/2.58), "Regular", "#ffffff")

helveticaPERIODROTATION = freetype.Font("helvetica-light.ttf", int(height/20))
helveticaPERIODROTATION.render_to(screen, (width/1.84, height/1.79), "This Period Is: Period 1")
helveticaPERIODROTATION.render_to(screen, (width/1.84, height/1.59), "The Next Period Is: Period 2")
helveticaPERIODROTATION.render_to(screen, (width/1.83, height/1.44), "Minutes Remaining: 3")
helveticaPERIODROTATION.render_to(screen, (width/1.84, height/1.31), "Testing Rotation: Science")
helveticaPERIODROTATION.render_to(screen, (width/37.2, height/1.15), "Insert Annoucement")

pygame.display.update()

#startw = width/3.25
#starth = height/2.20
while True:
    #startw += 0.05
    #screen.fill("#ffffff")
    #helveticasmallLOADING.render_to(screen, (startw, height/2.20), "Countdown Board Project v1.1.0")
    #pygame.display.update()
    pass