import os 
import shutil 
import random 
from config import *

dir_list = os.listdir(DIR_PATH)
path_list = []
image_file_list = []
for dirs in dir_list:
    path_list.append( os.path.join(DIR_PATH, dirs))

for path in path_list:
    for image_name in os.listdir(path):
        image_file_list.append(os.path.join(path,image_name))

if SHUFFLE:
    random.shuffle(image_file_list)

dir_count = 0
image_count = 0
while True:
    if image_count % DIR_PER_IMAGE == 0:
        dir_count +=1
    image_save_path = './outputs/' + SAVA_DIR_NAME + '_{}'.format(dir_count)
    if os.path.exists(image_save_path) == False :
        os.mkdir(image_save_path)

    root, child = os.path.splitext( image_save_path)

    shutil.move(image_file_list[image_count], image_save_path) 
    # shutil.copy(image_file_list[image_count], image_save_path) 
    image_count +=1

    if STOP:
        if STOP_COUNT == image_count:break
    else:
        if image_count >= len(image_file_list): break
    
        

