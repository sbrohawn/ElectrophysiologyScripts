import pyabf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#############Assumes .abf (int) filename is "Patch#_0001.abf", etc...############

Patch=input("Enter the patch number (i.e. 1) :")
Traces=input("Enter the number of traces as a,b,c..(nospace) :")
Voltage_Range=input("Enter the Voltage sweep range and interval (i.e -100,100,20) : ")
Time_Range=input("Enter the interval of time values (assumes 100us sampling i.e 1 second=10000) Enter as 3500,5000 : ")

filename="Patch"+Patch

Traces=Traces.strip('][').split(',')
Integer_traces=[]
for i in range(0, len(Traces)):
	Integer_traces.append(int(Traces[i]))
#Traces is a list of strings
#Integer_Traces is a list of ints

#Build time range
Str_Time_Range=Time_Range.strip('][').split(',')
Times=[]
for i in Str_Time_Range:
	Times.append(int(i))

##Build Voltage Family sweep and interval for dataframe #######
StrVoltRange=Voltage_Range.strip('][').split(',')

IntVoltRange=[]
for i in StrVoltRange:
	IntVoltRange.append(int(i))
Voltage_Sweep=[]

start, end, interval = IntVoltRange[0],IntVoltRange[1],IntVoltRange[2]
if start<end:
	Voltage_Sweep.extend(range(start,end,interval))
	Voltage_Sweep.append(end)

epoch=0
epochs=[]
for i in Voltage_Sweep:
	epochs.append(epoch)
	epoch+=1

#Build the DataFrame that stores IV values for all input recordings

mV={'mV':Voltage_Sweep} 
df=pd.DataFrame(mV)

#This part pads with 0 for correct filename
for z in Integer_traces:
	if 0<z<10:
		pad='000'
		pass
	if 9<z<100:
		pad='00'
		pass
	if 99<z<1000:
		pad='0'
		pass
#Now the first file gets opened
	abf = pyabf.ABF(filename+"_"+pad+str(z)+'.abf')
	mean_current=[]
	#match stimulus waveform
	epoch_index=[]
	epoch_mV=[]

	for sweepNumber in abf.sweepList:
		abf.setSweep(sweepNumber)
		epoch_index.append(sweepNumber)
		epoch_mV.append(abf.sweepC[Times[0]])

	for i in epoch_mV:
		if i==Voltage_Sweep[0]:
			break
			####Add one to epochs index until the desiresed starting voltage sweep is found in the .abf file##
		else:
			holder=[]
			for i in epochs:
				holder.append(i+1)
			epochs=holder

	for i in epochs:

#extract time average for each sweep
		abf.setSweep(i)
		mean=np.mean(abf.sweepY[Times[0]:Times[1]])
		mean_current.append(mean)
		index_as_string=str(z)
	df[index_as_string]=mean_current

#Write the csv out
df.to_csv(filename+'.csv', sep='\t')

#Make a quick IV plot of all traces in the csv
df.plot(x='mV',y=Traces, kind="line")
plt.xlabel('mV')
plt.ylabel('pA')
plt.gca().spines['bottom'].set_position('zero')
plt.gca().spines['top'].set_position('zero')
plt.gca().spines['left'].set_position('zero')
plt.gca().spines['right'].set_position('zero')
plt.legend(loc='center left', bbox_to_anchor=(-0.15, 0.5))
plt.savefig(filename+'_IV.png')




