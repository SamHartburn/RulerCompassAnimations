# RulerCompassAnimations
Animated ruler-and-compass constructions

Code is offered as-is for anyone who is interested. It works for Python 3. It is messy, undocumented, has no error handling and is probably full of bugs. Feel free to download and play but don't expect it to be perfect.

To see the animation you will need python to open an interactive window. If you use the command line, "python -i Main.py" should work. If you use Spyder on a PC, you can do this by going to Tools > preferences > IPython console > Graphics > Graphics backend and setting Backend to Automatic. If you use anything else, you'll have to figure it out for yourself.

You will need to install the following libraries:
* NumPy (see https://docs.scipy.org/doc/numpy/user/install.html)
* Matplotlib (see https://matplotlib.org/3.1.1/users/installing.html)

Main.py shows how to use the SquarePolygons library. Run this file as-is to see an animation of construction of a square with the same area as a given rectangle, or change the code as indicated in the comments to see construction of a square with the same area as a given polygon. It probably only works for convex polygons.

SquarePolygons.py is a library to use RulerCompassAnimations to construct a square with the same area as a given polygon.

RulerCompassAnimations.py is a library to use Matplotlib to create ruler-and-compass constructions. It includes basic constructions such as perpendicular bisector, and helper functions such as calculating distances between points.

RulerCompassAnimations.mplstyle defines Matplotlib styles to use.

I welcome contructive feedback and collaboration and would love to hear your comments. If you think you can improve the code then feel free to submit a pull request and let me know what you've changed and why.
