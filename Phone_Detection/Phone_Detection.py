import cv2
import RPi.GPIO as GPIO
import time

pin1  = 16#Y-
pin2 = 18#18 Y+

pin3 = 24 #X+
pin4 = 22#A1 X-

Xpos1 = 680
Xpos2 = 680
Ypos1 = 330
Ypos2 = 3390

fcount = 0
Xdiff = 0
Ydiff = 0
center1 = 0
center2 = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin1,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(pin3,GPIO.OUT)
GPIO.setup(pin4,GPIO.OUT)

classNames = []
classFile = "/home/pi/Desktop/ESE519Final/Object-detection/coco/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/ESE519Final/Object-detection/coco/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/ESE519Final/Object-detection/coco/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# def getPos(Xpos,Ypos):
#     Xdiff = Xpos-Xpos1
#     Ydiff  = Ypos-Ypos1
#     if(Xdiff<=0):
#         Xpos1 = Xpos1-Xdiff
#     if(Xdiff >0):
#         Xpos1 = Xpos1+Xdiff
#     if(Ydiff <=0):
#         Ypos1 = Ypos1-Ydiff
#     if(Ydiff>0):
#         Ypos1 = Ypos1+Ydiff
#     if((abs(Xdiff)<=20)and (abs(Ydiff)<=20)):
#         fcount = fcount+1
#         if(fcount==10):
#             print(Xpos1,Ypos1)
#             fcount=0
#     if(!(abs(Xdiff)<=20)and (abs(Ydiff)<=20)):
#         fcount = 0
def getObjects(center1,center2,img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    #cv2.circle(img,(960,540),2,(255,0,0),2)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    #print(box)
                    center1 = int((box[0]+box[0]+box[2])/2)
                    center2 = int((box[1]+box[1]+box[3])/2)-20
                    
                    #print(center1,center2)
                    #print(box)
                    #print("The coordinate of the phone is at\n")
                    #print(center1,center2-30,round(confidence*100))
                    #getPos(center1,center2)
                    # yhnhgb cv2.circle(img,(center1,center2),100,(0,0,255),5)
                    cv2.circle(img,(center1,center2),int(0.8*box[2]/2),(0,0,255),5)
                    #cv2.circle(img,(box[0]+box[2],box[1]+box[3]),5,(0,0,255),5)
                    
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+220,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo,center1,center2


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    #cap.set(10,70)
    #starttime =time.time()

    while True:
        
        success, img = cap.read()
        #cv2.circle(img,(0,0),5,(0,0,255),5)
        #cv2.circle(img,(1920,1080),5,(0,0,255),5)
        #nowtime = time.time()
        #if(int(nowtime-starttime)>2):
        result, objectInfo, Xpos2, Ypos2= getObjects(center1,center2,img,0.3,0.3,objects=['cell phone'])
        if(abs(Xpos2-Xpos1)>=10 or abs(Ypos2-Ypos1)>=10):
            fcount = fcount+1
        if(abs(Xpos2-Xpos1)<10 and abs(Ypos2-Ypos1)<10):
            fcount = 0
        if(Xpos2 == 0):
            fcount = 0
        if(fcount == 3):           
            stepY = (120/196)*23.78*(abs(Ypos2-Ypos1))
            stepX = (363/493)*(2200/570)*(abs(Xpos2-Xpos1))
            Yout = (1/4400)*stepY
            Xout = (1/2200)*stepX
            print("Target Locked!")
            if(Xpos2>=Xpos1):#X+
                GPIO.output(pin4,GPIO.HIGH)
                time.sleep(Xout)
                GPIO.output(pin4,GPIO.LOW)
                time.sleep(1)
            if(Xpos2<Xpos1):#X-
                GPIO.output(pin3,GPIO.HIGH)
                time.sleep(Xout)
                GPIO.output(pin3,GPIO.LOW)
                time.sleep(1)
            if(Ypos2>=Ypos1):#Y+
                GPIO.output(pin2,GPIO.HIGH)
                time.sleep(Yout)
                GPIO.output(pin2,GPIO.LOW)
                time.sleep(1)
            if(Ypos2<Ypos1):#Y-
                GPIO.output(pin1,GPIO.HIGH)
                time.sleep(Yout)
                GPIO.output(pin1,GPIO.LOW)
                time.sleep(1)
            Ypos1 = Ypos2
            Xpos1 = Xpos2
            #starttime = time.time()
        #print("Location:")
        #print(Xpos2,Ypos2-30)
        cv2.imshow("Output",img)
        print(fcount)
        print(Xpos2,Ypos2)
        if cv2.waitKey(1) ==27:#press ESC to stop the code
           break
    cap.release()
    cv2.destroyAllWindows()
