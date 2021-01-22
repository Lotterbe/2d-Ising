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
    counter = 0
    metro = Metropolis(*(512, 512), beta=beta, flip=False)
    metro.itersteps = 2200 * metro.total_number_of_points
    metro.first_skip = 200 * metro.total_number_of_points
    metro.skip = 100 * metro.total_number_of_points
    metro.reset()
    configs = metro.start_simulation()
    observables = Observables(configs, beta=beta)
    observables.nabs_magnetisation()
    magneti.append(observables.nabs_m_average)
    #metro.itersteps = 1020 * metro.total_number_of_points
    #metro.first_skip = 20 * metro.total_number_of_points
    #metro.skip = 10 * metro.total_number_of_points
    # Leas Visualisierung: Bedingung
    #config_array = np.array(configs)
    config_array = [configs[-1]] 
    for b_field in external_field_list:
        #print('Start measuring...!')
        print(counter)
        metro.reset()
        metro.b_ext = b_field
        configsneu = metro.start_simulation()
        config_array.append(configsneu[-1])
        # Leas Visualisierung
        #config_array = np.append(config_array, configsneu, axis=0)
        observables.all_configs = configsneu
        # b_ext wird fuer magnetisation nicht benoetigt
        #observables.b_ext() = b_field
        observables.nabs_magnetisation()
        magneti.append(observables.nabs_m_average)
        #filename = 'Analyse/128x128/Hysterese/' + '128x128' + 'lattice_beta_' \
        #                   + str(beta).replace('.', '') + 'external_field_' + str(b_field)
        #filename = 'Analyse/128x128/Hysterese/Visual/' + '128x128' + 'lattice_beta_'  \
        #                + str(beta).replace('.', '') + 'external_field_' + str(b_field)
        #Insert your file path in the first ''
        filename = 'Analyse/512x512/Hysterese/' + '210115_' + '512x512' + 'lattice_beta_' \
                           + str(beta).replace('.', '') + 'external_field_' + str(b_field)
        counter += 1
    np.savez_compressed(filename, x=external_field_list, y=magneti, configs=config_array)


