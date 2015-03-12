import time, signal, sys
import utils
#from Adafruit_ADS1x15 import ADS1x15

# Ch: 0, 1, 2, 3
# sps: 8, 16, 32, 64, 128, 250, 475, 860
# pga: 6144, 4096, 2048, 1024, 512, 256

#sps = 8
#pga = 256
samp = 100


load_raw = []
load = []
load_max = []
load_min = []
load_diff = []
load_avg = []

#adc = ADS1x15(ic=0x01)
#for i in range(4):
#    load_raw.append(adc.readADCSingleEnded(i, 6144, 8))

load = utils.Load()

for i in range (samp):
    load_row = []
    for j in range(1, 3, 1):
#        load_row.append(adc.readADCDifferential(j, (j+1), pga, sps))
         load_row.append(load.store_load(j))
    print i
    print load_row
    load_raw.append(load_row)

load = zip(*load_raw)

for i in range(len(load)):
    load_max.append(max(load[i]))

for i in range(len(load)):
    load_min.append(min(load[i]))

for i in range(len(load)):
    load_diff.append(load_max[i]-load_min[i])

for i in range(len(load)):
    load_avg.append(sum(load[i])/len(load[i]))

print load
print load_max
print load_min
print load_diff
print load_avg
