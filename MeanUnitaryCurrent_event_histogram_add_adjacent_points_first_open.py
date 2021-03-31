

######VERY VERY VERY IMPORTANT! INPUT .ABF FILES MUST BE RESAVED AS INTEGER AND NOT FLOAT. ABF SAVED AS FLOAT CANNOT BE READ BY PYABF###########

import pyabf
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt


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

for z in Time:
	current_index=current_index+1
	if Transition_Index>len(classification)-1:
			pass
	else:
		if z<msTransitions[0]:
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

						else:
							new_Current_Histogram.append(np.nan)
							new_Class_list.append(classification[Transition_Index-1])
				else:
					new_Current_Histogram.append(Current[current_index])
					new_Class_list.append(classification[Transition_Index-1])
					
			else:
				Transition_Index=Transition_Index+1
				if Transition_Index>len(classification)-1:#excludes the last transition
					pass
				else:
					if classification[Transition_Index-1]==0:
						####This block adds 0 events one timeframe directly after 1 event
						if Class_list[current_index-1]==1:
							new_Current_Histogram.append(Current[current_index])
							new_Class_list.append(classification[Transition_Index-1])
						else:			
							new_Current_Histogram.append(np.nan)
							new_Class_list.append(classification[Transition_Index-1])
					else:
						new_Current_Histogram.append(Current[current_index])
						new_Class_list.append(classification[Transition_Index-1])


df['current']=new_Current_Histogram
df['classification']=new_Class_list

#Write the csv out
df.to_csv('Eventslist_2_Histogram_1adjacent_FirstOpen.csv', sep='\t')


