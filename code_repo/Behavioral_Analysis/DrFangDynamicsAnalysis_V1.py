from statisticsAnalysisV3 import height_pipline_processing, violin_plot, box_plot, \
    anova_test, amplitude_pipline_processing, create_dict

if __name__ == '__main__':
    total_path_dict = {
        "intact":[
            r"./fnao/intact/intact02/tr12.csv", r"./fnao/intact/intact02/tr19.csv",
            r"./fnao/intact/intact02/tr21.csv", r"./fnao/intact/intact02/tr27.csv",
            r"./fnao/intact/intact02/tr29.csv", r"./fnao/intact/intact02/tr30.csv",
            r"./fnao/intact/intact02/tr32.csv", r"./fnao/intact/intact03/tr05.csv",
            r"./fnao/intact/intact03/tr06.csv", r"./fnao/intact/intact03/tr07.csv",
            r"./fnao/intact/intact04/tr06.csv", r"./fnao/intact/intact04/tr07.csv",
        ],
        "control":[
            r"./fnao/ctrl/A1/tr01.csv", r"./fnao/ctrl/A1/tr03.csv",
            # r"./fnao/ctrl/A1/tr05.csv", r"./fnao/ctrl/A051/tr01.csv",
            # r"./fnao/ctrl/A051/tr06.csv", r"./fnao/ctrl/A051/tr11.csv",
            r"./fnao/ctrl/A1/tr05.csv",
            r"./fnao/ctrl/A051/tr06.csv",r"./fnao/ctrl/A053/tr02.csv",
             # r"./fnao/ctrl/A053/tr02.csv",r"./fnao/ctrl/A051/tr12.csv",
            r"./fnao/ctrl/A053/tr03.csv", r"./zym_csv/tosend/0615/C068/tr02.csv",
            r"./zym_csv/tosend/0615/control/tr08.csv", r"./zym_csv/tosend/0615/control/tr09.csv",
            r"./zym_csv/tosend/0615/control/tr10.csv", r"./zym_csv/tosend/0615/control/tr11.csv"
        ],
        "MN":[
            r"./fnao/mn/A2/tr03.csv", r"./fnao/mn/A2/tr05.csv",
            r"./fnao/mn/A2/tr07.csv", r"./fnao/mn/A037/tr02.csv",
            r"./fnao/mn/A037/tr03.csv", r"./fnao/mn/A037/tr05.csv",
            r"./fnao/mn/A037/tr13.csv", r"./fnao/mn/A037/tr14.csv",
            r"./fnao/mn/A052/tr01.csv", r"./fnao/mn/A052/tr02.csv",
            r"./fnao/mn/A052/tr06.csv", r"./fnao/mn/A055/tr01.csv",
            r"./fnao/mn/A055/tr06.csv", r"./fnao/mn/A055/tr07.csv",
            r"./fnao/mn/A055/tr08.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial01_1.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial01_2.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial01_3.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial01_4.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial01_5.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial01_6.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial01_7.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial02_1.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial02_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial02_3.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial03_1.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial03_2.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial03_3.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial03_4.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial04.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial05_1.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial05_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial06_1.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial06_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial06_3.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial07_1.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial07_2.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial08_1.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial08_2.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial08_3.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial09_1.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial09_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial09_2.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial10_1.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial10_2.csv",
            # r"./Dr.F/Behaviordata/Day7/A132/Trial10_3.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial11_1.csv",
            # r"./Dr.F/Behaviordata/Day7/A132/Trial11_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial11_3.csv",
            # r"./Dr.F/Behaviordata/Day7/A132/Trial11_4.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial12_1.csv",
            # r"./Dr.F/Behaviordata/Day7/A132/Trial12_2.csv", r"./Dr.F/Behaviordata/Day7/A132/Trial12_3.csv",
            r"./Dr.F/Behaviordata/Day7/A132/Trial12_4.csv",
        ],
        "MN-MSC":[
            # r"./fnao/mn-msc/A22/tr08.csv", r"./fnao/mn-msc/A22/tr09.csv",
            # r"./fnao/mn-msc/A22/tr10.csv", r"./fnao/mn-msc/A22/tr11.csv",
            r"./fnao/mn-msc/A48/tr02.csv", r"./fnao/mn-msc/A48/tr03-1.csv",
            r"./fnao/mn-msc/A48/tr04-1.csv", r"./fnao/mn-msc/A48/tr04-2.csv",
            r"./fnao/mn-msc/A48/tr07.csv", r"./fnao/mn-msc/A049/tr02_1.csv",
            r"./fnao/mn-msc/A049/tr03_1.csv", r"./fnao/mn-msc/A049/tr04_1.csv",
            # r"./fnao/mn-msc/A049/tr07.csv", r"./fnao/mn-msc/A050/tr01.csv",
            # r"./fnao/mn-msc/A050/tr03.csv",
            # r"./fnao/mn-msc/A050/tr04.csv",
            # r"./fnao/mn-msc/A050/tr05.csv",
            r"./fnao/mn-msc/A50/tr06.csv",
            r"./fnao/mn-msc/A50/tr11.csv", r"./fnao/mn-msc/A50/tr12.csv",
            r"./fnao/mn-msc/A50/tr13.csv",
            # r"./fnao/mn-msc/A050/tr01.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial02_1.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial02_2.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial02_3.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial02_4.csv",
            # r"./Dr.F/Behaviordata/Day7/A137/Trial02_5.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial03_1.csv",
            # r"./Dr.F/Behaviordata/Day7/A137/Trial03_2.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial04_1.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial05_1.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial05_2.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial09.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial10.csv",
            r"./Dr.F/Behaviordata/Day7/A137/Trial12_1.csv", r"./Dr.F/Behaviordata/Day7/A137/Trial14_1.csv",
        ]
    }
    param_dict = {"header": 5,
                  "lindex": 4,
                  "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                            'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    rc_dict = {"intact": [], "control": [], "MN": [], "MN-MSC": []}
    group = ["intact", "control", "MN", "MN-MSC"]
    cre_height_dict = height_pipline_processing(pathdict=total_path_dict, param_dict=param_dict,\
                                                rc_dict=create_dict(group=group))

    # Crest Height Analysis
    violin_plot(group=group, rc_dict=cre_height_dict, dtype="crest")
    # box_plot(group=group,rc_dict=cre_height_dict,dtype="crest")
    print("Max Height of Crest")
    print(anova_test(re_dict=cre_height_dict, dtype="crest"))
    print(rc_dict)

    # Toe Height Analysis-----------------------------------------------------------------
    param_dict_toe = {"header": 5,
                      "lindex": 16,
                      "names": ['Frame', 'SubFrame', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2',
                                'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5']}
    toe_rc_dict = height_pipline_processing(pathdict=total_path_dict, param_dict=param_dict_toe,\
                                            rc_dict=create_dict(group=group))
    violin_plot(group=group, rc_dict=toe_rc_dict, dtype="toe")
    # box_plot(group=group, rc_dict=toe_rc_dict, dtype="toe")
    print("Max Height of Toe")
    print(anova_test(re_dict=toe_rc_dict, dtype="toe"))

    # Crest Amplitude------------------------------------------------------------------
    crest_rc_dict_amp = amplitude_pipline_processing(pathdict=total_path_dict, param_dict=param_dict, \
                                                     rc_dict=create_dict(group=group))
    violin_plot(group=group, rc_dict=crest_rc_dict_amp, dtype="crest_amp")
    # box_plot(group=group, rc_dict=crest_rc_dict_amp, dtype="crest_amp")
    print("Crest Amplitude")
    print(anova_test(re_dict=crest_rc_dict_amp, dtype="crest_amp"))

    # Toe Amplitude-------------------------------------------------------------------------
    toe_rc_dict_amp = amplitude_pipline_processing(pathdict=total_path_dict, param_dict=param_dict_toe, \
                                                   rc_dict=create_dict(group=group))
    violin_plot(group=group, rc_dict=toe_rc_dict_amp, dtype="toe_amp")
    # box_plot(group=group, rc_dict=toe_rc_dict_amp, dtype="toe_amp")
    print("Toe Amplitude")
    print(anova_test(re_dict=toe_rc_dict_amp, dtype="toe_amp"))
