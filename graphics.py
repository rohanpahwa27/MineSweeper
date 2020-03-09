import pygame

#DISPLAY GRAPHICS
def display_graphics(matrix, dim, clicked):
    print(clicked)
    pygame.init()

    #define variables
    swidth = int(600/dim)*dim
    width = int(swidth/dim)
    white = (255,255,255)
    black = (0,0,0)
    orange = (255,69,0)
    green = (0,100,0)
    blue = (0,0,128)
    purple = (128,0,128)
    gray = (169,169,169)
    maroon = (115,0,0)
    rust = (210,150,75)
    skyblue = (0,255,255)
    mine_pic = pygame.image.load('mine.jpg')
    flag_pic = pygame.image.load('flag.png')
    mine_pic = pygame.transform.scale(mine_pic,(width-2,width-2))
    flag_pic = pygame.transform.scale(flag_pic,(width-2,width-2))
    font = pygame.font.SysFont("arial", width)

    #set up drawing window
    screen = pygame.display.set_mode([swidth+20,swidth+20])
    screen.fill(white) #fill background with white
    pygame.display.set_caption("Game Board")

    running = False

    #draw grid
    pygame.draw.rect(screen, gray, (10,10,swidth,swidth))
    pygame.draw.rect(screen, black, (10,10,swidth,swidth),2)
    for i in range(width, swidth, width):
        pygame.draw.line(screen, black,(i+10,10),(i+10,swidth+10))
        pygame.draw.line(screen, black,(10,i+10),(swidth+10,i+10))
    pygame.display.flip()


    #need in order to update screen
    clock = pygame.time.Clock()
    move = -1

    while not running:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                running = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                move+=1
                #if move < dim*dim:
                #     print(clicked[move][1], clicked[move][0])
                # else:
                #     print("done")

                if move < dim*dim:
                    for m in range(move+1):
                        x = clicked[move][0]
                        y = clicked[move][1]

                        #set colors for numbers and display
                        if(matrix[y,x].num == 0):
                            color = black
                        if(matrix[y,x].num == 1):
                            color = green
                        if(matrix[y,x].num == 2):
                            color = blue
                        if(matrix[y,x].num == 3):
                            color = orange
                        if(matrix[y,x].num == 4):
                            color = purple
                        if(matrix[y,x].num == 5):
                            color = rust
                        if(matrix[y,x].num == 6):
                            color = maroon
                        if(matrix[y,x].num == 7):
                            color = blue
                        if(matrix[y,x].num == 8):
                            color = skyblue
                        #draw numbers in box
                        if(matrix[y,x].mine == 2):
                            text = font.render(str(matrix[y,x].num), True, color)
                            screen.blit(text,(x*width+10+(width/4),y*width+10-(width/12)))
                        if(matrix[y,x]).mine == 3: #display flags
                            screen.blit(flag_pic,(x*width+11,y*width+11))
                        if(matrix[y,x].mine == 1): #display mines
                            screen.blit(mine_pic,(x*width+11,y*width+11))


            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    pygame.quit()
