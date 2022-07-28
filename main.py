import cv2
import mediapipe as mp 

class Queue():
    def __init__(self):
        self.queue = []
        self.max_elements = 8
    
    def enqueue(self, position):
        self.queue.append(position)
        if len(self.queue) > self.max_elements:
            self.dequeue()
    
    def dequeue(self):
        first = self.queue[0]
        self.queue = self.queue[1:]
        return first

    def len(self):
        return len(self.queue)
    
capture = cv2.VideoCapture(0) # camera id, if only 1 camera, use 0Y
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.2)
# hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
hand_landmarks_style = mpDraw.DrawingSpec(color=(0, 50, 255), thickness=5)
hand_connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=3)

bone_toggle = True

queue = Queue()

while True:
    ret, img = capture.read()
    if ret:
        frame = cv2.flip(img, 1)
        frame = cv2.resize(frame, (0, 0), fx=2, fy=2)
        
        imgHeight, imgWidth = frame.shape[0], frame.shape[1]
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        edge = cv2.Canny(frame, 50, 50)
        edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
        result = hands.process(frame)
        
        if result.multi_hand_landmarks:
            # print(result.multi_hand_landmarks)
            for id, hand_landmarks in enumerate(result.multi_hand_landmarks):
                if bone_toggle:
                    mpDraw.draw_landmarks(edge, hand_landmarks, mpHands.HAND_CONNECTIONS, hand_landmarks_style, hand_connection_style)
                
                if id==0: # if first hand
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        xPos, yPos = int(landmark.x*imgWidth), int(landmark.y*imgHeight)
                        if i == 8: # 食指
                            queue.enqueue((xPos, yPos))
                    # overlay = edge.copy()
                    for queue_id, pos in enumerate(queue.queue):
                        
                        # print(pos)
                        cv2.circle(edge, pos, 10, (0, 200, 200), cv2.FILLED)
                        # cv2.circle(overlay, pos, 10, (0, 200, 200), cv2.FILLED)
                        # edge = cv2.addWeighted(overlay, queue_id/queue.len(), edge, 1-queue_id/queue.len(), 0)
                    
                
                
        cv2.imshow('img', edge)
        
        
        
        
        
    if cv2.waitKey(1) == ord('q'): # press q to quit
        break
    if cv2.waitKey(1) == ord('b'): # bone_toggle
        if bone_toggle:
            bone_toggle = False
        else:
            bone_toggle = True



