import pandas as pd
from pandas import DataFrame
import numpy as np
import PIV
import h5py
import matplotlib.pyplot as plt
import hotwire as hw

### PIV INNER PLOTS AND ANALYSIS ########
#########################################

def piv_inner(date, num_tests, utau):
	################################################
	#   PURPOSE
	#   1. Inner Normalize
	#   2. PLOT
	#       uplus vs yplus
	#       urmsplus vs yplus
	#       uvprimeplus vs yplus
	##################################################
	##note- vel and axis are flipped to properlly calc delta

	## Initalize variables
	conf = dict()
	# yplus = dict()
	# urmsplus = dict()
	# uvprimeplus = dict()
	#read in variables
	name = 'data/PIV_' + date + '.h5'
	umean = np.array(pd.read_hdf(name, 'umean_profile_avg'))[:-3]*-1
	vmean = np.array(pd.read_hdf(name, 'vmean_profile_avg'))[:-3]
	urms = np.array(pd.read_hdf(name, 'urms_profile_avg'))[:-3]
	vrms = np.array(pd.read_hdf(name, 'vrms_profile_avg'))[:-3]
	uvprime = np.array(pd.read_hdf(name, 'uvprime_profile_avg'))[:-3]
	x = np.array(pd.read_hdf(name, 'xaxis'))[:-3]
	y = np.array(pd.read_hdf(name, 'yaxis'))[:-3]
	conf = pd.read_hdf(name, 'confidence')[:-3]
	#air_prop = hw.air_prop(23)
	####Vincenti data###
	name = 'data/outside_data/FPF_Vincenti_Data.h5'
	unorm = np.array(pd.read_hdf(name, 'unorm'))
	ynorm = np.array(pd.read_hdf(name, 'ynorm'))
	Re_tau = ['1450', '2180', '2280', '3270', '5680', '6430', '10770', '15480', '15740']
	urms_vincenti = pd.read_csv('data/outside_data/urmsplus_fpf_primary.csv', delimiter=',')
	yplus_vincenti = pd.read_csv('data/outside_data/yplus_fpf_primary.csv', delimiter=',')
	# ### WUMOIN DATA #######
	wumoin = dict()
	temp = pd.read_csv('data/outside_data/yplus_versus_-uv_plus_Re_1840.dat', delimiter=' ')
	temp = temp.shift(1)
	temp.columns = ['0', 'yplus','uvplus']
	temp['yplus'][0] = 0.2558821659990199
	temp['uvplus'][0] = 0.00009276450027256462
	wumoin['yplus_1840'] = temp['yplus']
	wumoin['uvplus_1840'] = temp['uvplus']
	# ## Reza Data ##
	# # #Reza PIV Velocity data
	name = 'data/outside_data/PIV_ZPG_071016.h5'
	urms_reza =np.array(pd.read_hdf(name, 'rms'))
	ynorm_reza = np.array(pd.read_hdf(name, 'yplus'))

	### INNER NORMALIZE #
	#####################
	#approximate utau, calculated and then adjusted
	#utau = [.133]
	uplus = umean/utau
	yplus = (y*utau)/(1.538*10**(-5))
	urmsplus = urms/utau
	vrmsplus = vrms/utau
	uvprimeplus = uvprime/utau**2
	conf['uplus'] = conf['u']/utau
	conf['urmsplus'] = conf['urms']/utau
	conf['vrmsplus'] = conf['vrms']/utau
	conf['uvprimeplus'] = conf['uvprime']/utau**2

	### Plot figure of heated and unheated PIV data
	###############################################
	legend1 = [r'$Re_\tau=$1450', r'$Re_\tau=$2180', r'$Re_\tau=$2280', r'$Re_\tau=$3270', r'$Re_\tau=$5680', r'$Re_\tau=$6430', r'$Re_\tau=$10770', r'$Re_\tau=$15480', r'$Re_\tau=$15740', 'Adrian PIV']
	marker_V = ['-xr', '-xg', '-xb', '-xm', '-xk', '-xc', '-sr', '-sg', '-sb']
	# marker = ['-or', '-ob']
	plt.figure()
	##Uplus Yplus
	#plot vincenti data
	for j in range(0, 9):
		plt.semilogx(ynorm[j], unorm[j], marker_V[j])
	#plot PIV data
	plt.semilogx(yplus, uplus, '-or')
	plt.fill_between(yplus, uplus[:,0], uplus[:,0] + np.array(conf['uplus']), color='r', alpha=.5)
	plt.fill_between(yplus, uplus[:,0], uplus[:,0] - np.array(conf['uplus']), color='r', alpha=.5)
	plt.legend(legend1, loc=0, fontsize=10)
	plt.ylabel('$U^+$', fontsize=20)
	plt.xlabel('$y^+$', fontsize=20)
	plt.grid(True)
	plt.axis([.001, 30000, 0, 35])
	plt.show()

	##Urmsplus Yplus
	plt.figure()
	legend1 =  [r'$Re_\tau=$6430, Hot-Wire', r'Adrian, PIV', r'Conf Int.']
	#plt.semilogx(ynorm_reza[3][:-1], urms_reza, 'k')
	plt.semilogx(yplus_vincenti['yplus_6430'], urms_vincenti['urmsplus_6430'], 'k')
	plt.semilogx(yplus, urmsplus, '-xb')
	plt.fill_between(yplus, urmsplus[:,0], urmsplus[:,0] + np.array(conf['urmsplus']), color='r', alpha=.5)
	plt.fill_between(yplus, urmsplus[:,0], urmsplus[:,0] - np.array(conf['urmsplus']), color='r', alpha=.5)
	plt.legend(legend1, loc=0, fontsize=10)
	plt.ylabel('$u_{rms}^+$', fontsize=20)
	plt.xlabel('$y^+$', fontsize=20)
	plt.grid(True)
	#plt.axis([.001, 30000, 0, 35])
	plt.show()

	##Vrmsplus Yplus
	plt.figure()
	legend1 =  [r'$Re_\tau=$6430, Hot-Wire', r'Adrian, PIV', r'Conf Int.']
	#plt.semilogx(ynorm_reza[3][:-1], urms_reza, 'k')
	plt.semilogx(yplus_vincenti['yplus_6430'], urms_vincenti['urmsplus_6430'], 'k')
	plt.semilogx(yplus, vrmsplus, '-xb')
	#plt.fill_between(yplus, urmsplus[:,0], urmsplus[:,0] + np.array(conf['urmsplus']), color='r', alpha=.5)
	#plt.fill_between(yplus, urmsplus[:,0], urmsplus[:,0] - np.array(conf['urmsplus']), color='r', alpha=.5)
	plt.legend(legend1, loc=0, fontsize=10)
	plt.ylabel('$u_{rms}^+$', fontsize=20)
	plt.xlabel('$y^+$', fontsize=20)
	plt.grid(True)
	#plt.axis([.001, 30000, 0, 35])
	plt.show()

	##UVprimeplus Yplus
	legend1 =  [r'$Re_{\theta}=$1840, WuMoin', r'Adrian, PIV', r'Conf Int']
	plt.figure()
	#WuMoin
	plt.semilogx(wumoin['yplus_1840'], wumoin['uvplus_1840'], 'k')
	#PIV data
	plt.semilogx(yplus, uvprimeplus, '-xr')
	plt.fill_between(yplus, uvprimeplus[:,0], uvprimeplus[:,0] + np.array(conf['uvprimeplus']), color='r', alpha=.5)
	plt.fill_between(yplus, uvprimeplus[:,0], uvprimeplus[:,0] - np.array(conf['uvprimeplus']), color='r', alpha=.5)
	plt.legend(legend1, loc=0, fontsize=10)
	plt.ylabel('$(u^,v^,)^+$', fontsize=16)
	plt.xlabel('$y^+$', fontsize=16)
	plt.axis([1, 10000, 0, 5])
	plt.grid(True)
	plt.show()

	return
