import librosa
import numpy as np
import matplotlib.pyplot as plot
signal,sr=librosa.load('../models/blues/From The Inside.au')
print(signal.shape)

melspec = librosa.feature.melspectrogram(signal[:660000],
              sr = sr, n_fft = 2048, hop_length = 512).T[:640,]
print(melspec.shape)
x1=np.arange(0,640,1)
plot.plot(x1,melspec)
plot.show()
arr=np.genfromtxt("../dataset/txt/blues.00000.wav.txt",dtype=(float,float),delimiter=' ')

arr=arr[:640,:]
print(arr.shape)
plot.plot(x1,arr)
plot.show()
