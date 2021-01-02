import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from Metropolis import Metropolis, Observables


class Ising_Plot:
    def __init__(self, ising):
        fig, ax = plt.subplots()
        self.data = ising
        update_number = len(self.data) - 1
        print(self.data[0])
        init_data = np.where(self.data[0] == -1, 0, 1)
        print(init_data)
        # 'nearest' or 'bilinear'
        # ret = ax.imshow(init_data, interpolation='nearest', cmap=cm.Greys_r)
        im = plt.imshow(init_data, cmap='gist_gray_r', vmin=0, vmax=1)
        print(type(im))

        # [-> pos, ^pos, length, thickness]
        axamp = plt.axes([0.25, .03, 0.50, 0.02])
        # Slider
        samp = Slider(axamp, 'Config number', 0, update_number, valinit=0, valstep=1)

        def update(val):
            # update curve
            # l.set_ydata(val*np.sin(t))
            im.set_data(self.data[int(val)])
            # redraw canvas while idle
            fig.canvas.draw_idle()

        # call update function on slider value change
        samp.on_changed(update)

        plt.show()
        


def lattice_measuring(beta_list, lattice_list, external_field_list):
    """This function starts an simulation and the measuring. If the file,
     in which all will be saved, already exist, this function is NOT needed.
     (Saves time ;) )

    :param beta_list: all beta values for which the observables should be calculated
    :param lattice_list: all lattice sizes which should be computed
    :param external_field_list: values of the magnetic field
    """
    beta = beta_list
    lattice = lattice_list
    external_b_field = external_field_list
    for b_field in external_b_field:
        print('Measuring external magnetic field B = ' + str(b_field))
        for lat in lattice:
            print(r'Measuring lattice size ' + str(lat))
            for b in beta:
                print(r'Measuring $\beta$ = ' + str(b))
                metro = Metropolis(*lat, beta=b, external_field=b_field)
                configs = metro.start_simulation()
                observables = Observables(configs, beta=b)
                observables.measure_observables()
                filename = 'Analyse/256x256/FinalTestVariance/Run3/' +  str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                           + str(b).replace('.', '') + 'external_field_' + str(b_field)
                observables.save_simulation(filename)
                del metro, observables


def make_nice_plot(beta, y_data, y_err, name, legend, lat, b_field):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    plt.rcParams['figure.figsize'] = 16, 9
    plt.errorbar(x=beta, y=y_data, yerr=y_err, fmt='o', label=legend)
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'U', fontsize=24)
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '256x256 Gitter', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Observablen/Plots/' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname)
    plt.close()
    
def make_nice_plot_Ons(beta, y_data, y_err, name, legend, lat, b_field, ons_energy, yang_mag):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    plt.rcParams['figure.figsize'] = 16, 9
    plt.errorbar(x=beta, y=y_data, yerr=y_err, fmt='o', label=legend)
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label='Onsager Energie')
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label='Yang Magnetisierung')
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '256x256, H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Observablen/Neu_201229/Plots/' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()            
                    
def make_nice_plot_Ons_double(beta, y_data1, y_err1, y_data2, y_err2, name, legend1, legend2, lat, b_field, ons_energy, yang_mag):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    plt.rcParams['figure.figsize'] = 16, 9
    plt.errorbar(x=beta, y=y_data1, yerr=y_err1, fmt='o', color='deeppink', label=legend1)
    plt.errorbar(x=beta, y=y_data2, yerr=y_err2, fmt='o', label=legend2)
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label='Onsager Energie')
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label='Yang Magnetisierung')
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
        print(y_err1)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '(256x256), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/FinalTestSkips/' + 'SkipTest_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()
    
def make_nice_plot_Ons_three(beta, y_data1, y_err1, y_data2, y_err2, y_data3, y_err3, name, legend1, legend2, legend3, lat, b_field, ons_energy, yang_mag):
    """

    :param beta: all values for beta
    :param y_data: observable values
    :param y_err: the error for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: for the plot
    :param lat: lattice size
    :param b_field: value of magnetic field
    """
    plt.rcParams['figure.figsize'] = 16, 9
    plt.errorbar(x=beta, y=y_data1, yerr=y_err1, fmt='o', label=legend1)
    plt.errorbar(x=beta, y=y_data2, yerr=y_err2, fmt='o', color='purple', label=legend2)
    plt.errorbar(x=beta, y=y_data3, yerr=y_err3, fmt='o', color='hotpink', label=legend3)
   # plt.fill_between([0.43, 0.45], -5, 300,  color='papayawhip')
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label='Onsager Energie')
        plt.ylim([-0.9, -0.35])
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label='Yang Magnetisierung')
        plt.ylim([-0.1, 1])
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
        plt.ylim([-1.2, 5.5])
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
        plt.ylim([-1, 250])
    #plt.ylim([min(y_data1)+max(y_err1), max(y_data1)+max(y_err1)])
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '256x256 Gitter, \n H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/FinalTestVariance/' + 'Ausreißer_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()    

    


