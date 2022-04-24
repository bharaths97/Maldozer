from keras.utils import np_utils
from gensim.models import Word2Vec
from MALDOZER_CONSTANTS import L, K, Word2Vec_Model_Dir, CLASSIFICATIONS, CLASS_LIST, CLASSIFICATIONS_map, append_to_list
import numpy as np

# index of k-fold crossing validation 
def K_FOLD_INDEX(folds, data_size):
	ret_index = []
	step_size = data_size // folds
	for i in range(folds - 1):
		ret_index.append(([[0,i * step_size], [(i + 1) * step_size, data_size]], [[i * step_size, (i + 1) * step_size]], data_size - step_size, step_size))
	ret_index.append(([[0,(folds - 1) * step_size]], [[(folds - 1) * step_size, data_size]], step_size * (folds - 1), data_size - step_size * (folds - 1)))
	return ret_index


def data_for_one_class(path, word2vec_model, class_map_index=0):
	all_data_from_class=[]
	files=append_to_list(all_data_from_class,path, L)
	outputs_to_return=[class_map_index]*len(files)
	inputs_to_return=[]
	for data in all_data_from_class:
		input_per_class=[]
		for item in data:
			try:
				input_per_class.extend(word2vec_model.wv[item])
			except Exception as e:
				print("Exception: ", e)
				continue
		inputs_to_return.extend(input_per_class)
	return inputs_to_return,outputs_to_return,len(files)


def data_for_all_classes (path):
	word2vec_model = Word2Vec.load(Word2Vec_Model_Dir)
	inputs = []
	outputs = []
	total_apks = 0
	for i in range(CLASSIFICATIONS):
		input_from_class, output_from_class, class_data_size = data_for_one_class(path+'/'+CLASS_LIST[i],word2vec_model,CLASSIFICATIONS_map[CLASS_LIST[i]])
		inputs.extend(input_from_class)
		outputs.extend(output_from_class)
		total_apks += class_data_size
	return np.array(inputs).reshape((total_apks, L, K, 1)).astype('float32')/255, np_utils.to_categorical(np.array(outputs).reshape((total_apks, 1)), CLASSIFICATIONS), total_apks


def batches(input, output, search_range, batch_size):
	X=[]
	Y=[]
	monitor_batch_size = 0
	while True:
		for each_range in search_range:
			range_start, range_end = each_range[0], each_range[1]
			for i in range(range_start, range_end):
				monitor_batch_size += 1
				X.append(input[i])
				Y.append(output[i])
				if count == batch_size:
					res = (np.array(X), np.array(Y))
					X = []
					Y = []
					count = 0
					yield(res)
					