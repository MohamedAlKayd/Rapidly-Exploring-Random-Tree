# Rapidly-Exploring Random Tree Program

# Libraries: 6 libraries used

# Library 1: random library used to generate random numbers
import random

# Library 2: drawSample python file used to draw elastic shapes on a canvas
import drawSample

# Library 3: sys library to have acces to python runtime enviroment
import sys

# Library 4: imagetoRects python file to binarize the image of the world given
import imageToRects

# Library 5: utils python file used to retrieve arguements from the command line
import utils

# Library 6: numpy library for arrays and matrices
import numpy
numpy.random.BitGenerator = numpy.random.bit_generator.BitGenerator

# Functions: 15 functions used

# Function 1 ~ Draw a new canvas with the graph
def redraw(canvas):
    
    # Clear the canvas
    canvas.clear()
    
    # Mark the canvas with the target position coordinates and the small step value
    canvas.markit(targetXPosition,targetYPosition,r=SMALLSTEP)
    
    # Draw the graph
    drawGraph(Graph,canvas)
    
    # Iterate over the obstacles and outline and fill them
    for o in obstacles: canvas.showRect(o, outline='blue', fill='blue')
    
    # Delete
    canvas.delete("debug")

# Function 2 ~ Draws the graph
def drawGraph(Graph, canvas):
    
    # Global variables to hold the vertices,nodes,edges
    global vertices,nodes,edges
    
    # If not true
    if not visualize: return
    
    # Iterate over the edges
    for edge in Graph[edges]:

        # Parent node in the current edge
        parent=edge[0]

        # Child node in the current edge
        child=edge[1]
        
        # Draw a line between the vertices ~ e.g. vertices: [[10, 270], [10, 280]]
        canvas.polyline([vertices[parent],vertices[child]])

# Function 3 ~ Use this function to generate points randomly for the RRT algo
def genPoint():

    # Variable to check if point generated
    bad = 1
    
    # If uniform, only once
    while bad:
        
        # Generate only 1 point per function call
        bad = 0
        
        # Use the Rapidly-Exploring Random Tree Sampling Policy ~ Uniform distribution
        if args.rrt_sampling_policy == "uniform":
            
            # Set the x value
            x = random.random()*XMAX
            
            # Set the y value
            y = random.random()*YMAX
        
        # Use the Rapidly-Exploring Random Tree Sampling Policy ~ Gaussian distribution
        elif args.rrt_sampling_policy == "gaussian":
            
            # Set the x value
            x = random.gauss(targetXPosition,sigmax_for_randgen)
            
            # Set the y value
            y = random.gauss(targetYPosition,sigmay_for_randgen)
        
        # Other cases
        else:
            
            # Not implemented yet
            print ("Not yet implemented")
            
            # Exit the program
            quit(1)
        
        # less than x range check for gaussian        
        if x<0: bad = 1
        
        # less than y range check for gaussian        
        if y<0: bad = 1
        
        # greater than x range check for gaussian        
        if x>XMAX: bad = 1
        
        # greater than y range check for gaussian        
        if y>YMAX: bad = 1
    
    # Return the generated point
    return [x,y]

# Function 4 ~ Returns the parent node for node k
def returnParent(k,canvas):

    # Iterate over the edges in the graph
    for edge in Graph[edges]:
        
        # Parent node in the current edge
        parent = edge[0]

        # Child node in the current edge
        child = edge[1]

        # If the edge is equal to the current vertex
        if child == k:

            # Draw a line from the Parent node to the vertex
            canvas.polyline([vertices[edge[0]],vertices[k]],style=3)
            
            # Return the parent node
            return parent

# Function 5 ~ Generate a vertex
def genvertex():
    
    # Generate a point and add it the list of vertices
    vertices.append(genPoint())
    
    # Return the current length of the list of vertices
    return len(vertices)-1

# Function 6 ~ Adds the point to the list of vertices
def pointToVertex(p):

    # Add the current point to the vertices list
    vertices.append(list(p))

    # Return the current length of the list of vertices
    return len(vertices)-1

# Function 7 ~ Choose random vertex
def pickvertex():
    
    # Returns a random vertex
    return random.choice(range(len(vertices)))

# Function 8
def lineFromPoints(p1,p2):
    
    #TODO
    return None

# Function 9 ~ Computes Euclidean distance between 2 points
def pointPointDistance(point1,point2):
    
    # Get the difference between the two points ~ (x,y)
    result = numpy.array(point1)-numpy.array(point2)
    
    # Get the distance between the two points
    distance = numpy.linalg.norm(result)
    
    # Return the distance
    return distance

