import math
import numba as nb
import numpy as np
import tkinter as tk

from mykit.app.label import Label
from mykit.kit.color import getgray, rgb_to_hex, interpolate_with_black
from mykit.kit.utils import printer

from main.dense import Dense
from main.runtime import Runtime as GlobalRt


"""

Reminder
========

- Weight-lines are not created using the normal `tkinter.Canvas.create_line`
  function. Instead, they will be created using the Bresenham line
  algorithm and drawn on a raw screen matrix. This matrix will then
  be rendered as a single image using `tkinter.PhotoImage`.

- The neurons are created normally using the `tkinter.Canvas.create_oval` function.

- Basically, there are two things: the rendered-weight-lines-image
  and the neuron-ovals. The z-order needs careful management to
  keep the neuron-circles on top of the weight-lines-image during redrawing.

"""


## local runtime
class Rt:
    
    ## the app's page
    page: tk.Canvas = None

    ## raw screen
    screen = None

    ## lines
    lines_map = {}

    ## holder
    tk_img = None


def make():

    printer('INFO: Making the linemaps')

    ## screen's geo
    TL_X = 10
    TL_Y = 10
    WIDTH = 500
    HEIGHT = 750

    LAYERS = [100, 50, 40, 35, 36]

    ## registering lines map
    for i in range(len(LAYERS)):

        l1 = LAYERS[i]    # current layer
        l2 = LAYERS[i+1]  # next layer

        H = (l1-1)*NEURON_PAD_Y[i]    # total height of current layer
        X1 = sum(NEURON_PAD_X[:i+1])  # x-position of the top neuron in current layer (must be an integer)
        Y1 = round((HEIGHT-H)/2)      # y-position of the top neuron in current layer (must be an integer)

        H = (l2-1)*NEURON_PAD_Y[i+1]    # total height of current layer
        X2 = sum(NEURON_PAD_X[:i+1+1])  # x-position of the top neuron in the next layer (must be an integer)
        Y2 = round((HEIGHT-H)/2)        # y-position of the top neuron in the next layer (must be an integer)

        for j in range(l1):
            for k in range(l2):

                y1 = Y1 + NEURON_PAD_Y[i]*j    # y-position of the neuron in current layer
                y2 = Y2 + NEURON_PAD_Y[i+1]*k  # y-position of the neuron in the next layer

                ## for each weight (uniquely identified by i, j, and k) has its own line coordinate to draw them on raw scren
                Rt.lines_map[(i, k, j)] = (X1, y1, X2, y2)
make()


@nb.njit
def line_overlay(screen: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: np.ndarray):
    """color: if red -> (255, 0, 0) or [255, 0, 0] or np.array([255, 0, 0])"""

    dx = x1 - x0
    dy = y1 - y0

    ## direction
    _x = 1 if dx > 0 else -1
    _y = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = _x, 0, 0, _y
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, _y, _x, 0
    
    ## optimization purposes
    dx2 = 2*dx
    dy2 = 2*dy

    d = dy2 - dx
    y = 0

    for x in range(dx + 1):

        screen[y0 + x*xy + y*yy, x0 + x*xx + y*yx] = color
        if d >= 0:
            y += 1
            d -= dx2
        d += dy2


class Interface:

    def recolor_neuron(layer: int, idx: int):
        """
        ## Params
        - `layer`: the index of the layer (starts from 0, which is the input layer)
        - `idx`: the index of the neuron (starts from 0) in the layer `layer`
        """
        pass

    def recolor_weight(layer: int, idx: int, idx2: int):
        """
        ## Params
        - `layer`: the index of the layer (starts from 0, which is the input layer)
        - `idx`: the index of the neuron (starts from 0) in the layer `layer`
        - `idx2`: the index of the neuron (starts from 0) in the next layer (`layer+1`)
        """
    
    def _delete():
        """reminder: can be used to forcefully hide the diagram"""
        Rt.page.delete('Diagram')

    def _draw():
        pass
    
    def redraw():

        Interface._delete()
        Interface._draw()






## [from left edge, input to 1st-hidden, 1st to 2nd-hidden, ..., last-hidden to output]
NEURON_PAD_X = [40, 230, 120, 120, 150]
## [input, 1st-hidden, 2nd-hidden, ..., last-hidden, output]
NEURON_PAD_Y = [6, 14, 14, 14, 20]
NEURON_RADIUS = [3, 5, 5, 5, 6]
NEURON_MAX_LUM = 250
NEURON_BD_WIDTH = [1, 1, 1, 1, 1]
NEURON_BD_COLOR = ['#f5f5f5', '#fafbfa', '#fafbfa', '#fafbfa', '#f5f5f5']

