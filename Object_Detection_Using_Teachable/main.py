import numpy as np
import cv2
import tensorflow as tf
import os
from keras.layers import TFSMLayer

np.set_printoptions(suppress=True)

def detect_and_score(model_path, labels_path, input_folder_path, output_folder_path):
    model = TFSMLayer(model_path, call_endpoint='serving_default')
    labels = open(labels_path, "r").readlines()
    for filename in os.listdir(input_folder_path):

        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder_path, filename)
            frame = cv2.imread(image_path)
            if frame is None:
                continue  

            image_resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
            image_array = (image_array / 127.5) - 1 
            predictions = model(image_array)
            predictions = predictions["sequential_3"].numpy() 
            score = 0
            
            for i, confidence_score in enumerate(predictions[0]):
                label = labels[i].strip()
                color = (0, 0, 0)

                if confidence_score > 0.3:

                    if i >= 0 and i <= 5:
                        score += 1  # +1 for labels 0 to 5
                        color = (0, 255, 0)  # Green
                    if i >= 6 and i <= 9:
                        score -= 1  # -1 for labels 6 to 9
                        color = (0, 0, 255)  # Red

                    # print(f"Class: {label} - Confidence Score: {np.round(confidence_score * 100)}%")
                    height, width, _ = frame.shape
                    start_point = (int(width * 0.1), int(height * 0.1))
                    end_point = (int(width * 0.9), int(height * 0.9))
                    thickness = 2
                    cv2.rectangle(frame, start_point, end_point, color, thickness)
                    text = f"{label}: {np.round(confidence_score * 100)}%"
                    cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

            print(f"Total Score for {filename}: {score}")
            output_image_path = os.path.join(output_folder_path, filename)
            cv2.imwrite(output_image_path, frame)

if __name__ == "__main__":
    model_path = r'C:\\Users\\gurum\\Downloads\\Child_Detection_Teachable\\model.savedmodel'
    labels_path = r'C:\\Users\\gurum\\Downloads\\Child_Detection_Teachable\\labels.txt'
    input_folder_path = r'C:\\Users\\gurum\\Downloads\\Child_Detection_Teachable\\input'  
    output_folder_path = r'C:\\Users\\gurum\\Downloads\\Child_Detection_Teachable\\output'
    
    detect_and_score(model_path, labels_path, input_folder_path, output_folder_path)