# Function 10 ~ Finds the closest existing point to the generated point in the graph
def closestPointToPoint(Graph,generatedPoint):

    # Variable to store the index of the current closest point
    currentClosestPoint = sys.maxsize * 2 + 1
    
    # Variable to hold the index of the closest point in the Graph edges list
    currentVertexIndex = 0
    
    # Counter to hold the current vertex index
    vertexIndexCounter=0
    
    # Iterate over all the edges
    for vertex in vertices:
        
        # Variable to store the distance between the current edge being checked and the generated point
        currentDistance = pointPointDistance(vertex,generatedPoint)
        
        # If the current distance is less that what was previously calculated
        if currentDistance<currentClosestPoint:
            
            # Set the current closest point variable to the new closest value
            currentClosestPoint=currentDistance
            
            # Set the current vertex variable the index of the new closest value
            currentVertexIndex=vertexIndexCounter
        
        # Increment the vertex index counter
        vertexIndexCounter+=1
    
    # Return the index of that point
    return currentVertexIndex

# Function 11 ~ Checks if the line will hit an obstacle
def lineHitsRect(p1,p2,r):

    # Left top x coordinate
    leftBottomx=r[0]
    
    # Left top y coordinate
    leftBottomy=r[1]
    
    # Right bottom x coordinate
    rightTopx=r[2]
    
    # Right bottom y coordinate
    rightTopy=r[3]

    # If the line is in the obstacle
    if leftBottomx<p1[0]<rightTopx and leftBottomy<p1[1]<rightTopy:
        
        # Return true to indicate that the line hits the obstacle
        return True
    
    # If it is not in the the obstacle
    else:
        # Return false to indicate that the line doesn't hit the obstacle
        return False

# Function 12 ~ Return 1 in p is inside rect, dilated by dilation (for edge cases).
def inRect(p,rect,dilation):
     # Left top x coordinate
    leftBottomx=rect[0]
    
    # Left top y coordinate
    leftBottomy=rect[1]
    
    # Right bottom x coordinate
    rightTopx=rect[2]
    
    # Right bottom y coordinate
    rightTopy=rect[3]

    # If the line is in the obstacle
    if leftBottomx-dilation<p[0]<rightTopx+dilation and leftBottomy-dilation<p[1]<rightTopy+dilation:
        
        # Return true to indicate that the line hits the obstacle
        return True
    
    # If it is not in the the obstacle
    else:
        # Return false to indicate that the line doesn't hit the obstacle
        return False

# Function 13 ~ Creates a new point
def addNewPoint(nearestPoint,randomGuidingPoint,stepsize):

    # Creates an Array of the guiding point - the nearest point (x,y)
    random_NearestPoint = numpy.array(randomGuidingPoint)-numpy.array(nearestPoint)

    # Measures the size of the vector array
    length = numpy.linalg.norm(random_NearestPoint)

    # Divides all the elements of the array by the length and multiples by the minimum between the step size and the length
    random_NearestPoint=(random_NearestPoint/length) * min(stepsize,length)
    
    # New point = nearest point + random_point
    newVertex = (nearestPoint[0]+random_NearestPoint[0],nearestPoint[1]+random_NearestPoint[1])
    
    # Return the new point
    return newVertex

