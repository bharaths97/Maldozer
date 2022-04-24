import os
import pickle
import random
from MALDOZER_CONSTANTS import L,VERBOSE_LOGGING,Extracted_Features_Dir,Training_Data_Dir,Testing_Data_Dir,api_to_method_id_pickle,CLASSIFICATIONS,CLASS_LIST,file_contents_to_list

def read_pickle_file():
	file=open(api_to_method_id_pickle,'rb')
	ID_mapping_dict=pickle.load(file)
	file.close
	return ID_mapping_dict

def mapping():
	ID_mapping_dict = read_pickle_file()
	for i in range(CLASSIFICATIONS):
		files=os.listdir(Extracted_Features_Dir+'/'+CLASS_LIST[i])
		random.shuffle(files)

		for j in range(len(files)):
			testing_files_path = Testing_Data_Dir+'/'+CLASS_LIST[i]+'/'+files[j]
			training_files_path = Training_Data_Dir+'/'+CLASS_LIST[i]+'/'+files[j]
			if os.path.exists(testing_files_path):
				if VERBOSE_LOGGING:
					print("Mapping file already exists for ", testing_files_path)
				continue
			elif os.path.exists(training_files_path):
				if VERBOSE_LOGGING:
					print("Mapping file already exists for ", training_files_path)
				continue
			to_write=[]
			file_path = Extracted_Features_Dir+'/'+CLASS_LIST[i]+'/'+files[j]
			file_contents=file_contents_to_list(file_path)
			try:
				length_of_file=len(file_contents)
				for k in range(L):
					if (k<length_of_file) and (file_contents[k][:-1] in ID_mapping_dict.keys()):
						file_line=file_contents[k][:-1]
						to_write.append(str(ID_mapping_dict[file_line])+'\n')
					else:
						to_write.append('0\n')
			except:
				print("file contents:",file_contents)
				print("file is empty", file_path)
			
			rand_num = random.random()
			if rand_num < 0.8:
				with open(training_files_path,'w') as file:
					if VERBOSE_LOGGING:
						print("Writing Method to Identifier mapping for: ", training_files_path)
					file.writelines(to_write)
			else:
				with open(testing_files_path,'w') as file:
					if VERBOSE_LOGGING:
						print("Writing Method to Identifier mapping for: ", testing_files_path)
					file.writelines(to_write)
	print("API method to Identifier Mapping Completed")