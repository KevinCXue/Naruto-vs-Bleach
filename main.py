###################### FINAL PROJECT BY: ANAS AHMED AND KEVIN XUE

################## 2-D Platform Fighter Game

from random import randint
from math import hypot

from pygame import Rect, display, draw, event, image, key, mouse, time, transform
from pygame.locals import *

from player import Player


# Below is a 2d list that loads the character sprites 
# The same type of sprite (for example; walk, attack, stand) are in their own list using list comprehension
# which are all contain inside one character list

########### CHARACTERS ###########

# Naruto Uzumaki
naruto=[[image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(1,7)], # Stand
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(7,13)], # Walk
        [image.load("assets\\naruto\\naruto24.png")], # Block
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(13,17)], # Jump
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(17,19)], # Hurt Light
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(19,23)], # Hurt Hard
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(23,36)], # Soft Attack
        [image.load("assets\\naruto\\naruto"+str(i)+".png") for i in range(36,40)]] # Hard Attack

# The code below will resize each of the sprite for naruto appropriately since naruto sprites are the smallest
for i in range(len(naruto)):
    naruto[i]=[transform.scale(x, (int(1.4 * x.get_width()), int(1.4 * x.get_height()))) for x in naruto[i]]
    
# Link 
link=[[image.load("assets\\link\\link"+str(i)+".png") for i in range(24,28)], # Stand
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(17,23)], # Walk
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(28,36)], # Run
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(36,40)], # Jump
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(23,25)], # Hurt Light
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(23,25)], # Hurt Hard
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(40,51)], # Soft Attack
      [image.load("assets\\link\\link"+str(i)+".png") for i in range(51,56)]] # Hard Attack

# Itachi Uchiha
itachi=[[image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(1,5)], # Stand
        [image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(11,17)], # Walk
        [image.load("assets\\itachi\\itachi21.png")], # Block
        [image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(17,21)], # Jump
        [image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(22,24)], # Hurt Light
        [image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(24,28)], # Hurt Hard
        [image.load("assets\\itachi\\itachi"+str(i)+".png") for i in range(28,41)], # Soft Attack
        [transform.flip(image.load("assets\\itachi\\itachi"+str(i)+".png"),1,0) for i in range(41,45)]] # Hard Attack

# Gaara of the Sand
gaara=[[image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(1,5)], # Stand
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(11,17)], # Walk
        [image.load("assets\\gaara\\gaara22.png")], # Block
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(18,22)], # Jump
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(23,29)], # Hurt Light
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(23,29)], # Hurt Hard
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(29,43)], # Soft Attack
        [image.load("assets\\gaara\\gaara"+str(i)+".png") for i in range(43,55)]] # Hard Attack

# Ichigo Kurosaki
ichigo=[[image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(2,6)], # Stand
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(6,14)], # Walk
        [image.load("assets\\ichigo\\ichigo19.png") ], # Block
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(14,18)], # Jump
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(32,34)], # Hurt Light
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(35,39)], # Hurt Hard
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(48,80)], # Soft Attack
        [image.load("assets\\ichigo\\ichigo"+str(i)+".png") for i in range(80,88)]] # Hard Attack


# Sprites for Chakra Regen Aura
aura=[image.load("assets\\effects\\aura\\aura"+str(i)+".png") for i in range(1,11)]



######## Character Selection #######

player_1=ichigo[:]
player_2=naruto[:]

player_1_obj = Player()
player_2_obj = Player()


screen = display.set_mode((800, 600))
running = True
myClock = time.Clock()

loopCount = 0 # A counter that increases by one every loop


####    PLAYER 1 VARIABLES    ####
# is_player_1_grounded=True  # status of whether or not player 1 is touching ground or not
p1x,p1y=200,300 # starting position of player 1
player_1_direction='Right' # direction of player 1
p1sprite=player_1[0][0] # this variable holds the sprite image of player 1
# Below are counters that keep track of the position in a list of a certain type of sprite, example: walking,jumping
p1wc=0  # walk
p1sc=0  # stand
p1cc=0  # combo attack/soft attack
p1hc=0  # hard attack
p1shc=0 # soft hurt
player_1_choice="none" # Keeps track of player 1's choice
p1block=False # Keeps track if player 1 is blocking or not
p1safe=0 # Keeps track of time invincible
p1protect=False # Keeps track if you are invincible or not

p1vely=0 # y velocity of player 1
p1softhurt=False  # indicates if player is getting hurt or not
p1rect=Rect(p1x,p1y,p1sprite.get_width(),p1sprite.get_height()) # rectangle of player 1 sprite
p1health,p1chakra=100,50 # health and chakra/energy of character 
p1jump,p1djump=0,0 # p1jump holds the position in a list of jump sprites for current jump, p1djump indicates stage of double
# jump

####    PLAYER 2 VARIABLES    ####
#Note, these are almost same variable as player 1 and therefore do not need to be commented again
is_player_2_grounded=True 
p2x,p2y=600,300
player_2_direction='Left'
p2sprite=player_2[0][0]
p2wc=0
p2sc=0
p2cc=0
p2hc=0
p2shc=0
p2vely=0
p2softhurt=False
p2rect=Rect(p2x,p2y,p2sprite.get_width(),p2sprite.get_height())
p2health,p2chakra=100,50
p2jump,p2djump=0,0

player_2_choice="none" # Keeps track of player 2's choice
p2block=False # Keeps track if player 2 is blocking or not
p2safe=0 # Keeps track of time invincible
p2protect=False # Keeps track if you are invincible or not


ac=0 # Position for the chakra recovering aura, used by both players
######################### STAGE LOADING ###########################
stages = [image.load("assets\\stages\\stage"+str(i+1)+".png") for i in range(5)]
stage_hitboxes = [[Rect(0,160,350,50),Rect(0,160,350,50),Rect(515,160,285,50),Rect(0,364,523,50),Rect(-100,550,1000,50)],
          [Rect(200,105,510,40),Rect(90,380,610,40)],
          [Rect(0,550,800,40)],
          [Rect(0,530,800,40),Rect(170,238,460,40)],
          [Rect(0,420,250,40),Rect(550,420,250,40),Rect(0,580,800,40)]]

### General Functions ###
## These are most of the functions used in our program ###########

########## PAGE FUNCTIONS ##############
# When these page functions are called, it draws a certain page
# using if statements, the pages are linked to other pages
start=False     #Determines if the game is started or not
page="frontpage" #Determines the page to show

fpics=[image.load("assets\\menu\\main.jpg"), #contain pictures for frontpage/firstpage
       [image.load("assets\\menu\\buttons"+str(i)+".png") for i in range(1,5)]]

def frontpage():#once this function is called
    global page
    # it blits all the images, and draws button images, when u hover your mouse over it, it draws
    # another highlighted image by checking if mouse collide with the button rect, if the
    # user clicks the start game button, the page is changed to playerselect,
    # if the user clicks the instructions button, the page is changed to instruction page
    screen.blit(fpics[0],(0,0))
    if Rect(300,250,fpics[1][0].get_width(),fpics[1][0].get_height()).collidepoint(mx,my):
        screen.blit(fpics[1][1],(300,250))
        if mb[0]==1:
            page="playerselect"
    else: screen.blit(fpics[1][0],(300,250))
    if Rect(300,300,fpics[1][2].get_width(),fpics[1][0].get_height()).collidepoint(mx,my):
        screen.blit(fpics[1][3],(300,300))
        if mb[0]==1:
            page="instruction"
    else: screen.blit(fpics[1][2],(300,300))
    
#ipics contains images for the instruction page
ipics=[image.load("assets\\menu\\instruction.png"),
   [image.load("assets\\menu\\goback"+str(i)+".png") for i in range(1,3)]] #go back buttons

def instruction():
    global page
    #this page blits a background that contains instructions, and has a go back button which
    #sends the user back to first page, it uses a similar, mouse-button collide detection
    #used in the last page
    screen.blit(ipics[0],(0,0))
    if Rect(50,50,100,100).collidepoint(mx,my):
        screen.blit(ipics[1][1],(50,50))
        if mb[0]:
            page="frontpage"
    else: screen.blit(ipics[1][0],(50,50))
    
#The next bunch of code, contains variables for the character selection page
playable_characters=["naruto","link","itachi","gaara","ichigo"] # List of characters
#loads images below into variables
selectpic= [image.load("assets\\pic\\"+playable_characters[i]+"_pic.png") for i in range(5)]#picture box
selectstand= [image.load("assets\\pic\\"+playable_characters[i]+"_stance.png") for i in range(5)]#cool stance
selectback=image.load("assets\\menu\\select.jpg")
startbutton=image.load("assets\\menu\\startbutton.png")


