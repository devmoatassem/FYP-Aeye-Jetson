"""


"""


import jetson.inference 
import jetson.utils 
import cv2 



       




#def main():
    net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold = 0.5) 
        
    cap = cv2.VideoCaputre(0) 
    cap.set(3,640) 
    cap.set(4,480) 



    while True: 
    success, img = cap.read() 
    imgCuda=jetson.utils.cudaFromNumpy(img)

    detections=net.Detect(imgCuda)

    for d in detections:
        print(d)
        x1,x2,x3,x4=int(d.Left),int(d.Top),int(d.Right),int(d.Bottom)
        className=net.GetClassDesc(d.ClassID)
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.putText(img,className,(x1+5,y1+15),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,0,255),2)

    #img=jetson.utils.cudaToNumpy(imgCuda)

    cv2.imshow("Image", img) 
    cv2.waitKey(1) 



# if __name__ == "__main__":
#     main()