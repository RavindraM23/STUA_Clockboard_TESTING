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
screen = pygame.display.set_mode((1280, 720))
#screen = pygame.display.set_mode()
#pygame.draw.rect(screen, "#888888", (0,70*gwidth,60,70)) #top left coords, width, height
height = screen.get_height()
width = screen.get_width()
#screen = pygame.display.set_mode((width, (5/6)*height))
sectionfactor = 1/7
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

#CRITICAL TIMES
seventh_ave_crit = 4
eighth_avenue_crit = 9
broadway_crit = 12
nassau_crit = 12
lexington_avenue_crit = 12

#LOADING SCREEN
screen.fill("#ffffff")
image = pygame.image.load('logo.png')
image = pygame.transform.scale(image, (width/3.125, height/2))
screen.blit(image, (width*0, height*0.5 - height * 0.25))
standardbigLOADING = freetype.Font("standard-medium.otf", int(height/17))
helveticasmallLOADING = freetype.Font("helvetica-light.ttf", int(height/17))
standardbigLOADING.render_to(screen, (width/3.25, height/2.45), "Stuyvesant Transit and Urbanism Association")
helveticasmallLOADING.render_to(screen, (width/3.25, height/2.15), "Countdown Board Project v1.1.0")
bar = pygame.draw.rect(screen, "#000000", pygame.Rect(width/3.25, width/3.10, height/0.86, height/22), 2)
#bar = pygame.draw.rect(screen, "#000000", pygame.Rect(width/3.25, width/3.25, height/0.86, height/22), 2)
#standardbigLOADING.render_to(screen, (width/3.25, height/1.96), "Loading Display...")
pygame.display.update()

def percent_update(percent):
    if percent == 0:
        bar = pygame.draw.rect(screen, "#ffffff", pygame.Rect(width/3.25, width/3.10, 1*(height/0.86), height/22))
    else:
        bar = pygame.draw.rect(screen, "#000000", pygame.Rect(width/3.25, width/3.10, percent*(height/0.86), height/22))
        pygame.display.update(bar)

"""
seventhup = [gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway()]
seventhdown = [gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway()]
#
eighthup = [gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway()]
eighthdown = [gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway(),gtfsSubway()]
#
bwayup = [gtfsSubway(),gtfsSubway()]
bwaydown = [gtfsSubway(),gtfsSubway()]
"""
#
#lexup = [gtfsSubway(),gtfsSubway()]
#jamaicaup = [gtfsSubway(),gtfsSubway()]
terminuslong = ("Van Cortlandt Park-242 St","137 St-City College", "Flatbush Av-Brooklyn College", "Jamaica Center-Parsons/Archer",
                "Ozone Park-Lefferts Blvd","Rockaway Park-Beach 116 St", "Far Rockaway-Mott Av", "Astoria-Ditmars Blvd", "Forest Hills-71 Av", "Bay Ridge-95 St",
                "Coney Island-Stillwell Av", "Whitehall St-South Ferry", "Kew Gardens-Union Turnpike", "Bedford Park Blvd-Lehman College", "Crown Heights-Utica Av")

terminusmed = ("Van Cortlandt Park", "137 St-Broadway", "Brooklyn College", "Jamaica Centre", "Ozone Park", "Beach 116 St", "Far Rockaway", "Astoria", "Forest Hills", "Bay Ridge",
               "Coney Island", "Ignore This", "Kew Gardens", "Bedford Park Blvd", "Crown Heights")
if loading == True:
    percent_update(0.05)
    
