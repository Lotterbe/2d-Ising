import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FFMpegWriter
from PIL import Image, ImageShow

class Ising_Plot:
    def __init__(self, ising_data, name_data, slider_data):
        self.fig, ax = plt.subplots() #figsize=(5, 5)
        self.data = ising_data
        self.name = name_data
        self.data_number = len(self.data) - 1
        self.data = np.where(self.data == -1, 0, 1)
        self.init_data = self.data[0]
        self.slider_data = slider_data
        self.paused = False
        #print(self.data[0])
        #self.init_data = np.where(self.data[0] == -1, 0, 1)
        #print(self.init_data)
        # 'nearest' or 'bilinear'
        # ret = ax.imshow(init_data, interpolation='nearest', cmap=cm.Greys_r)
        self.im = plt.imshow(self.init_data, cmap='gist_gray_r', vmin=0, vmax=1, animated=True, origin='upper')
        self.im.axes.xaxis.tick_top()
        #self.im.set_figure(size=(5, 5))
        #print(type(self.im.set_figure()))
        # [-> pos, ^pos, length, thickness]
        axamp = plt.axes([0.25, .07, 0.50, 0.02])
        #slider_steps = (slider_data[-1] - slider_data[0])/len(slider_data)
        # Slider
        self.samp = Slider(axamp, str(self.name), self.slider_data[0], self.data_number, valinit=self.slider_data[0], valstep=1)#, valstep=slider_steps, valfmt="%s")
        self.samp.on_changed(self.update)
        axamp.xaxis.set_visible(True)
        axamp.set_xticks([0, 29, 59, 89, 119, 149])
        axamp.set_xticklabels([str(self.slider_data[0]), str(self.slider_data[29]), str(self.slider_data[59]), str(self.slider_data[89]),
        str(self.slider_data[119]), str(self.slider_data[149])])
        #plt.axvline(1.5, color = 'green')
        axamp.axvline(0, color='green')
        axamp.axvline(29, color='green')
        axamp.axvline(59, color='darkred')
        axamp.axvline(89, color='green')
        axamp.axvline(119, color='darkred')
        axamp.axvline(149, color='green')
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
        #self.playbutton.connect_event('button_press_event', self.play)
        # Animation controls
        self.is_manual = False # True if user has taken control of the animation
        self.interval = 200 # ms, time between animation frames
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
            print(type(self.axpause.images[0]))#.ImageShow #set_data()
        self.paused = not self.paused


    def start_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=self.interval)
        plt.show()

    def plot(self):
        plt.show()

    def update(self, val):
        # update curve
        # l.set_ydata(val*np.sin(t))
        self.im.set_data(self.data[int(val)])
        valtext = self.slider_data[int(val)]
        self.samp.valtext.set_text('{}'.format(valtext))
        # redraw canvas while idle
        self.fig.canvas.draw_idle()

    def update_plot(self, num):
        if self.is_manual:
            return self.im # don't change

        #val = (self.samp.val + self.scale) % self.samp.valmax
        #self.samp.set_val(val)
        val = num % self.data_number
        self.samp.set_val(val)
        self.is_manual = False # the above line called update_slider, so we need to reset this
        return self.im

        # call update function on slider value change


    #def ani_update(self, frame):
#        self.im.set_data(self.data[int(frame)])
#        self.samp.set_val(frame)
#        self.update(frame)

#    def start_ani(self):
        # ims = []
        # for i in range(len(self.slider_data)):
        #     self.ani_update(i)
        #     ims = ims + [self.im]
        #     print(type(ims))
        #
        # ani = animation.ArtistAnimation(self.fig, ims, interval=50, blit=False,
        #                         repeat_delay=1000, repeat=True)
        # plt.show()
        #
        #writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        #ani.save("Analyse/128x128/Hysterese/Visual/movie.mp4", writer=writer)
        #ani.save("Analyse/128x128/Hysterese/Visual/ani.mp4")
        #plt.show()







