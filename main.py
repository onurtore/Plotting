from plotter import *
import matplotlib.patches as mpatches


title0 = (0,0,".")
axis_titles = [title0]
patch1 = mpatches.Patch(color='b', label='Rewards')

handle_list = [patch1]

plotter_params = {
        "mode"            : 'rectilinear', #it can be also 3d
        "nFig"            : 1,
        "window_titles"   : ["Spline"]*1,
        "nrows"           : [1] * 1,
        "ncols"           : [1] * 1,
        "font_size"       : [4]  * 1 ,
        "fig_size"        : [(4,3)] *1,
        "xlabel"          : ['Time Step'] * 1 ,
        "ylabel"          : ['EE Pose']   * 1,
        "xlim"            : [[-10,210]]   * 1,
        "ylim"            : [[0.2,0.350]],
        "handles"         : [("Blue","DBN Sampled Keyframe")],
        "axis_titles"     : axis_titles,
        "save_fig"        : False,
        "file_names"      : None,
        "vis_until"       : 1,
        "handle_list"     : handle_list,
        "useTex"          : True
}


my_plotter = plotter(plotter_params)
my_plotter.set_event('onclick-point',my_plotter.fig_list[0])
my_plotter.wait()