while 1:
    try:
        t0 = time.time()
        masterlistSUBWAY = stua.gtfsSubwayBATCHED([("137", "N", 1, seventh_ave_crit, "NONE"), ("137", "N", 2, seventh_ave_crit, "NONE"), ("137", "N", 3, seventh_ave_crit, "NONE"), ("137", "N", 4, seventh_ave_crit, "NONE"), ("137", "N", 5, seventh_ave_crit, "NONE"), #0-4
                                        ("137", "S", 1, seventh_ave_crit, "NONE"), ("137", "S", 2, seventh_ave_crit, "NONE"), ("137", "S", 3, seventh_ave_crit, "NONE"), ("137", "S", 4, seventh_ave_crit, "NONE"), ("137", "S", 5, seventh_ave_crit, "NONE"), #5-9
                                        ("A34", "N", 1, eighth_avenue_crit, "NONE"), ("A34", "N", 2, eighth_avenue_crit, "NONE"), ("A34", "N", 3, eighth_avenue_crit, "NONE"), ("A34", "N", 4, eighth_avenue_crit, "NONE"), ("A34", "N", 5, eighth_avenue_crit, "NONE"), #10-14
                                        ("A36", "S", 1, eighth_avenue_crit, "NONE"), ("A36", "S", 2, eighth_avenue_crit, "NONE"), ("A36", "S", 3, eighth_avenue_crit, "NONE"), ("A36", "S", 4, eighth_avenue_crit, "NONE"), ("A36", "S", 5, eighth_avenue_crit, "NONE"), #15-19
                                        ("R24", "N", 1, broadway_crit, "NONE"), ("R24", "N", 2, broadway_crit, "NONE"), #20-21
                                        ("R28", "S", 1, broadway_crit, "NONE"), ("R28", "S", 2, broadway_crit, "NONE"), #22-23
                                        ("M21", "N", 1, nassau_crit, "NONE"), ("M21", "N", 2, nassau_crit, "NONE"), #24-25
                                        ("640", "N", 1, lexington_avenue_crit, "NONE"), ("640", "N", 2, lexington_avenue_crit, "NONE"), ("640", "N", 3, lexington_avenue_crit, "NONE"), ("640", "N", 4, lexington_avenue_crit, "NONE"), ("640", "N", 5, lexington_avenue_crit, "NONE")]) #26-29
        if loading == True:
            percent_update(0.65)
        
        
        if barclay: 
            masterlistBUS = stua.gtfsBusBATCHED([("404969", 0, 1, 1, "NONE"), ("404969", 0, 2, 1, "NONE"),
                                        ("803147", 0, 1, 2, "NONE"), ("803147", 0, 2, 2, "NONE"),
                                        ("404238", 1, 1, 7, "SIM1"), ("404238", 1, 2, 7, "SIM1"), ("404238", 1, 1, 7, "SIM2"), ("404238", 1, 2, 7, "SIM2"),
                                        ("404225", 1, 1, 7, "X27"), ("404225", 1, 2, 7, "X27"), ("404225", 1, 1, 7, "X28"), ("404225", 1, 2, 7, "X28")])
        else:
            masterlistBUS = stua.gtfsBusBATCHED([("404969", 0, 1, 1, "NONE"), ("404969", 0, 2, 1, "NONE"),
                                        ("803147", 0, 1, 2, "NONE"), ("803147", 0, 2, 2, "NONE"),
                                        ("405065", 0, 1, 1, "M20"), ("405065", 0, 2, 1, "M20"), ("903013", 1, 1, 6, "SIM7"), ("903013", 1, 2, 6, "SIM7"),
                                        ("903013", 1, 1, 6, "SIM33"), ("903013", 1, 2, 6, "SIM33"), ("404219", 1, 1, 7, "SIM34"), ("404219", 1, 2, 7, "SIM34")])
        
        #
        
        if loading == True:
            percent_update(1)
            time.sleep(1.5)
            percent_update(0.00)
        #
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.KEYDOWN:
                pass
        #
        #
        #begin UI Drawing
        #
        #1/2/3/a/c/e
        screen.fill("#000000") 
        pygame.draw.rect(screen, "#eeeeee", (0,0,halfwidth,sectionfactor*height*6))
        pygame.draw.rect(screen, "#dddddd", (halfwidth,0,0.125*width,sectionfactor*height*6))
        pygame.draw.rect(screen, "#cccccc", (0.625*width,0,0.125*width,sectionfactor*height*6))
        pygame.draw.rect(screen, "#bbbbbb", (0.75*width,0,0.125*width,sectionfactor*height*6))
        pygame.draw.rect(screen, "#aaaaaa", (0.875*width,0,0.125*width,sectionfactor*height*6))
        ##4/5/a/c
        pygame.draw.rect(screen, "#eeeeee", (0,5*sectionfactor*height,0.375*width,sectionfactor*height))
        pygame.draw.rect(screen, "#dddddd", (0.375*width,5*sectionfactor*height,0.125*width,sectionfactor*height))
        pygame.draw.rect(screen, "#cccccc", (0.5*width,5*sectionfactor*height,0.375*width,sectionfactor*height))
        pygame.draw.rect(screen, "#aaaaaa", (0.875*width,5*sectionfactor*height,0.125*width,sectionfactor*height))
        pygame.draw.rect(screen, "#eeeeee", (0*width,6*sectionfactor*height,0.125*width,sectionfactor*height))
        pygame.draw.rect(screen, "#dddddd", (0.125*width,6*sectionfactor*height,0.125*width,sectionfactor*height))

        # bus
        pygame.draw.rect(screen, "#111111", (0.25*width,6*sectionfactor*height,0.125*width,sectionfactor*height))
        pygame.draw.rect(screen, "#111111", (0.5*width,6*sectionfactor*height,0.125*width,sectionfactor*height))
        pygame.draw.rect(screen, "#111111", (0.75*width,6*sectionfactor*height,0.125*width,sectionfactor*height))
        
        pygame.draw.line(screen, "#ffffff", (0,sectionfactor*height) , (width,sectionfactor*height), int(height*0.01))
        pygame.draw.line(screen, "#ffffff", (0,2*sectionfactor*height) , (width,2*sectionfactor*height), int(height*0.01))
        pygame.draw.line(screen, "#ffffff", (0,3*sectionfactor*height) , (width,3*sectionfactor*height), int(height*0.01))
        pygame.draw.line(screen, "#ffffff", (0,4*sectionfactor*height) , (width,4*sectionfactor*height), int(height*0.01))
        pygame.draw.line(screen, "#ffffff", (0,5*sectionfactor*height) , (width,5*sectionfactor*height), int(height*0.01))
        pygame.draw.line(screen, "#ffffff", (0,6*sectionfactor*height) , (width,6*sectionfactor*height), int(height*0.01))
        
        print("UI drawing done")
        #
        #end of UI Drawing
        #functions begin
        #
        def colouroftext(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if trainID.route_id == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == seventh_ave_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def colouroftextIND(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if trainID.route_id == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == eighth_avenue_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def colouroftext8thDown(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if trainID.route_id == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == eighth_avenue_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def colouroftextBwayDown(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if str(trainID.route_id) == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == broadway_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def colouroftextJamaica(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if str(trainID.route_id) == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == nassau_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def colouroftextLex(trainID): #checks if train arrival time is the threshold and makes text blink yellow if yes
            if str(trainID.route_id) == "NO TRAINS":
                return "#000000"
            elif str(trainID.time) == lexington_avenue_crit and orange:
                return "#f28305"
            else:
                return "#000000"
        def bulletIRT(trainID): #converts routes to bullet form (IRT lines only)
            if str(trainID.route_id) == "NO TRAINS":
                return "X"
            else: 
                return bulletlist[routelist.index(str(trainID.route_id))]
        def bulletB(trainID): #converts routes to bullet form (IRT lines only)
            if str(trainID.route_id) == "NO TRAINS":
                return "o"
            else: 
                return trainID.route_id
        def terminusmedf(trainID): #shortens destination to medium length if too long
            if trainID.route_id == "NO TRAINS":
                return "Nowhere"
            elif str(trainID.terminus) in terminuslong:
                return terminusmed[terminuslong.index(str(trainID.terminus))]
            else:
                return trainID.terminus
        def checktime(trainID): #makes sure no error occurs when there are NO TRAINs
            if str(trainID.route_id) == "NO TRAINS":
                return "N/A"
            else: 
                return str(trainID.time)
        def checktimeIND(trainID): #makes sure no error occurs when there are NO TRAINs
            if str(trainID.route_id) == "NO TRAINS":
                return "N/A"
            else: 
                return trainID.time
            
        def smalltimeIRT (trainID, offsetx, offsety, colour): #function for outputting the minor times (the ~1x1 squares)
            if str(trainID.route_id) == "NO TRAINS":
                smallbulletfont.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), bulletB(trainID), colour)
            else:
                standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), bulletIRT(trainID), colour)
            standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.55)*sectionfactor*height), checktime(trainID) + "m", colouroftext(trainID))
        def smalltimeLex (trainID, offsetx, offsety, colour): #function for outputting the minor times (the ~1x1 squares)
            if str(trainID.route_id) == "NO TRAINS":
                smallbulletfont.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), bulletB(trainID), colour)
            else:
                standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), bulletIRT(trainID), colour)
            standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.55)*sectionfactor*height), checktime(trainID) + "m", colouroftextLex(trainID))
        def smalltimeIND (trainID, offsetx, colour): #function for outputting the minor times (the ~1x1 squares), offsety removed (re add if >3 lines) ONLY FOR UPTOWN 8 AV
            #standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), trainID.route_id, colour)
            #standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.55)*sectionfactor*height), checktime(trainID) + "m", colouroftextIND(trainID))
            smallbulletfont.render_to(screen, ((offsetx+0.1)*0.125*width,2.1*sectionfactor*height), bulletB(trainID), colour)
            standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,2.55*sectionfactor*height), str(checktimeIND(trainID)-2) + "m", colouroftextIND(trainID))
            ###print("eightsmall")
        def smalltimeBdiv (trainID, offsetx, offsety, colour): #function for outputting the minor times (the ~1x1 squares), offsety removed ONLY FOR DOWNTOWN 8 AV
            #standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), trainID.route_id, colour)
            #standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.55)*sectionfactor*height), checktime(trainID) + "m", colouroftextIND(trainID))
            smallbulletfont.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), bulletB(trainID), colour)
            standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.55)*sectionfactor*height), str(checktimeIND(trainID)) + "m", colouroftext8thDown(trainID))
            if trainID.terminus == "Ozone Park-Lefferts Blvd":
                standardc.render_to(screen, ((offsetx+0.4)*0.125*width,(offsety+0.1)*sectionfactor*height), "OP", "#0039a6")
            elif trainID.terminus == "Far Rockaway-Mott Av":
                standardc.render_to(screen, ((offsetx+0.4)*0.125*width,(offsety+0.1)*sectionfactor*height), "FR", "#0039a6")
            elif trainID.terminus == "Rockaway Park-Beach 116 St":
            #else: 
                standardc.render_to(screen, ((offsetx+0.4)*0.125*width,(offsety+0.1)*sectionfactor*height), "RP", "#0039a6")
            ###print("BdivSmall")



        #
        #functions end
        #7th Av Uptown data begins
        #137 is the code for Chambers St/IRT 7th Av Line
        #
        """
        position = 1 #checks the 1st train and sees if it's below the time threshold
        #(in this case, 3 minutes) and if not, increases it by one (to 2) to check next train
        #
        while True:
            seventhup[0].get("137","N",position)
            if seventhup[0].time < 2.9:
                position += 1
            else:
                break
            if position > 5: #if there are over 5 trains under the threshold this likely means that all the values are 0, meaning there are NO TRAINS, therefore this breaks the loop 
                break
        #fill out remaining 7th Av trains
        seventhup[1].get("137","N",position+1)
        seventhup[2].get("137","N",position+2)
        seventhup[3].get("137","N",position+3)
        seventhup[4].get("137","N",position+4)
        #
        """
        #begin outputting 7th Av uptown data to screen
            #
        #This is train #1
            #
        if str(masterlistSUBWAY[0].route_id) == "NO TRAINS":
            bulletfont.render_to(screen, (0.1*sectionfactor*height,0.1*sectionfactor*height),  bulletB(masterlistSUBWAY[0]) , "#ee352e")
        else:
            standardbig.render_to(screen, (0.1*sectionfactor*height,0.1*sectionfactor*height),  bulletIRT(masterlistSUBWAY[0]) , "#ee352e")
        
        standardsmall.render_to(screen, (sectionfactor*height,0.1*sectionfactor*height), checktime(masterlistSUBWAY[0]) + " minutes", colouroftext(masterlistSUBWAY[0]))
        standardsmall.render_to(screen, (sectionfactor*height,0.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[0]), "#222222")
        #
        #train #2-5
        smalltimeIRT(masterlistSUBWAY[1], 4, 0, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[2], 5, 0, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[3], 6, 0, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[4], 7, 0, "#ee352e")

        ###print("7thUp")
        #end of 7th Av Uptown
        #start of 7th downtown
        #
        """
        position = 1
        while 1:
            seventhdown[0].get("137","S",position)
            if seventhdown[0].time < 2.9:
                position += 1
            else:
                break
            if position > 5: 
                break
        #fill out remaining 7th Av dt trains
        seventhdown[1].get("137","S",position+1)
        seventhdown[2].get("137","S",position+2)
        seventhdown[3].get("137","S",position+3)
        seventhdown[4].get("137","S",position+4)
        """
        #main 7 dt
        if str(masterlistSUBWAY[5].route_id) == "NO TRAINS":
            bulletfont.render_to(screen, (0.1*sectionfactor*height,1.1*sectionfactor*height),  bulletB(masterlistSUBWAY[5]) , "#ee352e")
        else:
            standardbig.render_to(screen, (0.1*sectionfactor*height,1.1*sectionfactor*height),  bulletIRT(masterlistSUBWAY[5]) , "#ee352e")
    
        standardsmall.render_to(screen, (sectionfactor*height,1.1*sectionfactor*height), checktime(masterlistSUBWAY[5]) + " minutes", colouroftext(masterlistSUBWAY[5]))
        standardsmall.render_to(screen, (sectionfactor*height,1.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[5]), "#222222")
        #
        #train #2-5
        smalltimeIRT(masterlistSUBWAY[6], 4, 1, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[7], 5, 1, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[8], 6, 1, "#ee352e")
        smalltimeIRT(masterlistSUBWAY[9], 7, 1, "#ee352e")
        #print("7thdone")
        #
        #end of 7th downtown, start of 8th uptown
        #canal st is A34
        #####################print("7thDown")
        #
        """
        position = 1
        while 1:
            eighthup[0].get("A34","N",position)
            if eighthup[0].time < 6.9:
                position += 1
            else:
                break
            if position > 8: 
                break
        
        #fill out remaining 8th Av upt trains
        eighthup[1].get("A34","N",position+1)
        eighthup[2].get("A34","N",position+2)
        eighthup[3].get("A34","N",position+3)
        eighthup[4].get("A34","N",position+4)
        """
        #main 8 upt
        bulletfont.render_to(screen, (0.1*sectionfactor*height,2.1*sectionfactor*height),  bulletB(masterlistSUBWAY[10]), "#0039a6") #EIGHTH UP 
        standardsmall.render_to(screen, (sectionfactor*height,2.1*sectionfactor*height), str(checktimeIND(masterlistSUBWAY[10])-2) + " minutes", colouroftextIND(masterlistSUBWAY[10]))
        standardsmall.render_to(screen, (sectionfactor*height,2.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[10]), "#222222")
        ###print("first 8th done")
        #
        #trains #2-5
        smalltimeIND(masterlistSUBWAY[11], 4, "#0039a6")
        smalltimeIND(masterlistSUBWAY[12], 5, "#0039a6")
        smalltimeIND(masterlistSUBWAY[13], 6, "#0039a6")
        smalltimeIND(masterlistSUBWAY[14], 7, "#0039a6")
        #
        ###print("8thUp")
        #end of 8 up, start of 8 down
        #EIGHTH DOWN
        #chambers st is A36
        #
        #
        """
        position = 1
        while 1:
            eighthdown[0].get("A36","S",position)
            if eighthdown[0].time < 4.9:
                position += 1
                print("pos+1")
            else:
                break
            if position > 8: 
                break
        
        #fill out remaining 8th Av upt trains
        eighthdown[1].get("A36","S",position+1)
        eighthdown[2].get("A36","S",position+2)
        eighthdown[3].get("A36","S",position+3)
        eighthdown[4].get("A36","S",position+4)
        print("8 down data good") 
        """
        #main 8 upt
        bulletfont.render_to(screen, (0.1*sectionfactor*height,3.1*sectionfactor*height),  bulletB(masterlistSUBWAY[15]), "#0039a6") #EIGHTH UP 
        standardsmall.render_to(screen, (sectionfactor*height,3.1*sectionfactor*height), str(checktimeIND(masterlistSUBWAY[15])) + " minutes", colouroftext8thDown(masterlistSUBWAY[15]))
        standardsmall.render_to(screen, (sectionfactor*height,3.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[15]), "#222222")
        ###print("first 8 down done")
        #
        #trains #2-5
        smalltimeBdiv(masterlistSUBWAY[16], 4,3, "#0039a6")
        smalltimeBdiv(masterlistSUBWAY[17], 5,3, "#0039a6")
        smalltimeBdiv(masterlistSUBWAY[18], 6,3, "#0039a6")
        smalltimeBdiv(masterlistSUBWAY[19], 7,3, "#0039a6")
        #
        #####################################print("8thDown")
        #end of 8 down
        #
        #beginning of b'way up
        #city hall is R24
        """
        position = 1
        while 1:
            bwayup[0].get("R24","N",position)
            if bwayup[0].time < 6.9:
                position += 1
            else:
                break
            if position > 10: 
                break
        #fill out remaining bwy upt trains
        bwayup[1].get("R24","N",position+1)
        #main 8 upt
        """
        bulletfont.render_to(screen, (0.1*sectionfactor*height,5.1*sectionfactor*height),  bulletB(masterlistSUBWAY[20]) , "#d9b411") #BWAY
        standardsmall.render_to(screen, (sectionfactor*height,5.1*sectionfactor*height), str(checktimeIND(masterlistSUBWAY[20])) + " minutes", colouroftextIND(masterlistSUBWAY[20]))
        standardsmall.render_to(screen, (sectionfactor*height,5.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[20]), "#222222")
        ###print("first bway up done")
        #
        #trains #2
        #smalltimeBdiv(bwayup[1], 3,4, "#d9b411")
        smallbulletfont.render_to(screen, (3.1*0.125*width,5.1*sectionfactor*height), bulletB(masterlistSUBWAY[21]), "#d9b411")
        standardsmall.render_to(screen, (3.1*0.125*width,5.55*sectionfactor*height), str(checktimeIND(masterlistSUBWAY[21])) + "m", colouroftextIND(masterlistSUBWAY[21]))

        #bway down
        #Court St is R28 
        """
        position = 1
        while 1:
            bwaydown[0].get("R28","S",position)
            if bwaydown[0].time < 13.9:
                position += 1
            else:
                break
            if position > 13: 
                break
        """
        #fill out remaining bwy dwn trains
        #bwaydown[1].get("R28","S",position+1)
        #main 8 upt
        bulletfont.render_to(screen, (0.5*width+0.1*sectionfactor*height,5.1*sectionfactor*height),  bulletB(masterlistSUBWAY[22]) , "#d9b411") #BWAY
        standardsmall.render_to(screen, ((0.5*width)+(sectionfactor*height),5.1*sectionfactor*height), str(checktimeIND(masterlistSUBWAY[22])-7) + " minutes", colouroftextBwayDown(masterlistSUBWAY[22]))
        standardsmall.render_to(screen, ((0.5*width)+(sectionfactor*height),5.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[22]), "#222222")
        ###print("first bway down done")
        #
        #train #2
        smallbulletfont.render_to(screen, (7.1*0.125*width,5.1*sectionfactor*height), bulletB(masterlistSUBWAY[23]), "#d9b411")
        standardsmall.render_to(screen, (7.1*0.125*width,(5.55*sectionfactor*height)), str(checktimeIND(masterlistSUBWAY[23])-7) + "m", colouroftextIND(masterlistSUBWAY[23]))
        # end broadway downtown
        #
        #BBCH is 640
        #lexington uptown
        if str(masterlistSUBWAY[26].route_id) == "NO TRAINS":
            bulletfont.render_to(screen, (0.1*sectionfactor*height,4.1*sectionfactor*height),  bulletB(masterlistSUBWAY[26]) , "#00933C")
        else:
            standardbig.render_to(screen, (0.1*sectionfactor*height,4.1*sectionfactor*height),  bulletIRT(masterlistSUBWAY[26]) , "#00933C")
        
        standardsmall.render_to(screen, (sectionfactor*height,4.1*sectionfactor*height), checktime(masterlistSUBWAY[26]) + " minutes", colouroftextLex(masterlistSUBWAY[5]))
        standardsmall.render_to(screen, (sectionfactor*height,4.55*sectionfactor*height), terminusmedf(masterlistSUBWAY[26]), "#222222")
        #
        #train #2-5
        smalltimeIRT(masterlistSUBWAY[27], 4, 4, "#00933C")
        smalltimeIRT(masterlistSUBWAY[28], 5, 4, "#00933C")
        smalltimeIRT(masterlistSUBWAY[29], 6, 4, "#00933C")
        smalltimeIRT(masterlistSUBWAY[30], 7, 4, "#00933C")
        #end lexington uptown
        #
        #JAMAICA UP; M21
        #train 1
        smallbulletfont.render_to(screen, (0.1*0.125*width,6.1*sectionfactor*height), bulletB(masterlistSUBWAY[24]), "#996633")
        standardsmall.render_to(screen, (0.1*0.125*width,(6.55*sectionfactor*height)), str(checktimeIND(masterlistSUBWAY[24])) + "m", colouroftextJamaica(masterlistSUBWAY[24]))
        #train 2
        smallbulletfont.render_to(screen, (1.1*0.125*width,6.1*sectionfactor*height), bulletB(masterlistSUBWAY[25]), "#996633")
        standardsmall.render_to(screen, (1.1*0.125*width,(6.55*sectionfactor*height)), str(checktimeIND(masterlistSUBWAY[25])) + "m", colouroftextJamaica(masterlistSUBWAY[25]))
        #end jamaica uptown
        # begin buses
        #bus functions
        def busname(busID): #converts routes to bullet form (IRT lines only)
            if str(busID.route_id) == "NO BUSES":
                return "X"
            else: 
                return busID.route_id
        def checktimebus(busID): #makes sure no error occurs when there are NO TRAINs
            if str(busID.route_id) == "NO BUSES":
                return "X"
            else: 
                return str(busID.time)
        def smalltimebus(busID0, busID1, route, offsetx, offsety):
            standardsmall.render_to(screen, ((offsetx+0.1)*0.125*width,(offsety+0.1)*sectionfactor*height), route, "#ffffff")
            standardcond.render_to(screen, ((offsetx+0.1)*0.125*width, (offsety+0.55)*sectionfactor*height), checktimebus(busID0) + "," + checktimebus(busID1) + "m", "#ffffff")
        #M22
        ##temporary while ravindra optimizes the bustime backend
        if barclay:
            smalltimebus(masterlistBUS[2], masterlistBUS[3], "M9", 2, 6)
            smalltimebus(masterlistBUS[0], masterlistBUS[1], "M22", 3, 6)
            smalltimebus(masterlistBUS[4], masterlistBUS[5], "SIM1", 4, 6)
            smalltimebus(masterlistBUS[6], masterlistBUS[7], "SIM2", 5, 6)
            smalltimebus(masterlistBUS[8], masterlistBUS[9], "X27", 6, 6)
            smalltimebus(masterlistBUS[10], masterlistBUS[11], "X28", 7, 6)
            #smalltimebus(masterlistBUS[], masterlistBUS[], "", , )
            """
            standardsmall.render_to(screen, (2.1*0.125*width,6.1*sectionfactor*height), "M9", "#ffffff")
            standardcond.render_to(screen, (2.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[2]) + "," + checktimebus(masterlistBUS[3]) + "m", "#ffffff")
            #M9
            standardsmall.render_to(screen, (3.1*0.125*width,6.1*sectionfactor*height), "M22", "#ffffff")
            standardcond.render_to(screen, (3.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[0]) + "," + checktimebus(masterlistBUS[1]) + "m", "#ffffff")
            #expb
            standardsmall.render_to(screen, (4.1*0.125*width,6.1*sectionfactor*height), "SIM1", "#ffffff")
            standardcond.render_to(screen, (4.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[4]) + "," + checktimebus(masterlistBUS[5]) + "m", "#ffffff")

            standardsmall.render_to(screen, (5.1*0.125*width,6.1*sectionfactor*height), "SIM2", "#ffffff")
            standardcond.render_to(screen, (5.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[6]) + "," + checktimebus(masterlistBUS[7]) + "m", "#ffffff")

            standardsmall.render_to(screen, (6.1*0.125*width,6.1*sectionfactor*height), "X27", "#ffffff")
            standardcond.render_to(screen, (6.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[8]) + "," + checktimebus(masterlistBUS[9]) + "m", "#ffffff")

            standardsmall.render_to(screen, (7.1*0.125*width,6.1*sectionfactor*height), "X28", "#ffffff")
            standardcond.render_to(screen, (7.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[10]) + "," + checktimebus(masterlistBUS[11]) + "m", "#ffffff")
            #stua.sort(bn)
            #busprintout = busname(bn[0]) + ":" + checktimebus(bn[0]) + "," + busname(bn[1]) + ":" + checktimebus(bn[1]) + "," + busname(bn[2]) + ":" + checktimebus(bn[2]) + "," + busname(bn[3]) + ":" + checktimebus(bn[3]) 
            #standardsmall.render_to(screen, (4.1*0.125*width,6.1*sectionfactor*height), "B'way and Barclays", "#ffffff")
            #standardc.render_to(screen, (4.1*0.125*width,(6.55*sectionfactor*height)), busprintout , "#ffffff")
            """
        else:
            smalltimebus(masterlistBUS[2], masterlistBUS[3], "M9", 2, 6)
            smalltimebus(masterlistBUS[0], masterlistBUS[1], "M22", 3, 6)
            smalltimebus(masterlistBUS[4], masterlistBUS[5], "M20", 4, 6)
            smalltimebus(masterlistBUS[6], masterlistBUS[7], "SIM7", 5, 6)
            """
            standardsmall.render_to(screen, (2.1*0.125*width,6.1*sectionfactor*height), "M9", "#ffffff")
            standardcond.render_to(screen, (2.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[2]) + "," + checktimebus(masterlistBUS[3]) + "m", "#ffffff")
            #M9
            standardsmall.render_to(screen, (3.1*0.125*width,6.1*sectionfactor*height), "M22", "#ffffff")
            standardcond.render_to(screen, (3.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[0]) + "," + checktimebus(masterlistBUS[1]) + "m", "#ffffff")
            #expb
            standardsmall.render_to(screen, (4.1*0.125*width,6.1*sectionfactor*height), "M20", "#ffffff")
            standardcond.render_to(screen, (4.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[4]) + "," + checktimebus(masterlistBUS[5]) + "m", "#ffffff")

            standardsmall.render_to(screen, (5.1*0.125*width,6.1*sectionfactor*height), "SIM7", "#ffffff")
            standardcond.render_to(screen, (5.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[6]) + "," + checktimebus(masterlistBUS[7]) + "m", "#ffffff")
            """
            
            standardcond.render_to(screen, (6.1*0.125*width,6.1*sectionfactor*height), "SIM33", "#ffffff")
            standardcond.render_to(screen, (6.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[8]) + "," + checktimebus(masterlistBUS[9]) + "m", "#ffffff")

            standardcond.render_to(screen, (7.1*0.125*width,6.1*sectionfactor*height), "SIM34", "#ffffff")
            standardcond.render_to(screen, (7.1*0.125*width,(6.55*sectionfactor*height)), checktimebus(masterlistBUS[10]) + "," + checktimebus(masterlistBUS[11]) + "m", "#ffffff")
            #stua.sort(bn)
            #busprintout = busname(bn[0]) + ":" + checktimebus(bn[0]) + "," + busname(bn[1]) + ":" + checktimebus(bn[1]) + "," + busname(bn[2]) + ":" + checktimebus(bn[2]) + "," + busname(bn[3]) + ":" + checktimebus(bn[3]) 
            #standardsmall.render_to(screen, (4.1*0.125*width,6.1*sectionfactor*height), "B'way and Barclays", "#ffffff")
            #standardc.render_to(screen, (4.1*0.125*width,(6.55*sectionfactor*height)), busprintout , "#ffffff")
        #expresses
        #end, update screen
        pygame.display.update()
        loading = False
        #orange = not orange ##uncomment if reload times drop below 3 seconds
        barclay = not barclay 
        print(time.time() - t0)
        counter += 1
        print(counter)
    except:
        pass
pygame.quit()