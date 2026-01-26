import mediapipe as mp
import cv2
mp_hands = mp.solutions.hands
hands = mp_hands.Hands( min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
def get_gesture(hand_landmarks):
    landmark = hand_landmarks.landmark[8]
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended=0
    if abs(landmarks[tip_ids[0]].x-landmarks[pip_ids[0]].x)>0.04:
        extended+=1
    for i in range(1,5):
        if landmarks[tip_ids[i]].y<landmarks[pip_ids[i]].y:
            extended+=1
    if extended>=4:
        return "OPEN"
    elif extended<=1:
        return "FIST"
    else:
        return "partial"
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        h,w,_=frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        gesture='no hand detected'
        if result.multi_hand_landmarks and result.multi_handedness:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                hand_label=result.multi_handedness[idx].classification[0].label
                gesture=get_gesture(hand_landmarks)
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingertip_ids=[4,8,12,16,20]
                for tip_id in fingertip_ids:
                    lm=hand_landmarks.landmark[tip_id]
                    x,y = int(lm.x * w),int(lm.y * h)
                    cv2.circle(frame,(x,y),10,(255,0,0),cv2.FILLED)
                    cv2.putText(frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                wrist=hand_landmarks.landmark[0]
                x_w,y_w=int(wrist.x*w),int(wrist.y*h)
                cv2.putText(frame, f'Wrist: ({x_w}, {y_w})', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        status_color = (0, 255, 0) if gesture in ['OPEN','FIST'] else (0,165,255)
        cv2.putText(frame, f'Status: {gesture}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        cv2.imshow("Hand gesture recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cap.release()
        cv2.destroyAllWindows()