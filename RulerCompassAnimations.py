"""
RulerCompassAnimations
Library to use Matplotlib to create ruler-and-compass constructions
Includes basic constructions such as perpendicular bisector, and helper
functions such as calculating distances between points

author: Sam Hartburn
email: sam@samhartburn.co.uk
website: www.samhartburn.co.uk
"""

"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import patches as pat

plt.style.use('RulerCompassAnimations.mplstyle')

speed = 1

fig = plt.figure()
ax = plt.axes()

class Animatable:
    def __init__(self, type, obj, start, end, i_min, radius=0, angle=0):
        self.type = type
        self.obj= obj
        self.start = start
        self.end = end
        self.i_min = i_min
        if (type=='line'):
            self.distance = distanceBetweenPoints(start, end)
        elif (type=='arc'):
            theta = abs(end - start)
            self.radius = radius
            self.distance = 2*math.pi*radius*theta/360
        elif (type=='polygon'):
            self.distance=(end-start)*speed
        elif (type=='lineTransform'):
            self.distance = abs(2*math.pi*distanceBetweenPoints(start[0], start[1])*angle/360)
            self.transform = [end[0].x-start[0].x,end[0].y-start[0].y]
            self.angle = angle
        self.frames=math.ceil(self.distance/speed)
        self.i_max = i_min+self.frames
        self.frameToUnemphasise = -1
        self.frameToHide = -1
        self.hide = True
        self.style=Style()
        
    def setStyle(self, style):
        #print(style.stdColour)
        self.style=style
        
class Style:
    def __init__(self, stdColour='black', stdLineWidth=0.5, stdLineStyle='--',
                 stdFaceColour='black', stdEdgeColour='black',
                 emphColour='black', emphLineWidth=1, emphLineStyle='-',
                 emphFaceColour='black', emphEdgeColour='black',):
        self.stdColour=stdColour
        self.stdLineWidth=stdLineWidth
        self.stdLineStyle=stdLineStyle
        self.stdFaceColour=stdFaceColour
        self.stdEdgeColour=stdEdgeColour
        self.emphColour=emphColour
        self.emphLineWidth=emphLineWidth
        self.emphLineStyle=emphLineStyle
        self.emphFaceColour=emphFaceColour
        self.emphEdgeColour=emphEdgeColour
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def list(self):
        return [self.x,self.y]
    
class LineTransform:
    def __init__(self, pos1Start, pos1End):
        self.pos1Start = pos1Start
        self.pos1End = pos1End
        self.length = distanceBetweenPoints(pos1Start, pos1End)
        self.angleWithX = angleWithXAxis(pos1Start, pos1End)
        self.angleToRotate = 0
        self.pos2Start = Point(0,0)
        self.pos2End = Point(0,0)
        
    def setEndPoint(self, pos2Start, angleToRotate):
        self.pos2Start = pos2Start
        self.angleToRotate = angleToRotate
        self.pos2End = extendLineAngle(pos2Start, self.length, angleToRotate+self.angleWithX)
           
