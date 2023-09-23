import cv2
import numpy as np
 
def circle_detect(video):
    sta,bgr_img = video.read()

    if bgr_img.shape[-1] == 3:           # color image
        b,g,r = cv2.split(bgr_img)       # get b,g,r
        rgb_img = cv2.merge([r,g,b])     # switch it to rgb
        gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = bgr_img
    img = cv2.medianBlur(gray_img, 5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=50,
                    minRadius=40,maxRadius=100)
    #print(circles)
    if circles is None:
        state = 0
        #cv2.imshow("1",cimg)
        #cv2.waitKey(10)
        return state,0,0,0
    circles = np.uint16(np.around(circles))
    r_max = 0
    x_final = 0
    y_final = 0
    for i in circles[0,:]:
        if i[2]>= r_max:
            r_max = i[2]
            x_final = i[0]
            y_final = i[1]
        # draw the outer circle
    #cv2.circle(cimg,(x_final,y_final),r_max,(0,255,0),2)
        # draw the center of the circle
    #cv2.circle(cimg,(x_final,y_final),2,(0,0,255),3)
    #cv2.imshow("1",cimg)
    #cv2.waitKey(10)
    return 1,x_final,y_final,r_max #x,y,r
 
def color_warped(video):
    sta,img = video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 颜色识别(红色)，过滤红色区域
    #lower_red1 = np.array([0, 43, 46])  # 红色阈值下界
    #higher_red1 = np.array([10, 255, 255])  # 红色阈值上界
    #mask_red1 = cv2.inRange(hsv, lower_red1, higher_red1)
    lower_red2 = np.array([165, 43, 200])  # 红色阈值下界
    higher_red2 = np.array([180, 255, 255])  # 红色阈值上界
    mask_red = cv2.inRange(hsv, lower_red2, higher_red2)
    #mask_red = cv2.add(mask_red1, mask_red2)  # 拼接过滤后的mask
    #img_show('mask_red', mask_red)
    
    # 形态学去噪，cv2.MORPH_OPEN先腐蚀再膨胀，cv2.MORPH_CLOSE先膨胀再腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel, iterations=1)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    #mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel, iterations=3)
               
    # 轮廓检测，找出线条的轮廓
    draw_cnt = img.copy()
    cnts = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    cv2.drawContours(draw_cnt, cnts, -1, (0, 255, 0), 2)
    #img_show('draw_cnt', draw_cnt)
    
    w_max = 0
    h_max = 0
    x_final = 0
    y_final = 0
    # 拟合，找到相应的的顶点
    for cnt in cnts:
        #area = cv2.contourArea(cnt)
        #perimeter = cv2.arcLength(area,True)
        #approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
        #print(len(approx))
        x, y, w, h = cv2.boundingRect(cnt)  #获取坐标值和宽度、高度
        if w>=w_max & h>=h_max:
            x_final = x
            y_final = y
        if w>=w_max:
            w_max = w
        if h>=h_max:
            h_max = h
        #print(x,y,w,h)
            '''
    if len(cnts) == 0:
        cv2.imshow("mg", img)
        cv2.waitKey(10)
        state = 0
        return state,0,0,0,0
        '''
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    #cv2.imshow("mg", img)
    #cv2.waitKey(10)
    state = 1
    return state,int(x_final+0.5*w_max),int(y_final+0.5*h_max),w_max,h_max

def human_detect(video):
    ret, frame = video.read()
    face_cas = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_rects = face_cas.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=7)
    #scaleFactor是每次缩小图像的比例，默认是1.1，minNeighbors匹配成功所需要的周围矩形框的数目，每一个特征匹配到的区域都是一个矩形框，只有多个矩形框同时存在的时候，才认为是匹配成功
    if len(face_rects) == 0 :
        #print(1)
        #cv2.imshow("1",frame)
        #cv2.waitKey(1)
        state = 0
        return state,0,0,0,0
    #print(face_rects)
    for face_rect in face_rects:
        x, y, w, h = face_rect
    print(x,y,w,h)
    # 画出人脸
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.imshow("1", frame)
    #cv2.waitKey(1)
    return 1,int(x+0.5*w),int(y+0.5*h),w,h


def detect(mode,video):
    if mode == 0:
        s,x,y,r = circle_detect(video)
        return s,x,y,r
    if mode == 1:
        # video: 640*480
        s,x,y,w,h = color_warped(video)
        return s,x,y,w,h
    if mode == 2:
        s,x,y,w,h = human_detect(video)
        return s,x,y,w,h
'''
if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    i = 0
    while True:
        i+=1
        print(i,detect(1,video))
    
'''

