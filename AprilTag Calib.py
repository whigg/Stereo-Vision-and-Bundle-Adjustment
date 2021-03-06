import os
import sys
import pyAprilTag
import numpy as np

CUR_DIR = os.getcwd()
LOG_DIR = os.path.join(CUR_DIR,'calib_log')
sys.path.insert(0, CUR_DIR) #otherwise importlib cannot find the path
if not os.path.exists(LOG_DIR) or len([f.endswith('.png') for f in os.listdir(LOG_DIR)]) < 2:
    os.makedirs(LOG_DIR)
    pyAprilTag.calib(pyAprilTag.calib_pattern_path,
                   'camera://{:d}'.format(0),
                   log_dir=LOG_DIR, nDistCoeffs=4)

import importlib
logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.py')])
if len(logs) == 0:
    print('no calibration log available!')
    exit(-1)

last_log = os.path.relpath(os.path.join(LOG_DIR, logs[-1])).replace(os.path.sep,'.')[:-3]
calib = importlib.import_module(last_log)
np.save("Data/K_external", calib.K)
np.save("Data/K_distCoeffs", calib.distCoeffs)
print('last log: '+last_log)
print('camera intrinsic matrix:')
print(calib.K)
print('camera distortion parameters:')
print(calib.distCoeffs)