COLOR_POSITIVE = np.array((200, 40, 10))
COLOR_NEGATIVE = np.array((9, 130, 211))
COLOR_DESICION = '#4fc778'

WEIGHT_MIN_ALPHA = 0.1

## optimization purposes
SHOWN_INPUT_NEURON_RATIO = 0.55  # if 0.75 -> only show 3/4 of the input-neurons (where the span location on `draw_pad` is as center as possible)
SHOWN_INPUT_NEURON_SCALE = 0.30  # if 0.75 -> only show 3/4 of the span, (3/4)^2 of all input-neurons
SHOWN_HIDDEN_NEURON_RATIO = 1  # if 0.5 -> only show the half of hidden neurons at each hidden layer
THRESHOLD = [0.1, 0.1, 0.1, 0.1, 0.005]  # only redraw if the change is significant


color_positive_in_hex = rgb_to_hex(*COLOR_POSITIVE)
color_negative_in_hex = rgb_to_hex(*COLOR_NEGATIVE)



class Weights:
    """for optimization purposes, the weight-lines represented as an image."""

    tk_img = None

    def __init__(self, page: tk.Canvas, nn: Dense, width, height, tl_x, tl_y):

        self.page = page
        self.nn = nn
        self.width = width
        self.height = height
        self.tl_x = tl_x
        self.tl_y = tl_y

        self.screen = np.zeros((self.height, self.width, 3))
        self.lines = {}
        self.ppm_header = f'P6 {self.width} {self.height} 255 '.encode()

        for i in range(nn.n_layer - 1):

            l1 = NetworkDiagram.shown_neurons[i]
            l2 = NetworkDiagram.shown_neurons[i+1]

            H = (len(l1) - 1)*NEURON_PAD_Y[i]
            X1 = sum(NEURON_PAD_X[:i+1])
            Y1 = round((self.height - H)*0.5)

            H = (len(l2) - 1)*NEURON_PAD_Y[i+1]
            X2 = sum(NEURON_PAD_X[:i+1+1])
            Y2 = round((self.height - H)*0.5)

            for j, idx1 in enumerate(l1.keys()):
                for k, idx2 in enumerate(l2.keys()):

                    y1 = Y1 + NEURON_PAD_Y[i]*j
                    y2 = Y2 + NEURON_PAD_Y[i+1]*k

                    if nn.weights[i][idx2, idx1] >= 0:
                        line_overlay(self.screen, X1, y1, X2, y2, COLOR_POSITIVE*WEIGHT_MIN_ALPHA)
                    else:
                        line_overlay(self.screen, X1, y1, X2, y2, COLOR_NEGATIVE*WEIGHT_MIN_ALPHA)

                    self.lines[(i, idx2, idx1)] = (X1, y1, X2, y2)

        self.altered = True
        self.redraw()

    def alter_weight(self, i, j, k, src):
        """src: the activation value of the neuron that feeds the weight-line, with interval: [-1, 1]"""

        if self.nn.weights[i][j, k] >= 0:
            line_overlay(self.screen, *self.lines[(i, j, k)], COLOR_POSITIVE*abs(src))
        else:
            line_overlay(self.screen, *self.lines[(i, j, k)], COLOR_NEGATIVE*abs(src))
        
        self.altered = True

    def redraw(self):
        if self.altered:
            ppm = self.ppm_header + self.screen.astype(np.uint8).tobytes()
            Weights.tk_img = tk.PhotoImage(width=self.width, height=self.height, data=ppm, format='PPM')
            self.page.delete('weights')
            self.page.create_image(self.tl_x, self.tl_y, image=Weights.tk_img, anchor='nw', tags='weights')
            self.page.tag_lower('weights')
            self.altered = False


