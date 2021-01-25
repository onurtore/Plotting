"""
This python module is consisting of the functions which
are responsible for different visualization requirements
during the DBN operations.
"""

import pylab as plt
import numpy as np
import os
import subprocess
import numpy.linalg as linalg
import matplotlib.patches as mpatches
import matplotlib as mpl

from matplotlib import rc
from matplotlib.patches import Ellipse
from non_blocking import *
from mpl_toolkits.mplot3d import Axes3D

class plotter:

    def __init__(self,param):

        self.mode               = param['mode'] #rectilinear, 3d
        self.nFig               = param["nFig"]
        self.window_titles      = param["window_titles"]
        self.nrows              = param["nrows"]
        self.ncols              = param["ncols"]
        self.font_size          = param["font_size"]
        self.fig_size           = param["fig_size"]
        self.xlabel             = param["xlabel"]
        self.ylabel             = param["ylabel"]
        self.axis_titles        = param["axis_titles"]
        self.xlim               = param["xlim"]
        self.ylim               = param["ylim"]
        if self.mode == '3d':
            self.zlim           = param['zlim']
        self.save_fig           = param["save_fig"]
        self.file_names         = param["file_names"]
        self.handles            = param["handles"]
        self.curr_color         = 'b'
        self.plot_queue         = []
        self.useTex             = param['useTex']
        self.mode               = param['mode'] #rectilinear, 3d

        self.create_figs()
        self.update_figs()

    def set_color_index(self,color):

        self.curr_color = color

    def save_figures(self):
        """
        Saves all the figures
        """

        for i in range(len(self.fig_list)):
            file_name = self.file_names[i]
            self.fig_list[0].savefig('./' + file_name + '.png')

    def ellipsoid(self, ax, mean, cov, color='black'):
        # your ellispsoid and center in matrix form

        # find the rotation matrix and radii of the axes
        U, s, rotation = linalg.svd(cov)
        radii = 2*np.sqrt(s)

        # now carry on with EOL's answer
        u = np.linspace(0.0, 2.0 * np.pi, 100)
        v = np.linspace(0.0, np.pi, 100)
        x = radii[0] * np.outer(np.cos(u), np.sin(v))
        y = radii[1] * np.outer(np.sin(u), np.sin(v))
        z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
        for i in range(len(x)):
            for j in range(len(x)):
                [x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + mean

        # plot
        ax = self.ax_list[ax[0]][ax[1]]
        ax.plot_wireframe(x, y, z,  rstride=4, cstride=4, color=color, alpha=0.2)




    def plot_error_ellipses(self,means,covs,fig,axs,drawNow = True):
        """
            Wrapper function for drawing multiple ellipses at 
            same time without drawing each of the indivudually
        """

        for i in range(0, len(means)):
            self.plot_error_ellipse(axs,means[i], covs[i], False)

        if drawNow == True:
            self.update_figs()

    def plot_confidence_ellipse(self):
        """
            To-Do
                Implement it
            
            Plots the confidence ellipse 
        """

        print("Not implemented yet")
        return None

    def plot_error_ellipse(self,ax,pos, cov, dashed, color='black'):

        """
            Plots the 2 standard deviation error ellipse.
        """

        ax = self.ax_list[ax[0]][ax[1]]
        def eigsorted(cov):

            vals, vecs = np.linalg.eigh(cov)
            order = vals.argsort()[::-1]
            return vals[order], vecs[:, order]

        vals, vecs = eigsorted(cov)
        theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))


        ls = 'dashed' if dashed else 'solid'
        width, height = 4 * np.sqrt(vals)

        ellipse = Ellipse(xy=pos, width=width, height=height, angle=theta, lw=1, alpha=0.90,
                        fill=False, linestyle=ls, color=color)
        ax.add_artist(ellipse)

    def annotate3d(self,ax,text,coordinate,color='black', drawNow = True, size= 1):

        self.ax_list[ax[0]][ax[1]].text(coordinate[0],coordinate[1],coordinate[2], text, color= color, size=size)
        if drawNow == True:
            self.update_figs()


    def annotate2d(self,ax,text,coordinate,color = 'black',drawNow = True, size=1 ):
        """
            Annotate the given coordinate point
        """

        self.ax_list[ax[0]][ax[1]].annotate(text, coordinate,color=color ,size = size)
        if drawNow == True:
            self.update_figs()

    def kill_all_python():
        """
            Kills the all plots/python scripts that are running
            this method will kill itself too
        
        """

        #For python2
        subprocess.call(["bash","-c",'pyIDs=($(pgrep python));for x in "${pyIDs[@]}"; do if [ "$x" -ne '+str(os.getpid())+' ];then  kill -9 "$x"; fi done'])

        #For python3
        #subprocess.call(["bash","-c",'pyIDs=($(pgrep python));for x in "${pyIDs[@]}"; do if [ "$x" -ne '+str(os.getpid())+' ];then  kill -9 "$x"; fi done'])



    def point3d(self,data,ax, color='b', drawNow = True,s=3):
        """
            Plots a point to the given axes.

            data: X,Y,Z tuple
            ax:   just a list consist of [figure_no,axis_no], example: [0,0]
            color: 
            drawNow: directly updates graphs
        """
        self.ax_list[ax[0]][ax[1]].scatter(data[0],data[1],data[2], c = color,s=s)

        if drawNow == True:
            self.update_figs()

    def point2d(self,data,ax, color ='b', drawNow = True,s= 3):
        """
            Plots a point to the given axes.

            data: X,Y tuple
            ax:   just a list consist of [figure_no,axis_no], example: [0,0]
            color: 
            drawNow: directly updates graphs
        """

        self.ax_list[ax[0]][ax[1]].scatter(data[0],data[1], c = color,s=s)

        if drawNow == True:
            self.update_figs()

    def line2d(self,data,ax,color='b',drawNow = True, s=1):

        self.ax_list[ax[0]][ax[1]].plot(data[0],data[1], linewidth=s, color=color)
        if drawNow == True:
            self.update_figs()


    def set_title(self,axs,title,drawNow = True):
        """
            Sets the title for the given axes
        """

        self.ax_list[ax[0]][ax[1]].set_title(title)

        if drawNow == True:
            self.update_figs()

    def wait(self):
        kb = KBHit()
        print('Hit any key, or ESC to exit')


        while True:

            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    input()


            self.update_figs()

        kb.set_normal_term()


    def add_handle(self,axs,color, label):
        handles, labels = self.ax_list[axs[0]][axs[1]].get_legend_handles_labels()
        patch = mpatches.Patch(color=color, label=label)
        handles.append(patch) 
        self.ax_list[axs[0]][axs[1]].legend(handles=handles)

    def set_event(self,mode,fig):
        if mode == 'onclick-point':
            cid = fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self,event):
        x = event.xdata
        y = event.ydata
        self.point((x,y), None,event.inaxes)


    def create_figs(self):
        """
            Creates the figures with the given parameters
        """


        if self.useTex == True:
            #Use latex
            rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            rc('text', usetex=True)
            mpl.rcParams['figure.dpi'] = 300


        self.fig_list = []
        self.ax_list  = []
        for i in range(self.nFig):
            print "Generating ", i, "th fig"
            plt.rc('font', size=self.font_size[i])# controls default text sizes
            handle_list = []
            subplot_kw = {
                'projection': self.mode
            }
            curr_fig, curr_axs = plt.subplots(self.nrows[i],self.ncols[i],figsize=self.fig_size[i], subplot_kw = subplot_kw)
            curr_fig.canvas.set_window_title(self.window_titles[i])

            if self.nrows[i] == 1:
                curr_axs = [curr_axs]

            curr_fig.suptitle(self.window_titles[i])

            for j in range(len(curr_axs)):
                curr_axs[j].set_xlabel(self.xlabel[i])
                curr_axs[j].set_ylabel(self.ylabel[i])
                curr_axs[j].set_xlim(self.xlim[i])
                curr_axs[j].set_ylim(self.ylim[i])
                if self.mode == '3d':
                    curr_axs[j].set_zlim(self.zlim[i])
                curr_axs[j].set_title(self.axis_titles[ (i * len(curr_axs) ) + j][2])

            for curr_handle in self.handles:
                if curr_handle[0] == "-1":
                    curr_handle[0] = self.curr_color

                handle_list.append(mpatches.Patch(color=curr_handle[0], label=curr_handle[1]))


            curr_fig.legend(  handles = handle_list, prop={'size': self.font_size[i]}   )

            self.fig_list.append(curr_fig)
            self.ax_list.append(curr_axs)





    #Updating figures in a hard way. 
    #I am not very good with matplotlib internals
    #and some of the figures do not update, so i had
    #to it with this way. 
    def update_figs(self):
        idx = 0
        for i in self.fig_list:
            i.canvas.draw()
            print idx, "th figure updated"
            idx += 1
        plt.draw()
        plt.pause(0.02)

    def draw_vector3D(self,X,Y,Z,U,V,W, ax,color = 'b', drawNow = True):
        self.ax_list[ax[0]][ax[1]].quiver(X,Y,Z,U,V,W,color=color)

        if drawNow == True:
            self.update_figs()

    def draw_line(self,data,fig,ax,color = 'b', drawNow = True):

        x = data[0]
        y = data[1]
        for i in range(0, len(x)):
            curr_x = x[i:i+2]
            curr_y = y[i:i+2]
            plt.plot(x[i:i+2], y[i:i+2], color + 'o-')

        if drawNow == True:
            self.update_figs()


    def normalize_vector(self,x):
        return x / np.linalg.norm(x)
