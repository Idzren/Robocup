import cv2
import mediapipe as mp
import time
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the speech rate (0.5 is slower, 2.0 is faster, 1.0 is the default)
engine.setProperty('rate', 1.0)

# Initialize mediapipe hands component
mp_hands = mp.solutions.hands

# Initialize mediapipe drawing tools
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Constants for landmarks
THUMB_TIP =  4
WRIST =  0
HAND_WAVE_HORIZONTAL_THRESHOLD =  0.02
HAND_RAISE_THRESHOLD =  0.02
HAND_WAVE_DURATION =  2

# State variables for hand gestures
hand_raise_active = False
hand_wave_active = False
hand_wave_start_time =  0
thumbs_up_detected = False

# Initialize hand model outside the loop
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        # Introduce a small delay to reduce processing load
        time.sleep(0.03)

        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hands
        results_hands = hands.process(rgb_frame)

        # Draw hand landmarks and skeleton on the frame
        if results_hands.multi_hand_landmarks:
            for landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the landmarks of interest
                thumb_tip = landmarks.landmark[THUMB_TIP]
                hand_wrist = landmarks.landmark[WRIST]

                # Calculate hand raise distance
                hand_raise_distance = thumb_tip.y - hand_wrist.y

                # Calculate horizontal movement of the hand for hand wave
                hand_horizontal_movement = thumb_tip.x - hand_wrist.x

                # Detect hand raise
                if hand_raise_distance < -HAND_RAISE_THRESHOLD:
                    if not hand_raise_active:
                        print('Hand Raise Detected')
                        hand_raise_active = True
                        hand_wave_active = False
                        hand_wave_start_time = time.time()  # Reset hand wave timer when hand is raised
                        # Custom message for hand raise
                        custom_message = "please wait, i am coming"
                        print(custom_message)
                        # Convert custom message to speech for hand raise
                        engine.say(custom_message)
                        engine.runAndWait()
                else:
                    hand_raise_active = False

                # Detect hand wave
                if hand_horizontal_movement > HAND_WAVE_HORIZONTAL_THRESHOLD:
                    if hand_raise_active and not hand_wave_active:
                        if time.time() - hand_wave_start_time >= HAND_WAVE_DURATION:
                            hand_wave_active = True
                            print("Hand Wave Detected")
                            # Custom message for hand raise
                            custom_message = "Hello there, nice to meet you , I am wheelchair robot"
                            print(custom_message)
                            # Convert custom message to speech for hand raise
                            engine.say(custom_message)
                            engine.runAndWait()
                else:
                    hand_wave_active = False

                # Detect thumbs up gesture (assuming the thumb is extended upwards)
                if thumb_tip.z > hand_wrist.z and thumb_tip.y < hand_wrist.y:
                    thumbs_up_detected = True
                    print('Thumbs Up Detected')
                    # Custom message for hand raise
                    custom_message = "All good, thank you.See you again"
                    print(custom_message)
                    # Convert custom message to speech for hand raise
                    engine.say(custom_message)
                    engine.runAndWait()
                else:
                    thumbs_up_detected = False

        # Display the frame
        cv2.imshow('Gestures Detection', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) &  0xFF == ord('q'):
            break

# Release the capture
cap.release()
cv2.destroyAllWindows()
