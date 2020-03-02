import pygame

#DISPLAY GRAPHICS
def display_graphics(matrix, dim):
    pygame.init()
    
    #set up drawing window
    screen = pygame.display.set_mode([520,520])
    
    pygame.display.set_caption("Game Board")
    running = True
    
    font = pygame.font.SysFont("arial", 36)
    
    #run the game
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False
        
        #define variables
        width = int(500/dim)
        white = (255,255,255)
        black = (0,0,0)
        orange = (255,69,0)
        green = (0,100,0)
        blue = (0,0,128)
        purple = (128,0,128)
        gray = (169,169,169)
        mine_pic = pygame.image.load('mine.jpg')
        flag_pic = pygame.image.load('flag.png')
        mine_pic = pygame.transform.scale(mine_pic,(width-2,width-2))
        flag_pic = pygame.transform.scale(flag_pic,(width-2,width-2))

        screen.fill(white) #fill background with white
        #screen.fill(gray,(10,10,width,width))
        pygame.draw.rect(screen, gray, (10,10,500,500))
        
        #draw grid
        pygame.draw.rect(screen, black, (10,10,500,500),2)
        for i in range(int(500/dim), 500, int(500/dim)):
            pygame.draw.line(screen, black,(i+10,10),(i+10,510))
            pygame.draw.line(screen, black,(10,i+10),(510,i+10))

        
        #draw mines
        radius = int(width/3) #radius of mine
        for i in range(0, dim):
            for j in range(0, dim):
                if(matrix[j,i]).mine == 0: #display hidden spots
                    text = font.render("?", True, purple)
                    screen.blit(text,(i*width+10+(width/3),j*width+10+(width/8)))
                if(matrix[j,i]).mine == 3: #display flags
                    screen.blit(flag_pic,(i*width+11,j*width+11))
                if(matrix[j,i].num == 9): #display mines
                    screen.blit(mine_pic,(i*width+11,j*width+11))
                #set colors for numbers and display
                if(matrix[j,i].num >= 0 and matrix[j,i].num <= 8):
                    color = green
                if(matrix[j,i].num == 0):
                    color = black
                if(matrix[j,i].num == 1):
                    color = green
                if(matrix[j,i].num == 2):
                    color = blue
                #add colors for rest of numbers
                if(matrix[j,i].mine == 2 and matrix[j,i].num >= 0 and matrix[j,i].num <= 8):
                    #draw numbers in box
                    text = font.render(str(matrix[j,i].num), True, color)
                    screen.blit(text,(i*width+10+(width/3),j*width+10+(width/8)))
        pygame.display.flip()

pygame.quit()
