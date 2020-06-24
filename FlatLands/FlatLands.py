# pygame and display setup
import os
import pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (460, 30)

pygame.init()
window = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('FlatLands')

# map setup
MAP_IMAGE = pygame.image.load('Assets/Map/map.jpg')
MAP_ARRAY = pygame.PixelArray(MAP_IMAGE)
Original_MAP = []
Variable_MAP = []
for x in range(len(MAP_ARRAY)):
    Original_MAP.append([])
    Variable_MAP.append([])
    for y in range(len(MAP_ARRAY[x])):
        color = list(pygame.Color(MAP_ARRAY[x][y]))
        del color[0]
        Original_MAP[x].append(color)
        Variable_MAP[x].append(color)
MAP_ARRAY.close()

# VARIABLES
Crafter_Selected = None
Map_Surface = pygame.Surface((20, 20))
MiniMap_Surface = pygame.Surface((3, 3))
camera = [100, 150]


# functions
def unpack():
    return eval(open("Content/SAVE").read()), eval(open("Content/NPC").read()), eval(
        open("Content/COLOR").read()), eval(open("Content/FONT").read()), eval(open("Assets/Skins/SKINS").read()), eval(
        open("Assets/Skins/CRAFTER").read())


SAVE_DICT, NPC_DICT, COLOR_DICT, FONT_DICT, SKIN_DICT, CRAFTER_DICT = unpack()


def save():
    f_save_dict = open("Content/SAVE", "w+")
    f_save_dict.write(str(SAVE_DICT))
    f_save_dict.flush()
    f_save_dict.close()


def skin(name):
    for style in name:
        Map_Surface.fill(style[0], style[1])


# setting icon using the skin function
skin(SKIN_DICT['Steve'])
# pygame.display.set_icon(Map_Surface)
pygame.display.set_icon(pygame.image.load('Assets/Icon/ICON.png'))


def layout_skin(section):
    for part in section:
        pygame.draw.rect(window, part[1], part[0], part[2])


def Map_load():
    for NonPlayable in NPC_DICT:
        skin(SKIN_DICT[NonPlayable])
        Variable_MAP[list(NPC_DICT[NonPlayable]['Locations'][NPC_DICT[NonPlayable]['Section']])[0]][
            list(NPC_DICT[NonPlayable]['Locations'][NPC_DICT[NonPlayable]['Section']])[1]] = SKIN_DICT[NonPlayable]
    for X in range(50):
        for Y in range(50):
            if type(Variable_MAP[X + camera[0]][Y + camera[1]]) == tuple:
                for SKIN in SKIN_DICT:
                    if Variable_MAP[X + camera[0]][Y + camera[1]] == SKIN_DICT[SKIN]:
                        skin(SKIN_DICT[SKIN])
            else:
                Map_Surface.fill(Variable_MAP[X + camera[0]][Y + camera[1]])
            window.blit(Map_Surface, (X * 20, Y * 20))


def Minimap_Load():
    for X in range(50):
        for Y in range(50):
            if type(Variable_MAP[X + camera[0]][Y + camera[1]]) == tuple:
                for SKIN in SKIN_DICT:
                    if Variable_MAP[X + camera[0]][Y + camera[1]] == SKIN_DICT[SKIN]:
                        MiniMap_Surface.fill(Variable_MAP[X + camera[0]][Y + camera[1]][0][0])
            else:
                MiniMap_Surface.fill(Variable_MAP[X + camera[0]][Y + camera[1]])
            window.blit(MiniMap_Surface, (X * 3, Y * 3))
    pygame.draw.rect(window, (0, 0, 0), (0, 0, 150, 150), 3)


def wall(XD=0, YD=0):
    return not Variable_MAP[camera[0] + 25 + steve.XO + XD][camera[1] + 25 + steve.YO + YD] in (COLOR_DICT['WALLS'])


def NPC():
    for Nearest_NPC in NPC_DICT:
        location = Variable_MAP[list(NPC_DICT[Nearest_NPC]['Locations'][NPC_DICT[Nearest_NPC]['Section']])[0]][
            list(NPC_DICT[Nearest_NPC]['Locations'][NPC_DICT[Nearest_NPC]['Section']])[1]]
        if Variable_MAP[camera[0] + 25 + steve.XO + 1][camera[1] + 25 + steve.YO] == location or \
                Variable_MAP[camera[0] + 25 + steve.XO - 1][camera[1] + 25 + steve.YO] == location or \
                Variable_MAP[camera[0] + 25 + steve.XO][camera[1] + 25 + steve.YO + 1] == location or \
                Variable_MAP[camera[0] + 25 + steve.XO][camera[1] + 25 + steve.YO - 1] == location:
            return True, Nearest_NPC
    else:
        return False, None