def playerselect(): #player select page
    global page,player_1_choice,player_2_choice,player_1,player_2
    screen.blit(selectback,(0,0)) #draws back
    if player_1_choice=="none": #once the first player is not choosen
        for i in range(5): #it goes through 5 numbers and blits image best on a factor of those number
            #in appropriate places
            screen.blit(transform.scale(selectpic[i],(100,100)),(i*120+100,400))

            #if the players mouse collides with a picture, it draws box around it
            #and it draws the stand picture of the character
            if Rect(i*120+100,400,100,100).collidepoint((mx,my)): 
                draw.rect(screen,(255,0,0),Rect(i*120+100,400,100,100),2)
                screen.blit(transform.scale(selectstand[i],(100,300)),(100,50))
                if mb[0]==1:
                    #once the player clicks on the picture
                    #the player_1_choice variable contain the name of the player using the playable_characters(player name list)
                    player_1_choice=playable_characters[i]
                    time.wait(800) #waits a bit so the user doesnt click twice and chooses player 2 character
            screen.blit(ipics[1][0],(330,540))#this draws a button to go back to the main menu
            if Rect(330,540,153,35).collidepoint((mx,my)):  
                screen.blit(ipics[1][1],(330,540)) #once clicked
                if mb[0]==1: #it sends user to main menu page
                    page="frontpage"
                    player_1_choice="none"
                    player_2_choice="none"
                    break
                
    elif player_1_choice!="none" and player_2_choice=="none": #once player 1 has chosen a character
        for i in range(5): #it does the same thing for player 2 as the code above, but draws and outline around
            #player 1 character and draws an image of his character on the left
            screen.blit(transform.scale(selectpic[i],(100,100)),(i*120+100,400))
            draw.rect(screen,(255,0,0),Rect(playable_characters.index(player_1_choice)*120+100,400,100,100),2)
            screen.blit(transform.scale(selectstand[playable_characters.index(player_1_choice)],(100,300)),(100,50))
            if Rect(i*120+100,400,100,100).collidepoint((mx,my)):
                draw.rect(screen,(0,0,255),Rect(i*120+100,400,100,100),2)
                screen.blit(transform.flip(transform.scale(selectstand[i],(100,300)),1,0),(600,50))
                if mb[0]==1:
                    player_2_choice=playable_characters[i] #player 2 character is choosen
            screen.blit(ipics[1][0],(330,540))#go back button
            if Rect(330,540,153,35).collidepoint((mx,my)): 
                screen.blit(ipics[1][1],(330,540))
                if mb[0]==1:
                    page="frontpage"
                    player_1_choice="none"
                    player_2_choice="none"
                    break  
    elif player_1_choice!="none" and player_2_choice!="none": #once both characters are choosen
        for i in range(5):#it draws a start button, that grows once the users mouse goes over it
            #it draws everything else; player 1 and player 2 character is highlighted and drawn
            screen.blit(transform.scale(selectpic[i],(100,100)),(i*120+100,400))
            draw.rect(screen,(255,0,0),Rect(playable_characters.index(player_1_choice)*120+100,400,100,100),2)
            draw.rect(screen,(0,0,255),Rect(playable_characters.index(player_2_choice)*120+100,400,100,100),2)   
            screen.blit(transform.scale(selectstand[playable_characters.index(player_1_choice)],(100,300)),(100,50))
            screen.blit(transform.flip(transform.scale(selectstand[playable_characters.index(player_2_choice)],(100,300)),1,0),(600,50))
            screen.blit(startbutton,(400-50,300-50-100))
            if Rect(350,250-100,100,100).collidepoint((mx,my)):
                screen.blit(transform.scale(startbutton,(150,150)),(400-75,300-50-100-25))
                if mb[0]==1: #once the player clicks the start button;
                    player_1=eval(player_1_choice) #this converts a string (player_1_choice) into a variable
                    player_2=eval(player_2_choice) #it makes the players sprite= to the appropriate character sprites
                    page="stage" #page turns into the stage page next
            screen.blit(ipics[1][0],(330,540)) #go back button code below
            if Rect(330,540,153,35).collidepoint((mx,my)):
                screen.blit(ipics[1][1],(330,540))
                if mb[0]==1:
                    page="frontpage" 
                    player_1_choice="none"
                    player_2_choice="none"
                    break

#Stage page code below
stageback=image.load("assets\\menu\\stageback.jpg") #background image of stage page
def stage():
    global page, platforms, selected_stage, start
    screen.blit(stageback,(0,0)) #draws the stage
    for i in range(5):
        screen.blit(transform.scale(stages[i],(120,90)),(40+i*150,500)) #draws the 5 stages appropriatly
        if Rect(40+i*150,500,120,90).collidepoint(mx,my): #if mouse goes over it 
            screen.blit(transform.scale(stages[i],(120,90)),(40+i*150,500)) #it draws a bigger picture of map
            draw.rect(screen,(255,0,0),(40+i*150,500,120,90),1) #and highlights it
            screen.blit(transform.scale(stages[i],(600,400)),(100,0))
            
            if mb[0]==1:
                start=True #the actual game starts once this status is true
                platforms=stage_hitboxes[i] #it sets the platforms into the appropriate map platforms
                selected_stage=stages[i] #the middle ground is also set




# Below is the page for the end screen which activates once a person has died
def end():
    global page,running
    screen.blit(transform.scale(selectback,(1200,900)),(0,0))
    if p1health>p2health:
        screen.blit(image.load("assets\\end\\player1win.png"),(300,200))
    else:
        screen.blit(image.load("assets\\end\\player2win.png"),(300,200))

            
    play_again_button_image = image.load("assets\\end\\play_again.png")
    quit_button_image = image.load("assets\\end\\quit.png")
    screen.blit(play_again_button_image,(300,300))
    if Rect(300, 300, play_again_button_image.get_width(), play_again_button_image.get_height()).collidepoint(mx,my) and mb[0]==1:  # TODO: do proper reset
        page="frontpage"

    screen.blit(quit_button_image,(300,400))
    if Rect(300, 400, quit_button_image.get_width(), quit_button_image.get_height()).collidepoint(mx,my) and mb[0]==1:
        running=False
        
#list of platform rects in a stage



# This function takes in a list of rectangle and checks whether a player has landed on it
#and then makes ground status true, sets velocity to 0, and other changes

def platform(platforms, player1):
    global p1x,p1y,p1djump,p1vely
    global p2x,p2y,p2djump,p2vely,is_player_2_grounded

    #Goes through the list of rectangles, checks if bottom of a sprite collides with each rect
    #if it does it sets ground true, and player position so it is on top of platform, and double jump stage is reset to 0
    #the velocity of y is turned to 0
    for i in range(len(platforms)):
        if platforms[i].collidepoint(p1x+p1sprite.get_width()/2,p1y+p1sprite.get_height()) and p1vely<=0 and not player1.is_grounded:
            p1y=platforms[i].y-player_1[0][0].get_height()
            player1.is_grounded=True
            p1vely=0
            p1djump=0
            break
        else:
            player1.is_grounded=False
    # Same thing for player 2
    for i in range(len(platforms)):
        if platforms[i].collidepoint(p2x+p2sprite.get_width()/2,p2y+p2sprite.get_height()) and p2vely<=0 and is_player_2_grounded==False:
            p2y=platforms[i].y-player_2[0][0].get_height()
            is_player_2_grounded=True
            p2vely=0
            p2djump=0
            break
        else:
            is_player_2_grounded=False

#The code below, draws food on the screen for player to grab to heal themselves
#it draws a random food every random time between 1, 100 loops
#if player goes over it he heals himself randomly from 0 to 25 health points
            
foods=[image.load("assets\\foods\\food"+str(i)+".png") for i in range(1,15)] #list of food sprites
#Below is a food counter that counts till hit a limit of when to pop a food in the field
foodc=0
#The food status states whether or not food is in the field
foodstatus=False
#The limit stops when a certain number of loops has passed so it can spawn another food
limit=100

#food keeps track of food image
food=foods[0]
#fx,fy is position of food
fx,fy=0,0
def foodsss():
    global foodc,foodstatus,limit,fx,fy,food,p1health,p2health
    #food status is on once a limit is reached
    if foodc==limit:
        foodstatus=True
        food=foods[randint(0,len(foods)-1)]
        fx,fy=randint(100,700),randint(100,500)
    #food counter increases
    foodc+=1

    #draws food if food status is on
    if foodstatus==True:
        screen.blit(food,(fx,fy))

    #if player 1 touches food , he heals himself
    if Rect(fx,fy,food.get_width(),food.get_height()).colliderect(p1rect) and foodstatus==True:
            p1health+=randint(0,5)
            foodstatus=False
            limit=randint(1,100)
            foodc=0
    #same for player 2
    elif Rect(fx,fy,food.get_width(),food.get_height()).colliderect(p2rect) and foodstatus==True:
            p2health+=randint(0,5)
            foodstatus=False
            limit=randint(1,100)
            foodc=0

#The function below just teleports(moves x value) player to other side of field if it goes out of the screen on one side        
def mapsides():
    global p1x,p2x
    if p1x>800: p1x=-50
    elif p1x<-50:p1x=800
    if p2x>800:p2x=-50
    elif p2x<-50:p2x=800

# The direction function is used to make other code work easily and cleanly
# It flips the image based on direction
def direction(x,direction):
    if direction=="Right":
        return x
    else:
        return transform.flip(x,1,0)
    
#The health function deals with the health and chakra of players
def health():
    global p1health,p2health,p1y,p2y
    global p1chakra,p2chakra
    global page, start
    if p1y>700: #kils player if he falls off land
        p1health=0
    if p2y>700:
        p2health=0
    #Below will make sure health does not go above 100
    if p1health>100:p1health=100
    if p1health<=0:
        page="end"
        start=False
    if p1chakra>100:p1chakra=100
    if p1chakra<0:p1chakra=0
    if p2health>100:p2health=100
    if p2health<=0:
        page="end"
        start=False

    
    if p2chakra>100:p2chakra=100
    if p2chakra<0:p2chakra=0

    #This recovers chakra over time
    p1chakra+=0.01
    p2chakra+=0.01

    #Draws Health Bars and Chakra Bars using the percent of health
    draw.rect(screen,(255,0,0),(0,0,3*p1health,20))
    draw.rect(screen,(0,0,0),(0,0,3*p1health,20),1)
    draw.rect(screen,(255,0,50*p2health/100),(800-3*p2health,0,3*p2health,20))
    draw.rect(screen,(0,0,0),(800-3*p2health,0,3*p2health,20),1)

    draw.rect(screen,(0,90,255),(0,20,3*p1chakra,20))
    draw.rect(screen,(0,0,0),(0,20,3*p1chakra,20),1)
    draw.rect(screen,(0,90,255),(801-3*p2chakra,20,3*p2chakra,20))
    draw.rect(screen,(0,0,0),(801-3*p2chakra,20,3*p2chakra,20),1)

background=image.load("assets\\backgrounds\\background" + str(randint(1,5)) + ".jpg")

# Function that draws the stage and background
def draw_environment():
    # Using an Algorithm created by Anas Ahmed, this moves the background map so the game looks 3 dimensional
    screen.blit(background,(0,(-p1y-p2y-background.get_height())/8))
    # This displays the background over it
    screen.blit(selected_stage,(0,0))
    
    
#The functions below adds velocity to each players y value, if the ground is false, meaning they are in the air
#The velocity is increased 
def groundcheck(player1):
        global p1vely,p1y
        global p2vely,p2y
        
        p1y-=p1vely
        if not player1.is_grounded:p1vely-=0.5
        p2y-=p2vely
        if is_player_2_grounded==False:p2vely-=0.5


#The loopcounter, changes all the sprite positions of player based on the Loop Counter
def loopcounter():
    global loopCount,ac
    global p1wc,p1sc,p1cc,p1hc,p1shc
    global p2wc,p2sc,p2cc,p2hc,p2shc

    #loopcounter increases by 1 every loop
    loopCount += 1

    #changes the other list positions
    #Credits: To Mr. Mckenzie for helping in making this formula
    #example; the  loopCount%10==0 says that every 10 loop do this:
                #the walk counter is increased by 1, and the % resets it once it hits max
                #value in list the counter was designed for

    #this is repeated for all he counter, each with their own preferences
    if loopCount % 10 == 0:
        p1wc = (p1wc + 1) % len(player_1[1])                    
    if loopCount % 10 == 0:
        p1sc= (p1sc + 1) % len(player_1[0])        
    if loopCount % 3 == 0:
        p1cc= (p1cc + 1) % len(player_1[6])
    if loopCount % 3 == 0:
        p1hc= (p1hc + 1) % len(player_1[7])
    if loopCount % 3 == 0:
        p1shc= (p1shc + 1) % len(player_1[4])

    
    if loopCount % 10 == 0:
        p2wc = (p2wc + 1) % len(player_2[1])                    
    if loopCount % 10 == 0:
        p2sc= (p2sc + 1) % len(player_2[0])        
    if loopCount % 3 == 0:
        p2cc= (p2cc + 1) % len(player_2[6])
    if loopCount % 3 == 0:
        p2hc= (p2hc + 1) % len(player_2[7])
    if loopCount % 3 == 0:
        p2shc= (p2shc + 1) % len(player_2[4])
        
    if loopCount % 3 == 0:
        ac= (ac + 1) % len(aura)

