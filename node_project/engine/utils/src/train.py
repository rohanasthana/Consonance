import gc
import os
import ast
import sys
import configparser
import tensorflow as tf

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import keras
from keras import backend as K

from audiomanip.audiostruct import AudioStruct
from audiomanip.audiomodels import ModelZoo
from audiomanip.audioutils import AudioUtils
from audiomanip.audioutils import MusicDataGenerator


os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
def freeze_session(session, keep_var_names=None, output_names="dense_15/Softmax:0", clear_devices=True):

    
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph

def main():

  config = configparser.ConfigParser()
  config.read('params.ini')

  GTZAN_FOLDER = config['FILE_READ']['GTZAN_FOLDER']
  MODEL_PATH = config['FILE_READ']['SAVE_MODEL']
  SAVE_NPY = ast.literal_eval(config['FILE_READ']['SAVE_NPY'])
  EXEC_TIMES = int(config['PARAMETERS_MODEL']['EXEC_TIMES'])
  CNN_TYPE = config['PARAMETERS_MODEL']['CNN_TYPE']


  batch_size = int(config['PARAMETERS_MODEL']['BATCH_SIZE'])
  epochs = int(config['PARAMETERS_MODEL']['EPOCHS'])

  if not ((CNN_TYPE == '1D') or (CNN_TYPE == '2D')):
    raise ValueError('Argument Invalid: The options are 1D or 2D for CNN_TYPE')


  data_type = config['FILE_READ']['TYPE']
  input_shape = (180, 180)
  print("data_type: %s" % data_type)


  if data_type == 'AUDIO_FILES':
    song_rep = AudioStruct(GTZAN_FOLDER)
    songs, genres = song_rep.getdata()


    if SAVE_NPY:
      np.save(GTZAN_FOLDER + 'songs.npy', songs)
      np.save(GTZAN_FOLDER + 'genres.npy', genres)

  elif data_type == 'NPY':
    songs = np.load(GTZAN_FOLDER + 'songs.npy')
    genres = np.load(GTZAN_FOLDER + 'genres.npy')

  else:
    raise ValueError('Argument Invalid: The options are AUDIO_FILES or NPY for data_type')

  print("Original songs array shape: {0}".format(songs.shape))
  print("Original genre array shape: {0}".format(genres.shape))


  val_acc = []
  test_history = []
  test_acc = []
  test_acc_mvs = []
  
  

  for x in range(EXEC_TIMES):

    X_train, X_test, y_train, y_test = train_test_split(
      songs, genres, test_size=0.1, stratify=genres)
    

    X_train, X_Val, y_train, y_val = train_test_split(
      X_train, y_train, test_size=1/6, stratify=y_train)
    print(y_train.shape)
        

    X_Val, y_val = AudioUtils().splitsongs_melspect(X_Val, y_val, CNN_TYPE)
    X_test, y_test = AudioUtils().splitsongs_melspect(X_test, y_test, CNN_TYPE)
    X_train, y_train = AudioUtils().splitsongs_melspect(X_train, y_train, CNN_TYPE)
    print(y_train.shape)

    if CNN_TYPE == '1D':
      cnn = ModelZoo.cnn_melspect_1D(input_shape)
    elif CNN_TYPE == '2D':
      cnn = ModelZoo.cnn_melspect_2D(input_shape)

    print("\nTrain shape: {0}".format(X_train.shape))
    print("Validation shape: {0}".format(X_Val.shape))
    print("Test shape: {0}\n".format(X_test.shape))
    print("Size of the CNN: %s\n" % cnn.count_params())
    

    sgd = keras.optimizers.SGD(lr=0.001, momentum=0.9, decay=1e-5, nesterov=True)
    adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-5)
    

    cnn.compile(loss=keras.losses.categorical_crossentropy,
      optimizer=sgd,
      metrics=['accuracy'])


    earlystop = keras.callbacks.EarlyStopping(monitor='val_loss',
      min_delta=0,
      patience=2,
      verbose=0,
      mode='auto')


    history = cnn.fit(X_train, y_train,
      batch_size=batch_size,
      epochs=epochs,
      verbose=1,
      validation_data=(X_Val, y_val))

    score = cnn.evaluate(X_test, y_test, verbose=0)
    score_val = cnn.evaluate(X_Val, y_val, verbose=0)
        

    pred_values = np.argmax(cnn.predict(X_test), axis = 1)
    mvs_truth, mvs_res = AudioUtils().voting(np.argmax(y_test, axis = 1), pred_values)
    acc_mvs = accuracy_score(mvs_truth, mvs_res)


    val_acc.append(score_val[1])
    test_acc.append(score[1])
    test_history.append(history)
    test_acc_mvs.append(acc_mvs)


    print('Test accuracy:', score[1])
    print('Test accuracy for Majority Voting System:', acc_mvs)

    cm = confusion_matrix(mvs_truth, mvs_res)
    print(cm)

  print("Validation accuracy - mean: %s, std: %s" % (np.mean(val_acc), np.std(val_acc)))
  print("Test accuracy - mean: %s, std: %s" % (np.mean(test_acc), np.std(test_acc)))
  print("Test accuracy MVS - mean: %s, std: %s" % (np.mean(test_acc_mvs), np.std(test_acc_mvs)))

  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  cnn.save(MODEL_PATH)

  del songs
  del genres
  gc.collect()
  frozen_graph = freeze_session(K.get_session(),
                              output_names=[out.op.name for out in cnn.outputs])
  tf.train.write_graph(frozen_graph, "../models", "my_model.pb", as_text=False)
  

if __name__ == '__main__':
  main()

