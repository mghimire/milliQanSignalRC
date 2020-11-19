import numpy as np
import matplotlib.pyplot as pl
import csv
import glob

filenames = glob.glob("*.csv")

#print filenames

data 	     = []

for name in filenames:
	with open(name, 'r') as csvfile:
		raw = csv.reader(csvfile)
		raw = list(raw)
		raw.pop(0)
		data.append(raw)

print('There are', len(data), 'files')

data 		= np.asarray(data)
data		= data.astype(np.float)

datanum		= np.shape(data)[0]

baseval		= -89

time        = data[0][:,0]
sgnldata    = data[:,:,2] - baseval
expndata    = data[:,:,1] - baseval

res			= np.shape(time)[0]

#plot samples for new parametrization

pl.figure(figsize=(7,5))
pl.plot(time, data[:,:,1][0], 'y', time, data[:,:,2][0], 'b')
#	pl.legend()
pl.grid()
#	pl.show()
pl.savefig('oldfig.jpg')
pl.close()

pl.figure(figsize=(7,5))
pl.plot(time, expndata[0], 'y', time, sgnldata[0], 'b')
#	pl.legend()
pl.grid()
#		pl.show()
pl.savefig('newfig.jpg')
pl.close()

#classify into single signal and multiple signal first

cutoff		= 5

monosgnl   	= []	#signals with a single peak
multisgnl   = []	#signals with multiple peaks
anomaly		= []	#signals where the expanded peaks are greater than the signal peaks

for i in range(datanum):
	if np.amax(sgnldata[i]) < np.amax(expndata[i]):
		anomaly.append(i)
	else:
		peaks = np.where(sgnldata[i]>cutoff)
		if np.shape(peaks)[1] < 4:
			monosgnl.append(i)
		else:
			multisgnl.append(i)

monosgnl 	= np.asarray(monosgnl)
print('There are', np.shape(monosgnl)[0], 'single signal events')
multisgnl 	= np.asarray(multisgnl)
print('There are', np.shape(multisgnl)[0], 'multiple signal events')
anomaly 	= np.asarray(anomaly)
print('There are', np.shape(anomaly)[0], 'anomalous events')

#examples of mono signal, multi signal and anomaly
pl.figure(figsize=(7,5))
pl.plot(time, expndata[monosgnl[0]], 'y', time, sgnldata[monosgnl[0]], 'b')
#	pl.legend()
pl.grid()
#		pl.show()
pl.savefig('mono.jpg')
pl.close()

pl.figure(figsize=(7,5))
pl.plot(time, expndata[multisgnl[1]], 'y', time, sgnldata[multisgnl[1]], 'b')
#	pl.legend()
pl.grid()
#		pl.show()
pl.savefig('multi.jpg')
pl.close()

pl.figure(figsize=(7,5))
pl.plot(time, expndata[anomaly[0]], 'y', time, sgnldata[anomaly[0]], 'b')
#	pl.legend()
pl.grid()
#		pl.show()
pl.savefig('anomaly.jpg')
pl.close()

#single signal analysis
#----------------------
#idea is to compare the integrals under the peaks of the signal event and the expanded signal event

mononum		= np.shape(monosgnl)[0]
sgnlint		= np.zeros(mononum)
expnint		= np.zeros(mononum)

j	= 0 #counter variable for integral arrays
for i in monosgnl:
	sgnlpeaks 	= np.where(sgnldata[i]>cutoff)
	sgnlint[j]	= np.sum(sgnldata[i][sgnlpeaks])
	expnpeaks	= np.where(expndata[i]>cutoff)
	expnint[j]	= np.sum(expndata[i][expnpeaks])
	j += 1

pl.figure(figsize=(7,5))
pl.scatter(sgnlint, expnint)
ax = pl.gca()
ax.set_xlabel('integral around original signal peak')
ax.set_ylabel('integral around stretched signal peak')
pl.grid()
#pl.show()
pl.savefig('peakint_correlation.jpg')
pl.close()

pl.figure(figsize=(7,5))
pl.scatter(sgnlint, expnint)
pl.plot(np.unique(sgnlint), np.poly1d(np.polyfit(sgnlint, expnint, 1))(np.unique(sgnlint)), 'r')
ax = pl.gca()
ax.set_xlabel('integral around original signal peak')
ax.set_ylabel('integral around stretched signal peak')
pl.grid()
pl.text(0.7, 0.1,'m = ' + '%.5f' % np.polyfit(sgnlint, expnint, 1)[0] + ' b = ' + '%.5f' % np.polyfit(sgnlint, expnint, 1)[1],
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes)
#pl.show()
pl.savefig('peakint_lobf.jpg')
pl.close()

trnsgrsrs = []

def error(i):
	return expnint[i] - 10.99*sgnlint[i] + 207.29

for i in range(mononum):
	err = error(i)
	if np.abs(err) > 150:
		trnsgrsrs.append([i,err])
		pl.figure(figsize=(7,5))
		pl.plot(time, expndata[monosgnl[i]], 'y', time, sgnldata[monosgnl[i]], 'b')
		#	pl.legend()
		pl.grid()
		#	pl.show()
		pl.savefig(filenames[monosgnl[i]] + '.jpg')
		pl.close()

trnsgrsrs = np.asarray(trnsgrsrs).astype(int)

print(trnsgrsrs[:,0])

cleansgnlint = np.delete(sgnlint, trnsgrsrs[:,0], 0)
cleanexpnint = np.delete(expnint, trnsgrsrs[:,0], 0)

pl.figure(figsize=(7,5))
pl.scatter(cleansgnlint, cleanexpnint)
ax = pl.gca()
ax.set_xlabel('integral around original signal peak without anomalies')
ax.set_ylabel('integral around stretched signal peak without anomalies')
pl.grid()
#pl.show()
pl.savefig('cleanint_correlation.jpg')
pl.close()

