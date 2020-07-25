from plotter import *
import matplotlib.patches as mpatches


title0 = (0,0,".")
axis_titles = [title0]
patch1 = mpatches.Patch(color='b', label='Rewards')

handle_list = [patch1]

plotter_params = {
    "nFig"            : 1,
    "window_titles"   : ["Reward Graph For Different Polices"],
    "nrows"           : [1],
    "ncols"           : [1],
    "font_size"       : [8],
    "fig_size"        : [(20,20)],
    "xlabel"          : ['Time Step'],
    "ylabel"          : ['Reward'],
    "xlim"            : [[-0.1,4.5]],
    "ylim"            : [[0,1.2]],
    "handles"         : [("r","Random Policy"),("G","Argmax Policy"), ("B","Policy iteration") ],
    "axis_titles"     : axis_titles,
    "save_fig"        : False,
    "file_names"      : None,
    "handle_list"     : handle_list
}
my_plotter = plotter(plotter_params)
my_plotter.set_event('onclick-point',my_plotter.fig_list[0])
my_plotter.wait()