#the functions below, changes the jump positions based on each players velocity
#there are 4 different positions at different moment of when a character is jumping
def jumpanimation():
    global p1jump,p2jump
    if p1vely>12 and p1vely<15:
        p1jump=0
    if p1vely>10 and p1vely<12:
        p1jump=1
    if p1vely>5 and p1vely<10:
        p1jump=2
    if p1vely<5 and p1vely<-5:
        p1jump=3
        
    if p2vely>12 and p2vely<15:
        p2jump=0
    if p2vely>10 and p2vely<12:
        p2jump=1
    if p2vely>5 and p2vely<10:
        p2jump=2
    if p2vely<5 and p2vely<-5:
        p2jump=3

#The code below does a sprite animation of someone falling after being hit by a strong attack
        
p1fallcount=0 #a counter that repreasents position in a fall sprite list
p1fallstatus=False #status of when the fall begins, this can be changed outside the function to trigger the function
#once it is True the functions starts to do the fall animation
p2fallcount=0
p2fallstatus=False
def falls():
    global p1fallcount,p1fallstatus,p1sprite,p1safe
    global p2fallcount,p2fallstatus,p2sprite,p2safe
    
    #once the status is true
    if p1fallstatus==True:
        if p1safe==0:
            p1safe=50 #Renewing invincibility
        #every 6 loops the position changes
        if loopCount % 6 == 0:
            p1fallcount= (p1fallcount+ 1)
        #once it hits the last image
        if p1fallcount==len(player_1[5]):
            #it is turned into False
            p1fallstatus=False
            #the counter is reset
            p1fallcount=0
        #it sets the player sprite to be a fall sprite based on player direction
        if player_2_direction=="Left":
            p1sprite=player_1[5][p1fallcount]
        else:p1sprite=transform.flip(player_1[5][p1fallcount],1,0)

    #same for player 2
    elif p2fallstatus==True:
        if p2safe==0:       
            p2safe=50
        if loopCount % 6 == 0:
            p2fallcount= (p2fallcount+ 1)
        if p2fallcount==len(player_2[5]):
            p2fallstatus=False
            p2fallcount=0
        if player_1_direction=="Left":
            p2sprite=player_2[5][p2fallcount]
        else:p2sprite=transform.flip(player_2[5][p2fallcount],1,0)

# The function below indicates when invincibility is turned on so the other guy
# cannot hurt the player once they're down
def invincibility():
    global p1safe,p2safe,p1protect,p2protect
    if p1safe>0:        # If the time is not up yet
        p1safe-=1
        p1protect=True  # the player is still invincible
    else:
        p1protect=False
        
    if p2safe>0:
        p2safe-=1
        p2protect=True
    else:
        p2protect=False
    
        
        
###################### SPECIAL FUNCTIONS ################################

#this function just calls the special attack functions based on who the player is
#as you can see below the special attack functions are called every loop and most of them are
#real time
        
def special():
    if player_1==naruto or player_1==ninetail:
        narutos1p1()
        narutos2p1()
    elif player_1==gaara:
        gaaras1p1()
        gaaras2p1()
    elif player_1==itachi:
        itachis1p1()
        itachis2p1()
    elif player_1==ichigo or player_1==bankai:
        ichigos1p1()
        ichigos2p1()
    elif player_1==link:
        links1p1()
        links2p1()
    
    if player_2==naruto or player_2==ninetail:
        narutos1p2()
        narutos2p2()
    elif player_2==gaara:
        gaaras1p2()
        gaaras2p2()
    elif player_2==itachi:
        itachis1p2()
        itachis2p2()
    elif player_2==ichigo or player_2==bankai:
        ichigos1p2()
        ichigos2p2()
    elif player_2==link:
        links1p2()
        links2p2()
        

####### ITACHI SPECIAL #########
#contains the images needed for the first itachi special
itachis1part1=[image.load("assets\\itachiS1\\itachiS"+str(x)+".png") for x in range(1,12)] #sprites
itachis1part2=[image.load("assets\\itachiS1\\itachi"+str(x)+".png") for x in range(1,21)] #blast
itachis1p1special=False #status to indicate if special is running or not
itachis1p1count=0 #keeps count of sprite position in list
itachis1p1count2=0 #keeps count of sprite position in other list
p1tempx,p1tempy=0,0 #variables to hold player_1 position so he does not move while he
#uses attack
itachis1p1dm=10 #distance the fire is away from player

def itachis1p1():
    global itachis1p1special,itachis1p1count,itachis1p1count2,p1sprite,p2health,p2x
    global p1vely,itachis1p1dm,p1tempx,p1tempy,p1x,p1y,p1chakra

    #Turns itachi special on once conditions are met,ex. appropriate key etc.
    if itachis1p1special==False and key.get_pressed()[K_u] and p1chakra>=25:
        #removes energy, resets counter, sets up temp position, and turns on special status 
        p1chakra-=25
        itachis1p1count,itachis1p1count2=0,0
        p1tempx,p1tempy=p1x,p1y
        itachis1p1dm=10
        itachis1p1special=True
    elif itachis1p1special==True:
        #once its true, the dm (distance moved) increases by 1 per loop
        itachis1p1dm+=1
        p1x,p1y=p1tempx,p1tempy #player 1 position is locked to when the player started attack
        p1vely=0 #velocity is reset

        #if player_1 is facing left
        if player_1_direction=="Left":
            #it calculates the picture to display, the rect of fireball,
            #it is broken down into simpler variables to keep things clean
            pic=itachis1part2[itachis1p1count2]
            x=p1x-itachis1part2[itachis1p1count2].get_width()-100-itachis1p1dm #the x value increases by the dm variable
            y=p1y-itachis1part2[itachis1p1count2].get_height()+78 #the height is fixed
            w=itachis1part2[itachis1p1count2].get_width() 
            h=itachis1part2[itachis1p1count2].get_height()
            #w and h are width and height
            p1sprite=itachis1part1[itachis1p1count] #the player sprite is equal to the sprite at certain loop count
            screen.blit(pic,(x,y)) #draws the fireball picture on screen
            #Below, uses the rect of the fire and check if it collides with player rect, if it does
            # player health decreases and the player is pushed to the left
            attackrect=Rect(x,y,w,h)
            if attackrect.colliderect(p2rect):
                p2health-=.5
                p2x-=1
        else: #Below is just a repeat and a little bit modified, it does the same thing but mirrored in the
            #oposite direction
            pic=transform.flip(itachis1part2[itachis1p1count2],1,0)
            x=p1x+itachis1part2[itachis1p1count2].get_width()+100+itachis1p1dm
            y=p1y-itachis1part2[itachis1p1count2].get_height()+78
            w=itachis1part2[itachis1p1count2].get_width()
            h=itachis1part2[itachis1p1count2].get_height()
            p1sprite=transform.flip(itachis1part1[itachis1p1count],1,0)
            screen.blit(pic,(x,y))
            attackrect=Rect(x,y,w,h)
            if attackrect.colliderect(p2rect):
                p2health-=.5
                p2x+=1

                
        if loopCount % 3 == 0: #this says that every 3 loops
            itachis1p1count= (itachis1p1count + 1) % len(itachis1part1) #the count of the sprite increases
            #and reset once it hits the last sprite in list
            
        if loopCount % 3 == 0:
            itachis1p1count2= (itachis1p1count2 + 1) #this works the same way but for the fire
            
        if itachis1p1count2==19: #once the fire is complete special is turned off
            itachis1p1special=False

#Below is just a repeat for player 2 using the player 2 variables
itachis1p2special=False
itachis1p2count=0
itachis1p2count2=0
p2tempx,p2tempy=0,0

def itachis1p2():
    global itachis1p2special,itachis1p2count,itachis1p2count2,p2sprite
    global p1health,p1x,p2vely,itachis1p2dm,p2tempx,p2tempy,p2x,p2y,p2chakra
    if itachis1p2special==False and key.get_pressed()[K_KP4] and p2chakra>=25:
        p2chakra-=25
        itachis1p2count,itachis1p2count2=0,0
        p2tempx,p2tempy=p2x,p2y
        itachis1p2dm=10
        itachis1p2special=True
    elif itachis1p2special==True:
        itachis1p2dm+=1
        p2x,p2y=p2tempx,p2tempy
        p2vely=0
        if player_2_direction=="Left":
            pic=itachis1part2[itachis1p2count2]
            x=p2x-itachis1part2[itachis1p2count2].get_width()-100-itachis1p2dm
            y=p2y-itachis1part2[itachis1p2count2].get_height()+78
            w=itachis1part2[itachis1p2count2].get_width()
            h=itachis1part2[itachis1p2count2].get_height()
            p2sprite=itachis1part1[itachis1p2count]
            screen.blit(pic,(x,y))
            attackrect=Rect(x,y,w,h)
            if attackrect.colliderect(p1rect):
                p1health-=.5
                p1x-=1  
        else:
            pic=transform.flip(itachis1part2[itachis1p2count2],1,0)
            x=p2x+itachis1part2[itachis1p2count2].get_width()+100+itachis1p2dm
            y=p2y-itachis1part2[itachis1p2count2].get_height()+78
            w=itachis1part2[itachis1p2count2].get_width()
            h=itachis1part2[itachis1p2count2].get_height()
            p2sprite=transform.flip(itachis1part1[itachis1p2count],1,0)
            screen.blit(pic,(x,y))
            attackrect=Rect(x,y,w,h)
            if attackrect.colliderect(p1rect):
                p1health-=.5
                p1x+=1
        if loopCount % 3 == 0:
            itachis1p2count= (itachis1p2count + 1) % len(itachis1part1)
        if loopCount % 3 == 0:
            itachis1p2count2= (itachis1p2count2 + 1) 
        if itachis1p2count2==19:
            itachis1p2special=False

# For Itachi's special 2, Itachi traps his opponent in an genjutsu.
# Everything freezes and Itachi stabs his opponent over time

# Images for the animation below are loaded
itachis2part1=[image.load("assets\\itachiS2\\Itachi"+str(i)+".png") for i in range(1,7)]
itachis2part2=[image.load("assets\\itachiS2\\ItachiS"+str(i)+".png") for i in range(1,15)]
itachifront=transform.scale(image.load("assets\\itachiS2\\Itachifront.png"),(1000,300))
itachiback=image.load("assets\\itachiS2\\ItachiBack.jpg")
cross=image.load("assets\\itachiS2\\cross.png")

