import pygame
from .base import BaseScreen

class NameScreen(BaseScreen):
    def __init__(self, screen, assets, clock):
        super().__init__(screen, assets)
        self.clock = clock
        self.fonts = assets['fonts']
        self.who_surf = self.fonts['50'].render("Who's Playing?", False, 'Black')
        self.who_rect = self.who_surf.get_rect(center=(assets['board_rect'].centerx, assets['board_rect'].centery - 150))
        self.bar_surf = pygame.Surface((5, 60))
        self.bar_surf.fill('Black')
        self.continue_surf = self.fonts['70'].render('CONTINUE', False, 'Grey')
        self.continue_hover_surf = self.fonts['70'].render('CONTINUE', False, 'Black')
        self.continue_rect = self.continue_surf.get_rect(center = (self.assets['board_rect'].centerx, self.assets['board_rect'].centery + 200))

    def run(self):
        typed_name = ""
        can_type = True
        frame_counter = 0
        # clock = pygame.time.Clock()

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
                    if event.unicode.isalpha() and len(typed_name) < 20:
                        typed_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE and len(typed_name) > 0:
                        typed_name = typed_name[:-1]
                    can_type = False
                if event.type == pygame.KEYUP:
                    can_type = True

            player_surf = self.fonts['50'].render(typed_name, False, 'Grey')
            player_rect = player_surf.get_rect(topleft=(self.assets['board_rect'].centerx - 300, self.assets['board_rect'].centery - 50))
            bar_rect = self.bar_surf.get_rect(midleft=player_rect.midright)

            # Draw
            self.screen.blit(self.assets['board'], self.assets['board_rect'])
            self.screen.blit(self.who_surf, self.who_rect)
            self.screen.blit(player_surf, player_rect)
            self.screen.blit(self.continue_surf, self.continue_rect)
            if (frame_counter // 30) % 2 == 0:
                self.screen.blit(self.bar_surf, bar_rect)

            mouse_pos = pygame.mouse.get_pos()
            if self.continue_rect.collidepoint(mouse_pos):
                self.screen.blit(self.continue_hover_surf, self.continue_rect)
                if clicked and typed_name:
                    return typed_name

            pygame.display.update()
            self.clock.tick(60)