# Function 14 ~ Graph, targetXPosition, targetYPosition, canvas.
def rrt_search(Graph,targetXPosition,targetYPosition,canvas):

    # Global variables
    global sigmax_for_randgen, sigmay_for_randgen
    
    # Counter used check when to update the canvas
    n=0
    
    # Number of steps taken to reach target
    nsteps=0
    
    # Loop until forced to break
    while 1:
        
        # This generates a point in form of [x,y] from either the normal dist or the Gaussian dist
        guidingPoint=genPoint()
        
        # Find the closest point in the existing graph to the guiding point ~ index value
        closestPointOnGraph=closestPointToPoint(Graph,guidingPoint)

        # Returns the new point ~ (x,y)
        newPoint=addNewPoint(vertices[closestPointOnGraph],guidingPoint,SMALLSTEP)   

        # True
        if visualize:

            # Increment the counter
            n=n+1
            
            # Count to 10
            if n>10:
                
                # Update the canvas
                canvas.events()
                
                # Set the counter back to 0
                n=0
        
        # Variable to hold whether new point is inside obstacle or not
        boolean = 0
        
        # Iterate over either the 43 obstacles in shot or the 6 obstacles in simple
        for obstacle in obstacles:
            
            # If the line has hit a rectangle or guiding point is in obstacle
            if lineHitsRect(newPoint,guidingPoint,obstacle) or inRect(guidingPoint,obstacle,SMALLSTEP):
                
                # Change the variable
                boolean+=1
                
                # Break out of the for loop
                break

        # If no obstacles have been hit
        if boolean==0:
            
            # Add the point p to the list of vertices ~ K is the length of the vertices ~ new vertex ID
            k = pointToVertex(newPoint)
            
            # Add the node to the graph nodes
            Graph[nodes].append(k)
            
            # Add the edge connecting the point to the current vertex to the graph edges
            Graph[edges].append((closestPointOnGraph,k))
            
            # If true
            if visualize:
                
                # Draw a line between that point and the current vertex
                canvas.polyline([vertices[closestPointOnGraph],vertices[k]])
            
            # If the difference between the point and the target is less than the small step
            if pointPointDistance(vertices[k],[targetXPosition,targetYPosition]) < SMALLSTEP:

                # Print the number of steps needed to reach target goal and the number of nodes in the tree
                print ("Target achieved.", len(vertices), "nodes in entire tree")
                
                # If true
                if visualize:
                    
                    # Set t to the length of the vertices ~ new vertex ID
                    t = pointToVertex([targetXPosition,targetYPosition])
                    
                    # Add the edge from the current vertex to t to the graph edges
                    Graph[edges].append((k,t))
                    
                    # If true
                    if visualize:
                        
                        # Draw a GREEN (1) line from the generated point to the vertex point
                        canvas.polyline([vertices[k],vertices[t]],1)

                    # Set the number of steps back to 0
                    nsteps = 0
                    
                    # Set the total distance to 0
                    totaldist = 0
                    
                    # While true
                    while 1:
                        
                        # Old point ~ remember point to compute distance
                        oldp = vertices[k]
                        
                        # Go back to parent ~ follow links back to root.
                        k = returnParent(k,canvas)
                        
                        # Update the canvas
                        canvas.events()
                        
                        # Once at parent ~ have we arrived?
                        if k <= 1: break
                        
                        # Count the number of steps from destination to parent
                        nsteps = nsteps + 1
                        
                        # Set the total distance to the distance from the parent to the  ~ sum lengths
                        totaldist = totaldist + pointPointDistance(vertices[k],oldp)
                    
                    # Print the total path length and the number of nodes taken
                    print ("Path length", totaldist, "using", nsteps, "nodes.")
                    
                    # Global variable
                    global prompt_before_next
                    
                    # If true
                    if prompt_before_next:
                        
                        # Update the canvas
                        canvas.events()
                        
                        # Print the list of possible options at this point
                        print ("More [c,q,g,Y]>")
                        
                        # Read the option chossen from the command line
                        d = sys.stdin.readline().strip().lstrip()
                        
                        # Print the option chosen
                        print ("[" + d + "]")
                        
                        # c --> deletes the canvas --> turns it to red
                        if d == "c": canvas.delete()
                        
                        # q --> quits 
                        if d == "q": return
                        
                        # g --> generate --> run for ever
                        if d == "g": prompt_before_next = 0
                    
                    # break out of the main while loop
                    break

# Function 15 ~ Main function
def main():

    #seed
    random.seed(args.seed)
    
    # If true
    if visualize:
        
        # Set up a canvas #, rescale=800/1800.)
        canvas = drawSample.SelectRect(xmin=0,ymin=0,xmax=XMAX,ymax=YMAX,nrects=0,keepcontrol=0)
        
        # Make the obstables blue and their boundries red
        for o in obstacles: canvas.showRect(o,outline='red',fill='blue')
    
    # While true
    while 1:
        
        # graph G
        redraw(canvas)
        
        # Add the starting edge to the graph
        Graph[edges].append((0,1))
        
        # Add the starting node to the graph
        Graph[nodes].append(1)
        
        # If true
        if visualize: canvas.markit(targetXPosition,targetYPosition,r=SMALLSTEP )
        
        # Draw the graph with the canvas
        drawGraph(Graph,canvas)
        
        # Call the Rapidly-Exploring Random Tree Algorithm with the graph, target position, and canvas
        rrt_search(Graph,targetXPosition,targetYPosition,canvas)
    
    # If true
    if visualize:
        
        # Infinite loop
        canvas.mainloop()

# Run if program is the main program executed
if __name__ == '__main__':
    
    # Get the arguements from the command line
    args=utils.get_args()
    
    # True
    visualize=utils.get_args()
    
    # 10 is good for normal real-time drawing
    drawInterval=10
    
    # Parameter to ask before re-running an rrt search # ask before re-running sonce solved
    prompt_before_next=1
    
    # Variable to hold local planner steps # what our "local planner" can handle.
    SMALLSTEP=args.step_size
    
    # Get the size and obstacles from the image # Note the obstacles are the two corner points of a rectangle (left-top,right-bottom) ~ Each obstacle is (x1,y1),(x2,y2), making for 4 points
    map_size,obstacles=imageToRects.imageToRects(args.world)
    
    # Variables to define the canvas size ~ The boundaries of the world are (0,0) and (XMAX,YMAX)
    XMAX=map_size[0]
    YMAX=map_size[1]
    
    # Graph = List of [Node,Edges]  # nodes, edges
    Graph=[[0],[]]
    
    # List that contains the [x,y] values for all the vertices
    vertices=[[args.start_pos_x,args.start_pos_y],[args.start_pos_x,args.start_pos_y+10]]
    
    # goal/target
    targetXPosition=args.target_pos_x
    targetYPosition=args.target_pos_y
    
    # start
    sigmax_for_randgen=XMAX/2.0
    sigmay_for_randgen=YMAX/2.0
    
    # Graph[[nodes],[edges]]
    nodes=0
    edges=1
    
    # Call the Main Function
    main()