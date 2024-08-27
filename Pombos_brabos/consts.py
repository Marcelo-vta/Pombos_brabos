import numpy as np
import os
import importlib.resources

def get_asset_path(relative_path):
    # Get the package path
    package_name = __package__
    
    # Access the asset using importlib.resources
    with importlib.resources.path(package_name, relative_path) as full_path:
        return full_path.__str__().replace("\\", "/")+"/"

const_G = 6.674 * 0.1

res = (1280,720)
grav = np.array([0,0.1])

title_image_day = f"{get_asset_path('assets/')}Title_Image_Day.png"