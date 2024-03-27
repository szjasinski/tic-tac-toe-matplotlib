# Szymon Jasinski
# Tic Tac Toe

from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import random
import copy


size = 3
colors = {'player': "#f49c37", 'computer': '#db3069', 'outer_bg': "#1446a0", 'inner_bg': '#b9d6f2', 'win_bg': "#ade79c"}

GAME_STATE = [[False for i in range(size)] for j in range(size)]
possible_moves = [(i, j) for i in range(size) for j in range(size)]

player_shape = input("Please enter 'o' or 'x' as your shape:) ")
computer_shape = {'o': 'x', 'x': 'o'}[player_shape]

fig, axarray = plt.subplots(size, size, figsize=(8, 8), facecolor=colors['outer_bg'])
fig.canvas.manager.set_window_title('Tic Tac Toe')

for ax in fig.axes:
    ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
    ax.set_facecolor(colors['inner_bg'])

plt.setp(axarray, xlim=(0, 1), ylim=(0, 1))
plt.tight_layout(pad=1.3)

# define restart_ax after calling plt.tight_layout to prevent UserWarning
restart_ax = fig.add_axes([0.93, 0, 0.07, 0.03])
restart_ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)


def restart_game(event):

    possible_moves.clear()
    for i in range(size):
        for j in range(size):
            GAME_STATE[i][j] = False
            possible_moves.append((i, j))

    # clear shapes, but not "Restart" text on a button
    for i, ax in enumerate(fig.axes):
        if i != size**2:
            ax.set_facecolor(colors['inner_bg'])
            ax.clear()

    # plt.setp() again to prevent weird 'x' shape formatting
    plt.setp(axarray, xlim=(0, 1), ylim=(0, 1))
    fig.canvas.draw()
    print("restarting game...")

    if computer_shape == 'o':
        move_computer()


def draw_shape(ax, shape, color):
    if shape == "o":
        ax.add_patch(plt.Circle((0.5, 0.5), 0.3, linewidth=13, fill=False, color=color))
    elif shape == "x":
        ax.plot([0.2, 0.8], [0.2, 0.8], linewidth=13, solid_capstyle='round', color=color)
        ax.plot([0.2, 0.8], [0.8, 0.2], linewidth=13, solid_capstyle='round', color=color)
    fig.canvas.draw()


def move_player(i, j):
    draw_shape(axarray[i][j], player_shape, colors['player'])
    GAME_STATE[i][j] = player_shape
    possible_moves.remove((i, j))


def move_computer():
    # COMPUTER STRATEGY - pick winning move, elif pick move that prevents player to win, else pick random possible move
    # (the only way to win with computer is to have two winning moves at the same time)
    if len(possible_moves) > 0:

        # make random possible move
        move = random.choice(possible_moves)

        # check if there is a winning move or a move that prevents player to win
        for i, j in possible_moves:
            new_game_state = copy.deepcopy(GAME_STATE)
            new_game_state[i][j] = computer_shape
            if game_over(new_game_state):
                move = (i, j)
                break
            new_game_state[i][j] = player_shape
            if game_over(new_game_state):
                move = (i, j)

        i, j = move[0], move[1]

        draw_shape(axarray[i][j], computer_shape, colors['computer'])
        GAME_STATE[i][j] = computer_shape
        possible_moves.remove((i, j))


def game_over(game_state=None):
    if game_state is None:
        game_state = GAME_STATE
    winning_squares = None

    # horizontal check
    for row in game_state:
        if row[0] and len(set(row)) == 1:
            winning_squares = [(game_state.index(row), i) for i in range(size)]

    # vertical check
    for col in range(size):
        if game_state[0][col] and len(set([game_state[i][col] for i in range(size)])) == 1:
            winning_squares = [(i, col) for i in range(size)]

    # diagonal checks
    if game_state[0][0] and len(set([game_state[i][i] for i in range(size)])) == 1:
        winning_squares = [(i, i) for i in range(size)]

    elif game_state[size - 1][0] and len(set([game_state[size - 1 - i][i] for i in range(size)])) == 1:
        winning_squares = [(size - 1 - i, i) for i in range(size)]

    return winning_squares


def highlight_winner():
    winning_squares = game_over()
    if winning_squares:
        for i, j in winning_squares:
            axarray[i][j].set_facecolor(colors['win_bg'])
        fig.canvas.draw()


def onclick(event):
    if event.inaxes is None:
        return None

    num = fig.axes.index(event.inaxes)
    i, j = num // size, num % size

    if (i, j) in possible_moves:
        if not game_over():
            move_player(i, j)
            highlight_winner()

        if not game_over():
            move_computer()
            highlight_winner()


if computer_shape == 'o':
    move_computer()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

restart_button = Button(restart_ax, 'Restart')
restart_button.on_clicked(restart_game)

plt.show()
