
from audiomanip.audiomodels import ModelZoo
from audiomanip.audioutils import AudioUtils
from audiomanip.audioutils import MusicDataGenerator
import librosa
import matplotlib.pyplot as plot
from keras.models import load_model
import numpy as np
import keras
from audiomanip.audioutils import AudioUtils
from audiomanip.audiostruct import AudioStruct
from keras.models import load_model
cnn= load_model('gtzan_hguimaraes.h5')
song_rep=AudioStruct("../models/")
songs,genres=song_rep.getdata()
temp_X=[]
for i,song in enumerate(songs):
    song_split=np.split(song,5)
    for s in song_split:
        temp_X.append(s)
temp_X=np.array(temp_X) 
pred = np.argmax(cnn.predict(temp_X), axis = 1)
print(pred[0])
