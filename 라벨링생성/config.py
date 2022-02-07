import os

# 동영상이 들어있는 폴더 상위경로 
ROOT_PATH = 'D:/YoungIn_VDS_VIDEO'

# 해당 이름으로 폴더명과 파일명이 생성됨 
ANALYSIS_LOCATION = 'YoungIn' 

# ROOT_PATH 안에 있는 파일들을 읽어와 리스트에 저장 
INPUT_PATH = []
for file in os.listdir(ROOT_PATH):
    dir_path2 = os.path.join(ROOT_PATH, file)
    for file2 in os.listdir(dir_path2):
        INPUT_PATH.append(os.path.join(dir_path2 , file2) + '/')

# 결과 파일이 저장될 경로              
OUTPUT_ROOT_DIR = './output/'

# 디렉토리 명을 설정하고 싶을 때 설정 
WORKER_NAME = ['worker1'] #['worker1', 'worker2', 'worker3']

# ROI를 설정하여 해당 영역만 crop 
ROI_SET = True

HOW_MANY_IMAGES = 350 # 하나의 디렉토리에 몇장의 이미지를 넣을것인지 
HOW_MANY_FRAME = 90   # 몇 프레임당 이미지 저장할 것인지 

# 차영상 기법을 사용하여 동적 객체가 있을 때만 이미지 crop
VUE_THREASHOLD = 10

# 이전의 생성기록을 저장하여 해당 파일이름 다음부터 저장되도록 설정 ( 1.jpg가 저장된 후 다시 돌리면 txt에 2가 저장되어있어 2.jpg부터 생성)
with open('./last_file_number.txt', 'r') as rd:
    lines = rd.readlines()
    CURRENT_IMAGE_NUM = int(lines[0].strip().split()[-1]) + 1
    CURRENT_DIR_NUM = int(lines[1].strip().split()[-1] ) 

# 영상의 이름이 시간으로 되어있을 때 불러오는 설정 
HAS_TIME_CONDITION = False
REGEX_FLAG = [180000, 60000]


# 검출 모델 관련 설정 
MODEL_PATH = './model/best_model_p5_252_0.682/1'
MODEL_INPUT = (608,608)