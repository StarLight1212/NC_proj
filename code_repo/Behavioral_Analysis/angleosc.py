import math
from mpl_toolkits.mplot3d import axes3d
import transfer as tr
from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
import os


# load data from file
# you can replace this using with open
def DataProcessing(path, header: int, index_list: list, names: list, processingtype="single"):
    if not os.path.exists(path):
        os.makedirs(path)

    # Loading Data and construct the Dataframe
    rawdata = read_csv(path, names=names)

    # Remove the padding headers of the DataFrame
    rawdata = rawdata[header:]

    def valueprocessing(from_: int, to_: int):
        datalist = []
        for i in range(to_ - from_):
            ls1 = list(rawdata.iloc[from_, 2:17].astype(np.float64).values)
            from_ += 1
            datalist.append(ls1)
        return datalist

    if processingtype == "single":
        if len(index_list) == 3:
            from_ = index_list[0]
            pst_ = index_list[1]
            to_ = index_list[2]
        elif len(index_list) == 2:
            from_ = index_list[0]
            pst_ = index_list[0]
            to_ = index_list[1]
        else:
            raise Exception("Index list length out of range!")
        # Index the real line code from the Frame info
        index_start = int(rawdata.loc[rawdata["Frame"] == str(from_)].index[0])
        index_pst = int(rawdata.loc[rawdata["Frame"] == str(pst_)].index[0])
        index_end = int(rawdata.loc[rawdata["Frame"] == str(to_)].index[0])
        if isinstance(index_start, int) and isinstance(index_end, int):
            datalist1 = valueprocessing(from_=index_start, to_=index_end)
            # datalist2 = valueprocessing(from_=index_pst, to_=index_end)
            print(datalist1)
            # Normalize the position of Pst point
            index_pst -= index_start
            return datalist1, index_pst

        elif isinstance(index_start, float) and isinstance(index_end, float):
            rawdata = rawdata.astype(np.float64)
            datalist1 = valueprocessing(from_=int(index_start), to_=int(index_end))
            # Normalize the position of Pst point
            index_pst -= index_start
            return datalist1, index_pst

        else:
            print("The input value of parameters(from_,pst_,to_)should use int type! ")


    elif processingtype == "multiple":
        from_, pst_, to_ = [], [], []
        # Continuous index list
        for i in range(0, len(rawlist) - 1, 2):
            from_.append(index_list[i])
            print(pst_)
            pst_.append(index_list[i + 1])
            to_.append(index_list[i + 2])
        index_start = [rawdata.loc[rawdata["Frame"] == str(from_[i])].index[0] for i in range(len(from_))]
        index_pst = [rawdata.loc[rawdata["Frame"] == str(pst_[i])].index[0] for i in range(len(pst_))]
        index_end = [rawdata.loc[rawdata["Frame"] == str(to_[i])].index[0] for i in range(len(to_))]
        if isinstance(index_start, list) and isinstance(index_pst, list) and isinstance(index_end, list):
            # suppose we got a continuous index list with each three steps
            # Notice each of the continuous three number represent the stance and the swing phase
            step_num = (len(index_pst) - 1) / 2
            total_datalist = []
            for i in range(int(step_num)):
                datalist1 = valueprocessing(from_=index_start[i], to_=index_pst[i])
                datalist2 = valueprocessing(from_=index_pst[i], to_=index_end[i])
                total_datalist.append(datalist1)
                total_datalist.append(datalist2)
            # datalist2 = valueprocessing(from_=index_pst, to_=index_end)
            # print(datalist)
            # Normalize the position of Pst point
            index_pst -= index_start
            return total_datalist, index_pst

        else:
            print("The input value of parameters(from_,pst_,to_)should use int type! ")

    else:
        raise Exception("The processing type is error")


def single_inforXYZ(datalist: list, iter_: int):
    X = []
    Y = []
    Z = []
    i = 0
    while i < len(datalist[0]):
        X.append(datalist[iter_][i])
        Y.append(datalist[iter_][i + 1])
        Z.append(datalist[iter_][i + 2])
        i += 3
    return X, Y, Z


