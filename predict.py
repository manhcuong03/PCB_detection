from ultralytics import YOLO
import time
import cv2
import os

# Load a model
weight = 'best2.pt'
model = YOLO(weight)

# Predict on the image
results = model.predict(r'D:\code\Final_xla\UI\captured_image_20241219_125456.jpg', show=False, save=True, save_dir='output')

# Process and extract results
for result in results:
    predictions = result.boxes
    
    # Extract bounding boxes, confidence scores, and labels
    boxes = predictions.xyxy.cpu().numpy()  # Bounding boxes in [x1, y1, x2, y2]
    scores = predictions.conf.cpu().numpy()  # Confi/kaggle/input/dataset-m/test/images/captured_image_20241219_124104.jpgdence scores
    labels = predictions.cls.cpu().numpy()  # Labels
    
    print("Bounding Boxes:\n", boxes)
    print("Confidence Scores:\n", scores)
    print("Labels:\n", labels)

# Save the result image with timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")  # Example: 20241205_152030
output_dir = r'D:\code\Final_xla\UI\output'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Save the result image
output_image_path = os.path.join(output_dir, f'output_image_{timestamp}.jpg')

# Assuming the processed image is saved in `result.imgs[0]`
output_image = results[0].plot()  # Visualize predictions on the image
cv2.imwrite(output_image_path, output_image)
print(f"Image saved at: {output_image_path}")
