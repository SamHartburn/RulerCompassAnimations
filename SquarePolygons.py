"""
SquarePolygons
Library to use RulerCompassAnimations to construct a square with the same area
as a given polygon.

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
import math


#Create a set of animations to show construction of a square with the same area
#as the rectangle defined by p1,p2,p3,p4.
#i_start is the frame the animation should start at
#Returns a list: first item is a list of the animations reqired
#second item is a list containing the four points of the square
def squareRectangle(p1,p2,p3,p4,i_start):
       
    #find out about the rectangle
    shortEdge = rc.distanceBetweenPoints(p3,p4)
    longEdge = rc.distanceBetweenPoints(p2,p3)
    #the code assumes that the short edge is between p3 and p4. If this isn't the case,
    #swap the points round so that it is
    if (shortEdge > longEdge):
        temp=p1
        p1=p4
        p4=p3
        p3=p2
        p2=temp
        shortEdge = rc.distanceBetweenPoints(p3,p4)
        longEdge = rc.distanceBetweenPoints(p2,p3)
        
    #find the side length of the square that will be created.
    squareEdge = math.sqrt(longEdge*shortEdge)
    #Find where the corners of the sqaure are, starting with the first corner at p3
    squareP1=p3
    squareP2=rc.extendLine(p4,p3,squareEdge)
    squareP4=rc.extendLine(p2,p3,squareEdge)  
    squareP3=rc.extendLineAngle(squareP2,squareEdge,rc.angleWithXAxis(squareP1,squareP4))
    
    #this helps us to know which way round the rectangle is, so that we draw arcs and lines in the right direction        
    a1=rc.anticlockwiseAngleThreePoints(p1,p2,p3)
    
    #draw an arc centred at the end of long edge, with radius of short edge
    if (a1<180):
        animations = rc.addStepArc(centre=p3, radius=shortEdge, rotation=rc.angleWithXAxis(p3,p4), theta1=0, 
                                 theta2=180, i_start=i_start)
    else:
        animations = rc.addStepArc(centre=p3, radius=shortEdge, rotation=rc.angleWithXAxis(p3,p4)+180, theta1=180, 
                                 theta2=0, i_start=i_start)
    
    #extend the long edge to meet the arc
    animations.append(rc.addStepLine(point1=p3, point2=rc.extendLine(p2,p3,squareEdge+1), i_start=animations[-1].i_max+1))
    
    stepsUsedAtEnd=[len(animations)-1]
    
    #find the intersection of the extended long edge and the arc
    intersection1=rc.extendLine(p2,p3,shortEdge)
    
    #this is the end of step 1
    step1EndIndex=len(animations)-1
    
    #draw perpendicular bisector and find the midpoint of new long edge
    new_long_edge = shortEdge+longEdge
    animations.extend(rc.perpendicularBisector(p2, intersection1, 0, animations[-1].i_max+1))
    mp = rc.midpoint(p2, intersection1)
    
    #this is the end of step 2
    step2EndFrame=animations[-1].i_max
    step2EndIndex=len(animations)
    
    #unemphasise step 1
    for i in range(0,step1EndIndex):
        animations[i].frameToUnemphasise=step2EndFrame
    
    #semicircle centred at midpoint, radius is half the new long edge
    if (a1<180):
        animations.extend(rc.addStepArc(centre=mp, radius=new_long_edge/2, rotation=rc.angleWithXAxis(p2,p3), theta1=0, 
                                 theta2=180, i_start=animations[-1].i_max+1))
    else:
        animations.extend(rc.addStepArc(centre=mp, radius=new_long_edge/2, rotation=rc.angleWithXAxis(p2,p3)+180, theta1=0, 
                                 theta2=180, i_start=animations[-1].i_max+1))
        
    #this is the end of step 3
    step3EndFrame=animations[-1].i_max
    step3EndIndex=len(animations)
    stepsUsedAtEnd.append(step3EndIndex)
    
    #unemphasise step 2
    for i in range(step1EndIndex, step2EndIndex):
        animations[i].frameToUnemphasise=step3EndFrame
    
    #extend the short edge to meet the semicircle (the length of this line is the length of the required square). The top of
    #the line is squareP2
    animations.append(rc.addStepLine(point1=p3, point2=rc.extendLine(p3,squareP2,squareEdge*0.1), i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-1)
    
    #diagonal from midpoint to second corner of square (not actually needed for the construction, but used to prove that the
    #side length is correct)
    #animations.append(rc.addStepLine(point1=mp, point2=rc.extendLine(mp,squareP2,squareEdge*0.1), i_start=animations[-1].i_max+1))
    
    #this is the end of step 4
    step4EndFrame=animations[-1].i_max
    step4EndIndex=len(animations)
    
    #unemphasise step 3
    for i in range(step2EndIndex, step3EndIndex):
        animations[i].frameToUnemphasise=step4EndFrame
    
    #now draw the final square
    #arc from corner of rectangle, with radius the length of the desired square. Arc needs to start at squareP2.
    if (a1<180):
        animations.extend(rc.addStepArc(centre=p3, radius=squareEdge, rotation=rc.angleWithXAxis(p2,p3), theta1=90, 
                                 theta2=0, i_start=animations[-1].i_max+1))
    else:
        animations.extend(rc.addStepArc(centre=p3, radius=squareEdge, rotation=rc.angleWithXAxis(p2,p3)+270, theta1=0, 
                                 theta2=90, i_start=animations[-1].i_max+1))
        
    #this is the end of step 5
    step5EndFrame=animations[-1].i_max
    step5EndIndex=len(animations)
    stepsUsedAtEnd.append(step5EndIndex-2)
    
    #unemphasise step 4
    for i in range(step3EndIndex, step4EndIndex):
        animations[i].frameToUnemphasise=step5EndFrame
         
    #construct the last vertex of the square by drawing arcs of radius squareEdge centred at the corners we already have   
    animations.extend(rc.addStepArc(centre=squareP2, radius=squareEdge, rotation=rc.angleWithXAxis(squareP2,squareP3)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    animations.extend(rc.addStepArc(centre=squareP4, radius=squareEdge, rotation=rc.angleWithXAxis(squareP4,squareP3)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    #this is the end of step 6
    step6EndFrame=animations[-1].i_max
    step6EndIndex=len(animations)
    
    #unemphasise step 5
    for i in range(step4EndIndex, step5EndIndex):
        animations[i].frameToUnemphasise=step6EndFrame
            
    #draw the last two sides of the square
    animations.append(rc.addStepLine(point1=squareP2, point2=squareP3, i_start=animations[-1].i_max+1))
    animations.append(rc.addStepLine(point1=squareP4, point2=squareP3, i_start=animations[-1].i_max+1))
    
    #this is the end of step 7
    step7EndFrame=animations[-1].i_max
    step7EndIndex=len(animations)
    
    #unemphasise step 6
    for i in range(step5EndIndex, step6EndIndex):
        animations[i].frameToUnemphasise=step7EndFrame
       
    #fill in the square
    animations.append(rc.addStepPolygon([squareP1,squareP2,squareP3,squareP4], (0.8,0.47,0.65,0.8), False, animations[-1].i_max+1,1))
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=(0.8,0.47,0.65,0.8)))
    
    #this is the end of step 8
    step8EndFrame=animations[-1].i_min
        
    #unemphasise step 7
    for i in range(step6EndIndex, step7EndIndex):
        animations[i].frameToUnemphasise=step8EndFrame
        
    #the long edge is used at the very end, so keep it emphasised until the square is drawn
    for i in stepsUsedAtEnd:
        animations[i].frameToUnemphasise=step8EndFrame
        
    #Hide all the constructions marks once the final square has been drawn
    lastFrame = animations[-1].i_max
    for a in animations:
        if (a.frameToHide==-1):
            a.frameToHide = lastFrame 
    
    return [animations, [squareP1,squareP2,squareP3,squareP4]]

#Create a set of animations to show construction of a square with the same area
#as the triangle defined by p1,p2,p3
#i_start is the frame the animation should start at
#Returns a list: first item is a list of the animations reqired
#second item is a list containing the four points of the square
def squareTriangle(p1,p2,p3, i_start):
    
    #Find height and base of desired rectangle
    height = rc.heightOfTriangle(p1,p2,p3)
    base = rc.distanceBetweenPoints(p1,p3)/2
    
    #treat p1 and p3 as the vertices of the base
    #midpoint will be one corner of rectangle
    mp = rc.midpoint(p1,p3)      
        
    #Use this angle to find out which side of the base to draw the rectangle - we want it on the same side as the top point
    a = rc.anticlockwiseAngleThreePoints(p2,mp,p1)
    
    #Find midpoint of first side and draw perpendicular bisector
    #Use a to find out which way to extend the bisector to ensure it is long enough
    #to make the side of the rectangle
    if (a<180):
        animations = rc.perpendicularBisector(p1,p3,height,i_start)
    else:
        animations = rc.perpendicularBisector(p3,p1,height,i_start)
    
    step1EndFrame=animations[-1].i_max
    step1EndIndex=len(animations)
    stepsUsedAtEnd=[step1EndIndex-1]
    for i in range(0,step1EndIndex):
        animations[i].frameToUnemphasise=step1EndFrame
        
    #draw line parallel to base through the top vertex
    animations.extend(rc.parallelLineThroughPoint(mp,p1,p2,animations[-1].i_max+1))
    
    step2EndIndex=len(animations)
    step2EndFrame=animations[-1].i_max
    stepsUsedAtEnd.append(step2EndIndex-1)
    for i in range(step1EndIndex, step2EndIndex):
        animations[i].frameToUnemphasise=step2EndFrame
           
    #find out where the third and fourth corners of the rectangle will be
    if (a<180):
        corner3 = rc.extendLineAngle(mp,height,rc.angleWithXAxis(mp,p1)-90)
        corner4 = rc.extendLineAngle(p1,height,rc.angleWithXAxis(mp,p1)-90)
    else:
        corner3 = rc.extendLineAngle(mp,height,rc.angleWithXAxis(mp,p1)+90)
        corner4 = rc.extendLineAngle(p1,height,rc.angleWithXAxis(mp,p1)+90)
       
    #draw perpendiculars to construct the third and fourth corners, and remaining sides
    animations.extend(rc.addStepArc(centre=corner3, radius=base, rotation=rc.angleWithXAxis(corner3,corner4)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    animations.extend(rc.addStepArc(centre=p1, radius=height, rotation=rc.angleWithXAxis(p1,corner4)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    
    step3EndIndex=len(animations)
    stepsUsedAtEnd.append(step3EndIndex-1)
    
    #draw the last two sides of the rectangle
    animations.append(rc.addStepLine(point1=corner3, point2=corner4, i_start=animations[-1].i_max+1))
    animations.append(rc.addStepLine(point1=p1, point2=corner4, i_start=animations[-1].i_max+1))
    
    step4EndIndex=len(animations)
    step4EndFrame=animations[-1].i_max
    stepsUsedAtEnd.append(step4EndIndex-1)
    for i in range(step2EndIndex, step3EndIndex):
        animations[i].frameToUnemphasise=step4EndFrame
        
    #show filled-in rectangle
    animations.append(rc.addStepPolygon([p1,mp,corner3,corner4], (0.94,0.89,0.26,0.8), False, animations[-1].i_max+1,1))
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=(0.94,0.89,0.26,0.8)))
    
    endFrame=animations[-1].i_min
    for i in range(step3EndIndex, step4EndIndex):
        animations[i].frameToUnemphasise=endFrame
    
    #the long edge is used at the very end, so keep it emphasised until the square is drawn
    for i in stepsUsedAtEnd:
        animations[i].frameToUnemphasise=endFrame
        
    #hide construction marks
    lastFrame = animations[-1].i_max+1
    for a in animations:
        if (a.frameToHide == -1):
            a.frameToHide = lastFrame
    
    
    #construct square with same area as rectangle
    #if (height>base):
        square=squareRectangle(p1,mp,corner3,corner4, animations[-1].i_max+1)
    #else:
        #square=squareRectangle(mp,corner3,corner4,basePoint, animations[-1].i_max+1)
    animations.extend(square[0])
        
    return [animations, square[1]]

#Create a set of animations to show construction of a square with the same area
#as the polygon defined by points
#Returns a list of the animations reqired
#second item is a list containing the four points of the square
def squarePolygon(*points, i_start):
    
    #draw diagonals from first vertex to other vertices
    animations=[rc.addStepLine(points[0], points[2], i_start)]
    maxX = points[0].x
    minY = points[0].y
    for i in range(3, len(points)):
        animations.append(rc.addStepLine(points[0], points[i], animations[-1].i_max+1))
    
    #the diagonals create triangles. Construct square with same area as each triangle
    lineTransforms = []       
    for i in range(2, len(points)):
        triangle = rc.addStepPolygon([points[0],points[i-1],points[i]], (0,0.45,0.7,1), False, animations[-1].i_max+1,1)
        triangle.setStyle(rc.Style(stdFaceColour=(0.84,0.37,0,1),stdLineStyle='-'))
        triangle.hide = True
        animations.append(triangle)
        triangleIndex=len(animations)-1
        square = squareTriangle(points[0], points[i-1], points[i], animations[-1].i_max+1)
        animations.extend(square[0])
        animations[triangleIndex].frameToHide=animations[-1].i_max
        #save details of the first line of the square just created
        lineTransforms.append(rc.LineTransform(square[1][0], square[1][1]))
        if (points[i].x > maxX):
            maxX = points[i].x
        if (points[i].y < minY):
            minY = points[i].y
        for i in range(1,3):
            if (square[1][i].x > maxX):
                maxX = square[1][i].x
    
    #now use the edges of the squares that we've saved, and Pythagoras' theorem, to calculate the length of the final square
    #Find where first two edges should move to, put them at right angles with each other
    initialPoint = rc.Point(maxX+1, minY)
    lineTransforms[0].setEndPoint(initialPoint,(-1*lineTransforms[0].angleWithX)%360)
    lineTransforms[1].setEndPoint(initialPoint,(90-lineTransforms[1].angleWithX)%360)        
    
    #find out where remaining edges should move to      
    for i in range(2, len(lineTransforms)):
        if (i%2 == 0):
            angleToRotate = rc.angleWithXAxis(lineTransforms[i-2].pos2End, lineTransforms[i-1].pos2End) - 90 - lineTransforms[i].angleWithX
        else:
            angleToRotate = 90 + rc.angleWithXAxis(lineTransforms[i-2].pos2End, lineTransforms[i-1].pos2End) - lineTransforms[i].angleWithX
        lineTransforms[i].setEndPoint(lineTransforms[i-2].pos2End, angleToRotate%360)
    
    #add the animation for moving the first edge            
    animations.append(rc.addStepLineTransform(lineTransforms[0], animations[-1].i_max+1))
    
    #for each subsequent edge, move it to the previous edge and join the ends
    #each one will be at right angles to the joining line from the previous step
    for i in range(1, len(lineTransforms)):
        animations.append(rc.addStepLineTransform(lineTransforms[i], animations[-1].i_max+1))
        animations.append(rc.addStepLine(lineTransforms[i-1].pos2End, lineTransforms[i].pos2End, animations[-1].i_max+1))
        animations[-2].frameToUnemphasise=animations[-1].i_max
        animations[-3].frameToUnemphasise=animations[-1].i_max
    
    #We don't want to unemphasise the final line until the end
    step1EndIndex=len(animations)
    stepsUsedAtEnd=[len(animations)-1]
          
    #find the vertices of the final square
    finalSquareP1 = lineTransforms[-2].pos2End
    finalSquareP2 = lineTransforms[-1].pos2End
    finalSquareLength = rc.distanceBetweenPoints(finalSquareP1, finalSquareP2)
    if (len(points)%2==0):
        finalSquareAngle = rc.angleWithXAxis(finalSquareP2, finalSquareP1)
    else:
        finalSquareAngle = rc.angleWithXAxis(finalSquareP1, finalSquareP2)
    finalSquareP3 = rc.extendLineAngle(finalSquareP2, finalSquareLength, finalSquareAngle+90)
    finalSquareP4 = rc.extendLineAngle(finalSquareP1, finalSquareLength, finalSquareAngle+90)
    
    #construct the final square
    animations.extend(rc.perpendicularThroughPointOnLine(finalSquareP1, finalSquareP2, finalSquareP2, animations[-1].i_max+1))
    
    step2EndFrame=animations[-1].i_max
    step2EndIndex=len(animations)
    stepsUsedAtEnd.append(step2EndIndex-1)
    for i in range(step1EndIndex, step2EndIndex):
        animations[i].frameToUnemphasise=step2EndFrame
    
    #arc from corner of square, with radius the length of the desired square
    a1=rc.anticlockwiseAngleThreePoints(finalSquareP1,finalSquareP2,finalSquareP3)
    if (a1<180):
        animations.extend(rc.addStepArc(centre=finalSquareP2, radius=finalSquareLength, rotation=rc.angleWithXAxis(finalSquareP2,finalSquareP1), theta1=0, 
                                 theta2=90, i_start=animations[-1].i_max+1))
    else:
        animations.extend(rc.addStepArc(centre=finalSquareP2, radius=finalSquareLength, rotation=rc.angleWithXAxis(finalSquareP2,finalSquareP1)+270, theta1=90, 
                                 theta2=0, i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-2)
        
    #construct the last vertex of the square by drawing arcs of radius squareEdge centred at the corners we already have   
    animations.extend(rc.addStepArc(centre=finalSquareP3, radius=finalSquareLength, rotation=rc.angleWithXAxis(finalSquareP3,finalSquareP4)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-2)
    animations.extend(rc.addStepArc(centre=finalSquareP1, radius=finalSquareLength, rotation=rc.angleWithXAxis(finalSquareP1,finalSquareP4)+350, theta1=0, 
                                 theta2=20, i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-2)
         
    #draw the last two sides of the square
    animations.append(rc.addStepLine(point1=finalSquareP3, point2=finalSquareP4, i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-1)
    animations.append(rc.addStepLine(point1=finalSquareP1, point2=finalSquareP4, i_start=animations[-1].i_max+1))
    stepsUsedAtEnd.append(len(animations)-1)
   
    #Fill in the square
    animations.append(rc.addStepPolygon([finalSquareP1,finalSquareP2,finalSquareP3,finalSquareP4], (0,0.45,0.7,1), False, animations[-1].i_max+1,1))
    animations[-1].setStyle(rc.Style(stdLineStyle='-',stdFaceColour=(0,0.45,0.7,1)))
    
    endFrame=animations[-1].i_min
    for i in stepsUsedAtEnd:
        animations[i].frameToUnemphasise=endFrame
        
    #Hide construction marks once the square has been shown
    lastFrame = animations[-1].i_max
    for a in animations:
        if (a.frameToHide==-1):
            a.frameToHide = lastFrame 
      
    return [animations, [finalSquareP1,finalSquareP2,finalSquareP3,finalSquareP4]]
