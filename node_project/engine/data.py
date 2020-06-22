import keras
import pandas as pd
import numpy as np
import os
from utils.src.audiomanip.audiomodels import ModelZoo
from utils.src.audiomanip.audioutils import AudioUtils
from utils.src.audiomanip.audioutils import MusicDataGenerator
import librosa
import matplotlib.pyplot as plot
from keras.models import load_model
from utils.src.audiomanip.audioutils import AudioUtils
from utils.src.audiomanip.audiostruct import AudioStruct
from keras.models import load_model
import mongo
import shutil
import sys
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods = ['POST'])

def func():
	content = request.get_json()
	songId = list(map(int, request.form['song'].split()))
	songNames = getsongname(songId)
	print(songNames)
	shutil.rmtree('utils/dataset/liked/userid/blues')
	os.mkdir('utils/dataset/liked/userid/blues')
	copy_data(songNames)
	ids=getdistance()
	for i in range(len(ids)):
		ids[i] += 1
		ids[i] = str(ids[i])

	ids = ' '.join(ids)
	return ids



def getsongname(songid):
	df_song_id=pd.read_csv('music_data.csv')
	print(df_song_id.columns)
	song_path=[]
	for i in songid:
		song_path.append(df_song_id.loc[df_song_id['id'] == i, 'filename'])
	return song_path

host=""
port=""'utils/dataset/liked/userid/blues'

username=""
password=""
userid=""
#df_song_id=mongo_to_df()




def copy_data(songNames):
	df_song_id=pd.read_csv('music_data.csv')
	#print(df_song_id.columns)
	for i in songNames:
		if str(i)  != ' ':
			#song_path=df_song_id.loc[df_song_id['title'] == str(i), 'filename']
			shutil.copy('../engine/utils/dataset/liked/userid/blues/id1/blues/'+str(i),'utils/dataset/liked/userid/blues'+ str(i))


#def genre_list(liked):
#	genrelist=[]
#	for i in liked:
#		genre=get_genre(i)
#		genrelist.append(genre)
#	return genrelist

def get_content(userid):
	cnn= load_model('model.h5')
	song_rep=AudioStruct("../engine/utils/dataset/liked/userid/id1/"+userid)
	songs,genres=song_rep.getdata()
	print(len(songs))
	temp_X=[]
	pred=[]
	for song in songs:
		song_split=np.split(song,5)
		for s in song_split:
			temp_X.append(s)
		temp_X=np.array(temp_X)
		pred.append(cnn.predict(temp_X))
		temp_X=[]
	pred=np.array(pred)
	return pred


		#pred = np.argmax(cnn.predict(temp_X), axis = 1)
		#genre_list.append(pred[0])
	#return genre_list

def mongo_to_df():
	connection=mongo._connect_mongo(host,port,username,password,db)
	songid=read_mongo(db, collection, query, host, port, username, password, no_id)
	return songid


def getdistance():

	distance=[]
	#predall=get_content('id1/')
	predall=np.loadtxt('all161.txt')
	pred=get_content('')
	predall=np.array(predall)
	predall=np.reshape(predall,(161,5,5))
	#np.savetxt('all161.txt',predall)
	print('Saved..')
	pred=np.array(pred)
	for ind,i in enumerate(predall):
		dist= np.linalg.norm(pred-i)
		distance.append(dist)
	distanceindex=[]
	for ind,i in enumerate(distance):
		distanceindex.append([ind,i])
	#print(distanceindex)
	distanceindex.sort(key=lambda x:x[1])
	print(distanceindex)
	recomm = []
	for i in range(5):
		recomm.append(distanceindex[i][0])

	# distanceindex=np.array(distanceindex)
	# recomm=distanceindex[:,0][:5]
	print(recomm)
	#for i in recomm:
		#print(len(os.listdir(os.getcwd()+'/utils/dataset/liked/userid/id1/blues')))
		#print(os.listdir(os.getcwd()+'/utils/dataset/liked/userid/id1/blues')[int(i)])
	
	return recomm



	
#print(os.listdir(os.getcwd()+'/utils/dataset/liked/userid/id1/blues'))
# getdistance()



