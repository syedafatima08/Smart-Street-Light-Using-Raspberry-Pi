import cv2
import numpy as np

def detect_fog(frame, threshold):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to identify foggy regions
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Count the number of white pixels (foggy regions)
    white_pixels = cv2.countNonZero(binary)
    
    # Set a threshold for fog detection
    fog_threshold = 0.1 * frame.shape[0] * frame.shape[1]  # 10% of the image size
    
    # Check if the number of foggy pixels exceeds the threshold
    if white_pixels > fog_threshold:
        return True
    else:
        return False

def main():
    # Open the default camera

    
    cap = cv2.VideoCapture(0)
    
    threshold = 200  # Initial threshold
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Calculate the average brightness of the frame
        brightness = np.mean(frame)
        
        # Adjust the threshold based on brightness
        if brightness < 100:
            threshold = 1
        else:
            threshold = 200
        
        # Detect fog
        fog_detected = detect_fog(frame, threshold)
        
        # Display the frame
        cv2.imshow('Frame', frame)
        
        # Display fog status
        if fog_detected:
            print("No Fog Detected on Highway!")
        else:
            print("Fog Detected on Highway")
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
