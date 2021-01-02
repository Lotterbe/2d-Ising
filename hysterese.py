import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from Metropolis import Metropolis, Observables



def hysterese_measuring(external_field_list, beta=0.49):
    print('Yes!')
    # 0 ist schon 'drin'
    # [0.25 ... 1, ... 0.25, 0, -0.25, ... -1, ... -0.25, 0.25, ... 1]
    magneti = []
    magneti_err = []
    counter = 0
    metro = Metropolis(*(128, 128), beta=beta, flip=False)
    metro.itersteps = 2200 * metro.total_number_of_points
    metro.first_skip = 200 * metro.total_number_of_points
    metro.skip = 100 * metro.total_number_of_points
    metro.reset()
    configs = metro.start_simulation()
    observables = Observables(configs, beta=beta)
    observables.nabs_magnetisation()
    magneti_err.append(observables.jackknife(observables.nabs_m_per_config, 10))
    magneti.append(observables.nabs_m_average)
    #metro.itersteps = 1020 * metro.total_number_of_points
    #metro.first_skip = 20 * metro.total_number_of_points
    #metro.skip = 10 * metro.total_number_of_points
    for b_field in external_field_list:
        print('Start measuring...!')
        print(counter)
        metro.reset()
        metro.b_ext = b_field
        configsneu = metro.start_simulation()
        observables.all_configs = configsneu
        magneti_err.append(observables.jackknife(observables.nabs_m_per_config, 10))
        # b_ext wird fuer magnetisation nicht benoetigt
        #observables.b_ext() = b_field
        observables.nabs_magnetisation()
        magneti.append(observables.nabs_m_average)
        filename = 'Analyse/128x128/Hysterese/' + '128x128' + 'lattice_beta_' \
                           + str(beta).replace('.', '') + 'external_field_' + str(b_field)
        counter += 1
    np.savez_compressed(filename, x=external_field_list, y=magneti, yerr=magneti_err)
    return magneti, magneti_err


def hysterese_plot(direc, beta=0.49, external_b_field_list=[0]):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    filepart = direc
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename = filepart + '128x128' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_0.15' + '.npz'
    data = np.load(filename)
    external_b_field = external_b_field_list
    y_data = data['y']
    y_err = data['yerr']
    plt.rcParams['figure.figsize'] = 16, 9
    legend = r'Datenpunkte' + '\n'+ r'$\beta$ = ' + str(beta)
    plt.plot(external_b_field[0], y_data[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data, yerr=y_err, fmt='-o', ecolor='red', label=legend, zorder = 1)
    #plt.axhline(y=0, xmin=-0.2, xmax=2, color='black', linestyle='dashed')
    #plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black', linestyle='dashed')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '128x128', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'Hysterese_' + '128x128' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201208_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201207_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname)
    plt.close()
    
def hysterese_plot_two(direc1, direc2, beta=0.49, external_b_field_list=[0]):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    filepart1 = direc1
    filepart2 = direc2
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename1 = filepart1 + '128x128' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '256x256' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_err1 = data1['yerr']
    y_data2 = data2['y']
    y_err2 = data2['yerr']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'128x128' 
    legend2 = r'256x256' 
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data1, yerr=y_err1, color = 'blue', fmt='-o', ecolor='red', label=legend1, zorder = 1)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data2, yerr=y_err2, color = 'purple', fmt='-o', ecolor='red', label=legend2, zorder = 1)
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'$\beta$ = ' + str(beta), title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/256x256/Hysterese/'  + 'VergleichGitterHysterese_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname)
    plt.close()
    
def hysterese_plot_three(direc1, direc2, direc3, beta=0.49, external_b_field_list=[0]):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename1 = filepart1 + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '128x128' + 'lattice_beta_' \
                        + str(0.45).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '128x128' + 'lattice_beta_' \
                        + str(0.43).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_err1 = data1['yerr']
    y_data2 = data2['y']
    y_err2 = data2['yerr']
    y_data3 = data3['y']
    y_err3 = data3['yerr']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'$\beta$ = 0.49' 
    legend2 = r'$\beta$ = 0.45'
    legend3 = r'$\beta$ = 0.43'
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data1, yerr=y_err1, color = 'blue', fmt='-o', ecolor='red', label=legend1, zorder = 1)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data2, yerr=y_err2, color = 'purple', fmt='-o', ecolor='red', label=legend2, zorder = 1)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data3, yerr=y_err3, color = 'dodgerblue', fmt='-o', ecolor='red', label=legend3, zorder = 1)
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'128x128', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'VergleichBetaHysterese' + '.pdf'
    plt.savefig(plotname)
    plt.close()

    
def hysterese_plot_newcurve(direc, beta=0.49, external_b_field_list=[0]):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    filepart = direc
    counter = 0
    print(counter)
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename = filepart + '128x128' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_0.15' + '.npz'
    data = np.load(filename)
    external_b_field = external_b_field_list
    y_data = data['y']
    y_err = data['yerr']
    plt.rcParams['figure.figsize'] = 16, 9
    legend = r'Datenpunkte' + '\n'+ r'$\beta$ = ' + str(beta)
    while counter != 5:
        if counter < 4:
            plt.plot(external_b_field[counter], y_data[counter], 'D', color='black', zorder = 2)
        if counter == 4:
            plt.plot(external_b_field[counter], y_data[counter], 'D', color='black', label='Neukurve', zorder = 2)
        counter += 1
        print(counter)
    plt.errorbar(x=external_b_field, y=y_data, yerr=y_err, fmt='-o', ecolor='red', label=legend, zorder = 1)
    #plt.axhline(y=0, xmin=-0.2, xmax=2, color='black', linestyle='dashed')
    #plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black', linestyle='dashed')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '128x128', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'HystereseNeukurve_' + '128x128' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201208_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201207_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname)
    plt.close()


