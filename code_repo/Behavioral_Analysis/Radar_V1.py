import os
import numpy as np
import matplotlib.pyplot as plt
from statisticsAnalysisV3 import height_pipline_processing, get_amplitude, amplitude_pipline_processing, create_dict
from angleOscillation import oscillation_pipline_processing, sa_read_csv
import pandas as pd
import seaborn as sns
import palettable


def average(ls: list):
    sum = 0
    for i in ls:
        sum += i
    return sum / len(ls)


def standardize_processing(path_dict: dict, param_dicts: dict, angle_flag=False):
    if isinstance(path_dict, dict) and isinstance(param_dicts, dict):
        header, names = param_dicts["header"], param_dicts["names"]
        raw_data_path = {"intact":[],"control":[],"ROS":[],"DOPA":[],"GABA":[]}
        for i, vals in enumerate(list(path_dict.keys())):
            for j in range(len(path_dict[vals])):
                raw_data = sa_read_csv(path=path_dict[vals][j], header=header, names=names).astype(np.float64)
                for o in range(raw_data.shape[1]):
                    raw_data[:][names[o+2]] = [(raw_data[:][names[o+2]][k+header]-np.mean(raw_data[:][names[o+2]])) \
                                                    / np.std(raw_data[:][names[o+2]]) for k in range(raw_data.shape[0])]

                if not os.path.exists(path="./dataset/"+vals):
                    os.makedirs("./dataset/"+vals)
                with open("./dataset/"+vals+"/rawdata"+str(j)+".csv","w") as f:
                    raw_data.to_csv("./dataset/"+vals+"/rawdata"+str(j)+".csv")
                f.close()
                raw_data_path[vals].append("./dataset/"+vals+"/rawdata"+str(j)+".csv")
        return raw_data_path
    else:
        raise TypeError("The input value of parameters should use dict type! ")


def post_data_standardize(datadict: dict, angle_flag=True):
    if isinstance(datadict, dict) and isinstance(angle_flag, bool):
        if angle_flag == True:
            for i in datadict:
                for j in datadict[i]:
                    datadict[i][j] = [(datadict[i][j][k] - np.mean(datadict[i][j])) \
                                        / np.std(datadict[i][j]) for k in range(len(datadict[i][j]))]
        elif angle_flag == False:
            for i in datadict:
                datadict[i] = [(datadict[i][j] - np.mean(datadict[i])) \
                                        / np.std(datadict[i]) for j in range(len(datadict[i]))]
        return datadict
    else:
        raise TypeError("The input value of parameters should use dict type! ")


