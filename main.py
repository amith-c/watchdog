import cv2
import time
from core.camera import CameraStreamManager
from core.alerts import Notifier

def main():
    print("--- WatchDog System Starting ---")
    
    # Initialize components
    notifier = Notifier()
    camera_ids = [4] # You can change this to [1, 2, 3, 4, etc]
    
    manager = CameraStreamManager(camera_ids, use_low_res=True, notifier=notifier)
    
    print(f"Starting streams for cameras: {camera_ids}")
    manager.start_streams()
    
    notifier.notify("WatchDog Active", f"Monitoring {len(camera_ids)} cameras.")

    try:
        while True:
            # Display the feed for the first camera in the list for visualization
            main_cam = camera_ids[0]
            frame = manager.get_frame(main_cam)
            
            if frame is not None:
                cv2.imshow(f'WatchDog - Cam {main_cam}', frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(0.01) # Small sleep to reduce CPU usage
            
    except KeyboardInterrupt:
        print("\nStopping system...")
    finally:
        manager.stop()
        print("--- WatchDog System Stopped ---")

if __name__ == "__main__":
    main()