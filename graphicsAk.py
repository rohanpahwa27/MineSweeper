import pygame

#DISPLAY GRAPHICS
def display_graphics(matrix, dim):
    pygame.init()

    #set up drawing window
    screen = pygame.display.set_mode([520,520])

    pygame.display.set_caption("Answer Key")
    running = True

    font = pygame.font.SysFont("arial", 36)

    #run the game
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False

        screen.fill((255,255,255)) #fill background with white

        #define variables
        width = int(500/dim)
        black = (0,0,0)
        orange = (255,69,0)
        green = (0,100,0)
        blue = (0,0,128)

        #draw grid
        pygame.draw.rect(screen, black, (10,10,500,500),2)
        for i in range(int(500/dim), 500, int(500/dim)):
            pygame.draw.line(screen, black,(i+10,10),(i+10,510))
            pygame.draw.line(screen, black,(10,i+10),(510,i+10))


        #draw mines
        radius = int(width/3) #radius of mine
        for i in range(0, dim):
            for j in range(0, dim):
                if(matrix[i,j] == 9):
                    si = 10+(i*width)
                    sj = 10+(j*width)
                    pygame.draw.circle(screen, orange, (int((10+(i*width)+(width/2))),int((10+(j*width)+(width/2)))),radius)
                    pygame.draw.polygon(screen, orange, ((si+width/2,sj+(width/10)),(si+(width/3),sj+(width/4)),(si+(2*width/3),sj+(width/4)))) #top triangle
                    pygame.draw.polygon(screen, orange, ((si+width/2,sj+(9*width/10)),(si+(width/3),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom triangle
                    pygame.draw.polygon(screen, orange, ((si+(2*width/3),sj+(width/4)),(si+(5*width/6),sj+(width/4)),(si+(3*width/4),sj+(width/2)))) #top right
                    pygame.draw.polygon(screen, orange, ((si+(3*width/4),sj+(width/2)),(si+(5*width/6),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom right
                    pygame.draw.polygon(screen, orange, ((si+(width/3),sj+(width/4)),(si+(width/6),sj+(width/4)),(si+(width/4),sj+(width/2)))) #top left
                    pygame.draw.polygon(screen, orange, ((si+(width/4),sj+(width/2)),(si+(width/6),sj+(3*width/4)),(si+(width/3),sj+(3*width/4)))) #bottom left

                if(matrix[i,j] >= 0 and matrix[i,j] <= 8):
                    color = green
                if(matrix[i,j] == 0):
                    color = black
                if(matrix[i,j] == 1):
                    color = green
                if(matrix[i,j] == 2):
                    color = blue
                #add colors for rest of numbers
                if(matrix[i,j] >= 0 and matrix[i,j] <= 8):
                    #draw numbers in box
                    text = font.render(str(matrix[i][j]), True, color)
                    screen.blit(text,(i*width+10+(width/3),j*width+10+(width/8)))
        pygame.display.flip()

    pygame.quit()
