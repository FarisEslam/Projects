from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
t=np.linspace(0,3,12*1024) #time axis
N = 3*1024
F=np.linspace(0,512,int(N/2)) #frequency axis
lefthandfreq=[130.81,220,196,130.81,220,196]
righthandfreq=[440,392,0,349.23,392,0]
start=[0,0.5,1,1.5,2,2.5]
end=[0.45,0.95,1.45,1.95,2.45,2.95]
x=np.zeros(12*1024)
i=0

while (i<6):
    lh=np.where((t>=start[i])&(t<=end[i]),np.sin(np.pi*t*2*lefthandfreq[i]),0)
    rh=np.where((t>=start[i])&(t<=end[i]),np.sin(np.pi*t*2*righthandfreq[i]),0)
    i+=1
    x=x+lh+rh
fn1,fn2= np.random.randint(0, 512, 2)
xinfrequency = fft(x)
xinfrequency = 2/N * np.abs(xinfrequency [0:np.int(N/2)])
noise= np.sin(np.pi*t*2*fn1)+np.sin(np.pi*t*2*fn2)
xandnoise=x+noise
xandnoiseinfrequency = fft(xandnoise)
xandnoiseinfrequency = 2/N * np.abs(xandnoiseinfrequency [0:np.int(N/2)])
tempmax=0
for i in range(len(xinfrequency)):
  if(xinfrequency[i]>tempmax):
    tempmax=xinfrequency[i]
tempmax=round(tempmax)
foundfrequency1 = 0
foundfrequency2 = 0
for i in range(len(xandnoiseinfrequency)):
    m=xandnoiseinfrequency[i]
    if(round(m)>tempmax and foundfrequency1==0):
      foundfrequency1=F[i]
    elif (round(m)>tempmax):
      foundfrequency2=F[i]
foundfrequency1 = round(foundfrequency1)
foundfrequency2 = round(foundfrequency2)   
print(fn1)
print(fn2)
print(foundfrequency1)
print(foundfrequency2)
noisetoberemoved=np.sin(2*np.pi*foundfrequency1*t)+np.sin(2*np.pi*foundfrequency2*t)

finalsong= xandnoise-noisetoberemoved
finalsonginfrequency = fft(finalsong)
finalsonginfrequency = 2/N * np.abs(finalsonginfrequency [0:np.int(N/2)])
plt.Figure()
plt.subplot(6,2,1)
plt.plot(t,x)
plt.subplot(6,2,2)
plt.plot(F,xinfrequency)
plt.subplot(6,2,3)
plt.plot(t,xandnoise)
plt.subplot(6,2,4)
plt.plot(F,xandnoiseinfrequency)
plt.subplot(6,2,5)
plt.plot(t,finalsong)
plt.subplot(6,2,6)
plt.plot(F,finalsonginfrequency)
sd.play(finalsong,3*1024)