def hysterese_plot(direc, beta=0.49, external_b_field_list=[0]):
    """
e size
    :param b_field: all values for external b-field
    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: latticlue of magnetic field
    """
    filepart = direc
    filename = filepart + '256x256' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + '128x128' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_0.15' + '.npz'
    data = np.load(filename)
    external_b_field = external_b_field_list
    y_data = data['y']
    y_err = data['yerr']
    plt.rcParams['figure.figsize'] = 16, 9
    legend = r'Datenpunkte' + '\n'+ r'$\beta$ = ' + str(beta)
    plt.plot(external_b_field[0], y_data[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.errorbar(x=external_b_field, y=y_data, yerr=y_err, fmt='-o', ecolor='red', label=legend, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '(256x256)', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    #plotname = 'Analyse/128x128/Hysterese/'  + 'Hysterese_' + '128x128' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201208_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201207_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
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
    #filename2 = filepart2 + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename1 = filepart1 + '210107_20Konfigs_'  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '210114_' + '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'$Run1$'
    legend2 = r'$Run2$'
    legend3 = r'$Run3$'
    #bD1, bU1, bD2, bU2, bD3, bU3 = hyst_width_var(direc1, direc2, direc3, external_b_field, txtFile=True)
    hyst_width_var(direc1, direc2, direc3, external_b_field, txtFile=True)
    #plt.fill_between([bD1, bU1], -1, 1,  color='papayawhip')
    #plt.fill_between([bD2, bU2], -1, 1,  color='papayawhip')
    #plt.fill_between([bD3, bU3], -1, 1,  color='papayawhip')
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.plot(external_b_field, y_data1, '-o', color = 'blue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3,'-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(128x128), $\beta=0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    #plt.tight_layout()
    plotname = 'Analyse/128x128/Hysterese/'  + 'TestHystereseBreite' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_Runs256(direc1, direc2, direc3, beta=0.49, external_b_field_list=[0]):
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
    filename1 = filepart1 + '210112_Run1_'  + '256x256' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_' + '256x256' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_015'  + '.npz'
    filename3 = filepart3 +'210112_Run2_'  + '256x256' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'$Run1$'
    legend2 = r'$Run2$'
    legend3 = r'$Run3$'
    hyst_width_var256(direc1, direc2, direc3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.plot(external_b_field, y_data1, '-o', color = 'blue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3,'-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(256x256), $\beta=0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    #plt.tight_layout()
    plotname = 'Analyse/256x256/Hysterese/'  + 'TestHystereseBreite' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_Runs64(direc1, direc2, direc3, beta=0.49, external_b_field_list=[0]):
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
    filename1 = filepart1 + '210114_Run1_'  + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_' + '64x64' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 +'210114_Run2_'  + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'$Run1$'
    legend2 = r'$Run2$'
    legend3 = r'$Run3$'
    hyst_width_var64(direc1, direc2, direc3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.plot(external_b_field, y_data1, '-o', color = 'blue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3,'-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(64x64), $\beta=0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    #plt.tight_layout()
    plotname = 'Analyse/64x64/Hysterese/'  + 'TestHystereseBreite' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_Runs512(direc1, direc2, direc3, beta=0.49, external_b_field_list=[0]):
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
    filename1 = filepart1 + '210106_'  + '512x512' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '210115_' + '512x512' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 +'lea_run'  + '512x512' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'Run1'
    legend2 = r'Run2'
    legend3 = r'Run3'
    hyst_width_var512(direc1, direc2, direc3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.plot(external_b_field, y_data1, '-o', color = 'blue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3,'-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(512x512), $\beta=0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    #plt.tight_layout()
    plotname = 'Analyse/512x512/Hysterese/'  + 'VergleichHystereseRuns_512' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_four(direc1, direc2, direc3, direc4, beta=0.49, external_b_field_list=[0]):
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
    filepart4 = direc4
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename2 = filepart2 + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename1 = filepart1  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_'+ '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '210107_20Konfigs_' + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename4 = filepart4 + '210114_' + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'Run1'
    legend2 = r'Run2'
    legend3 = r'Run3'
    legend4 = r'Run4'
    # Calculation of the mean value of the des-/ascending curve is in
    hyst_width_var(direc1, direc2, direc3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data4[0], 'D', color='black', label='Startpunkt', zorder = 2)
    #plt.errorbar(x=external_b_field, y=y_data2, yerr=y_err2, color = 'purple', fmt='-o', ecolor='red', label=legend2, zorder = 1)
    #plt.errorbar(x=external_b_field, y=y_data3, yerr=y_err3, color = 'hotpink', fmt='-o', ecolor='red', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data1, '-o', color = 'royalblue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3, '-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data4, '-o', color = 'orange', label=legend4, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '(128x128)\n' r'$\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'VergleichRuns128x128' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_four64(direc1, direc2, direc3, direc4, beta=0.49, external_b_field_list=[0]):
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
    filepart4 = direc4
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename2 = filepart2 + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename1 = filepart1  + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_'+ '64x64' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '210114_Run1_' + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename4 = filepart4 + '210114_Run2_' + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'Run1'
    legend2 = r'Run2'
    legend3 = r'Run3'
    legend4 = r'Run4'
    # Calculation of the mean value of the des-/ascending curve is in
    hyst_width_var64(direc1, direc2, direc3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data4[0], 'D', color='black', label='Startpunkt', zorder = 2)
    #plt.errorbar(x=external_b_field, y=y_data2, yerr=y_err2, color = 'purple', fmt='-o', ecolor='red', label=legend2, zorder = 1)
    #plt.errorbar(x=external_b_field, y=y_data3, yerr=y_err3, color = 'hotpink', fmt='-o', ecolor='red', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data1, '-o', color = 'royalblue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'purple', label=legend2, zorder = 1)
    plt.plot(external_b_field, y_data3, '-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data4, '-o', color = 'orange', label=legend4, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(64x64), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/64x64/Hysterese/'  + 'VergleichRuns64x64' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hysterese_plot_fourKonfigs(direc1, direc2, direc3, direc4, beta=0.49, external_b_field_list=[0]):
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
    filepart4 = direc4
    filename1 = filepart1 + '210107_15Konfigs_'+ '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename2 = filepart2 + '210107_20Konfigs_'+ '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '210107_30Konfigs_'+ '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename4 = filepart4 + '210113_40Konfigs_'+ '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    external_b_field = external_b_field_list
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend1 = r'15'
    legend2 = r'20'
    legend3 = r'30'
    legend4 = r'40'
    # Calculation of the mean value of the des-/ascending curve is in
    hyst_width_calc_three(filepart1, filepart2, filepart3, external_b_field, txtFile=True)
    plt.plot(external_b_field[0], y_data1[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data2[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data3[0], 'D', color='black', zorder = 2)
    plt.plot(external_b_field[0], y_data4[0], 'D', color='black', label='Startpunkt', zorder = 2)
    plt.plot(external_b_field, y_data1, '-o', color = 'blue', label=legend1, zorder = 1)
    plt.plot(external_b_field, y_data2, '-o', color = 'hotpink', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data3, '-o', color = 'purple', label=legend3, zorder = 1)
    plt.plot(external_b_field, y_data4, '-o', color = 'orange', label=legend4, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = r'(128x128), $\beta = 0.49$', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'VergleichKonfigsHysterese_Neu' + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
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
    #filename = filepart + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    #filename = filepart + 'Nochmal_' + '256x256' + 'lattice_beta_' \
    #                    + str(beta).replace('.', '') + 'external_field_015'  + '.npz'
    filename = filepart + '128x128' + 'lattice_beta_' \
                        + str(beta).replace('.', '') + 'external_field_0.15' + '.npz'
    data = np.load(filename)
    external_b_field = external_b_field_list
    y_data = data['y']
    plt.rcParams['figure.figsize'] = 16, 9
    legend = r'Datenpunkte' 
    plt.plot(external_b_field[0:4], y_data[0:4], '-D', color='black', zorder = 2, label = 'Neukurve')
    plt.plot(external_b_field[56:65], y_data[56:65], '-D', color='hotpink', zorder = 2, label = 'Abfallend')
    plt.plot(external_b_field[116:125], y_data[116:125], '-D', color='purple', zorder = 2, label = 'Aufsteigend')
    plt.plot(external_b_field, y_data, '-o', label=legend, zorder = 1)
    plt.axhline(y=0, xmin=-0.2, xmax=2, color='black')
    plt.axvline(x=0, ymin=-1.2, ymax=1.2, color='black')
    plt.xlabel(r'H', fontsize=24)
    plt.ylabel(r'M', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = r'(128x128), $\beta$ = 0.43', title_fontsize = 24, fontsize=24)
    #plt.legend(loc='best', framealpha=0.5, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'HystereseNeukurve_' + '128x128' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201208_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    #plotname = 'Analyse/256x256/Hysterese/Neu_201204/'  + 'Hysterese_201207_' + '256x256' + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def hyst_width_var(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filename1 = filepart1 + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    #filename2 = filepart2 + 'Nochmal_' + '128x128' +  'lattice_beta_' \
    #                    + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename2 = filepart2 + '210114_' + '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '210107_20Konfigs_'  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    y_data1 = data1['y']
    y_err1 = data1['yerr']
    y_data2 = data2['y']
    y_err2 = data2['yerr']
    y_data3 = data3['y']
    y_err3 = data3['yerr']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data2[131:134])
    '''
    external_b_field = external_b_field_list
    # Mean of the bfield values
    # filepart1 + '128x128' +
    b_M1_down = np.mean(external_b_field[72:76])
    b_M1_up = np.mean(external_b_field[129:133])
    # filepart2 + 'Nochmal_'
    b_M2_down = np.mean(external_b_field[72:76])
    b_M2_up = np.mean(external_b_field[132:136])
    # '210114_'
    b_M3_down = np.mean(external_b_field[71:74])
    b_M3_up = np.mean(external_b_field[131:134])
    # filepart3 + '210107_20Konfigs_'
    b_M4_down = np.mean(external_b_field[69:73])
    b_M4_up = np.mean(external_b_field[131:135])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    W4 = b_M4_up + abs(b_M4_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3))
    SD_W = np.std((W1, W2, W3))
    # Mean b_field values of the descending and ascending curves
    b_DownM = np.mean((b_M1_down, b_M2_down, b_M3_down))
    b_DownSD = np.std((b_M1_down, b_M2_down, b_M3_down))
    b_UpM = np.mean((b_M1_up, b_M2_up, b_M3_up))
    b_UpSD = np.std((b_M1_up, b_M2_up, b_M3_up))
    if (txtFile == True):
        np.savetxt('Analyse/128x128/Hysterese/' + 'WidthData(128x128)_4Runs.txt', \
                   (W1, W2, W3, W4, M_W, SD_W, b_DownM, b_UpM), \
                    header = '-, Nochmal_, 210114_, 210107_20Konfigs_, MeanWidth, StdDeviWidth, DescendingMeanBField, AscendingMeanBField' )
    #return M_W, SD_W, b_M2_down, b_M2_up
    #return b_DownSD, b_UpSD, b_M2_down, b_M2_up
    #return b_M1_down, b_M1_up, b_M2_down, b_M2_up, b_M3_down, b_M3_up

def hyst_width_var256(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filename1 = filepart1 + '210112_Run1_'  + '256x256' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_' + '256x256' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_015'  + '.npz'
    filename3 = filepart3 +'210112_Run2_'  + '256x256' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data3[129:134])
    '''
    external_b_field = external_b_field_list
    # Mean of the bfield values
    # '210112_Run1_'
    b_M1_down = np.mean(external_b_field[69:73])
    b_M1_up = np.mean(external_b_field[130:134])
    # 'Nochmal_'
    b_M2_down = np.mean(external_b_field[68:73])
    b_M2_up = np.mean(external_b_field[128:133])
    # '210112_Run2_'
    b_M3_down = np.mean(external_b_field[68:73])
    b_M3_up = np.mean(external_b_field[129:134])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3))
    SD_W = np.std((W1, W2, W3))
    # Mean b_field values of the descending and ascending curves
    b_DownM = np.mean((b_M1_down, b_M2_down, b_M3_down))
    b_DownSD = np.std((b_M1_down, b_M2_down, b_M3_down))
    b_UpM = np.mean((b_M1_up, b_M2_up, b_M3_up))
    b_UpSD = np.std((b_M1_up, b_M2_up, b_M3_up))
    if (txtFile == True):
        np.savetxt('Analyse/256x256/Hysterese/' + 'WidthData(256x256)_3Runs.txt', \
                   (W1, W2, W3, M_W, SD_W, b_DownM, b_UpM), \
                    header = 'Run1, Nochmal_, Run2, MeanWidth, StdDeviWidth, DescendingMeanBField, AscendingMeanBField' )

def hyst_width_var64(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filename1 = filepart1 + '210114_Run1_'  + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + 'Nochmal_' + '64x64' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 +'210114_Run2_'  + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename4 = filepart3 + '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data4[132:135])
    '''
    external_b_field = external_b_field_list
    # Mean of the bfield values
    # '210112_Run1_'
    b_M1_down = np.mean(external_b_field[71:75])
    b_M1_up = np.mean(external_b_field[130:133])
    # 'Nochmal_'
    b_M2_down = np.mean(external_b_field[69:72])
    b_M2_up = np.mean(external_b_field[132:135])
    # '210112_Run2_'
    b_M3_down = np.mean(external_b_field[70:73])
    b_M3_up = np.mean(external_b_field[133:136])
    # '-'
    b_M4_down = np.mean(external_b_field[72:76])
    b_M4_up = np.mean(external_b_field[132:135])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    W4 = b_M4_up + abs(b_M4_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3))
    SD_W = np.std((W1, W2, W3))
    # Mean b_field values of the descending and ascending curves
    b_DownM = np.mean((b_M1_down, b_M2_down, b_M3_down))
    b_DownSD = np.std((b_M1_down, b_M2_down, b_M3_down))
    b_UpM = np.mean((b_M1_up, b_M2_up, b_M3_up))
    b_UpSD = np.std((b_M1_up, b_M2_up, b_M3_up))
    if (txtFile == True):
        np.savetxt('Analyse/64x64/Hysterese/' + 'WidthData(64x64)_4Runs.txt', \
                   (W1, W2, W3, W4, M_W, SD_W, b_DownM, b_UpM), \
                    header = 'Run1, Nochmal_, Run2, -, MeanWidth, StdDeviWidth, DescendingMeanBField, AscendingMeanBField' )

def hyst_width_var512(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filename1 = filepart1 + '210106_'  + '512x512' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '210115_' + '512x512' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 +'lea_run'  + '512x512' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data3[129:134])
    '''
    external_b_field = external_b_field_list
    # Mean of the bfield values
    # 'Run1'
    b_M1_down = np.mean(external_b_field[68:73])
    b_M1_up = np.mean(external_b_field[129:134])
    # 'Run2'
    b_M2_down = np.mean(external_b_field[69:74])
    b_M2_up = np.mean(external_b_field[128:134])
    # 'Lea'
    b_M3_down = np.mean(external_b_field[69:74])
    b_M3_up = np.mean(external_b_field[129:134])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3))
    SD_W = np.std((W1, W2, W3))
    # Mean b_field values of the descending and ascending curves
    b_DownM = np.mean((b_M1_down, b_M2_down, b_M3_down))
    b_DownSD = np.std((b_M1_down, b_M2_down, b_M3_down))
    b_UpM = np.mean((b_M1_up, b_M2_up, b_M3_up))
    b_UpSD = np.std((b_M1_up, b_M2_up, b_M3_up))
    if (txtFile == True):
        np.savetxt('Analyse/512x512/Hysterese/' + 'WidthData(512x512)_3Runs.txt', \
                   (W1, W2, W3, M_W, SD_W, b_DownM, b_UpM), \
                    header = 'Run1, Run2, Lea, MeanWidth, StdDeviWidth, DescendingMeanBField, AscendingMeanBField' )

def hyst_width_calc_three(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filepart4 = direc3
    filename1 = filepart1 + '210107_15Konfigs_' + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '210107_20Konfigs_' + '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + '210107_30Konfigs_'  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename4 = filepart4 + '210113_40Konfigs_'  + '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data4[126:130])
    '''
    # Mean of the
    external_b_field = external_b_field_list
    b_M1_down = np.mean(external_b_field[71:75])
    b_M2_down = np.mean(external_b_field[69:73])
    b_M3_down = np.mean(external_b_field[70:74])
    b_M4_down = np.mean(external_b_field[67:70])
    b_M1_up = np.mean(external_b_field[129:133])
    b_M2_up = np.mean(external_b_field[131:135])
    b_M3_up = np.mean(external_b_field[129:133])
    b_M4_up = np.mean(external_b_field[126:131])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    W4 = b_M4_up + abs(b_M4_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3))
    SD_W = np.std((W1, W2, W3))
    # Mean b_field values of the descending and ascending curves
    b_DownM = np.mean((b_M1_down, b_M2_down, b_M3_down))
    b_DownSD = np.std((b_M1_down, b_M2_down, b_M3_down))
    b_UpM = np.mean((b_M1_up, b_M2_up, b_M3_up))
    b_UpSD = np.std((b_M1_up, b_M2_up, b_M3_up))
    if (txtFile == True):
        np.savetxt('Analyse/128x128/Hysterese/' + 'WidthData(128x128)_Konfigs.txt', \
                   (W1, W2, W3, W4, M_W, SD_W), \
                    header = '15K, 20K, 30K, 40K, MeanWidth, StdDeviWidth' )
    #return M_W, SD_W, b_M2_down, b_M2_up
    #return b_DownSD, b_UpSD, b_M2_down, b_M2_up
    #return b_M1_down, b_M1_up, b_M2_down, b_M2_up, b_M3_down, b_M3_up


def hyst_width_calc_beta(direc1, direc2, direc3, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filename1 = filepart1 + '210107_20Konfigs_'+ '128x128' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2  + '128x128' +  'lattice_beta_' \
                        + str(0.45).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3  + '128x128' + 'lattice_beta_' \
                        + str(0.43).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    print(y_data3[58:70])
    print(y_data3[100:110])
    '''
    # Mean of the
    external_b_field = external_b_field_list
    b_M1_down = np.mean(external_b_field[69:73])
    b_M2_down = np.mean(external_b_field[61:65])
    #b_M3_down = np.mean(external_b_field[])
    b_M1_up = np.mean(external_b_field[131:135])
    b_M2_up = np.mean(external_b_field[121:125])
    #b_M3_up = np.mean(external_b_field[])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    if (txtFile == True):
        np.savetxt('Analyse/128x128/Hysterese/' + 'WidthData(128x128)_Betas.txt', \
                   (W1, W2), \
                    header = 'WidthR1, WidthR2' )
    #return M_W, SD_W, b_M2_down, b_M2_up
    #return b_DownSD, b_UpSD, b_M2_down, b_M2_up
    #return b_M1_down, b_M1_up, b_M2_down, b_M2_up, b_M3_down, b_M3_up

def hyst_width_calc(direc1, direc2, direc3, direc4, external_b_field_list, txtFile = False):
    '''
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    filepart4 = direc4
    filename1 = filepart1 + 'Nochmal_'+ '64x64' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15' + '.npz'
    filename2 = filepart2 + '210107_20Konfigs_' + '128x128' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    filename3 = filepart3 + 'Nochmal_'+ '256x256' + 'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_015' + '.npz'
    filename4 = filepart4 + '210106_' + '512x512' +  'lattice_beta_' \
                        + str(0.49).replace('.', '') + 'external_field_0.15'  + '.npz'
    data1 = np.load(filename1)
    data2 = np.load(filename2)
    data3 = np.load(filename3)
    data4 = np.load(filename4)
    y_data1 = data1['y']
    y_data2 = data2['y']
    y_data3 = data3['y']
    y_data4 = data4['y']
    print(y_data1[68:72])
    print(y_data1[132:136])
    # Mean of the y_data
    y_M1_down = np.mean(y_data1[72:76])
    y_M2_down = np.mean(y_data2[72:76])
    y_M3_down = np.mean(y_data3[69:74])
    y_M1_up = np.mean(y_data1[129:134])
    y_M2_up = np.mean(y_data2[132:137])
    y_M3_up = np.mean(y_data3[131:136])
    '''
    # Mean of the
    external_b_field = external_b_field_list
    b_M1_down = np.mean(external_b_field[68:72])
    b_M2_down = np.mean(external_b_field[69:73])
    b_M3_down = np.mean(external_b_field[68:73])
    b_M4_down = np.mean(external_b_field[68:73])
    b_M1_up = np.mean(external_b_field[132:136])
    b_M2_up = np.mean(external_b_field[131:135])
    b_M3_up = np.mean(external_b_field[129:133])
    b_M4_up = np.mean(external_b_field[129:134])
    # Width of the hsterese curves
    W1 = b_M1_up + abs(b_M1_down)
    W2 = b_M2_up + abs(b_M2_down)
    W3 = b_M3_up + abs(b_M3_down)
    W4 = b_M4_up + abs(b_M4_down)
    # Mean and StdDevi of the widths
    M_W = np.mean((W1, W2, W3, W4))
    SD_W = np.std((W1, W2, W3, W4))
    if (txtFile == True):
        np.savetxt('Analyse/256x256/Hysterese/' + 'WidthData.txt', \
                   (W1, W2, W3, W4), \
                    header = '(64x64), (128x128), (256x256), (512x512)' )
    #return M_W, SD_W, b_M2_down, b_M2_up
    #return b_DownSD, b_UpSD, b_M2_down, b_M2_up
    #return b_M1_down, b_M1_up, b_M2_down, b_M2_up, b_M3_down, b_M3_up


def HystereseWidth_plottingAllLats(file1, file2):
    # txt-File zum plotten
    width1 = np.genfromtxt(file1, skip_header=1).T
    # txt-File für Standardabweichung
    data2 = np.genfromtxt(file2, skip_header=1).T
    plt.errorbar(x=[1, 2, 3, 4], y=width1, yerr=data2, fmt='o', color = 'royalblue', ecolor='red', label=r'$\mu\pm\sigma$')
    plt.annotate('(64x64)', xytext=(1+0.05, 0.119-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('(128x128)', xytext=(2+0.05, 0.125-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('(256x256)', xytext=(3+0.05, 0.105-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('(512x512)', xytext=(3.59, 0.107-0.0005), xy = (1, 0.105), fontsize=20)
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    plt.yticks(fontsize=20)
    plt.ylabel('Breite der Hysterese', fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = r'$\beta=0.49$', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Hysterese/'  + 'Hysterese_Breiten_AllMeanEnger.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()

def HystereseWidth_plottingKonfigs(file1, file2):
    # txt-File zum plotten
    width1 = np.genfromtxt(file1, skip_header=1).T
    # txt-File für Standardabweichung
    data2 = np.genfromtxt(file2, skip_header=1).T
    x_points = np.array([1, 2, 3, 4])
    print(width1[0:4])
    plt.errorbar(x=x_points, y=width1[0:4], yerr=data2[4], fmt='o', color = 'royalblue', ecolor='red', label='Datenpunkte')
    plt.annotate('15 Konfigurationen', xytext=(1+0.05, 0.115-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('20 Konfigurationen', xytext=(2+0.05, 0.115-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('30 Konfigurationen', xytext=(3+0.05, 0.110-0.0005), xy = (1, 0.105), fontsize=20)
    plt.annotate('40 Konfigurationen', xytext=(3.25, 0.080-0.0005), xy = (1, 0.105), fontsize=20)
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    plt.yticks(fontsize=20)
    plt.ylabel('Breite der Hysterese', fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = r'(128x128), $\beta=0.49$', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/128x128/Hysterese/'  + 'Hysterese_Breiten_Konfigs_Neu.pdf'
    plt.savefig(plotname, bbox_inches='tight')
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
            0.13, 0.135, 0.14, 0.145, 0.15, 0.145, 0.14, 0.135, 0.13, 0.125, 0.12, 0.115, 0.11, 0.105, 0.10,
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
            0.13, 0.135, 0.14, 0.145, 0.15, 0.145, 0.14, 0.135, 0.13, 0.125, 0.12, 0.115, 0.11, 0.105, 0.10,
            0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.105, -0.11,
            -0.115, -0.12, -0.125, -0.13, -0.135, -0.14, -0.145, -0.15, -0.145, -0.14, -0.135, -0.13, -0.125,
            -0.12, -0.115, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
            0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15]

b_fields_visual = [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
                    0.08, 0.085, 0.09, 0.095, 0.1, 0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
            0.09, 0.095, 0.1]

b_fields_variation = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.105, 0.10,
            0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.15, -0.11,
            -0.12, -0.13, -0.14, -0.15,  -0.14, -0.13, -0.12, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
            0.09, 0.095, 0.1, 0.12, 0.13, 0.14, 0.15]
beta_list = [0.43, 0.45, 0.49]
#hysterese_measuring(b_fields_smaller)
#print(magneti_vals)
#werte aus der letzten hysterese
#[0.8971023559570312, 0.9008499145507812, 0.9068191528320313, 0.9094329833984375, 0.9121749877929688, 0.9152801513671875, 0.9181655883789063, 0.92039794921875, 0.9223312377929688, 0.9234466552734375, 0.9276473999023438, 0.9283401489257812, 0.9304168701171875, 0.9325439453125, 0.933148193359375, 0.9351364135742187, 0.9335189819335937, 0.9317977905273438, 0.9310470581054687, 0.928314208984375, 0.927032470703125, 0.9248870849609375, 0.9229385375976562, 0.9201507568359375, 0.9174057006835937, 0.916278076171875, 0.9128402709960938, 0.9082656860351562, 0.905029296875, 0.9004776000976562, 0.8964508056640625, 0.8905487060546875, 0.880438232421875, 0.5385879516601563, -0.8015274047851563, -0.9154510498046875, -0.9184188842773438, -0.9207611083984375, -0.9224273681640625, -0.924359130859375, -0.926373291015625, -0.9281875610351562, -0.93013916015625, -0.9312225341796875, -0.932403564453125, -0.934967041015625, -0.9342330932617188, -0.9318817138671875, -0.9301345825195313, -0.9278610229492188, -0.9264846801757812, -0.9249588012695312, -0.9225845336914062, -0.920074462890625, -0.9178390502929688, -0.9155426025390625, -0.911810302734375, -0.90841064453125, -0.9046340942382812, -0.9017913818359375, -0.8979049682617187, -0.8902740478515625, -0.8741226196289062, -0.6992218017578125, 0.6101470947265625, 0.9152618408203125, 0.9171249389648437, 0.9204254150390625, 0.9225296020507813, 0.9237762451171875, 0.9270477294921875, 0.928912353515625, 0.9306808471679687, 0.9312484741210938, 0.93338623046875, 0.9351638793945313]
#hysterese_plot('Analyse/128x128/Hysterese/', beta=0.43, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot('Analyse/256x256/Hysterese/Neu_201204/', beta=0.49, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_newcurve('Analyse/128x128/Hysterese/', beta=0.43, external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_three('Analyse/128x128/Hysterese/', 'Analyse/256x256/Hysterese/Neu_201204/', 'Analyse/64x64/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_three('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', external_b_field_list=b_fields_smaller_plot)
hysterese_plot_four('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_four64('Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_fourKonfigs('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_Runs256('Analyse/256x256/Hysterese/', 'Analyse/256x256/Hysterese/Neu_201204/', 'Analyse/256x256/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_Runs64('Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hysterese_plot_Runs512('Analyse/512x512/Hysterese/', 'Analyse/512x512/Hysterese/', 'Analyse/512x512/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hyst_width_var256('Analyse/256x256/Hysterese/', 'Analyse/256x256/Hysterese/Neu_201204/', 'Analyse/256x256/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hyst_width_var64('Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', 'Analyse/64x64/Hysterese/', external_b_field_list=b_fields_smaller_plot)
#hyst_width_var512('Analyse/512x512/Hysterese/', 'Analyse/512x512/Hysterese/', 'Analyse/512x512/Hysterese/', external_b_field_list=b_fields_smaller_plot)


#HystereseWidth_plottingAllLats('Analyse/256x256/Hysterese/WidthMean.txt', 'Analyse/256x256/Hysterese/WidthStd.txt')
#HystereseWidth_plottingKonfigs('Analyse/128x128/Hysterese/WidthData(128x128)_Konfigs.txt', 'Analyse/128x128/Hysterese/WidthData(128x128)_3Runs.txt')
#data = np.genfromtxt('t', skip_header = 1).T

#hyst_width_calc('Analyse/64x64/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/256x256/Hysterese/Neu_201204/', 'Analyse/512x512/Hysterese/', b_fields_smaller_plot)
#hyst_width_var('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', b_fields_smaller_plot, True)
#hyst_width_calc_three('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', b_fields_smaller_plot, True)
#hyst_width_calc_beta('Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', 'Analyse/128x128/Hysterese/', b_fields_smaller_plot, True)
