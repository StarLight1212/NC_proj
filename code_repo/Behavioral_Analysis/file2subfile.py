HEADER = "Trajectories\n \
100\n \
,,Patient 2:011,,,Patient 2:012,,,Patient 2:022,,,Patient 2:032,,,Patient 2:042,,,\n \
Frame,Sub Frame,X,Y,Z,X,Y,Z,X,Y,Z,X,Y,Z,X,Y,Z\n \
,,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm,mm\n "


def filesplitsub(origin_pth: str, split_list: list):
    with open(origin_pth, 'r') as fr:
        lines = fr.readlines()[5:]
        for i, sig_lst in enumerate(split_list):
            start_, end_ = sig_lst
            save_path = 'C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/split/'
            #with open(origin_pth[:-4]+'_'+str(i)+'.csv', 'w') as fw:
            with open(save_path + origin_pth[-9:-4] + '_' + str(i) + '.csv', 'w') as fw:
                fw.write(HEADER)
                for line in lines:
                    try:
                        index = int(line.split(',')[0])
                    except ValueError as ve:
                        continue
                    if start_ <= index <= end_:
                        fw.write(line)
                    elif index <= start_:
                        continue
                    else:
                        break
        fw.close()
    fr.close()


# filesplitsub('../data/Fangao/B88/B8801.csv', [[110, 304], [305, 510]])
# filesplitsub('../data/Fangao/B88/B8814.csv', [[961, 1165], [1166, 1391]])
# filesplitsub('../data/Fangao/B88/B8815.csv', [[283, 377], [378, 535]])
# filesplitsub('../data/Fangao/B88/B8822.csv', [[1, 95], [96, 179], [180, 274], [275, 396]])
# filesplitsub('../data/Fangao/B88/B8823.csv', [[336, 427], [428, 487], [488, 579], [580, 618], [619, 657], [658, 707], [708, 749], [750, 796]])
# filesplitsub('../data/Fangao/B88/B8824.csv', [[730, 882], [883, 1000], [1001, 1082], [1083, 1182], [1183, 1265], [1266, 1333]])
# filesplitsub('../data/Fangao/B88/B8825.csv', [[354, 448], [449, 519], [520, 618], [619, 748]])
# filesplitsub('../data/Fangao/B88/B8826.csv', [[54, 219], [383, 510], [511, 584], [585, 637], [638, 757], [758, 840], [1236, 1270], [1271, 1319], [1320, 1369], [1370, 1412], [1413, 1526], [1527, 1588], [1589, 1675], [1676, 1778]])
# filesplitsub('../data/Fangao/B88/B8827.csv', [[1, 62], [139, 216], [217, 264], [455, 513], [514, 695], [696, 814], [815, 1059], [2113, 2156], [2157, 2247], [2248, 2367]])
# filesplitsub('../data/Fangao/B88/B8828.csv', [[327, 378], [379, 441], [442, 501], [502, 593], [666, 772], [773, 844], [845, 927]])
# filesplitsub('../data/Fangao/B88/B8829.csv', [[501, 579], [580, 654], [655, 795], [796, 863], [864, 980], [981, 1136], [1137, 1302]])
# filesplitsub('../data/Fangao/B88/B8830.csv', [[382, 455], [456, 534], [535, 735], [736, 816], [817, 877], [878, 953], [954, 1042], [1043, 1180]])

# filesplitsub('../data/Fangao/C55/C5504.csv', [[2753, 3135], [3136, 3337], [3338, 3477], [3478, 3802]])
# filesplitsub('../data/Fangao/C55/C5505.csv', [[42, 149], [581, 626], [627, 710], [711, 831], [900, 1007]])
# filesplitsub('../data/Fangao/C55/C5506.csv', [[200, 270], [271, 344], [345, 407], [408, 480], [630, 769]])
# filesplitsub('../data/Fangao/C55/C5507.csv', [[210, 400], [401, 597], [598, 776]])
# filesplitsub('../data/Fangao/C55/C5508.csv', [[221, 282], [283, 393], [394, 497], [498, 606], [607, 789]])
# filesplitsub('../data/Fangao/C55/C5509.csv', [[213, 353], [354, 468], [469, 582], [583, 744], [745, 914]])
# filesplitsub('../data/Fangao/C55/C5510.csv', [[354, 555], [1034, 1130]])
# filesplitsub('../data/Fangao/C55/C5511.csv', [[198, 292], [293, 368], [369, 645]])
# filesplitsub('../data/Fangao/C55/C5512.csv', [[227, 322], [333, 535], [536, 678], [678, 762], [763, 913]])
# filesplitsub('../data/Fangao/C55/C5513.csv', [[214, 291], [292, 395], [396, 519], [520, 742], [743, 936], [1102, 1272]])
# filesplitsub('../data/Fangao/C55/C5514.csv', [[230, 355], [356, 480], [481, 673]])
# filesplitsub('../data/Fangao/C55/C5515.csv', [[358, 436], [437, 587], [588, 792], [793, 1124]])
# filesplitsub('../data/Fangao/C55/C5516.csv', [[1, 133], [134, 302], [303, 535], [536, 714], [715, 880], [881, 1161], [1162, 1340]])
# filesplitsub('../data/Fangao/C55/C5517.csv', [[60, 167], [168, 296], [297, 493]])
# filesplitsub('../data/Fangao/C55/C5518.csv', [[110, 220], [221, 325], [326, 527], [528, 622], [623, 696], [697, 812]])
# filesplitsub('../data/Fangao/C55/C5519.csv', [[91, 141], [142, 216], [217, 294], [295, 373], [374, 434], [435, 505], [506, 619], [620, 797]])

