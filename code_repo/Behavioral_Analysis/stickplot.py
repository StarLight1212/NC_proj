import os
import pandas as pd
from mpl_toolkits.mplot3d import axes3d
import transfer as tr
import matplotlib.pyplot as plt


def get_file_name(path):
    for root, dir, file in os.walk(path):
        print(file)
    return file


def construct_df(df_path: str, df_header: int, df_interval: int, df_columns: list):
    """
    :param df_path: to load the dataframe from each file path
    :param df_header: empty or nan information in each file
    :param df_interval: sample interval among the column dimension of dataframe
    :param df_columns: columns information redefine on dataframe
    :return: a preprocessed dataframe
    """
    # df = pd.read_excel(df_path, engine='openpyxl',)[df_header:]
    df = pd.read_csv(df_path, names=df_columns)[df_header:].astype('float32')
    df.columns = df_columns
    df = df[df.index % df_interval == 0]
    print(df)
    return df


def loc_index(df: pd.DataFrame, from_: int, pst_: int, to_: int):
    index_start = df.loc[df["Frames"].astype('int32') == from_].index[0] - header
    index_pst = df.loc[df["Frames"].astype('int32') == pst_].index[0] - header
    index_end = df.loc[df["Frames"].astype('int32') == to_].index[0] - header
    return index_start, index_pst, index_end


def construct_XYZ_lst(df_input: pd.DataFrame, start_: int, end_: int):
    """
    :param df_input:
    :param start_:
    :param end_:
    :return: [[X11, X12, ..., X17], [X21, X22, ..., X27], ... [Xpst1, Xpst2, ..., Xpst7]],
    [[Y11, Y12, ..., Y17], [Y21, Y22, ..., Y27], ... [Ypst1, Ypst2, ..., Ypst7]],
    [[Z11, Z12, ..., Z17], [Z21, Z22, ..., Z27], ... [Zpst1, Zpst2, ..., Zpst7]]
    """
    X_tmp, Y_tmp, Z_tmp = [], [], []
    df_processed = df_input.iloc[start_:end_, 2:]
    # print(df_processed.iloc[0]['X1'])
    for u in range(end_-start_):
        X_inner, Y_inner, Z_inner = [], [], []
        # Record the points sequentially
        for i in range(point_num):
            X_inner.append(df_processed.iloc[u]['X' + str(i + 1)])
            Y_inner.append(df_processed.iloc[u]['Y' + str(i + 1)])
            Z_inner.append(df_processed.iloc[u]['Z' + str(i + 1)])
        X_tmp.append(X_inner)
        Y_tmp.append(Y_inner)
        Z_tmp.append(Z_inner)
        #print(Z_tmp)
    return X_tmp, Y_tmp, Z_tmp


def construct_ensemble_axes_in_one_step(step_path: str, from_: int, pst_: int, to_: int):
    dataframe = construct_df(step_path, header, interval, column_cus)
    index_start, index_pst, index_end = loc_index(dataframe, from_, pst_, to_)
    # Get the Swing stage axes
    Stage1_X, Stage1_Y, Stage1_Z = construct_XYZ_lst(dataframe, index_start, index_pst)
    # Get the Stance stage axes
    Stage2_X, Stage2_Y, Stage2_Z = construct_XYZ_lst(dataframe, index_pst, index_end)

    return Stage1_X, Stage1_Y, Stage1_Z, Stage2_X, Stage2_Y, Stage2_Z


def all_step_pack(single_path: str, obj_step_num: int, record_lst: list):
    step_pack_X_S1, step_pack_Y_S1, step_pack_Z_S1 = [], [], []
    step_pack_X_S2, step_pack_Y_S2, step_pack_Z_S2 = [], [], []
    for i in range(obj_step_num):
        tmp_start, tmp_pst, tmp_end = record_lst[i]
        Stage1_X, Stage1_Y, Stage1_Z, Stage2_X, Stage2_Y, Stage2_Z = \
            construct_ensemble_axes_in_one_step(single_path, tmp_start, tmp_pst, tmp_end)
        step_pack_X_S1.append(Stage1_X)
        step_pack_Y_S1.append(Stage1_Y)
        step_pack_Z_S1.append(Stage1_Z)
        step_pack_X_S2.append(Stage2_X)
        step_pack_Y_S2.append(Stage2_Y)
        step_pack_Z_S2.append(Stage2_Z)
    return step_pack_X_S1, step_pack_Y_S1, step_pack_Z_S1, step_pack_X_S2, step_pack_Y_S2, step_pack_Z_S2


