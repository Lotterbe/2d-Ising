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
                filename = 'Analyse/256x256/TestKonfigs/' + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                           + str(b).replace('.', '') + 'external_field_' + str(b_field)
                observables.save_simulation(filename)
                #metro.b_field += 1
                #all configs = 0!!!
                #metro.start_simulation()
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
        plt.ylabel(r'M', fontsize=24)
    if name == 'specific_heat':
        plt.ylabel(r'$c_p$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '256x256 Gitter', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/OhneBFeld/Plots/' + str(name) + '_plot_' + str(lat[0]) + 'x' \
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
        plt.ylabel(r'M', fontsize=24)
        plt.plot(beta, yang_mag, 'r+', markersize=10, label='Yang Magnetisierung')
    if name == 'specific_heat':
        plt.ylabel(r'$c_p$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #plt.legend(loc='best', framealpha=0.5, title = r'H = ' + str(b_field), title_fontsize = 24, fontsize=24)
    plt.legend(loc='best', framealpha=0.5, title = '256x256 Gitter', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/OhneBFeld/Plots/Special/' + 'OnsEner' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'b_field_' + str(b_field) + '.pdf'
    plt.savefig(plotname)
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
                plt.ylabel(r'M', fontsize=24)
            if name == 'specific_heat':
                plt.ylabel(r'$c_p$', fontsize=24)
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
        plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), title = '256x256 Gitter', title_fontsize = 24, fontsize=24)
        plt.tight_layout()
        #plotname = 'Analyse/256x256/Beides/Plots/' + str(name) + '_plot_all_in_one_b_field_' + str(b_field) + '.pdf'
        plotname = 'Analyse/256x256/Beides/Plots/Special/' + 'NurPos_' + str(name) + '_plot_all_in_one_lattice_256x256.pdf'
        plt.savefig(plotname)
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
                plt.ylabel(r'M', fontsize=24)
            if name == 'specific_heat':
                plt.ylabel(r'$c_p$', fontsize=24)
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
        plotname = 'Analyse/Volumen/Deutsch/Plots/Special/' + 'NurGross_' + str(name) + '_plot_all_in_one_b_field_' + str(b_field) + '.pdf'
        plt.savefig(plotname)
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
                        filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                                   + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                        data = np.load(filename)
                        obs.append(data[obs_name])
                        obs_var.append(data[obs_var_name])
                        ons_energy.append(data['Onsager_Energy'])
                        yang_mag.append(data['Onsager_Magnetisation'])
                        conf_number = str(data['infos'][0]).replace('#', '')
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' lattice' + '\n' \
                    #           + 'B_ext = ' + str(b_field)
                    #legend = conf_number + '\n' + leg_part
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' Gitter' + '\n' \
                    #           + r'$B_{ext}$ = ' + str(b_field)
                    #leg_part = str(lat[0]) + 'x' + str(lat[1]) + ' H = 0' 
                    leg_part = 'H = 0' 
                    legend = conf_number + '\n' + leg_part
                    obs_legend.append(leg_part)
                    #make_nice_plot(beta, obs, obs_var, obs_name, legend, lat, b_field)
                    make_nice_plot_Ons(beta, obs, obs_var, obs_name, legend, lat, b_field, ons_energy, yang_mag)             
                    obs_arr.append(obs)
                    obs_var_arr.append(obs_var)
                #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
            if OnlyBig == True:
                for lat in lattice[5:9]:
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

def hysterese_measuring(beta_list, lattice_list, external_field_list):
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
    for b in beta:
        print(r'Measuring $\beta$ = ' + str(b))
        for lat in lattice:
            print(r'Measuring lattice size ' + str(lat))
            for b_field in external_b_field:
                print('Measuring external magnetic field B = ' + str(b_field))
                metro = Metropolis(*lat, beta=b, external_field=b_field)
                configs = metro.start_simulation()
                observables = Observables(configs, beta=b)
                observables.measure_observables()
                filename = 'Analyse/256x256/Hysterese/' + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                           + str(b).replace('.', '') + 'external_field_' + str(b_field)
                observables.save_simulation(filename)
                del metro, observables
                
def hysterese_plot(beta, y_data, y_err, name, legend, lat, b_field):
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
    plt.errorbar(x=b_field, y=y_data, yerr=y_err, fmt='o', label=legend)
    plt.xlabel(r'H', fontsize=24)
    if name == 'energy':
        plt.ylabel(r'U', fontsize=24)
    if name == 'magnetisation':
        plt.ylabel(r'M', fontsize=24)
    if name == 'specific_heat':
        plt.ylabel(r'$c_p$', fontsize=24)
    if name == 'chi':
        plt.ylabel(r'$\chi$', fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(loc='best', framealpha=0.5, title = '256x256 Gitter', title_fontsize = 24, fontsize=24)
    plotname = 'Analyse/256x256/Hysterese/Plots/' + str(name) + '_plot_' + str(lat[0]) + 'x' \
               + str(lat[1]) + '_lattice_' + 'beta' + str(beta) + '.pdf'
    plt.savefig(plotname)
    plt.close()

def hysterese_plotting(direc, beta_list, lattice_list, external_field_list, observables):
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
            for b in beta:
                print(r'$\beta$ = ' + str(b))
                obs = []
                obs_var = []
                for b_field in external_b_field:
                    print(r'External B-Field = ' + str(b_field))
                    filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
                        + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
                    data = np.load(filename)
                    obs.append(data[obs_name])
                    obs_var.append(data[obs_var_name])
                    conf_number = str(data['infos'][0]).replace('#', '')
                leg_part = r'$\beta$ = ' + str(b) 
                legend = conf_number + '\n' + leg_part
                obs_legend.append(leg_part)
                hysterese_plot(b, obs, obs_var, obs_name, legend, lat, external_b_field)
                obs_arr.append(obs)
                obs_var_arr.append(obs_var)
            #make_all_in_one_plot(beta, obs_arr, obs_var_arr, obs_name, obs_legend, b_field, OnlyBig)
    


'''Do not change the following three lists'''
#beta_all_for_all_lattices = [0.39, 0.40, 0.41, 0.415, 0.42, 0.425, 0.43, 0.4325, 0.435, 0.4375, 0.44, 0.4425, 0.445, 0.4475, 0.45, 0.455, 0.46, 0.465, 0.47, 0.48, 0.49]
beta_all_setted = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.44, 0.44125,  0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]
beta_min = [0.39, 0.42, 0.44, 0.441, 0.46, 0.49]
#lattice = [(2 ** i, 2 ** i) for i in range(1, 10)]
setted_lattice = [(256, 256)]
b_field_all = [-1, -0.875, -0.75, -0.625, -0.5, -0.375, -0.25, -0.125, 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
#b_field_min = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
b_field_min = [0, 0.25, 0.5, 0.75, 1]
observables = [('energy', 'energy_var'), ('magnetisation', 'magnetisation_var'),
               ('specific_heat', 'heat_var'), ('chi', 'chi_var')]

'''Here lives your main measure and plot code'''
# If you have already measured the needed configs,
# then uncomment the following line!
lattice_measuring(beta_list=beta_all_setted, lattice_list=setted_lattice, external_field_list = [0])
#hysterese_measuring(beta_list=beta_min, lattice_list=setted_lattice, external_field_list = b_field_all)
#Observables.OnsagerMagn()


# Here you can call the plot function, with lists (!) for beta,
# lattice sizes and external magnetic field values
# If you only want to plot for example one magnetic field value = 0
# for some lattice sizes call lattice_plotting with external_field_list=[0]

#lattice_plotting(direc='Analyse/256x256/OhneBFeld/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables, OnlyBig = False)
#bfield_plotting(direc='Analyse/256x256/OhneBFeld/', beta_list=beta_all_setted, lattice_list=setted_lattice,
#                 external_field_list=[0], observables=observables, OnlyBig = False)
#hysterese_plotting(direc='Analyse/256x256/Hysterese/', beta_list=beta_min, lattice_list=setted_lattice,
#                 external_field_list=b_field_all, observables=observables)

   
