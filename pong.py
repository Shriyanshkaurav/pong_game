import pygame
from paddle import Paddle
from ball import Ball
pygame.init()

WIDTH, HEIGHT = 700, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong game")
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
PADDLE_W,PADDLE_H =10,100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 10



def draw(win,paddles,ball,player1,player2):
    win.fill(BLACK)
    player1_text =SCORE_FONT.render(f"{player1}",1, WHITE)
    player2_text =SCORE_FONT.render(f"{player2}",1, WHITE)

    win.blit(player1_text,(WIDTH//4 - player1_text.get_width()//2,20))
    win.blit(player2_text,(WIDTH*(3/4) - player2_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10,HEIGHT,HEIGHT//2):
        if i%2==1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 5    , HEIGHT//2))   

    ball.draw(win)

    pygame.display.update()

def handle_collision(ball, paddle1, paddle2):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= paddle1.y and ball.y <= paddle1.y + paddle1.height:
            if ball.x - ball.radius <= paddle1.x + paddle1.width:
                ball.x_vel *= -1

                middle_y = paddle1.y + paddle1.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (paddle1.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= paddle2.y and ball.y <= paddle2.y + paddle2.height:
            if ball.x + ball.radius >= paddle2.x:
                ball.x_vel *= -1

                middle_y = paddle2.y + paddle2.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (paddle2.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys,paddle1,paddle2):
    if keys[pygame.K_w] and paddle1.y-paddle1.VEL>=10:
        paddle1.move(up =True)
    if keys[pygame.K_s] and paddle1.y+paddle1.height+paddle1.VEL <= HEIGHT:
        paddle1.move(up = False)

    if keys[pygame.K_UP] and paddle2.y-paddle2.VEL>=10:
        paddle2.move(up =True)
    if keys[pygame.K_DOWN] and paddle2.y+paddle2.height+paddle2.VEL <= HEIGHT:
        paddle2.move(up = False)        



def main():
    run = True
    clock = pygame.time.Clock()
    PADDLE1 = Paddle(10,HEIGHT//2-PADDLE_H//2,PADDLE_W,PADDLE_H)
    PADDLE2 = Paddle(WIDTH-10-PADDLE_W,HEIGHT//2-PADDLE_H//2,PADDLE_W,PADDLE_H)

    ball = Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS)

    player1 = 0
    player2 = 0


    while run:
        clock.tick(FPS)
        draw(WIN,[PADDLE1,PADDLE2],ball,player1,player2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,PADDLE1,PADDLE2)
        ball.move()
        handle_collision(ball,PADDLE1,PADDLE2)

        if ball.x <0:
            player2+=1
            ball.reset()
        elif ball.x>WIDTH:
            player1 += 1
            ball.reset()
        won = False    
        if player1 >= WINNING_SCORE:
            won = True
            win_text = "player 1 won!" 
        elif player2 >= WINNING_SCORE:
            won = True
            win_text = "player 2 won!"
        if won:    
            text = SCORE_FONT.render(win_text,1,WHITE)
            WIN.blit(text,(WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(10000)
            ball.reset()
            PADDLE1.reset()
            PADDLE2.reset()      
            player1=0
            player2=0


    pygame.quit()  # This should be inside the main function

if __name__ == '__main__':
    main()

