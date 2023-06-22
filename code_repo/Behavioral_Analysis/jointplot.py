import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import math


def sa_read_csv(path, header: int, names: list):
    if not os.path.exists(path):
        os.makedirs(path)
    rawdata = pd.read_csv(path, names=names)
    if isinstance(header, int):
        return rawdata.iloc[header:, 2:23]
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
            B = math.degrees(np.arccos((a * a + c * c - b * b) / (2 * a * c)))

        else:
            continue
        if np.isnan(B):
            print("NaN Value Raise!")
            continue
        angle.append(B)
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

        dynamics_df = pd.DataFrame([rc_dict[i][dtype] for i in rc_dict], index=group).T
        sns.violinplot(data=dynamics_df, split=True, palette="Set2")
        sns.swarmplot(data=dynamics_df, color="k")
        if dtype == "hip":
            plt.ylabel("Hip angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Hip angle oscillation (°)"), dpi=3400)
        elif dtype == "knee":
            plt.ylabel("Knee angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Knee angle oscillation (°)"), dpi=3400)
        elif dtype == "ankle":
            plt.ylabel("Ankle angle oscillation (°)")
            plt.savefig(r'C:\Users\Giraffe\Desktop\{}.png'.format("Ankle angle oscillation (°)"), dpi=3400)
        else:
            raise ValueError("dtype can not be blank or the type of dtype should be string!")
    else:
        raise TypeError("The input value of parameters(group, rc_dict, dtype) should use int type!")
    plt.close()


def boxline_plot(group: list, rc_dict: dict, dtype: str):

    if isinstance(dtype, str) and isinstance(rc_dict, dict) and isinstance(group, list):
        dynamics_df = pd.DataFrame([rc_dict[i][dtype] for i in rc_dict], index=group).T

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
        angle_dict = {
            "Intact": {"hip": [], "knee": [], "ankle": []},
            "Control": {"hip": [], "knee": [], "ankle": []},
            "MN": {"hip": [], "knee": [], "ankle": []},
            "MN-MSC": {"hip": [], "knee": [], "ankle": []},
            "Gel-EV": {"hip": [], "knee": [], "ankle": []},
            "MN-EV": {"hip": [], "knee": [], "ankle": []},
            "MSC-PBS": {"hip": [], "knee": [], "ankle": []},
            "MSC-IV": {"hip": [], "knee": [], "ankle": []},
            "Gel-MSC": {"hip": [], "knee": [], "ankle": []},
                      }

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


def anova_test(re_dict: dict, dtype: str):
    dynamics_df = pd.DataFrame([re_dict["Intact"][dtype], re_dict["Control"][dtype], \
                                re_dict["MN"][dtype], re_dict["MN-MSC"][dtype], \
                                re_dict["Gel-EV"][dtype], re_dict["MN-EV"][dtype],
                                re_dict["MSC-PBS"][dtype], \
                                re_dict["MSC-IV"][dtype], re_dict["Gel-MSC"][dtype]], index=group).T
    dynamics_df.columns.name = dtype
    data_new = dynamics_df.melt().dropna()
    model = ols('value~C('+dtype+')', data=data_new).fit()
    pair_t = model.t_test_pairwise('C('+dtype+')')
    return anova_lm(model), pair_t.result_frame