def itachis2p1():
    global p2health, p1chakra
    if key.get_pressed()[K_i] and p1chakra>=50: #starts when the condition is met
        p1chakra-=40
        for i in range(len(itachis2part1)):
            for j in range(3): 
                draw_environment() #draws back / health
                health()
                if player_1_direction=="Left": #draws the player using hand signs
                    screen.blit(transform.flip(itachis2part1[i],1,0),(p1x,p1y))
                else:
                    screen.blit(itachis2part1[i],(p1x,p1y))
                screen.blit(p2sprite,(p2x,p2y))  #draws player_2 sprite
                display.flip()
        for i in range(100):
            screen.blit(itachifront,(0-i,100)) #a banner is moved across screen
            display.flip()
        for i in range(len(itachis2part2)*2):
            for j in range(10):
                screen.blit(transform.scale(itachiback,(850,650)),(0-randint(0,10),0-randint(0,10))) #draws a randomly moving
                #background
                health()#health bar
                #draws player who used the attack, attacking the victim on a cross
                screen.blit(itachis2part2[i%len(itachis2part2)],(370,300)) 
                screen.blit(cross,(400,300))
                screen.blit(transform.flip(player_2[4][j%2],1,0),(410,300))
                draw.line(screen,(255,255,255),(0,375),(800,375))
                display.flip()
                p2health-=0.08 #health is decreased slowly

# Below is the same attack for player 2 with player 2 variables
def itachis2p2():
    global p1health,p2chakra
    if key.get_pressed()[K_KP5] and p2chakra>=50:
        p2chakra-=50
        for i in range(len(itachis2part1)):
            for j in range(3):
                draw_environment()
                health()
                if player_2_direction=="Left":
                    screen.blit(transform.flip(itachis2part1[i],1,0),(p2x,p2y))
                else:
                    screen.blit(itachis2part1[i],(p2x,p2y))
                screen.blit(p1sprite,(p1x,p1y))
                display.flip()
        for i in range(100):
            screen.blit(itachifront,(0-i,100))
            display.flip()
        for i in range(len(itachis2part2)*2):
            for j in range(10):
                screen.blit(transform.scale(itachiback,(850,650)),(0-randint(0,10),0-randint(0,10)))
                health()
                screen.blit(itachis2part2[i%len(itachis2part2)],(370,300))
                screen.blit(cross,(400,300))
                screen.blit(transform.flip(player_1[4][j%2],1,0),(410,300))
                draw.line(screen,(255,255,255),(0,375),(800,375))
                display.flip()
                p1health-=0.08

    
############ Naruto special ########################

# This is a steroid special naruto

# Naruto is turns into a demon fox which moves alot faster and hurts players if it touches them
narutos1p1special=False # Special status
narutos1p1temp=[] # Container for player_1 sprites
narutos1p1counter=0 # Counter that acts as a time limit
# Below are all sprites for the ninetail
ninetail=[[image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(1,8)],#Stand #
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(8,15)],#Walk
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(8,15)],#run
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(16,20)],#jump
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(21,23)],#hurtlight
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(23,27)],#hurthard
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(28,36)],#softattack
         [image.load("assets\\narutoS1\\ninetail"+str(i)+".png") for i in range(38,46)]]#hardattack

def narutos1p1():
    global narutos1p1temp,player_1,narutos1p1special,narutos1p1counter
    global p1x,p2health,p1sc,p1wc,p1jump,p1cc,p1hc,p1shc,p2fallstatus,p1chakra
    if key.get_pressed()[K_u] and narutos1p1special==False and p1chakra>=40: 
        p1chakra-=40 
        narutos1p1temp=player_1[:] #the temp variable holds all the player sprites before they are changed
        player_1=ninetail[:] #all of player 1 sprites are replaced with ninetail sprites
        narutos1p1special=True # special is on
    if narutos1p1special==True:
        narutos1p1counter+=1 #counter increases

        #the code below will move the player much faster when he press left or right
        if key.get_pressed()[K_d]:
            p1x+=15 
        if key.get_pressed()[K_a]:
            p1x-=15
        if p1rect.colliderect(p2rect): # if the player hits the opponent, the opponent falls down, and health decreases over time
            p2health-=0.8
            p2fallstatus=True
        if narutos1p1counter==150: #once it reaches limit 
            narutos1p1counter=0 #everything is reset
            player_1=narutos1p1temp[:] # the pl sprites are then turned back into the original sprites that were in it
            narutos1p1special=False
            p1sc,p1wc,p1jump,p1cc,p1hc,p1shc=0,0,0,0,0,0 #all counter are reset, so p1sprite position wont go out of range


#Same for player 2 special naruto attack  
narutos1p2special=False
narutos1p2temp=[]
narutos1p2counter=0
def narutos1p2():
    global narutos1p2temp,player_2,narutos1p2special,narutos1p2counter
    global p2x,p1health,p2sc,p2wc,p2jump,p2cc,p2hc,p2shc,p1fallstatus,p2chakra
    if key.get_pressed()[K_KP4] and narutos1p2special==False and p2chakra>=40:
        p2chakra-=40
        narutos1p2temp=player_2[:]
        player_2=ninetail[:]
        narutos1p2special=True
        p2sc,p2wc,p2jump,p2cc,p2hc,p2shc=0,0,0,0,0,0
    if narutos1p2special==True:
        narutos1p2counter+=1
        if key.get_pressed()[K_RIGHT]:
            p2x+=15
        if key.get_pressed()[K_LEFT]:
            p2x-=15
        if p2rect.colliderect(p1rect):
            p1health-=0.8
            p1fallstatus=True
        if narutos1p2counter==150:
            narutos1p2counter=0
            player_2=narutos1p2temp[:]
            narutos1p2special=False
            p2sc,p2wc,p2jump,p2cc,p2hc,p2shc=0,0,0,0,0,0


#the second special attack throws a rasengan ball at opponent

#all the sprites below
rassprite=[[image.load("assets\\narutoS2\\naruto"+str(i)+".png") for i in range(1,13)],
                [image.load("assets\\narutoS2\\naruto"+str(i)+".png") for i in range(14,19)],
                [image.load("assets\\narutoS2\\naruto"+str(i)+".png") for i in range(21,30)],
                [image.load("assets\\narutoS2\\naruto"+str(i)+".png") for i in range(44,47)]]

#the sprites are resized
for i in range(len(rassprite)):
    rassprite[i] = [
        transform.scale(x, (int(1.4 * x.get_width()), int(1.4 * x.get_height())))
        for x in rassprite[i]
    ]

#amost same variables as previous special 
narutos2p1special=False
narutos2p1counter=0
p1tempx,p1tempy,p1tempdirect=p1x,p1y,player_1_direction
p1rasx,p1rasy=0,0 #Position of rasengan ball
p1smallx,p1smally=0,0 #slope and/or direction in which way the ball should traval
     
def narutos2p1():
    global narutos2p1special,narutos2p1counter,p1sprite,p1tempx,p1tempy,p1tempdirect
    global p1x,p1y,player_1_direction,p1rasx,p1rasy,p1smallx,p1smally,p2health,p2fallstatus,p1chakra
    if narutos2p1special==False and key.get_pressed()[K_i] and p1chakra>40:
        p1chakra-=25
        narutos2p1counter=0
        narutos2p1special=True
        #temporory position and direction are saved
        p1tempx,p1tempy,p1tempdirect=p1x,p1y,player_1_direction
        p1rasx,p1rasy=p1x,p1y
    elif narutos2p1special==True:
        if loopCount % 2 == 0:
            narutos2p1counter+=1 #the counter increases every 2 real loops

        #The rasengan attack does certain animation at differnt times(counter)
        if narutos2p1counter<30:  #if the counter is less then 30, it does the animation to make the rasengan
            player_1_direction=p1tempdirect
            if player_1_direction=="Right":
                #sets the player sprite, player positions are locked
                p1x,p1y=p1tempx,p1tempy
                p1sprite=rassprite[0][narutos2p1counter%4+8]

                #once it is less then 7 sprites it plays the sprites normally
                if narutos2p1counter-8<7:
                    pic=rassprite[2][narutos2p1counter-8]
                    x=p1x+pic.get_width()-75
                    y=p1y-pic.get_height()+p1sprite.get_height()
                    screen.blit(pic,(x,y))
                else: #later after 7 loops it starts repeating the sprites
                    pic=rassprite[2][(narutos2p1counter-8)%2+7]
                    x=p1x+pic.get_width()-75
                    y=p1y-pic.get_height()+p1sprite.get_height()
                    screen.blit(pic,(x,y))
                #notes the slope using similar triangles, and the start position
                p1rasx,p1rasy=x,y
                p1smallx=(p2x-x)/hypot(p2x-x,p2y-y)
                p1smally=(p2y-y)/hypot(p2x-x,p2y-y)
                rasrect=Rect(x,y,pic.get_width(),pic.get_width())

                
            elif player_1_direction=="Left": #same thing as right but flipped
                p1x,p1y=p1tempx,p1tempy
                p1sprite=transform.flip(rassprite[0][narutos2p1counter%4+8],1,0)
                
                if narutos2p1counter-8<7:
                    pic=transform.flip(rassprite[2][narutos2p1counter-8],1,0)
                    x=p1x-pic.get_width()+20
                    y=p1y-pic.get_height()+p1sprite.get_height()
                    screen.blit(pic,(x,y))
                else:
                    pic=transform.flip(rassprite[2][(narutos2p1counter-8)%2+7],1,0)
                    x=p1x-pic.get_width()+20
                    y=p1y-pic.get_height()+p1sprite.get_height()
                    screen.blit(pic,(x,y))
                p1rasx,p1rasy=x,y
                p1smallx=(p2x-x)/hypot(p2x-x,p2y-y)
                p1smally=(p2y-y)/hypot(p2x-x,p2y-y)
                
        if narutos2p1counter>30: #after 30 loops, it starts moving the rasengan using the slope into the players direction
            p1rasx+=10*p1smallx #the 10x makes it move 10x faster
            p1rasy+=10*p1smally
            pic=rassprite[3][narutos2p1counter%4-1] #draws the giant rasengan pic
            screen.blit(pic,(p1rasx,p1rasy))
            rasrect=Rect(p1rasx,p1rasy,pic.get_width(),pic.get_width()) #rasrect is a temporery rect used to 
            #check if it collides of with other player , if it does the other player loses health and falls down
            if rasrect.colliderect(p2rect):
                p2health-=1.5
                p2fallstatus=True
            
        if narutos2p1counter>60: # once the counter hits 60 the special is turned off
            narutos2p1special=False

