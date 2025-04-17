from ultralytics import YOLO
import cv2
import time
import json
import os

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(PROJECT_ROOT, "input_images")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

AMBULANCE_MODEL = os.path.join(PROJECT_ROOT, "best.pt")

# Detection parameters
EMERGENCY_CONFIDENCE = 0.65  # Balanced confidence threshold
EMERGENCY_CLASSES = [0, 1]   # Class IDs for emergency vehicles
MIN_BOX_AREA = 3000          # Minimum detection area in pixels
DISPLAY_TIME = 5000          # Milliseconds to display image results

def detect_emergency_vehicles(frame, model):
    """Enhanced detection with better visualization"""
    results = {"emergency": False, "boxes": []}
    detections = model(frame, conf=EMERGENCY_CONFIDENCE, verbose=False)[0]
    
    for box in detections.boxes:
        class_id = int(box.cls)
        confidence = float(box.conf)
        
        if class_id in EMERGENCY_CLASSES:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            area = (x2 - x1) * (y2 - y1)
            
            if area > MIN_BOX_AREA:
                results["emergency"] = True
                results["boxes"].append({
                    "class": detections.names[class_id],
                    "confidence": confidence,
                    "position": [x1, y1, x2, y2],
                    "area": area
                })
                
                # Draw bounding box (thicker for emergencies)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                
                # Draw label with background for readability
                label = f"{detections.names[class_id]} {confidence:.2f}"
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
                cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), (0, 0, 255), -1)
                cv2.putText(frame, label, (x1, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    # Add red border if emergency detected
    if results["emergency"]:
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 15)
        alert_text = "EMERGENCY VEHICLE DETECTED!"
        cv2.putText(frame, alert_text, (50, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    
    return frame, results

def process_image(image_path):
    """Process image with proper display handling"""
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error loading image: {image_path}")
        return None

    model = YOLO(AMBULANCE_MODEL)
    processed_frame, results = detect_emergency_vehicles(frame, model)

    # Save output
    output_path = os.path.join(OUTPUT_DIR, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, processed_frame)

    # Display results
    cv2.imshow("Emergency Vehicle Detection", processed_frame)
    key = cv2.waitKey(DISPLAY_TIME)
    cv2.destroyAllWindows()

    return {
        "file": os.path.basename(image_path),
        "emergency": results["emergency"],
        "detections": results["boxes"]
    }

def process_video(video_path):
    """Process video with frame-by-frame detection (without emergency count)"""
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video: {video_path}")
        return None

    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Prepare output
    output_path = os.path.join(OUTPUT_DIR, f"processed_{os.path.basename(video_path)}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    model = YOLO(AMBULANCE_MODEL)
    results = {
        "file": os.path.basename(video_path),
        "total_frames": total_frames,
        "emergency_frames": []
    }

    frame_count = 0
    print(f"\nProcessing: {os.path.basename(video_path)}")
    print(f"Size: {width}x{height} | FPS: {fps:.1f} | Frames: {total_frames}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        processed_frame, detection = detect_emergency_vehicles(frame, model)

        if detection["emergency"]:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            results["emergency_frames"].append({
                "frame": frame_count,
                "timestamp": timestamp,
                "detections": detection["boxes"]
            })

        # Write frame to output
        out.write(processed_frame)

        # Display without emergency counter
        cv2.imshow("Emergency Vehicle Detection", processed_frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

        # Print progress
        if frame_count % 10 == 0:
            print(f"Processed {frame_count}/{total_frames} frames", end='\r')

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"\nProcessing complete. Emergency events detected: {len(results['emergency_frames'])}")
    return results

def main():
    # Verify model exists
    if not os.path.exists(AMBULANCE_MODEL):
        print(f"\nERROR: Ambulance model not found at {AMBULANCE_MODEL}")
        return

    # Get input file (modify this path as needed)
    input_file = os.path.join(INPUT_DIR, "ambulance.jpg")  # Change to your file
    
    if not os.path.exists(input_file):
        print(f"\nInput file not found: {input_file}")
        return

    start_time = time.time()
    
    # Process based on file type
    if input_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        result = process_image(input_file)
    elif input_file.lower().endswith(('.mp4', '.avi', '.mov')):
        result = process_video(input_file)
    else:
        print(f"\nUnsupported file format: {input_file}")
        return

    # Save and display results
    if result:
        result_file = os.path.join(OUTPUT_DIR, "detection_results.json")
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print("\nDetection Results:")
        if "emergency_frames" in result:  # Video results
            print(f"- Emergency events detected: {len(result['emergency_frames'])}")
        else:  # Image results
            status = "DETECTED" if result["emergency"] else "NOT DETECTED"
            print(f"- Emergency vehicle: {status}")
            if result["emergency"]:
                for det in result["detections"]:
                    print(f"  - {det['class']} (confidence: {det['confidence']:.2f}, area: {det['area']} px)")
        
        print(f"\nVisual results saved to: {OUTPUT_DIR}")
        print(f"Processing time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("EMERGENCY VEHICLE DETECTION SYSTEM")
    print("="*50)
    main()