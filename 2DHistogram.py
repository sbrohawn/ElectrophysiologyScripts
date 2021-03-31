

######VERY VERY VERY IMPORTANT! INPUT .ABF FILES MUST BE RESAVED AS INTEGER AND NOT FLOAT. ABF SAVED AS FLOAT CANNOT BE READ BY PYABF###########

import pyabf
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as lol

#define bins
Xbin=input("Enter desired X (ms) histogram as smallest, largest, # of bins  i.e 0,150,1500: ")
Ybin=input("Enter desired Y(pA) histogram as smallest, largest, # of bins  i.e 0,4,40: ")
Files=input("Enter the number of files you want to analyze (Assumes filename dwell_and_meanCurrent_#.csv and first # is 1)")
Files_int=int(Files)

Xbi=list(Xbin.split(","))
Ybi=list(Ybin.split(","))
Filelist=[]

filecounter=1
while filecounter < Files_int+1:
	Filelist.append(str('dwell_and_meanCurrent_'+str(filecounter)+'.csv'))
	filecounter=filecounter+1
	print(filecounter)

Xbins=[]
for i in Xbi:
	Xbins.append(int(i))
Ybins=[]
for i in Ybi:
	Ybins.append(int(i))
	
#Build the DataFrame that stores all records, df[list name]=[list you want to add] slaps whatever [list] onto the end of the df as a column
df=pd.DataFrame()

#Pull transitions out of the eventslist
xbin=[]
ybin=[]
N=[]
for i in Filelist:
	skip=0
	with open(i) as input_file:##INPUT later
		for line in input_file:
			if skip==0:
				skip=skip+1
			else:
				split=line.split()
				xbin.append(float(split[1]))
				ybin.append(float(split[2]))

#3D hist
Dwell_array=np.array(xbin)
Current_array=np.array(ybin)


x_bins = np.linspace(Xbins[0],Xbins[1],Xbins[2]) 
y_bins = np.linspace(Ybins[0],Ybins[1],Ybins[2])

fig, ax = plt.subplots()
ax.set_aspect("equal")
hist, xbins, ybins, im = ax.hist2d(Dwell_array,Current_array, bins=[x_bins,y_bins])


X_values=[]
Y_values=[]

N_values=[]
Label=[]
for i in range(len(y_bins)-1):
    for j in range(len(x_bins)-1):
    	if hist.T[i,j]!=0:
    		N_values.append(hist.T[i,j])
    		X_values.append(x_bins[j])
    		Y_values.append(y_bins[i])
    		Label.append('LPO')
    	else:
    		pass

X_plus_half_bin=[]
for i in X_values:
	X_plus_half_bin.append(i+((Xbins[1]/Xbins[2])/2))

Y_plus_half_bin=[]
for i in Y_values:
	Y_plus_half_bin.append(i+((Ybins[1]/Ybins[2])/2))

gf=pd.DataFrame()


gf['Dwelltime (ms)']=X_plus_half_bin
gf['Current']=Y_plus_half_bin
gf['N']=N_values
gf['Label']=Label

#Write the csv out
gf.to_csv('Dwell_and_MeanCurrent_2DHist.csv', sep='\t')



