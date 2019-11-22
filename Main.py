"""
Sample to show how to use the RulerCompassAnimations and SquarePolygons
libraries.

Copyright (C) 2019 Sam Hartburn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

author: Sam Hartburn
email: sam@samhartburn.co.uk
website: www.samhartburn.co.uk
"""

import RulerCompassAnimations as rc
import SquarePolygons as poly

"""
1: Rectangle
2: Triangle
3: 5+ Polygon (uncomment set of points for desired polygon)
"""
plot = 1

#Define the points of your initial polygon
if (plot==1):
    #Initial coordinates rectangle
    p1 = rc.Point(0,2)
    p2 = rc.Point(5,2)
    p3 = rc.Point(5,0)
    p4 = rc.Point(0,0)
    
if (plot==2):
    #Initial coordinates triangle
    p1 = rc.Point(0,0)
    p2 = rc.Point(5,1)
    p3 = rc.Point(1,3)

if (plot==3):
    #Initial coordinates n-gon

    #regular pentagon
    #"""
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(3.93,2.85)
    p4 = rc.Point(1.5,4.62)
    p5 = rc.Point(-0.93,2.85)
    points = [p1,p2,p3,p4,p5]
    #"""
    
    #regular hexagon
    """
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(4.5,2.6)
    p4 = rc.Point(3,5.2)
    p5 = rc.Point(0,5.2)
    p6 = rc.Point(-1.5,2.6)
    points = [p1,p2,p3,p4,p5,p6]
    """
    
    #regular heptagon
    """
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(4.87,2.35)
    p4 = rc.Point(4.2,5.27)
    p5 = rc.Point(1.5,6.57)
    p6 = rc.Point(-1.2,5.27)
    p7 = rc.Point(-1.87,2.35)
    points = [p1,p2,p3,p4,p5,p6,p7]
    """
    
    #regular octagon
    """
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(5.12,2.12)
    p4 = rc.Point(5.12,5.12)
    p5 = rc.Point(3,7.24)
    p6 = rc.Point(0,7.24)
    p7 = rc.Point(-2.12,5.12)
    p8 = rc.Point(-2.12,2.12)
    points = [p1,p2,p3,p4,p5,p6,p7,p8]
    """
    
    #regular nonagon
    """
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(5.3,1.93)
    p4 = rc.Point(5.82,4.88)
    p5 = rc.Point(4.32,7.48)
    p6 = rc.Point(1.5,8.51)
    p7 = rc.Point(-1.32,7.48)
    p8 = rc.Point(-2.82,4.88)
    p9 = rc.Point(-2.3,1.93)
    points = [p1,p2,p3,p4,p5,p6,p7,p8,p9]
    """
    
    #regular decagon
    """
    p1 = rc.Point(0,0)
    p2 = rc.Point(3,0)
    p3 = rc.Point(5.43,1.76)
    p4 = rc.Point(6.35,4.62)
    p5 = rc.Point(5.43,7.47)
    p6 = rc.Point(3,9.23)
    p7 = rc.Point(0,9.23)
    p8 = rc.Point(-2.43,7.47)
    p9 = rc.Point(-3.35,4.62)
    p10 = rc.Point(-2.43,1.76)
    points = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
    """

initialColor = (0,0.45,0.7,0.8)

if (plot==1):
    #Plot rectangle
    animations = [rc.addStepPolygon([p1,p2,p3,p4], initialColor, True, 0)]
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=initialColor))
    square = poly.squareRectangle(p1,p2,p3,p4,1)
    animations.extend(square[0])
elif (plot==2):
    #Plot triangle
    animations = [rc.addStepPolygon([p1,p2,p3], initialColor, True, 0)]
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=initialColor))
    square = poly.squareTriangle(p1,p2,p3,1)
    animations.extend(square[0])
elif (plot==3):
    #Plot polygon
    animations = [rc.addStepPolygon(points, initialColor, True, 0)]
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=initialColor))
    square = poly.squarePolygon(*points,i_start=1)
    animations.extend(square[0])

#Animation will play in interactive Python screen. To save as MP4, change saveAsMP4
#below to True and specify a filename     
anim = rc.performAnimation(animations, saveAsMP4=False, filename='C:\SquareDecagon')
    

        



