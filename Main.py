import pygame
from sys import exit
from blackjack import BlackjackGame

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

click_primed = False
clicking = False
playing = True
animation = False




########## fonts
text_font = pygame.font.Font('font/BJ_Font.ttf', 50)
button_font = pygame.font.Font('font/BJ_Font.ttf', 60)
title_font = pygame.font.Font('font/BJ_Font.ttf', 150)
play_font = pygame.font.Font('font/BJ_Font.ttf', 100)
warning_font = pygame.font.Font('font/BJ_Font.ttf', 30)

########### background
board_surf = pygame.image.load('graphics/BJB.png').convert()
board_rect = board_surf.get_rect(topleft = (0,0))

########### title
title_surf = title_font.render('Blackjack', False, 'Black')
title_rect = title_surf.get_rect(center = (board_rect.centerx, board_rect.centery - 200))

########### deck
deck_surf = pygame.image.load('graphics/blueback.png').convert()
deck_rect = deck_surf.get_rect(center = (1400, board_rect.centery))

########### text typing location thing
bar_surf = pygame.Surface((5, 60))
bar_surf.fill('Black')

########### who's playing text
who_surf = text_font.render("Who's Playing?", False, 'Black')
who_rect = who_surf.get_rect(center = (board_rect.centerx, board_rect.centery - 150))

########### bet amount warning
bet_warn_surf = warning_font.render("Please enter a value less than or equal to your current balance", False, 'Black')
bet_warn_rect = bet_warn_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 250))

######################  BUTTONS   ###################################
########## play button
play_surf = play_font.render('PLAY', False, 'Grey')
play_surf_hover = play_font.render('Play', False, 'Black')
play_rect = play_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 100))

########### hit button
hit_surf = button_font.render('HIT', False, 'Grey')
hit_surf_hover = button_font.render('HIT', False, 'Black')
hit_rect = hit_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 100))

########### stand button
stand_surf = button_font.render('STAND', False, 'Grey')
stand_surf_hover = button_font.render('STAND', False, 'Black')
stand_rect = stand_surf.get_rect(midright = (hit_rect.left - 50, board_rect.centery + 100))

########### double button
double_surf = button_font.render('DOUBLE', False, 'Grey')
double_surf_hover = button_font.render('DOUBLE', False, 'Black')
double_rect = double_surf.get_rect(midleft = (hit_rect.right + 50, board_rect.centery + 100))

########### bet button
bet_surf = button_font.render('BET', False, 'Red')
bet_surf_hover = button_font.render('BET', False, '#af0000')
bet_rect = bet_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 150))

########### continue button
continue_surf = button_font.render('CONTINUE', False, 'Grey')
continue_surf_hover = button_font.render('CONTINUE', False, 'Black')
continue_rect = continue_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 200))











