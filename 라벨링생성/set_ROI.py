import cv2 
import numpy as np 

class DrawLineMouseGesture():
    def __init__(self) -> None:
        self.is_dragging = False
        self.is_drawing = False
        # self.x0, self.y0, self.w0, self.h0 = -1, -1, -1, -1
        self.point_list = []
        self.poly_list = []
        self.img_draw = []
        self.image_name = 'images'

    def left_button_down(self, x, y):
        self.is_dragging = True
        self.point_list.append(tuple((x,y)))

    def mouse_move(self, x, y, img):
        if self.is_dragging:
            if len(self.point_list) != 4:
                self.img_draw = img.copy()
                if len(self.point_list) >= 2:
                    for index, point in enumerate(self.point_list):
                        if index != 0:
                            cv2.line(self.img_draw, (self.point_list[index][0], self.point_list[index][1]), (self.point_list[index-1][0], self.point_list[index-1][1]), 255, 2)
                # 이미 그려진 선이 있으면 화면에 표시함 
                if len(self.poly_list) > 0:
                    for poly_list in self.poly_list:
                        # 첫 점과 마지막 점 이어서 사각형 만듬 
                        cv2.line(self.img_draw, poly_list[0], poly_list[-1], 255, 2)
                        for index in range(len(poly_list)-1):
                            # 첫점부터 다음점으로 직선 그림 
                            cv2.line(self.img_draw, poly_list[index], poly_list[index+1], 255, 2)
                #첫 점에서 다음점, 다음점에서 첫점 계속 그림 
                cv2.line(self.img_draw, (self.point_list[0][0], self.point_list[0][1]), (x, y), 255, 2)
                cv2.line(self.img_draw, (self.point_list[-1][0], self.point_list[-1][1]), (x,y), 255, 2)
                cv2.imshow(self.image_name, self.img_draw)
            else:
                # 사각형이 그려지기 위한 4개의 점이 찍혔다면 해당 4개점을 리스트에 저장하고 초기화함 
                self.is_dragging = False
                self.poly_list.append(self.point_list)
                self.point_list = []

    def right_button_down(self):
        self.is_dragging = False
        self.poly_list.append(self.point_list)
        self.point_list = []

    def onMouse(self, event, x, y, flags, param):
        img = param
        if event == cv2.EVENT_LBUTTONDOWN:
            self.left_button_down(x,y)
        elif event == cv2.EVENT_MOUSEMOVE:
            self.mouse_move(x,y,img)
        
    def draw_line(self, frame):
        cv2.imshow(self.image_name,frame)
        cv2.moveWindow(self.image_name, 0, 0)
        cv2.setMouseCallback(self.image_name, self.onMouse, frame)
        key_input = cv2.waitKey()
        cv2.destroyAllWindows()
    
        return self.poly_list, key_input, frame

def ROI_crop(frame, poly_list):
    for index, poly_points in enumerate(poly_list):
        poly_points = np.array(poly_points, np.int32)

        # x,y,w,h = cv2.boundingRect(poly_points)

        # ROI_poly_point = poly_points - poly_points.min(axis=0) 
        h,w = frame.shape[:2]
        mask = np.zeros((h,w), np.uint8)   
        cv2.drawContours(mask, [poly_points], -1, 255, -1) 
        mask = np.stack((mask,)*3,axis=-1)
        masked_ROI = cv2.bitwise_and(frame, mask)
    return masked_ROI


    