pl.figure(figsize=(7,5))
pl.scatter(cleansgnlint, cleanexpnint)
pl.plot(np.unique(cleansgnlint), np.poly1d(np.polyfit(cleansgnlint, cleanexpnint, 1))(np.unique(cleansgnlint)), 'r')
ax = pl.gca()
ax.set_xlabel('integral around original signal peak')
ax.set_ylabel('integral around stretched signal peak')
pl.grid()
pl.text(0.7, 0.1,'m = ' + '%.5f' % np.polyfit(cleansgnlint, cleanexpnint, 1)[0] + ' b = ' + '%.5f' % np.polyfit(cleansgnlint, cleanexpnint, 1)[1],
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes)
#pl.show()
pl.savefig('cleanint_lobf.jpg')
pl.close()

cleanerr = sgnlint - (expnint + 226.62)/11.43

pl.figure(figsize=(7,5))
pl.hist(cleanerr, bins=100, label = 'error distribution')
ax = pl.gca()
ax.set_xlabel('difference between predicted and actual area under signal')
pl.grid()
pl.text(0.7, 0.1,'mean = ' + '%.5f' % np.mean(cleanerr) + ' std dev = ' + '%.5f' % np.std(cleanerr),
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes)
#pl.show()
pl.savefig('err_hist.jpg')
pl.close()

# sgnlpksval	= np.zeros(datanum)
# expnpksval	= np.zeros(datanum)
# sgnlpksloc	= np.zeros(datanum)
# expnpksloc	= np.zeros(datanum)

# for i in range(datanum):
# 	sgnlpksval[i] = np.amax(data[i][:,2])
# 	expnpksval[i] = np.amax(data[i][:,1])
# 	sgnlpksloc[i] = data[i][np.argmax(data[i][:,2]),0]
# 	expnpksloc[i] = data[i][np.argmax(data[i][:,1]),0]
     


# sgnlpksloc = sgnlpksloc*1e7
# expnpksloc = expnpksloc*1e7

# pl.figure(figsize=(7,5))
# pl.scatter(sgnlpksval, expnpksval)
# ax = pl.gca()
# ax.set_xlabel('value of original signal peak')
# ax.set_ylabel('value of stretched signal peak')
# pl.grid()
# #pl.show()
# pl.savefig('peakval_correlation.pdf')
# pl.close()

# pl.figure(figsize=(7,5))
# pl.scatter(sgnlpksval, expnpksval)
# pl.plot(np.unique(sgnlpksval), np.poly1d(np.polyfit(sgnlpksval, expnpksval, 1))(np.unique(sgnlpksval)), 'r')
# ax = pl.gca()
# ax.set_xlabel('value of original signal peak')
# ax.set_ylabel('value of stretched signal peak')
# pl.grid()
# pl.text(0.7, 0.1,'m = ' + '%.5f' % np.polyfit(sgnlpksval, expnpksval, 1)[0] + ' b = ' + '%.5f' % np.polyfit(sgnlpksval, expnpksval, 1)[1],
#      horizontalalignment='center',
#      verticalalignment='center',
#      transform = ax.transAxes)
# #pl.show()
# pl.savefig('peakval_lobf.pdf')
# pl.close()

# pl.figure(figsize=(7,5))
# pl.scatter(sgnlpksval, expnpksval)
# pl.plot(np.unique(sgnlpksval), np.poly1d(np.polyfit(sgnlpksval, expnpksval, 2))(np.unique(sgnlpksval)), 'r')
# ax = pl.gca()
# ax.set_xlabel('value of original signal peak')
# ax.set_ylabel('value of stretched signal peak')
# pl.grid()
# pl.text(0.7, 0.1,'a = ' + '%.5f' % np.polyfit(sgnlpksval, expnpksval, 2)[0] + ' b = ' + '%.5f' % np.polyfit(sgnlpksval, expnpksval, 2)[1] + ' c = ' + '%.5f' % np.polyfit(sgnlpksval, expnpksval, 2)[2],
#      horizontalalignment='center',
#      verticalalignment='center',
#      transform = ax.transAxes)
# #pl.show()
# pl.savefig('peakval_pobf.pdf')
# pl.close()

# pl.figure(figsize=(7,5))
# pl.scatter(sgnlpksloc, expnpksloc)
# ax = pl.gca()
# ax.set_xlabel('location of original signal peak')
# ax.set_ylabel('location of stretched signal peak')
# pl.grid()
# #pl.show()
# pl.savefig('peakloc_correlation.pdf')
# pl.close()

# outliers = np.argwhere(sgnlpksloc > -2)

# sgnlpksloc = np.delete(sgnlpksloc, outliers)
# expnpksloc = np.delete(expnpksloc, outliers)

# pl.figure(figsize=(7,5))
# pl.scatter(sgnlpksloc, expnpksloc)
# pl.plot(np.unique(sgnlpksloc), np.poly1d(np.polyfit(sgnlpksloc, expnpksloc, 1))(np.unique(sgnlpksloc)), 'r')
# ax = pl.gca()
# ax.set_xlabel('location of original signal peak')
# ax.set_ylabel('location of stretched signal peak')
# pl.text(0.7, 0.1,'m = ' + '%.5f' % np.polyfit(sgnlpksloc, expnpksloc, 1)[0] + ' b = ' + '%.5f' % np.polyfit(sgnlpksloc, expnpksloc, 1)[1],
#      horizontalalignment='center',
#      verticalalignment='center',
#      transform = ax.transAxes)
# pl.grid()
# #pl.show()
# pl.savefig('peakloc_lobf_no_outliers.pdf')
# pl.close()
