# https://towardsdatascience.com/an-in-depth-efficientnet-tutorial-using-tensorflow-how-to-use-efficientnet-on-a-custom-dataset-1cab0997f65c
from keras.applications import * #Efficient Net included here
from keras import models
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
import timm
import numpy as np
import os
import shutil
import pandas as pd
from sklearn import model_selection
from tqdm import tqdm
from keras import optimizers
import tensorflow as tf #Use this to check if the GPU is configured correctly
from tensorflow.python.client import device_lib

#print(device_lib.list_local_devices())
height, width = 460,460
input_shape=(height,width, 3)
conv_base = EfficientNetB6(weights="imagenet", include_top=False, input_shape=input_shape)

model = models.Sequential()
model.add(conv_base)
model.add(layers.GlobalMaxPooling2D(name="gap"))
#avoid overfitting
model.add(layers.Dropout(rate=0.2, name="dropout_out"))
# Set NUMBER_OF_CLASSES to the number of your final predictions.
NUMBER_OF_CLASSES = 10
model.add(layers.Dense(NUMBER_OF_CLASSES, activation="softmax", name="fc_out"))
conv_base.trainable = False

TRAIN_IMAGES_PATH = './efficientNet/imagenette2-160/images/train' #12000
VAL_IMAGES_PATH = './efficientNet/imagenette2-160/images/val' #3000
External_DIR = './efficientNet/imagenette2-160/train' # 15000
os.makedirs(TRAIN_IMAGES_PATH, exist_ok = True)
os.makedirs(VAL_IMAGES_PATH, exist_ok = True)

classes = [ "n01440764", "n02102040", "n02979186", "n03000684", "n03028079", "n03394916", "n03417042", "n03425413", "n03445777", "n03888257"]# Create directories for each class.
for class_id in [x for x in range(len(classes))]:
    os.makedirs(os.path.join(TRAIN_IMAGES_PATH, str(class_id)), exist_ok = True)
    os.makedirs(os.path.join(VAL_IMAGES_PATH, str(class_id)), exist_ok = True)

Input_dir = './efficientNet/imagenette2-160/train'
def preproccess_data(df, images_path):
    for column, row in tqdm(df.iterrows(), total=len(df)):
        class_id = row['class_id']
        shutil.copy(os.path.join(Input_dir, f"{row['image_id']}.png"), os.path.join(images_path, str(class_id)))
        
df = pd.read_csv('./efficientNet/imagenette2-160/train.csv')
df.head()#Split the dataset into 80% training and 20% validation
df_train, df_valid = model_selection.train_test_split(df, test_size=0.2, random_state=42, shuffle=True)#run the  function on each of them
preproccess_data(df_train, TRAIN_IMAGES_PATH)
preproccess_data(df_valid, VAL_IMAGES_PATH)

# I love the  ImageDataGenerator class, it allows us to specifiy whatever augmentations we want so easily...
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)# Note that the validation data should not be augmented!#and a very important step is to normalise the images through  rescaling
test_datagen = ImageDataGenerator(rescale=1.0 / 255)
batch_size = 1
train_generator = train_datagen.flow_from_directory(
    # This is the target directory
    TRAIN_IMAGES_PATH,
    # All images will be resized to target height and width.
    target_size=(height, width),
    batch_size=batch_size,
    # Since we use categorical_crossentropy loss, we need categorical labels
    class_mode="categorical",
)
validation_generator = test_datagen.flow_from_directory(
    VAL_IMAGES_PATH,
    target_size=(height, width),
    batch_size=batch_size,
    class_mode="categorical",
)
model.compile(
    loss="categorical_crossentropy",
    optimizer=optimizers.RMSprop(lr=2e-5),
    metrics=["acc"],
)

