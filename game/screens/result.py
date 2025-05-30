import pygame
import os
from .base import BaseScreen

class ResultScreen(BaseScreen):
    def __init__(self, screen, game, bet_value, assets, clock):
        super().__init__(screen, assets)
        self.clock = clock
        self.fonts = assets['fonts']
        self.warning_font = self.fonts['30']
        self.button_font = self.fonts['50']
        self.title_font = self.fonts['150']
        self.play_font = self.fonts['100']
        self.game = game
        self.bet_value = bet_value
        self.assets = assets
        self.screen = screen



        ########### player WIN title
        self.win_surf = self.title_font.render("WIN", False, 'Black')
        self.win_rect = self.win_surf.get_rect(center = (assets['board_rect'].centerx, 100))

        ########### player LOSS title
        self.loss_surf = self.title_font.render("LOSS", False, 'Black')
        self.loss_rect = self.loss_surf.get_rect(center = (assets['board_rect'].centerx, 100))

        ########### player PUSH title
        self.push_surf = self.title_font.render("PUSH", False, 'Black')
        self.push_rect = self.push_surf.get_rect(center = (assets['board_rect'].centerx, 100))

        ########### player BLACKJACK title
        self.blackjack_surf = self.fonts['70'].render("PLAYER BLACKJACK", False, 'Black')
        self.blackjack_rect = self.blackjack_surf.get_rect(midtop = self.win_rect.midbottom)

        ########### player BUST title
        self.bust_surf = self.fonts['70'].render("PLAYER BUST", False, 'Black')
        self.bust_rect = self.bust_surf.get_rect(midtop = self.loss_rect.midbottom)

        ########### dealer BUST title
        self.dealer_bust_surf = self.fonts['70'].render("DEALER BUST", False, 'Black')
        self.dealer_bust_rect = self.dealer_bust_surf.get_rect(midtop = self.win_rect.midbottom)

        ########### exit button
        self.exit_button_surf = self.button_font.render("EXIT", False, 'Grey')
        self.exit_button_hover_surf = self.button_font.render("EXIT", False, 'Black')
        self.exit_button_rect = self.exit_button_surf.get_rect(center = (1300, assets['board_rect'].centery + 75))

        ################# ADJUST BET BUTTON
        self.adjust_button_surf = self.button_font.render("Adjust Bet", False, 'Grey')
        self.adjust_button_hover_surf = self.button_font.render("Adjust Bet", False, 'Black')
        self.adjust_button_rect = self.adjust_button_surf.get_rect(topright = (self.exit_button_rect.left - 50, self.exit_button_rect.top))
        # screen.blit(adjust_button_surf, adjust_button_rect)

        ################# PLAY AGAIN BUTTON
        self.again_button_surf = self.button_font.render("Play Again", False, 'Grey')
        self.again_button_hover_surf = self.button_font.render("Play Again", False, 'Black')
        self.again_button_rect = self.again_button_surf.get_rect(topright = (self.adjust_button_rect.left - 50, self.exit_button_rect.top))
        # screen.blit(again_button_surf, again_button_rect)

        ########### player total title
        self.player_total_text_surf = self.warning_font.render("Player Total", False, 'Black')
        self.player_total_text_rect = self.player_total_text_surf.get_rect(center = (200, 600))

        ########### dealer total title
        self.dealer_total_text_surf = self.warning_font.render("Dealer Total", False, 'Black')
        self.dealer_total_text_rect = self.dealer_total_text_surf.get_rect(center = (200, 450))

        ########### current balance display
        self.balance_surf = self.button_font.render("Balance:", False, 'Black')
        self.balance_rect = self.balance_surf.get_rect(topleft = (1150, 30))

        ########### play again warning
        self.again_warn_surf = self.warning_font.render("Current Bet Exceeds Balance", False, 'Black')
        self.again_warn_rect = self.again_warn_surf.get_rect(center = assets['board_rect'].center)



    def run(self):
        # clock = pygame.time.Clock()
        self.game.pay()

        while True:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True

            self.screen.blit(self.assets['board'], self.assets['board_rect'])

            # Dealer Cards
            self._draw_hand(self.game.dealer_hand, y=350)

            # Player Cards
            self._draw_hand(self.game.player_hand, y=750)

            # Totals
            self._draw_totals(self.game)

            # Deck stack
            deck_rect = self.assets["card_back"].get_rect(center = (120, 150))
            for i in range(13):
                self.screen.blit(self.assets['card_back'], (deck_rect.left + 2 * i, deck_rect.top + 2 * i))

            # Outcome
            if self.game.player_win:
                self.screen.blit(self.win_surf, self.win_rect)
                if self.game.player_blackjack:
                    self.screen.blit(self.blackjack_surf, self.blackjack_rect)
                elif self.game.dealer_bust:
                    self.screen.blit(self.dealer_bust_surf, self.dealer_bust_rect)
            elif self.game.dealer_win:
                self.screen.blit(self.loss_surf, self.loss_rect)
                if self.game.player_bust:
                    self.screen.blit(self.bust_surf, self.bust_rect)
            else:
                self.screen.blit(self.push_surf, self.push_rect)

            # Balance
            self.screen.blit(self.balance_surf, self.balance_rect)
            player_balance_surf = self.button_font.render(str(self.game.balance), False, 'Black')
            player_balance_rect = player_balance_surf.get_rect(midtop=self.balance_rect.midbottom)
            self.screen.blit(player_balance_surf, player_balance_rect)

            # Payout
            payout = self.game.payout()
            payout_surf = self.button_font.render("Payout: " + str(payout), False, 'Black')
            payout_rect = payout_surf.get_rect(midtop = player_balance_rect.midbottom)
            self.screen.blit(payout_surf, payout_rect)

            # Buttons
            self.screen.blit(self.adjust_button_surf, self.adjust_button_rect)
            self.screen.blit(self.again_button_surf, self.again_button_rect)
            self.screen.blit(self.exit_button_surf, self.exit_button_rect)
            decision = self._handle_buttons(mouse_pos, clicked, self.game, self.bet_value)
            if decision:
                return decision

            pygame.display.update()
            self.clock.tick(60)

    def _draw_hand(self, hand, y):
        x = 75
        for card in hand:
            card_surf = self.assets['cards'][self.game.get_card(card)]
            self.screen.blit(card_surf, card_surf.get_rect(midleft=(x, y)))
            x += 136

    def _draw_totals(self, game):
        # Player total
        pt, pt_alt = game.get_player_totals()
        player_text = f"{pt}/{pt_alt}" if pt != pt_alt else str(pt)
        player_total_surf = self.warning_font.render(player_text, False, 'Black')
        player_total_rect = player_total_surf.get_rect(midtop = self.player_total_text_rect.midbottom)
        self.screen.blit(self.player_total_text_surf, self.player_total_text_rect)
        self.screen.blit(player_total_surf, player_total_rect)

        # Dealer total
        dt, dt_alt = game.get_dealer_totals()
        dealer_text = f"{dt}/{dt_alt}" if dt != dt_alt else str(dt)
        dealer_total_surf = self.warning_font.render(dealer_text, False, 'Black')
        dealer_total_rect = dealer_total_surf.get_rect(midtop = self.dealer_total_text_rect.midbottom)
        self.screen.blit(self.dealer_total_text_surf, self.dealer_total_text_rect)
        self.screen.blit(dealer_total_surf, dealer_total_rect)

    def _handle_buttons(self, mouse_pos, clicked, game, bet_value):
        if self.again_button_rect.collidepoint(mouse_pos):
            if game.balance >= bet_value:
                self.screen.blit(self.again_button_hover_surf, self.again_button_rect)
                if clicked:
                    return [False, False]
            else:
                self.screen.blit(self.again_warn_surf, self.again_warn_rect)

        if self.adjust_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.adjust_button_hover_surf, self.adjust_button_rect)
            if clicked:
                return [True, False]

        if self.exit_button_rect.collidepoint(mouse_pos):
            self.screen.blit(self.exit_button_hover_surf, self.exit_button_rect)
            if clicked:
                return [False, True]
