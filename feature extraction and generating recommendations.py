# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KLd2Ur15uK97C9aPmlJ7rJ-okhCZaBgA
"""

!pip install ultralytics
from ultralytics import YOLO

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from keras.models import Model
from tensorflow.keras import Sequential
from keras.utils import plot_model
import keras
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pickle
from sklearn.neighbors import NearestNeighbors

img_path = "/content/drive/MyDrive/dataset/test_2/images/img_00001445.jpg"

model = YOLO('/content/drive/MyDrive/runs 2/detect/yolov8n_v8/weights/best.pt')
results = model.predict(img_path)
res = results[0]

boxes = res.boxes
box = boxes[0]
coords = (box.xyxy[0]).tolist()
for i in range(len(coords)):
  coords[i] = round(coords[i])

res = res.plot()
req_img = res[coords[1]:coords[3], coords[0]:coords[2]]

resnet = ResNet50(include_top = False, weights = 'imagenet', input_shape = (224,224,3))
resnet.trainable = False
model  = Sequential([resnet, GlobalMaxPooling2D()])
model.summary()

def feature_extractor(img, model):

  img = cv2.resize(img,(224,224))
  expand_img = np.expand_dims(img,axis = 0)
  preprocessed_img  = preprocess_input(expand_img)
  predicted  = model.predict(preprocessed_img)
  res = predicted / np.linalg.norm(predicted)

  return res.flatten()

feature_list = np.array(pickle.load(open('/content/drive/MyDrive/runs 2/embeddings.pkl','rb')))
file_names = pickle.load(open('/content/drive/MyDrive/runs 2/file_names.pkl','rb'))

inp = feature_extractor(req_img, model)
neighbors = NearestNeighbors(n_neighbors = 5, algorithm = 'brute', metric= 'euclidean').fit(feature_list)
distances,indices = neighbors.kneighbors([inp])

for index in indices[0] :
    img = cv2.imread(file_names[index])
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.imshow(img_rgb)
    plt.axis('off')  # To remove axes and ticks
    print(distances)
    plt.show()

def feature_extractor(img_path, model):

  img = cv2.imread(img_path)
  img = cv2.resize(img,(224,224))
  preprocessed_img  = preprocess_input(img)
  plt.imshow(preprocessed_img)
  plt.show()

feature_extractor('/content/drive/MyDrive/dataset/test_2/images/img_00012524.jpg',model)

