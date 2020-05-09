'''
foo three
'''

from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, adadelta, rmsprop
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
import cPickle
import numpy as np

dropout = 0.5
weight_init='he_normal'

def foo():

    # Determine proper input shape
	if keras.__version__ > '1.0.3':
		K.common.set_image_dim_ordering('th')
	input_shape = (1, 224, 224)

	#img_input = Input(shape=input_shape)

	model = Sequential()

	model.add(Convolution2D(32, 3, 3,
			        input_shape=input_shape,init=weight_init, name='conv1_1'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(Convolution2D(32, 3, 3,init=weight_init, name='conv1_2'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(dropout))

	model.add(Convolution2D(64, 3, 3,init=weight_init, name='conv2_1'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(Convolution2D(64, 3, 3,init=weight_init, name='conv2_2'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(Convolution2D(64, 3, 3,init=weight_init, name='conv2_3'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))  
	model.add(Dropout(dropout))

	model.add(Convolution2D(128, 3, 3,init=weight_init, name='conv3_1'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(Convolution2D(128, 3, 3,init=weight_init, name='conv3_2'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))  
	model.add(Dropout(dropout))

	model.add(Convolution2D(512, 3,3,init=weight_init, border_mode='same', name='conv4_1'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(Convolution2D(512, 3,3,init=weight_init, border_mode='same', name='conv4_2'))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))  
	model.add(Dropout(dropout))

	model.add(Flatten())
	model.add(Dense(120, init=weight_init))
	model.add(Activation('relu'))
	model.add(Dropout(dropout))

	model.add(Dropout(dropout))
	model.add(Dense(2))
	model.add(Activation('sigmoid'))

	return model


