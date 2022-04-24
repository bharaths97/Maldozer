from keras import layers
from keras.optimizers import rmsprop_v2
from keras.backend import clip,round,sum,epsilon
from keras.models import Sequential

import random
import numpy as np
import matplotlib.pyplot as plt

from MALDOZER_CONSTANTS import Testing_Data_Dir,Training_Data_Dir,Final_Model_Dir
from MALDOZER_CONSTANTS import CLASSIFICATIONS,L,K,k_fold_cross_val,k_fold_cross_val_folds
from MALDOZER_CONSTANTS import filter_count,kernel_size,neuron_count,dropout,epochs,batch_size,maxpooling_size, test_split_percent, validation_split_percent
from Deep_Learning_Model_Utils import batches,data_for_all_classes,K_FOLD_INDEX

def recall_m(y_true, y_pred):
    true_positives = sum(round(clip(y_true * y_pred, 0, 1)))
    possible_positives = sum(round(clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + epsilon())
    return recall
       
def precision_m(y_true, y_pred):
    true_positives = sum(round(clip(y_true * y_pred, 0, 1)))
    predicted_positives = sum(round(clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+epsilon()))

def deep_learning():
	
	training_input,training_output,training_APKs = data_for_all_classes(Training_Data_Dir)
	testing_input,testing_output,testing_APKs = data_for_all_classes(Testing_Data_Dir)
	total_APKs = training_APKs + testing_APKs
	seed = random.random()

	random.seed(seed)
	all_inputs = np.vstack((training_input, testing_input))
	random.shuffle(all_inputs)

	random.seed(seed)
	all_outputs = np.vstack((training_output, testing_output))
	random.shuffle(all_outputs)
	print("Initialized relevant sizes and data for input & output")

	#Splitting dataset for training, testing and Validation based on K-fold cross validation settings
	testing_data_size  = int(total_APKs * test_split_percent)
	validation_data_size = int(total_APKs * validation_split_percent)
	if k_fold_cross_val:
		training_data_size = total_APKs-testing_data_size
		training_input, training_output = all_inputs[testing_data_size:], all_outputs[testing_data_size:]
		testing_input, testing_output = all_inputs[:testing_data_size], all_outputs[:testing_data_size]
		
	else:
		training_data_size = total_APKs-testing_data_size-validation_data_size
		validation_input, validation_output = all_inputs[:validation_data_size], all_outputs[:validation_data_size]
		testing_input, testing_output = all_inputs[total_APKs - testing_data_size:total_APKs], all_outputs[total_APKs - testing_data_size:total_APKs]
		training_input, training_output = all_inputs[validation_data_size: total_APKs - testing_data_size], all_outputs[validation_data_size: total_APKs - testing_data_size]

	print("Dataset splitting completed")

	#CNN
	model = Sequential()
	print("Model initialized")
	model.add(layers.Conv2D(activation='relu',input_shape=(L , K, 1),filters=filter_count, kernel_size=kernel_size))
	model.summary()

	model.add(layers.MaxPooling2D(maxpooling_size))
	model.add(layers.Flatten())
	model.summary()

	#Populating Layer
	model.add(layers.Dense(activation='relu', units=neuron_count))
	model.summary()

	model.add(layers.Dropout(dropout))
	model.summary()

	#populating Layer
	model.add(layers.Dense(activation='softmax',units=CLASSIFICATIONS))
	model.summary()

	model.compile(optimizer=rmsprop_v2(learning_rate=1e-4),metrics=['acc', f1_m],loss='binary_crossentropy')
	print("Model compiled")

	if k_fold_cross_val:
		for i in K_FOLD_INDEX(k_fold_cross_val_folds, training_data_size):
			model_fitting_out = model.fit_generator(batches(training_input, training_output, i[0], batch_size),
			steps_per_epoch=int(i[2] / batch_size),
			epochs=epochs,
			validation_data=batches(training_input, training_output, i[1], 1),
			validation_steps=int(i[3] / 1),
			verbose=2)
	else:
		model_fitting_out = model.fit_generator(batches(training_input, training_output, [[0,training_data_size]], batch_size),
		steps_per_epoch=int(training_data_size / batch_size),
		epochs=epochs,
		validation_data=batches(validation_input, validation_output, [[0, validation_data_size]], 1),
		validation_steps=int(validation_data_size / 1),
		verbose=2)
	model.save(Final_Model_Dir)

	print("Model fitted and saved")

	# Data for plotting
	accuracy = model_fitting_out.history['accuracy']
	loss = model_fitting_out.history['loss']
	validation_accuracy = model_fitting_out.history['val_accuracy']
	validation_loss = model_fitting_out.history['val_loss']
	epochs_plot = range(len(accuracy))

	plt.plot(epochs_plot, accuracy, 'bo', label='Training accuracy')
	plt.plot(epochs_plot, validation_accuracy, 'b', label='Validation accuracy')
	plt.title('Accuracy of training and validation in model')
	plt.legend()

	plt.figure()

	plt.plot(epochs_plot, loss, 'bo', label='Training loss')
	plt.plot(epochs_plot, validation_loss, 'b', label='Validation loss')
	plt.title('Loss of training and validation in model')
	plt.legend()
	
	testing_loss, testing_accuracy = model.evaluate_generator(batches(testing_input, testing_output, [[0, testing_data_size]], batch_size), steps=int(testing_data_size / batch_size))
	print('Testing accuracy:', testing_accuracy)
	print('Testing loss:', testing_loss)

	plt.show()
	print("Having finished fourth stop:deep learning!")

deep_learning()