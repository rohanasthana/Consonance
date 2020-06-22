import numpy as np
import math
import matplotlib.pyplot as plot
import os
genres = {'blues': 0,'jazz': 1,'metal': 2, 
     'pop': 3, 'rock': 4}
GTZAN="../dataset/txt/"
song_data=[]
sub=np.zeros((41280*8,1))
blue=np.genfromtxt("../dataset/txt/blues/blues.00000.wav.txt",dtype=(float,float),delimiter=' ')
for i in range (0,41280,1):
    for j in range(0,8,1):
        sub[i*8+j]=blue[i][j]
x=np.arange(0,41280*8,1)
plot.plot(x,sub)
plot.show()
#print(sub.shape)
#song_data.append(sub)

#for x,_ in genres.items():
 #     for root, subdirs, files in os.walk(GTZAN + x):
  #      for file in files:
   #       # Read the txt file
    #        file_name = GTZAN + x + "/" + file
     #       print(file_name)
      #      if(file_name=="../dataset/txt/blues/blues.00000.wav.txt"):
       #         continue
        #    arr=np.genfromtxt(file_name,dtype=(float,float),delimiter=' ')
         #   arr=arr[:645,:512]
          #  for i in range (0,645,1):
           #     for j in range(0,512,1):
            #        sub[i*512+j]=arr[i][j]
            
           # song_data.append(sub)
            
            
         
#print(np.array(song_data).shape)