def plot_motor_graph(path_file, obj_step_num, record_lst, dpi=300, linewidth=0.5):
    X_S1, Y_S1, Z_S1, X_S2, Y_S2, Z_S2 = all_step_pack(path_file, obj_step_num, record_lst)
    fig = plt.figure(dpi=dpi)
    ax = fig.gca(projection='3d')
    # set figure information
    ax.axis('auto')
    ax.set_xlabel("x(mm)", fontsize=5)
    ax.set_ylabel("y(mm)", fontsize=5)
    ax.set_zlabel("z(mm)", fontsize=5)
    plt.tick_params(labelsize=5)
    ax.grid(False)
    plt.axis('off')
    #plt.gca().set_box_aspect((1, 1, 1.2))  # 当x、y、z轴范围之比为3:5:2时。
    for step_iter in range(obj_step_num):
        tmp_start, tmp_pst, tmp_end = record_lst[step_iter]
        for i in range(tmp_pst-tmp_start):
            figure = ax.plot(X_S1[step_iter][i], Y_S1[step_iter][i], Z_S1[step_iter][i], c='black', linewidth=linewidth)
        for i in range(tmp_end - tmp_pst):
            figure = ax.plot(X_S2[step_iter][i], Y_S2[step_iter][i], Z_S2[step_iter][i], c='red', linewidth=linewidth)
    plt.show()


path = '../data/'
# Initialize the parameters
header, interval, point_num, start, pst, end = 5, 1, 5, 0, 0, 0

# Gel-EV
# tmp_path = '../data/Fangao/B88/origin/B8801.csv'
# from_pst_end = [[110, 304, 304], [305, 510, 510]]
# -----------------
# tmp_path = '../data/Fangao/B88/origin/B8814.csv'
# from_pst_end = [[961, 1165, 1165], [1166, 1391, 1391]]
# -----------------
# tmp_path = '../data/Fangao/B88/origin/B8815.csv'
# from_pst_end = [[283, 377, 377], [378, 535, 535]]
# ------------------
# Best
# tmp_path = '../data/Fangao/B88/origin/B8822.csv'
# from_pst_end = [[30, 50, 84], [85, 105, 123], [124, 156, 190]]
# tmp_path = '../data/Fangao/B88/origin/B8823.csv'
# from_pst_end = [[383, 410, 447], [448, 460, 492]]
# from_pst_end = [[525, 553, 571], [572, 587, 640], [641, 650, 674], [675, 708, 727]]
# from_pst_end = [[525, 553, 571], [572, 587, 640], [641, 650, 674]]
# tmp_path = '../data/Fangao/B88/origin/B8824.csv'
# from_pst_end = [[995, 1009, 1018], [1019, 1084, 1135], [1136, 1148, 1188]]
# tmp_path = '../data/Fangao/B88/origin/B8825.csv'
# from_pst_end = [[383, 415, 454], [455, 490, 520], [521, 558, 615]]
# tmp_path = '../data/Fangao/B88/origin/B8826.csv'
# from_pst_end = [[368, 408, 460], [460, 490, 538], [539, 602, 627]]
# tmp_path = '../data/Fangao/B88/origin/B8827.csv'
# from_pst_end = [[2092, 2141, 2156], [2157, 2179, 2201], [2202, 2220, 2235]]
# -------------
# tmp_path = '../data/Fangao/B88/origin/B8828.csv'
# from_pst_end = [[385, 420, 455], [456, 481, 540], [541, 555, 602], [603, 625, 669]]
# from_pst_end = [[456, 481, 540], [541, 555, 602], [603, 625, 669]]
# -------------
# tmp_path = '../data/Fangao/B88/origin/B8829.csv'
# from_pst_end = [[501, 549, 579], [580, 600, 654], [655, 714, 795]]

# New Plain
# tmp_path = '../data/Fangao/B88/origin/B8822.csv'
# from_pst_end = [[30, 84, 84], [85, 123, 123], [124, 190, 190]]
# tmp_path = '../data/Fangao/B88/origin/B8823.csv'
# from_pst_end = [[383, 410, 447], [448, 460, 492]]
# from_pst_end = [[525, 553, 571], [572, 587, 640], [641, 650, 674], [675, 708, 727]]
# from_pst_end = [[525, 571, 571], [572, 640, 640], [641, 674, 674]]
# tmp_path = '../data/Fangao/B88/origin/B8824.csv'
# from_pst_end = [[995, 1018, 1018], [1019, 1135, 1135], [1136, 1188, 1188]]
# tmp_path = '../data/Fangao/B88/origin/B8825.csv'
# from_pst_end = [[383, 454, 454], [455, 520, 520], [521, 615, 615]]
# tmp_path = '../data/Fangao/B88/origin/B8826.csv'
# from_pst_end = [[368, 460, 460], [460, 538, 538], [539, 627, 627]]
# tmp_path = '../data/Fangao/B88/origin/B8827.csv'
# from_pst_end = [[2092, 2156, 2156], [2157, 2201, 2201], [2202, 2235, 2235]]
# -------------
# tmp_path = '../data/Fangao/B88/origin/B8828.csv'
# from_pst_end = [[385, 420, 455], [456, 481, 540], [541, 555, 602], [603, 625, 669]]
# from_pst_end = [[456, 540, 540], [541, 602, 602], [603, 669, 669]]
# -------------

tmp_path = 'C:/Users/Giraffe/Desktop/data0224/data0224/patient2/G23/G2304.csv'
from_pst_end = [[3127,3176],[3177,3201],[3202,3291]]
from_pst_end = tr.transfer(from_pst_end)

