from numpy import sin, cos, sqrt, exp, pi
from scipy.special import erfi
import numpy as np
import plt2latex

def f(t, x, m, w):
	omega = sqrt((-1*beta+pi**2*rho*T*m**2/l/l)/rho/rho)
	value = (12*exp(-1*beta*t/rho) * l**4 *
		(4 - 4*(-1)**m + (-1)**m * pi ** 2*m**2) *
		sin(pi*x*m/l)*
		(2*beta*exp(beta*t/rho)*l**4*rho*w*cos(w*t)*omega-
			2*beta*l**4*rho*w*cos(t*omega)*omega+
			l**2*(exp(beta*t/rho)*rho*(l**2*rho*w**2-pi**2*T*m**2)*omega
				*sin(w*t) +
				w*(-2*beta**2*l**2 - rho*(l**2*rho*w**2-pi**2*T*m**2)) *
				sin(t*omega)
			)
		)	
	)/(
		pi**5*rho*m**5*omega*(4*beta**2*l**4*w**2 +
			(l**2*rho*w**2 - pi**2*T*m**2)**2)
	)
	return value


#def f(t, x, m, w):
#	omega = sqrt((-1*beta+pi**2*rho*T*m**2/l/l)/rho/rho)
#	value = (np.exp(-beta*t/rho-(np.pi*m*(2j*l*w+a*a*np.pi*m))/(2*l*l))*
#		((np.exp(2*1j*np.pi* w*m/l)*
#			(erfi(1j*l*(l-w)+a*a*np.pi*m/(np.sqrt(2)*a*l))-
#			erfi(-1j*l*w+a*a*np.pi*m/(np.sqrt(2)*a*l)))-
#		erfi(1j*l*w+a*a*np.pi*m/(np.sqrt(2)*a*l))+
#		erfi(1j*l*(-l+w)+a*a*np.pi*m/(np.sqrt(2)*a*l)))*sin(pi*m*x/l)*
#		(2*beta*exp(beta*t/rho)*l**4*rho*w*cos(w*t)*omega-
#		2*beta*l**4*rho*w*cos(t*omega)*omega+
#		l**2*(exp(beta*t/rho)*rho*(l**2*rho*w**2-pi**2*T*m**2)*omega
#		*sin(w*t) +
#		w*(-2*beta**2*l**2 - rho*(l**2*rho*w**2-pi**2*T*m**2)) *
#		sin(t*omega)))
#		)) / (
#			(2*l*rho*omega)*(4*beta**2*l**4*w**2+(l**2*rho*w**2-pi**2*T*m**2)**2)
#		)
#	return(value)
	
	
l = 1
rho = 0.01
beta = 0.01
T = 10
#a = 0.2

def rope(t, x, w):
	value = 0
	for i in range(1, 100):
		value += f(t, x, i, w)
		return value
	

from matplotlib import pyplot as plt
x = np.linspace(0, 1, 10)
t = np.linspace(1, 50, 1000)
w = np.linspace(20, 500, 100)




def maxim(w):
	data = []
	for ww in w:
		print(str(int(ww/max(w)*100))  +  "%")
		value = 0
		for tt in t:
			for xx in x:
				temp = rope(tt, xx, ww)
				if temp > value:
					value = temp
		data.append(value)
	return data

				
			
			
	

plt.plot(w, maxim(w))
plt.show()





import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

plt.rcParams["figure.figsize"] = [4, 2]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
ax = plt.axes(xlim=(0, 1), ylim=(-0.1, 0.1))
line, = ax.plot([], [], lw=2)
time_text = ax.text(0.05, 0.9, '')

def init():
	line.set_data([], [])
#	time_text = ax.text(0.05, 0.9, '')
	return line,

def animate(i):
	x = np.linspace(0, 1, 100)
	w = 90 + i/100
	y = rope(i/250, x, w)
	line.set_data(x, y)
	print(i/100+90)
#	time_text.set_text(str(w))
	return line, time_text

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=2000, interval=20, blit=True)
plt.show()