def make_all_in_one_plot(beta, y_data, y_err, name, legend, b_field, OnlyBig):
    """Plots more than one data set of the observable. Give the function a list
    of data_lists.

    :param beta: all values for beta
    :param y_data: list of different observable values (which also are lists)
    :param y_err: list of the corresponding errors for the observable values
    :param name: of the observable (e.g. energy)
    :param legend: list of different legends for each plot
    :param b_field: value of magnetic field
    """
    colors = ['blue', 'red', 'orange', 'green', 'purple', 'dodgerblue', 'deeppink', 'darkslateblue', 'crimson']
    forms = ['s', 'o', '^', 'X', 's', 'd', '>', 'D', 'v', '<']
    counter = 0
    if OnlyBig == False:
        for y, yerr, leg in zip(y_data, y_err, legend):
            plt.rcParams['figure.figsize'] =16, 9
            plt.errorbar(x=beta, y=y, yerr=yerr, color=colors[counter], fmt=forms[counter], label=leg)
            plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            plt.xlabel(r'$\beta$', fontsize=24)
            if name == 'energy':
                plt.ylabel(r'U', fontsize=24)
            if name == 'magnetisation':
                plt.ylabel(r'|M|', fontsize=24)
            if name == 'specific_heat':
                plt.ylabel(r'$c_V$', fontsize=24)
                #plt.xlim(0.409, 0.4709)
                #plt.ylim(-2, 10)
            if name == 'chi':
                plt.ylabel(r'$\chi$', fontsize=24)
                #plt.xlim(0.409, 0.4709)
                #plt.ylim(-2, 200)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            counter += 1
            print(leg)
        #plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
        plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), title = 'H = 0', title_fontsize = 24, fontsize=24)
        plt.tight_layout()
        #plotname = 'Analyse/256x256/Beides/Plots/' + str(name) + '_plot_all_in_one_b_field_' + str(b_field) + '.pdf'
        plotname = 'Analyse/Volumen/Deutsch/Neu_201208/Plots/' + str(name) + '_plot_all_in_one_lattice_256x256.pdf'
        plt.savefig(plotname, bbox_inches='tight')
        plt.close()
    if OnlyBig == True:
        for y, yerr, leg in zip(y_data, y_err, legend):
            plt.rcParams['figure.figsize'] =16, 9
            plt.errorbar(x=beta, y=y, yerr=yerr, color=colors[counter], fmt=forms[counter], label=leg)
            plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            plt.xlabel(r'$\beta$', fontsize=24)
            if name == 'energy':
                plt.ylabel(r'U', fontsize=24)
            if name == 'magnetisation':
                plt.ylabel(r'|M|', fontsize=24)
            if name == 'specific_heat':
                plt.ylabel(r'$c_V$', fontsize=24)
                plt.xlim(0.409, 0.4709)
                #plt.ylim(-0.1, 10)
            if name == 'chi':
                plt.ylabel(r'$\chi$', fontsize=24)
                plt.xlim(0.409, 0.4709)
                #plt.ylim(-2, 200)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            counter += 1
            print(leg)
        plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
        plt.tight_layout()
        plotname = 'Analyse/Volumen/Deutsch/Neu_201208/Plots/Special/' + 'NurGross_' + str(name) + '_plot_all_in_one_b_field_' + str(b_field) + '.pdf'
        plt.savefig(plotname, bbox_inches='tight')
        plt.close()


