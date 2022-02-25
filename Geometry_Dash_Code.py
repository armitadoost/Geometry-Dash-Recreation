import pygame, sys
from pygame.locals import *
from random import *
from time import *

#Window
pygame.init()
WIDTH  = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

def redrawGameWindow(): # function that redraws all objects
    pygame.display.set_caption('Times New Roman') #This sets the font I want to use
    gameWindow.blit(character, (objectX,objectY))
    
    font = pygame.font.SysFont(None, 40) #Creates the size of my text
    text = font.render('Score: ' + str(score), True, WHITE) #How the score is shown
    textrect = text.get_rect() #Used to figure out dimensions of the text
    textrect.centerx = gameWindow.get_rect().centerx #Centers the text at the top of my screen
    gameWindow.blit(text,textrect) #Prints the text
    
    
    counting_time = pygame.time.get_ticks() - start_time #Gives the time of how long the player has been playing
    counting_minutes = str(counting_time/60000).zfill(2) #Changes the start time to seconds and minutes
    counting_seconds = str( (counting_time%60000)/1000 ).zfill(2) 
    counting_string = str(counting_minutes) + ":" + str(counting_seconds) #This prints the time
    counting_text = font.render(str(counting_string), True, WHITE) #This sets the font and colour 
    counting_rect = counting_text.get_rect() #gets x and y values of text
    gameWindow.blit(counting_text, counting_rect)
    
    drawAsteroids() #Prints the obstacles
    pygame.display.update()

#Colors
WHITE = (255,255,255)
BLACK = (0,  0,  0)
RED   = (255, 0,0)

GROUND = 512 #The ground height


bkgd = pygame.image.load("back.jpg") #Imports my background


#Rotation
def rotate(image, angle): #Function to rotate my image 
    ORIGINALrect = image.get_rect()
    rotatedImage = pygame.transform.rotate(image,angle)
    rotatedRect = ORIGINALrect.copy()
    rotatedRect.center = rotatedImage.get_rect().center
    rotatedImage = rotatedImage.subsurface(rotatedRect).copy()
    return rotatedImage

angle = 0 #angle for rotation


#Sound
explosion = pygame.mixer.Sound("explosion.wav") #Sound effect for collision
explosion.set_volume(0.5) #Volume for the sound effect
hit = pygame.mixer.Sound("Hit.wav") #Sound effect for collision
hit.set_volume(0.5) #Volume for the sound effect

clap = pygame.mixer.Sound("clapping.wav")
clap.set_volume(0.1)

def drawAsteroids(): #Draws obstacles
    for i in range(numAsteroids): 
        if asteroidVisible[i]:
            pygame.draw.rect(gameWindow, asteroidCLR[i], (asteroidX[i], asteroidY - asteroidH[i], asteroidW[i] ,asteroidH[i])) #Draws different sized rectangles
        
numAsteroids = 150 #Number of asteroids that will be draw
asteroidH = [] #Appends different heights, widths for each rectangle
asteroidW = [] 
asteroidX = []
asteroidY = GROUND
asteroidVisible = []
asteroidStep = []
asteroidCLR=[]
for i in range(numAsteroids):        # generate the asteroids
    asteroidX.append(randint(WIDTH*-70, 0))  # scattered along 7 screens above the game window
    asteroidH.append(randint(50,90))
    asteroidW.append(randint(50,90))
    asteroidVisible.append(True)
    asteroidStep.append(randint(1,8))
    asteroidCLR.append((randint(0,255), randint(0,255), randint(0,255)))


#Jumping
RUN_SPEED = 10 #Speed of running
JUMP_SPEED = -35 #Height of Jump
GRAVITY = 2

character = pygame.image.load("character.png") #Character image
Ocharacter = character.copy() #Creates a copy for rotation
characterSize = character.get_size() #Gets the width and height of character
objectW = characterSize[0] #The width of character
objectH = characterSize[1] #The height of character
objectX = 450 #The x-value where the character starts
objectY = GROUND #The y-value of the character
objectVx = 0
objectVy = 0

x,y = 0,0


#Scoring
score = 0
highest_time = []

#WHILE LOOP 
print ("Hit ESC to end the program.")


starts = pygame.image.load("start.png") #Start screen
instruction = pygame.image.load("instructions.png") #Introduction Screen
end = pygame.image.load("gameover.png") #End screen
clock = pygame.time.Clock()
FPS = 30
inPlay = True #Used to see if the game is exited or not
display_instructions = True #Used to enter while loop for start and intro screen
instruction_page = 1 #Determines which screen to print

game_over = False #Used when score hits 5000 to end game


