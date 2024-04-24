import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parametere
alpha = 0.1  # Thermal diffusivity
dx = dy = 0.1  # Spatial step size
dt = 0.01  # Time step size
nx, ny = 100, 100  # Number of grid points in x and y

# Stabilitetssjekk i forhold til FTCS metoden
if alpha * dt / (dx * dx) >= 0.25 or alpha * dt / (dy * dy) >= 0.25:
    raise ValueError("The simulation may be unstable. Adjust dt, dx, or dy.")

# Initialbetingelser: u(x, y, 0) er 0 overalt med et opphetet punkt i sentrum
u = np.zeros((nx, ny))
u[nx//2 - 5:nx//2 + 5, ny//2 - 5:ny//2 + 5] = 100  # Opphetet punkt

def update(u):
    
    u_new = u.copy()
    for i in range(1, nx-1):
        for j in range(1, ny-1):
            u_new[i, j] = (u[i, j] + alpha * dt / dx**2 * (u[i+1, j] + u[i-1, j] - 2 * u[i, j]) +
                           alpha * dt / dy**2 * (u[i, j+1] + u[i, j-1] - 2 * u[i, j]))
    return u_new

# Litt animasjon for å gjøre det gøy
fig, ax = plt.subplots()
img = ax.imshow(u, cmap='hot', interpolation='nearest', vmin=0, vmax=100)
plt.colorbar(img)

def animate(frame):
    global u
    u = update(u)
    img.set_data(u)
    return [img]

ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)
plt.show()