def lattice_plotting(direc, beta_list, lattice_list, external_field_list, observables, OnlyBig):
    """This function goes through the different lattice and
    external magnetic field values and calls different plot functions for you.
    There is a special (consistent) naming for the save files.

    :param dir: directory in which the plots should be saved in
    :param beta_list: all values for beta
    :param lattice_list: all lattice sizes
    :param external_field_list: all external magnetic field values
    :param observables: all :observables which should be plotted
    """
    beta = beta_list
    lattice = lattice_list
    external_b_field = external_field_list
    filepart = direc
    for obs_name, obs_var_name in observables:
        for b_field in external_b_field:
            obs_arr = []
            obs_var_arr = []
            obs_legend = []
            if OnlyBig == False:
                for lat in lattice:
                    obs = []
                    obs_var = []
                    ons_energy = []
                    yang_mag = []
                    print(r'Lattice size' + str(lat))
                    for b in beta:
                        print(r'$\beta$ = ' + str(b))
                        #filename = filepart + 'WenigSkips_' + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        #           + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                        filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                                   + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                        data = np.load(filename)
                        obs.append(data[obs_name])
                        obs_var.append(data[obs_var_name])
                        ons_energy.append(data['Onsager_Energy'])
                        yang_mag.append(data['Yang_Magnetisation'])
                        conf_number = str(data['infos'][0]).replace('#', '')
                    leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                               + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) #+ ' H = 0' 
                    #leg_part = 'Angepasste Skips, H = 0' 
                    conf_number = str(data['infos'][0]).replace('#', '')
                    legend = 'Datenpunkte \n' + conf_number 
                    obs_legend.append(leg_part)
                    #make_nice_plot(beta, obs, obs_var, obs_name, legend, lat, b_field)
                    make_nice_plot_Ons(beta, obs, obs_var, obs_name, legend, lat, b_field, ons_energy, yang_mag)             
                    obs_arr.append(obs)
                    obs_var_arr.append(obs_var)
                #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
            if OnlyBig == True:
                for lat in lattice[6:9]:
                    obs = []
                    obs_var = []
                    print(r'Lattice size' + str(lat))
                    for b in beta:
                        print(r'$\beta$ = ' + str(b))
                        filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                                   + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                        data = np.load(filename)
                        obs.append(data[obs_name])
                        obs_var.append(data[obs_var_name])
                        conf_number = str(data['infos'][0]).replace('#', '')
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                    #           + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' 
                    legend = conf_number + '\n' + leg_part
                    obs_legend.append(leg_part)
                    obs_arr.append(obs)
                    obs_var_arr.append(obs_var)
                make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
                

def lattice_plotting_double(direc1, direc2, beta_list, lattice_list, external_field_list, observables):
    """This function goes through the different lattice and
    external magnetic field values and calls different plot functions for you.
    There is a special (consistent) naming for the save files.

    :param dir: directory in which the plots should be saved in
    :param beta_list: all values for beta
    :param lattice_list: all lattice sizes
    :param external_field_list: all external magnetic field values
    :param observables: all :observables which should be plotted
    """
    beta = beta_list
    lattice = lattice_list
    external_b_field = external_field_list
    filepart1 = direc1
    filepart2 = direc2
    for obs_name, obs_var_name in observables:
        for b_field in external_b_field:
            obs_arr1 = []
            obs_var_arr1 = []
            obs_legend1 = []
            obs_arr2 = []
            obs_var_arr2 = []
            obs_legend2 = []
            for lat in lattice:
                obs1 = []
                obs_var1 = []
                obs2 = []
                obs_var2 = []
                ons_energy = []
                yang_mag = []
                print(r'Lattice size' + str(lat))
                for b in beta:
                    print(r'$\beta$ = ' + str(b))
                    filename1 = filepart1  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename2 = filepart2  + str(256) + 'x' + str(256) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    data1 = np.load(filename1)
                    data2 = np.load(filename2)
                    obs1.append(data1[obs_name])
                    obs_var1.append(data1[obs_var_name])
                    obs2.append(data2[obs_name])
                    obs_var2.append(data2[obs_var_name])
                    #the same theoretical results for the data 
                    ons_energy.append(data1['Onsager_Energy'])
                    yang_mag.append(data1['Yang_Magnetisation'])
                    # Maybe different configuration numbers
                    conf_number1 = str(data1['infos'][0]).replace('#', '')
                    conf_number2 = str(data2['infos'][0]).replace('#', '')
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                    #           + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' H = 0' 
                leg_part1 = conf_number1 
                legend1 = conf_number1 + '\n' + leg_part1
                obs_legend1.append(leg_part1)
                leg_part2 = conf_number2
                legend2 = conf_number2 + '\n' + leg_part2
                obs_legend2.append(leg_part1)
                make_nice_plot_Ons_double(beta, obs1, obs_var1, obs2, obs_var2, obs_name, leg_part1, leg_part2, lat, b_field, ons_energy, yang_mag)             
                obs_arr1.append(obs1)
                obs_var_arr1.append(obs_var1)
                obs_arr2.append(obs2)
                obs_var_arr2.append(obs_var2)
                #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
 