if __name__ == '__main__':
    total_path_dict = {
               "Intact": [
            r"../fnao/intact/intact02/tr12.csv", r"../fnao/intact/intact02/tr19.csv",
            r"../fnao/intact/intact02/tr21.csv", r"../fnao/intact/intact02/tr27.csv",
            r"../fnao/intact/intact02/tr29.csv", r"../fnao/intact/intact02/tr30.csv",
            r"../fnao/intact/intact02/tr32.csv", r"../fnao/intact/intact03/tr05.csv",
            r"../fnao/intact/intact03/tr06.csv", r"../fnao/intact/intact03/tr07.csv",
            r"../fnao/intact/intact04/tr06.csv", r"../fnao/intact/intact04/tr07.csv",
        ],
        "MN-EV": [
            r"../data/Day7/A132/Trial01_1.csv", r"../data/Day7/A132/Trial01_2.csv",
            r"../data/Day7/A132/Trial01_3.csv", r"../data/Day7/A132/Trial01_4.csv",
            r"../data/Day7/A132/Trial01_5.csv", r"../data/Day7/A132/Trial01_6.csv",
            r"../data/Day7/A132/Trial01_7.csv", r"../data/Day7/A132/Trial02_1.csv",
            r"../data/Day7/A132/Trial02_2.csv", r"../data/Day7/A132/Trial02_3.csv",
            r"../data/Day7/A132/Trial03_1.csv", r"../data/Day7/A132/Trial03_2.csv",
            r"../data/Day7/A132/Trial03_3.csv", r"../data/Day7/A132/Trial03_4.csv",
            r"../data/Day7/A132/Trial04.csv", r"../data/Day7/A132/Trial05_1.csv",
            r"../data/Day7/A132/Trial05_2.csv", r"../data/Day7/A132/Trial06_1.csv",
            r"../data/Day7/A132/Trial06_2.csv", r"../data/Day7/A132/Trial06_3.csv",
            r"../data/Day7/A132/Trial07_1.csv", r"../data/Day7/A132/Trial07_2.csv",
            r"../data/Day7/A132/Trial08_1.csv", r"../data/Day7/A132/Trial08_2.csv",
            r"../data/Day7/A132/Trial08_3.csv", r"../data/Day7/A132/Trial09_1.csv",
            r"../data/Day7/A132/Trial09_2.csv", r"../data/Day7/A132/Trial09_2.csv",
            r"../data/Day7/A132/Trial10_1.csv", r"../data/Day7/A132/Trial10_2.csv",
            # r"../data/Day7/A132/Trial10_3.csv", r"../data/Day7/A132/Trial11_1.csv",
            # r"../data/Day7/A132/Trial11_2.csv", r"../data/Day7/A132/Trial11_3.csv",
            # r"../data/Day7/A132/Trial11_4.csv", r"../data/Day7/A132/Trial12_1.csv",
            # r"../data/Day7/A132/Trial12_2.csv", r"../data/Day7/A132/Trial12_3.csv",
            # r"../data/Day7/A132/Trial12_4.csv",
                ],
        "MN-MSC": [
            r"../data/Day7/A137/Trial02_1.csv", r"../data/Day7/A137/Trial02_2.csv",
            r"../data/Day7/A137/Trial02_3.csv", r"../data/Day7/A137/Trial02_4.csv",

            r"../data/Day7/A137/Trial02_5.csv", r"../data/Day7/A137/Trial03_1.csv",
            r"../data/Day7/A137/Trial03_2.csv",
            r"../data/Day7/A137/Trial04_1.csv",
            r"../data/Day7/A137/Trial05_1.csv", r"../data/Day7/A137/Trial05_2.csv",
            r"../data/Day7/A137/Trial09.csv", r"../data/Day7/A137/Trial10.csv",
            r"../data/Day7/A137/Trial12_1.csv", r"../data/Day7/A137/Trial14_1.csv"
        ],
        "Gel-EV": [
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3103_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3103_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_7.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3104_8.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3105_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3107_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3109_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3109_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3110_7.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_10.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_7.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_8.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3111_9.csv',

            #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_0.csv',
            #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_3.csv',

            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_3.csv',

            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_6.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_3.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3117_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3117_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3124_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3125_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3125_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3125_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3126_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3126_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3126_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3127_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3127_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_1.csv',

            #abnormal data r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_2.csv',
             r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3129_0.csv',
             r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3129_1.csv',
             r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3131_0.csv',
             r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3131_1.csv',
        ],
        "Control": [
            r"../data/Fangao/B90/B9008.csv", r"../data/Fangao/B90/B9011.csv", r"../data/Fangao/B90/B9017.csv",
            r"../data/Fangao/B90/B9018.csv", r"../data/Fangao/B90/B9019.csv", r"../data/Fangao/B90/B9020.csv",
            r"../data/Fangao/B90/B9021.csv", r"../data/Fangao/B90/B9022.csv", r"../data/Fangao/B90/B9023.csv",
            # r"../data/Fangao/B90/B9011_2.csv",
            # r"../data/Fangao/B90/B9011_3.csv",
            r"../data/Fangao/B90/B9017_2.csv",
            r"../data/Fangao/B90/B9017_3.csv", r"../data/Fangao/B90/B9017_4.csv", r"../data/Fangao/B90/B9018_2.csv",
            r"../data/Fangao/B90/B9018_3.csv", r"../data/Fangao/B90/B9018_4.csv", r"../data/Fangao/B90/B9019_2.csv",
            r"../data/Fangao/B90/B9019_3.csv", r"../data/Fangao/B90/B9020_2.csv", r"../data/Fangao/B90/B9020_3.csv",
            r"../data/Fangao/B90/B9022_2.csv", r"../data/Fangao/B90/B9022_3.csv", r"../data/Fangao/B90/B9022_4.csv",
            r"../data/Fangao/B90/B9022_5.csv", r"../data/Fangao/B90/B9022_6.csv", r"../data/Fangao/B90/B9022_7.csv",
            r"../data/Fangao/B90/B9023_2.csv", r"../data/Fangao/B90/B9023_3.csv", r"../data/Fangao/B90/B9023_4.csv",
            r"../data/Fangao/B90/B9023_5.csv", r"../data/Fangao/B90/B9023_6.csv", r"../data/Fangao/B90/B9023_7.csv",
                ],
        "MN": [
            r"../data/Fangao/C55/C5501.csv",
            # r"../data/Fangao/C55/C5504_0.csv",
            r"../data/Fangao/C55/C5504_1.csv",
            r"../data/Fangao/C55/C5504_2.csv", r"../data/Fangao/C55/C5504_3.csv", r"../data/Fangao/C55/C5505_0.csv",
            r"../data/Fangao/C55/C5505_1.csv", r"../data/Fangao/C55/C5505_2.csv", r"../data/Fangao/C55/C5505_3.csv",
            r"../data/Fangao/C55/C5505_4.csv", r"../data/Fangao/C55/C5506_0.csv", r"../data/Fangao/C55/C5506_1.csv",
            r"../data/Fangao/C55/C5506_2.csv", r"../data/Fangao/C55/C5506_3.csv", r"../data/Fangao/C55/C5506_4.csv",
            r"../data/Fangao/C55/C5507_0.csv", r"../data/Fangao/C55/C5507_1.csv", r"../data/Fangao/C55/C5507_2.csv",
            r"../data/Fangao/C55/C5508_0.csv", r"../data/Fangao/C55/C5508_1.csv", r"../data/Fangao/C55/C5508_2.csv",
            r"../data/Fangao/C55/C5508_3.csv", r"../data/Fangao/C55/C5508_4.csv", r"../data/Fangao/C55/C5509_0.csv",
            r"../data/Fangao/C55/C5509_1.csv", r"../data/Fangao/C55/C5509_2.csv", r"../data/Fangao/C55/C5509_3.csv",
            r"../data/Fangao/C55/C5509_4.csv", r"../data/Fangao/C55/C5510_0.csv", r"../data/Fangao/C55/C5510_1.csv",
            r"../data/Fangao/C55/C5511_0.csv", r"../data/Fangao/C55/C5511_1.csv", r"../data/Fangao/C55/C5511_2.csv",
            r"../data/Fangao/C55/C5512_0.csv",
            # r"../data/Fangao/C55/C5512_1.csv", r"../data/Fangao/C55/C5512_2.csv",
            r"../data/Fangao/C55/C5512_3.csv", r"../data/Fangao/C55/C5512_4.csv", r"../data/Fangao/C55/C5513_0.csv",
            r"../data/Fangao/C55/C5513_1.csv", r"../data/Fangao/C55/C5513_2.csv", r"../data/Fangao/C55/C5513_3.csv",
            r"../data/Fangao/C55/C5513_4.csv", r"../data/Fangao/C55/C5513_5.csv", r"../data/Fangao/C55/C5514_0.csv",
            r"../data/Fangao/C55/C5514_1.csv", r"../data/Fangao/C55/C5514_2.csv", r"../data/Fangao/C55/C5515_0.csv",
            r"../data/Fangao/C55/C5515_1.csv", r"../data/Fangao/C55/C5515_2.csv", r"../data/Fangao/C55/C5515_3.csv",
            r"../data/Fangao/C55/C5516_0.csv", r"../data/Fangao/C55/C5516_1.csv", r"../data/Fangao/C55/C5516_2.csv",
            r"../data/Fangao/C55/C5516_3.csv", r"../data/Fangao/C55/C5516_4.csv", r"../data/Fangao/C55/C5516_5.csv",
            r"../data/Fangao/C55/C5516_6.csv", r"../data/Fangao/C55/C5517_0.csv", r"../data/Fangao/C55/C5517_1.csv",
            r"../data/Fangao/C55/C5517_2.csv", r"../data/Fangao/C55/C5518_0.csv", r"../data/Fangao/C55/C5518_1.csv",
            r"../data/Fangao/C55/C5518_2.csv", r"../data/Fangao/C55/C5518_3.csv", r"../data/Fangao/C55/C5518_4.csv",
            r"../data/Fangao/C55/C5518_5.csv", r"../data/Fangao/C55/C5519_0.csv", r"../data/Fangao/C55/C5519_1.csv",
            r"../data/Fangao/C55/C5519_2.csv", r"../data/Fangao/C55/C5519_3.csv",  r"../data/Fangao/C55/C5519_4.csv",
            r"../data/Fangao/C55/C5519_5.csv", r"../data/Fangao/C55/C5519_6.csv",  r"../data/Fangao/C55/C5519_7.csv",
        ],
        "Gel-MSC": [
            # r"../data/Fangao/E33/E3301_0.csv",
            r"../data/Fangao/E33/E3301_1.csv", r"../data/Fangao/E33/E3301_2.csv",
            r"../data/Fangao/E33/E3301_3.csv", r"../data/Fangao/E33/E3301_4.csv",
            # r"../data/Fangao/E33/E3302_0.csv",
            r"../data/Fangao/E33/E3302_1.csv", r"../data/Fangao/E33/E3302_2.csv", r"../data/Fangao/E33/E3302_3.csv",
            r"../data/Fangao/E33/E3303_0.csv", r"../data/Fangao/E33/E3303_1.csv", r"../data/Fangao/E33/E3305_0.csv",
            r"../data/Fangao/E33/E3306_0.csv", r"../data/Fangao/E33/E3306_1.csv", r"../data/Fangao/E33/E3307_0.csv",
            r"../data/Fangao/E33/E3307_1.csv", r"../data/Fangao/E33/E3307_2.csv", r"../data/Fangao/E33/E3308_0.csv",

            r"../data/Fangao/E33/E3308_1.csv", "../data/Fangao/E33/E3308_2.csv",  r"../data/Fangao/E33/E3309_0.csv",
            "../data/Fangao/E33/E3309_1.csv", r"../data/Fangao/E33/E3310_0.csv", r"../data/Fangao/E33/E3310_1.csv",
            r"../data/Fangao/E33/E3310_2.csv", r"../data/Fangao/E33/E3313_0.csv", r"../data/Fangao/E33/E3313_1.csv",
            r"../data/Fangao/E33/E3313_2.csv", r"../data/Fangao/E33/E3313_3.csv", r"../data/Fangao/E33/E3314_0.csv",
            r"../data/Fangao/E33/E3314_1.csv", r"../data/Fangao/E33/E3315_0.csv", r"../data/Fangao/E33/E3316_0.csv",
            r"../data/Fangao/E33/E3316_1.csv", r"../data/Fangao/E33/E3316_2.csv", r"../data/Fangao/E33/E3317_0.csv",
            r"../data/Fangao/E33/E3317_1.csv", r"../data/Fangao/E33/E3318_0.csv", r"../data/Fangao/E33/E3319_0.csv",
            r"../data/Fangao/E33/E3321_0.csv",
            # r"../data/Fangao/E33/E3322_0.csv",
            r"../data/Fangao/E33/E3325_0.csv", r"../data/Fangao/E33/E3325_1.csv", r"../data/Fangao/E33/E3327_0.csv",
            r"../data/Fangao/E33/E3327_1.csv", r"../data/Fangao/E33/E3328_0.csv", r"../data/Fangao/E33/E3329_0.csv",

        ]}
    param_dict = {"header": 5,
                  "lindex": 4,
                  "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                            'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    param_dict_toe = {"header": 5,
                      "lindex": 16,
                      "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                                'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    param_dict_angle = {"header": 5,
                        "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                                  'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    group = ["Intact", "Control", "MN", "Gel-EV", "Gel-MSC", "MN-EV", "MN-MSC"]
    rc_dict = {
        "Intact": [], "Control": [], "MN": [], "MN-MSC": [],
        "Gel-EV": [], "MN-EV": [], "Gel-MSC": []
    }


    # Standardize & Normalization
    # raw_data_path = standardize_processing(path_dict=total_path_dict, param_dicts=param_dict)
    # print(raw_data_path)

    # Angle values exporting
    angle_amp_dict = {"Intact": {"hip": [], "knee": [], "ankle": []},
                      "Control": {"hip": [], "knee": [], "ankle": []},
                      "MN": {"hip": [], "knee": [], "ankle": []},
                      "MN-MSC": {"hip": [], "knee": [], "ankle": []},
                      "Gel-EV": {"hip": [], "knee": [], "ankle": []},
                      "MN-EV": {"hip": [], "knee": [], "ankle": []},
                      "Gel-MSC": {"hip": [], "knee": [], "ankle": []},
                      }
    angle_rc_dict = oscillation_pipline_processing(pathdict=total_path_dict, param_dict=param_dict_angle, angle_amp_dict=angle_amp_dict)
    angle_rc_dict = post_data_standardize(datadict=angle_rc_dict)

    rc_dict = post_data_standardize(datadict=height_pipline_processing(pathdict=total_path_dict, param_dict=param_dict, rc_dict=create_dict(group=group)), angle_flag=False)

    toe_rc_dict = post_data_standardize(datadict=height_pipline_processing(pathdict=total_path_dict, param_dict=param_dict_toe, rc_dict=create_dict(group=group)), angle_flag=False)
    crest_rc_dict_amp = post_data_standardize(datadict=amplitude_pipline_processing(pathdict=total_path_dict, param_dict=param_dict, rc_dict=create_dict(group=group)), angle_flag=False)
    toe_rc_dict_amp = post_data_standardize(datadict=amplitude_pipline_processing(pathdict=total_path_dict, param_dict=param_dict_toe, rc_dict=create_dict(group=group)), angle_flag=False)
    print('ok')
    print(rc_dict)
    # ls = [average(rc_dict[i]) / max([average(rc_dict[i]) for i in rc_dict]) for i in rc_dict]

    plt.style.use('ggplot')

    # Data Construction
    # Crest Height
    value1 = [average(np.exp(rc_dict[i])) / max([average(np.exp(rc_dict[i])) for i in rc_dict]) for i in rc_dict]
    print(value1)

    # Toe Height
    value2 = [average(np.exp(toe_rc_dict[i])) / max([average(np.exp(toe_rc_dict[i])) for i in toe_rc_dict]) for i in toe_rc_dict]

    # Crest Amplitude
    value3 = [average(np.exp(crest_rc_dict_amp[i])) / max([average(np.exp(crest_rc_dict_amp[i])) for i in crest_rc_dict_amp]) for i in crest_rc_dict_amp]

    # Toe Amplitude
    value4 = [average(np.exp(toe_rc_dict_amp[i])) / max([average(np.exp(toe_rc_dict_amp[i])) for i in toe_rc_dict_amp]) for i in toe_rc_dict_amp]

    # hip angle amplitude
    value5 = [average(np.exp(angle_rc_dict[i]["hip"])) / max([average(np.exp(angle_rc_dict[i]["hip"])) for i in angle_rc_dict])
              for i in angle_rc_dict]

    # knee angle amplitude
    value6 = [average(np.exp(angle_rc_dict[i]["knee"])) / max([average(np.exp(angle_rc_dict[i]["knee"])) for i in angle_rc_dict])
              for i in angle_rc_dict]

    # ankle angle amplitude
    value7 = [average(np.exp(angle_rc_dict[i]["ankle"])) / max([average(np.exp(angle_rc_dict[i]["ankle"])) for i in angle_rc_dict])
              for i in angle_rc_dict]
    #mas
    #nan = 0
    for arr in [value1,value2,value3,value4,value5,value6,value7]:
        for i in arr:
            print(i)
            if i == 'nan':
                print('change')
                i = average(arr)
                print('the array is changed to {}.'.format(arr))


    feature = ['Crest Height', 'Toe Height', 'Crest Amplitude', 'Toe Amplitude',
               'Hip Angle Amplitude', 'Knee Angle Amplitude', 'Ankle Angle Amplitude']
    feature = ["0","1","2","3","4","5","6","0"]
    #mas#label = ["Intact", "Control", "ROS", "DOPA", "GABA"]
    label = ["Intact", "Control", "MN", "Gel-EV", "Gel-MSC", "MN-EV", "MN-MSC"]

    #mas#values = {"Intact":[],"Control":[],"ROS":[],"DOPA":[],"GABA":[]}
    values = {"Intact": [], "Control": [], "MN": [], "MN-MSC": [],
    "Gel-EV": [], "MN-EV": [],  "Gel-MSC": []}

    for i, val in enumerate(zip(value1,value2,value3,value4,value5,value6,value7)):
        values[label[i]] = list(val)
    print(values["Intact"])

    angles = np.linspace(0, 2 * np.pi, len(values["Intact"]), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    fig = plt.figure(figsize=(8,8), dpi=300)
    ax = fig.add_subplot(111, polar=True)

    for i, key in enumerate(values.keys()):
        values[key] = np.concatenate([values[key], [values[key][0]]])
        ax.plot(angles, values[key], 'o-', linewidth=3.5, label=label[i])
        #ax.fill(angles, values[key], alpha=0.25)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(0, 1.2)
    plt.legend(loc='lower right',fontsize = 6)
    #plt.legend(loc='best')
    ax.grid(True)
    plt.savefig(r"C:\Users\Giraffe\Desktop\fig_radar\fig_1.png")
    plt.close()
    #plt.show()

    # Intact as benchmark
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_subplot(111, polar=True)
    colors = ["darkviolet","red","yellow","darkcyan","#853f04","#aa2116","#6f60aa","#ea66a6", "#cd3eca"]#mas
    for i in values:
        if i == "Intact":
            continue
        else:
            values[i] = [values[i][j]/values["Intact"][j] for j in range(len(values[i]))]
    del values["Intact"]
    label.remove("Intact")
    for i, key in enumerate(values.keys()):
        #print('ok')
        #print(key,i)
        ax.plot(angles, values[key], 'o-', color=colors[i], linewidth=2, label=label[i])
        # ax.fill(angles, values[key], alpha=0.25)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(0, 3.3)
    plt.legend(loc='lower right')
    ax.grid(True)
    plt.savefig(r"C:\Users\Giraffe\Desktop\fig_radar\fig2.svg")
    plt.close()
    #plt.show()

    for i, key in enumerate(values.keys()):
        fig = plt.figure(figsize=(8, 8), dpi=300)
        ax = fig.add_subplot(111, polar=True)
        print('ok')
        print(key,i)
        ax.plot(angles, values[key], 'o-', color=colors[i], linewidth=2, label=label[i])
        # ax.fill(angles, values[key], alpha=0.25)

        ax.set_thetagrids(angles * 180 / np.pi, feature)
        ax.set_ylim(0, 3.3)
        #plt.legend(loc='lower right')
        #plt.legend(loc='lower right')#mas
        plt.legend(loc = 'best',fontsize = 12)
        ax.grid(True)
        fig = plt.figure(1)
        fig.savefig(r"C:\Users\Giraffe\Desktop\fig_radar\fig{}.svg".format(i+3))
        #plt.close(fig)
        plt.show()