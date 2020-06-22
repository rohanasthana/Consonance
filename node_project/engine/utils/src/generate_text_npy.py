import numpy as np
import math
import os
import sys
genres = {'blues': 0,'jazz': 1,'metal': 2, 
     'pop': 3, 'rock': 4}
GTZAN="../dataset/txt/"
song_data=[]
ar=np.zeros((3*468,128))

for x,_ in genres.items():
      for root, subdirs, files in os.walk(GTZAN + x):
            for file in files:
          # Read the txt file
                  file_name = GTZAN + x + "/" + file
                  print(file_name)
                  arr=np.genfromtxt(file_name,dtype=(float,float),delimiter=' ')
                  if(file_name=="../dataset/txt/pop/pop.00099.wav.txt"):
                        for i in range(3):
                              for j in range(0,468,1):
                                    for k in range(0,128,1):
                  
                                          ar[i*468+j][k]=arr[j][k]
                                          ar=ar[:1280,:128]
                                          song_data.append(ar)
                  
                  else:
                        if(file_name=="../dataset/txt/blues.00035.wav.txt"):
                              continue
                        print(arr.shape)
                        
                        #if(arr.shape!=(1280,128)):
                              
                              #sys.exit("Error")
                        arr=arr[:1280,:128]
                        song_data.append(arr)
songs=np.array(song_data)
print(songs.shape)
np.save(GTZAN+"songs.npy",songs)
            
            