while playing:

    #################### Play/Intro screen
    while True:
        clicked = False
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True

        ########### PLACE ELEMENTS
        screen.blit(board_surf,board_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(play_surf, play_rect)
        mouse_pos = pygame.mouse.get_pos()

        if play_rect.collidepoint(mouse_pos):
            screen.blit(play_surf_hover, play_rect)
            if clicked:
                break

        pygame.display.update()
        clock.tick(60)








    ########################### WHO'S PLAYING?
    can_type = True
    typed_name = ""
    frame_counter = 0
    while True:
        clicked = False
        frame_counter += 1
        if frame_counter == 60:
            frame_counter = 0
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True
            if event.type == pygame.KEYDOWN and can_type:
                if event.unicode.isalpha() and len(typed_name) < 20:
                    typed_name += event.unicode
                    print("Typed:", typed_name)
                elif event.key == pygame.K_BACKSPACE and len(typed_name) > 0:
                    typed_name = typed_name[:-1]
                can_type = False
            if event.type == pygame.KEYUP:
                can_type = True

        ########### Generate text surface/rectangle

        player_surf = text_font.render(typed_name, False, 'Grey')
        player_rect = player_surf.get_rect(topleft = (board_rect.centerx - 300, board_rect.centery - 50))

        bar_rect = bar_surf.get_rect(midleft = player_rect.midright)

        ########### PLACE ELEMENTS
        screen.blit(board_surf,board_rect)
        screen.blit(who_surf, who_rect)
        screen.blit(player_surf, player_rect)
        screen.blit(continue_surf, continue_rect)
        if (frame_counter // 30) % 2 == 0:
            screen.blit(bar_surf, bar_rect)

        mouse_pos = pygame.mouse.get_pos()

        if continue_rect.collidepoint(mouse_pos):
            screen.blit(continue_surf_hover, continue_rect)
            if clicked and typed_name is not "":
                break

        pygame.display.update()
        clock.tick(60)

    game = BlackjackGame(typed_name)






    can_type = True
    typed_number = ""
    frame_counter = 0
    player_balance = game.get_balance()
    ######################### Bet amount screen
    while True:
        clicked = False
        frame_counter += 1
        if frame_counter == 60:
            frame_counter = 0

        balance_warning = False
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True
            if event.type == pygame.KEYDOWN and can_type:
                if event.unicode.isdigit() and len(typed_number) < 4:  # checks if it's a number key
                    typed_number += event.unicode
                    print("Typed:", typed_number)
                elif event.key == pygame.K_BACKSPACE and len(typed_number) > 0:
                    typed_number = typed_number[:-1]
                can_type = False
            if event.type == pygame.KEYUP:
                can_type = True

        ########### Generate text surface/rectangle
        text_surf = text_font.render(typed_number, False, 'Grey')
        text_rect = text_surf.get_rect(topleft = (board_rect.centerx - 100, board_rect.centery - 50))
        current_balance_surf = warning_font.render("Current Balance is " + str(player_balance) + ":", False, 'Black')
        current_balance_rect = current_balance_surf.get_rect(right = text_rect.left - 50, centery = text_rect.centery)
        
        bar_rect = bar_surf.get_rect(midleft = text_rect.midright)

        ########### PLACE ELEMENTS
        screen.blit(board_surf,board_rect)
        screen.blit(bet_surf, bet_rect)
        screen.blit(text_surf, text_rect)
        screen.blit(current_balance_surf, current_balance_rect)
        if typed_number is not "":
            if int(typed_number) > player_balance:
                screen.blit(bet_warn_surf, bet_warn_rect)
                balance_warning = True
        if (frame_counter // 30) % 2 == 0:
            screen.blit(bar_surf, bar_rect)

        mouse_pos = pygame.mouse.get_pos()

        if bet_rect.collidepoint(mouse_pos):
            screen.blit(bet_surf_hover, bet_rect)
            if clicked and not balance_warning:
                break

        pygame.display.update()
        clock.tick(60)














    while True:
        clicked = False
        for event in pygame.event.get():

            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True

        ########### PLACE ELEMENTS
        screen.blit(board_surf,board_rect)

        for i in range(13):
            screen.blit(deck_surf, (deck_rect.left + 2 * i, deck_rect.top + 2 * i))

        # screen.blit(hitbordertop, (400, board_rect.centery - 50))
        # screen.blit(hitbordertop, (410, board_rect.centery + 50))
        # screen.blit(hitborderside, (400, board_rect.centery - 40))
        # screen.blit(hitborderside, (600, board_rect.centery - 50))
        screen.blit(hit_surf, hit_rect)
        screen.blit(stand_surf, stand_rect)
        screen.blit(double_surf, double_rect)

        mouse_pos = pygame.mouse.get_pos()

        if hit_rect.collidepoint(mouse_pos):
            screen.blit(hit_surf_hover, hit_rect)
            if clicked and not animation:
                print("clicked")

        if stand_rect.collidepoint(mouse_pos):
            screen.blit(stand_surf_hover, stand_rect)
            if clicked and not animation:
                print("clicked")

        if double_rect.collidepoint(mouse_pos):
            screen.blit(double_surf_hover, double_rect)
            if clicked and not animation:
                print("clicked")







        pygame.display.update()
        clock.tick(60)
