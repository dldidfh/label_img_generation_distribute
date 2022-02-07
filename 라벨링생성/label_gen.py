import datetime
from config import * # global variables 
from model.video_detect import video_detection
from background_subtractor import BackgroundSub
import os
import cv2
import time
from set_ROI import DrawLineMouseGesture
from set_ROI import ROI_crop

class label_gen():
    def __init__(self, detecting=False, ROI_set=False) -> None:
        self.today_variable = str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(datetime.datetime.today().day)
        self.worker_name = WORKER_NAME
        self.model_path = MODEL_PATH
        self.detecting = detecting
        if detecting == True:
            import tensorflow as tf
            physical_devices = tf.config.list_physical_devices('GPU')
            if physical_devices:
                tf.config.experimental.set_memory_growth(physical_devices[0], True) ##########################################################
            self.model = tf.saved_model.load(self.model_path)

        self.dir_num = 0 + CURRENT_DIR_NUM
        self.image_num = 0 + CURRENT_IMAGE_NUM
        self.output_root_dir = OUTPUT_ROOT_DIR
        self.file_list = self.video_list()
        self.analysis_location = ANALYSIS_LOCATION
        self.ROI_set = ROI_set
        self.poly_list = []

    def data_gen(self):
        BGS = BackgroundSub()
        frame_num = 0
        for file in self.file_list:
            vid = cv2.VideoCapture(file)             
            frame_check = 0
            return_value_check = 0
            while True:
                # time1 = time.time()
                return_value, frame = vid.read()
                frame_check +=1
                if not return_value:
                    return_value_check +=1
                    if return_value_check > 1000:
                        break
                    continue
                elif frame_check >= int(vid.get(cv2.CAP_PROP_FRAME_COUNT)):
                    frame_check = 0
                    break
                if self.ROI_set == True:
                    if self.poly_list == []:
                        self.poly_list, _, _ = DrawLineMouseGesture().draw_line(frame)
                        frame = ROI_crop(frame, self.poly_list)
                    else:
                        frame = ROI_crop(frame, self.poly_list)
                if frame_num % HOW_MANY_FRAME == 0:
                    vue_mean = BGS.execute(frame)
                    if vue_mean > VUE_THREASHOLD:
                        # 
                        if self.image_num % HOW_MANY_IMAGES == 0 or frame_num==0:
                            root_dir_path = self.mkdir()
                        output_path = root_dir_path + self.analysis_location + '_' + str(self.image_num)
                        if self.detecting:
                            boxes, _, classes, resized_frame, pad_size = video_detection('args',frame, self.model)
                            self.txt_save(boxes, output_path, pad_size, classes, resized_frame)
                        cv2.imwrite(output_path+'.jpg', frame)
                        self.image_num +=1   
                        # print("소요시간 : {:.2f}".format(time.time()- time1))             
                frame_num += 1
        # txt 파일 저장 
        with open('./last_file_number.txt','w') as wd:
            string = "{} {}\n{} {}".format("image_num",self.image_num, 'dir_num', self.dir_num)
            wd.write(string)

    def mkdir(self):        
        worker_len = len(self.worker_name)
        worker = self.worker_name[self.dir_num % worker_len] 
        path = OUTPUT_ROOT_DIR + worker + '_' +  self.today_variable + '_' + str(self.dir_num) + '/'
        self.dir_num +=1
        os.makedirs(path, exist_ok=True)
        return path

    def txt_save(self, boxes, output_path, pad_size, classes,resized_frame):

        x_width = pad_size[1] // 2 
        y_width = MODEL_INPUT[0] - pad_size[1] // 2
        x_height = pad_size[0] // 2 
        y_height = MODEL_INPUT[1] - pad_size[0] // 2
        resized_frame = resized_frame[0,x_width:y_width, x_height:y_height,:]        
        resized_size  = resized_frame.shape[:2]

        with open(output_path + '.txt','w') as wd:
            for i, box in enumerate(boxes):

                box[0] = box[0] - pad_size[0]//2
                box[1] = box[1] - pad_size[1]//2
                box[2] = box[2] - pad_size[0]//2
                box[3] = box[3] - pad_size[1]//2
                box_width = box[2] - box[0]
                box_height = box[3] - box[1]    
                center_x = box[2] - box_width//2
                center_y = box[3] - box_height//2

                box_width = box_width / resized_size[1]
                box_height = box_height / resized_size[0]
                center_x = center_x / resized_size[1]
                center_y = center_y / resized_size[0]

                string = "{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(classes[i], center_x, center_y, box_width, box_height)
                wd.write(string)

    def video_list(self):
        video_list = []
        for path in INPUT_PATH:
            for file in os.listdir(path):
                # 조건 추가 해서 해당 시간대 동영상만 불러옴 
                if HAS_TIME_CONDITION :
                    file_name_split_list = file.split('_')
                    root, _ = os.path.splitext(file_name_split_list[2])
                    root = int(root)
                    if root >= REGEX_FLAG[0] or root <= REGEX_FLAG[1]:
                        video_list.append(path+ '/' + file)
                    ##########################################
                else:
                    video_list.append(os.path.join(path, file))

        return video_list