class NetworkDiagram:

    shown_neurons = None
    decision = None  # the last decision

    def optimize(self):
        """
        selecting the shown input neurons, weight-lines, and hidden neurons.
        also store their previous values.
        """

        grid = int(math.sqrt(self.nn.n_input))

        span = round(grid*SHOWN_INPUT_NEURON_RATIO)
        skip = round((grid - span)/2)  # skip the first `skip` rows and columns

        area = np.linspace(skip, skip + span - 1, round(span*SHOWN_INPUT_NEURON_SCALE)).astype(int).tolist()

        input_neurons = {}
        for row in area:
            for column in area:
                input_neurons[row + column*grid] = 0

        hidden_neurons = []
        for n in self.nn.hidden_layers:
            hidden_neurons.append({i: 0 for i in np.linspace(0, n - 1, round(n*SHOWN_HIDDEN_NEURON_RATIO)).astype(int).tolist()})

        NetworkDiagram.shown_neurons = [input_neurons, *hidden_neurons, {i: 0 for i in range(self.nn.n_output)}]

        printer(f'#shown neurons: {[len(i) for i in NetworkDiagram.shown_neurons]}')

    def __init__(self, page: tk.Canvas, nn: Dense, width, height, tl_x, tl_y) -> None:
        """
        width, height: of the diagram (border is excluded).
        tl_x, tl_y: top-left of the diagram (not the diagram border).
        """

        self.page = page
        self.nn = nn

        page.create_rectangle(
            tl_x - 1, tl_y - 1,
            tl_x + width, tl_y + height,
            width=1, outline=THEME_BORDER_COLOR
        )

        self.optimize()

        printer('Weight-lines initialization..')
        self.weights = Weights(page, nn, width, height, tl_x, tl_y)
        printer('Weight-lines created.')

        for i, neuron_values in enumerate(NetworkDiagram.shown_neurons):

            H = (len(neuron_values) - 1)*NEURON_PAD_Y[i]
            X = tl_x + sum(NEURON_PAD_X[:i+1])
            Y = tl_y + (height - H)*0.5
            
            for j, neuron_idx in enumerate(neuron_values.keys()):

                page.create_oval(
                    X - NEURON_RADIUS[i],
                    Y + NEURON_PAD_Y[i]*j - NEURON_RADIUS[i],
                    X + NEURON_RADIUS[i],
                    Y + NEURON_PAD_Y[i]*j + NEURON_RADIUS[i],
                    fill='#000000',
                    width=NEURON_BD_WIDTH[i],
                    outline=NEURON_BD_COLOR[i],
                    tags=f'neuron_{i}_{neuron_idx}'
                )

                if i == (nn.n_layer - 1):
                    Label(
                        id=f'output_label_{j}', x=X+18, y=Y+NEURON_PAD_Y[i]*j,
                        text='0123456789abcdefghijklmnopqrstuvwxyz'[j],
                        font='Consolas 10', anchor='w',
                        fg='#dbe8fc', bg='#000000',
                        tags=['nd', 'train']
                    )
                    Label(
                        id=f'output_value_{j}', x=X+28, y=Y+NEURON_PAD_Y[i]*j,
                        text=': 0.00',
                        font='Consolas 10', anchor='w',
                        fg='#dbe8fc', bg='#000000',
                        tags=('clarity', 'nd', 'train')
                    )

    def recolor(self):
        """after feedforwarding"""

        for i, neuron_values in enumerate(NetworkDiagram.shown_neurons):
            for neuron_idx, neuron_value in neuron_values.items():

                new = self.nn.a_values[i][neuron_idx, 0]
                if abs(new - neuron_value) > THRESHOLD[i]:

                    NetworkDiagram.shown_neurons[i][neuron_idx] = new

                    if i in {0, self.nn.n_layer - 1}:
                        self.page.itemconfigure(f'neuron_{i}_{neuron_idx}', fill=getgray(new, NEURON_MAX_LUM))
                    else:
                        if new >= 0:
                            color = interpolate_with_black(color_positive_in_hex, new)
                        else:
                            color = interpolate_with_black(color_negative_in_hex, -new)

                        self.page.itemconfigure(f'neuron_{i}_{neuron_idx}', fill=color)

                    if i < (self.nn.n_layer - 1):
                        for neuron_idx2 in NetworkDiagram.shown_neurons[i+1].keys():
                            self.weights.alter_weight(i, neuron_idx2, neuron_idx, new)

                    if i == (self.nn.n_layer - 1):
                        Label.set_text_by_id(f'output_value_{neuron_idx}', f': {new:.2f}')

        if NetworkDiagram.decision is None:
            self.page.itemconfigure(f'neuron_{i}_{self.nn.decision}', outline=COLOR_DESICION)
            NetworkDiagram.decision = self.nn.decision
        else:
            if self.nn.decision != NetworkDiagram.decision:
                self.page.itemconfigure(f'neuron_{i}_{NetworkDiagram.decision}', outline=NEURON_BD_COLOR[i])
                self.page.itemconfigure(f'neuron_{i}_{self.nn.decision}', outline=COLOR_DESICION)
                NetworkDiagram.decision = self.nn.decision

        self.weights.redraw()