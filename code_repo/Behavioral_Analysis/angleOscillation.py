import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import math

def average(ls: list):
    count = 0
    sum = 0
    for i in ls:
        if not pd.isna(i):
            sum += i
            count += 1
    try:
        return sum / count
    except:
        print('zero')

def sa_read_csv(path, header: int, names: list):
    if not os.path.exists(path):
        os.makedirs(path)
    rawdata = pd.read_csv(path, names=names)
    if isinstance(header, int):
        return rawdata.iloc[header:, 2:17]
    else:
        raise TypeError("The input value of parameters(from_,pst_,to_)should use int type! ")


def euler_distance(point_1:list, point_2:list, i:int):
    return math.sqrt((point_1[i][0] - point_2[i][0]) ** 2 + (point_1[i][1] - point_2[i][1]) ** 2 +\
                         (point_1[i][2]-point_2[i][2]) ** 2)


def cal_ang(point_1:list, point_2:list, point_3:list, sequence: int)->list:
    """
    Calculate the value of angle based on three points' position.
    :param point_1: Point1's position
    :param point_2: Point2's position
    :param point_3: Point3's position
    :return: return the value of angle2.
    Note: angle1 and angle3 are relative angles which are calculated by the triangle constructed by three points.
    """
    angle = []
    for i in range(sequence):
        a = euler_distance(point_2,point_3,i=i)
        b = euler_distance(point_1,point_3,i=i)
        c = euler_distance(point_1,point_2,i=i)
        i += 1
        if a != 0 and c != 0:
            B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))
            angle.append(B)

        else:
            continue
        # C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    return angle


def extract_position(datalist : pd.DataFrame)-> dict:
    position_dict = {"p1": [], "p2": [], "p3": [], "p4": [], "p5": []}
    if isinstance(datalist, pd.DataFrame):
        for i in range(datalist.shape[0]):
            data_l1 = list(datalist.iloc[i].astype(np.float64).values)
            position_dict["p1"].append(data_l1[0:3])
            position_dict["p2"].append(data_l1[3:6])
            position_dict["p3"].append(data_l1[6:9])
            position_dict["p4"].append(data_l1[9:12])
            position_dict["p5"].append(data_l1[12:15])
            i += 1
        return position_dict
    else:
        raise TypeError("The input value of parameter(datalist) should use pd.DataFrame type!")


def get_oscillation(ls: list)->float:
    if isinstance(ls, list):
        maxValue = max(ls)
        minValue = min(ls)
        return maxValue - minValue
    else:
        raise TypeError("The input value of parameters(from_,pst_,to_)should use int type! ")


def oscillation_pipline_processing(pathdict: dict, param_dict: dict, angle_amp_dict: dict):
    header, names = param_dict["header"], param_dict["names"]

    if isinstance(pathdict, dict) and isinstance(param_dict, dict):

        for i, vals in enumerate(list(angle_amp_dict.keys())):
            for j in range(len(pathdict[vals])):
                ctrl_raw_data = sa_read_csv(path=pathdict[vals][j], header=header, names=names)
                position_dict = extract_position(ctrl_raw_data)
                # hip angle
                angle_amp_dict[vals]["hip"].append(get_oscillation(ls=cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p1"],
                                    point_2=position_dict["p2"], point_3=position_dict["p3"])))
                # knee angle
                angle_amp_dict[vals]["knee"].append(get_oscillation(ls=cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p2"],
                                     point_2=position_dict["p3"], point_3=position_dict["p4"])))
                # ankle angle
                angle_amp_dict[vals]["ankle"].append(get_oscillation(ls=cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p3"],
                                      point_2=position_dict["p4"], point_3=position_dict["p5"])))
                j += 1
        #mas
        for useless, vals in enumerate(list(angle_amp_dict.keys())):
            print(vals)
            for i in ['hip','knee','ankle']:
                ave = average(angle_amp_dict[vals][i])
                index = 0
                for j in angle_amp_dict[vals][i]:
                    #print(angle_amp_dict[vals][i])
                    if pd.isna(j):
                        print('the original array is {}.'.format(angle_amp_dict[vals][i]))
                        #j = average(angle_amp_dict[vals])
                        angle_amp_dict[vals][i][index] = ave
                        print('the array is changed to {}.'.format(angle_amp_dict[vals][i]))
                    index += 1

            # for i in angle_amp_dict[vals]:
            #     if pd.isna(i):
            #         print('the original array is {}.'.format(angle_amp_dict[vals]))
            #         i = average(angle_amp_dict[vals])
            #         print('the array is changed to {}.'.format(angle_amp_dict[vals]))

        return angle_amp_dict
    else:
        raise TypeError("The input value of parameters(from_,pst_,to_)should use int type! ")


