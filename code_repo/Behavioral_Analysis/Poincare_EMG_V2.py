import pyhrv.frequency_domain as fd
import pandas as pd
import neurokit2 as nk
import listfile as li
import os

import pyhrv
import pyhrv.nonlinear as nl
import biosppy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def poincare(group,nni=None,
             rpeaks=None,
             show=True,
             figsize=None,
             ellipse=True,
             vectors=True,
             legend=True,
             marker='o',):
    # Check input values
    nn = pyhrv.utils.check_input(nni, rpeaks)

    # Prepare Poincaré data
    x1 = np.asarray(nn[:-1])
    x2 = np.asarray(nn[1:])

    # SD1 & SD2 Computation
    sd1 = np.std(np.subtract(x1, x2) / np.sqrt(2))
    sd2 = np.std(np.add(x1, x2) / np.sqrt(2))

    # Area of ellipse
    area = np.pi * sd1 * sd2

    # Prepare figure
    if figsize is None:
        figsize = (6, 6)
    fig = plt.figure(figsize=figsize)
    fig.tight_layout()
    ax = fig.add_subplot(111)

    ax.set_title(r'$Poincar\acute{e}$')
    ax.set_ylabel('$NNI_{i+1}$ [ms]')
    ax.set_xlabel('$NNI_i$ [ms]')
    ax.set_xlim([-2000, 2000])
    ax.set_ylim([-2000, 2000])
    ax.grid(False)
    # ax.plot(x3, x4, 'c%s' % marker, markersize=2, alpha=0.5, zorder=3)
    # sns.jointplot(x=x1, y=x2, ax=ax)
    # sns.relplot(x=x1, y=x2, ax=ax)
    # g = sns.jointplot(x=x1, y=x2, kind="kde", color="lightcoral",shade_lowest=False, n_levels=200,xlim=(-400,400),ylim=(-400,400))
    # g.plot_joint(plt.scatter,c="silver",s=30,linewidth=1,marker="+")

    # h = sns.jointplot(x=x1, y=x2, color="sandybrown",xlim=(-400,400),ylim=(-400,400)).plot_joint(sns.kdeplot, zorder=0, n_levels=2000)
    # plt.xlim([-2000, 2000])
    # plt.ylim([-2000, 2000])
    # sns.jointplot(x=x1, y=x2, kind="hex", color="sandybrown",xlim=(-400,400),ylim=(-400,400))
    # g = sns.jointplot(x=x1, y=x2, color="indianred",ratio=5,kind="hist",xlim=(-400,400),ylim=(-400,400))
    # h = g.plot_joint(plt.scatter,c="dimgrey",linewidth=1,s=3,alpha=0.01)
    # h.plot_joint(sns.jointplot,color="darksalmon",kind="hist")
    limit = 0
    if group[-1] == '1':
        limit = 450
    elif group[-1] == '2':
        limit = 400
    sns.jointplot(x=x1, y=x2, space=0, color="indianred", xlim=(-limit,limit),ylim=(-limit,limit),marginal_ticks=True,
                  marginal_kws=dict(bins=800, rug=True))
    # sns.jointplot(x=x1, y=x2, space=0, color="indianred").plot_joint(sns.kdeplot, zorder=0, n_levels=6)
    # sns.jointplot(x=x1, y=x2, kind="resid")
    # sns.scatterplot(x1,x2, ax=ax)
    # ax.plot(x1, x2, 'm%s' % marker, markersize=2, alpha=0.5, zorder=3)
    # sns.stripplot(x1, x2)

    # Compute mean NNI (center of the Poincaré plot)
    nn_mean = np.mean(nn)

    # Draw poincaré ellipse
    if ellipse:
        ellipse_ = mpl.patches.Ellipse((nn_mean, nn_mean), sd1 * 2, sd2 * 2, angle=-45, fc='k', zorder=1)
        ax.add_artist(ellipse_)
        ellipse_ = mpl.patches.Ellipse((nn_mean, nn_mean), sd1 * 2 - 1, sd2 * 2 - 1, angle=-45, fc='lightyellow',
                                       zorder=1)
        ax.add_artist(ellipse_)
    # Add poincaré vectors (SD1 & SD2)
    if vectors:
        arrow_head_size = 3
        na = 4
        a1 = ax.arrow(
            nn_mean, nn_mean, (-sd1 + na) * np.cos(np.deg2rad(45)), (sd1 - na) * np.sin(np.deg2rad(45)),
            head_width=arrow_head_size, head_length=arrow_head_size, fc='g', ec='g', zorder=4, linewidth=1.5)
        a2 = ax.arrow(
            nn_mean, nn_mean, (sd2 - na) * np.cos(np.deg2rad(45)), (sd2 - na) * np.sin(np.deg2rad(45)),
            head_width=arrow_head_size, head_length=arrow_head_size, fc='b', ec='b', zorder=4, linewidth=1.5)
        a3 = mpl.patches.Patch(facecolor='white', alpha=0.0)
        a4 = mpl.patches.Patch(facecolor='white', alpha=0.0)
        ax.add_line(mpl.lines.Line2D(
            (min(nn), max(nn)),
            (min(nn), max(nn)),
            c='b', ls=':', alpha=0.6))
        ax.add_line(mpl.lines.Line2D(
            (nn_mean - sd1 * np.cos(np.deg2rad(45)) * na, nn_mean + sd1 * np.cos(np.deg2rad(45)) * na),
            (nn_mean + sd1 * np.sin(np.deg2rad(45)) * na, nn_mean - sd1 * np.sin(np.deg2rad(45)) * na),
            c='g', ls=':', alpha=0.6))
        # Add legend
        if legend:
            ax.legend(
                [a1, a2, a3, a4],
                ['SD1: %.3f$ms$' % sd1, 'SD2: %.3f$ms$' % sd2, 'S: %.3f$ms^2$' % area, 'SD1/SD2: %.3f' % (sd1 / sd2)],
                framealpha=1)
    # Show plot
    fig1 = plt.figure(1)
    #fig1.savefig(r'C:/Users/Giraffe/Desktop/fig/poincare_1_{}.png'.format(group), dpi=300)
    fig2 = plt.figure(2)
    fig2.savefig(r'C:/Users/Giraffe/Desktop/fig/{}/{}.png'.format(group[:3],group[:5] + '_' + group[12:]), dpi=300)
    plt.close(fig1)
    plt.close(fig2)

    # if show:
    #     plt.show()
    #print('ok')
    # Output
    args = (fig, sd1, sd2, sd2 / sd1, area)
    names = ('poincare_plot', 'sd1', 'sd2', 'sd_ratio', 'ellipse_area')
    return biosppy.utils.ReturnTuple(args, names)

