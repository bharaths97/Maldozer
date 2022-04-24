import os

CLASSIFICATIONS = 5
CLASS_LIST=["Benign","Adware","Banking","Riskware","SMS"]
CLASSIFICATIONS_map={CLASS_LIST[i]:i for i in range(CLASSIFICATIONS)}


APK_Files_Dir ='../Maldozer/Resources/APK Files'
Extracted_Features_Dir='../Maldozer/Resources/APIs and Features'
api_to_method_id_pickle='../Maldozer/Resources/API_to_ID.pickle'
Word2Vec_Files_Dir='../Maldozer/Resources/Word2Vec Files'
Word2Vec_Model_Dir='../Maldozer/Resources/Word2Vec Files/word2vec_normalized.model'
Mapping_Method_to_ID_path='../Maldozer/Resources/Methods Mapping'
Training_Data_Dir='../Maldozer/Resources/Methods Mapping/Testing Data'
Testing_Data_Dir='../Maldozer/Resources/Methods Mapping/Training Data'
Unique_APIs_Dir ='../Maldozer/Resources/uniqueAPIs.features'
Final_Model_Dir = '../Maldozer/MalDozer.model'


def create_required_directories(path_to_make):
	if os.path.exists(path_to_make):
		print(path_to_make,"already exists")
	else:
		os.makedirs(path_to_make)
		print(path_to_make,"created")

def file_contents_to_list(path,L=-1):
	with open(path,encoding='ISO-8859-1') as file:
		try:
			file_lines_list = file.readlines()
			if L != -1:
				lens=len(file_lines_list)
				if L <= lens:
					file_lines_list=file_lines_list[:L]
				else:
					file_lines_list.extend(['0\n']*(L-lens))
			return file_lines_list
		except Exception as e:
			print("Issue in reading : ", path)
			print("Exception: ", e)

def append_to_list(needed_list,path,L=-1):
	files_in_dir=os.listdir(path)
	for i in range(len(files_in_dir)):
		needed_list.append(file_contents_to_list(path+'/' + files_in_dir[i],L))
	return files_in_dir

#logging level
VERBOSE_LOGGING = 1

#dimensions for vector of size L x K
K = 64 #as set by the authors
L = 2500 #Own Discression

#K-Fold Cross Validation (Can range anywhere from the set of 2,3,5,10). Using 
k_fold_cross_val = True
k_fold_cross_val_folds = 5

#Setting Training Parameters 
maxpooling_size = (3,3) #own discression
batch_size = 10 #own discression
filter_count = 512 #as done by authors
kernel_size = 3 #as done by authors
dropout = 0.5 #as done by authors
epochs = 10 #as done by authors for the datasets
test_split_percent = 0.1 #will be used if K-fold cross validation is not enabled
validation_split_percent = 0.2 #will be used if K-fold cross validation is not enabled
neuron_count = 256 #as done by authors