#same attack for player 2 with player 2 variables
narutos2p2special=False
narutos2p2counter=0
p2tempx,p2tempy,p2tempdirect=p2x,p2y,player_2_direction
p2rasx,p2rasy=0,0
p2smallx,p2smally=0,0
    
def narutos2p2():
    global narutos2p2special,narutos2p2counter,p2sprite,p2tempx,p2tempy,p2tempdirect
    global p2x,p2y,player_2_direction,p2rasx,p2rasy,p2smallx,p2smally,p1health,p1fallstatus,p2chakra
    if narutos2p2special==False and key.get_pressed()[K_KP5] and p2chakra>=25:
        p2chakra-=25
        narutos2p2counter=0
        narutos2p2special=True
        p2tempx,p2tempy,p2tempdirect=p2x,p2y,player_2_direction
        p2rasx,p2rasy=p2x,p2y
    elif narutos2p2special==True:
        if loopCount % 2 == 0:
            narutos2p2counter+=1
        if narutos2p2counter<30:
            player_2_direction=p2tempdirect
            if player_2_direction=="Right":
                p2x,p2y=p2tempx,p2tempy
                p2sprite=rassprite[0][narutos2p2counter%4+8]
                if narutos2p2counter-8<7:
                    pic=rassprite[2][narutos2p2counter-8]
                    x=p2x+pic.get_width()-75
                    y=p2y-pic.get_height()+p2sprite.get_height()
                    screen.blit(pic,(x,y))
                else:
                    pic=rassprite[2][(narutos2p2counter-8)%2+7]
                    x=p2x+pic.get_width()-75
                    y=p2y-pic.get_height()+p2sprite.get_height()
                    screen.blit(pic,(x,y))
                p2rasx,p2rasy=x,y
                p2smallx=(p1x-x)/hypot(p1x-x,p1y-y)
                p2smally=(p1y-y)/hypot(p1x-x,p1y-y)
                rasrect=Rect(x,y,pic.get_width(),pic.get_width()) 
            elif player_2_direction=="Left":
                p2x,p2y=p2tempx,p2tempy
                p2sprite=transform.flip(rassprite[0][narutos2p2counter%4+8],1,0)
                if narutos2p2counter-8<7:
                    pic=transform.flip(rassprite[2][narutos2p2counter-8],1,0)
                    x=p2x-pic.get_width()+20
                    y=p2y-pic.get_height()+p2sprite.get_height()
                    screen.blit(pic,(x,y))
                else:
                    pic=transform.flip(rassprite[2][(narutos2p2counter-8)%2+7],1,0)
                    x=p2x-pic.get_width()+20
                    y=p2y-pic.get_height()+p2sprite.get_height()
                    screen.blit(pic,(x,y))
                p2rasx,p2rasy=x,y
                p2smallx=(p1x-x)/hypot(p1x-x,p1y-y)
                p2smally=(p1y-y)/hypot(p1x-x,p1y-y)     
        if narutos2p2counter>30:
            p2rasx+=10*p2smallx
            p2rasy+=10*p2smally
            pic=rassprite[3][narutos2p2counter%4-1]
            screen.blit(pic,(p2rasx,p2rasy))
            rasrect=Rect(p2rasx,p2rasy,pic.get_width(),pic.get_width())
            if rasrect.colliderect(p1rect):
                p1health-=1.5
                p1fallstatus=True
            
        if narutos2p2counter>60:
            narutos2p2special=False

##################### Ichigo Special #############################
# Steroid special that puts Ichigo into Bankai form
bankai=[[image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(1,5)],#Stand
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(5,13)],#Walk
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(5,13)],#run
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(13,19)],#Jump
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(20,22)],#Hurt Light
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(29,32)],#Hurt Hard
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(49,88)],#Soft Attack
        [image.load("assets\\ichigoS1\\bankai"+str(i)+".png") for i in range(106,114)]]#Hard Attack
ichigos1p1special=False
ichigos1p1temp=[]
ichigos1p1counter=0
def ichigos1p1():
    global ichigos1p1temp,player_1,ichigos1p1special,ichigos1p1counter
    global p1x,p2health,p1sc,p1wc,p1jump,p1cc,p1hc,p1shc,p2fallstatus,p1chakra
    if key.get_pressed()[K_u] and ichigos1p1special==False and p1chakra>=30:
        p1chakra-=40
        ichigos1p1temp=player_1[:]
        player_1=bankai[:]
        ichigos1p1special=True
    if ichigos1p1special==True:
        ichigos1p1counter+=1
        if key.get_pressed()[K_d]:
            p1x+=15
        if key.get_pressed()[K_a]:
            p1x-=15
        if p1rect.colliderect(p2rect):
            p2health-=0.8
            p2fallstatus=True
        if ichigos1p1counter==150:
            ichigos1p1counter=0
            player_1=ichigos1p1temp[:]
            ichigos1p1special=False
            p1sc,p1wc,p1jump,p1cc,p1hc,p1shc=0,0,0,0,0,0

# Same for player 2
ichigos1p2special=False
ichigos1p2temp=[]
ichigos1p2counter=0
def ichigos1p2():
    global ichigos1p2temp,player_2,ichigos1p2special,ichigos1p2counter
    global p2x,p1health,p2sc,p2wc,p2jump,p2cc,p2hc,p2shc,p1fallstatus,p2chakra
    if key.get_pressed()[K_KP4] and ichigos1p2special==False and p2chakra>=30:
        p2chakra-=40
        ichigos1p2temp=player_2[:]
        player_2=bankai[:]
        ichigos1p2special=True
    if ichigos1p2special==True:
        ichigos1p2counter+=1
        if key.get_pressed()[K_RIGHT]:
            p2x+=15
        if key.get_pressed()[K_LEFT]:
            p2x-=15
        if p2rect.colliderect(p1rect):
            p1health-=0.8
            p1fallstatus=True
        if ichigos1p2counter==150:
            ichigos1p2counter=0
            player_2=ichigos1p2temp[:]
            ichigos1p2special=False
            p2sc,p2wc,p2jump,p2cc,p2hc,p2shc=0,0,0,0,0,0

            
ichispecial=[image.load("assets\\ichigoS2\\ichigo"+str(i)+".png") for i in range(1,24)] #contains all the sprites
#similar variables as functions above
ichigos2p1counter=0
ichigos2p1special=False
p1tempx,p1tempy=0,0
p1tempdirect=player_1_direction

# The special 2 for Ichigo sends out a sword blast wave from his Zanpakuto
def ichigos2p1():
    global ichigos2p1counter,ichigos2p1special,p1tempx,p1tempy
    global p1sprite,p1tempdirect,player_1_direction,p1x,p1y,p2fallstatus,p1chakra,p2health
    if key.get_pressed()[K_i] and ichigos2p1special==False and p1chakra>=25: #special activates
        p1chakra-=25
        ichigos2p1counter=0 #counter is reset
        p1tempdirect=player_1_direction #direction and positions are locked on
        ichigos2p1special=True 
        p1tempx,p1tempy=p1x,p1y
    if ichigos2p1special==True:
        if loopCount%2==0:
            ichigos2p1counter+=1
        if ichigos2p1counter<15: #once it is below 15 sprites, it only changes the players sprites
            player_1_direction=p1tempdirect
            p1sprite=direction(ichispecial[ichigos2p1counter],player_1_direction)
            p1x,p1y=p1tempx,p1tempy
        if ichigos2p1counter>15:          
            screen.blit(direction(ichispecial[ichigos2p1counter/2%2+15],p1tempdirect),(p1tempx,p1tempy-50)) #after that
            #it frees the player and the attack moves on its own
            if p1tempdirect=="Right":
                p1tempx+=20 #20 units in the players direction every loop
            else:
                p1tempx-=20

        #Below is a code that says that when the blast collides with other player, the special is false
        if Rect(p1tempx,p1tempy-50,ichispecial[ichigos2p1counter%2+15].get_width(),ichispecial[ichigos2p1counter%2+15].get_height()).colliderect(p2rect):
            p2fallstatus=True
            p2health-=25
            ichigos2p1special=False
        if p1tempx<-50 or p1tempx>850: #also turns status off once it goes out of map
            ichigos2p1special=False

# Same attack for player 2
ichigos2p2counter=0
ichigos2p2special=False
p2tempx,p2tempy=0,0
p2tempdirect=player_2_direction

def ichigos2p2():
    global ichigos2p2counter,ichigos2p2special,p2tempx,p2tempy,p2chakra
    global p2sprite,p2tempdirect,player_2_direction,p2x,p2y,p1fallstatus,p1health
    if key.get_pressed()[K_KP5] and ichigos2p2special==False and p2chakra>=25:
        p2chakra-=25
        ichigos2p2counter=0
        p2tempdirect=player_2_direction
        ichigos2p2special=True
        p2tempx,p2tempy=p2x,p2y
    if ichigos2p2special==True:
        if loopCount%2==0:
            ichigos2p2counter+=1
        if ichigos2p2counter<15:
            player_2_direction=p2tempdirect
            p2sprite=direction(ichispecial[ichigos2p2counter],player_2_direction)
            p2x,p2y=p2tempx,p2tempy
        if ichigos2p2counter>15:
            screen.blit(direction(ichispecial[ichigos2p2counter/2%2+15],p2tempdirect),(p2tempx,p2tempy-50))
            if p2tempdirect=="Right":
                p2tempx+=20
            else:
                p2tempx-=20
        if Rect(p2tempx,p2tempy-50,ichispecial[ichigos2p2counter%2+15].get_width(),ichispecial[ichigos2p2counter%2+15].get_height()).colliderect(p1rect):
            p1fallstatus=True
            ichigos2p2special=False
            p1health-=25
        if p2tempx<-50 or p2tempx>850:
            ichigos2p2special=False
            
################### LINK SPECIAL ###############################
############ Link Specials #############################
linkS1=[image.load("assets\\linkS1\\linkS1"+str(i)+".png") for i in range(1,19)]
linkArrows=[image.load("assets\\linkS1\\linkArrows"+str(i)+".png") for i in range(1,4)]
links1p1count,links1p1count2=0,0
links1p1special=False
links1p1x2=p1x-linkArrows[links1p1count2].get_width()-0
links1p1tempdirect="Left"
links1p1tempx2="Left"