# path = li.command_generate('G31')
# for i in path:
#     gr = i[4:-4]
#     rawdatan = pd.read_csv(i)
#     #plt.plot(range(len(rawdatan)), rawdatan)
#     #plt.savefig(r'C:/Users/Giraffe/Desktop/fig/rawdatan_{}.png'.format(gr), dpi=300)
#     #plt.show()
#     #plt.close()
#     results2 = poincare(gr,rawdatan)

def mo_loc(array):
    target = -1
    while array[target] != '\\':
        target -= 1
    return target
def mooaision_intergrate(group_name):
    path = li.command_generate(group_name)
    for i in path:
        start = mo_loc(i)+1
        gr = group_name + i[start+4:-4]
        print(gr)
        rawdatan = pd.read_csv(i)
        # plt.plot(range(len(rawdatan)), rawdatan)
        # plt.savefig(r'C:/Users/Giraffe/Desktop/fig/rawdatan_{}.png'.format(gr), dpi=300)
        # plt.show()
        # plt.close()
        results2 = poincare(gr, rawdatan)

#mooaision_intergrate('G31')
#print(mo_loc('C:/Users/Giraffe/Desktop/fig/G31at_Poincare\\G31\\File10.btn_m_4.png'))
array_group = os.listdir('D:\data\pack\Poincare')
mooaision_intergrate('Tr2')
# mooaision_intergrate('G31')
# mooaision_intergrate('E33')
# mooaision_intergrate('B90')
# mooaision_intergrate('C55')
# for group in array_group:
#     print('processing:{}'.format(group))
#     mooaision_intergrate(group)






# intact Group
# intact TA
# rawdatan = pd.read_csv('D:\\data\\pack\\Poincare\\B88\\B88_22.btn_m_12.csv')
# # plt.plot(range(len(rawdatan)), rawdatan)
# # plt.savefig(r'C:/Users/Giraffe/Desktop/fig/rawdatan_{}.png'.format(gr),dpi = 300)
# # plt.show()
# results2 = poincare('check',rawdatan)

# # intact GS
# rawdatanGS = pd.read_csv(r"..Poincare\B88\B88_22.btn_m_11.csv")
# results3 = poincare(rawdatanGS)
#
# # Control
# rawdatactrlTA = pd.read_csv(r"./Data/EMG/ZYM/20211102/control/m04_1.csv")
# # results4 = poincare(rawdatactrlTA)
#
# rawdatactlGS = pd.read_csv(r"./Data/EMG/ZYM/20211102/control/m08_2.csv")
# # results5 = poincare(rawdatactlGS)
#
# # GABA
# rawdatagabaTA = pd.read_csv(r"./Data/EMG/ZYM/20211102/gaba/m05_1.csv")
# # results6 = poincare(rawdatagabaTA)
#
# rawdatagabaGS = pd.read_csv(r"./Data/EMG/ZYM/20211102/gaba/m02_2.csv")
# # results7 = poincare(rawdatagabaGS)
#
# # DOPA
# rawdatadopaTA = pd.read_csv(r"./Data/EMG/ZYM/20211102/dopa/m08_1.csv")
# # results8 = poincare(rawdatadopaTA)
#
# rawdatadopaGS = pd.read_csv(r"./Data/EMG/ZYM/20211102/dopa/m07_2.csv")
# # results9 = poincare(rawdatadopaGS)
#
# # ROS
# rawdatarosTA = pd.read_csv(r"./Data/EMG/ZYM/20211102/ros/m02_1.csv")
#
# # results10 = poincare(rawdatarosTA)
#
# rawdatarosGS = pd.read_csv(r"./Data/EMG/ZYM/20211102/ros/m04_2.csv")[18000:]


# results11 = poincare(rawdatarosGS)


# results = poincare(rawdatadopaTA, nnii=rawdatagabaTA)
# print(results['sd1'])
# results2 = poincare(rawdata2)

# ls1cubic = [i**3 for i in ls1]
# new_ls = []
# for i in range(len(ls1)):
#     if ls1[i]**3 not in ls1cubic:
#         new_ls.append(ls1[i])
#     else:
#         continue
#
# print(ls1)
# # Load NNI sample series
# nni = pyhrv.utils.load_sample_nni()
# print(nni)
#
# # Compute the PSD and frequency domain parameters using the NNI series
# result = fd.welch_psd(ls1)
#
# # Access peak frequencies using the key 'fft_peak'
# print(result['fft_peak'])
