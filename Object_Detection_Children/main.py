import os
import cv2
import numpy as np

score = 0

def load_yolo_model(config_path, weights_path, classes_path):
    net = cv2.dnn.readNet(weights_path, config_path)
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
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
    safe_objects = ["pen", "pencil", "toy", "book","cup"] 
    harmful_objects = ["knife","scissors"] 

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

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)
    for i in range(len(boxes)):
        global score
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            if label in safe_objects:
                score += 1
                color = (0, 255, 0)  # Green for safe objects
            elif label in harmful_objects:
                score -= 1
                color = (0, 0, 255)  # Red for harmful objects
            else:
                color = (255, 255, 255)  # White for others
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def process_image(image_path, net, classes, output_layers):
    global score
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not load image from {image_path}")
        return

    outputs, width, height = detect_objects(net, output_layers, frame)
    frame = draw_predictions(outputs, width, height, frame, classes)
    text , color = "" , (0, 0, 0)
    if score < 0:
        text = f"Score is {score} \n It's not Suitable for Children!"
        color = (0, 0, 255)
    elif score > 0:
        text = f"Score is {score} \n It's Suitable for Children."
        color = (0, 255, 0)
    elif score == 0:
        text = f"Score is {score} \n It's quite Suitable for Children, but need improvements."
        color = (0, 165, 255)
    cv2.putText(frame, text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    # cv2.imwrite(r"C:\Users\gurum\Desktop\SpacECE_TASKS\Object_Detection_Children\test1.webp", frame)
    cv2.imwrite(r"C:\Users\gurum\Desktop\SpacECE_TASKS\Object_Detection_Children\test3.jpg", frame)
    # print(f"Object detection results saved to: {output_path}")

def main():

    config_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_Detection_Children\\yolov3.cfg"
    weights_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_Detection_Children\\yolov3.weights"
    classes_path = r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_Detection_Children\\coco.names"
    # image_path=r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_Detection_Children\\test.webp"
    image_path=r"C:\\Users\\gurum\\Desktop\\SpacECE_TASKS\\Object_Detection_Children\\test2.jpg"

    net, classes, output_layers = load_yolo_model(config_path, weights_path, classes_path)
    process_image(image_path, net, classes, output_layers)

if __name__ == "__main__":
    main()