# filesplitsub('../data/Fangao/E33/E3301.csv', [[309, 560], [561, 819], [820, 1064], [1578, 1841], [1842, 2620]])
# filesplitsub('../data/Fangao/E33/E3302.csv', [[280, 652], [653, 1187], [1867, 2303], [2304, 2579]])
# filesplitsub('../data/Fangao/E33/E3303.csv', [[543, 991], [1212, 1539]])
# filesplitsub('../data/Fangao/E33/E3305.csv', [[1262, 1378]])
# filesplitsub('../data/Fangao/E33/E3306.csv', [[573, 878], [879, 1007]])
# filesplitsub('../data/Fangao/E33/E3307.csv', [[1, 149], [300, 550], [551, 745]])
# filesplitsub('../data/Fangao/E33/E3308.csv', [[17, 140], [552, 734], [735, 930]])
# filesplitsub('../data/Fangao/E33/E3309.csv', [[116, 268], [269, 441]])
# filesplitsub('../data/Fangao/E33/E3310.csv', [[487, 676], [677, 798], [799, 943]])
# filesplitsub('../data/Fangao/E33/E3313.csv', [[362, 530], [531, 652], [653, 750], [935, 1100]])
# filesplitsub('../data/Fangao/E33/E3314.csv', [[584, 750], [754, 950]])
# filesplitsub('../data/Fangao/E33/E3315.csv', [[1282, 1621]])
# filesplitsub('../data/Fangao/E33/E3316.csv', [[1, 127], [128, 292], [293, 360]])
# filesplitsub('../data/Fangao/E33/E3317.csv', [[189, 390], [880, 1190]])
# filesplitsub('../data/Fangao/E33/E3318.csv', [[306, 480]])
# filesplitsub('../data/Fangao/E33/E3319.csv', [[1, 99]])
# filesplitsub('../data/Fangao/E33/E3321.csv', [[859, 1048]])
# filesplitsub('../data/Fangao/E33/E3322.csv', [[451, 854]])
# filesplitsub('../data/Fangao/E33/E3325.csv', [[269, 523], [988, 1292]])

# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3116.csv', [[930,1001],[1002,1044],[1045,1085],[1244,1289],[1290,1324]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3117.csv', [[996,1021],[2540,2584]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3124.csv', [[1100,1154]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3125.csv', [[4609,4663],[4664,4727],[4728,4777]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3126.csv', [[271,325],[326,368],[394,458]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3127.csv', [[2419,2468],[2469,2502]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3128.csv', [[1295,1327],[1541,1577],[1578,1633]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3129.csv', [[707,742],[743,799]])
# filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G31/G3131.csv', [[1605,1651],[1740,1772]])


filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2304.csv',[[3127,3176],[3177,3201],[33203,3291],[3292,3356]])
#filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2305.csv',[[3775,3837],[3838,3869]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2308.csv',[[4137,4159],[4160,4181],[4196,4233]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2309.csv',[[1480,1556],[1557,1568],[1569,1626],[1852,1899],[1904,1933],[1934,1955],[1969,2004]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2311.csv',[[602,643],[644,677],[678,707],[714,752],[2893,2921]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2312.csv',[[3351,3391],[3392,3428],[3429,3471],[6150,6184]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2314.csv',[[1270,1325],[1432,1468],[1469,1490],[1491,1523]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2315.csv',[[1793,1837],[1887,1929],[3064,3108],[3109,3155],[3156,3185],[4186,4220],[4221,4253],[4344,4375]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2317.csv',[[1618,1668],[1669,1704],[1705,1740],[1741,1769],[1801,1834]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2318.csv',[[1960,1987],[1997,2012],[2152,2181]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2319.csv',[[1799,1849],[1861,1899]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2320.csv',[[2239,2273],[2274,2307],[2308,2329]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2321.csv',[[1177,1218],[1253,1292],[3436,3483],[3484,3504]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2324.csv',[[1925,1949],[1984,2023],[2058,2087]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2325.csv',[[346,365],[366,408],[696,789],[790,824],[825,870]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2328.csv',[[2119,2161],[2162,2210]])
filesplitsub('C:/Users/Giraffe/Desktop/data 0224/data 0224/patient 2/G23/G2329.csv',[[2640,2674],[2675,2720],[2721,2756]])