b_fields = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12,
            0.13, 0.14, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04,
            0.03, 0.02, 0.01, 0, -0.01, -0.02, -0.03, -0.04, -0.05, -0.06, -0.07,
            -0.08, -0.09, -0.1, -0.11, -0.12, -0.13, -0.14, -0.15,  -0.14, -0.13,
            -0.12, -0.11, -0.10, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03,
            -0.02, -0.01,0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
            0.1, 0.11, 0.12, 0.13, 0.14, 0.15]
            #0.16, 0.17, 0.18, 0.19, 0.2, 0.19, 0.18, 0.17, 0.16,
            #0.15,
            #-0.16, -0.17,
            #-0.18, -0.19, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15,
            #ä, 0.16, 0.17, 0.18, 0.19, 0.2
b_fields_smaller = [0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 
                    0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125,
            0.13, 0.135, 0.14, 0.145, 0.15, 0.145, 0.14, 0.145, 0.13, 0.125, 0.12, 0.115, 0.11, 0.105, 0.10, 
            0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045, 
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.105, -0.11, 
            -0.115, -0.12, -0.125, -0.13, -0.135, -0.14, -0.145, -0.15, -0.145, -0.14, -0.135, -0.13, -0.125,
            -0.12, -0.115, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06, 
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 
            0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15]

b_fields_smaller_plot = [0, 0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 
                    0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125,
            0.13, 0.135, 0.14, 0.145, 0.15, 0.145, 0.14, 0.145, 0.13, 0.125, 0.12, 0.115, 0.11, 0.105, 0.10, 
            0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045, 
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.105, -0.11, 
            -0.115, -0.12, -0.125, -0.13, -0.135, -0.14, -0.145, -0.15, -0.145, -0.14, -0.135, -0.13, -0.125,
            -0.12, -0.115, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06, 
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 
            0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15]

b_fields_variation = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.105, 0.10, 
            0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045, 
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.15, -0.11, 
            -0.12, -0.13, -0.14, -0.15,  -0.14, -0.13, -0.12, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06, 
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 
            0.09, 0.095, 0.1, 0.12, 0.13, 0.14, 0.15]
beta_list = [0.43, 0.45, 0.49]
#magneti_vals, magneti_err = hysterese_measuring(b_fields_smaller)
#print(magneti_vals)
#werte aus der letzten hysterese
#[0.8971023559570312, 0.9008499145507812, 0.9068191528320313, 0.9094329833984375, 0.9121749877929688, 0.9152801513671875, 0.9181655883789063, 0.92039794921875, 0.9223312377929688, 0.9234466552734375, 0.9276473999023438, 0.9283401489257812, 0.9304168701171875, 0.9325439453125, 0.933148193359375, 0.9351364135742187, 0.9335189819335937, 0.9317977905273438, 0.9310470581054687, 0.928314208984375, 0.927032470703125, 0.9248870849609375, 0.9229385375976562, 0.9201507568359375, 0.9174057006835937, 0.916278076171875, 0.9128402709960938, 0.9082656860351562, 0.905029296875, 0.9004776000976562, 0.8964508056640625, 0.8905487060546875, 0.880438232421875, 0.5385879516601563, -0.8015274047851563, -0.9154510498046875, -0.9184188842773438, -0.9207611083984375, -0.9224273681640625, -0.924359130859375, -0.926373291015625, -0.9281875610351562, -0.93013916015625, -0.9312225341796875, -0.932403564453125, -0.934967041015625, -0.9342330932617188, -0.9318817138671875, -0.9301345825195313, -0.9278610229492188, -0.9264846801757812, -0.9249588012695312, -0.9225845336914062, -0.920074462890625, -0.9178390502929688, -0.9155426025390625, -0.911810302734375, -0.90841064453125, -0.9046340942382812, -0.9017913818359375, -0.8979049682617187, -0.8902740478515625, -0.8741226196289062, -0.6992218017578125, 0.6101470947265625, 0.9152618408203125, 0.9171249389648437, 0.9204254150390625, 0.9225296020507813, 0.9237762451171875, 0.9270477294921875, 0.928912353515625, 0.9306808471679687, 0.9312484741210938, 0.93338623046875, 0.9351638793945313]
#hysterese_plot('Analyse/128x128/Hysterese/', beta=0.43, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot('Analyse/256x256/Hysterese/Neu_201204/', beta=0.49, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_newcurve('Analyse/128x128/Hysterese/', beta=0.43, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_two('Analyse/128x128/Hysterese/', 'Analyse/256x256/Hysterese/Neu_201204/', external_b_field_list=b_fields_smaller_plot)
hysterese_plot_three('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', external_b_field_list=b_fields_smaller_plot)
