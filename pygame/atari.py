#Importar librerias
import sys
import pygame
import time
import os
pygame.init()
pygame.mixer.init()



####################################################################################
#Classes
####################################################################################
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_ball = pygame.image.load('images/bolita.png')
        self.rect = self.img_ball.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        #[0,1]
        self.speed = [5, 2] # []
    
    def pibot(self):
        #Validate Y !¡
        if self.rect.bottom >= HEIGHT or self.rect.top <=0:
            self.speed[1] = -self.speed[1]
        #Validate X <- X ->
        elif self.rect.right >= WIDTH or self.rect.left <=0:
            self.speed[0] = -self.speed[0]

        self.rect.move_ip(self.speed) 

####################################################################################
class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_bar = pygame.image.load('images/paleta.png')
        self.rect = self.img_bar.get_rect()
        self.rect.midbottom = (WIDTH / 2, HEIGHT - 10)
        self.speed = [0, 0]

    def slide(self, listener):
        if listener.key == pygame.K_LEFT and self.rect.left > 0 :
            self.speed = [-5, 0]
        elif listener.key == pygame.K_RIGHT and self.rect.right < WIDTH :
            self.speed = [5, 0]
        else :
            self.speed = [0, 0]     

        self.rect.move_ip(self.speed)
####################################################################################
class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ladrillo.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Wall(pygame.sprite.Group):
    def __init__(self, totalBricks):
        pygame.sprite.Group.__init__(self)
        posX = 0
        posY = 10

        for i in range(totalBricks):
            brick = Brick(( posX, posY ))
            self.add(brick)

            posX += brick.rect.width
            if posX >= WIDTH :
                posX = 0
                posY += brick.rect.height


def game_over():
    msg = "Perdiste. Vuelve a intentarlo"
    text_color = (63, 74, 106)
    text_style = pygame.font.SysFont('Arial',40) #(Tipo de letra, Tamaño)
    txt_screen = text_style.render(msg,True,text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.center = [WIDTH/2,HEIGHT/2]
    screen.blit(txt_screen,txt_screen_rect)
    pygame.display.flip()
    print("perdiste")
    time.sleep(1)
    #sys.exit()
    
def set_score():
    text_color = (255, 255, 255)
    text_style = pygame.font.SysFont('Arial',40) #(Tipo de letra, Tamaño)
    txt_screen = text_style.render(str(score).zfill(3),True,text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.topleft = [1,400]
    screen.blit(txt_screen,txt_screen_rect)

def set_lives():
    label = "Vidas: "
    text_color = (255, 255, 255)
    text_style = pygame.font.SysFont('Arial',20) #(Tipo de letra, Tamaño)
    text = label + str(player_lives).zfill(1)
    txt_screen = text_style.render(text,True,text_color)
    #txt_screen = text_style.render(label + str(player_lives).zfill(1),True,text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.topleft = [500,400]
    screen.blit(txt_screen,txt_screen_rect)




    
####################################################################################


#General settings
WIDTH = 640
HEIGHT = 480

#Configure full-screen
#WIDTH = ?
#HEIGHT = ?

BG_COLOR = (4, 152, 231) # (Red, Green, Blue)

screen = pygame.display.set_mode( (WIDTH,  HEIGHT) )
pygame.display.set_caption('Atari')
icon = pygame.image.load('images/main_icon.png')
pygame.display.set_icon(icon)

game_clock = pygame.time.Clock()
pygame.key.set_repeat(20)

print("Menu nivel de juego")
print("1. Nivel Normal")
print("2. Nivel Intermedio")
print("3. Nivel Avanzado")
print("4. Salir")

status = True
while status:
    opt = int (input("Seleccione el nivel: "))
    if opt >= 1 and opt <= 4:
        status = False 


if opt==1:
    ladrillos=20
elif opt==2:
    ladrillos=100
elif opt==3:
    ladrillos=200
elif opt==4:
    print("Has salido del juego")
    os.system("pause")
    sys.exit()
else:
    print("Opcion invalida")
    os.system("pause")
    sys.exit()
              

ball = Ball()
player = Bar()

wall = Wall(ladrillos)
score = 0
player_lives = 2

#Loop (Revisión cíclica de los eventos) => Listener
while True:
    game_clock.tick(60)
    for event in pygame.event.get():
        #Verificar si se presiono el botón X de la ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Verificar si el jugador presionó tecla del teclado
        elif event.type == pygame.KEYDOWN :
            player.slide(event)


    #Call pibot
    ball.pibot()     

    #colisiones entre bola y barra  ( destruir ladrillos )
    elements=pygame.sprite.spritecollide(ball,wall, False,collided =None)
    if elements : #mientras hay ladrillos por chocar
        brick=elements[0]
        centX =ball.rect.centerx

        if centX < brick.rect.left or centX>brick.rect.right:
            ball.speed[0] =-ball.speed[0]
        else :
            ball.speed[0] =-ball.speed[1]    
        wall.remove(brick)  
        sound = pygame.mixer.Sound("sonido/meta.wav")
        sound.play()


        score = score+1 #score+=1  

    #llamar la funcion game over caundo la bola toque el piso

    #if ball.rect.bottom >= HEIGHT:
        #game_over()

    #Restar vida  
    if ball.rect.bottom >= HEIGHT:
        player_lives = player_lives-1 #player_lives-=1  

    if player_lives == 0:
        sound = pygame.mixer.Sound("sonido/perdiste.wav")
        sound.play()
        os.system("pause")
        game_over()
        
        
        
        

    #cambio de trayectoria de la bola
    if pygame.sprite.collide_rect(ball,player):#el jugador es la barra
        ball.speed[1] = -ball.speed[1]  
        sound = pygame.mixer.Sound("sonido/piso.wav")
        sound.play()  
   
    #Set background color
    screen.fill(BG_COLOR)   
    set_score() 
   

    set_lives()    
    #Draw de la ball
    screen.blit(ball.img_ball, ball.rect)
    #Draw de la bar
    screen.blit(player.img_bar, player.rect)
    #Dibujar muro
    wall.draw(screen)       
    #Refresh de elementos en screen
    pygame.display.flip()