def links1p1(): #Link's Arrow Attack
    global links1p1special,links1p1count,links1p1count2,p1sprite,sp,loopcount,p2rect,p2health,p1x,p1y,p1vely,p2x,links1p1x2,linkS1,linkArrows
    global links1p1x2,player_1_direction,links1p1tempdirect,p1tempx,p1tempy,links1p1tempx2,p1chakra
    if links1p1special!=True and key.get_pressed()[K_u] and p1chakra>=10: #U Key
        p1chakra-=10
        links1p1count=0
        links1p1count2=0
        p1tempx,p1tempy=p1x,p1y #Lock position
        links1p1special=True
        links1p1x2=0            #Changing x variable
        links1p1tempdirect=player_1_direction #Variable keeping the direction of player while he shoots arrow
        links1p1tempx2=player_1_direction     #Variable keeping the direction of arrow, letting player move
    elif links1p1special==True:
        
        
        if links1p1tempx2=="Left":
            p1sprite=direction(linkS1[links1p1count],"Left")
            if links1p1count<=12:                       #Wile shooting arrow
                player_1_direction=links1p1tempdirect             #Lock Direction
                p1x,p1y=p1tempx,p1tempy                 #Lock Position
                p1vely=0
            if links1p1count>12:                        #After arrow is shot
                screen.blit(direction(linkArrows[links1p1count2],"Left"),(p1tempx-linkArrows[links1p1count2].get_width()-links1p1x2,p1tempy-linkArrows[links1p1count2].get_height()+39))                
                attackrect=Rect(p1tempx-linkArrows[links1p1count2].get_width()-links1p1x2,p1tempy-linkArrows[links1p1count2].get_height()+39,
                                linkArrows[links1p1count2].get_width(),linkArrows[links1p1count2].get_height())
                links1p1x2+=15 #Only variable that changes, arrow is straight line
                
                if attackrect.colliderect(p2rect): #Damage if rect touches
                    p2health-=3
                    p2x-=1                          #Push character
            
        elif links1p1tempx2=="Right":               #Same for right
            p1sprite=direction(linkS1[links1p1count],"Right")
            if links1p1count<=12:
                player_1_direction=links1p1tempdirect
                p1x,p1y=p1tempx,p1tempy
                p1vely=0
            if links1p1count>12:
                screen.blit(direction(linkArrows[links1p1count2],"Right"),(p1tempx+linkArrows[links1p1count2].get_width()-links1p1x2,p1tempy-linkArrows[links1p1count2].get_height()+39))                
                attackrect=Rect(p1tempx-linkArrows[links1p1count2].get_width()-links1p1x2,p1tempy-linkArrows[links1p1count2].get_height()+39,
                                linkArrows[links1p1count2].get_width(),linkArrows[links1p1count2].get_height())
                
                links1p1x2-=15
                
                if attackrect.colliderect(p2rect):
                    p2health-=3
                    p2x+=1
                
        
    if loopCount % 3 == 0 and links1p1count!=13:            #Loopcounter for arrow
        links1p1count= (links1p1count + 1) % len(linkS1)
    if p1tempx-linkArrows[links1p1count2].get_width()-links1p1x2<0 or p1tempx-linkArrows[links1p1count2].get_width()-links1p1x2>800:
        links1p1special=False       #If arrow is out of field, special is done


links1p2count,links1p2count2=0,0 #same for player 2
links1p2special=False
links1p2x2=p2x-linkArrows[links1p2count2].get_width()-0
links1p2tempdirect="Left"
links1p2tempx2="Left"
        
def links1p2():
    global links1p2special,links1p2count,links1p2count2,p2sprite,sp,loopcount,p1rect,p1health,p2x,p2y,p2vely,p1x,links1p2x2,linkS1,linkArrows,links1p2x2
    global player_2_direction,links1p2tempdirect,p2tempx,p2tempy,links1p2tempx2,p2chakra
    if links1p2special!=True and key.get_pressed()[K_KP4]:
        p2chakra-=10
        links1p2count=0
        links1p2count2=0
        p2tempx,p2tempy=p2x,p2y
        links1p2special=True
        links1p2x2=0
        links1p2tempdirect=player_2_direction
        links1p2tempx2=player_2_direction
    elif links1p2special==True:
        if links1p2tempx2=="Left":
            p2sprite=direction(linkS1[links1p2count],"Left")
            if links1p2count<=12:
                player_2_direction=links1p2tempdirect
                p2x,p2y=p2tempx,p2tempy
                p2vely=0
            if links1p2count>12:
                screen.blit(direction(linkArrows[links1p2count2],"Left"),(p2tempx-linkArrows[links1p2count2].get_width()-links1p2x2,p2tempy-linkArrows[links1p2count2].get_height()+39))                
                attackrect=Rect(p2tempx-linkArrows[links1p2count2].get_width()-links1p2x2,p2tempy-linkArrows[links1p2count2].get_height()+39,
                                linkArrows[links1p2count2].get_width(),linkArrows[links1p2count2].get_height())
                links1p2x2+=15 
                if attackrect.colliderect(p1rect):
                    p1health-=3
                    p1x-=1
        elif links1p2tempx2=="Right":
            p2sprite=direction(linkS1[links1p2count],"Right")
            if links1p2count<=12:
                player_2_direction=links1p2tempdirect
                p2x,p2y=p2tempx,p2tempy
                p2vely=0
            if links1p2count>12:
                screen.blit(direction(linkArrows[links1p2count2],"Right"),(p2tempx+linkArrows[links1p2count2].get_width()-links1p2x2,p2tempy-linkArrows[links1p2count2].get_height()+39))                
                attackrect=Rect(p2tempx-linkArrows[links1p2count2].get_width()-links1p2x2,p2tempy-linkArrows[links1p2count2].get_height()+39,
                                linkArrows[links1p2count2].get_width(),linkArrows[links1p2count2].get_height())
                links1p2x2-=15
                if attackrect.colliderect(p1rect):
                    p1health-=3
                    p1x+=1
            
    if loopCount % 3 == 0 and links1p2count!=13:
        links1p2count= (links1p2count + 1) % len(linkS1)
    if linkArrows[links1p2count2].get_width()-links1p2x2>0:
        links1p2count2=0
    elif linkArrows[links1p2count2].get_width()-links1p2x2>100:
        links1p2count2=1
    elif linkArrows[links1p2count2].get_width()-links1p2x2>200:
        links1p2count2=2

    if p2tempx-linkArrows[links1p2count2].get_width()-links1p2x2<0 or p2tempx-linkArrows[links1p2count2].get_width()-links1p2x2>800:
        links1p2special=False


linkS2=[image.load("assets\\linkS2\\linkS2"+str(i)+".png") for i in range(1,21)]
linkBomb=[image.load("assets\\linkS2\\linkBomb"+str(i)+".png") for i in range(1,6)]
linkExplosion=[image.load("assets\\linkS2\\linkExplosion"+str(i)+".png") for i in range(1,6)]        
links2p1count,links2p1count2=0,0
links2p1special=False
links2p1x2=p2x-linkBomb[links2p1count2].get_width()-0
links2p1y2=p2y-linkBomb[links2p1count2].get_height()-0
links2p1tempdirect="Left"
linkp1Bcount=0
links2p1tempx2="Left"

def links2p1(): #Bomb Attack
    global links2p1special,links2p1count,links2p1count2,p1sprite,sp,loopcount,p2rect,p2health,p1x,p1y,p1vely,p2x,links2p1x2,linkS2,linkBomb
    global linkExpolsion,links2p1x2,player_1_direction,links2p1tempdirect,linkp1Bcount,p1tempx,p1tempy,links2p1tempx2,p1chakra
    if links2p1special!=True and key.get_pressed()[K_i] and p1chakra>=15: #I Key
        p1chakra-=15
        links2p1count=0
        links2p1count2=0
        linkp1Bcount=0
        p1tempx,p1tempy=p1x,p1y         #Lock player while throwing bomb
        links2p1special=True
        links2p1x2=0                    #x values of a straight line
        links2p1tempdirect=player_1_direction     #Keeps player direction while throwing bomb
        links2p1tempx2=player_1_direction         #Keeps track of bomb direction after throw to let player move
        
    elif links2p1special==True:
        
        if links2p1tempx2=="Left":
            p1sprite=direction(linkS2[links2p1count],"Left")
            if links2p1count<=13:       #Throwing bomb
                player_1_direction=links2p1tempdirect
                p1x,p1y=p1tempx,p1tempy
                p1vely=0
            if links2p1count>13:        #Bomb Thrown
                pic=linkBomb[0]
                bx=p1tempx-linkBomb[0].get_width()-links2p1x2 #x values of line used for parobola
                if links2p1x2>=370:                             #if x hits the next zero of the parobola
                    if loopCount % 3 == 0:
                        linkp1Bcount= (linkp1Bcount + 1)
                    if linkp1Bcount==4:
                        links2p1special=False                   #Start explosion sequence    
                    pic=linkExplosion[linkp1Bcount]
                    
                elif Rect(bx,0.001*(bx-p1tempx)*(bx-p1tempx+300)+p1tempy,linkBomb[0].get_width(),linkBomb[0].get_width()).colliderect(p2rect):
                    if loopCount % 3 == 0:                      #if the bomb hit the opponent
                        linkp1Bcount= (linkp1Bcount + 1)
                    if linkp1Bcount==4:
                        links2p1special=False                   #bomb explodes on opponent
                    p2health-=4
    
                    pic=linkExplosion[linkp1Bcount]
                    
                elif p1tempx-linkBomb[0].get_width()-links2p1x2<0 or p1tempx-linkBomb[0].get_width()-links2p1x2>800:
                    if loopCount % 3 == 0:                      #if bomb is out of field, it misses
                        linkp1Bcount= (linkp1Bcount+ 1)
                    if linkp1Bcount==4:
                        links2p1special=False
                    pic=linkExplosion[linkp1Bcount]
                        
                        
                else:                                           #else, keep travelling in parabola
                    links2p1x2+=10                              
                by=0.001*(bx-p1tempx)*(bx-p1tempx+300)+p1tempy  #equation of our parabola          
                screen.blit(pic,(bx,by))
                if linkBomb[4]==True:
                    links2p1special=False
               
          
        if links2p1tempx2=="Right":                             #Same for right
            p1sprite=direction(linkS2[links2p1count],"Right")
            if links2p1count<=13:
                player_1_direction=links2p1tempdirect
                p1x,p1y=p1tempx,p1tempy
                p1vely=0
            if links2p1count2>13:
                pic=linkBomb[0]
                bx=p1tempx+p1sprite.get_width()-linkBomb[0].get_width()+links2p1x2
                if links2p1x2>=370:
                    if loopCount % 3 == 0:
                        linkp1Bcount= (linkp1Bcount + 1)
                    if linkp1Bcount==4:
                        links2p1special=False
                    pic=linkExplosion[linkp1Bcount]
                elif Rect(bx,0.001*(bx-p1tempx)*(bx-p1x-300)+p1tempy,linkBomb[0].get_width(),linkBomb[0].get_width()).colliderect(p2rect):
                    if loopCount % 3 == 0:
                        linkp1Bcount= (linkp1Bcount + 1)
                    if linkp1Bcount==4:
                        links2p1special=False
                    p2health-=4
    
                    pic=linkExplosion[linkp1Bcount]
                elif p1tempx-linkBomb[0].get_width()+links2p1x2<0 or p1tempx-linkBomb[0].get_width()+links2p1x2>800:
                    if loopCount % 3 == 0:
                        linkp1Bcount= (linkp1Bcount + 1)
                    if linkp1Bcount==4:
                        links2p1special=False
                    pic=linkExplosion[linkp1Bcount]
                        
                        
                else:
                    links2p1x2+=10
                by=0.001*(bx-p1tempx)*(bx-p1tempx-300)+p1tempy               
                screen.blit(pic,(bx,by))
                if linkBomb[4]==True:
                    links2p1special=False
            
    if loopCount % 3 == 0 and links2p1count!=19:
        links2p1count= (links2p1count + 1)
    if loopCount % 3 == 0 and links2p1count2!=19:
        links2p1count2= (links2p1count2 + 1)
        
    if p1tempx-linkBomb[0].get_width()-links2p1x2<0:
        pic=linkExplosion[linkp1Bcount%(len(linkExplosion))]                    
        if linkp1Bcount%len(linkExplosion)==4:
            links2p1special=False

