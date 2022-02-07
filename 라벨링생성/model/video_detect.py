
import tensorflow as tf
import numpy as np
from model.nms import yolov4_nms,NonMaxSuppression
from model.preprocess import resize_img

def detect_batch_img(img,model,args):
    img = img / 255
    img = tf.image.convert_image_dtype(img, tf.float32)
    pre_nms_decoded_boxes, pre_nms__scores = model(img, training=False)
    pre_nms_decoded_boxes = pre_nms_decoded_boxes.numpy()
    pre_nms__scores = pre_nms__scores.numpy()
    boxes, scores, classes, valid_detections = yolov4_nms(args)(pre_nms_decoded_boxes, pre_nms__scores, args)
    return boxes, scores, classes, valid_detections

def tta_nms(boxes,scores,classes,valid_detections,args):
    all_boxes = []
    all_scores = []
    all_classes = []
    batch_index = 0
    valid_boxes = boxes[batch_index][0:valid_detections[batch_index]]
    valid_boxes[:, (0, 2)] = (1.-valid_boxes[:,(2,0)])
    all_boxes.append(valid_boxes)
    all_scores.append(scores[batch_index][0:valid_detections[batch_index]])
    all_classes.append(classes[batch_index][0:valid_detections[batch_index]])
    for batch_index in range(1,boxes.shape[0]):
        all_boxes.append(boxes[batch_index][0:valid_detections[batch_index]])
        all_scores.append(scores[batch_index][0:valid_detections[batch_index]])
        all_classes.append(classes[batch_index][0:valid_detections[batch_index]])
    all_boxes = np.concatenate(all_boxes,axis=0)
    all_scores = np.concatenate(all_scores, axis=0)
    all_classes = np.concatenate(all_classes, axis=0)
    all_boxes,all_scores,all_classes = np.array(all_boxes), np.array(all_scores), np.array(all_classes)
    boxes, scores, classes, valid_detections = NonMaxSuppression.diou_nms_np_tta(np.expand_dims(all_boxes,0),np.expand_dims(all_scores,0),np.expand_dims(all_classes,0),args)
    boxes, scores, classes, valid_detections = np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes), np.squeeze(valid_detections)
    return boxes[:valid_detections], scores[:valid_detections], classes[:valid_detections]



# 이미지 읽어서 불러옴 
def video_detection(args, frame, model):
    
    img_ori,_,pad_size = resize_img(frame, (608,608))
    # aug_imgs = []
    # aug_imgs.append(img_ori)
    batch_img = np.array([img_ori])

    boxes,scores,classes,valid_detections = detect_batch_img(batch_img, model,args)
    boxes, scores, classes = tta_nms(boxes, scores, classes,valid_detections,args)

    # origin_coor_boxes = [[int(box[0]*608),int(box[1]*608), int(box[2]*608), int(box[3]*608)] for box in boxes]
    origin_coor_boxes = [[int(608 - box[2]*608 ),
                          int(box[1]*608 ), 
                          int(608 - box[0]*608 ), 
                          int(box[3]*608 )] 
                          for box in boxes]

    return origin_coor_boxes, scores, classes, batch_img,pad_size