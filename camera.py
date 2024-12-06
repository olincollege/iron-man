from picamera2 import Picamera2, Preview
import cv2
import time

def main():
    # Initialize Picamera2
    picam2 = Picamera2()
    
    # Configure the camera for preview and capturing
    camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})
    picam2.configure(camera_config)
    
    # Start the camera
    picam2.start()
    print("Camera started...")
    
    # Allow the camera to warm up
    time.sleep(2)
    
    # Capture a single frame
    frame = picam2.capture_array()
    
    # Display the captured frame using OpenCV
    cv2.imshow("Captured Image", frame)
    
    # Wait for a key press to exit
    print("Press any key to exit...")
    cv2.waitKey(0)
    
    # Cleanup
    cv2.destroyAllWindows()
    picam2.stop()
    print("Camera stopped.")

if __name__ == "__main__":
    main()