if __name__ == '__main__':
    # Crest Height Analysis

    total_path_dict = {
        "Intact": [
            r"../fnao/intact/intact02/tr12.csv", r"../fnao/intact/intact02/tr19.csv",
            r"../fnao/intact/intact02/tr21.csv", r"../fnao/intact/intact02/tr27.csv",
            r"../fnao/intact/intact02/tr29.csv", r"../fnao/intact/intact02/tr30.csv",
            r"../fnao/intact/intact02/tr32.csv", r"../fnao/intact/intact03/tr05.csv",
            r"../fnao/intact/intact03/tr06.csv", r"../fnao/intact/intact03/tr07.csv",
            r"../fnao/intact/intact04/tr06.csv", r"../fnao/intact/intact04/tr07.csv",
        ],
        "Control": [
            r"../fnao/ctrl/A1/tr01.csv", r"../fnao/ctrl/A1/tr03.csv",
            # r"../fnao/ctrl/A1/tr05.csv", r"../fnao/ctrl/A051/tr01.csv",
            # r"../fnao/ctrl/A051/tr06.csv", r"../fnao/ctrl/A051/tr11.csv",
            r"../fnao/ctrl/A1/tr05.csv",
            # r"../fnao/ctrl/A051/tr06.csv",
            r"../fnao/ctrl/A053/tr02.csv",
            # r"../fnao/ctrl/A053/tr02.csv",r"../fnao/ctrl/A051/tr12.csv",
            # r"../fnao/ctrl/A053/tr03.csv",
            r"../data/zym_csv/tosend/0615/C068/tr02.csv",
            r"../data/zym_csv/tosend/0615/control/tr08.csv", r"../data/zym_csv/tosend/0615/control/tr09.csv",
            r"../data/zym_csv/tosend/0615/control/tr10.csv", r"../data/zym_csv/tosend/0615/control/tr11.csv"

               ],
        "MN-EV": [
            # r"../fnao/mn/A2/tr03.csv",
            # r"../fnao/mn/A2/tr05.csv",
            # r"../fnao/mn/A2/tr07.csv",
            r"../fnao/mn/A037/tr02.csv",
            # r"../fnao/mn/A037/tr03.csv",
            # r"../fnao/mn/A037/tr05.csv",
            # r"../fnao/mn/A037/tr13.csv", r"../fnao/mn/A037/tr14.csv",
            # r"../fnao/mn/A052/tr01.csv",
            r"../fnao/mn/A052/tr02.csv",
            r"../fnao/mn/A052/tr06.csv", r"../fnao/mn/A055/tr01.csv",
            r"../fnao/mn/A055/tr06.csv", r"../fnao/mn/A055/tr07.csv",
            r"../fnao/mn/A055/tr08.csv",
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
            # r"../fnao/mn-msc/A22/tr08.csv", r"../fnao/mn-msc/A22/tr09.csv",
            # r"../fnao/mn-msc/A22/tr10.csv", r"../fnao/mn-msc/A22/tr11.csv",
            r"../fnao/mn-msc/A48/tr02.csv",
            # r"../fnao/mn-msc/A48/tr03-1.csv",
            r"../fnao/mn-msc/A48/tr04-1.csv",
            r"../fnao/mn-msc/A48/tr04-2.csv",
            # r"../fnao/mn-msc/A48/tr07.csv",
            r"../fnao/mn-msc/A049/tr02_1.csv",
            r"../fnao/mn-msc/A049/tr03_1.csv", r"../fnao/mn-msc/A049/tr04_1.csv",
            # r"../fnao/mn-msc/A049/tr07.csv", r"../fnao/mn-msc/A050/tr01.csv",
            # r"../fnao/mn-msc/A050/tr03.csv",
            # r"../fnao/mn-msc/A050/tr04.csv",
            # r"../fnao/mn-msc/A050/tr05.csv",
            r"../fnao/mn-msc/A50/tr06.csv",
            r"../fnao/mn-msc/A50/tr11.csv", r"../fnao/mn-msc/A50/tr12.csv",
            r"../fnao/mn-msc/A50/tr13.csv",
            # r"../fnao/mn-msc/A050/tr01.csv",
            r"../data/Day7/A137/Trial02_1.csv", r"../data/Day7/A137/Trial02_2.csv",
            r"../data/Day7/A137/Trial02_3.csv", r"../data/Day7/A137/Trial02_4.csv",
            # r"../data/Day7/A137/Trial02_5.csv", r"../data/Day7/A137/Trial03_1.csv",
            # r"../data/Day7/A137/Trial03_2.csv",
            # r"../data/Day7/A137/Trial04_1.csv",
            # r"../data/Day7/A137/Trial05_1.csv", r"../data/Day7/A137/Trial05_2.csv",
            # r"../data/Day7/A137/Trial09.csv", r"../data/Day7/A137/Trial10.csv",
            # r"../data/Day7/A137/Trial12_1.csv", r"../data/Day7/A137/Trial14_1.csv"
        ],
        "Gel-EV": [
            r"../data/Fangao/B88/B8801_0.csv", r"../data/Fangao/B88/B8801_1.csv", r"../data/Fangao/B88/B8806.csv",
            r"../data/Fangao/B88/B8807.csv", r"../data/Fangao/B88/B8808.csv", r"../data/Fangao/B88/B8811.csv",
            r"../data/Fangao/B88/B8814_0.csv", r"../data/Fangao/B88/B8814_1.csv", r"../data/Fangao/B88/B8815_0.csv",
            r"../data/Fangao/B88/B8815_1.csv", r"../data/Fangao/B88/B8819.csv", r"../data/Fangao/B88/B8822_0.csv",
            r"../data/Fangao/B88/B8822_1.csv", r"../data/Fangao/B88/B8822_2.csv", r"../data/Fangao/B88/B8822_3.csv",
            r"../data/Fangao/B88/B8823_0.csv", r"../data/Fangao/B88/B8823_1.csv", r"../data/Fangao/B88/B8823_2.csv",
            r"../data/Fangao/B88/B8823_3.csv",
            # r"../data/Fangao/B88/B8823_4.csv",
            r"../data/Fangao/B88/B8823_5.csv",
            r"../data/Fangao/B88/B8823_6.csv", r"../data/Fangao/B88/B8823_7.csv",
            # r"../data/Fangao/B88/B8824_0.csv",
            r"../data/Fangao/B88/B8824_1.csv", r"../data/Fangao/B88/B8824_2.csv",
            r"../data/Fangao/B88/B8824_3.csv", r"../data/Fangao/B88/B8824_4.csv", r"../data/Fangao/B88/B8824_5.csv",
            r"../data/Fangao/B88/B8825_0.csv", r"../data/Fangao/B88/B8825_1.csv", r"../data/Fangao/B88/B8825_2.csv",
            r"../data/Fangao/B88/B8825_3.csv", r"../data/Fangao/B88/B8826_0.csv", r"../data/Fangao/B88/B8826_1.csv",
            r"../data/Fangao/B88/B8826_2.csv", r"../data/Fangao/B88/B8826_3.csv", r"../data/Fangao/B88/B8826_4.csv",
            r"../data/Fangao/B88/B8826_5.csv", r"../data/Fangao/B88/B8826_6.csv", r"../data/Fangao/B88/B8826_7.csv",
            r"../data/Fangao/B88/B8826_8.csv", r"../data/Fangao/B88/B8826_9.csv", r"../data/Fangao/B88/B8826_10.csv",
            r"../data/Fangao/B88/B8826_11.csv", r"../data/Fangao/B88/B8826_12.csv", r"../data/Fangao/B88/B8826_13.csv",
            r"../data/Fangao/B88/B8827_0.csv", r"../data/Fangao/B88/B8827_1.csv", r"../data/Fangao/B88/B8827_2.csv",

            r"../data/Fangao/B88/B8827_3.csv", r"../data/Fangao/B88/B8827_4.csv", r"../data/Fangao/B88/B8827_5.csv",
            r"../data/Fangao/B88/B8827_6.csv", r"../data/Fangao/B88/B8827_7.csv", r"../data/Fangao/B88/B8827_8.csv",
            # r"../data/Fangao/B88/B8827_9.csv",
            r"../data/Fangao/B88/B8828_0.csv", r"../data/Fangao/B88/B8828_1.csv",
            r"../data/Fangao/B88/B8828_2.csv", r"../data/Fangao/B88/B8828_3.csv", r"../data/Fangao/B88/B8828_4.csv",
            r"../data/Fangao/B88/B8828_5.csv", r"../data/Fangao/B88/B8828_6.csv", r"../data/Fangao/B88/B8829_0.csv",
            r"../data/Fangao/B88/B8829_1.csv", r"../data/Fangao/B88/B8829_2.csv", r"../data/Fangao/B88/B8829_3.csv",
            r"../data/Fangao/B88/B8829_4.csv", r"../data/Fangao/B88/B8829_5.csv", r"../data/Fangao/B88/B8829_6.csv",
            r"../data/Fangao/B88/B8830_0.csv", r"../data/Fangao/B88/B8830_1.csv", r"../data/Fangao/B88/B8830_2.csv",
            r"../data/Fangao/B88/B8830_3.csv", r"../data/Fangao/B88/B8830_4.csv", r"../data/Fangao/B88/B8830_5.csv",
            r"../data/Fangao/B88/B8830_6.csv", r"../data/Fangao/B88/B8830_7.csv",

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
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_0.csv',

            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3112_1.csv',
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

             #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3113_6.csv',
             #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_0.csv',
             #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_1.csv',
             #abnormal r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_2.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_3.csv',
            #
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_4.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_5.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3114_6.csv',
            #
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3116_2.csv',
            #
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
            #abnormal data r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3128_2.csv',

            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3129_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3129_1.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3131_0.csv',
            r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G3131_1.csv',

        ],
        "MN": [
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
        "MSC-PBS": [
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
        "MSC-IV": [
            r"../data/Fangao/C69/C6901.csv",
            # r"../data/Fangao/C69/C6902.csv",
            r"../data/Fangao/C69/C6903.csv",
            r"../data/Fangao/C69/C6904.csv",
            # r"../data/Fangao/C69/C6906.csv", r"../data/Fangao/C69/C6901_2.csv",
            r"../data/Fangao/C69/C6901_3.csv", r"../data/Fangao/C69/C6901_4.csv", r"../data/Fangao/C69/C6901_5.csv",
            r"../data/Fangao/C69/C6901_6.csv",
            # r"../data/Fangao/C69/C6902_2.csv",

            r"../data/Fangao/C69/C6903_2.csv",
            r"../data/Fangao/C69/C6903_3.csv",
            r"../data/Fangao/C69/C6903_4.csv",
            r"../data/Fangao/C69/C6903_5.csv",
            r"../data/Fangao/C69/C6904_2.csv",
            r"../data/Fangao/C69/C6906_2.csv",
            r"../data/Fangao/C69/C6906_3.csv",

            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2304_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2304_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2304_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2304_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2308_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2308_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2308_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_4.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_5.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2309_6.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2311_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2311_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2311_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2311_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2311_4.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2312_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2312_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2312_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2312_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2314_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2314_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2314_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2314_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_4.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_5.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_6.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2315_7.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2317_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2317_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2317_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2317_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2317_4.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2318_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2318_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2318_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2319_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2319_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2320_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2320_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2320_2.csv',
            #
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2321_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2321_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2321_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2321_3.csv',
            #
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2324_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2324_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2324_2.csv',
            #
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2325_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2325_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2325_2.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2325_3.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2325_4.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2328_0.csv',
            #
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2328_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2329_0.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2329_1.csv',
            # r'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/G2329_2.csv',

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
        ]
    }

    param_dict = {"header": 5,
                  "lindex": 4,
                  "names": ['Frame', 'Time', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                            'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5'
                            ]}
    group = ["Intact", "Control", "MSC-PBS", "MN", "MSC-IV", "Gel-EV", "Gel-MSC", "MN-EV", "MN-MSC"]
    angle_amp_dict = {
        "Intact": {"hip": [], "knee": [], "ankle": []},
        "Control": {"hip": [], "knee": [], "ankle": []},
        "MN": {"hip": [], "knee": [], "ankle": []},
        "MN-MSC": {"hip": [], "knee": [], "ankle": []},
        "Gel-EV": {"hip": [], "knee": [], "ankle": []},
        "MN-EV": {"hip": [], "knee": [], "ankle": []},
        "MSC-PBS": {"hip": [], "knee": [], "ankle": []},
        "MSC-IV": {"hip": [], "knee": [], "ankle": []},
        "Gel-MSC": {"hip": [], "knee": [], "ankle": []},
                      }

    angle_rc_dict = oscillation_pipline_processing(pathdict=total_path_dict, param_dict=param_dict,\
                                                   angle_amp_dict=angle_amp_dict)
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

    # angle_s = coordinates_pipline_processing(pathdict=total_path_dict, param_dict=param_dict)
    # coordinate_plot(group=group, rc_dict=angle_s, dtype="knee")

    print("-----------ANOVA Analysis---------")
    print("ANOVA for Hip Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="hip"))

    print("ANOVA for Knee Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="knee"))

    print("ANOVA for Ankle Amplitude")
    print(anova_test(re_dict=angle_rc_dict, dtype="ankle"))
