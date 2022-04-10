import math
import numpy as np

def data_measurement(data):
    measurements = []
    Fre_SUM = 0
    fre_total = 0
    Tre_SUM = 0

    for x in range(len(data)):
        Tre_SUM = Tre_SUM + data[x][0]
        for y in range(len(data[x]) - 1):
            Fre_SUM = Fre_SUM + data[x][y+1]
            fre_total = fre_total + 1

    measurements.append(math.sqrt(Fre_SUM/fre_total))
    measurements.append(math.sqrt(Tre_SUM/len(data)))
    return measurements

def measure_FRE_TRE(CT_fiducials, US_fiducials, CT_Target, US_Target):
    squared_dist_array = []
    p1 = np.array([CT_Target[0], CT_Target[1], CT_Target[2]])
    p2 = np.array([US_Target[0], US_Target[1], US_Target[2]])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    squared_dist_array.append(squared_dist)
    for x in range(len(CT_fiducials)):
        p1 = np.array([CT_fiducials[x][0], CT_fiducials[x][1], CT_fiducials[x][2]])
        p2 = np.array([US_fiducials[x][0], US_fiducials[x][1], US_fiducials[x][2]])
        squared_dist = np.sum((p1-p2)**2, axis=0)
        squared_dist_array.append(squared_dist)
    return squared_dist_array
