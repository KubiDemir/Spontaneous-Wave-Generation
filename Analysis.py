# %% import packages

# maths
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# GIF packages
import os
import imageio
import shutil

# %% read data
data = xr.open_dataset("TankDimensionPablo.cdf")
temp = data["temp"] # temperature(t,z,y,x)

# %% Compute Rossy Radius from Stratification

# FORMULAS
# N = +- sqrt( - g/rho_0 * drho/dz)
# R = N_0 H_0 / |f|

temp_z0 = temp[50,0,:,:] # temperature at top
temp_z1 = temp[50,-1,:,:] # temperature at bottom
dtemp = np.mean(np.mean(temp_z0 - temp_z1,axis=1)).values # average temperature difference from top to bottom
dH = 0.07 # tank depth
dTdz = dtemp/dH # temperature gradient

drhodT = 4e-4 # alpha: thermal expansion
drhodz = drhodT * dTdz # density stratification

g = 9.81 # gravity constant
rho_0 = 1e+3 # reference density
N2 = - g/rho_0 * drhodz 
N = np.sqrt(N2) # buoyancy frequency

f = 0.5 # inertial frequency
R = N * dH / abs(f) # Barotropic Rossby Radius


# %% create directory for images
dirName = 'img'
if  not os.path.exists(dirName) :
    os.makedirs(dirName)
else :
    shutil.rmtree(dirName)
    os.makedirs(dirName)
    
dirGIF = 'GIF'
if  not os.path.exists(dirGIF) :
    os.makedirs(dirGIF)
else :
    shutil.rmtree(dirGIF)
    os.makedirs(dirGIF)

# %% Space dimensions
x = np.arange(200)*0.01
y = np.arange(35)*0.01
z = np.arange(6)*0.01

# %% Plot T(x,y) at z = 3cm
    
plt.figure()
for t in range(100):
    print("Time Step " + str(t+1) + "/100")
    file_name = "Txy" + str(t+1).zfill(3) + ".png" 
    plt.pcolormesh(x,y,temp[t,3,:,:])
    #plt.colorbar(label='T [°C]')
    plt.title("temperature in x-y plane at z = 3cm")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.savefig('img/' + file_name, format='png')
    plt.close 
plt.close

# %% Generate GIF for x-y-plane
FrameRate = 10
images = []
for file_name in sorted(os.listdir(dirName)) :
    if file_name.startswith('Txy') :
        file_path = os.path.join(dirName,file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('GIF/Txy.gif',images,format='GIF',fps=FrameRate)

# %% Plot T(y,z) at x = 10cm

plt.figure()
for t in range(100):
    print("Time Step " + str(t+1) + "/100")
    file_name = "Tyz" + str(t+1).zfill(3) + ".png" 
    plt.pcolormesh(y,z,temp[t,:,:,10])
    #plt.colorbar(label='T [°C]')
    plt.title("temperature in y-z plane at x = 10cm")
    plt.xlabel("y [m]")
    plt.ylabel("z [m]")
    plt.savefig('img/' + file_name, format='png')
    plt.close 
plt.close 

# %% GIF for x-y-plane
FrameRate = 10
images = []
for file_name in sorted(os.listdir(dirName)) :
    if file_name.startswith('Tyz') :
        file_path = os.path.join(dirName,file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('GIF/Tyz.gif',images,format='GIF',fps=FrameRate)

# %% remove pictures
shutil.rmtree(dirName)        
    