def get_max_height(datalist: list) -> int:
    if isinstance(datalist, list):
        maxValue = max(datalist)
        return maxValue
    else:
        raise TypeError("The input value of parameters(from_,pst_,to_)should use int type! ")


def violin_plot(group: list, rc_dict: dict, dtype: str):

    if isinstance(dtype, str) and isinstance(rc_dict, dict) and isinstance(group, list):
        # dynamics_df = pd.DataFrame([rc_dict["intact"][dtype], rc_dict["control"][dtype], \
        #                     rc_dict["ROS"][dtype], rc_dict["DOPA"][dtype], \
        #                     rc_dict["GABA"][dtype]], index=group).T
        dynamics_df = pd.DataFrame([rc_dict[i][dtype] for i in rc_dict], index=group).T
        sns.violinplot(data=dynamics_df, split=True, palette="Set2")
        sns.swarmplot(data=dynamics_df, color="k")
        if dtype == "hip":
            plt.ylabel("Hip angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Hip angle oscillation (°)"), dpi=1000)
        elif dtype == "knee":
            plt.ylabel("Knee angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Knee angle oscillation (°)"), dpi=1000)
        elif dtype == "ankle":
            plt.ylabel("Ankle angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Ankle angle oscillation (°)"), dpi=1000)
        else:
            raise ValueError("dtype can not be blank or the type of dtype should be string!")
    else:
        raise TypeError("The input value of parameters(group, rc_dict, dtype) should use int type!")
    plt.close()


def boxline_plot(group: list, rc_dict: dict, dtype: str):

    if isinstance(dtype, str) and isinstance(rc_dict, dict) and isinstance(group, list):
        dynamics_df = pd.DataFrame([rc_dict[i][dtype] for i in rc_dict], index=group).T
        # dynamics_df = pd.DataFrame([rc_dict["intact"][dtype], rc_dict["control"][dtype], \
        #                     rc_dict["ROS"][dtype], rc_dict["DOPA"][dtype], \
        #                     rc_dict["GABA"][dtype]], index=group).T
        # sns.swarmplot(data=dynamics_df, color="k")
        dynamics_df.boxplot(grid=False, showmeans=True, patch_artist=True, sym="r*")

        if dtype == "hip":
            plt.ylabel("Hip angle oscillation (°)")
        elif dtype == "knee":
            plt.ylabel("Knee angle oscillation (°)")
        elif dtype == "ankle":
            plt.ylabel("Ankle angle oscillation (°)")
        else:
            raise ValueError("dtype can not be blank or the type of dtype should be string!")
    else:
        raise TypeError("The input value of parameters(group, rc_dict, dtype) should use int type!")
    plt.close()


def coordinates_pipline_processing(pathdict: dict, param_dict: dict):
    header, names = param_dict["header"], param_dict["names"]

    if isinstance(pathdict, dict) and isinstance(param_dict, dict):
        angle_dict = {"Intact": {"hip": [], "knee": [], "ankle": []},
                      "Control": {"hip": [], "knee": [], "ankle": []},
                      "MN": {"hip": [], "knee": [], "ankle": []},
                      "MN-MSC": {"hip": [], "knee": [], "ankle": []},
                      "Gel-EV": {"hip": [], "knee": [], "ankle": []},
                      "MN-EV": {"hip": [], "knee": [], "ankle": []},
                      "Gel-MSC": {"hip": [], "knee": [], "ankle": []},}

        for i, vals in enumerate(list(angle_dict.keys())):
            for j in range(len(pathdict[vals])):
                ctrl_raw_data = sa_read_csv(path=pathdict[vals][j], header=header, names=names)
                position_dict = extract_position(ctrl_raw_data)
                # hip angle
                angle_dict[vals]["hip"].append(cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p1"],
                                    point_2=position_dict["p2"], point_3=position_dict["p3"]))
                # knee angle
                angle_dict[vals]["knee"].append(cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p2"],
                                     point_2=position_dict["p3"], point_3=position_dict["p4"]))
                # ankle angle
                angle_dict[vals]["ankle"].append(cal_ang(sequence=ctrl_raw_data.shape[0], point_1=position_dict["p3"],
                                      point_2=position_dict["p4"], point_3=position_dict["p5"]))
                j += 1

        return angle_dict
    else:
        raise TypeError("The input value of parameters(from_,pst_,to_)should use int type! ")