def lattice_plotting_three(direc1, direc2, direc3, beta_list, lattice_list, external_field_list, observables):
    """This function goes through the different lattice and
    external magnetic field values and calls different plot functions for you.
    There is a special (consistent) naming for the save files.

    :param dir: directory in which the plots should be saved in
    :param beta_list: all values for beta
    :param lattice_list: all lattice sizes
    :param external_field_list: all external magnetic field values
    :param observables: all :observables which should be plotted
    """
    beta = beta_list
    lattice = lattice_list
    external_b_field = external_field_list
    filepart1 = direc1
    filepart2 = direc2
    filepart3 = direc3
    for obs_name, obs_var_name in observables:
        for b_field in external_b_field:
            obs_arr1 = []
            obs_var_arr1 = []
            obs_legend1 = []
            obs_arr2 = []
            obs_var_arr2 = []
            obs_legend2 = []
            obs_arr3 = []
            obs_var_arr3 = []
            obs_legend3 = []
            for lat in lattice:
                obs1 = []
                obs_var1 = []
                obs2 = []
                obs_var2 = []
                obs3 = []
                obs_var3 = []
                ons_energy = []
                yang_mag = []
                print(r'Lattice size' + str(lat))
                for b in beta:
                    print(r'$\beta$ = ' + str(b))
                    filename1 = filepart1  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename2 = filepart2  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename3 = filepart3 + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    data1 = np.load(filename1)
                    data2 = np.load(filename2)
                    data3 = np.load(filename3)
                    obs1.append(data1[obs_name])
                    obs_var1.append(data1[obs_var_name])
                    obs2.append(data2[obs_name])
                    obs_var2.append(data2[obs_var_name])
                    obs3.append(data3[obs_name])
                    obs_var3.append(data3[obs_var_name])
                    #the same theoretical results for the data 
                    ons_energy.append(data1['Onsager_Energy'])
                    yang_mag.append(data1['Yang_Magnetisation'])
                    # Maybe different configuration numbers
                    conf_number1 = str(data1['infos'][0]).replace('#', '')
                    conf_number2 = str(data2['infos'][0]).replace('#', '')
                    conf_number3 = str(data3['infos'][0]).replace('#', '')
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                    #           + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' H = 0' 
                leg_part1 = 'Run 1' 
                legend1 = conf_number1 + '\n' + leg_part1
                obs_legend1.append(leg_part1)
                leg_part2 = 'Run 2' 
                legend2 = conf_number2 + '\n' + leg_part2
                obs_legend2.append(leg_part1)
                leg_part3 = 'Run 3' 
                legend3 = conf_number3 + '\n' + leg_part3
                obs_legend3.append(leg_part3)
                make_nice_plot_Ons_three(beta, obs1, obs_var1, obs2, obs_var2, obs3, obs_var3, obs_name, leg_part1, leg_part2, leg_part3, lat, b_field, ons_energy, yang_mag)             
                #obs_arr1.append(obs1)
                #obs_var_arr1.append(obs_var1)
                #obs_arr2.append(obs2)
                #obs_var_arr2.append(obs_var2)
                #obs_arr3.append(obs3)
                #obs_var_arr3.append(obs_var3)
                #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
            

def bfield_plotting(direc, beta_list, lattice_list, external_field_list, observables, OnlyBig):
    """This function goes through the different lattice and
    external magnetic field values and calls different plot functions for you.
    There is a special (consistent) naming for the save files.

    :param dir: directory in which the plots should be saved in
    :param beta_list: all values for beta
    :param lattice_list: all lattice sizes
    :param external_field_list: all external magnetic field values
    :param observables: all :observables which should be plotted
    """
    beta = beta_list
    lattice = lattice_list
    external_b_field = external_field_list
    filepart = direc
    for obs_name, obs_var_name in observables:
        for lat in lattice:
            print(r'Lattice size' + str(lat))
            obs_arr = []
            obs_var_arr = []
            obs_legend = []
            for b_field in external_b_field:
                print(r'External B-Field = ' + str(b_field))
                obs = []
                obs_var = []
                for b in beta:
                    print(r'$\beta$ = ' + str(b))
                    filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    data = np.load(filename)
                    obs.append(data[obs_name])
                    obs_var.append(data[obs_var_name])
                    conf_number = str(data['infos'][0]).replace('#', '')
                leg_part = r'H = ' + str(b_field) 
                legend = conf_number + '\n' + leg_part
                obs_legend.append(leg_part)
                make_nice_plot(beta, obs, obs_var, obs_name, legend, lat, b_field)
                obs_arr.append(obs)
                obs_var_arr.append(obs_var)
            #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig) 

