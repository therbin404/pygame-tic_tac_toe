import sys, pygame

# on doit init tous les composants pygame
pygame.init()

##### SCREEN AND MAP DEFINITION #####
WHITE = 255, 255, 255
BLACK = 0, 0, 0
size = width, height = 1281, 720
screen = pygame.display.set_mode(size)

border_width = 2
square_length = 240
square_height = int(height / 3)
square_size = square_length, square_height

state_screen_width = (width - square_length * 3) // 2 + square_length * 3

# coordonnées de départ de chaque case
ttt_map = [
    [0, 0],
    [square_length, 0],
    [square_length * 2, 0],
    [0, square_height],
    [square_length, square_height],
    [square_length * 2, square_height],
    [0, square_height * 2],
    [square_length, square_height * 2],
    [square_length * 2, square_height * 2],
]
# played map, filled with 'x' or 'o'
# first three elements are the first line, next three are second, ...
played_map = ["", "", "", "", "", "", "", "", ""]

right_borders = [0, 1, 3, 4, 6, 7]
bottom_borders = [0, 1, 2, 3, 4, 5]

font = pygame.font.Font("freesansbold.ttf", 32)
font_52 = pygame.font.Font("freesansbold.ttf", 52)
###############


##### GAME DEFINITION #####
players = ["x", "o"]
finished_game = False
player_1_text = font.render(players[0], True, BLACK)
player_1_text_rect = player_1_text.get_rect()
player_2_text = font.render(players[1], True, BLACK)
player_2_text_rect = player_2_text.get_rect()

game_state_text = font.render("", True, BLACK)

retry_button = font_52.render("RETRY", True, BLACK)
retry_button_rect = retry_button.get_rect()
retry_button_rect.x = state_screen_width - retry_button_rect.width // 2
retry_button_rect.y = square_height * 2

# index des combinaisons gagnantes
win_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]
###############


def reset_map(pos):
    if (
        retry_button_rect.left < pos[0] < retry_button_rect.right
        and retry_button_rect.top < pos[1] < retry_button_rect.bottom
    ):
        return True
    return False


def update_game_state_text(text_to_display):
    game_state_text = font.render(text_to_display, True, BLACK)
    game_state_text_rect = game_state_text.get_rect()
    game_state_text_rect.x = state_screen_width - game_state_text_rect.width // 2
    game_state_text_rect.y = square_height
    # fill only game state rec, not the entire map !
    # +5 au height pour cacher ce qui dépasserait éventuellement (p, y, j, ...)
    screen.fill(
        WHITE,
        (
            square_length * 3,
            game_state_text_rect.y,
            state_screen_width,
            game_state_text_rect.height + 5,
        ),
    )
    screen.blit(game_state_text, game_state_text_rect)


def check_win():
    for combination in win_combinations:
        first_result = played_map[combination[0]]
        second_result = played_map[combination[1]]
        third_result = played_map[combination[2]]
        if (first_result == second_result == third_result) and first_result:
            return first_result
    return False


def draw_move(index):
    cell = ttt_map[index]
    # on calcule la position x et y pour qu'elle soit centrée dans la case
    # on calcule le texte du joueur qui doit être affiché
    if player == players[0]:
        player_1_text_rect.x = (
            cell[0] + square_length // 2 - player_1_text_rect.width // 2
        )
        player_1_text_rect.y = (
            cell[1] + square_height // 2 - player_1_text_rect.height // 2
        )
        text = player_1_text
        textRect = player_1_text_rect
    else:
        player_2_text_rect.x = (
            cell[0] + square_length // 2 - player_2_text_rect.width // 2
        )
        player_2_text_rect.y = (
            cell[1] + square_height // 2 - player_2_text_rect.height // 2
        )
        text = player_2_text
        textRect = player_2_text_rect
    screen.blit(text, textRect)


def check_map(pos, player):
    for index, cell in enumerate(ttt_map):
        # pos[0] = x
        # pos[1] = y
        coordinates_x = [cell[0], cell[0] + cell[2]]
        coordinates_y = [cell[1], cell[1] + cell[3]]
        # on va chercher à savoir dans quelle case la position retournée par le click se situe sur la map
        # et surtout, si cette case n'est pas jouée
        if (
            coordinates_x[0] < pos[0] < coordinates_x[1]
            and coordinates_y[0] < pos[1] < coordinates_y[1]
            and not played_map[index]
        ):
            played_map[index] = player
            draw_move(index)
            return True
    return False


##### GENERATION INITIALE DE L'ECRAN #####

# fill entire screen whith white
screen.fill(WHITE)
# except for map background, to let borders appear
pygame.draw.rect(screen, BLACK, (0, 0, square_length * 3, square_height * 3))

# GENERATION DE LA MAP
for index, cell in enumerate(ttt_map):
    # pour draw, on a besoin du x,y de départ, et de la longueur/hauteur de l'élément
    # la longueur/hauteur ne variant jamais, on l'ajoute ici
    cell.append(square_length)
    cell.append(square_height)
    # on retire 2 px du draw, pour générer un espace noir, et donc afficher une grille
    # on veut des borders uniquement au centre, et non sur les contours
    # on evite donc de retirer des pixels aux bords droits des cases les plus à droite
    if index in right_borders:
        cell[2] -= border_width
    # idem pour les bords du dessous
    if index in bottom_borders:
        cell[3] -= border_width
    pygame.draw.rect(screen, WHITE, cell)

# INITIALISATION DE LA PARTIE
player = players[0]
update_game_state_text("{} plays !".format(player))
screen.blit(retry_button, retry_button_rect)
pygame.display.flip()

while 1:
    # ici on va attendre qu'un event ait lieu
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        sys.exit()
    if e.type == pygame.MOUSEBUTTONDOWN:
        if reset_map(e.pos):
            # reset cells
            for cell in ttt_map:
                screen.fill(
                    WHITE,
                    (
                        cell[0],
                        cell[1],
                        cell[2],
                        cell[3],
                    ),
                )
            # reinit all game values
            played_map = ["", "", "", "", "", "", "", "", ""]
            update_game_state_text("{} plays !".format(player))
            finished_game = False
            pygame.display.update()

        if check_map(e.pos, player) and not finished_game:
            # On a joué le coup, on change de joueur
            player = players[1] if player == players[0] else players[0]
            update_game_state_text("{} plays !".format(player))

            winner = check_win()
            if winner:
                update_game_state_text("{} wins !".format(winner))
                finished_game = True
            elif not winner and len(list(filter(None, played_map))) == 9:
                update_game_state_text("No one wins.".format(winner))
                finished_game = True

            pygame.display.update()