def start(inPlay, display_instructions,instruction_page):
    while inPlay and display_instructions:
        pygame.mixer.music.load("music.mp3") #Imports background music
        pygame.mixer.music.set_volume(0.2) #Volume for the sound
        pygame.mixer.music.play(-1) #How many times it plays
        
        mousePosition = pygame.mouse.get_pos()
        x,y = mousePosition #Gets position of mouse
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if (600 > mousePosition[0] > 225 and 500 > mousePosition[1] > 445) and event.type == pygame.MOUSEBUTTONDOWN: #checks if the instruction button is pressed
                instruction_page += 1 #This goes into the intro screen
    
        if instruction_page == 1: #Prints start screen
            
            gameWindow.blit(starts,(0,0))
            if (470 > mousePosition[0] > 332 and 379 > mousePosition[1] > 245)  and event.type == pygame.MOUSEBUTTONDOWN: #If the start button is pressed, the game starts
                display_instructions = False #Used to enter next while loop
     
        if instruction_page == 2:
            gameWindow.blit(instruction,(0,0))
            if (760 > mousePosition[0] > 660 and 561 > mousePosition[1] > 463) and event.type == pygame.MOUSEBUTTONDOWN: #If the back button is picked, it will return back to the start screen
                instruction_page -= 1 
        
        pygame.display.update()
    
   
start(inPlay, display_instructions, instruction_page)
start_time = pygame.time.get_ticks() #Starts timer
while inPlay:
    if game_over == False: #Starts the game if the if the score is under 5000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        redrawGameWindow()
        clock.tick(FPS)
        
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = False
    
        #Moving Background
        rel_x = x % bkgd.get_rect().width
        gameWindow.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < WIDTH:
            gameWindow.blit(bkgd, (rel_x, 0))
        x += 6 #Speed to the background moves at
        
        #Jumping
        if objectX + objectW >= WIDTH:
            objectX -= objectW
        if objectX == 0:
            objectX += objectW
        # set horizontal and vertical velocity    
        if keys[pygame.K_UP] and objectY + objectH == GROUND:
            # if the UP key is pressed and the object is on the ground
            objectVy = JUMP_SPEED
            angle += 90
            character = rotate(Ocharacter,angle)
        elif keys[pygame.K_LEFT]:
            objectVx = -RUN_SPEED
        elif keys[pygame.K_RIGHT]:
            objectVx = RUN_SPEED
        else:
            objectVx = 0
    # move the object in horizontal direction
        objectX = objectX + objectVx
    # update object's vertical velocity
        objectVy = objectVy + GRAVITY
    # move the object in vertical direction
        objectY += objectVy
        if objectY+objectH >= GROUND:
            objectY = GROUND - objectH
            objectVy = 0
        
        #Moving the obstacles
        for i in range(numAsteroids):
            asteroidX[i] += asteroidStep[i]
            if 0 > asteroidX[i] > 800 + asteroidW[i]:
                asteroidX[i] = -6*WIDTH
                asteroidVisible[i] = True
        
        #Collision between obstacle and player   
        for i in range(numAsteroids):
            if asteroidVisible[i] and ((asteroidY - asteroidH[i]) +asteroidH[i]) > objectY and ((asteroidY - asteroidH[i])-asteroidH[i]) < objectY and (asteroidX[i]+asteroidW[i]) > objectX and (asteroidX[i] - asteroidW[i]) < (objectX):
                asteroidVisible[i] = False
                explosion.play()
                score -= 250
        #Every 15 seconds 870 points are added per millisecond from 15- 16 seconds
        if float((pygame.time.get_ticks() - start_time)/1000) >= 10 and float((pygame.time.get_ticks() - start_time)/1000)%15 == 0:
            score += 30
            
        
        #Boundaries for the sides
        if  objectX <= 0:
            hit.play() #Sound plays when character hits sides
            objectX = 0
            
        if  objectX + objectW >= WIDTH:
            hit.play()
            objectX = WIDTH - objectW
            
        
        if score > 5000: #if score passes 5000 the game ends and enters the game_over section
            highest_time.append((pygame.time.get_ticks() - start_time)/1000)
            game_over = True
            

    
    if game_over: #prints end screen and allows for the player to restart
        mousePosition = pygame.mouse.get_pos()
        x,y = mousePosition #Gets position of mouse
        
        pygame.mixer.music.fadeout(10) #Ends music
        pygame.display.set_caption("Times New Roman")
        font = pygame.font.SysFont(None,60)
        text = font.render("Time: " + str(highest_time[-1]) + " seconds" , True, WHITE) #prints time of round played
        highs = font.render("Highest Time: " + str(min(highest_time)) + " seconds", True, WHITE) #prints the best time (so the lowest time)
        
        pygame.time.delay(5) #added 5 millisecond pause to make the screen transition better into the end screen
        clap.play() #plays claping sound instead of the music
        gameWindow.blit(end,(0,0)) #displays end screen
        gameWindow.blit(text,(161, 320)) #displays texts
        gameWindow.blit(highs,(161, 239))
        pygame.display.flip() #Updates screen
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if 551 > mousePosition[0] > 208 and 560 > mousePosition[1] > 462 and event.type == pygame.MOUSEBUTTONDOWN: #if the restart button is pressed
                display_instructions = True
                game_over = False
                score = 0 #Reset the variables for time and score if the player chooses to replay
                start_time = 0
                start_time = pygame.time.get_ticks()# restarts timer 
                start(inPlay, display_instructions, instruction_page) #prints intro page again
            
        
         

pygame.quit()