def coordinate_plot(group: list, rc_dict: dict, dtype: str):

    if isinstance(dtype, str) and isinstance(rc_dict, dict) and isinstance(group, list):
        # dynamics_df = pd.DataFrame([rc_dict["intact"][dtype], rc_dict["control"][dtype], \
        #                     rc_dict["ROS"][dtype], rc_dict["DOPA"][dtype], \
        #                     rc_dict["GABA"][dtype]], index=group).T
        dynamics_df = pd.DataFrame([rc_dict["intact"][dtype], rc_dict["control"][dtype], \
                            rc_dict["ROS"][dtype], rc_dict["DOPA"][dtype], \
                            rc_dict["GABA"][dtype]], index=group).T
        for _, vals in enumerate(list(rc_dict.keys())):
            for i in range(len(rc_dict[vals][dtype])):
                # print(rc_dict[vals][dtype])
                plt.plot(list(range(len(rc_dict[vals][dtype][i]))), rc_dict[vals][dtype][i])
                if dtype == "hip":
                    plt.ylabel("Hip angle oscillation (°)")
                elif dtype == "knee":
                    plt.ylabel("Knee angle oscillation (°)")
                elif dtype == "ankle":
                    plt.ylabel("Ankle angle oscillation (°)")
                else:
                    raise ValueError("dtype can not be blank or the type of dtype should be string!")
                plt.show()
    else:
        raise TypeError("The input value of parameters(group, rc_dict, dtype) should use int type!")


def anova_test(re_dict:dict, dtype:str):
    dynamics_df = pd.DataFrame([re_dict["Intact"][dtype], re_dict["Control"][dtype], \
                                re_dict["MN"][dtype], re_dict["Gel-EV"][dtype], \
                                re_dict["Gel-MSC"][dtype], \
                                re_dict["MN-EV"][dtype], \
                                re_dict["MN-MSC"][dtype], \
                                ], index=group).T
    dynamics_df.columns.name = dtype
    data_new = dynamics_df.melt().dropna()
    model = ols('value~C('+dtype+')',data=data_new).fit()
    pair_t = model.t_test_pairwise('C('+dtype+')')
    return anova_lm(model), pair_t.result_frame


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
            #r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3103_0.csv',
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

            # abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_0.csv',
            # abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_1.csv',
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

            # abnormal data r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_2.csv',
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
            r"../data/Fangao/C55/C5519_2.csv", r"../data/Fangao/C55/C5519_3.csv", r"../data/Fangao/C55/C5519_4.csv",
            r"../data/Fangao/C55/C5519_5.csv", r"../data/Fangao/C55/C5519_6.csv", r"../data/Fangao/C55/C5519_7.csv",
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

            r"../data/Fangao/E33/E3308_1.csv", "../data/Fangao/E33/E3308_2.csv", r"../data/Fangao/E33/E3309_0.csv",
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
    param_dict = {"header": 5,
                  "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                            'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    group = ["Intact", "Control", "MN", "Gel-EV", "Gel-MSC", "MN-EV", "MN-MSC"]
    angle_amp_dict = {"Intact": {"hip": [], "knee": [], "ankle": []},
                      "Control": {"hip": [], "knee": [], "ankle": []},
                      "MN": {"hip": [], "knee": [], "ankle": []},
                      "MN-MSC": {"hip": [], "knee": [], "ankle": []},
                      "Gel-EV": {"hip": [], "knee": [], "ankle": []},
                      "MN-EV": {"hip": [], "knee": [], "ankle": []},
                      "Gel-MSC": {"hip": [], "knee": [], "ankle": []}}

    angle_rc_dict = oscillation_pipline_processing(pathdict=total_path_dict, param_dict=param_dict, angle_amp_dict=angle_amp_dict)
    # hip angle amplitude
    violin_plot(group=group, rc_dict=angle_rc_dict, dtype="hip")
    boxline_plot(group=group, rc_dict=angle_rc_dict, dtype="hip")

    # knee angle amplitude
    violin_plot(group=group, rc_dict=angle_rc_dict, dtype="knee")
    boxline_plot(group=group, rc_dict=angle_rc_dict, dtype="knee")

    # ankle angle amplitude
    violin_plot(group=group, rc_dict=angle_rc_dict, dtype="ankle")
    boxline_plot(group=group, rc_dict=angle_rc_dict, dtype="ankle")

    print(angle_rc_dict)

    angle_s = coordinates_pipline_processing(pathdict=total_path_dict, param_dict=param_dict)
    # coordinate_plot(group=group, rc_dict=angle_s, dtype="knee")

    print("-----------ANOVA Analysis---------")
    print("ANOVA for Hip Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="hip"))

    print("ANOVA for Knee Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="knee"))

    print("ANOVA for Ankle Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="ankle"))




