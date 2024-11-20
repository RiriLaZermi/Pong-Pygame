import pygame,sys
import random

SCREEN_WIDTH=2000
SCREEN_HEIGHT=1000

COLOR_BAR=(200,200,200)
COLOR_BALL=(255,255,255)
COLOR_BG=(20,20,20)

class Circle:
    center=[0,0]
    radius=0
    def __init__(self, center, radius):
         self.center=center
         self.radius=radius
         
        


    
def pong_update(screen,bar1,bar2,ball,ball_xspeed,ball_yspeed):

    ball.center[0] += ball_xspeed
    ball.center[1] += ball_yspeed
    pixel_tolerance= abs(ball_xspeed)
    # rebonds sur le plafond et le bas
    if abs(ball.center[1]+ball.radius - SCREEN_HEIGHT)<pixel_tolerance and ball_yspeed>0 or abs(ball.center[1]-ball.radius)<pixel_tolerance and ball_yspeed<0:
         ball_yspeed *=-1


    #rebond sur les joueurs
    if  abs(ball.center[0]-ball.radius -bar1.right)<pixel_tolerance and ball.center[1]>bar1.top and ball.center[1]<bar1.bottom and ball_xspeed<0:
         if abs(ball_xspeed)<30:
            ball_xspeed *= -1.3
         else:
            ball_xspeed *= -1
        
         
    elif abs(ball.center[0]+ball.radius -bar2.left)<pixel_tolerance and ball.center[1]>bar2.top and ball.center[1]<bar2.bottom and ball_xspeed>0:
        if abs(ball_xspeed)<30:
            ball_xspeed *= -1.3
        else:
            ball_xspeed *= -1
    
        

         
    pygame.draw.rect(screen, COLOR_BAR, bar1)
    pygame.draw.rect(screen, COLOR_BAR, bar2)
    pygame.draw.circle(screen,COLOR_BALL,ball.center,ball.radius)

    

    return ball_xspeed, ball_yspeed


def bar1_update(bar_speed,bar1,up=0,down=0):

    if up:
        bar1.top -= bar_speed
    if down:
        bar1.bottom += bar_speed

    if bar1.top <= 0:
         bar1.top=0
    elif bar1.bottom >= SCREEN_HEIGHT:
         bar1.bottom = SCREEN_HEIGHT
    
  
    

def bar2_update(bar_speed,bar2,up=0,down=0):
    if bar2.top >= 0 and bar2.bottom <= SCREEN_HEIGHT:
        if up:
            bar2.top -= bar_speed
        if down:
            bar2.bottom += bar_speed

        if bar2.top <= 0:
            bar2.top=0
        elif bar2.bottom >= SCREEN_HEIGHT:
            bar2.bottom = SCREEN_HEIGHT


def pong_init(screen,ballRadius):
    barWidth =20
    barLenght=100

    r=random.randint(0,1)
    r= -1 * r + 1 * (1-r)

    y_speed=r*random.randint(5,10)
    y_hight=random.randint(-int(SCREEN_HEIGHT/3),int(SCREEN_HEIGHT/3))
    

    rect1=pygame.Rect(0,SCREEN_HEIGHT/2 - barLenght/2,barWidth,barLenght)
    rect2=pygame.Rect(SCREEN_WIDTH-barWidth,SCREEN_HEIGHT/2 - barLenght/2,barWidth,barLenght)
    ball = Circle( [SCREEN_WIDTH/2,SCREEN_HEIGHT/2 +y_hight],ballRadius)

    return rect1,rect2,ball, r, y_speed
    
def ScorePrint(screen, score_p1, score_p2):
    font= pygame.font.SysFont(None,100)
    img = font.render(str(score_p1)+" - "+str(score_p2),True, (255,0,0,50))
    rect= img.get_rect(center=(SCREEN_WIDTH/2,50))
    screen.blit(img,rect)

        
def main():
    global score_p1,score_p2

    bar_speed= 10
    
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock=pygame.time.Clock()

    ballRadius= 10
    ball_xspeed= 10
    ball_yspeed= 10 #redefine in pong_init
    
    bar1, bar2, ball, r, ball_yspeed=pong_init(screen,ballRadius)
    ball_xspeed *= r # random direction left or right
    

    running = True

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                 if event.key==pygame.K_SPACE:
                      running= not running
            
        if running:   
            keys=pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                    bar2_update(bar_speed,bar2,up=1,down=0)
            if keys[pygame.K_DOWN]:
                    bar2_update(bar_speed,bar2,up=0,down=1)
            if keys[pygame.K_LCTRL]:
                    bar1_update(bar_speed,bar1,up=0,down=1)
            if keys[pygame.K_LSHIFT]:
                    bar1_update(bar_speed,bar1,up=1,down=0)
            
            screen.fill(COLOR_BG)
            ball_xspeed, ball_yspeed=pong_update(screen,bar1,bar2,ball,ball_xspeed,ball_yspeed)    
            ScorePrint(screen, score_p1, score_p2)
            pygame.display.update()
            clock.tick(60)

        #finish condition
        if ball.center[0]<0:
             score_p2 += 1
             break
        elif ball.center[0]>SCREEN_WIDTH:
             score_p1 +=1
             break
            

if __name__=="__main__":
    score_p1=0
    score_p2=0
    while True:
        pygame.time.wait(1000)
        main()