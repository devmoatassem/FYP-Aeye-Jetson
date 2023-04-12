"""
ClassID: 76
   -- Confidence: 0.520996
   -- Left:    6.71875
   -- Top:     74.2969
   -- Right:   385
   -- Bottom:  414.141
   -- Width:   378.281
   -- Height:  339.844
   -- Area:    128557
   -- Center:  (195.859, 244.219)


"""


import jetson.inference 
import jetson.utils 
import cv2 




class mnSSD():
    def __init__(self,path,threshold):
        self.path=path
        self.threshold=threshold
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold = 0.5) 
        
    def detect(self,img,display=False):
        imgCuda=jetson.utils.cudaFromNumpy(img)
        detections=self.net.Detect(imgCuda,overlay="OVERLAY_NONE")


        #create a list to add vallues x y etc so that we can detect the location of objects 
        objects=[]
        for d in detections:
        className=self.net.GetClassDesc(d.classID)
        objects.append([className,d])
        if display:
            x1,x2,x3,x4=int(d.Left),int(d.Top),int(d.Right),int(d.Bottom)
            className=net.GetClassDesc(d.ClassID)
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.circle(img,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.line(img,(x1,cy),(x2,cy),(255,0,255),1)
            cv2.line(img,(x1,cy),(x2,cy),(255,0,255),1)
            cv2.

            cv2.putText(img,className,(x1+5,y1+15),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,0,255),2)

        return objects




def main():
    
    cap = cv2.VideoCaputre(0) 
    cap.set(3,640) 
    cap.set(4,480) 



    while True: 
    success, img = cap.read() 
    

    

    
    img=jetson.utils.cudaToNumpy(imgCuda)

    cv2.imshow("Image", img) 
    cv2.waitKey(1) 



if __name__ == "__main__":
    main()