from .models import Detections
import cv2
import numpy as np
import math
from .tracker import *

tracker = EuclideanDistTracker() 

count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0


class VideoCamera:
    def __init__(self):
        self.tracker = EuclideanDistTracker()
        self.count = 0
        self.center_points_prev_frame = []
        self.tracking_objects = {}
        self.track_id = 0
        self.video = cv2.VideoCapture(0)
        self.confidenceThreshold = 0.5
        self.NMSThreshold = 0.3
        self.modelConfiguration = 'cfg/yolov3.cfg'
        self.modelWeights = 'yolov3.weights'
        self.labelsPath = 'coco.names'
        self.labels = open(self.labelsPath).read().strip().split('\n')
        self.COLORS = np.random.randint(
            0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.net = cv2.dnn.readNetFromDarknet(
            self.modelConfiguration, self.modelWeights)
        self.outputLayer = self.net.getLayerNames()
        self.outputLayer = [self.outputLayer[i - 1]
                            for i in self.net.getUnconnectedOutLayers()]
        
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        
        global track_id
        global center_points_prev_frame
        global count
       
        
        (W, H) = (None, None)
        ret, frame = self.video.read()
        count += 1
        frame = cv2.flip(frame, 1)
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        center_points_cur_frame = []

        blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layersOutputs = self.net.forward(self.outputLayer)

        
        boxes = []
        confidences = []
        classIDs = []
        

        for output in layersOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > self.confidenceThreshold:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY,  width, height) = box.astype('int')
                        x = int(centerX - (width/2))
                        y = int(centerY - (height/2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

                # Apply Non Maxima Suppression
                detectionNMS = cv2.dnn.NMSBoxes(
                    boxes, confidences,self.confidenceThreshold, self.NMSThreshold)
                if (len(detectionNMS) > 0):
                    for i in detectionNMS.flatten():
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])

                        cx = int((x + x + w) / 2)
                        cy = int((y + y + h) / 2)

                        center_points_cur_frame.append((cx,cy))

                        color = [int(c) for c in self.COLORS[classIDs[i]]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        text = '{}: {:.4f}'.format(self.labels[classIDs[i]], confidences[i])
                        cv2.putText(frame, text, (x, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Count the number of detected vehicles
                    
                    count_str = "Count: {}".format(len(tracking_objects))
                    cv2.putText(frame, count_str, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                   
                    if count <= 2:
                        for pt in center_points_cur_frame:
                            for pt2 in center_points_prev_frame:
                                distance = math.hypot(pt2[0]-pt[0], pt2[1]- pt[1])
                
                                if distance < 20: 
                                    tracking_objects[track_id] = pt
                                    track_id += 1
                    else:
        
                        tracking_objects_copy = tracking_objects.copy()
                        center_points_cur_frame_copy = center_points_cur_frame.copy()
        
                        for object_id, pt2 in tracking_objects_copy.items():
                            object_exists = False
                            for pt in center_points_cur_frame_copy:
            
                                distance = math.hypot(pt2[0]-pt[0], pt2[1]- pt[1])
                
                                if distance < 20:
                                    tracking_objects[object_id] = pt
                                    object_exists = True
                                    if pt in center_points_cur_frame:
                                        center_points_cur_frame.remove(pt)
                                    else:
                                         print("Point not found in list.")
                                    continue
                    
                            if not object_exists:
                                tracking_objects.pop(object_id)
    
                        for pt in center_points_cur_frame:
                            tracking_objects[track_id] = pt
                            track_id += 1
    
                    for object_id, pt in tracking_objects.items():
                        cv2.circle(frame, pt, 5, (0,0,255), -1)
                        cv2.putText(frame, "", (pt[0], pt[1] - 7),0, 1, (0,0,255), 2)
                        
                    def gen(camera):
                        while True:
                            frame = camera.get_frame()
                            yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

               
                    print("Tracking Objects")  
                    print(tracking_objects)
                    
                    
                    count_int = int(count_str.split(":")[1])
                    print(count_str)
                    print(text)

                                  
                        

                    # Sending data to model file so data can be saved to database
                    data =Detections(text=text, count_str=count_int)
                    data.save()

                    # print("CUR FRAME LEFT PTS")
                    # print(center_points_cur_frame)
                
                    cv2.imshow('Output', frame)
                    center_points_prev_frame = center_points_cur_frame.copy()
                    if (cv2.waitKey(1) & 0xFF == ord('q')):
                        break
        
        # Your provided code for object detection goes here
        
        


    
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
     
  