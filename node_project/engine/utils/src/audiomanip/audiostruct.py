import os
import keras
import librosa
import numpy as np


class AudioStruct(object):
  def __init__(self, file_path):
    # Constants
    self.song_samples = 660000
    self.file_path = file_path
    self.n_fft = 2048
    self.hop_length = 512
    self.genres = {'metal': 2, 'jazz': 1,
     'pop': 3, 'blues': 0, 'rock': 4}

  def getdata(self):
    
    song_data = []
    genre_data = []
        
    
    for x,_ in self.genres.items():
      for root, subdirs, files in os.walk(self.file_path + x):
        for file in files:
          
            file_name = self.file_path + x + "/" + file
            print(file_name)
            signal, sr = librosa.load(file_name)
          
            
            
            
          
            
            melspec = librosa.feature.melspectrogram(signal[:self.song_samples],
              sr = sr, n_fft = self.n_fft, hop_length = self.hop_length).T[:640,]
            
            
            song_data.append(melspec)
            genre_data.append(self.genres[x])
    return np.array(song_data), keras.utils.to_categorical(genre_data, len(self.genres))
