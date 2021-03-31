

######VERY VERY VERY IMPORTANT! INPUT .ABF FILES MUST BE RESAVED AS INTEGER AND NOT FLOAT. ABF SAVED AS FLOAT CANNOT BE READ BY PYABF###########

import pyabf
import numpy as np
import pandas as pd



#Build the DataFrame that stores all records, df[list name]=[list you want to add] slaps whatever [list] onto the end of the df as a column
df=pd.DataFrame()

#Pull transitions out of the eventslist
events=[]
classification=[]

text=input('Type the name of the txt file(omit .txt)')
textfile=str(text)+'.txt'
abfinput=input('Type the name of the abf file(omit .abf)')
abffile=str(abfinput)+'.abf'

with open(textfile) as input_file:##INPUT later
	for line in input_file:
		split=line.split()
		events.append(float(split[1]))
		classification.append(int(split[0]))

#Sum the events sequentially to construct transition list in real time
Transitions=[0]
for i in events:
	Transitions.append((max(Transitions)+i))

#Divide by 1000 to convert Transitions to ms to match the units of abf in seconds
msTransitions=[x/1000 for x in Transitions]

#Open up the abf and pull out time and current Must be saved as int, floats will not be read
abf = pyabf.ABF(abffile)
Current=abf.sweepY
Time=abf.sweepX

Current_Histogram=[]
Class_list=[]
Transition_Index=1
current_index=-1
for z in Time:
	current_index=current_index+1
	if Transition_Index>len(classification)-1:
			pass
	else:
		if z<msTransitions[0]:
			print('before first transition point')
			pass
		else:
			if z<=msTransitions[Transition_Index]:
				if classification[Transition_Index-1]==0:
					Current_Histogram.append(Current[current_index])
					Class_list.append(classification[Transition_Index-1])

				else:
					Current_Histogram.append(Current[current_index])
					Class_list.append(classification[Transition_Index-1])
			else:
				Transition_Index=Transition_Index+1
				if Transition_Index>len(classification)-1:
					pass
				else:
					if classification[Transition_Index-1]==0:
						Current_Histogram.append(np.nan)
						Class_list.append(classification[Transition_Index-1])
					else:
						Current_Histogram.append(Current[current_index])
						Class_list.append(classification[Transition_Index-1])

new_Current_Histogram=[]
new_Class_list=[]
Transition_Index=1
current_index=-1
Skip_counter=-1
end_counter=[100000000000000000000000000000000000000]
for z in Time:
	current_index=current_index+1
	if Transition_Index>len(classification)-1:
		end_counter.append(current_index)
		pass
	else:
		if z<msTransitions[0]:
			Skip_counter=Skip_counter+1
			print('before first transition point')
			pass
		else:
			if z<=msTransitions[Transition_Index]:
				if classification[Transition_Index-1]==0:
		#			####This block adds 0 events one timeframe directly before 1 event
					if current_index==len(Class_list)-1:
						pass
					else:
						if Class_list[current_index+1]==1:
							new_Current_Histogram.append(Current[current_index])
							new_Class_list.append(classification[Transition_Index-1])
		#					
						else:
							new_Current_Histogram.append(np.nan)
							new_Class_list.append(classification[Transition_Index-1])
				else:
					new_Current_Histogram.append(Current[current_index])
					new_Class_list.append(classification[Transition_Index-1])
					
			else:
				Transition_Index=Transition_Index+1

				if Transition_Index>len(classification)-1:#excludes the last transition
					end_counter.append(current_index)
					pass
				else:
					if classification[Transition_Index-1]==0:
						####This block adds 0 events one timeframe directly after 1 event
						if Class_list[current_index-1]==1:
							new_Current_Histogram.append(Current[current_index])
							new_Class_list.append(classification[Transition_Index-1])
#							
						else:			
							new_Current_Histogram.append(np.nan)
							new_Class_list.append(classification[Transition_Index-1])
					else:
						new_Current_Histogram.append(Current[current_index])
						new_Class_list.append(classification[Transition_Index-1])

#Create a bin to collect the MeanCurrents
MeanCurrents=[]
Dwelltime=[]
index=-1
loop_bin=[]
start_time=0
stop_time=0
for z in Time:
	index=index+1
	if index<Skip_counter or index>=min(end_counter):
		pass
	else:
		if index-2<0 or index+2>len(new_Class_list)-1:
			pass
		else:
			if new_Class_list[index-2]==0 and new_Class_list[index-1]==0 and new_Class_list[index]==0 and new_Class_list[index+1]!=0:
				start_time=Time[index]
				loop_bin.append(new_Current_Histogram[index])
			else:
				if new_Class_list[index+2]==0 and new_Class_list[index+1]==0 and new_Class_list[index]==0 and new_Class_list[index-1]!=0:
					loop_bin.append(new_Current_Histogram[index])
					MeanCurrents.append(np.mean(loop_bin))
					loop_bin=[]

					duration=Time[index]-start_time
					Dwelltime.append(duration)
				else:
					if new_Class_list[index]!=0:
						loop_bin.append(new_Current_Histogram[index])
					else:
						if new_Class_list[index-1]!=0 and new_Class_list[index]==0 and new_Class_list[index+1]==0 and new_Class_list[index+2]!=0:
							loop_bin.append(new_Current_Histogram[index])
						else:
							if new_Class_list[index-2]!=0 and new_Class_list[index-1]==0 and new_Class_list[index]==0 and new_Class_list[index+1]!=0:
								loop_bin.append(new_Current_Histogram[index])
							else:
								pass #this should skip the 0 events not flanking anything

#Transform MeanCurrents
transformed_MeanCurrents=[]
transformed_Dwelltime=[]
ln_Dwelltime=[]
for i in MeanCurrents:
	transformed_MeanCurrents.append(-1*i)
for i in Dwelltime:
	transformed_Dwelltime.append(i*1000)#convert seconds to ms
for i in transformed_Dwelltime:
	ln_Dwelltime.append(np.log10(i))#convert ms to ln(ms)


#Option to write out in log(time) is commented out

df['dwelltime (ms)']=transformed_Dwelltime
#df['(dwelltime) (ms)']=ln_Dwelltime
df['mean current']=transformed_MeanCurrents


#Write the csv out
df.to_csv('dwell_and_meanCurrent_1.csv', sep='\t')
#gf.to_csv('2D_Hist_nonzero_values_ms.csv', sep='\t')
#log10time.to_csv('2D_Hist_nonzero_values_log10ms.csv', sep='\t')



