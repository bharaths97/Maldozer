from gensim.test.utils import get_tmpfile
from gensim.models import word2vec
import os
from MALDOZER_CONSTANTS import K, VERBOSE_LOGGING,Training_Data_Dir,Testing_Data_Dir,Word2Vec_Model_Dir,CLASS_LIST,CLASSIFICATIONS, file_contents_to_list

def normalize_words():
	Mapping_words=[]
	for i in range (CLASSIFICATIONS):
		if VERBOSE_LOGGING:
			print("Mapping words list started for",CLASS_LIST[i],"class of APKs")
		files_testing = os.listdir(Testing_Data_Dir+"/"+CLASS_LIST[i])
		files_training = os.listdir(Training_Data_Dir+"/"+CLASS_LIST[i])
		no_test_files = len(files_testing)
		no_train_files = len(files_training)
		for j in range(no_test_files):
			testing_files_path = Testing_Data_Dir+'/'+CLASS_LIST[i]+'/'+files_testing[j]
			Mapping_words.append(file_contents_to_list(testing_files_path))
		for j in range(no_train_files):
			training_files_path = Training_Data_Dir+'/'+CLASS_LIST[i]+'/'+files_training[j]
			Mapping_words.append(file_contents_to_list(training_files_path))
		if VERBOSE_LOGGING:
			print("Mapping words list completed for",CLASS_LIST[i],"class of APKs")
	
	print("Starting Word2Vec function")
	#if hs is 1 Hierarchical Softmax is used otherwise Negative sampling is used window=15
	get_tmpfile(Word2Vec_Model_Dir)
	model = word2vec.Word2Vec(Mapping_words, window=4, hs=1, min_count=1, vector_size=K)
	model.save(Word2Vec_Model_Dir)
	if VERBOSE_LOGGING:
			print("Creating Word2Vec's model file")
	print("Word to vector normalization completed")