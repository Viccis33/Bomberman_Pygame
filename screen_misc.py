import pygame

def start_pause(map):

    WHITE = (255, 255, 255)
    TRANSPARENT_GRAY = (64, 64, 64, 20)
    WINDOW_WIDTH = map.res[0]
    WINDOW_HEIGHT = map.res[1]
    
    pause_font = pygame.font.SysFont(None, 40)
    pause_text = pause_font.render("Paused", True, WHITE)
    pause_text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))

    gray_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    gray_surface.fill(TRANSPARENT_GRAY)
    map.screen.blit(gray_surface, (0, 0))

    # Draw pause menu
    map.screen.blit(pause_text, pause_text_rect)
    
def game_over_screen(map):

    WHITE = (255, 255, 255)
    TRANSPARENT_RED = (200, 0, 0, 10)
    WINDOW_WIDTH = map.res[0]
    WINDOW_HEIGHT = map.res[1]
    
    pause_font = pygame.font.SysFont(None, 40)
    pause_text = pause_font.render("GAME OVER", True, WHITE)
    pause_text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    
    main_menu_font = pygame.font.SysFont(None, 40)
    main_menu_text = main_menu_font.render("Go to main menu", True, WHITE)
    main_menu_text_rect = main_menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*2 // 3))
    touch_rect = pygame.Rect(WINDOW_WIDTH//4, WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 2, WINDOW_HEIGHT*5 // 6)

    gray_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    gray_surface.fill(TRANSPARENT_RED)
    map.screen.blit(gray_surface, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click was inside the square
            if touch_rect.collidepoint(event.pos):
                print("touched")
                return True

    # Draw pause menu
    map.screen.blit(pause_text, pause_text_rect)
    map.screen.blit(main_menu_text, main_menu_text_rect)

    return False

def game_won_screen(map):

    WHITE = (255, 255, 255)
    TRANSPARENT_GREEN = (0, 128, 0, 3)
    WINDOW_WIDTH = map.res[0]
    WINDOW_HEIGHT = map.res[1]
    
    pause_font = pygame.font.SysFont(None, 40)
    pause_text = pause_font.render("GOOD GAME!", True, WHITE)
    pause_text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    
    main_menu_font = pygame.font.SysFont(None, 40)
    main_menu_text = main_menu_font.render("Go to main menu", True, WHITE)
    main_menu_text_rect = main_menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*2 // 3))
    touch_rect = pygame.Rect(WINDOW_WIDTH//4, WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 2, WINDOW_HEIGHT*5 // 6)

    gray_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    gray_surface.fill(TRANSPARENT_GREEN)
    map.screen.blit(gray_surface, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click was inside the square
            if touch_rect.collidepoint(event.pos):
                print("touched")
                return True
    # Draw pause menu
    map.screen.blit(pause_text, pause_text_rect)
    map.screen.blit(main_menu_text, main_menu_text_rect)
    return False