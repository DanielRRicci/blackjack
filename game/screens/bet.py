import pygame
from .base import BaseScreen

class BetScreen(BaseScreen):
    def __init__(self, screen, game, assets, clock):
        super().__init__(screen, assets)
        self.clock = clock
        self.fonts = assets['fonts']
        self.warning_font = self.fonts['30']
        self.text_font = self.fonts['50']
        self.bet_button = self.fonts['70']
        self.bar_surf = pygame.Surface((5, 60))
        self.bar_surf.fill('Black')
        self.game = game

        self.bet_surf = self.fonts['70'].render('BET', False, 'Red')
        self.bet_surf_hover = self.fonts['70'].render('BET', False, '#af0000')
        self.bet_rect = self.bet_surf.get_rect(center = (assets['board_rect'].centerx, assets['board_rect'].centery + 150))

    def run(self):
        typed_number = ""
        can_type = True
        frame_counter = 0
        clock = pygame.time.Clock()
        balance = self.game.balance

        while True:
            clicked = False
            frame_counter = (frame_counter + 1) % 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
                if event.type == pygame.KEYDOWN and can_type:
                    if event.unicode.isdigit() and len(typed_number) < 4:
                        typed_number += event.unicode
                    elif event.key == pygame.K_BACKSPACE and len(typed_number) > 0:
                        typed_number = typed_number[:-1]
                    can_type = False
                if event.type == pygame.KEYUP:
                    can_type = True

            screen = self.screen
            assets = self.assets
            balance_warning = False

            # Draw elements
            screen.blit(assets['board'], assets['board_rect'])

            text_surf = self.text_font.render(typed_number, False, 'Grey')
            text_rect = text_surf.get_rect(topleft=(assets['board_rect'].centerx - 100, assets['board_rect'].centery - 50))

            current_balance_surf = self.warning_font.render(f"Current Balance: {balance}", False, 'Black')
            current_balance_rect = current_balance_surf.get_rect(right=text_rect.left - 50, centery=text_rect.centery)
            bar_rect = self.bar_surf.get_rect(midleft=text_rect.midright)

            screen.blit(text_surf, text_rect)
            screen.blit(current_balance_surf, current_balance_rect)
            screen.blit(self.bet_surf, self.bet_rect)

            if typed_number:
                if int(typed_number) > balance:
                    screen.blit(assets['bet_warning'], assets['bet_warning_rect'])
                    balance_warning = True

            if (frame_counter // 30) % 2 == 0:
                screen.blit(self.bar_surf, bar_rect)

            mouse_pos = pygame.mouse.get_pos()

            if self.bet_rect.collidepoint(mouse_pos):
                screen.blit(self.bet_surf_hover, self.bet_rect)
                if clicked and not balance_warning and typed_number and int(typed_number) > 0:
                    return int(typed_number)

            pygame.display.update()
            self.clock.tick(60)