def TEXT(font, text, location, boxed=False, text_color=(0, 0, 0)):
    if boxed:
        text_color = (255, 255, 255)
    if '\n' not in text:
        content = font.render(text, True, text_color)
        rect = content.get_rect(center=location)
        if boxed:
            pygame.draw.rect(window, (128, 128, 128),
                             (rect[0] - rect[3] // 4, rect[1] - rect[3] // 3, rect[2] + rect[3] // 2, rect[3] * 1.5))
        window.blit(content, (rect[0], rect[1]))
    else:
        lines = text.splitlines()
        for segment, line in enumerate(lines):
            content = font.render(line, True, color)
            rect = content.get_rect(center=(location[0], location[1] + 25 * segment))
            window.blit(content, rect)


def E_load():
    if NPC_DICT[NPC()[1]]['Requirements'][NPC_DICT[NPC()[1]]['Section']][0] is not None:
        if NPC_DICT[NPC_DICT[NPC()[1]]['Requirements'][NPC_DICT[NPC()[1]]['Section']][0]]['Completed'][
            NPC_DICT[NPC()[1]]['Section']]:
            TEXT(FONT_DICT['keybox'], 'E', (500 + steve.XO * 20, 500 + steve.YO * 20 - 50), True)
    else:
        TEXT(FONT_DICT['keybox'], 'E', (500 + steve.XO * 20, 500 + steve.YO * 20 - 50), True)


def interact(NPC_NAME):
    TEXT(FONT_DICT['chatbox'], NPC_DICT[NPC_NAME][NPC_DICT[NPC_NAME]['Section']][NPC_DICT[NPC_NAME]['Part']],
         (500, 900), True)


def crafter():
    if Crafter_Selected is None:
        layout_skin(CRAFTER_DICT['Basic Layout'])


def Quest_Load():
    cnt = 0
    for npc in NPC_DICT:
        if NPC_DICT[npc]['Quest'] is not None:
            TEXT(FONT_DICT['quests'], 'QUESTS', (900, 25), False, (255, 255, 0))
            TEXT(FONT_DICT['quests'], NPC_DICT[npc]['Quests'][NPC_DICT[npc]['Quest']], (900, 50 + 80 * cnt))
        cnt += 1


# classes
class player:
    def __init__(self, XO, YO, interacting=False, crafting=False, movable=False, interacting_with=None):
        self.XO = XO
        self.YO = YO
        self.interacting = interacting
        self.crafting = crafting
        self.movable = movable
        self.interacting_with = interacting_with

    def load(self):
        skin(SKIN_DICT['Steve'])
        window.blit(Map_Surface, (500 + self.XO * 20, 500 + self.YO * 20))
        MiniMap_Surface.fill((0, 255, 0))
        window.blit(MiniMap_Surface, (75 + self.XO * 3, 75 + self.YO * 3))


steve = player(0, 0)

# main
run = True
while run:
    # detection
    steve.movable = True
    if steve.interacting or steve.crafting:
        steve.movable = False

    # draw out the visuals
    if not steve.crafting:
        Map_load()
        Minimap_Load()
        steve.load()
    else:
        crafter()
    if NPC()[0]:
        E_load()
        if steve.interacting:
            interact(NPC()[1])
    Quest_Load()
    pygame.display.flip()

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # KEY EVENTS
        if event.type == pygame.KEYDOWN:

            # interacting and crafting
            if event.key == pygame.K_e:
                if NPC()[0]:
                    if steve.interacting:
                        NPC_DICT[NPC()[1]]['Part'] += 1
                        if len(NPC_DICT[NPC()[1]][NPC_DICT[NPC()[1]]['Section']]) == NPC_DICT[NPC()[1]]['Part']:
                            NPC_DICT[NPC()[1]]['Part'] -= 1
                            NPC_DICT[NPC()[1]]['Quest'] = NPC_DICT[NPC()[1]]['Section']
                            steve.interacting = False
                    elif NPC_DICT[NPC()[1]]['Requirements'][NPC_DICT[NPC()[1]]['Section']][0] is not None:
                        if NPC_DICT[NPC_DICT[NPC()[1]]['Requirements'][NPC_DICT[NPC()[1]]['Section']][0]][
                            'Completed'][NPC_DICT[NPC()[1]]['Section']]:
                            steve.interacting = True
                    else:
                        steve.interacting = True
                else:
                    steve.crafting = not steve.crafting

            # moving
            elif steve.movable:
                if event.key == pygame.K_a:
                    if steve.XO > 0 and wall(-1, 0):
                        steve.XO -= 1
                    elif camera[0] > 0 and wall(-1, 0):
                        camera[0] -= 1
                    else:
                        if steve.XO > -25 and wall(-1, 0):
                            steve.XO -= 1
                if event.key == pygame.K_d:
                    if steve.XO < 0 and wall(1, 0):
                        steve.XO += 1
                    elif camera[0] < 200 and wall(1, 0):
                        camera[0] += 1
                    else:
                        if steve.XO < 24 and wall(1, 0):
                            steve.XO += 1
                if event.key == pygame.K_w:
                    if steve.YO > 0 and wall(0, -1):
                        steve.YO -= 1
                    elif camera[1] > 0 and wall(0, -1):
                        camera[1] -= 1
                    else:
                        if steve.YO > -25 and wall(0, -1):
                            steve.YO -= 1
                if event.key == pygame.K_s:
                    if steve.YO < 0 and wall(0, 1):
                        steve.YO += 1
                    elif camera[1] < 200 and wall(0, 1):
                        camera[1] += 1
                    else:
                        if steve.YO < 24 and wall(0, 1):
                            steve.YO += 1

# save
# save()

# quit
pygame.quit()
