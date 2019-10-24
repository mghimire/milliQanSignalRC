import vxi11
import pylab as pl
from datetime import datetime
import time
import csv

#data collection variables

starttime	= time.time()
runtime 	= 0.5	#in hours

def main():
	sds = vxi11.Instrument("192.168.1.22") #read instrument IP address based on lxi discover
	sds.write("chdr off") #turn off command header in responses
	vdiv1 = sds.ask("c1:vdiv?") #get vertical sensitivity in Volts/div
	vdiv2 = sds.ask("c2:vdiv?")
	ofst1 = sds.ask("c1:ofst?") #get vertical offset of channels
	ofst2 = sds.ask("c2:ofst?")
	tdiv = sds.ask("tdiv?") #get horizontal scale per division
	sara = sds.ask("sara?") #get sample rate
	sara_unit = {'G':1E9,'M':1E6,'k':1E3} #set G, M, k unit multipliers
	
	for unit in sara_unit.keys():
		if sara.find(unit)!=-1: #verify unit type
			sara = sara.split(unit) #get number before unit and multiply
			sara = float(sara[0])*sara_unit[unit] #with appropriate unit multiplier
			break
	sara = float(sara)

	#csv file writing variables
	header = ['time', ' c1', ' c2']
	
	while (time.time() - starttime)/(60*60) <= runtime:
		updatedtime = time.time()
		
		sds.timeout = 2000 #default value is 2000(2s)
		sds.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
		sds.write("c1:wf? dat2") #get data from channel 1
		recv1 = list(sds.read_raw())[15:] #set to list, getting rid of header
		recv1.pop() #get rid of last two \n elements
		recv1.pop()
		volt_value1 = []
		
		for data in recv1:
			data = data.encode('hex')
			data = int(data, 16)
			if data > 127:
				data = data - 255
			else:
				pass
			volt_value1.append(data)
			
		sds.write("c2:wf? dat2") #get data from channel 2
		recv2 = list(sds.read_raw())[15:] #set to list, getting rid of header
		recv2.pop() #ghttps://www.google.com/search?client=ubuntu&channel=fs&q=numpy+output+format&ie=utf-8&oe=utf-8et rid of last two \n elements
		recv2.pop()
		volt_value2 = []
		
		for data in recv2:
			data = data.encode('hex')
			data = int(data, 16)
			if data > 127:
				data = data - 255
			else:
				pass
			volt_value2.append(data)

		time_value = []
		
		for idx in range(0,len(volt_value1)):
#			volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
			time_data = -(float(tdiv)*14/2)+idx*(1/sara)
			time_value.append(time_data)
		
		timestamp = str(datetime.fromtimestamp(updatedtime))[:-7]	#get time up to seconds
		filename = timestamp + '.csv'
		
		pl.figure(figsize=(7,5))
		pl.plot(time_value, volt_value1, 'y', time_value, volt_value2, 'b')
#		pl.legend()
		pl.grid()
#		pl.show()
		pl.savefig(timestamp + '.pdf')
		pl.close()
		
		with open(filename, 'wb') as datFile:
			writer = csv.writer(datFile)
			writer.writerow(header)
			for i in range(0,len(time_value)):
				writer.writerow([time_value[i], volt_value1[i], volt_value2[i]])
		
		datFile.close()
		
		if time.time() - updatedtime < 2.0:
			time.sleep(2.0 - ((time.time() - updatedtime)/2.0))
	
	
if __name__=='__main__':
	main()
