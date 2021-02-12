import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FFMpegWriter
from PIL import Image, ImageShow

class Ising_Ani:
    def __init__(self, ising_data, name_data, slider_data, configs_per_value=1):
        self.fig, ax = plt.subplots() #figsize=(5, 5)
        self.data = ising_data
        self.name = name_data
        self.data_number = len(self.data) - 1
        self.data = np.where(self.data == -1, 0, 1)
        self.init_data = self.data[0]
        self.slider_data = slider_data
        self.configs_per_value = configs_per_value
        self.paused = False
        self.im = plt.imshow(self.init_data, cmap='gist_gray_r', vmin=0, vmax=1, animated=True, origin='upper')
        self.im.axes.xaxis.tick_top()
        #self.im.set_figure(size=(5, 5))
        # [-> pos, ^pos, length, thickness]
        axamp = plt.axes([0.25, .07, 0.50, 0.02])
        # Slider
        self.samp = Slider(axamp, str(self.name), valmin=0, valmax=self.data_number, valinit=self.slider_data[0],valstep=1)#, valstep=slider_steps, valfmt="%s")
        self.samp.on_changed(self.update_slider)
        axamp.xaxis.set_visible(True)
        x_start = 0*self.configs_per_value
        x_first_return = 29*self.configs_per_value
        x_first_zero = 59*self.configs_per_value
        x_second_return = 89*self.configs_per_value
        x_second_zero = 119*self.configs_per_value
        x_end = 149*self.configs_per_value
        field_values = np.array(self.slider_data)
        x_zeros = np.array(np.where(field_values == 0))[0] *self.configs_per_value
        x_maxs = np.array(np.where(field_values == np.max(field_values)))[0]*self.configs_per_value
        x_mins = np.array(np.where(field_values == np.min(field_values)))[0]*self.configs_per_value
        for zero in x_zeros:
            axamp.axvline(zero, color='darkred')
        for max in x_maxs:
            axamp.axvline(max, color='green')
        for min in x_mins:
            axamp.axvline(min, color='green')
        x_total = np.sort(np.append(np.append(x_zeros, x_maxs), x_mins))
        x_indices = x_total/self.configs_per_value
        x_label = []
        for index in x_indices:
            x_label.append(str(self.slider_data[np.int(index)]))
        axamp.set_xticks(x_total)#, x_end])
        axamp.set_xticklabels(x_label)#,
        empty_box = Image.new(mode='RGBA', size=(600, 400), color='rgba(0,0,0,0)')
        self.mybox = empty_box.copy()
        img = Image.open('orig.png').resize((400, 200))
        img = img.convert('RGBA')
        self.mybox.paste(img, (100,100))
        img_ret = Image.open('return.png').resize((700, 600))
        self.myreturn = Image.new(mode='RGBA', size=(800, 650), color='rgba(0,0,0,0)')
        self.myreturn.paste(img_ret, (50,25))
        #ImageShow.show(mybox)
        self.axplay = plt.axes([0.05, .07, 0.05, 0.04])
        self.playbutton = Button(self.axplay, label='$\u25B6$', image=self.myreturn)
        self.axplay.images[0].set_alpha(0)
        self.playbutton.on_clicked(self.play)
        self.axpause = plt.axes([0.1, .07, 0.05, 0.04])
        self.pausebutton = Button(self.axpause, label='', image=self.mybox)
        self.pausebutton.on_clicked(self.pause)

        # Animation controls
        self.is_manual = False # True if user has taken control of the animation
        self.interval = 50 # ms, time between animation frames
        #self.loop_len = 5.0 # seconds per loop
        #self.scale = self.interval/1000/self.loop_len
        #self.plot()
        #self.start_ani()

    def play(self, val):
        self.playbutton.label.set_text('')
        self.axplay.images[0].set_alpha(1)
        self.start_animation()


    def pause(self, val):
        if self.paused:
            self.ani.event_source.start()
            self.pausebutton.label.set_text('')
            self.axpause.images[0].set_alpha(1)
        else:
            self.ani.event_source.stop()
            self.pausebutton.label.set_text('$\u25B6$')
            self.axpause.images[0].set_alpha(0)
        self.paused = not self.paused

    def start_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.interval, repeat=False, save_count=self.data_number)

    def plot(self):
        plt.show()

    def update_slider(self, val):
        self.im.set_data(self.data[int(val)])
        valtext = self.slider_data[int((val - val%self.configs_per_value)/self.configs_per_value)]
        self.samp.valtext.set_text('{}'.format(valtext))
        # redraw canvas while idle
        self.fig.canvas.draw_idle()

    def update_plot(self, num):
        if self.is_manual:
            return self.im # don't change
        val = num % self.data_number
        self.samp.set_val(val)
        self.is_manual = False # the above line called update_slider, so we need to reset this
        return self.im

    def save(self, name='ising_model', dtype='ffmpeg'):
        """Ermoeglicht das Speichern der zuvor gezeigten
        Simulation

        :param name: Name der Datei
        :param dtype: Dateityp zum Speichern
        """
        Writer = animation.writers['ffmpeg']
        writer = Writer(metadata=dict(artist='Me'), fps=10) # bitrate=1800
        self.ani.save(name + '.mp4', writer=writer)

        if(dtype=='html'):
            file = open(name + '.html', "w")
            file.write(
                '<!DOCTYPE html> <html> <head> <meta charset="utf-8"/>'
                '<title>Projektpraktikum M. Weitz und L. Debus</title>'
                '</head> <body> <div align="center"> <h1>Simulation Ising Modell</h1>'
                '<video width="50%" controls> <source src="' + name + '.mp4' +
                '" type="video/mp4"/> Your browser does not support the video tag.'
                '</video> </div> </body> </html> '
            )
            file.close()



