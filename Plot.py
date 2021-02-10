import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from Metropolis import Metropolis, Observables
from scipy.special import ellipk as elli


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
                filename = 'Analyse/256x256/FinalTestSkips/Run3_200Konfigs/' +  str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
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
        plt.ylabel(r'$\beta$U', fontsize=24)
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
    plt.errorbar(x=beta, y=y_data, yerr=y_err, color='purple', ecolor='royalblue', fmt='o', label=legend)
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'$\beta$U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}|$')
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '(256x256), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Observablen/Neu_201229/Plots/' + 'BootstrapErr_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
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
        plt.ylabel(r'$\beta$U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}|$')
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
        plt.ylabel(r'$\beta$U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
        plt.ylim([-0.9, -0.35])
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}$|')
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
    plt.legend(loc='best', framealpha=0.5, title = '(256x256), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/FinalTestVariance/Neu_210104/' + 'Ausreißer_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()    
    
def make_nice_plot_Ons_six(beta, y_data1, y_err1, y_data2, y_err2, y_data3, y_err3, y_data4, y_err4, y_data5, y_err5, y_data6, y_err6, name, legend1, legend2, lat, b_field, ons_energy, yang_mag):
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
    plt.errorbar(x=beta, y=y_data1, yerr=y_err1, fmt='o', color='royalblue', label=legend1)
    plt.errorbar(x=beta, y=y_data2, yerr=y_err2, fmt='o', color='royalblue')
    plt.errorbar(x=beta, y=y_data3, yerr=y_err3, fmt='o', color='royalblue')
    plt.errorbar(x=beta, y=y_data4, yerr=y_err4, fmt='o', color='hotpink', label=legend2)
    plt.errorbar(x=beta, y=y_data5, yerr=y_err5, fmt='o', color='hotpink')
    plt.errorbar(x=beta, y=y_data6, yerr=y_err6, fmt='o', color='hotpink')
   # plt.fill_between([0.43, 0.45], -5, 300,  color='papayawhip')
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'$\beta$U', fontsize=24)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
        plt.ylim([-0.7, -0.54])
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}$|')
        plt.ylim([-0.1, 0.8])
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
    plt.legend(loc='best', framealpha=0.5, title = '(256x256), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/FinalTestSkips/' + 'SkipTestBoot_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()    

    


def make_all_in_one_plot(beta, y_data, y_err, name, legend, b_field, ons_energy, yang_mag, OnlyBig):
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
                plt.ylabel(r'$\beta$U', fontsize=24)
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
        plotname = 'Analyse/Volumen/Deutsch/Neu_201208/Plots/' + str(name) + '_plot_all_in_one_lattice_Boot.pdf'
        plt.savefig(plotname, bbox_inches='tight')
        plt.close()
    if OnlyBig == True:
        counter1 = 0
        counter2 = 0
        for y, yerr, leg in zip(y_data, y_err, legend):
            plt.rcParams['figure.figsize'] =16, 9
            plt.errorbar(x=beta, y=y, yerr=yerr, color=colors[counter], fmt=forms[counter], label=leg)
            plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
            plt.xlabel(r'$\beta$', fontsize=24)
            if name == 'energy':
                if counter1 == 0:
                    plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
                    counter1 += 1
                plt.ylabel(r'$\beta$U', fontsize=24)
            if name == 'magnetisation':
                if counter2 == 0:
                    plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}$|')
                    counter2 += 1
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
        plotname = 'Analyse/Volumen/Deutsch/Neu_201208/Plots/Special/' + 'NurGrossOns_' + str(name) + '_plot_all_in_one_b_field_' + str(b_field) + '.pdf'
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
                    leg_part = str(lat[0]) + 'x' + str(lat[1]) 
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) #+ ' H = 0' 
                    #leg_part = 'Angepasste Skips, H = 0' 
                    conf_number = str(data['infos'][0]).replace('#', '')
                    legend = 'Datenpunkte \n' + conf_number 
                    obs_legend.append(leg_part)
                    #make_nice_plot(beta, obs, obs_var, obs_name, legend, lat, b_field)
                    #make_nice_plot_Ons(beta, obs, obs_var, obs_name, legend, lat, b_field, ons_energy, yang_mag)             
                    obs_arr.append(obs)
                    obs_var_arr.append(obs_var)
                make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, ons_energy, yang_mag, OnlyBig)
            if OnlyBig == True:
                for lat in lattice[6:9]:
                    obs = []
                    obs_var = []
                    ons_energy = []
                    yang_mag = []
                    print(r'Lattice size' + str(lat))
                    for b in beta:
                        print(r'$\beta$ = ' + str(b))
                        filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                                   + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                        data = np.load(filename)
                        obs.append(data[obs_name])
                        obs_var.append(data[obs_var_name])
                        ons_energy.append(data['Onsager_Energy'])
                        yang_mag.append(data['Yang_Magnetisation'])
                        conf_number = str(data['infos'][0]).replace('#', '')
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                    #           + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    leg_part = str(lat[0]) + 'x' + str(lat[1]) 
                    obs_legend.append(leg_part)
                    obs_arr.append(obs)
                    obs_var_arr.append(obs_var)
                make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, ons_energy, yang_mag, OnlyBig)
                

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
            

