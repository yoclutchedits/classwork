import mediapipe as mp
import cv2
import time
import pyautogui
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7,max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
scroll_s=300
scroll_d=1
cam_width, cam_height = 640, 480
def detect_gesture(landmaks,handness):
    fingers=[]
    tips=mp_hands.HandLandmark.INDEX_FINGER_DIP,mp_hands.HandLandmark.MIDDLE_FINGER_DIP,mp_hands.HandLandmark.RING_FINGER_DIP,mp_hands.HandLandmark.PINKY_DIP
    for tip in tips:
        for lm in landmaks.landmark:
            if landmaks.landmark[tip].y < landmaks.landmark[tip - 2].y:
                fingers.append(1)
    thumb_tip=landmaks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip=landmaks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if(handness=="Right"and thumb_tip.x>thumb_ip.x)or(handness=="Left"and thumb_tip.x<thumb_ip.x):
        fingers.append(1)
    return "scroll_up" if sum(fingers)==4 else "scroll_down" if sum(fingers)==0 else "none"
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)
last_scroll=p_time=0
print('gesture control started')
print('show all fingers to scroll up')
print('show fist to scroll down')
print('press q to quit')
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break 
    img=cv2.flip(img,1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    gesture="none"
    if results.multi_hand_landmarks:
        for hand,handedness_info in zip(results.multi_hand_landmarks,results.multi_handedness):
            handness=handedness_info.classification[0].label
            gesture=detect_gesture(hand,handness)
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            if time.time()-last_scroll>scroll_d:
                if gesture=="scroll_up":
                    pyautogui.scroll(scroll_s)
                elif gesture=="scroll_down":
                    pyautogui.scroll(-scroll_s)
                last_scroll=time.time()
    fps=1/(time.time()-p_time)if (time.time()-p_time>0) else 0
    p_time=time.time()
    cv2.putText(img,f'FPS:{int(fps)}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(img,f'Gesture:{gesture}',(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()