linkS2=[image.load("assets\\linkS2\\linkS2"+str(i)+".png") for i in range(1,21)]
linkBomb=[image.load("assets\\linkS2\\linkBomb"+str(i)+".png") for i in range(1,6)]
linkExplosion=[image.load("assets\\linkS2\\linkExplosion"+str(i)+".png") for i in range(1,6)]        
links2p2count,links2p2count2=0,0
links2p2special=False
links2p2x2=p2x-linkBomb[links2p2count2].get_width()-0
links2p2y2=p2y-linkBomb[links2p2count2].get_height()-0
links2p2tempdirect="Left"
linkp2Bcount=0
links2p2tempx2="Left"

# Same for player 2

def links2p2():
    global links2p2special,links2p2count,links2p2count2,p2sprite,sp,loopcount,p1rect,p1health,p2x,p2y,p2vely,p1x,links2p2x2,linkS2,linkBomb
    global linkExpolsion,links2p2x2,player_2_direction,links2p2tempdirect,linkp2Bcount,p2tempx,p2tempy,links2p2tempx2,p2chakra
    if links2p2special!=True and key.get_pressed()[K_KP5]:
        p2chakra-=15
        
        links2p2count=0
        links2p2count2=0
        linkp2Bcount=0
        p2tempx,p2tempy=p2x,p2y
        links2p2special=True
        links2p2x2=0
        links2p2tempdirect=player_2_direction
        links2p2tempx2=player_2_direction
        
    elif links2p2special==True:
        
        
        if links2p2tempx2=="Left":
            p2sprite=direction(linkS2[links2p2count],"Left")
            if links2p2count<=13:
                player_2_direction=links2p2tempdirect
                p2x,p2y=p2tempx,p2tempy
                p2vely=0
            if links2p2count>13:
                pic=linkBomb[0]
                bx=p2tempx-linkBomb[0].get_width()-links2p2x2
                if links2p2x2>=370:
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
    
                    pic=linkExplosion[linkp2Bcount]
                elif Rect(bx,0.001*(bx-p2x)*(bx-p2x+300)+p2tempy,linkBomb[0].get_width(),linkBomb[0].get_width()).colliderect(p1rect):
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
                    p1health-=4
    
                    pic=linkExplosion[linkp2Bcount]
                elif p2tempx-linkBomb[0].get_width()-links2p2x2<0 or p2tempx-linkBomb[0].get_width()-links2p2x2>800:
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
                    pic=linkExplosion[linkp2Bcount]
                        
                        
                else:
                    links2p2x2+=10
                by=0.001*(bx-p2tempx)*(bx-p2tempx+300)+p2tempy               
                screen.blit(pic,(bx,by))
                if linkBomb[4]==True:
                    links2p2special=False
               
          
        if links2p2tempx2=="Right":
            if links2p2count<=13:
                player_2_direction=links2p2tempdirect
                p2x,p2y=p2tempx,p2tempy
                p2vely=0
            p2sprite=direction(linkS2[links2p2count],"Right")
            if links2p2count2>13:
                pic=linkBomb[0]
                bx=p2tempx+p2sprite.get_width()-linkBomb[0].get_width()+links2p2x2
                if links2p2x2>=370:
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
                    pic=linkExplosion[linkp2Bcount]
                elif Rect(bx,0.001*(bx-p2tempx)*(bx-p2tempx-300)+p2tempy,linkBomb[0].get_width(),linkBomb[0].get_width()).colliderect(p1rect):
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
                    p1health-=4
    
                    pic=linkExplosion[linkp2Bcount]
                elif p2tempx-linkBomb[0].get_width()+links2p2x2<0 or p2tempx-linkBomb[0].get_width()+links2p2x2>800:
                    if loopCount % 3 == 0:
                        linkp2Bcount= (linkp2Bcount + 1)
                    if linkp2Bcount==4:
                        links2p2special=False
                    pic=linkExplosion[linkp2Bcount]
                        
                        
                else:
                    links2p2x2+=10
                by=0.001*(bx-p2tempx)*(bx-p2x-300)+p2tempy                
                screen.blit(pic,(bx,by))
                if linkBomb[4]==True:
                    links2p2special=False
            
    if loopCount % 3 == 0 and links2p2count!=19:
        links2p2count= (links2p2count + 1)
    if loopCount % 3 == 0 and links2p2count2!=19:
        links2p2count2= (links2p2count2 + 1)
        
    if p2tempx-linkBomb[0].get_width()-links2p2x2<0:
        pic=linkExplosion[linkp2Bcount%(len(linkExplosion))]                    
        if linkp2Bcount%len(linkExplosion)==4:
            links2p2special=False
########################################### Gaara Specials ########################################

gaaraS1=[image.load("assets\\gaaraS1\\gaaraS1"+str(i)+".png") for i in range(1,22)]
gaaraCoffin=[image.load("assets\\gaaraS1\\gaaraCoffin"+str(i)+".png") for i in range(1,18)]

gaaras1p1count=0
gaaras1p1special=False
gaaras1p1tempdirect="Left"
p1tempx,p1tempy

def gaaras1p1(): # Gaara's Sand Coffin Attack
    global gaaras1p1special,gaaras1p1count,p1sprite,p2health,player_1_direction,p2sprite,p1chakra
    global p1x,p1y,p1tempx,p1tempy,gaaras1p1tempdirect,p1vely
    if gaaras1p1special!=True and key.get_pressed()[K_u] and p1chakra>30:
        p1chakra-=30
        gaaras1p1count=0
        p1tempx,p1tempy=p1x,p1y             #Locks Position of player
        gaaras1p1special=True
        gaaras1p1tempdirect=player_1_direction        #Locks Direction
    elif gaaras1p1special==True:
        player_1_direction=gaaras1p1tempdirect
        p1x,p1y=p1tempx,p1tempy
        p1vely=0
        p1sprite=direction(gaaraS1[gaaras1p1count],player_1_direction)
        if gaaras1p1count>4:                #Blit coffin where opponent is
            screen.blit(gaaraCoffin[gaaras1p1count-4],(p2x-30,p2y-gaaraCoffin[gaaras1p1count-4].get_height()+p1sprite.get_height()))                
            if gaaras1p1count>12:           #Coffin crushes opponent and takes damage 
                p2sprite=gaaraCoffin[0]
            p2health-=0.1
    if loopCount % 4 == 0:
        gaaras1p1count= (gaaras1p1count + 1) % len(gaaraS1)
    if gaaras1p1count==17:
        gaaras1p1special=False              #Finish when sequence is over

gaaras1p2count=0
gaaras1p2special=False
gaaras1p2tempdirect="Left"
p2tempx,p2tempy

def gaaras1p2(): # Same for Player 2
    global gaaras1p2special,gaaras1p2count,p2sprite,p1health,player_2_direction,p1sprite
    global p2x,p2y,p2tempx,p2tempy,gaaras1p2tempdirect,p2vely
    if gaaras1p2special!=True and key.get_pressed()[K_KP4]:
        gaaras1p2count=0
        p2tempx,p2tempy=p2x,p2y
        gaaras1p2special=True
        gaaras1p2tempdirect=player_2_direction
    elif gaaras1p2special==True:
        player_2_direction=gaaras1p2tempdirect
        p2x,p2y=p2tempx,p2tempy
        p2vely=0
        p2sprite=direction(gaaraS1[gaaras1p2count],player_2_direction)
        if gaaras1p2count>4:
            screen.blit(gaaraCoffin[gaaras1p2count-4],(p1x-30,p1y-gaaraCoffin[gaaras1p2count-4].get_height()+p1sprite.get_height()))                
            if gaaras1p2count>12:
                p1sprite=gaaraCoffin[0]
            p1health-=0.1 
    if loopCount % 4 == 0:
        gaaras1p2count= (gaaras1p2count + 1) % len(gaaraS1)
    if gaaras1p2count==17:
        gaaras1p2special=False

        
gsprite=[image.load("assets\\gaaraS2\\gaara"+str(i)+".png")for i in range(1,4)]
gball=[image.load("assets\\gaaraS2\\gaaraball"+str(i)+".png")for i in range(1,7)]
p1gspecial=False

p1gcount=0
p1bx,p1by=650,150
def gaaras2p1(): # Gaara's Ichibi Transformation Chakra Blast of DOOM!
    global p1gspecial, p1bx,p1by,p1gcount,p2health,p2fallstatus,p2x,p1chakra
    if p1gspecial==False and key.get_pressed()[K_i] and p1chakra>50:
        p1chakra-=50
        p1gcount=0
        p1gspecial=True
        p1bx,p1by=100,400
    if p1gspecial==True:
        if loopCount %2==0:
            p1gcount+=1
        if p1gcount<10: #Show cinematics
            screen.blit(transform.scale(gsprite[0],(900,300)),(0-p1gcount*10,200))
        elif p1gcount>10 and p1gcount<15:
            screen.blit(transform.scale(gsprite[1],(400,300)),(100,100))
        elif p1gcount>20 and p1gcount<30:
            screen.blit(transform.scale(gsprite[2],(400,800)),(-50+p1gcount,100))
            if Rect(-50+p1gcount,100,400,800).colliderect(p1rect): #If the monster touches you, you get hurt
                p2health-=.2
                p2x+=25
                p2fallstatus=True
        elif p1gcount>29 and p1gcount<32:                   #Equation for following the opponent 
            screen.blit(transform.scale(gsprite[2],(400,800)),(-10,100))
            screen.blit(gball[p1gcount%3],(p1bx,p1by))
            p1bx+=20*(p2x-p1bx)/hypot(p2x-p1bx,p2y-p1by)    #distance formula to gradually get closer to target
            p1by+=20*(p2y-p1by)/hypot(p2x-p1bx,p2y-p1by)
        elif p1gcount>31:
            screen.blit(transform.scale(gsprite[2],(400,800)),(-10,100))    
            screen.blit(gball[p1gcount%3+3],(p1bx,p1by))
            p1bx+=20*(p2x-p1bx)/hypot(p2x-p1bx,p2y-30-p1by)
            p1by+=20*(p2y-30-p1by)/hypot(p2x-p1bx,p2y-30-p1by)
            
            if Rect(p1bx,p1by,gball[p1gcount%3+3].get_width(),gball[p1gcount%3+3].get_height()).colliderect(p2rect):
                p1gspecial=False                        #if the ball touches you, you get hurt more
                p2health-=25
                p2x+=25
                p2fallstatus=True
        elif p1gcount==65:
            p1gspecial=True

