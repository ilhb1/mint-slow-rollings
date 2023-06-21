import pygame
import math
import pygame.locals as pl
import time
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
    INIT_ANGLE = 7/12 * math.pi


    def __init__(self, w=1000, h=800):
        self.entities = []
        self.screen_width = w
        self.screen_height = h
        self.screen = None
        self.event_queue = []

    # helper functions
    def draw_binary_tree(self, achains, starting, size, v=None):
        sizex, sizey = size
        lengths = [len(v) for v in achains]
        max_depth = max(lengths)
        local_height = sizey//max_depth
        angle_dec = (math.atan((sizex / (2**(max_depth))) / (2*local_height)) / self.INIT_ANGLE) ** (1/(max_depth + 1))
        # angle_dec = sizex / sizey / 1.1
        # print(angle_dec)
        self.rec_draw("", achains, starting, starting, self.INIT_ANGLE * angle_dec, local_height,angle_dec, v)

    def rec_draw(self, string, achains, coords, ancestor, angle, local_height, angle_dec, v=None):
        (x,y) = coords
        # pygame.draw.circle(screen, WHITE, (x, y), NODE_RADIUS)
        # pygame.draw.circle(screen, BLACK, (x, y), NODE_RADIUS, 1)
        # font = pygame.font.Font(None, 20)
        # text = font.render(str(string), True, BLACK)
        # text_rect = text.get_rect(center=(x, y))
        # screen.blit(text, text_rect)

        if string in achains:
            # print(achains.index(string))
            font = pygame.font.Font(None, 32)
            # text = font.render(string + ": " + str(achains.index(string)), True, self.TEXT_COLOUR)
            try: 
                text = font.render(str(achains.index(string) + 1), True, self.TEXT_COLOUR)
                text_rect = text.get_rect(center=(x, y + local_height //4))
                self.screen.blit(text, text_rect)

            except e:
                print("Exception:")
                print(string, achains)
                        # if v != None:
                # print(string, [pair[0] for pair in v.repellers])
                # if string in [pair[0] for pair in v.repellers]:
                    # print("balls")
                    # r = 10
                    # angle = 30
                    # t = (x,y + r)
                    # p = (math.cos(angle)*t[0] - math.sin(angle)*t[1], math.sin(angle)*t[0] + math.cos(angle)*t[1])

                    # q = (math.cos(2*angle)*t[0] - math.sin(2*angle)*t[1], math.sin(2*angle)*t[0] + math.cos(2*angle)*t[1])

                    # n = (math.cos(3*angle)*t[0] - math.sin(3*angle)*t[1], math.sin(3*angle)*t[0] + math.cos(3*angle)*t[1])
                    # pygame.draw.polygon(self.screen, (255, 0, 0), (p,q,n))
                    # time.sleep(10)
                    

        # Calculate the coordinates for the child nodes
        left_x = x - local_height * math.tan(angle)
        right_x = x + local_height * math.tan(angle)
        child_y = y + local_height

        if string == "":
            pass
        elif string[-1] == "1":
            # pygame.draw.line(screen, BLACK, (ancestor[0], ancestor[1] + NODE_RADIUS), (coords[0], coords[1]- NODE_RADIUS), 2)

            pygame.draw.line(self.screen, self.LINE_COLOUR, ancestor, coords, 2)
        elif string[-1] == "0":

            # pygame.draw.line(screen, BLACK, (ancestor[0], ancestor[1] + NODE_RADIUS), (coords[0], coords[1]- NODE_RADIUS), 2)
            pygame.draw.line(self.screen, self.LINE_COLOUR, ancestor, coords, 2)
        if string not in achains:
            self.rec_draw(string + "1", achains, (right_x, child_y), coords, angle * angle_dec, local_height, angle_dec, v)
            self.rec_draw(string + "0", achains, (left_x, child_y), coords, angle * angle_dec, local_height, angle_dec, v)

    # Function to handle window resizing
    def handle_resize(self, event):
        self.screen_width, self.screen_height = event.w, event.h

    def handle_text(self, text):
        print(text)

    def draw_tree_pair(self, v, pos1, pos2, size):
        self.draw_binary_tree(v.D, pos1, size, v)
        self.draw_binary_tree(v.R, pos2, size, v)
    
    def add_entity(self, v):
        self.event_queue.append(("E", v))
        # self.entities.append(v)
    def clear_entities(self):
        self.event_queue.append(("C", None))
        # self.entities = []
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
                    self.handle_resize(event)
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
                            self.handle_text(text)
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            if len(self.event_queue) > 0:
                current_event = self.event_queue[0]
                self.event_queue.pop(0)

                if current_event[0] == "E":
                    self.entities.append(current_event[1])
                elif current_event[1] == "C":
                    self.entities = []

            # Fill the screen with a background color
            self.screen.fill(self.BACKGROUND_COLOUR)

            treesize = (self.screen_width//2,self.screen_height//2)
            # self.draw_binary_tree(antichain, (SCREEN_WIDTH//2, 50)/t, tree_size)
            for entity in self.entities:
                # draw tree pair
                self.draw_tree_pair(entity, (self.screen_width//4,50),(self.screen_width//4*3,50),(treesize[0]/2,treesize[1]))


            # pygame.draw.rect(screen, WHITE, pygame.Rect(SCREEN_WIDTH//2 - tree_size[0]//2, 50, tree_size[0], tree_size[1]), width = 1)

            # Draw the input box
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Render the text
            txt_surface = FONT.render(text, True, self.TEXT_COLOUR)

            # Calculate the position of the text
            text_x = input_box.x + 5
            text_y = input_box.y + 10

            # Blit the text onto the screen
            self.screen.blit(txt_surface, (text_x, text_y))
            # Update the screen
            pygame.display.flip()

        # Quit the program
        pygame.quit()
