import pygame
from .base import BaseScreen

class TitleScreen(BaseScreen):
    def __init__(self, screen, assets, clock):
        super().__init__(screen, assets)
        self.clock = clock
        self.fonts = assets['fonts']
        self.title_surf = self.fonts['150'].render('Blackjack', False, 'Black')
        self.title_rect = self.title_surf.get_rect(center=(assets['board_rect'].centerx, assets['board_rect'].centery - 200))

        self.play_surf = self.fonts['100'].render('PLAY', False, 'Grey')
        self.play_surf_hover = self.fonts['100'].render('Play', False, 'Black')
        self.play_rect = self.play_surf.get_rect(center=(assets['board_rect'].centerx, assets['board_rect'].centery + 100))

    def run(self):
        # clock = pygame.time.Clock()
        while True:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True

            self.screen.blit(self.assets['board'], self.assets['board_rect'])
            self.screen.blit(self.title_surf, self.title_rect)
            self.screen.blit(self.play_surf, self.play_rect)

            mouse_pos = pygame.mouse.get_pos()
            if self.play_rect.collidepoint(mouse_pos):
                self.screen.blit(self.play_surf_hover, self.play_rect)
                if clicked:
                    return 

            pygame.display.update()
            self.clock.tick(60)
