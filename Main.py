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

again = True
adjust = True




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
deck_rect = deck_surf.get_rect(center = (120, 100))

########### text typing location thing
bar_surf = pygame.Surface((5, 60))
bar_surf.fill('Black')

########### who's playing text
who_surf = text_font.render("Who's Playing?", False, 'Black')
who_rect = who_surf.get_rect(center = (board_rect.centerx, board_rect.centery - 150))

########### bet amount warning
bet_warn_surf = warning_font.render("Please enter a value less than or equal to your current balance", False, 'Black')
bet_warn_rect = bet_warn_surf.get_rect(center = (board_rect.centerx, board_rect.centery + 250))

########### double warning
double_warn_surf = warning_font.render("Double would exceed current Balance", False, 'Black')
double_warn_rect = double_warn_surf.get_rect(center = (board_rect.centerx, 200))

########### play again warning
again_warn_surf = warning_font.render("Current Bet Exceeds Balance", False, 'Black')
again_warn_rect = again_warn_surf.get_rect(center = board_rect.center)

########### player total title
player_total_text_surf = warning_font.render("Player Total", False, 'Black')
player_total_text_rect = player_total_text_surf.get_rect(center = (200, 600))

########### dealer total title
dealer_total_text_surf = warning_font.render("Dealer Total", False, 'Black')
dealer_total_text_rect = dealer_total_text_surf.get_rect(center = (200, 400))

########### player WIN title
win_surf = title_font.render("WIN", False, 'Black')
win_rect = win_surf.get_rect(center = (board_rect.centerx, 100))

########### player LOSS title
loss_surf = title_font.render("LOSS", False, 'Black')
loss_rect = loss_surf.get_rect(center = (board_rect.centerx, 100))

########### player BLACKJACK title
blackjack_surf = play_font.render("BLACKJACK: ", False, 'Black')
blackjack_rect = blackjack_surf.get_rect(center = (board_rect.centerx - 500, 100))

########### player BUST title
bust_surf = play_font.render("BUST: ", False, 'Black')
bust_rect = bust_surf.get_rect(center = (board_rect.centerx - 400, 100))

########### dealer BUST title
dealer_bust_surf = play_font.render("BUST: ", False, 'Black')
dealer_bust_rect = dealer_bust_surf.get_rect(center = (board_rect.centerx - 400, 100))

########### player PUSH title
push_surf = title_font.render("PUSH", False, 'Black')
push_rect = push_surf.get_rect(center = (board_rect.centerx, 100))

########### current balance display
balance_surf = button_font.render("Balance:", False, 'Black')
balance_rect = balance_surf.get_rect(topleft = (1100, 30))


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

