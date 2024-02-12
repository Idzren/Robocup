import cv2
import numpy as np

# Use webcam, change 0 to the index of your webcam (it might be 1, 2, etc.)
cap = cv2.VideoCapture(0)
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = 'coco.names'
classNames = []

with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObject(outputs, im):
    hT, wT, cT = im.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    print(indices)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        
        if classNames[classIds[i]] == 'person':
        	cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
        	cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        	print('person')
        	
        if classNames[classIds[i]] == 'diningtable':
        	cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
        	cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        	print('table')
        
        if classNames[classIds[i]] == 'chair':
        	cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
        	cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        	print('chair')
        
        
while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()

    # Resize the frame to the specified dimensions for processing
    frame = cv2.resize(frame, (whT, whT))

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)

    # Set the blob as input to the network
    net.setInput(blob)

    # Get the names of the output layers
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Forward pass through the network
    outputs = net.forward(outputNames)

    # Process the outputs and draw bounding boxes on the frame
    findObject(outputs, frame)

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
