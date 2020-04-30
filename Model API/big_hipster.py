# -*- coding: utf-8 -*-
'''
Getting hip and trying the Keras Functional API implementation of my Cifar10 code. 
'''
from __future__ import print_function
from __future__ import absolute_import

import warnings
import keras
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D, SpatialDropout2D
from keras import backend as K
from keras.utils import np_utils

def cifar(): #maybe change border mode, idk; also maybe add BatchNormalization(axis=1)

    # Determine proper input shape
    K.common.set_image_dim_ordering('th')
    input_shape = (1, 256, 192)
    img_input = Input(shape=input_shape)

    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='conv1_1')(img_input)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='conv1_2')(x)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='conv1_3')(x)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='conv1_4')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool1')(x)
    x = Dropout(0.25)(x)

    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='conv2_1')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='conv2_2')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='conv2_3')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='conv2_4')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool2')(x)
    x = Dropout(0.25)(x)

    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='conv3_1')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='conv3_2')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='conv3_3')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='conv3_4')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='conv3_5')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool3')(x)
    x = Dropout(0.25)(x)

    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_3')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_4')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_5')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='conv4_6')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='pool4')(x)
    x = Dropout(0.25)(x)

    x = Flatten(name='flatten')(x)
    x = Dense(1000, activation='relu', name='fc1')(x)
    x = Dropout(0.5)(x)
    x = Dense(1000, activation='relu', name='fc2')(x)
    x = Dropout(0.5)(x)
    x = Dense(2, activation='softmax', name='pred')(x)

    # Create model.
    model = Model(img_input, x)

    #weights=''
    #model.load_weights(weights)

    return model