def multi_inforXYZ(datalist: list, from_: int, to_: int):
    totalx = []
    totaly = []
    totalz = []
    for i in range(to_ - from_):
        X, Y, Z = single_inforXYZ(datalist=datalist, iter_=i)
        totalx.append(X)
        totaly.append(Y)
        totalz.append(Z)

    return totalx, totaly, totalz


# def eulerDistance(point_1:list, point_2:list, num:int, i:int):
#     if num < 0:
#         return 0
#     else:
#         return math.sqrt((point_1[i][num] - point_2[i][num]) ** 2) + eulerDistance(point_1 = point_1,point_2 = point_2, num = num-1, i = i)


def euler_distance(point_1: list, point_2: list, i: int):
    return math.sqrt((point_1[i][0] - point_2[i][0]) ** 2 + (point_1[i][1] - point_2[i][1]) ** 2 + \
                     (point_1[i][2] - point_2[i][2]) ** 2)


def cal_ang(point_1: list, point_2: list, point_3: list, sequence: int):
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
        a = euler_distance(point_2, point_3, i=i)
        b = euler_distance(point_1, point_3, i=i)
        c = euler_distance(point_1, point_2, i=i)

        i += 1
        if a != 0 and c != 0:
            B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))

            angle.append(B)

        else:
            continue
        # C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    return angle