########### exit button
exit_button_surf = button_font.render("EXIT", False, 'Grey')
exit_button_hover_surf = button_font.render("EXIT", False, 'Black')
exit_button_rect = exit_button_surf.get_rect(center = (1300, board_rect.centery + 100))









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
            if clicked and typed_name != "":
                break

        pygame.display.update()
        clock.tick(60)




    bet_value = 0
    while again:
        game = BlackjackGame(typed_name)

        while adjust:
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
                if typed_number != "":
                    if int(typed_number) > player_balance:
                        screen.blit(bet_warn_surf, bet_warn_rect)
                        balance_warning = True
                if (frame_counter // 30) % 2 == 0:
                    screen.blit(bar_surf, bar_rect)

                mouse_pos = pygame.mouse.get_pos()

                if bet_rect.collidepoint(mouse_pos):
                    screen.blit(bet_surf_hover, bet_rect)
                    if clicked and not balance_warning and typed_number != "" and int(typed_number) != 0:
                        bet_value = int(typed_number)
                        adjust = False
                        break

                pygame.display.update()
                clock.tick(60)














        game.start_round()
        game.place_bet(bet_value)
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
            screen.blit(hit_surf, hit_rect)
            screen.blit(stand_surf, stand_rect)
            screen.blit(double_surf, double_rect)
            screen.blit(player_total_text_surf, player_total_text_rect)

            screen.blit(balance_surf, balance_rect)
            balance_display_surf = button_font.render(str(game.get_balance()), False, 'Black')
            balance_display_rect = balance_display_surf.get_rect(midtop = balance_rect.midbottom)
            screen.blit(balance_display_surf, balance_display_rect)

            player_card_total = game.get_player_totals()[0]
            player_card_alt_total = game.get_player_totals()[1]
            dealer_card_total = game.get_dealer_totals()[0]
            dealer_card_alt_total = game.get_dealer_totals()[1]
            if(player_card_total != player_card_alt_total):
                player_total_surf = warning_font.render(str(player_card_total) + "/" + str(player_card_alt_total), False, 'Black')
            else:
                player_total_surf = warning_font.render(str(player_card_total), False, 'Black')
            player_total_rect = player_total_surf.get_rect(midtop = player_total_text_rect.midbottom)
            screen.blit(player_total_surf, player_total_rect)

            ############################### DISPLAYING PLAYER CARDS
            card_x_pos = 75
            card_y_pos = 750

            for card in game.player_hand:
                card_surf = pygame.image.load("graphics/" + game.get_card(card) + ".png").convert()
                card_rect = card_surf.get_rect(midleft = (card_x_pos, card_y_pos))
                card_x_pos += 136
                screen.blit(card_surf, card_rect)
            ##############################

            ############################### DISPLAYING DEALER CARDS
            card_x_pos = 75
            card_y_pos = 300

            card_surf = pygame.image.load("graphics/" + game.get_card(game.dealer_hand[0]) + ".png"). convert()
            card_rect = card_surf.get_rect(midleft = (card_x_pos, card_y_pos))
            card_x_pos += 136
            screen.blit(card_surf, card_rect)
            blank_surf = pygame.image.load("graphics/blueback.png").convert()
            blank_rect = blank_surf.get_rect(midleft = (card_x_pos, card_y_pos))
            screen.blit(blank_surf, blank_rect)

            ##############################

            mouse_pos = pygame.mouse.get_pos()

            if hit_rect.collidepoint(mouse_pos) and not game.is_game_over():
                screen.blit(hit_surf_hover, hit_rect)
                if clicked and not animation:
                    game.player_hit()

            if stand_rect.collidepoint(mouse_pos) and not game.is_game_over():
                screen.blit(stand_surf_hover, stand_rect)
                if clicked and not animation:
                    game.stand()

            if double_rect.collidepoint(mouse_pos) and not game.is_game_over() and game.can_double:
                screen.blit(double_surf_hover, double_rect)
                if clicked and not animation and game.get_balance() >= bet_value * 2:
                    game.double()
                elif game.get_balance() < bet_value * 2:
                    screen.blit(double_warn_surf, double_warn_rect)

            pygame.display.update()
            clock.tick(60)
            if game.is_game_over():
                break




    ################################################################################################
    ############################## Game end screen #################################################
        game.pay()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            clicked = False
            for event in pygame.event.get():

                if(event.type == pygame.QUIT):
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
        #################################################### DISPLAY ELEMENTS
        ################# DISPLAY SCREEN
            screen.blit(board_surf, board_rect)

        ################# DISPLAY DEALER CARDS
            card_x_pos = 75
            card_y_pos = 300

            for card in game.dealer_hand:
                card_surf = pygame.image.load("graphics/" + game.get_card(card) + ".png").convert()
                card_rect = card_surf.get_rect(midleft = (card_x_pos, card_y_pos))
                card_x_pos += 136
                screen.blit(card_surf, card_rect)
        ################# DISPLAY PLAYER CARDS
            card_x_pos = 75
            card_y_pos = 750

            for card in game.player_hand:
                card_surf = pygame.image.load("graphics/" + game.get_card(card) + ".png").convert()
                card_rect = card_surf.get_rect(midleft = (card_x_pos, card_y_pos))
                card_x_pos += 136
                screen.blit(card_surf, card_rect)

        ################# DISPLAY PLAYER CARD TOTAL
            player_card_total = game.get_player_totals()[0]
            player_card_alt_total = game.get_player_totals()[1]

            if(player_card_total != player_card_alt_total):
                player_total_surf = warning_font.render(str(player_card_total) + "/" + str(player_card_alt_total), False, 'Black')
            else:
                player_total_surf = warning_font.render(str(player_card_total), False, 'Black')
            player_total_rect = player_total_surf.get_rect(midtop = player_total_text_rect.midbottom)
            screen.blit(player_total_surf, player_total_rect)

        ################# DISPLAY DEALER CARD TOTAL
            dealer_card_total = game.get_dealer_totals()[0]
            dealer_card_alt_total = game.get_dealer_totals()[1]

            if(dealer_card_total != dealer_card_alt_total):
                dealer_total_surf = warning_font.render(str(dealer_card_total) + "/" + str(dealer_card_alt_total), False, 'Black')
            else:
                dealer_total_surf = warning_font.render(str(dealer_card_total), False, 'Black')
            dealer_total_rect = dealer_total_surf.get_rect(midtop = dealer_total_text_rect.midbottom)
            screen.blit(dealer_total_surf, dealer_total_rect)
            screen.blit(dealer_total_text_surf, dealer_total_text_rect)

        ################# DISPLAY DECK
            for i in range(13):
                screen.blit(deck_surf, (deck_rect.left + 2 * i, deck_rect.top + 2 * i))

        ################# DISPLAY WIN
            if game.player_win:
                screen.blit(win_surf, win_rect)

        ################# DISPLAY BLACKJACK
                if game.player_blackjack:
                    screen.blit(blackjack_surf, blackjack_rect)
        
        ################# DISPLAY DEALER BUST
                elif game.dealer_bust:
                    screen.blit(dealer_bust_surf, dealer_bust_rect)

        ################# DISPLAY LOSS
            elif game.dealer_win:
                screen.blit(loss_surf, loss_rect)

        ################# DISPLAY PLAYER BUST
                if game.player_bust:
                    screen.blit(bust_surf, bust_rect)

        ################# DISPLAY PUSH
            else:
                screen.blit(push_surf, push_rect)

        ################# DISPLAY BALANCE
            screen.blit(balance_surf, balance_rect)
            balance_display_surf = button_font.render(str(game.get_balance()), False, 'Black')
            balance_display_rect = balance_display_surf.get_rect(midtop = balance_rect.midbottom)
            screen.blit(balance_display_surf, balance_display_rect)

        ################# DISPLAY AMOUNT PAID
            payout = game.payout()
            payout_surf = button_font.render("Payout: " + str(payout), False, 'Black')
            payout_rect = payout_surf.get_rect(midtop = balance_display_rect.midbottom)
            screen.blit(payout_surf, payout_rect)

        ################# ADJUST BET BUTTON
            adjust_button_surf = button_font.render("Adjust Bet", False, 'Grey')
            adjust_button_hover_surf = button_font.render("Adjust Bet", False, 'Black')
            adjust_button_rect = adjust_button_surf.get_rect(topright = (exit_button_rect.left - 50, exit_button_rect.top))
            screen.blit(adjust_button_surf, adjust_button_rect)

        ################# PLAY AGAIN BUTTON
            again_button_surf = button_font.render("Play Again", False, 'Grey')
            again_button_hover_surf = button_font.render("Play Again", False, 'Black')
            again_button_rect = again_button_surf.get_rect(topright = (adjust_button_rect.left - 50, exit_button_rect.top))
            screen.blit(again_button_surf, again_button_rect)

        ################# EXIT BUTTON
            screen.blit(exit_button_surf, exit_button_rect)

        #################################################### MAKE BUTTONS WORK
        ################ PLAY AGAIN BUTTON CLICK
            if again_button_rect.collidepoint(mouse_pos):
                if game.get_balance() >= bet_value:
                    screen.blit(again_button_hover_surf, again_button_rect)
                    if clicked:
                        again = True
                        adjust = False
                        break
                else:
                    screen.blit(again_warn_surf, again_warn_rect)

        ################ ADJUST BET BUTTON CLICK
            if adjust_button_rect.collidepoint(mouse_pos):
                screen.blit(adjust_button_hover_surf, adjust_button_rect)
                if clicked:
                    adjust = True
                    break

        ################ EXIT GAME BUTTON CLICK
            if exit_button_rect.collidepoint(mouse_pos):
                screen.blit(exit_button_hover_surf, exit_button_rect)
                if clicked:
                    pygame.quit()
                    exit()

            pygame.display.update()
            clock.tick(60)
        game.save_data()