def lattice_plotting_six(direc1, direc2, direc3, direc4, direc5, direc6, beta_list, lattice_list, external_field_list, observables):
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
    filepart4 = direc4
    filepart5 = direc5
    filepart6 = direc6
    for obs_name, obs_var_name in observables:
        for b_field in external_b_field:
            for lat in lattice:
                obs1 = []
                obs_var1 = []
                obs2 = []
                obs_var2 = []
                obs3 = []
                obs_var3 = []
                obs4 = []
                obs_var4 = []
                obs5 = []
                obs_var5 = []
                obs6 = []
                obs_var6 = []
                ons_energy = []
                yang_mag = []
                for b in beta:
                    filename1 = filepart1  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename2 = filepart2  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename3 = filepart3 + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename4 = filepart4  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename5 = filepart5  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    filename6 = filepart6 + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    data1 = np.load(filename1)
                    data2 = np.load(filename2)
                    data3 = np.load(filename3)
                    data4 = np.load(filename4)
                    data5 = np.load(filename5)
                    data6 = np.load(filename6)
                    obs1.append(data1[obs_name])
                    obs_var1.append(data1[obs_var_name])
                    obs2.append(data2[obs_name])
                    obs_var2.append(data2[obs_var_name])
                    obs3.append(data3[obs_name])
                    obs_var3.append(data3[obs_var_name])
                    obs4.append(data4[obs_name])
                    obs_var4.append(data4[obs_var_name])
                    obs5.append(data5[obs_name])
                    obs_var5.append(data5[obs_var_name])
                    obs6.append(data6[obs_name])
                    obs_var6.append(data6[obs_var_name])
                    #the same theoretical results for the data 
                    ons_energy.append(data1['Onsager_Energy'])
                    yang_mag.append(data1['Yang_Magnetisation'])
                    # Maybe different configuration numbers
                    conf_number1 = str(data1['infos'][0]).replace('#', '')
                    conf_number2 = str(data4['infos'][0]).replace('#', '')
                leg_part1 = ' ' 
                legend1 = conf_number1 #+ '\n' + leg_part1
                leg_part2 = ' ' 
                legend2 = conf_number2 #+ '\n' + leg_part2
                make_nice_plot_Ons_six(beta, obs1, obs_var1, obs2, obs_var2, obs3, obs_var3, obs4, obs_var4, obs5, obs_var5, obs6, obs_var6, obs_name, legend1, legend2, lat, b_field, ons_energy, yang_mag)             
    



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


def plot_phasediagram_magn():
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
    plt.plot(beta_list, yang_magnetisation, '-r', label=r'$M_{Yang}$')
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
    
def write_ons_ener():
    beta_list = np.arange(0.39, 0.49, 0.001)
    ons_ener = np.ones(len(beta_list))
    counter = 0
    for beta in beta_list:
        k = 2 * np.tanh(2 * beta ) ** 2 - 1
        l = (2 * np.sinh(2 * beta )) \
            / (np.cosh(2 * beta ) ** 2 )
        integral = elli(l)
        ons_ener[counter] = (-(1)
                          / (np.tanh(2 * beta))) *\
                        (1 + 2 / np.pi * k * integral)
        counter += 1
    np.savetxt('OnsEnerWerte_ML.txt', (beta_list, ons_ener), header = 'beta ' + 'Onsager Energy')
    '''
    print(len(ons_ener))
    print(len(beta_list))
    plt.plot(beta_list, ons_ener)
    plt.savefig('Test.pdf')
    plt.close()
    '''
    
