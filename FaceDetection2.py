import cv2
import time
import os
import csv
# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')  

def FaceDetect(mode):
    if mode=="dataset":
        id=str(len(os.listdir('Dataset'))+1)
        name=input("Enter Name : ")
        row=[name,id]
        try:
            os.mkdir("Dataset\\"+id+'.'+name)
        except:
            print("File already exist")
        with open("StudentList.csv",'a') as fa:
            writer=csv.writer(fa,lineterminator="\n")
            writer.writerow(row)
    if mode=="recognize":
        try:
            os.mkdir("RecognizeFaces")
        except: pass
    images=list()
    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)
    # To use a video file as input 
    # cap = cv2.VideoCapture('filename.mp4')
    i=0
    while i<20:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        eyes = eye_cascade.detectMultiScale(gray,1.1,4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_color = img[y:y + h, x:x + w]
            roi_gray=gray[y:y+h,x:x+w]

            eyes = eye_cascade.detectMultiScale(img)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 1)
            if len(eyes)!=0:
                print(str(i+1)+".[INFO] Object found.")
                if mode=='dataset': 
                    cv2.imwrite("Dataset\\"+id+"."+name+"\\"+str(id)+"."+str(i)+".jpg",roi_gray)
                elif mode=='recognize':
                    j=str(len(os.listdir("RecognizeFaces"))+1)
                    cv2.imwrite("RecognizeFaces\\"+j+".jpg",roi_gray)
                else :
                    images.append(roi_gray)   

                i=i+1
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
        time.sleep(0)

    # Release the VideoCapture object
    cap.release()
    return images

print("****MENU****")
print("1. Create Dataset")
print("2. Run Face Detector")
ch=int(input("Enter Your Choice :"))
if ch==1:
    FaceDetect('dataset')
if ch==2:
    FaceDetect('recognize')
# id=input("Enter ID : ")
# try:
#     os.mkdir("Dataset\\"+id)
# except:
#     print("File already exist")

# images=FaceDetect()
# i=0
# for image in images:
#     i=i+1
#     print(str(i)+".[INFO] Object found. Saving locally.") 
#     cv2.imwrite("Dataset\\"+id+"\\"+str(image[1]) + str(image[2]) + '_faces('+str(i)+').jpg', image[0]) 
                