def main(path, names: list, header: int, rawlist: list):
    datalist1, index_pst = DataProcessing(path=path, names=names, header=header, index_list=rawlist)

    ndatalist = []
    i = 0
    while i < len(datalist1):
        ndatalist.append(datalist1[i])
        i += 1

    totalx = []
    totaly = []
    totalz = []
    for i in range(len(ndatalist)):
        X, Y, Z = single_inforXYZ(datalist=ndatalist, iter_=i)
        totalx.append(X)
        totaly.append(Y)
        totalz.append(Z)

    angle_p1 = []
    angle_p2 = []
    angle_p3 = []
    angle_p4 = []
    angle_p5 = []
    i0 = 0
    for i0 in range(len(ndatalist)):
        angle_p1.append([ndatalist[i0][0], ndatalist[i0][1], ndatalist[i0][2]])
        angle_p2.append([ndatalist[i0][3], ndatalist[i0][4], ndatalist[i0][5]])
        angle_p3.append([ndatalist[i0][6], ndatalist[i0][7], ndatalist[i0][8]])
        angle_p4.append([ndatalist[i0][9], ndatalist[i0][10], ndatalist[i0][11]])
        angle_p5.append([ndatalist[i0][12], ndatalist[i0][13], ndatalist[i0][14]])
        i0 += 1

    hip_angle = cal_ang(sequence=len(ndatalist), point_1=angle_p1,
                        point_2=angle_p2, point_3=angle_p3)
    knee_angle = cal_ang(sequence=len(ndatalist), point_1=angle_p2,
                         point_2=angle_p3, point_3=angle_p4)
    ankle_angle = cal_ang(sequence=len(ndatalist), point_1=angle_p3,
                          point_2=angle_p4, point_3=angle_p5)

    return hip_angle, knee_angle, ankle_angle, index_pst


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']

    names = ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
             'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']
    header = 5

    #B90
    hip_scale, knee_scale, ankle_scale =  [95,120],[25,60], [20,180]
    path = r'C:/Users/Giraffe/Desktop/Behaviordata/Day7/A137/Trial02_5.csv'
    rawlist = [[9535,9588,9652],[9653,9679,9878], [9879,9902,9965]]
    #rawlist = tr.transfer(rawlist)

    # A137
    # 03
    # path = r'./Dr.F/Behaviordata/Day7/A137/Trial02_5.csv'
    # rawlist = [9535,9588,9652,9679,9878,9902,9965]
    # 02
    # path = r'./Dr.F/Behaviordata/Day7/A137/Trial02_3.csv'
    # rawlist = [4903,4930,5016,5042,5136,5178,5193]
    # 01
    # path = r'./Dr.F/Behaviordata/Day7/A137/Trial02_2.csv'
    # rawlist = [893, 930, 1079, 1132, 1506, 1519, 1732]

    # A132 tr1
    # 04
    # path = r'./Dr.F/Behaviordata/Day7/A132/Trial01_6.csv'
    # rawlist = [11913, 11919, 11938, 11963, 11994, 12003, 12045]
    # 03
    # path = r'./Dr.F/Behaviordata/Day7/A132/Trial01_4.csv'
    # rawlist = [7442, 7470, 7489, 7499, 7520, 7554, 7593]
    # 02
    # path = r'./Dr.F/Behaviordata/Day7/A132/Trial01_2.csv'
    # rawlist = [2915,2963,2995,3011,3032,3041,3066]
    # 01
    # path = r'./Dr.F/Behaviordata/Day7/A132/Trial01_1.csv'
    # rawlist = [324,335,360,373,395,424,444]




    # Gel-EV
    scale_set = True
    plain_step = True
    # hip_scale, knee_scale, ankle_scale = [80, 140], [40, 100], [60, 180]
    # path = '../data/Fangao/B88/origin/B8822.csv'
    # rawlist = [[30, 50, 84], [85, 105, 123], [124, 156, 190]]
    # path = '../data/Fangao/B88/origin/B8823.csv'
    # rawlist = [[525, 553, 571], [572, 587, 630], [631, 650, 674]]
    # path = '../data/Fangao/B88/origin/B8824.csv'
    # rawlist = [[995, 1009, 1018], [1019, 1084, 1135], [1136, 1148, 1188]]
    # path = '../data/Fangao/B88/origin/B8825.csv'
    # rawlist = [[383, 415, 454], [455, 490, 520], [521, 558, 615]]
    # path = '../data/Fangao/B88/origin/B8826.csv'
    # rawlist = [[368, 408, 460], [460, 490, 538], [539, 602, 627]]
    # path = '../data/Fangao/B88/origin/B8827.csv'
    # rawlist = [[2092, 2141, 2156], [2157, 2179, 2201], [2202, 2220, 2235]]
    # path = '../data/Fangao/B88/origin/B8828.csv'
    # rawlist = [[456, 481, 540], [541, 555, 602], [603, 625, 669]]
    # path = '../data/Fangao/B88/origin/B8829.csv'
    # rawlist = [[501, 549, 579], [580, 600, 654], [655, 714, 795]]
    
    # MSC-PBS
    # plain_step = True
    # scale_set = True
    # path = '../data/Fangao/C55/origin/C5504.csv'
    # rawlist = [[2753, 2844, 2844], [2845, 2910, 2910], [2911, 3005, 3005]]
    # hip_scale, knee_scale, ankle_scale = [40, 80], [10, 50], [120, 180]
    # path = '../data/Fangao/C55/origin/C5505.csv'
    # rawlist = [[581, 626, 626], [627, 710, 710], [711, 831, 831]]
    # path = '../data/Fangao/C55/origin/C5506.csv'
    # rawlist = [[200, 270, 270], [271, 344, 344], [345, 407, 407]]
    # path = '../data/Fangao/C55/origin/C5507.csv'
    # rawlist = [[310, 400, 400], [401, 497, 497], [498, 576, 576]]
    # path = '../data/Fangao/C55/origin/C5509.csv'
    # rawlist = [[213, 353, 353], [354, 468, 468], [469, 582, 582]]
    # path = '../data/Fangao/C55/origin/C5514.csv'
    # rawlist = [[230, 355, 355], [356, 480, 480], [481, 673, 673]]
    # path = '../data/Fangao/C55/origin/C5515.csv'
    # rawlist = [[358, 436, 436], [437, 587, 587], [588, 792, 792]]
    # path = '../data/Fangao/C55/origin/C5518.csv'
    # rawlist = [[110, 220, 220], [221, 325, 325], [326, 527, 527]]

    # MSC-IV
    # scale_set = True
    # plain_step = True
    # hip_scale, knee_scale, ankle_scale = [60, 110], [60, 120], [120, 180]
    # path = '../data/Fangao/ori/C69/C6901.csv'
    # rawlist = [[396, 460, 460], [461, 515, 515], [516, 587, 587]]
    # rawlist = [[811, 900, 900], [901, 1015, 1015], [1016, 1097, 1097]]
    # path = '../data/Fangao/ori/C69/C6903.csv'
    # hip_scale, knee_scale, ankle_scale = [60, 110], [60, 120], [90, 180]
    # rawlist = [[419, 543, 543], [544, 608, 608], [609, 670, 670]]
    # path = '../data/Fangao/ori/C69/C6906.csv'
    # hip_scale, knee_scale, ankle_scale = [60, 110], [40, 120], [90, 180]
    # rawlist = [[1147, 1257, 1257], [1258, 1350, 1350], [1351, 1572, 1572]]

    # Gel-MSC
    # scale_set = True
    # plain_step = True
    # path = '../data/Fangao/ori/E33/E3301.csv'
    # hip_scale, knee_scale, ankle_scale = [60, 110], [30, 90], [120, 180]
    # rawlist = [[309, 410, 410], [411, 560, 560], [561, 819, 819]]
    # path = '../data/Fangao/ori/E33/E3308.csv'
    # hip_scale, knee_scale, ankle_scale = [40, 110], [30, 90], [120, 180]
    # rawlist = [[552, 630, 630], [630, 734, 734], [735, 930, 930]]
    # path = '../data/Fangao/ori/E33/E3309.csv'
    # hip_scale, knee_scale, ankle_scale = [30, 90], [30, 90], [120, 180]
    # rawlist = [[116, 268, 268], [269, 350, 350], [351, 441, 441]]
    # path = '../data/Fangao/ori/E33/E3310.csv'   # Search
    # hip_scale, knee_scale, ankle_scale = [30, 90], [30, 90], [120, 180]
    # rawlist = [[487, 676, 676], [677, 798, 798], [799, 943, 943]]
    # path = '../data/Fangao/ori/E33/E3313.csv'
    # hip_scale, knee_scale, ankle_scale = [30, 90], [30, 90], [120, 180]
    # rawlist = [[362, 530, 530], [531, 652, 652], [653, 750, 750]]
    # path = '../data/Fangao/ori/E33/E3314.csv'
    # hip_scale, knee_scale, ankle_scale = [30, 90], [30, 90], [120, 180]
    # rawlist = [[584, 650, 650], [651, 750, 750], [751, 950, 950]]
    # path = '../data/Fangao/ori/E33/E3316.csv'   # Search
    # hip_scale, knee_scale, ankle_scale = [30, 90], [30, 90], [120, 180]
    # rawlist = [[1, 127, 127], [128, 292, 292], [293, 360, 360]]
    
    # MN-EV
    # scale_set = True
    # plain_step = True
    # path = '../data/Fangao/ori/B90/B9017.csv'
    # hip_scale, knee_scale, ankle_scale = [0, 60], [0, 60], [120, 180]
    # rawlist = [[220, 433, 433], [434, 580, 580], [581, 712, 712]]
    # path = '../data/Fangao/ori/B90/B9018.csv'
    # rawlist = [[118, 243, 243], [244, 379, 379], [380, 443, 443]]
    # path = '../data/Fangao/ori/B90/B9019.csv'
    # rawlist = [[512, 622, 622], [623, 826, 826], [827, 982, 982]]
    # path = '../data/Fangao/ori/B90/B9020.csv'
    # rawlist = [[197, 264, 264], [265, 417, 417], [418, 598, 598]]
    # path = '../data/Fangao/ori/B90/B9022.csv'   # Search
    # rawlist = [[374, 465, 465], [466, 546, 546], [547, 630, 630]]
    # path = '../data/Fangao/ori/B90/B9023.csv'
    # rawlist = [[216, 338, 338], [339, 438, 438], [439, 530, 530]]

    index_lst = [rawlist[0][0], rawlist[-1][-1]]
    # line_x = rawlist[1]
    start_1, pst_1, start_2, pst_2, start_3, pst_3 = rawlist[0][0], rawlist[0][1], rawlist[1][0], rawlist[1][1], rawlist[2][0], rawlist[2][1]
    hip_angle, knee_angle, ankle_angle, index_pst = main(path=path, names=names, header=header, rawlist=index_lst)
    line_x = index_pst
    print(line_x)
    fig = plt.figure(figsize=(6, 3), dpi=300)

    # ...........................................................................................
    # Comprehensive Plotting

    # plt.plot(range(len(hip_angle)),hip_angle,'-.',color='red',label="Hip Angle")
    # plt.plot(range(len(knee_angle)),knee_angle,'--.',color='blue',label="Knee Angle")
    # plt.plot(range(len(ankle_angle)),ankle_angle,'--',color='orange',label="Ankle Angle")
    # # plt.title("各关节角度数据")
    # plt.axvline(x=13/len(hip_angle), ls="--", c="gray")  # Add vertical line
    # ax = plt.axes()
    # for i in ['top', 'right', 'bottom', 'left']:
    #     ax.spines[i].set_visible(False)
    # plt.xlabel("Time Sequence/Frame")
    # plt.ylabel("Angle/°")
    # plt.xlim([0,30])
    # plt.grid(False)
    # # plt.legend(loc='best')
    # plt.tight_layout()
    # plt.show()

    # ...........................................................................................
    # KneePlotting
    x = [(i / len(knee_angle)) * 100 for i in range(len(knee_angle))]
    print(x)
    max_v = max(len(knee_angle), len(ankle_angle), len(hip_angle))
    plt.plot(x, knee_angle, '-', color="black", linewidth=4.5)
    # plt.axvline(x=line_x/len(knee_angle)*100, ls="--", c="gray")  # Add vertical line
    if not plain_step:
        plt.axvline(x=(pst_1 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_3 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_3 - start_1) / max_v * 100, ls="--", c="gray")

    # ax = plt.axes()
    # for i in ['top', 'right', 'bottom', 'left']:
    #     ax.spines[i].set_visible(False)

    plt.xlabel("Motion Stage/%")
    plt.ylabel("Knee Angle/°")
    plt.xlim([0, 100])
    if scale_set:
        plt.ylim(knee_scale)
    # plt.yticks(range(0,210,60))
    plt.grid(False)
    plt.tight_layout()
    plt.show()

    # ...........................................................................................
    # HipPlotting
    fig = plt.figure(figsize=(6, 3), dpi=300)
    x = [i / len(hip_angle) * 100 for i in range(len(hip_angle))]
    plt.plot(x, hip_angle, '-', color="black", linewidth=4.5)
    if not plain_step:
        plt.axvline(x=(pst_1 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_3 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_3 - start_1) / max_v * 100, ls="--", c="gray")

    # plt.axvline(x=line_x/len(hip_angle)*100, ls="--", c="gray")  # Add vertical line
    # ax = plt.axes()
    # for i in ['top', 'right', 'bottom', 'left']:
    #     ax.spines[i].set_visible(False)

    plt.xlabel("Motion Stage/%")
    plt.ylabel("Hip Angle/°")
    plt.xlim([0, 100])
    if scale_set:
        plt.ylim(hip_scale)
    # plt.yticks(range(0, 210, 60))
    plt.grid(False)
    plt.tight_layout()
    plt.show()

    # ...........................................................................................
    # AnklePlotting
    fig = plt.figure(figsize=(6, 3), dpi=300)
    x = [i / len(ankle_angle) * 100 for i in range(len(ankle_angle))]
    plt.plot(x, ankle_angle, '-', color="black", linewidth=4.5)
    if not plain_step:
        plt.axvline(x=(pst_1 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_2 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(start_3 - start_1) / max_v * 100, ls="--", c="gray")
        plt.axvline(x=(pst_3 - start_1) / max_v * 100, ls="--", c="gray")

    # plt.axvline(x=line_x/len(ankle_angle)*100, ls="--", c="gray")  # Add vertical line
    # ax = plt.axes()
    # for i in ['top', 'right', 'bottom', 'left']:
    #     ax.spines[i].set_visible(False)

    plt.xlabel("Motion Stage/%")
    plt.ylabel("Ankle Angle/°")
    plt.xlim([0, 100])
    if scale_set:
        plt.ylim(ankle_scale)
    # plt.yticks(range(0, 210, 60))
    plt.grid(False)
    plt.tight_layout()
    plt.show()
