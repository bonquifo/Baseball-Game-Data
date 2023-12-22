import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import math
from mpl_toolkits import mplot3d

pd.options.display.max_rows = 999

df = pd.read_csv('20220423-Olsen-1.csv')



axisCoords = df.loc[:,["Pitcher", "x0", "y0", "z0"]]
        
x0 = axisCoords['x0']
y0 = axisCoords['y0']
z0 = axisCoords['z0']
#Average of initial position coordinates
xInitialAvg = (sum(x0)/len(x0))
yInitialAvg = (sum(y0)/len(y0))
zInitialAvg = (sum(z0)/len(z0))
        
#Average of initial velocity coordinates
        
axisCoordsV = df.loc[:,["Pitcher", "vx0", "vy0", "vz0"]]

vx0 = axisCoordsV['vx0']
vy0 = axisCoordsV['vy0']
vz0 = axisCoordsV['vz0']

vxInit = (sum(vx0)/len(vx0))
vyInit = (sum(vy0)/len(vy0))
vzInit = (sum(vz0)/len(vz0))

        #Average of initial acceleration coordinates

        
axisCoordsA = df.loc[:,["Pitcher", "ax0", "ay0", "az0"]]

ax0 = axisCoordsA['ax0']
ay0 = axisCoordsA['ay0']
az0 = axisCoordsA['az0']

axInit = (sum(ax0)/len(ax0))
ayInit = (sum(ay0)/len(ay0))
azInit = (sum(az0)/len(az0))

positionResultant = np.linalg.norm([x0,y0,z0])
velocityResultant = np.linalg.norm([vx0,vy0,vz0])
accelerationResultant = np.linalg.norm([ax0,ay0,az0])




def avgSpeed():
    x = df.loc[:,['Pitcher', 'RelSpeed']]
    y = x['RelSpeed'].mean()
    x['RelSpeed'].fillna(y, inplace=True)
    print(y)

class BaseballTrajectory:
    def __init__(self, initial_position, initial_velocity, acceleration):
        self.position = np.array(initial_position, dtype=np.float64)
        self.velocity = np.array(initial_velocity, dtype=np.float64)
        self.acceleration = np.array(acceleration, dtype=np.float64)

    def update_position(self, time_step):
        self.velocity += self.acceleration * time_step
        self.position += self.velocity * time_step

# Set up the baseball trajectory
initial_position = [x0, y0, z0]
initial_velocity = [vx0, vy0, vz0]
acceleration = [ax0, ay0, az0]  # Assuming gravity in the negative y-direction

baseball_trajectory = BaseballTrajectory(initial_position, initial_velocity, acceleration)

# Simulate the trajectory for a certain duration
num_steps = 100
time_step = 0.1
positions = []

for _ in range(num_steps):
    positions.append(baseball_trajectory.position.copy())
    baseball_trajectory.update_position(time_step)

# Convert positions to a NumPy array
positions = np.array(positions)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label='Baseball Trajectory')

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.legend()
plt.show()