def plot_phasediagram_ener():
    beta_list = np.arange(0.1, 0.9, 0.0001)
    beta_crit = np.log(1 + np.sqrt(2)) / 2
    ons_ener = np.ones(len(beta_list))
    counter = 0
    for beta in beta_list:
        k = 2 * np.tanh(2 * beta ) ** 2 - 1
        l = (2 * np.sinh(2 * beta )) \
            / (np.cosh(2 * beta ) ** 2 )
        integral = elli(l)
        ons_ener[counter] = (-(beta)
                          / (np.tanh(2 * beta))) *\
                        (1 + 2 / np.pi * k * integral)
        counter += 1
    wiki_ons_ener = np.ones(len(beta_list))
    counter = 0
    for beta in beta_list:
        r = 1 / ((np.sinh(2 * beta)) ** 2)  # faktor um rechnung zu vereinfachen
        s = 4*r*(1+r)**(-2)
        inte = elli(s)
        wiki_ons_ener[counter] = (-beta) / (np.tanh(2 * beta)) * (1 + 2 / np.pi * (2 * np.tanh(2 * beta) ** 2 - 1) * inte)
    plt.rcParams['figure.figsize'] =16, 9
    #plt.axhline(y=0, xmin=-200 , xmax=200, color='black', ls='-')
    plt.axvline(x=beta_crit, ymin=-200 , ymax=200, color='black', ls='--')
    plt.plot(beta_list, ons_ener, '-r', label=r'$U_{Onsager}$')
    #plt.plot(beta_list, wiki_ons_ener, '-b', label=r'$U_{Wiki, Onsager}$')
    #plt.annotate('Phasenübergang \n 1. Ordnung', xytext=(0.4625, -0.2), xy=(0.46, -0.5), fontsize=20)
    #plt.annotate(r'', xytext=(0.46, 0.5), xy=(0.46, -0.5), fontsize=20, arrowprops={'arrowstyle': '<|-|>'})
    #plt.annotate('Phasenübergang \n 2. Ordnung', xytext=(0.42, 0.3), xy=(0.46, -0.5), fontsize=20)
    #plt.annotate(r'', xytext=(0.43, 0.5), xy=(0.45, 0.5), fontsize=20, arrowprops={'arrowstyle': '<|-|>'})
    plt.xlim([0.39,0.49])
    plt.ylim([-0.88, -0.35])
    plt.xlabel(r'$\beta$', fontsize = 24)
    plt.ylabel(r'$\beta$$U_{Onsager}$', fontsize = 24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = 'H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/' + 'PhasendiagrammEnergie.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()    


def VarianceFlucMagn(direc1, direc2, direc3, name, beta_list, lattice_list, external_field_list):
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
    for b_field in external_b_field:
        for lat in lattice:
            obs1 = []
            obs2 = []
            obs3 = []
            for b in beta:
                filename1 = filepart1  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                    + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                filename2 = filepart2  + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                    + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                filename3 = filepart3 + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                    + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                data1 = np.load(filename1)
                data2 = np.load(filename2)
                data3 = np.load(filename3)
                obs1.append(data1[name])
                obs2.append(data2[name])
                obs3.append(data3[name])
            # Calculaion of the variance of the data
            magn_var_est = []
            for i in np.arange(0, len(obs1), 1):
                #print(np.mean([obs1[i]**2, obs2[i]**2, obs3[i]**2])-(np.mean([obs1[i], obs2[i], obs3[i]]))**2)
                magn_var_est.append(np.mean([obs1[i]**2, obs2[i]**2, obs3[i]**2])-(np.mean([obs1[i], obs2[i], obs3[i]]))**2)
                #print(magn_var_est)
            return magn_var_est
            
            
def lattice_plotting_KorrMagnVar(direc, direc1, direc2, direc3, beta_list, lattice_list, external_field_list, observables):
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
            obs_legend = []
            for lat in lattice:
                obs = []
                obs_var = []
                ons_energy = []
                yang_mag = []
                ener_var = []
                config_energy_arr = []
                #MagnKorrVar = []
                for b in beta:
                    filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    '''
                    data_alt = np.load(filename)
                    observables = Observables(data_alt['configs'], beta=b)
                    observables.save_simulation(filename)
                    '''
                    data = np.load(filename)
                    obs.append(data[obs_name])
                    if obs_name == 'energy':
                        #ener_var.append(data['specific_heat'])
                        observables = Observables(data['configs'], b) 
                        observables.total_energy()
                        ener_var.append(np.std(observables.energy_per_config \
                                                 / (lat[0]*lat[1])))
                    obs_var.append(data[obs_var_name])
                    ons_energy.append(data['Onsager_Energy'])
                    yang_mag.append(data['Yang_Magnetisation'])
                    conf_number = str(data['infos'][0]).replace('#', '')
                leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                             + 'B_ext = ' + str(b_field)
                conf_number = str(data['infos'][0]).replace('#', '')
                legend = 'Datenpunkte \n' + conf_number 
                obs_legend.append(leg_part)
                MagnKorrVar = []
                if obs_name == 'magnetisation':
                    MagnKorrVar = np.sqrt(VarianceFlucMagn(direc1, direc2, direc3, obs_name, beta[12:40], lattice, external_b_field))
                if obs_name == 'energy':
                    obs_var = np.sqrt(np.array(ener_var))
                make_nice_plot_Ons_Korr(beta, obs, obs_var, obs_name, legend, lat, b_field, ons_energy, yang_mag, MagnKorrVar=MagnKorrVar)             
                
def make_nice_plot_Ons_Korr(beta, y_data, y_err, name, legend, lat, b_field, ons_energy, yang_mag, MagnKorrVar):
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
    plt.errorbar(x=beta, y=y_data, yerr=y_err, color='royalblue', fmt='o', label=legend, zorder=1)
    plt.axvline(x=0.4407, ymin=-200 , ymax=200, color='black', ls='--')
    # plt.xlim([beta[0], beta[-1]])
    plt.xlabel(r'$\beta$', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'$\beta$U', fontsize=24)
        #plt.errorbar(x=beta, y=np.array(y_data)/np.array(beta), yerr=y_err, color='purple', fmt='o', label=r'$U_{neu}$', zorder=1)
        plt.plot(beta, ons_energy, 'r+', markersize=10, label=r'$U_{Onsager}$')
    if name == 'magnetisation':
        plt.ylabel(r'|M|', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label=r'$|M_{Yang}|$')
        plt.errorbar(x=beta[12:40], y=y_data[12:40], yerr=MagnKorrVar, color='royalblue', ecolor='orange', fmt='o', zorder=2)
    if name == 'specific_heat':
        plt.ylabel(r'$c_V$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '(256x256), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Observablen/Test_Plots/' + 'Test_' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()    
    
def corr_err_obs(beta_list, lattice_list, ext_bfield_list = 0):
    beta_all = beta_list
    lattice = lattice_list
    b_field = ext_bfield_list
    counter = 0
    for lat in lattice:
        for b in beta_all:
            print(counter)
            filename = 'Analyse/256x256/FinalTestSkips/Run3_200Konfigs/' +  str(lat[0]) + 'x' + str(lat[0]) + 'lattice_beta_' \
                       + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
            data = np.load(filename)
            observables = Observables(data['configs'], beta=b)
            observables.measure_observables()
            observables.save_simulation(filename)
            counter += 1
            del observables
            
def ener_konfig_plot(direc, beta_list, lattice_list, observables):
    beta = beta_list
    lattice = lattice_list
    numb_latpoints = lattice[0][0]*lattice[0][1]
    filepart = direc
    for b in beta:
        filename = filepart + str(lattice[0][0]) + 'x' + str(lattice[0][1]) + 'lattice_beta_' \
                                       + str(b).replace('.', '') + 'external_field_0' + '.npz'                 
        data = np.load(filename)
        obs = Observables(data['configs'], b)
        obs.total_energy()
        energy = obs.energy_per_config
        # Comparison values of mean of data and ons_energy
        ener_avg = np.mean(energy)/numb_latpoints
        k = 2 * np.tanh(2 * b ) ** 2 - 1
        l = (2 * np.sinh(2 * b )) \
            / (np.cosh(2 * b ) ** 2 )
        integral = elli(l)
        ons_ener = (-(b) / (np.tanh(2 * b))) *\
                        (1 + 2 / np.pi * k * integral)
        plt.rcParams['figure.figsize'] = 16, 9
        legend  = r'$\beta = $' + str(b)
        conf_number = np.arange(1, len(data['configs'])+1, 1)
        plt.plot(conf_number, energy/numb_latpoints, '.', color='royalblue', label=legend, zorder = 1)
        plt.axhline(y=ener_avg, xmin=0, xmax=2000, color='red', label = 'Mittelwert', zorder = 2)
        plt.axhline(y=ons_ener, xmin=0, xmax=2000, color='black', ls='--', label = r'$U_{Onsager}$', zorder = 2)
        # plt.xlim([beta[0], beta[-1]])
        plt.xlabel(r'Anzahl der Konfigurationen', fontsize=24)
        plt.ylabel(r'$\beta$U', fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(loc='best', framealpha=0.5, title = '(128x128), H = 0', title_fontsize = 24, fontsize=24)
        plotname = 'Analyse/128x128/ObsENTBUG/UKonfigs_beta_'  + str(b) + '.pdf'
        plt.savefig(plotname, bbox_inches='tight')
        plt.close()
        
def zustandssumme_plot(direc, lattice_list, observables):
    lattice = lattice_list
    filepart = direc
    filename_arr = filepart + 'energyandbetavalues.npz'                 
    arr = np.load(filename_arr)
    betas = arr['beta']
    theo_energy = arr['energy']
    sim_ener = []
    sim_ener_std = []
    for b in betas:
        filename = filepart + str(lattice[0][0]) + 'x' + str(lattice[0][1]) + 'lattice_beta_' \
                                       + str(b).replace('.', '') + 'external_field_0' + '.npz'                 
        data = np.load(filename)
        sim_ener.append(data['energy'])
        sim_ener_std.append(data['energy_var'])
        
    plt.rcParams['figure.figsize'] = 16, 9
    plt.plot(betas, betas*theo_energy, 'o', color='tomato', label=r'U$_{Theo}$', zorder = 2)
    plt.errorbar(betas, sim_ener, yerr=sim_ener_std, fmt='o', color='royalblue',\
                 label=r'Messdaten', zorder = 1)
    plt.xlabel(r'$\beta$', fontsize=24)
    plt.ylabel(r'$\beta$U', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '(2x2), H = 0', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/2x2/Zustandssumme.pdf'  
    plt.savefig(plotname, bbox_inches='tight')
    plt.close()
        


'''Do not change the following three lists'''
beta_all_for_all_lattices = [0.39, 0.40, 0.41, 0.415, 0.42, 0.425, 0.43, 0.4325, 0.435, 0.4375, 0.44, 0.4425, 0.445, 0.4475, 0.45, 0.455, 0.46, 0.465, 0.47, 0.48, 0.49]
beta_all_setted = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]
beta_min = [0.39, 0.42, 0.44, 0.441, 0.46, 0.49]
beta_test = [0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.44, 0.44125,  0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45]
beta_fine = [0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45]
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

#lattice_plotting(direc='Analyse/256x256/Observablen/Neu_201229/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                                  external_field_list=[0], observables=observables, OnlyBig = False)
#lattice_plotting(direc='Analyse/Volumen/Deutsch/Neu_201208/', beta_list=beta_all_for_all_lattices, lattice_list=lattice,
#                                  external_field_list=[0], observables=observables, OnlyBig = True)
#lattice_plotting_double(direc1='Analyse/256x256/FinalTestSkips/100Konfigs/', direc2='Analyse/256x256/FinalTestSkips/200Konfigs/', beta_list=beta_test, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables)
#lattice_plotting_three(direc1='Analyse/256x256/FinalTestVariance/Neu_210104/Run1/', direc2='Analyse/256x256/FinalTestVariance/Neu_210104/Run2/', direc3='Analyse/256x256/FinalTestVariance/Neu_210104/Run3/', beta_list=beta_test, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables)
#bfield_plotting(direc='Analyse/256x256/OhneBFeld/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables, OnlyBig = False)

#lattice_measuring(beta_list=[0.39], lattice_list=setted_lattice, external_field_list = [0])
#plot_phasediagram_magn()
#plot_phasediagram_ener()

#corr_err_obs(beta_test, setted_lattice)
#ener_konfig_plot('Analyse/128x128/ObsENTBUG/', [0.39, 0.49], [(128, 128)], observables=observables)

zustandssumme_plot('Analyse/2x2/', [(2, 2)], observables=observables)


#lattice_plotting_KorrMagnVar('Analyse/256x256/Observablen/Neu_201229/', 'Analyse/256x256/FinalTestVariance/Neu_210104/Run1/', 'Analyse/256x256/FinalTestVariance/Neu_210104/Run2/', \
#                             'Analyse/256x256/FinalTestVariance/Neu_210104/Run3/', beta_list=beta_all_setted, lattice_list=setted_lattice, external_field_list=[0], observables=observables)

#lattice_plotting_six(direc1='Analyse/256x256/FinalTestSkips/Run1_100Konfigs/', \
#                     direc2='Analyse/256x256/FinalTestSkips/Run2_100Konfigs/', \
#                     direc3='Analyse/256x256/FinalTestSkips/Run3_100Konfigs/', \
#                     direc4='Analyse/256x256/FinalTestSkips/Run1_200Konfigs/', \
#                     direc5='Analyse/256x256/FinalTestSkips/Run2_200Konfigs/', \
#                     direc6='Analyse/256x256/FinalTestSkips/Run3_200Konfigs/', \
#                     beta_list=beta_test, lattice_list=setted_lattice, \
#                 external_field_list=[0], observables=observables)


'''
for i in np.arange(0, len(beta_all_setted), 1):
    if beta_all_setted[i] == 0.43:
        print(i)
    if beta_all_setted[i] == 0.45:
        print(i)
'''


 