#Construct perpendicular bisector of line segment from p1 to p2
#Extend the line so that it goes minLength beyond the second bisector point
#i_start is the frame the animation should start at
#Returns a list of the animations reqired
def perpendicularBisector(p1,p2,minLength,i_start):
    
    #Setting arc radius to 0.75 * distance between points guarantees that the arcs will intersect
    radius = distanceBetweenPoints(p1,p2)*0.75
    angleWithX = angleWithXAxis(p1,p2)
    
    #Draw the arcs. Rotation angles are calculated so that the arcs will intersect
    animations=addStepArc(centre=p1, radius=radius, rotation=angleWithX+300, theta1=0, 
                                 theta2=20, i_start=i_start)

    animations.extend(addStepArc(centre=p1, radius=radius, rotation=angleWithX+40, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    animations.extend(addStepArc(centre=p2, radius=radius, rotation=angleWithX+120, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
      
    animations.extend(addStepArc(centre=p2, radius=radius, rotation=angleWithX+220, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
      
    #Find the points where the arcs intersect - use a slightly larger radius so that the line goes beyond the intersection points
    bisectorPoints = circleIntersects(p1, p2, radius*2.1/2)
    
    #Extend the line by minLength beyond the second intersection
    bisectorPoints[1] = extendLine(bisectorPoints[0], bisectorPoints[1], minLength)
  
    #Add the line animation
    line = addStepLine(point1=bisectorPoints[0], point2=bisectorPoints[1], i_start=animations[-1].i_max+1)
    animations.append(line)
    
    return animations

#Construct perpendicular to line through lineP1 and lineP2, going through point
#point must be a point on the line
#i_start is the frame the animation should start at
#Returns a list of the animations reqired
def perpendicularThroughPointOnLine(lineP1, lineP2, point, i_start):
    
    #The perpendicular is constructed by drawing two arcs with equal radius, centred at point, then constructing the
    #perpendicular bisector of the points where the arcs intersect the line
    radius = distanceBetweenPoints(lineP1, point)
    angleWithX = angleWithXAxis(lineP1, lineP2)
    lineP3 = extendLine(lineP1, point, radius)
    
    animations = addStepArc(centre=point, radius=radius, rotation=angleWithX+170, theta1=0, 
                                 theta2=20, i_start=i_start)
    
    animations.extend(addStepArc(centre=point, radius=radius, rotation=angleWithX+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    animations.extend(perpendicularBisector(lineP1, lineP3, 0, animations[-1].i_max+1))
        
    return animations

#Construct line parallel to line through lineP1 and lineP2, going through point
#i_start is the frame the animation should start at
#Returns a list of the animations reqired
def parallelLineThroughPoint(lineP1, lineP2, point, i_start):
    
    #Construction works by copying angle point-lineP1-lineP2 with point at the vertex
    baseLine = distanceBetweenPoints(lineP1,lineP2)
    #First arc should pass somewhere between lineP1 and lineP2, so set radius accordingly
    radius1 = baseLine*0.75
    
    vertexToPoint = distanceBetweenPoints(lineP1,point)
    
    #draw a line from lineP1, going through point
    animations = [addStepLine(point1=lineP1, point2=extendLine(lineP1, point, vertexToPoint*0.75), i_start=i_start)]
       
    #find the size of the angle to copy
    angleToCopy = angleThreePoints(lineP2, lineP1, point)
    
    angleWithX = angleWithXAxis(lineP1,lineP2)
    centre1 = extendLine(lineP1, point, radius1-vertexToPoint)
    
    #work out where to draw the arcs to make sure they intersect with the line and each other
    a = anticlockwiseAngleThreePoints(point,lineP1,lineP2)
    if (a<=180):
        arcAngle1 = angleWithXAxis(lineP1, point)+350
        if (distanceBetweenPoints(centre1,lineP1)<vertexToPoint):
            arcAngle2 = angleWithXAxis(lineP1, point)+angleThreePoints(point, centre1, extendLineAngle(lineP1,radius1,angleWithX))+350
        else:
            arcAngle2 = angleWithXAxis(centre1,lineP1)-angleThreePoints(point, centre1, extendLineAngle(lineP1,radius1,angleWithX))+350
    else:
        arcAngle1 = angleWithX+350
        if (distanceBetweenPoints(centre1,lineP1)<vertexToPoint):
            arcAngle2 = angleWithXAxis(lineP1, point)-angleThreePoints(point, centre1, extendLineAngle(lineP1,radius1,angleWithX))+350
        else:
            arcAngle2 = angleWithXAxis(centre1,lineP1)+angleThreePoints(point, centre1, extendLineAngle(lineP1,radius1,angleWithX))+350
        
    #the first two arcs are centered at lineP1 and point     
    animations.extend(addStepArc(centre=lineP1, radius=radius1, rotation=arcAngle1, theta1=0, 
                                 theta2=angleToCopy+20, i_start=animations[-1].i_max+1))
    
    animations.extend(addStepArc(centre=point, radius=radius1, rotation=arcAngle1, theta1=0, 
                                 theta2=angleToCopy+20, i_start=animations[-1].i_max+1))
    
    radius2 = thirdSideEnclosedAngle(radius1, radius1, angleToCopy)
    
    #the second two arcs are centred at the points where the first two arcs cross the line from lineP1 to point
    animations.extend(addStepArc(centre=centre1, radius=radius2, rotation=arcAngle2, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    centre2 = extendLine(lineP1, point, radius1)
    animations.extend(addStepArc(centre=centre2, radius=radius2, rotation=arcAngle2, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    #the parallel line joins point to the place where the two upper arcs intersect
    parallel1 = extendLineAngle(point, baseLine*-1.1, angleWithX)
    parallel2 = extendLineAngle(point, baseLine*1.1, angleWithX)
    animations.append(addStepLine(point1=parallel1, point2=parallel2, i_start=animations[-1].i_max+1))
    
    
    return animations

#construct the centre of a circle
#yes, the centre is passed in as an argument. but we want to show how to find it using
#ruler and straight edge
def centreOfCircle(centre, radius, i_start):
    #from https://www.mathopenref.com/printcirclecenter.html
    
    #Draw two chords of the circle
    #We need four points on the circle
    #Choose four angles and use trig form of point on circle to find points
    angles = [30, 90, 120, 205]
    points = []
    for theta in angles:
        x = centre.x+radius*math.cos(math.radians(theta))
        y = centre.y+radius*math.sin(math.radians(theta))
        points.append(Point(x,y))
        
    animations=[addStepLine(points[0], points[1],i_start)]
    animations.append(addStepLine(points[2], points[3],animations[-1].i_max+1))
    
    animations.extend(perpendicularBisector(points[0],points[1],radius,animations[-1].i_max+1))
    animations.extend(perpendicularBisector(points[2],points[3],radius,animations[-1].i_max+1))
    
    return animations

"""
sort out later
#draw a diameter of a circle by drawing a chord and constructing its perpendicular
#bisector
#angle is the desired angle of the diameter with the x-axis
def diameterOfCircle(centre, radius, angle, i_start):
    
    #The chord should be perpendicular to the desired diameter angle
    chordAngle = angle + 90
    pointAngles = [30, 90, 135, 220]
    points = []
    for theta in angles:
        x = centre.x+radius*math.cos(math.radians(theta))
        y = centre.y+radius*math.sin(math.radians(theta))
        points.append(Point(x,y))
        
    animations=[addStepLine(points[0], points[1],i_start)]
    animations.append(addStepLine(points[2], points[3],animations[-1].i_max+1))
    
    animations.extend(perpendicularBisector(points[0],points[1],radius,animations[-1].i_max+1))
    animations.extend(perpendicularBisector(points[2],points[3],radius,animations[-1].i_max+1))
    
    return animations
"""

#Create an animation to add an arc
#theta1 and theta2 are the angles (with the x-axis) that the arc should start and stop
#at. If theta2>theta1 it will be drawn anti-clockwise, otherwise it will be drawn clockwise
#The whole thing is then rotated by the value in rotation.
def addStepArc(centre, radius, rotation, theta1, theta2, i_start):
    
    #Create the arc and add it to the plot
    #Pass in theta1 for both angles, so it is invisible at first
    arc = pat.Arc((centre.x,centre.y), radius*2, radius*2, rotation, theta1, theta1)
    ax.add_patch(arc)
    
    #Create the object that defines how the arc should be animated
    steps = [Animatable('arc', arc, theta1, theta2, i_start, radius)]
    #Draw a line at the same time, showing where the centre of the arc is and
    #rotating to match the point on the arc that is currently being drawn
    lt = LineTransform(centre, extendLineAngle(centre, radius, rotation+theta1))
    lt.setEndPoint(centre, theta2-theta1)
    step2 = addStepLineTransform(lt, i_start)
    #The line should be hidden when the arc has finished
    step2.frameToHide = step2.i_max+1
    steps.append(step2)
        
    return steps

#create an animation to add a polygon
def addStepPolygon(points, initialColor, visible, i_start, pause=10):
    
    #build list of points in correct format for matplotlib
    pts = []
    for p in points:
        pts.append(p.list())
    
    poly = plt.Polygon(pts,facecolor=initialColor)
    poly.set_visible(visible)
    ax.add_patch(poly)
    step = Animatable('polygon', poly, 0, pause, i_start)
    step.hide = False
            
    return step

#create an animation to add a polygon, drawing the lines first
def addStepDrawPolygon(points, initialColor, visible, i_start):
    
    #build list of points in correct format for matplotlib
    pts = []
    steps = []
    for p in points:
        pts.append(p.list())
        
    for i in range(0,len(points)-1):
        if (i==0):
            start=i_start
        else:
            start=steps[-1].i_max+1
        steps.append(addStepLine(points[i],points[i+1],start))
        
    steps.append(addStepLine(points[-1],points[0],steps[-1].i_max+1))
    
    steps.append(addStepPolygon(points, initialColor, visible, steps[-1].i_max+1))
            
    return steps

#create an animation to add a line
def addStepLine(point1, point2, i_start):
    
    line, = ax.plot([], [])
    #line = plt.Line2D([],[])
    step = Animatable('line', line, point1, point2, i_start)
    
    return step

#create an animation to move and rotate a line
def addStepLineTransform(lt, i_start):
    
    line, = ax.plot([], [])
    #line = plt.Line2D([],[])
    step = Animatable('lineTransform', line, [lt.pos1Start, lt.pos1End], [lt.pos2Start, lt.pos2End], i_start, angle=lt.angleToRotate)
    
    return step

#Set the frame at which each animation should be unemphasised
def setStepEndFrame(animations, frame):
    
    for a in animations:
        a.frameToUnemphasise=frame
    return animations

#Find height of triangle, assuming that p1 and p3 are the vertices on the base
def heightOfTriangle(p1, p2, p3):
    
    a = distanceBetweenPoints(p1,p2)
    b = distanceBetweenPoints(p2,p3)
    c = distanceBetweenPoints(p1,p3)
    
    height = 0.5 * math.sqrt((a+b+c)*(b+c-a)*(a-b+c)*(a+b-c))/c
    
    return height

#Find the distance between p1 and p2
def distanceBetweenPoints(p1,p2):
    distance = math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
    return distance

#Find the angle between the points given (0 to 180 degrees)
def angleThreePoints(end1,vertex,end2):
    
    a = distanceBetweenPoints(end1,vertex)
    b = distanceBetweenPoints(end2,vertex)
    c = distanceBetweenPoints(end1,end2)
    
    angle = math.degrees(math.acos((a**2+b**2-c**2)/(2*a*b)))
    
    return angle

#Find the clockwise angle between the points given
def anticlockwiseAngleThreePoints(end1,vertex,end2):
    
    #convert both arms of vertex into vectors
    x1 = end1.x-vertex.x
    y1 = end1.y-vertex.y
    
    x2 = end2.x-vertex.x
    y2 = end2.y-vertex.y
    
    angle1 = math.degrees(math.atan2(x1*y2-y1*x2, x1*x2+y1*y2))
    
    return (angle1 + 360) % 360

#Find the third side of a triangle, given the other two sides and the enclosed angle
def thirdSideEnclosedAngle(a, b, angle):
    
    c = math.sqrt(a**2+b**2-2*a*b*math.cos(math.radians(angle)))
    
    return c

#Use sine rule to find angle opposite l2, given l1 and its opposite angle
def angleSineRule(l1, a1, l2):
    
    a2 = math.degrees(math.asin((l2*math.sin(math.radians(a1)))/l1))
    
    return a2
    
#Find the angle that the line through p1 and p2 makes with the x axis
def angleWithXAxis(p1,p2):
    x1=p1.x
    y1=p1.y
    x2=p2.x
    y2=p2.y
      
    if (abs(x1-x2)==0):
        if (y2>y1):
            angle = 90
        else:
            angle = 270
    elif (abs(y1-y2)==0):
        if (x2>x1):
            angle = 0
        else:
            angle = 180
    else:
        angle = math.degrees(math.atan(abs(y1-y2)/abs(x1-x2)))
        if (y2<y1 and x2>x1):
            angle = 360 - angle
        elif (y2>y1 and x2<x1):
            angle = 180 - angle
        elif (y2<y1 and x2<x1):
            angle = 180 + angle
    return angle

#Return the point reached by extending the line from p1 to p2 by length
def extendLine(p1,p2,length):
    angle = math.radians(angleWithXAxis(p1,p2))
    x = p2.x+length*math.cos(angle)
    y = p2.y+length*math.sin(angle)
    return Point(x,y)

#Return the point reached by extending the line from p1 by length at angle to x axis
def extendLineAngle(p1,length,angle):
    x = p1.x+length*math.cos(math.radians(angle))
    y = p1.y+length*math.sin(math.radians(angle))
    return Point(x,y)

#Find the midpoint of p1 and p2
def midpoint(p1,p2):
    x=(p1.x+p2.x)/2
    y=(p1.y+p2.y)/2
    return Point(x,y)

#Find the points where the two circles with centre1 and centre 2 intersect. Assumes that radius is the same for
#both circles
def circleIntersects(centre1, centre2, radius):
    mp = midpoint(centre1, centre2)
    d = distanceBetweenPoints(centre1, mp)
    x1 = mp.x + (math.sqrt(radius**2-d**2)*(centre2.y-centre1.y))/(2*d)
    x2 = mp.x - (math.sqrt(radius**2-d**2)*(centre2.y-centre1.y))/(2*d)
    y1 = mp.y - (math.sqrt(radius**2-d**2)*(centre2.x-centre1.x))/(2*d)
    y2 = mp.y + (math.sqrt(radius**2-d**2)*(centre2.x-centre1.x))/(2*d)
    return [Point(x1,y1),Point(x2,y2)]   

#animate function is called for each frame, up to the number of frames passed in to FuncAnimation
#animations is a list of objects of type Animatable
def animate(frame, animations):
    objects = []
    for a in animations:
        if (frame>=a.i_min and frame<=a.i_max):
            i = frame - a.i_min
            if (a.type=='arc'):
                if (a.end > a.start):
                    a.obj.theta2 = a.start+((a.end-a.start)/a.frames)*i
                else:
                    a.obj.theta1 = a.start/a.frames*(a.i_max-a.i_min-i)
            elif (a.type=='line'):
                x = np.linspace(a.start.x, a.start.x+(a.end.x-a.start.x)*i/a.frames, 2)
                y = np.linspace(a.start.y, a.start.y+(a.end.y-a.start.y)*i/a.frames, 2)
                a.obj.set_data(x,y)
            elif (a.type=='lineTransform'):
                x1=a.start[0].x
                y1=a.start[0].y
                x2=a.start[1].x
                y2=a.start[1].y
                angle=a.angle*i/a.frames
                cos=math.cos(math.radians(angle))
                sin=math.sin(math.radians(angle))
                x = np.linspace(x1+a.transform[0]*i/a.frames, x1+(x2-x1)*cos-(y2-y1)*sin+a.transform[0]*i/a.frames, 2)
                y = np.linspace(y1+a.transform[1]*i/a.frames, y1+(x2-x1)*sin+(y2-y1)*cos+a.transform[1]*i/a.frames, 2)
                a.obj.set_data(x,y)
            else:
                a.obj.set_visible(True)
                
        if (a.frameToHide == frame and a.hide == True):
            a.obj.set_visible(False)
        
        if (frame<a.frameToUnemphasise):
            a.obj.set_color(a.style.emphColour)
            a.obj.set_linestyle(a.style.emphLineStyle)
            a.obj.set_linewidth(a.style.emphLineWidth)
            if (a.type=='polygon'):
                a.obj.set_facecolor(a.style.emphFaceColour)
                a.obj.set_edgecolor(a.style.emphEdgeColour)
        else:
            a.obj.set_color(a.style.stdColour)
            a.obj.set_linestyle(a.style.stdLineStyle)
            a.obj.set_linewidth(a.style.stdLineWidth)
            if (a.type=='polygon'):
                a.obj.set_facecolor(a.style.stdFaceColour)
                a.obj.set_edgecolor(a.style.stdEdgeColour)
            
        objects.append(a.obj)
    
    return objects

def performAnimation(animations, saveAsMP4=False, saveAsGIF=False, filename=''):
    
    # First set up the figure, the axis, and the plot element we want to animate
    #fig = plt.figure()
    #ax = plt.axes()
    #ax = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
    ax.axes.set_aspect('equal')
    plt.tight_layout()
    #plt.grid(b=True)
    #line, = ax.plot([], [])
    #ax.axes.get_xaxis().set_visible(False)
    #ax.axes.get_yaxis().set_visible(False)
    
    frames = animations[-1].i_max+1
    anim = animation.FuncAnimation(fig, animate, fargs = [animations], frames=frames, interval=200, blit=True, repeat=False)  
    
    #plt.axis('scaled')
    
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    if (saveAsMP4==True):
        anim.save(filename+'.mp4', extra_args=['-vcodec', 'libx264'])
        
    if (saveAsGIF==True):
        print('saveasgif')
        anim.save(filename+'.gif', writer='imagemagick', fps=60)
    
    
    plt.show()
    
    return anim
