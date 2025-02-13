import pygame
from levels.level_0 import play_level_0
from play_level import play_level
import json

with open('data/levels.json') as f:
    all_levels = json.load(f)

print(all_levels)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

LEVEL_RECT_WIDTH = 160
LEVEL_RECT_HEIGHT = LEVEL_RECT_WIDTH

level_rects = {int(i) :pygame.Rect(200*(1+int(i)%5), 200 + 200*(int(i)//5), LEVEL_RECT_WIDTH, LEVEL_RECT_HEIGHT) for i in all_levels['levels'].keys()}
level_rect_font = pygame.font.SysFont(None, 40)
level_rects_texts = {level_rect: level_rect_font.render(str(level_rect+1), True, (255,255,255)) for level_rect in level_rects}
level_rect_text_rects = {level_rect: level_rects_texts[level_rect].get_rect(center=(level_rects[level_rect].left + LEVEL_RECT_WIDTH // 2, level_rects[level_rect].top + LEVEL_RECT_HEIGHT // 2)) for level_rect in level_rects}


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click was inside the square
            for level_i in level_rects:
                if level_rects[level_i].collidepoint(event.pos):
                    finished = play_level(all_levels["levels"][str(level_i)])
                    print(finished)
                    all_levels["levels"][str(level_i)]['finished'] = finished or all_levels["levels"][str(level_i)]['finished']
            
    screen.fill((0,0,0))

    # Draw the square
    for level_rect in level_rects:
        level_rect_color = (255, 0, 0)
        if all_levels["levels"][str(level_rect)]['finished']:
            level_rect_color = (0, 255, 0)
        pygame.draw.rect(screen, level_rect_color, level_rects[level_rect])
        
        screen.blit(level_rects_texts[level_rect], level_rect_text_rects[level_rect])

    # Update the display
    # pygame.display.flip()
            
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()