def plot_phasediagram():
    beta_list = np.arange(0.39, 0.49, 0.0001)
    beta_crit = np.log(1 + np.sqrt(2)) / 2
    yang_magnetisation = np.ones(len(beta_list))
    counter = 0
    for beta in beta_list:
        if beta > beta_crit:
                yang_magnetisation[counter] = (1 - np.sinh(
                    np.log(1 + np.sqrt(2) * beta / beta_crit)
                ) ** (-4)) ** (1 / 8)
        else:
                yang_magnetisation[counter] = 0
        counter += 1
    plt.rcParams['figure.figsize'] =16, 9
    plt.axhline(y=0, xmin=-200 , xmax=200, color='black', ls='-')
    plt.axvline(x=beta_crit, ymin=-200 , ymax=200, color='black', ls='--')
    plt.plot(beta_list, yang_magnetisation, '-r', label='Yang Magnetisierung')
    plt.plot(beta_list, -yang_magnetisation, '-r')
    plt.annotate('Phasenübergang \n 1. Ordnung', xytext=(0.4625, -0.2), xy=(0.46, -0.5), fontsize=20)
    plt.annotate(r'', xytext=(0.46, 0.5), xy=(0.46, -0.5), fontsize=20, arrowprops={'arrowstyle': '<|-|>'})
    plt.annotate('Phasenübergang \n 2. Ordnung', xytext=(0.42, 0.3), xy=(0.46, -0.5), fontsize=20)
    plt.annotate(r'', xytext=(0.43, 0.5), xy=(0.45, 0.5), fontsize=20, arrowprops={'arrowstyle': '<|-|>'})
    plt.xlim([min(beta_list), max(beta_list)])
    plt.xlabel(r'$\beta$', fontsize = 24)
    plt.ylabel(r'$M_{Yang}$', fontsize = 24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = 'H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/' + 'PhasendiagrammMagnetisierung.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()            
    
    
    


'''Do not change the following three lists'''
beta_all_for_all_lattices = [0.39, 0.40, 0.41, 0.415, 0.42, 0.425, 0.43, 0.4325, 0.435, 0.4375, 0.44, 0.4425, 0.445, 0.4475, 0.45, 0.455, 0.46, 0.465, 0.47, 0.48, 0.49]
beta_all_setted = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]
beta_min = [0.39, 0.42, 0.44, 0.441, 0.46, 0.49]
beta_test = [0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.44, 0.44125,  0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45]
beta_fine = [0.43894, 0.43896, 0.43898]
lattice = [(2 ** i, 2 ** i) for i in range(1, 10)]
setted_lattice = [(256, 256)]
b_field_all = [-1, -0.875, -0.75, -0.625, -0.5, -0.375, -0.25, -0.125, 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
#b_field_min = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
b_field_min = [0, 0.25, 0.5, 0.75, 1]
observables = [('energy', 'energy_var'), ('magnetisation', 'magnetisation_var'),
               ('specific_heat', 'heat_var'), ('chi', 'chi_var')]

'''Here lives your main measure and plot code'''
# If you have already measured the needed configs,
# then uncomment the following line!
#lattice_measuring(beta_list=beta_test, lattice_list=setted_lattice, external_field_list = [0])


# Here you can call the plot function, with lists (!) for beta,
# lattice sizes and external magnetic field values
# If you only want to plot for example one magnetic field value = 0
# for some lattice sizes call lattice_plotting with external_field_list=[0]

#lattice_plotting(direc='Analyse/256x256/Observablen/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                                  external_field_list=[0], observables=observables, OnlyBig = False)
#lattice_plotting(direc='Analyse/Volumen/Deutsch/Neu_201208/', beta_list=beta_all_for_all_lattices, lattice_list=lattice,
#                                  external_field_list=[0], observables=observables, OnlyBig = True)
#lattice_plotting_double(direc1='Analyse/256x256/FinalTestSkips/100Konfigs/', direc2='Analyse/256x256/FinalTestSkips/200Konfigs/', beta_list=beta_test, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables)
lattice_plotting_three(direc1='Analyse/256x256/FinalTestVariance/Run1/', direc2='Analyse/256x256/FinalTestVariance/Run2/', direc3='Analyse/256x256/FinalTestVariance/Run3/', beta_list=beta_test, lattice_list=setted_lattice,
                 external_field_list=[0], observables=observables)
#bfield_plotting(direc='Analyse/256x256/OhneBFeld/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables, OnlyBig = False)

#lattice_measuring(beta_list=[0.39], lattice_list=setted_lattice, external_field_list = [0])
#plot_phasediagram()


 
