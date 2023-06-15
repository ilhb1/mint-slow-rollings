import pygame
import math
import pygame.locals as pl

class Graphics:
    # Define the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LINE_COLOUR = WHITE
    TEXT_COLOUR = WHITE
    BACKGROUND_COLOUR = BLACK

    # Set up node dimensions
    NODE_RADIUS = 20
    NODE_GAP = 50
    HEIGHT = 50
    ANGLE_DEC_FACTOR = 0.75
    INIT_ANGLE = 5/12 * math.pi

    def __init__(self, w=1000, h=800):
        self.entities = []
        self.screen_width = w
        self.screen_height = h
        self.screen = None

    # helper functions
    def draw_binary_tree(self, achains, starting, size):
        sizex, sizey = size
        d = 1
        lengths = [len(v) for v in achains]
        max_depth = max(lengths)
        local_height = sizey//max_depth
        angle_dec = (math.atan((sizex / (2**(max_depth))  - d) / (2*local_height)) / INIT_ANGLE) ** (1/(max_depth + 1))
        # print(angle_dec)
        rec_draw("", achains, starting, starting, INIT_ANGLE * angle_dec, local_height,angle_dec)

    def rec_draw(self, string, achains, coords, ancestor, angle, local_height, angle_dec):
        (x,y) = coords
        # pygame.draw.circle(screen, WHITE, (x, y), NODE_RADIUS)
        # pygame.draw.circle(screen, BLACK, (x, y), NODE_RADIUS, 1)
        # font = pygame.font.Font(None, 20)
        # text = font.render(str(string), True, BLACK)
        # text_rect = text.get_rect(center=(x, y))
        # screen.blit(text, text_rect)

        if string in achains:
            font = pygame.font.Font(None, 32)
            text = font.render(string + ": " + str(achains.index(string)), True, TEXT_COLOUR)
            # text = font.render(str(achains.index(string)), True, TEXT_COLOUR)
            text_rect = text.get_rect(center=(x, y + local_height //4))
            self.screen.blit(text, text_rect)

        # Calculate the coordinates for the child nodes
        left_x = x - local_height * math.tan(angle)
        right_x = x + local_height * math.tan(angle)
        child_y = y + local_height

        if string == "":
            pass
        elif string[-1] == "1":
            # pygame.draw.line(screen, BLACK, (ancestor[0], ancestor[1] + NODE_RADIUS), (coords[0], coords[1]- NODE_RADIUS), 2)

            pygame.draw.line(self.screen, LINE_COLOUR, ancestor, coords, 2)
        elif string[-1] == "0":

            # pygame.draw.line(screen, BLACK, (ancestor[0], ancestor[1] + NODE_RADIUS), (coords[0], coords[1]- NODE_RADIUS), 2)
            pygame.draw.line(self.screen, LINE_COLOUR, ancestor, coords, 2)
        if string not in achains:
            rec_draw(string + "1", achains, (right_x, child_y), coords, angle * angle_dec, local_height, angle_dec)
            rec_draw(string + "0", achains, (left_x, child_y), coords, angle * angle_dec, local_height, angle_dec)

    # Function to handle window resizing
    def handle_resize(event):
        self.screen_width, self.screen_height = event.w, event.h

    def handle_text(text):
        print(text)
        pass
    
    # use this function
    def run_window(self):
        # Initialize Pygame
        pygame.init()
        FONT = pygame.font.Font(None, 32)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Tree pair")

        # Set up the text input box
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        text = ''
        active = False

        # Game loop
        running = True
        while running:
            input_box = pygame.Rect(10, self.screen_height - 40, self.screen_width - 20, 40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    handle_resize(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the user clicked on the input box
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable
                        active = not active
                    else:
                        active = False
                    # Change the input box color based on its active state
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            handle_text(text)
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Fill the screen with a background color
            self.screen.fill(self.BACKGROUND_COLOUR)

            # tree_size = (600,500)
            # self.draw_binary_tree(antichain, (SCREEN_WIDTH//2, 50), tree_size)

            # pygame.draw.rect(screen, WHITE, pygame.Rect(SCREEN_WIDTH//2 - tree_size[0]//2, 50, tree_size[0], tree_size[1]), width = 1)

            # Draw the input box
            pygame.draw.rect(screen, color, input_box, 2)

            # Render the text
            txt_surface = FONT.render(text, True, TEXT_COLOUR)

            # Calculate the position of the text
            text_x = input_box.x + 5
            text_y = input_box.y + 10

            # Blit the text onto the screen
            screen.blit(txt_surface, (text_x, text_y))
            # Update the screen
            pygame.display.flip()

        # Quit the program
        pygame.quit()
