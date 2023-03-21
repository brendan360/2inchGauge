import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Define fonts
FONT = pygame.font.SysFont(None, 30)
SELECTED_FONT = pygame.font.SysFont(None, 35, bold=True)

# Define menu items
MENU_ITEMS = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10"]

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define scrollable area dimensions
AREA_WIDTH = 200
AREA_HEIGHT = 300
AREA_X = (SCREEN_WIDTH - AREA_WIDTH) // 2
AREA_Y = 150

# Define button dimensions
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
TOP_BUTTON_X = AREA_X + (AREA_WIDTH - BUTTON_WIDTH) // 2
TOP_BUTTON_Y = AREA_Y - BUTTON_HEIGHT - 10
BOTTOM_BUTTON_X = TOP_BUTTON_X
BOTTOM_BUTTON_Y = AREA_Y + AREA_HEIGHT + 10

# Define selected item dimensions
SELECTED_ITEM_X = AREA_X + (AREA_WIDTH - SELECTED_FONT.size(MENU_ITEMS[0])[0]) // 2
SELECTED_ITEM_Y = AREA_Y + (AREA_HEIGHT - SELECTED_FONT.size(MENU_ITEMS[0])[1]) // 2

# Define variables
scroll_offset = 0
selected_item_index = None

# Define functions
def draw_scrollable_area():
    area_surface = pygame.Surface((AREA_WIDTH, AREA_HEIGHT))
    area_surface.fill(WHITE)
    for i, item in enumerate(MENU_ITEMS[scroll_offset:scroll_offset+5]):
        text_surface = FONT.render(item, True, BLACK)
        text_rect = text_surface.get_rect(x=10, y=10+i*(text_surface.get_height()+10))
        area_surface.blit(text_surface, text_rect)
    screen.blit(area_surface, (AREA_X, AREA_Y))
    
def draw_buttons():
    top_button_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    top_button_surface.fill(GRAY)
    bottom_button_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    bottom_button_surface.fill(GRAY)
    top_text_surface = FONT.render("^", True, BLACK)
    top_text_rect = top_text_surface.get_rect(center=(BUTTON_WIDTH//2, BUTTON_HEIGHT//2))
    bottom_text_surface = FONT.render("v", True, BLACK)
    bottom_text_rect = bottom_text_surface.get_rect(center=(BUTTON_WIDTH//2, BUTTON_HEIGHT//2))
    top_button_surface.blit(top_text_surface, top_text_rect)
    bottom_button_surface.blit(bottom_text_surface, bottom_text_rect)
    screen.blit(top_button_surface, (TOP_BUTTON_X, TOP_BUTTON_Y))
    screen.blit(bottom_button_surface, (BOTTOM_BUTTON_X, BOTTOM_BUTTON_Y))

def draw_selected_item():
    if selected_item_index is not None:
        selected_item_surface = SELECTED_FONT.render(MENU_ITEMS[selected_item_index], True, BLACK)
        selected_item_rect = selected_item_surface.get_rect(x=SELECTED_ITEM_X, y=SELECTED_ITEM_Y)
        screen.blit(selected_item_surface, selected_item_rect)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame
