import datetime

# 한 디렉토리에 몇장의 이미지 분배할것인지 
DIR_PER_IMAGE = 100 
# 입력 이미지 경로 
DIR_PATH = 'E:/pri_work/work_10/image_gen/labeling_data_gen/output'
# 섞을것인지 
SHUFFLE = True 

# 특정 개수만큼만 이동시키고  그만할 때 설정
STOP = True
STOP_COUNT = 400 # 총 몇개 분배할 것인지 

# 저장 디렉토리 경로 
SAVE_DIR = './outputs/'
# 저장 디렉토리 이름 ( 파일이름은 기존 파일이름 그대로 사용 )
SAVA_DIR_NAME = 'YongIn_{}'.format(str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(datetime.datetime.today().day))
