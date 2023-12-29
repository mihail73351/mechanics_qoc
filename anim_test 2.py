import numpy as np
import pickle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

import LinearPDESolvers as linPDEs


import time
#solve wave eq

T=40
xLeft=-0
xRight=2
c=1

#Nx = 510
#Nt = 1000
Nx=50
Nt=5000
hx = (xRight-xLeft)/Nx
ht = T/Nt


solver = linPDEs.ExplicitEulerSolver(np.array([ht,hx]), cCoef=c)


xs = np.arange(xLeft,xRight+hx/2,hx)
ts = np.arange(0,T+ht/2,ht)

#assume u'(0,x)=0
def initFunc(xx):
    return ((2*xx)*(xx<0.5) + (xx>=0.5)*(-2/3*xx + 4/3))
def dtFunc(xx):
    return 0
uInits = np.zeros([2,len(xs)])
uInits[0,:] = initFunc(xs)
duts = dtFunc(xs)
uInits[1,:] = uInits[0,:] + duts*ht

#SOLVE!
res=solver.solveBVProblem1D(uInits, Nt)


# initializing a figure in 
# which the graph will be plotted
fig = plt.figure() 
   
# marking the x-axis and y-axis
axis = plt.axes(xlim =(xLeft, xRight), 
                ylim =(-1.5, 1.5)) 
  
# initializing a line variable
line, = axis.plot([], [], lw = 3) 

cross = axis.scatter([xLeft,xRight],[0,0], marker="x", s=90, color="red")

txt = axis.text(xLeft+1e-1,-1,"t="+str(ht*0))
# data which the line will 
# contain (x, y)
def init(): 
    line.set_data(xs, res[0,:])
    txt.set_text("t="+str(ht*0))
    return line,txt,
   
def animate(i):
    line.set_data(xs, res[i,:])
    txt.set_text("t={:.2f}".format(ht*i) )
    return line,txt,
   
anim = FuncAnimation(fig, animate, init_func = init,
                     frames = np.arange(0,res.shape[0],1), interval = ht*1000, blit = False, repeat=False)#ms scale

# anim.save('explEuler.mp4',fps=30)

# with open("./solveTempOut.pkl", "wb") as f:
#     pickle.dump({"res": res},f)

plt.show()