class Ising_Anim:
    def __init__(self, ising_data, name_data, slider_data):
        self.fig, ax = plt.subplots()
        self.data = ising_data
        self.name = name_data
        self.data_number = len(self.data) - 1
        self.data = np.where(self.data == -1, 0, 1)
        self.init_data = self.data[0]
        self.slider_data = slider_data
        #axamp = plt.axes([0.25, .03, 0.50, 0.02])
        #self.samp = Slider(axamp, str(self.name), self.slider_data[0], self.data_number, valinit=self.slider_data[0], valstep=1)
        self.start_ani()
        #, frames=149, interval=20
        #print(self.data[0])
        #self.init_data = np.where(self.data[0] == -1, 0, 1)
        #print(self.init_data)
        # 'nearest' or 'bilinear'
        # ret = ax.imshow(init_data, interpolation='nearest', cmap=cm.Greys_r)
    def start_ani(self):
        ims = []
        for i in range(len(self.data)):
            #im = plt.imshow(data[counter], animated=True)
            axamp = plt.axes([0.25, .03, 0.50, 0.02])
            self.samp = Slider(axamp, str(self.name), self.slider_data[0], self.data_number, valinit=self.slider_data[0], valstep=1)
            self.samp.on_changed(self.update)
            im = plt.imshow(self.data[i], cmap='gist_gray_r', vmin=0, vmax=1, animated=True)
            ims.append([im])

        ani = animation.ArtistAnimation(self.fig, ims, interval=50, blit=True,
                                        repeat_delay=1000)
        plt.show()

    def init_ani(self):
        im = plt.imshow(self.init_data, cmap='gist_gray_r', vmin=0, vmax=1)
        # [-> pos, ^pos, length, thickness]
        axamp = plt.axes([0.25, .03, 0.50, 0.02])
        #slider_steps = (slider_data[-1] - slider_data[0])/len(slider_data)
        # Slider
        self.samp = Slider(axamp, str(self.name), self.slider_data[0], self.data_number, valinit=self.slider_data[0], valstep=1)#, valstep=slider_steps, valfmt="%s")
        return self.samp

    def update(self, val):
            # update curve
            # l.set_ydata(val*np.sin(t))
        print('huhu')
        self.samp.set_val(val)
        #im.set_data(self.data[int(val)])
        valtext = self.slider_data[int(val)]
        self.samp.valtext.set_text('{}'.format(valtext))
            # redraw canvas while idle
        fig.canvas.draw_idle()
        return self.samp

        # call update function on slider value change
        #self.samp.on_changed(update)

        #plt.show()

        #anim.save('Analyse/128x128/Hysterese/Visual/animation.gif', writer='imagemagick', fps=60)


lat = (128,128)
b = 0.49
b_field = 0.15
b_field_array = [0, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075,
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
filepart = 'Analyse/128x128/Hysterese/Visual/'
filename = filepart + str(lat[0]) + 'x' + str(lat[1]) + 'lattice_beta_' \
          + str(b).replace('.', '') + 'external_field_' + str(b_field) + '.npz'

data = np.load(filename)
#print(type(data))
#for k in data:
#    print(k)
#ising = Ising_Anim(ising_data=data['configs'][2:], name_data='b_field', slider_data=b_field_array)
ising = Ising_Plot(ising_data=data['configs'][2:], name_data='b_field', slider_data=b_field_array)
ising.start_animation()
# lattice = (256,256)
# b_lattice = [0.39, 0.40, 0.41, 0.415, 0.42, 0.425, 0.43, 0.4325, 0.435, 0.4375, 0.44, 0.4425, 0.445, 0.4475, 0.45, 0.455, 0.46, 0.465, 0.47, 0.48, 0.49]
# b_field_lattice = 0
# name_lattice =
# filepart_lattice = 'Analyse/256x256/Observablen/Neu201229/'
# configs = []
#for beta in b_lattice:
#    filename_lattice = filepart_lattice + str(lattice[0]) + 'x' + str(lattice[1]) + 'lattice_beta_' \
#            + str(b_lattice).replace('.', '') + 'external_field_' + str(b_field_lattice) + '.npz'
#            data = np.load(filename_lattice)
#            configs = configs + data['configs'])
#ising = Ising_Plot(ising_data=configs, name_data=name_lattice, slider_data=b_lattice)
