import argparse
import numpy as np
import os
import sys

from mykit.app import App
from mykit.kit.path import SafeJSON
from mykit.kit.utils import printer

from main.draw_pad import DrawPad, width as draw_pad_width
from main.dataset import Dataset
from main.dense import Dense

from main.diagram import (
    NetworkDiagram,
    Interface as DiagramAPI
)
from main.datasets import (
    Interface as DatasetsAPI
)
from main.datasets import (
    Interface as DatasetsAPI
)

from main.register_buttons import register_buttons
from main.constants import SOFTWARE_NAME, SOFTWARE_VER, SAVED_NETWORK_DIR_PTH


class Runtime:
    realtime = False
    clarity = False



draw_pad = DrawPad(app.page, 15, (app.page.winfo_reqheight() - 64*4)//2)
dataset = Dataset(app.page)

## <neural network>
if NN_NEW:
    weights = None
    biases = None
    metadata = None
else:

    printer('Loading the saved network.')
    weights = SafeJSON.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'weights.json'))
    weights = [np.array(w) for w in weights]

    biases = SafeJSON.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'biases.json'))
    biases = [np.array(b) for b in biases]

    metadata = SafeJSON.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'metadata.json'))
    printer(f'Using network with {metadata["n_learn"]} total learns.')

nn = Dense(sizes=NN_SIZES, weights=weights, biases=biases, metadata=metadata)
## </neural network>

NETWORK_DIAGRAM_WIDTH = 750
NETWORK_DIAGRAM_HEIGHT = 750
NETWORK_DIAGRAM_TL_X = draw_pad.tl_x + draw_pad_width + 10
NETWORK_DIAGRAM_TL_Y = (app.page.winfo_reqheight() - NETWORK_DIAGRAM_HEIGHT)*0.5
network_diagram = NetworkDiagram(
    app.page, nn,
    NETWORK_DIAGRAM_WIDTH, NETWORK_DIAGRAM_HEIGHT,
    NETWORK_DIAGRAM_TL_X, NETWORK_DIAGRAM_TL_Y,
)

graph = Graph(
    app.page, nn,
    NETWORK_DIAGRAM_WIDTH, NETWORK_DIAGRAM_HEIGHT,
    NETWORK_DIAGRAM_TL_X, NETWORK_DIAGRAM_TL_Y,
)

output_box = OutputBox(
    app.page,
    310,
    app.page.winfo_reqheight()*0.15,
    NETWORK_DIAGRAM_TL_X + NETWORK_DIAGRAM_WIDTH + 10,
    (app.page.winfo_reqheight() - app.page.winfo_reqheight()*0.15)*0.5,
)


def show_result():

    inputs_vectorized = np.round(draw_pad.get_img_raw()/255, 2).ravel().reshape((-1, 1))
    nn.feedforward(inputs_vectorized)

    network_diagram.recolor()
    output_box.tell(nn.decision)


def left_mouse_press_and_hold_callback(e):
    if draw_pad.paint() and Runtime.realtime:
        show_result()
app.listen(to='left-mouse-press', do=left_mouse_press_and_hold_callback)
app.listen(to='left-mouse-hold', do=left_mouse_press_and_hold_callback)


register_buttons(
    NN_DATASET_RATIO,
    NN_N_EPOCH,
    NN_SAMPLE_SIZE,
    NN_LEARNING_RATE,
    NN_REGULARIZATION,
    NN_EARLY_STOP_AFTER,
    Runtime,
    app.root,
    app.page,
    draw_pad,
    dataset,
    nn,
    network_diagram,
    graph,
    output_box,
    show_result
)

def core():

        app = App(f'{SOFTWARE_NAME}_v{SOFTWARE_VER}', '#131313')


        DiagramAPI()


        app.run()



def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['run', 'settings'], help='Specify the command')
    args = parser.parse_args()

    if args.cmd == 'run':
        core()

    elif args.cmd == 'settings':

        printer('INFO: Opening the settings file and then exit.')
        sys.exit(0)


def layout():
    pass

