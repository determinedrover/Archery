import numpy as np
import cv2
import math
cap=cv2.VideoCapture(0)
prevCircle=None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2
x=[]
y=[]
count=0
while True:
    ret, frame= cap.read()
    if not ret: break


    grayFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurFrame=cv2.GaussianBlur(grayFrame,(17,17),0)

    circles=cv2.HoughCircles(blurFrame,cv2.HOUGH_GRADIENT,1.2,100,param1=70,param2=60,minRadius=0,maxRadius=700)

    if circles is not None:
        circles=np.uint16(np.around(circles))
        chosen=None
        for i in circles[0,:]:
            
            if chosen is None: chosen=i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])<=dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen=i
        cv2.circle(frame,(chosen[0],chosen[1]),1,(0,100,100),3)
        cv2.circle(frame,(chosen[0],chosen[1]),chosen[2],(255,0,255),3)
        prevCircle=chosen
        
        if count==0:
            x.append(chosen[0])
            y.append(chosen[1])
        
        if len(x)>=20 and dist(chosen[0],chosen[1],x[0],y[0])<150:
 #Finding if the array already has atleast 20 points and distance between current point and first detected point is less than 150
            
            count=1
            
            

        
        
    cv2.imshow("circles",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
x_mean=np.mean(x)
y_mean=np.mean(y)

print('x ' ,x_mean)
print('y ', y_mean)
rad=math.sqrt(dist(x_mean,y_mean,x[0],y[0]))
print('Radius',rad)