#lat = (128,128)
#lat = (256,256)
#lat = (512,512)
#b = 0.49
#b_field = 0.15
# b_field_array = [0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
#                     0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125,
#             0.13, 0.135, 0.14, 0.145, 0.15, 0.145, 0.14, 0.145, 0.13, 0.125, 0.12, 0.115, 0.11, 0.105, 0.10,
#             0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
#             0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
#             -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.105, -0.11,
#             -0.115, -0.12, -0.125, -0.13, -0.135, -0.14, -0.145, -0.15, -0.145, -0.14, -0.135, -0.13, -0.125,
#             -0.12, -0.115, -0.11, -0.105, -0.10, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
#             -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
#             0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
#             0.09, 0.095, 0.1, 0.105, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15]
#filepart = 'Analyse/128x128/Hysterese/Visual/MORECONFIGS'

#b_field = 0.05
#b_field = 0.1
#b_field = 0.15
# filepart = 'Analyse/128x128/Hysterese/Visual/MORECONFIGSLESSFIELD'
# filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
#           + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
#
# b_field_array = [0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
#                    0.08, 0.085, 0.09, 0.095, 0.1, 0.095, 0.09, 0.085, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025,
#            0.02, 0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045,
#            -0.05, -0.055, -0.06, -0.065, -0.07, -0.075, -0.08, -0.085, -0.09, -0.095, -0.1, -0.095, -0.09, -0.085, -0.08, -0.075, -0.07, -0.065, -0.06,
#            -0.055, -0.05, -0.045, -0.04, -0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0, 0.005, 0.01,
#            0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085,
#            0.09, 0.095, 0.1]
# data = np.load(filename)
# print(len(data['configs']))
# ising = Ising_Plot(ising_data=data['configs'][int(40*20):], name_data='b_field', slider_data=b_field_array[40:], configs_per_value=20)
# ising.start_animation()
# ising.save()
#ising.save(dtype='html')

#plt.show()


# b_field = 0
# filepart = 'Analyse/256x256/Observablen/Neu_201229/'#MORECONFIGS'
# beta_array = [0.39, 0.395, 0.4, 0.405, 0.41, 0.4125, 0.415, 0.4175, 0.42, 0.4225, 0.425, 0.4275, 0.43, 0.43125, 0.4325, 0.43375, 0.435, 0.43625, 0.4375, 0.43875, 0.43894, 0.43896, 0.43898, 0.44, 0.4402, 0.4404, 0.4406, 0.4408, 0.441, 0.4412, 0.44125, 0.4414, 0.4416, 0.4418, 0.4425, 0.44375, 0.445, 0.44625, 0.4475, 0.44875, 0.45, 0.4525, 0.455, 0.4575, 0.46, 0.4625, 0.465, 0.4675, 0.47, 0.475, 0.48, 0.485, 0.49]
#
# for bet in beta_array:
#     filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
#           + str(bet).replace('.', '') + 'external_field_' + str(b_field) + '.npz'
#     newdata = np.load(filename)
#     if bet > 0.39:
#         data_array = np.append(data_array, newdata['configs'][::2], axis=0)
#     else:
#         data_array = newdata['configs'][::2]

#ising = Ising_Ani(ising_data=data_array, name_data='beta', slider_data=beta_array, configs_per_value=int(200/2))
#ising.start_animation()
#ising.save(name='ising_model_all_betas')

#plt.show()
