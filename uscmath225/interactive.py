from ipywidgets import interact, interactive, fixed, interact_manual,Layout
import ipywidgets as widgets


from functools import partial

class Interacter:
    def __init__(self):
        pass

    def angle(self,func,angle_arg_name="theta",step=15):
        param = {}
        param[angle_arg_name]=widgets.IntSlider(min=-180, max=180, step=step, value=0,continuous_update=False,layout=Layout(width='75%'))
        interact(func, **param );