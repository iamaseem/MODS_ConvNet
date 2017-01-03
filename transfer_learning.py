# -*- coding: utf-8 -*-
'''
Transfer learning from pre-trained network
'''

import keras
from keras.applications.inception_v3 import InceptionV3
from keras.optimizers import SGD, adadelta, rmsprop, adam, nadam
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils

import cPickle
import numpy as np

import getpass
username = getpass.getuser()


def get_data(n_dataset):    
    f = file('MODS_dataset_cv_{0}.pkl'.format(n_dataset),'rb')
    data = cPickle.load(f)
    f.close()
    training_data = data[0]
    validation_data = data[1]
    t_data = training_data[0]
    t_label = training_data[1]
    v_data = validation_data[0]
    v_label = validation_data[1]
    
    t_data = np.array(t_data)
    t_label = np.array(t_label)
    v_data = np.array(v_data)
    v_label = np.array(v_label)
    t_data = t_data.reshape(t_data.shape[0], 1, 256, 192)
    v_data = v_data.reshape(v_data.shape[0], 1, 256, 192)
    
    #less precision means less memory needed: 64 -> 32 (half the memory used)
    t_data = t_data.astype('float32')
    v_data = v_data.astype('float32')
    
    return (t_data, t_label), (v_data, v_label)

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        
nb_classes = 2
nb_epoch = 100
data_augmentation = True
n_dataset = 5

#Hyperparameters for tuning
#weight_init = 'he_normal' #['glorot_normal']
#regl1 = [1.0, 0.1, 0.01, 0.001, 0.0]
#regl2 = [1.0, 0.1, 0.01, 0.001, 0.0]
dropout = 0.5 #[0.0, 0.25, 0.5, 0.7]
batch_size = 40 #[32, 70, 100, 150]
#learning_rate = 0.003 #[0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3]
optimizer = 'rmsprop' #['sgd', 'adadelta']

base_model = InceptionV3(weights='imagenet', include_top=False)

x = base_model.output
x = Dense(1024, activation='relu')(x)
predictions = Dense(nb_classes, activation='softmax')(x)
model = Model(input=base_model.input, output=predictions)

for i in xrange(n_dataset):
    # the data, shuffled and split between train and test sets
    (X_train, y_train), (X_test, y_test) = get_data(i)
    print('X_train shape:', X_train.shape)
    print(X_train.shape[0], 'train samples')
    print(X_test.shape[0], 'test samples')
    
    # convert class vectors to binary class matrices
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)

    history = LossHistory()

    X_train /= 255
    X_test /= 255
    
    #data augmentation generator for training, with desired settings
    datagen = ImageDataGenerator(
	featurewise_center=False,  # set input mean to 0 over the dataset
	samplewise_center=False,  # set each sample mean to 0
	featurewise_std_normalization=False,  # divide inputs by std of the dataset
	samplewise_std_normalization=False,  # divide each input by its std
	zca_whitening=False,  # apply ZCA whitening
	#rotation_range=180,  # randomly rotate images in the range (degrees, 0 to 180)
	width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
	height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
	horizontal_flip=True,  # randomly flip images
	vertical_flip=True,  # randomly flip images
	fill_mode='nearest')  
    datagen.fit(X_train)

    #data augmentation generator for testing
    test_datagen = ImageDataGenerator(
	featurewise_center=False, 
	samplewise_center=False,
	featurewise_std_normalization=False, 
	samplewise_std_normalization=False,
	zca_whitening=False,
	#rotation_range=180,
	width_shift_range=0.1,
	height_shift_range=0.1,
	horizontal_flip=True,
	vertical_flip=True,
	fill_mode='nearest')  
    test_datagen.fit(X_test)

    #Shows all layers and names
    for i, layer in enumerate(model.layers):
	print(i, layer.name)

    #Train FC layers first
    for layer in base_model.layers:
    	layer.trainable = False

    model.compile(optimizer=rmsprop(lr=0.005),
		 loss='binary_crossentropy')
                 metrics=['accuracy'])
                     
    print('Using real-time data augmentation.')

    # fit the model on the batches generated by datagen.flow()
    model.fit_generator(datagen.flow(X_train, Y_train,
            batch_size=batch_size),
            samples_per_epoch=X_train.shape[0],
            nb_epoch=nb_epoch, #maybe I should change this or increase lr 
            validation_data=test_datagen.flow(X_test, Y_test, batch_size=batch_size),
	    nb_val_samples=X_test.shape[0])
    
    print('Finished training FC layers')

    # Now train convolutional layers

    for layer in model.layers[:172]:
	   layer.trainable = False
    for layer in model.layers[172:]:
	   layer.trainable = True
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), 
		 loss='binary_crossentropy')
                 metrics=['accuracy'])


    print('Using real-time data augmentation.')

    # fit the model on the batches generated by datagen.flow()
    model.fit_generator(datagen.flow(X_train, Y_train,
            batch_size=batch_size),
            samples_per_epoch=X_train.shape[0],
            nb_epoch=nb_epoch,
            validation_data=test_datagen.flow(X_test, Y_test, batch_size=batch_size),
	    nb_val_samples=X_test.shape[0])

    print('Finished training convolutional layers')
        

    # Now all layers
    for layer in model.layers:
	layer.trainable = True

    model.compile(optimizer='rmsprop',
		 loss='binary_crossentropy')
                 metrics=['accuracy'])

    print('Using real-time data augmentation.')

    # fit the model on the batches generated by datagen.flow()
    model.fit_generator(datagen.flow(X_train, Y_train,
            batch_size=batch_size),
            samples_per_epoch=X_train.shape[0],
            nb_epoch=nb_epoch,
            validation_data=test_datagen.flow(X_test, Y_test, batch_size=batch_size),
	    nb_val_samples=X_test.shape[0])

    print('Finished training network.')
                    
    score = model.evaluate(X_test, Y_test, verbose=1)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    name = 'MODS_transfer_learning_weights_{0}_{1}_{2}_{3}_{4}.h5'.format(i, dropout, optimizer, batch_size,username)
    model.save_weights(name,overwrite=True)
    print('weights saved')

model.reset_states()

#import matplotlib.pylab as plt
#plt.plot(history.losses,'bo')
#plt.xlabel('Iteration')
#plt.ylabel('loss')
#plt.show()
