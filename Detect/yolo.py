import cv2
import numpy as np
from .models import Detection



# class YOLO:
#     def __init__(self):
#         self.weights_path = 'yolov3.weights'
#         self.config_path = 'cfg/yolov3.cfg'
#         self.labels_path = 'coco.names'

#         self.labels = open(self.labels_path).read().strip().split('\n')
#         self.net = cv2.dnn.readNetFromDarknet(
#             self.config_path, self.weights_path)

#     def detect_objects(self, frame):
#         blob = cv2.dnn.blobFromImage(
#             frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         self.net.setInput(blob)
#         layer_outputs = self.net.forward(self.get_output_layers())

#         return layer_outputs

#     def get_output_layers(self):
#         layer_names = self.net.getLayerNames()
#         output_layers = [layer_names[i - 1]
#                          for i in self.net.getUnconnectedOutLayers()]

#         return output_layers


# class VideoCamera:
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         self.yolo = YOLO()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret, frame = self.video.read()
#         layer_outputs = self.yolo.detect_objects(frame)

#         # Process the layer outputs and draw bounding boxes, labels, etc. on the frame

#         ret, jpeg = cv2.imencode('.jpg', frame)
#         return jpeg.tobytes()


class VideoCamera:
    def __init__(self):
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
        (W, H) = (None, None)
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        if W is None or H is None:
            (H, W) = frame.shape[:2]
            
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

                        color = [int(c) for c in self.COLORS[classIDs[i]]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        text = '{}: {:.4f}'.format(self.labels[classIDs[i]], confidences[i])
                        cv2.putText(frame, text, (x, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        if confidence > self.confidenceThreshold:
                            # ...
                            # After the detection is made:
                            detection = Detection(
                                label=self.labels[classID], confidence=float(confidence))
                            detection.save()

                cv2.imshow('Output', frame)
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    break
                

               
        
        # Your provided code for object detection goes here

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
    




