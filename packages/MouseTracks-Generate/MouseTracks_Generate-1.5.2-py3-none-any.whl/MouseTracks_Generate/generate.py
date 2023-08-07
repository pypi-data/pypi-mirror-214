import pandas as pd
import os
import time
from keras.models import load_model
import numpy as np
from typing import List, Tuple
import pyautogui
import os
import random
import math
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'length_analysis.csv')
ana = pd.read_csv(file_path)
ana = ana.sort_values(by='distance')
y = ana['length'].values
x = ana['distance'].values
p = np.polyfit(x, y, 6)
fx = np.poly1d(p)


def get_length(startx ,starty, stopx, stopy):
    dx = abs(stopx - startx)
    dy = abs(stopy - starty)
    distance = int(math.sqrt(dx**2 + dy**2))
    length = int(fx(distance))
    length = random.randint(length-10, length+10)
    return length


def create_actions(startx, starty, stopx, stopy):
    length = get_length(startx, starty, stopx, stopy)

    x1 = startx
    x2 = stopx
    y1 = starty
    y2 = stopy
    n = min(length, 128)
    dx = (x2 - x1) / n
    dy = (y2 - y1) / n
    x = []
    y = []
    for i in range(0, n + 1):
        x.append(x1 + i * dx)
        y.append(y1 + i * dy)
    # x, y coordinates - integers
    x_int = [int(a) for a in x]
    y_int = [int(a) for a in y]

    dx_list = np.diff(x_int).tolist()
    dy_list = np.diff(y_int).tolist()

    dx_list.extend([0] * (128 - n))
    dy_list.extend([0] * (128 - n))

    d_list: List[int] = dx_list
    d_list.extend(dy_list)
    d_list = np.array(d_list)
    # d_list = pd.DataFrame(d_list, index=None)
    d_list = d_list.reshape(1, -1)
    return d_list, length
def change_rate(startx, starty, stopx, stopy, length, gener):
    df_generated = gener
    array = df_generated.iloc[0].values
    X1 = array[0:256]
    input_size = 128

    ############### recalculate x and y ###############

    dx1 = X1[0:input_size]
    dy1 = X1[input_size:2 * input_size]
    # trajectory original
    x1 = [startx]
    for j in dx1:
        x1.append(x1[-1] + j)
    y1 = [starty]
    for j in dy1:
        y1.append(y1[-1] + j)
    x1 = x1[0:length]
    y1 = y1[0:length]
    dx1 = dx1[0:length]
    dy1 = dy1[0:length]
    x1_end = x1[-1]
    y1_end = y1[-1]
    rate_x = (stopx - startx) / (x1_end - startx)
    rate_y = (stopy - starty) / (y1_end - starty)

    x = x1
    y = y1
    for k in range(length):
        x[k] = int((x1[k] - startx) * rate_x + startx)
        y[k] = int((y1[k] - starty) * rate_y + starty)

    ############### record x and y ###############

    # f_out = open('generated_actions/regener.csv', 'w')

    x_int = [int(a) for a in x]
    y_int = [int(a) for a in y]

    dx_list = np.array(x_int).tolist()
    dy_list = np.array(y_int).tolist()

    dx_list.extend([0] * (128 - length))
    dy_list.extend([0] * (128 - length))

    d_list: List[int] = dx_list
    d_list.extend(dy_list)
    # d_list = [str(e) for e in d_list]
    # f_out.write(",".join(d_list) + ' \n')
    d_list = np.array(d_list)
    # data = pd.DataFrame(d_list)
    # data.reshape(1, -1)
    # data.to_csv(f_out, index=False)
    return d_list

def setup_pyautogui():
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0.030  # Default: 0.1
    pyautogui.FAILSAFE = False

def move(points):

    data = points
    x = data[:128]
    y = data[128: 256]
    x = x.flatten().tolist()
    y = y.flatten().tolist()

    cord = list(zip(x, y))
    setup_pyautogui()
    zero_position = 0
    for i in range(128):
        if cord[i] == (0, 0):
            zero_position = i
            break
    spots = cord[0:zero_position]
    for spot in spots:
        pyautogui.moveTo(spot)
    pyautogui.click()

# OUTPUT_DIR = 'generated_actions'
MODEL_NAME = 'model2.h5'

point = Tuple[int, int]
points = List[point]
# List[Tuple[int, int]]
def generate_trace(endpoints: points):
    # load model
    current_dirr = os.path.dirname(__file__)
    file_path = os.path.join(current_dirr, MODEL_NAME)
    autoencoder = load_model(file_path, compile=False)
    steps = len(endpoints)
    for i in range(steps):
        startx, starty = pyautogui.position()
        stopx = endpoints[i][0]
        stopy = endpoints[i][1]
        array, length = create_actions(startx, starty, stopx, stopy)
        nsamples, nfeatures = array.shape  # 行数，列数
        # nfeatures = nfeatures - 1
        X = array[:, 0:nfeatures]
        X = X.reshape(-1, 128, 2)
        # generate actions using the autoencoder
        df_generated = autoencoder.predict(X)
        dim1, dim2, dim3 = df_generated.shape
        df_generated = df_generated.reshape(dim1, dim2 * dim3)
        df_generated = pd.DataFrame(data=df_generated)
        df_generated = df_generated.apply(np.round)
        # Fix negative zeros issue
        df_generated[df_generated == 0.] = 0.
        # filename = OUTPUT_DIR + "/gener.csv"
        # df_generated.to_csv(filename, index=False)
        regener = change_rate(startx, starty, stopx, stopy, length, df_generated)
        move(regener)




