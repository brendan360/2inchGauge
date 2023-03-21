import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the window
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Menu Example")

# Set up the font
font = pygame.font.SysFont('Calibri', 20, True, False)

# Set up the menu items
menu_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10"]
num_items = len(menu_items)

# Set up the menu dimensions
menu_width = 200
menu_height = num_items * 30
menu_top = (size[1] - menu_height) // 2
menu_left = (size[0] - menu_width) // 2
menu_rect = pygame.Rect(menu_left, menu_top, menu_width, menu_height)

# Set up the scrolling
scroll_amount = 30
scroll_top = 0
scroll_bottom = menu_height - size[1] + menu_top
scroll_offset = 0

# Set up the selected item
selected_index = None

# Set up the main loop
done = False
clock = pygame.time.Clock()

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Handle clicks on menu items
            if menu_rect.collidepoint(event.pos):
                index = (event.pos[1] - menu_top + scroll_offset) // 30
                if 0 <= index < num_items:
                    selected_index = index
            # Handle clicks on scroll buttons
            elif event.pos[0] < menu_left:
                scroll_offset += scroll_amount
                if scroll_offset > scroll_bottom:
                    scroll_offset = scroll_bottom
            elif event.pos[0] > menu_left + menu_width:
                scroll_offset -= scroll_amount
                if scroll_offset < -scroll_top:
                    scroll_offset = -scroll_top
        elif event.type == pygame.KEYDOWN:
            # Handle Enter key to print selected item
            if event.key == pygame.K_RETURN and selected_index is not None:
                print(menu_items[selected_index])
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the menu
    pygame.draw.rect(screen, GRAY, menu_rect, 1)
    for i in range(num_items):
        text = font.render(menu_items[i], True, BLACK)
        text_rect = text.get_rect()
        text_rect.left = menu_left + 10
        text_rect.top = menu_top + i * 30 - scroll_offset
        screen.blit(text, text_rect)
    
    # Draw the scroll buttons
    pygame.draw.rect(screen, RED, pygame.Rect(0, 0, menu_left, size[1]))
    pygame.draw.rect(screen, RED, pygame.Rect(menu_left + menu_width, 0, size[0] - menu_left - menu_width, size[1]))
    
    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(60)

# Clean up Pygame
pygame.quit()
