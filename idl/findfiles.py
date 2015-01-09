# findfiles.py
# ------------
#
# Re-implementation of findfiles.ksh
# Re-implementation of findfiles.pro

from subprocess 
import numpy as np 
import netCDF4
from os import listdir
from os.path import isfile, join
import yaml

numRegions = 5 
openDay = np.zeros(numRegions)
openNight = np.zeros(numRegions)
iunDay = np.arange(numRegions)
iunDay = iunDay + 10 
iunNight = iunDay[numRegions - 1] + iunDay + 1 

# List containing all special regions
regionName = ['MR', 'ER', 'SR', 'WN', 'BS']

# List of day granules
dayGranules = {}

# List of night granules
nightGranules = {}


# Path of files to look into
# path = input_dir + '_' +  satellite + '_' +  mmdd + '.hdf'
# Need to get a regex to sort files inside the right directory
# TODO: FIND REGEX 
# filterFiles(path)
path = "/Users/DrkSephy/Dropbox/granules/"
fileList = [ f for f in listdir(path) if isfile(join(path, f)) ]
# print fileList

specialRegions = {
    'MR': {'lonmin': 98, 'lonmax': -82, 'latmin': 18, 'latmax': 30},
    'ER': {'lonmin': -80, 'lonmax': -61, 'latmin': 30, 'latmax': 47},
    'SR': {'lonmin': -89, 'lonmax': -72, 'latmin': 22, 'latmax': 38},
    'WN': {'lonmin': -136, 'lonmax': -121, 'latmin': 39, 'latmax': 51},
    'BS': {'lonmin': 27, 'lonmax': 42, 'latmin': 40, 'latmax': 48}
}

# Create global data structure which has a list for each 
data = { name: [] for name in regionName }
daynightData = { }
daynightData['day'] = { name: [] for name in regionName }
daynightData['night'] = { name: [] for name in regionName }
# print data

# Loop over all granules inside fileList
for f in fileList: 
    ds = netCDF4.Dataset(path + f)
    # Select l2p_flags variable
    flags = np.array(ds.variables['l2p_flags'])
    # Read day/night bit (bit 10: 0=night, 1=day)
    bit10 = np.array(np.ones(flags.shape)*(2**9), dtype='uint16')
    # Create array of all day pixels 
    dayMask = np.squeeze(np.bitwise_and(flags, bit10) > 0)
    print dayMask.shape
    # Create array of all night pixels
    nightMask = np.bitwise_not(dayMask)
    print nightMask.shape

    # Grab the longitude
    lon = np.array(ds.variables['lon']) 

    # Grab the latitude
    lat = np.array(ds.variables['lat'])

    # Iterate over each special region
    # Get the maximum number of pixels bounded in the region
    maxRegion = 0
    # Which region had the most bounded pixels?
    maxRegionName = ''

    for reg in regionName:

        # Create an array of records in the file which are  
        # within the special region

        # NOTE: Need to figure out how to do this properly with np.where.
        #       We need to use this array to get the number of day pixels
        region_arr = (np.logical_and(np.logical_and(lon >= specialRegions[reg]['lonmin'], lon <= specialRegions[reg]['lonmax']),
                        np.logical_and(lat >= specialRegions[reg]['latmin'], lat <= specialRegions[reg]['latmax']))).nonzero()

        dayCount = len(dayMask[region_arr].nonzero()[0])
        nightCount = len(nightMask[region_arr].nonzero()[0])
        if dayCount > 0: 
            daynightData['day'][reg].append((f, dayCount))
        if nightCount > 0:
            daynightData['night'][reg].append((f, nightCount))

print yaml.dump(daynightData)

# Calling command line functions

# Option 1
# from subprocess import Popen, PIPE
# cmd = "ls foobar"
# pid = Popen(cmd, shell=True)
# pid.wait()

# Option 2
# from subprocess import Popen, PIPE
# cmd = "ls foobar"
# pid = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
# stdout, stderr = pid.communicate()


