# Same for player 2
p2gspecial=False
p2gcount=0
p2bx,p2by=650,150
def gaaras2p2():
    global p2gspecial, p2bx,p2by,p2gcount,p1health,p1fallstatus,p1x,p2chakra
    if p2gspecial==False and key.get_pressed()[K_KP5] and p2chakra>30:
        p2chakra-=30
        p2gcount=0
        p2gspecial=True
        p2bx,p2by=100,400
    if p2gspecial==True:
        if loopCount %2==0:
            p2gcount+=1
        if p2gcount<10:
            screen.blit(transform.scale(gsprite[0],(900,300)),(0-p2gcount*10,200))
        elif p2gcount>10 and p2gcount<15:
            screen.blit(transform.scale(gsprite[1],(500,300)),(100,100))
        elif p2gcount>20 and p2gcount<30:
            screen.blit(transform.scale(gsprite[2],(400,800)),(-50+p2gcount,100))
            if Rect(-50+p2gcount,100,400,800).colliderect(p1rect):
                p1health-=.2
                p1x+=10
                p1fallstatus=True
        elif p2gcount>29 and p2gcount<32:
            screen.blit(transform.scale(gsprite[2],(400,800)),(-10,100))
            screen.blit(gball[p2gcount%3],(p2bx,p2by))
            p2bx+=20*(p2x-p2bx)/hypot(p1x-p2bx,p1y-p2by)
            p2by+=20*(p2y-p2by)/hypot(p1x-p2bx,p1y-p2by)
        elif p2gcount>31:
            screen.blit(transform.scale(gsprite[2],(400,800)),(-10,100))
            screen.blit(gball[p2gcount%3+3],(p2bx,p2by))
            p2bx+=20*(p1x-p2bx)/hypot(p1x-p2bx,p1y-30-p2by)
            p2by+=20*(p1y-30-p2by)/hypot(p1x-p2bx,p1y-30-p2by)
            if Rect(p2bx,p2by,gball[p1gcount%3+3].get_width(),gball[p1gcount%3+3].get_height()).colliderect(p1rect):
                p2gspecial=False
                p1health-=20
                p1fallstatus=True
                p1x+=10
        elif p2gcount==65:
            p2gspecial=True

           
while running:
    for evnt in event.get():          
        if evnt.type == QUIT:
            running = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
    if start==False:
        eval(page)()
        display.flip()
    else:
        draw_environment()
        screen.blit(p1sprite,(p1x,p1y-p1sprite.get_height()+player_1[0][0].get_height()))
        screen.blit(p2sprite,(p2x,p2y-p2sprite.get_height()+player_2[0][0].get_height()))
        
        keys = list(key.get_pressed())
        
    ########################## Player 1 #####################################
        if p1softhurt==False and p1fallstatus==False:   # If character is not hurt or fallen, character can operate
            if key.get_pressed()[K_d]:               # Right Key A Key
                if player_1_obj.is_grounded:      # On the ground, character walk
                    p1x+=10
                    player_1_direction="Right"
                    p1sprite=player_1[1][p1wc]
                else:
                    p1x+=10             #In air, character float
                    player_1_direction="Right"
                    
                
            elif key.get_pressed()[K_a]:              #Left Key D Key
                if player_1_obj.is_grounded:
                    p1x-=10
                    player_1_direction="Left"
                    p1sprite=transform.flip(player_1[1][p1wc],1,0)
                else:
                    p1x-=10
                    player_1_direction="Left"
                                
            else:
                if player_1_obj.is_grounded and not key.get_pressed()[K_UP]:        # Standing if character does nothing
                    p1sprite=direction(player_1[0][p1sc],player_1_direction)
                    
            if key.get_pressed()[K_l] and player_1_obj.is_grounded:# L Key Blocking
                p1sprite=direction(player_1[2][0],player_1_direction)
                p1block=True
                    
            jumpanimation()
            if key.get_pressed()[K_w]:#Up Key
                if player_1_obj.is_grounded:
                    p1sprite=direction(player_1[3][p1jump],player_1_direction)
                    p1djump=1
                    p1vely=15           #Set velocity to 15
                    ground=False        #Character off the ground

                if p1vely<0 and p1djump==1:     #Double Jump
                    p1vely=10
                    p1djump=2
                    p1sprite=direction(player_1[3][p1jump],player_1_direction)

            if not player_1_obj.is_grounded:
                p1sprite=direction(player_1[3][p1jump],player_1_direction) #Float animation
                
                
            if key.get_pressed()[K_j]and key.get_pressed()[K_d]==False and key.get_pressed()[K_a]==False and key.get_pressed()[K_w]==False:  #Soft J key Can not move while attacking
                
                p1sprite=direction(player_1[6][p1cc],player_1_direction)
                if p1rect.colliderect(p2rect):
                    if p2block==False and p2protect==False: #If not blocking or invincible, opponent gets hurt
                        p2health-=0.2                
                        p2softhurt=True     #Opponent can not retaliate             
                    if player_1_direction=="Right":
                        p2sprite=player_2[4][p2shc]
                        p2x+=1
                    else:
                        p2sprite=direction(player_2[4][p2shc],"Right")
                        p2x-=1
                else:p2softhurt=False
            else:p2softhurt=False
            
            if key.get_pressed()[K_k]and key.get_pressed()[K_d]==False and key.get_pressed()[K_a]==False and key.get_pressed()[K_w]==False:#Hard K Key Can not move while attacking
                p1sprite=direction(player_1[7][p1hc],player_1_direction)
                if p1rect.colliderect(p2rect):
                    if p2block==False and p2protect==False:#If not blocking or invincible, opponent gets hurt
                        p2health-=.5                
                        p2fallstatus=True   #Opponent falls and is invincible for a few seconds
                    p1chakra+=1             #Gain chakra for hard attacking
                    if player_1_direction=="Right":
                        p2x+=1
                    else:
                        p2x-=1
                        
            if key.get_pressed()[K_s] and key.get_pressed()[K_a]==False and key.get_pressed()[K_d]==False and player_1_obj.is_grounded: # Chakra Charge S Key
                p1chakra+=.5 
                screen.blit(aura[ac],(p1x-25,p1y-30))
            
        
        
        
    ######################### Player 2 ######################################
        if p2softhurt==False and p2fallstatus==False: #same for player 2
            if key.get_pressed()[K_RIGHT]:
                if is_player_2_grounded==True:
                    p2x+=10
                    player_2_direction="Right"
                    p2sprite=player_2[1][p2wc]
                else:
                    p2x+=10
                    player_2_direction="Right"
                    
                
            elif key.get_pressed()[K_LEFT]:
                if is_player_2_grounded==True:
                    p2x-=10
                    player_2_direction="Left"
                    p2sprite=transform.flip(player_2[1][p2wc],1,0)
                else:
                    p2x-=10
                    player_2_direction="Left"
                                
            else:
                if is_player_2_grounded==True and not key.get_pressed()[K_UP]:
                    p2sprite=direction(player_2[0][p2sc],player_2_direction)
                    
            if key.get_pressed()[K_KP3] and is_player_2_grounded==True:
                p2sprite=direction(player_2[2][0],player_2_direction)
                p2block=True
                    
            if key.get_pressed()[K_UP]:
                if is_player_2_grounded==True:
                    p2djump=1
                    p2vely=15
                    is_player_2_grounded=False

                if p2vely<0 and p2djump==1:
                    p2vely=10
                    p2djump=2
                    
            
            if key.get_pressed()[K_DOWN] and key.get_pressed()[K_LEFT]==False and key.get_pressed()[K_RIGHT]==False and is_player_2_grounded==True:
                p2chakra+=.5
                screen.blit(aura[ac],(p2x-25,p2y-30))
            
            
            if is_player_2_grounded==False:
                p2sprite=direction(player_2[3][p2jump],player_2_direction)
                    
            if key.get_pressed()[K_KP1]and key.get_pressed()[K_RIGHT]==False and key.get_pressed()[K_LEFT]==False and key.get_pressed()[K_UP]==False:                                                       
                p2sprite=direction(player_2[6][p2cc],player_2_direction)
                if p2rect.colliderect(p1rect):
                    if p1block==False and p2protect==False:
                        p1health-=0.2
                        p1softhurt=True
                    if player_2_direction=="Right":
                        p1sprite=player_1[4][p1shc]
                        p1x+=1
                    else:
                        p1sprite=direction(player_1[4][p1shc],"Right")
                        p1x-=1
                else:p1softhurt=False
            else:p1softhurt=False
            
            if key.get_pressed()[K_KP2]and key.get_pressed()[K_RIGHT]==False and key.get_pressed()[K_LEFT]==False and key.get_pressed()[K_UP]==False:
                p2sprite=direction(player_2[7][p2hc],player_2_direction)
                if p2rect.colliderect(p1rect):
                    if p1block==False and p2protect==False:
                        p1health-=.5               
                        p1fallstatus=True
                    p2chakra+=1
                    if player_2_direction=="Right":
                        p1x+=4
                    else:
                        p1x-=4
            
        ########################## Execute all functions ###################################
        platform(platforms, player_1_obj)
        p1rect=Rect(p1x,p1y,p1sprite.get_width(),p1sprite.get_height())
        p2rect=Rect(p2x,p2y,p2sprite.get_width(),p2sprite.get_height())
        
        if p1softhurt==True:
            p1sprite=transform.flip(direction(player_1[4][p1shc],player_2_direction),1,0)
        if p2softhurt==True:
            p2sprite=transform.flip(direction(player_2[4][p2shc],player_1_direction),1,0)
        groundcheck(player_1_obj)
        
        loopcounter()
        mapsides()
        falls()
        invincibility()
        health()
        special()
        foodsss()
        myClock.tick(60)
        display.flip()
quit()


