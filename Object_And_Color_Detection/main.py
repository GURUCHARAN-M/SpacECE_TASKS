import os
import cv2
import numpy as np
from sklearn.cluster import KMeans

def load_yolo_model(config_path, weights_path, classes_path):
    try:
        net = cv2.dnn.readNet(weights_path, config_path)
        with open(classes_path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        return net, classes, output_layers
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None, None, None

def detect_objects(net, output_layers, frame, classes, confidence_threshold=0.5):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    class_ids, confidences, boxes, results = [], [], [], []
    safe_objects = ["pen", "pencil", "toy", "book", "cup", "chair", "bed"]
    harmful_objects = ["knife", "scissors"]
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)
    if indexes is None:
        return frame, results
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (0, 255, 0) if label in safe_objects else (0, 0, 255) if label in harmful_objects else (255, 255, 255)
            results.append(label)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame, results

def calculate_room_brightness(image):
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    gray_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
    return np.mean(gray_image)

def get_dominant_color(image):
    resized_image = cv2.resize(image, (150, 150))
    data = resized_image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=1, random_state=42)
    kmeans.fit(data)
    return tuple(map(int, kmeans.cluster_centers_[0]))

def process_images(input_folder, output_folder_objects, output_folder_colors, config_path, weights_path, classes_path):
    os.makedirs(output_folder_objects, exist_ok=True)
    os.makedirs(output_folder_colors, exist_ok=True)
    net, classes, output_layers = load_yolo_model(config_path, weights_path, classes_path)
    if not net:
        print("Error loading YOLO model.")
        return
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Could not read image {image_path}. Skipping.")
            continue
        processed_frame, object_results = detect_objects(net, output_layers, frame.copy(), classes)
        object_output_path = os.path.join(output_folder_objects, f"{os.path.splitext(image_file)[0]}_objects.jpg")
        cv2.imwrite(object_output_path, processed_frame)
        brightness = calculate_room_brightness(frame)
        dominant_color = get_dominant_color(frame)
        color_info = f"Brightness: {brightness:.2f}, Dominant Color: {dominant_color}"
        color_output_path = os.path.join(output_folder_colors, f"{os.path.splitext(image_file)[0]}_colors.jpg")
        color_frame = frame.copy()
        cv2.putText(color_frame, color_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imwrite(color_output_path, color_frame)

if __name__ == "__main__":
    # C:\Users\gurum\Desktop\SpacECE_TASKS\Object_And_Color_Detection
    input_folder = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\images"
    output_folder_objects = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\output_objects"
    output_folder_colors = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\output_colors"
    config_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\yolov3.cfg"
    weights_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\yolov3.weights"
    classes_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_And_Color_Detection\\coco.names"
    process_images(input_folder, output_folder_objects, output_folder_colors, config_path, weights_path, classes_path)
