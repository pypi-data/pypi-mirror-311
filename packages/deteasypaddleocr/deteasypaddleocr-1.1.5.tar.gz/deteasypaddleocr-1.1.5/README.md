## OCR Detection Library 
## deteasypaddleocr 
## version 1.1.5
P.S. In previous versions - fixed some bugs

This library provides a flexible OCR (Optical Character Recognition) detection system that supports multiple OCR backends including EasyOCR and PaddleOCR.

It's designed to detect text regions in images with high accuracy and configurable parameters.  

# Features:

1. Support for multiple OCR types (EasyOCR and PaddleOCR)
2. Azure ML model integration for downloading pre-trained models
3. Image resizing capabilities
4. Bounding box coordinate adjustment
5. Configurable detection parameters
6. Visualization utilities for detected text regions (cv2 + matplotlib)


# Installation

## Requirements:  
Python 3.7 or higher  
CUDA-compatible GPU (recommended for optimal performance)  
Azure VPN Client connection for model downloads  

## Basic Installation

pip install deteasypaddleocr  # Install base package  

## Installation with specific backends

pip install deteasypaddleocr[easyocr]    # Install additional libraries for EasyOCR  
pip install deteasypaddleocr[paddleocr]  # Install additional libraries for PaddleOCR  
pip install deteasypaddleocr[all]        # Install both EasyOCR and PaddleOCR (adviced)  

# Configuration

You may use your own config.json file with the following structure:  

{  
    "ocr_type": "easyocr",  // or "paddleocr"  
}  


# Usage

# Basic Usage

from deteasypaddleocr.ocr_detection import process_image  

## Process an image with default settings
result = process_image(  
    image_path="path/to/image.png",  
)  

## Process with specific OCR type and image resizing
result = process_image(  
    image_path="path/to/image.png", - User is required to provide an image path  
    config_path=config_path, - Has default ocr parameter  
    target_width=1920, - Optional parameters, if you need to resize an image during the detection process  
    target_height=1080,  
    ocr_type="easyocr"  - or "paddleocr", if not specified - used the "config.json" one, by default - "easyocr"  
)  


# Advanced Usage

from deteasypaddleocr.ocr_detection import OCRDetector  
import cv2  

## Initialize detector, ocr_type specification is optional
detector = OCRDetector(ocr_type="paddleocr")  

## Process image
img = cv2.imread(image_path)  
bboxes = detector.detection(  
    img,  
    target_width=1920,  
    target_height=1080  
)  


# Model Download

The library automatically handles model downloading from Azure ML workspace. You'll need:  

Azure ML workspace access  
Proper authentication credentials  
Internet connection for first-time model download  
To be connected to VPN using Azure VPN Client  


# Detection Default Parameters (may be changed in ocr_detection.py)

## EasyOCR

text_threshold: 0.5 - Minimum confidence score for detected text to be considered valid  
low_text: 0.3 - Threshold for detecting low-confidence text regions  
link_threshold: 0.4 - Threshold for linking text boxes to form a complete word/line  

## PaddleOCR

det_algorithm: 'DB' - Detection algorithm to use ('DB' for Differentiable Binarization)  
det_db_thresh: 0.3 - Threshold for binarization during text box detection  
det_db_box_thresh: 0.25 - Confidence score threshold for retaining detected text boxes  
det_db_unclip_ratio: 1.5 - Expansion ratio to enlarge detected text boxes  
det_max_candidates: 10000 - Maximum number of text boxes to process in a single image  
det_db_min_area: 3 - Minimum area of a detected box to be considered valid  
det_db_score_mode: "fast" - Mode for calculating box confidence scores ("fast" or "slow")  


# Visualization

The library includes utilities for visualizing detected text regions. Example:  

import matplotlib.pyplot as plt  
import cv2  

## Read and process image
img = cv2.imread(image_path)  
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
img_with_boxes = img.copy()  

## Draw bounding boxes
plt.figure(figsize=(15,15))  
for box in result:  
    x1, y1 = box[0]  
    x2, y2 = box[1]  
    cv2.rectangle(img_with_boxes,  
                 (int(x1), int(y1)),  
                 (int(x2), int(y2)),  
                 (0, 255, 255),  
                 1)  

plt.imshow(img_with_boxes)  
plt.show()  
