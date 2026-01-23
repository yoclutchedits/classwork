import cv2
import numpy as np
def apply_color_filter(image, ft):
    img=image.copy()
    if ft=='red':
        img[:,:,1]=0
        img[:,:,0]=0
    elif ft=='green':
        img[:,:,2]=0
        img[:,:,0]=0
    elif ft=='blue':
        img[:,:,2]=0
        img[:,:,1]=0
    elif ft=='sobel':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        Sobel_x=cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
        Sobel_y=cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
        sob=cv2.bitwise_or(Sobel_x.astype(np.uint8),Sobel_y.astype(np.uint8))
        img=cv2.cvtColor(sob,cv2.COLOR_GRAY2BGR)
    elif ft=='canny':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        can=cv2.Canny(gray,100,200)
        img=cv2.cvtColor(can,cv2.COLOR_GRAY2BGR)
    elif ft=='cartoon':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=cv2.medianBlur(gray,5)
        ct=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color=cv2.bilateralFilter(image,9,300,300)
        img=cv2.bitwise_and(color,color,mask=ct)
    return img
def main():
    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        print('cannot import camera')
        return
    ft='original'
    print("r. Red filter")
    print("g. Green filter")
    print("b. Blue filter")
    print("s. Sobel filter")
    print("c. Canny filter")
    print("o. Cartoon filter")
    print("q. Quit")

    while True:
        ret,frame=cap.read()
        if not ret:
            print('failed to capture image')
            break
        out=apply_color_filter(frame,ft)
        cv2.imshow('Filtered Video',out)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('r'):
            ft='red'
        elif key==ord('g'):
            ft='green'
        elif key==ord('b'):
            ft='blue'
        elif key==ord('s'):
            ft='sobel'
        elif key==ord('c'):
            ft='canny'
        elif key==ord('o'):
            ft='cartoon'
        elif key==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__=='__main__':
    main()