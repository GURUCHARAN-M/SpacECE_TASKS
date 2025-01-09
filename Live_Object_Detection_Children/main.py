import cv2
import numpy as np

def load_yolo_model(config_path, weights_path, classes_path):
    try:
        net = cv2.dnn.readNet(weights_path, config_path)
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None, None, None
    try:
        with open(classes_path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Classes file not found: {classes_path}")
        return None, None, None
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers

def detect_objects(net, output_layers, frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    return outputs, width, height

def draw_predictions(outputs, width, height, frame, classes, confidence_threshold=0.5):
    class_ids = []
    confidences = []
    boxes = []
    safe_objects = ["pen", "pencil", "toy", "book", "cup", "chair", "bed"]  # Add more safe objects here
    harmful_objects = ["knife", "scissors"]  # Add more harmful objects here

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression (NMS)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)

    results = []  # Store numerical results
    if indexes is None or len(indexes) == 0:  # Handle empty or invalid NMS results
        return frame, results

    for i in indexes.flatten():  # Safely flatten the indexes
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        if label in safe_objects:
            color = (0, 255, 0)  # Green for safe objects
            result_str = f"{label}: Positive"
            results.append(1)  # Numerical result
        elif label in harmful_objects:
            color = (0, 0, 255)  # Red for harmful objects
            result_str = f"{label}: Negative"
            results.append(-1)  # Numerical result
        else:
            color = (255, 255, 255)  # White for others
            result_str = f"{label}: Neutral"
            results.append(0)  # Numerical result

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        print(result_str)

    return frame, results


def live_detection(net, classes, output_layers):
    cap = cv2.VideoCapture(0)  # Open default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        outputs, width, height = detect_objects(net, output_layers, frame)
        frame, results = draw_predictions(outputs, width, height, frame, classes)

        # Display results in the terminal
        overall_result = "Neutral"
        if all(x == 1 for x in results):
            overall_result = "Positive"
        elif any(x == -1 for x in results):
            overall_result = "Mixed (Contains Negative)"

        print(f"Overall result: {overall_result}")

        # Show the video feed
        cv2.imshow("Live Detection", frame)

        # Exit on pressing 'q'
        ke = cv2.waitKey(1)
        if ke!=-1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Define your YOLO model paths
    config_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Live_Object_Detection_Children\\yolov3.cfg"
    weights_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Live_Object_Detection_Children\\yolov3.weights"
    classes_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Live_Object_Detection_Children\\coco.names"

    # Load YOLO model
    net, classes, output_layers = load_yolo_model(config_path, weights_path, classes_path)
    if net is None or classes is None or output_layers is None:
        print("Error: Model loading failed.")
        exit()

    # Start live detection
    live_detection(net, classes, output_layers)
