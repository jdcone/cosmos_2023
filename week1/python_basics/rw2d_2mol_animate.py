#
#  Program simulates two molecules attempting to find each other
#  inside a 2D elliptical cell by conducting random walks from 
#  different start locations. 
#  Program uses matplotlib animation function to animate the 
#  movement of each molecule.
#
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Ellipse  # Used to draw ellipse
random.seed(None)        # Seed generator, None => system clock

def rand_angle():
    """  
    Performs unit 2D random step at random angle ( 0 to 2*PI)
    Returns (x,y) co-ordinates of unit step at random angle
     """
    step_factor = .1
    angle = random.uniform(0,2*np.pi)
    xdelta = np.sin(angle)* step_factor
    ydelta = np.cos(angle)* step_factor
    return xdelta, ydelta


def check_inside_ellipse(xvalue, yvalue, ellipse):
    """  
    Checks if point is inside a ellipse. Returns True if inside.
    False if not      
    """ 
    center, height, width = ellipse
    x0,y0 = center
    a = width/2
    b = height/2
    if ((xvalue-x0)/a)**2 + ((yvalue-y0)/b)**2 < 1:
        return True
    else:
        return False

def move_molecule(x, y, ellipse):
    """
    Moves molecule one step inside cell boundary
    """
    valid_move = False
    while not valid_move: # Continue loop until move is valid
        xdelta, ydelta = rand_angle()
        xtry = x + xdelta
        ytry = y + ydelta
    #  Check if trial inside boundary
        if  check_inside_ellipse(xtry, ytry, ellipse):
            x_new,y_new = xtry,ytry
            valid_move = True 
    return  (x_new,y_new)       

def draw_ellipse(ax):
    """  
    Draws boundary of cell as 2D ellipse onto graph object(ax)
    """
    center, height, width = ellipse
    ax.add_patch(Ellipse(xy=center, width=width, height=height, angle = 180, fill=False, edgecolor='k',lw=4))
    return

def init():
    """ Functions initializes animation lists """
    molecule1.set_data([], [])
    molecule2.set_data([], []) 
    return molecule1,molecule2,    

def random_move(i):
    """ Function moves each molecule and updates animation frame """
    # Get next move for both molecules 
    x1 = x1walk[-1]
    y1 = y1walk[-1]
    x2 = x2walk[-1]
    y2 = y2walk[-1]
    x1,y1 = move_molecule(x1,y1, ellipse)
    x2,y2 = move_molecule(x2,y2, ellipse) 
    x1walk.append(x1)
    y1walk.append(y1)        
    x2walk.append(x2)
    y2walk.append(y2)
    # Update animation walk data (x1walk,x2walk)   
    molecule1.set_data(x1walk[:i], y1walk[:i])
    molecule2.set_data(x2walk[:i], y2walk[:i])
    #  Check if molecules are close. If so, mark spot, 
    #  end animation, and return
    if (x1-x2)**2 + (y1-y2)**2 <= .2:
        mol_got_close = True
        ax.plot(x1walk[-1],y1walk[-1], 'g*', ms=30)  # Large * to mark end of walk
        ax.text(0.1, 0.9,'# of steps =' + str(i), ha='center', va='center',fontsize=20, transform=ax.transAxes)
        animate.event_source.stop()  # This statement stops the animation
#  
#  Set up confining ellipse and starting points for each molecule, 
# 
height = 2.0
width = 8.0     
ellipse = ( (0.0,0.0), height, width)
start_loc1   = (-width/2 +2.0,0.0)
start_loc2   = ( width/2 -2.0,0.0)
x1walk = [ start_loc1[0]]
y1walk = [ start_loc1[1]]
x2walk = [ start_loc2[0]]
y2walk = [ start_loc2[1]]

# Set up canvas to conduct animation
fig, ax = plt.subplots()
ax.set_ylim([-height/2 -.2,height/2 + .2])
ax.set_xlim([-width/2 -.2,width/2+.2])
draw_ellipse(ax)
ax.set_title('Two molecules trying to find each other in a cell',size= 16)
ax.plot(start_loc1[0], start_loc1[1], 'k*', ms=16)  # Large * to mark start of mol1
ax.plot(start_loc2[0], start_loc2[1], 'k*', ms=16)  # Large * to mark start of mol2
# These are graph variables updated at each animation step
molecule1, =  ax.plot([], [], color="blue", lw=2, label = 'molecule 1')
molecule2, =  ax.plot([], [], color="red", lw=2, label = 'molecule 2')
ax.legend(loc="upper right")
ax.grid(True)

#  This function conducts animation, interval = delay in frames in msec 
animate = animation.FuncAnimation(fig = fig, func = random_move, init_func= init, blit=False, interval = 1)
plt.show()
