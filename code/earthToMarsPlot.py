# to run this code, i created a venv and downloaded spiceypi and matplotlib into the venv
# honestly not sure if you need to create your own venv or you can just use mine
# i guess try both lol
# terminal commands:
# cd intro_to_spiceyp
# python3 -m venv venv                 (creates a virtual env folder in this directory)
# source venv/bin/activate             (will initialize your venv in the terminal)
# pip3 install spiceypy matplotlib
# cd code
# python3 ./earthToMarsPlot.py         (to run this code)     


import os
import spiceypy as spice
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np

#Define our kernels path
kernelsPath = os.path.join(os.path.dirname(os.getcwd()), "kernelzzz")

#Define the path to the leap second kernel
leapSecondsKernelPath = os.path.join(kernelsPath, "naif0012.tls")

#Load the leap second kernel
spice.furnsh(leapSecondsKernelPath)

#Define 'now'
nowDT = datetime.now()
now = str(nowDT)
print(now)

#Convert it to ET
nowET = spice.str2et(now)

# take time and add seconds for a loop 2yrs
# try plot output (1 val per day)
print(nowET)

#Define the path to the solar system ephemeris kernel
solarSystemEpheremisKernelPath = os.path.join(kernelsPath, "de405.bsp")

#Load the kernel
spice.furnsh(solarSystemEpheremisKernelPath)

#Define frames : target=earth, observer=sun
target = "EARTH"
observer = "MARS"
reference = "J2000"

lightseconds = []
minsFromT0 = []

YEARS = 5

#Get earth positions
earthPositions = spice.spkpos(target, nowET, reference, 'NONE', observer)
for i in range(0, 365*YEARS):
    nowDT += timedelta(days=1)
    earthPositions = spice.spkpos(target, spice.str2et(str(nowDT)), reference, 'NONE', observer)
    print(earthPositions)
    lightseconds.append(earthPositions[1])
    minsFromT0.append(i)

x = np.array(minsFromT0)
y = np.array(lightseconds)
plt.scatter(x,y)
plt.title("Distance between Earth and Mars (in lightseconds) over the span of " + str(YEARS) + " years")
plt.xlabel("Days from t0")
plt.ylabel("Lightseconds")
plt.show()

#Unload kernels
spice.kclear()
