import cv2
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


canvas = None
last_point = None
drawing_color = (0, 255, 0)  
line_thickness = 5
eraser_mode = False

# Set up webcam
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8)

# Control points
color_boxes = [
    [(20, 20, 60, 60), (0, 0, 255)],    # Red
    [(80, 20, 120, 60), (0, 255, 0)],   # Green
    [(140, 20, 180, 60), (255, 0, 0)],  # Blue
    [(200, 20, 240, 60), (0, 255, 255)],  # Yellow
]
clear_box = [(width - 60, 20, width - 20, 60), (0, 0, 0)]  # Clear canvas button
eraser_box = [(width - 120, 20, width - 80, 60), (255, 255, 255)]  # Eraser button

def is_point_in_box(point, box):
    """Check if a point is within a box"""
    x, y = point
    x1, y1, x2, y2 = box
    return x1 < x < x2 and y1 < y < y2

def draw_controls(frame):
    """Draw control boxes on frame"""
    # Draw color selection boxes
    for box, color in color_boxes:
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, -1)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 255), 2)
    
    # Draw clear canvas button
    cv2.rectangle(frame, (clear_box[0][0], clear_box[0][1]), (clear_box[0][2], clear_box[0][3]), clear_box[1], -1)
    cv2.rectangle(frame, (clear_box[0][0], clear_box[0][1]), (clear_box[0][2], clear_box[0][3]), (255, 255, 255), 2)
    cv2.putText(frame, "Clear", (clear_box[0][0] + 5, clear_box[0][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Draw eraser button
    cv2.rectangle(frame, (eraser_box[0][0], eraser_box[0][1]), (eraser_box[0][2], eraser_box[0][3]), eraser_box[1], -1)
    cv2.rectangle(frame, (eraser_box[0][0], eraser_box[0][1]), (eraser_box[0][2], eraser_box[0][3]), (0, 0, 0), 2)
    cv2.putText(frame, "Eraser", (eraser_box[0][0] - 5, eraser_box[0][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return frame

def main():
    global canvas, last_point, drawing_color, eraser_mode
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip the frame horizontally for a more intuitive experience
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hand detection
        results = hands.process(rgb_frame)
        
        # Draw control UI
        frame = draw_controls(frame)
        
        # Combine canvas with the frame
        combined_img = cv2.addWeighted(frame, 0.7, canvas, 0.7, 0)
        
        # Check for hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    combined_img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get index finger tip coordinates
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)
                
                # Check if finger is on a control button
                button_pressed = False
                
                # Check color selection
                for box, color in color_boxes:
                    if is_point_in_box((x, y), box):
                        drawing_color = color
                        eraser_mode = False
                        button_pressed = True
                        break
                
                # Check clear button
                if is_point_in_box((x, y), clear_box[0]):
                    canvas = np.zeros((height, width, 3), dtype=np.uint8)
                    button_pressed = True
                
                # Check eraser button
                if is_point_in_box((x, y), eraser_box[0]):
                    eraser_mode = True
                    button_pressed = True
                
                # Draw a circle at the tip of the index finger
                cv2.circle(combined_img, (x, y), 10, drawing_color if not eraser_mode else (255, 255, 255), -1)
                
                # Draw on canvas if not pressing a button
                if not button_pressed:
                    if last_point is not None:
                        if eraser_mode:
                            # Erase by drawing black with thicker line
                            cv2.line(canvas, last_point, (x, y), (0, 0, 0), line_thickness * 2)
                        else:
                            cv2.line(canvas, last_point, (x, y), drawing_color, line_thickness)
                    last_point = (x, y)
            
        else:
            last_point = None
        
        # Show the result
        cv2.imshow('MediaPipe Drawing', combined_img)
        
        # Exit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    hands.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