# MSC-PBS
# tmp_path = '../data/Fangao/C55/origin/C5504.csv'
# from_pst_end = [[2753, 2844, 2844], [2845, 2910, 2910], [2911, 3005, 3005]]
# tmp_path = '../data/Fangao/C55/origin/C5505.csv'
# from_pst_end = [[581, 626, 626], [627, 710, 710], [711, 831, 831]]
# tmp_path = '../data/Fangao/C55/origin/C5506.csv'
# from_pst_end = [[200, 270, 270], [271, 344, 344], [345, 407, 407]]
# tmp_path = '../data/Fangao/C55/origin/C5507.csv'
# from_pst_end = [[310, 400, 400], [401, 497, 497], [498, 576, 576]]
# tmp_path = '../data/Fangao/C55/origin/C5508.csv'  # None
# from_pst_end = [[221, 282, 282], [283, 393, 393], [394, 497, 497]]
# tmp_path = '../data/Fangao/C55/origin/C5509.csv'
# from_pst_end = [[213, 353, 353], [354, 468, 468], [469, 582, 582]]
# tmp_path = '../data/Fangao/C55/origin/C5514.csv'
# from_pst_end = [[230, 355, 355], [356, 480, 480], [481, 673, 673]]
# tmp_path = '../data/Fangao/C55/origin/C5515.csv'
# from_pst_end = [[358, 436, 436], [437, 587, 587], [588, 792, 792]]
# tmp_path = '../data/Fangao/C55/origin/C5518.csv'
# from_pst_end = [[110, 220, 220], [221, 325, 325], [326, 527, 527]]

# MSC-IV
# tmp_path = '../data/Fangao/ori/C69/C6901.csv'
# from_pst_end = [[396, 460, 460], [461, 515, 515], [516, 587, 587]]
# from_pst_end = [[811, 900, 900], [901, 1015, 1015], [1016, 1097, 1097]]
# tmp_path = '../data/Fangao/ori/C69/C6903.csv'
# from_pst_end = [[419, 543, 543], [544, 608, 608], [609, 670, 670]]
# tmp_path = '../data/Fangao/ori/C69/C6906.csv'
# from_pst_end = [[1147, 1257, 1257], [1258, 1350, 1350], [1351, 1572, 1572]]

# Gel-MSC
# tmp_path = '../data/Fangao/ori/E33/E3301.csv'
# from_pst_end = [[309, 410, 410], [411, 560, 560], [561, 819, 819]]
# tmp_path = '../data/Fangao/ori/E33/E3302.csv'  None
# from_pst_end = [[280, 410, 410], [411, 560, 560], [561, 819, 819]]
# tmp_path = '../data/Fangao/ori/E33/E3308.csv'
# from_pst_end = [[552, 630, 630], [630, 734, 734], [735, 930, 930]]
# tmp_path = '../data/Fangao/ori/E33/E3309.csv'
# from_pst_end = [[116, 268, 268], [269, 350, 350], [351, 441, 441]]
# tmp_path = '../data/Fangao/ori/E33/E3310.csv'   # Search
# from_pst_end = [[487, 676, 676], [677, 798, 798], [799, 943, 943]]
# tmp_path = '../data/Fangao/ori/E33/E3313.csv'
# from_pst_end = [[362, 530, 530], [531, 652, 652], [653, 750, 750]]
# tmp_path = '../data/Fangao/ori/E33/E3314.csv'
# from_pst_end = [[584, 650, 650], [651, 750, 750], [751, 950, 950]]
# tmp_path = '../data/Fangao/ori/E33/E3316.csv' #Search
# from_pst_end = [[1, 127, 127], [128, 292, 292], [293, 360, 360]]
# tmp_path = '../data/Fangao/ori/E33/E3327.csv' # Search
# from_pst_end = [[346, 556, 556], [557, 730, 730], [731, 941, 941]]

# MN
# tmp_path = '../data/Fangao/ori/B90/B9017.csv'
# from_pst_end = [[220, 433, 433], [434, 580, 580], [581, 712, 712]]
# tmp_path = '../data/Fangao/ori/B90/B9018.csv'
# from_pst_end = [[118, 243, 243], [244, 379, 379], [380, 443, 443]]
# tmp_path = '../data/Fangao/ori/B90/B9019.csv'
# from_pst_end = [[512, 622, 622], [623, 826, 826], [827, 982, 982]]
# tmp_path = '../data/Fangao/ori/B90/B9020.csv'
# from_pst_end = [[197, 264, 264], [265, 417, 417], [418, 598, 598]]
# tmp_path = '../data/Fangao/ori/B90/B9022.csv'   # Search
# from_pst_end = [[374, 465, 465], [466, 546, 546], [547, 630, 630]]
# tmp_path = '../data/Fangao/ori/B90/B9023.csv'
# from_pst_end = [[216, 338, 338], [339, 438, 438], [439, 530, 530]]

step_num = len(from_pst_end)
# assert len(from_pst_end) == step_num, 'The lst Info is not coordinate with the step number'
column_cus = ['Frames', 'Times', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']
# file_name = get_file_name(path)
# tmp_path = path+file_name[index_monkey]

plot_motor_graph(tmp_path, step_num, from_pst_end)
