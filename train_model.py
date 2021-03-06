# import the necessary packages
import tensorflow.python.keras.applications.mobilenet_v2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.applications import NASNetMobile
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
#Change the preprocess according to the model used
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
import pandas as pd
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os

def autoAI(DIRECTORY):
    # initialize the initial learning rate, number of epochs to train for,
    # and batch size
    INIT_LR = 1e-4
    EPOCHS = 2
    BS = 64


    CATEGORIES = ["NFMD", "IFMD", "CFMD"]

    # grab the list of images in our dataset directory, then initialize
    # the list of data (i.e., images) and class images
    print("[INFO] loading images...")

    data = []
    labels = []

    try:
        tf_gpus = tf.config.list_physical_devices('GPU')
        for gpu in tf_gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except:
        pass

    for category in CATEGORIES:
        path = os.path.join(DIRECTORY, category)
        #class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_path = os.path.join(path, img)
                image = load_img(img_path)#image = load_img(img_path, target_size=(224, 224))
                image = img_to_array(image)
                #change preprocess according to model
                image = tf.keras.applications.densenet.preprocess_input(image)
                data.append(image)
                labels.append(category)
                print(img_path)
            except Exception:
                pass

    # perform one-hot encoding on the labels
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)

    #print(labels[0])

    #labels = to_categorical(labels)

    #print(labels)

    data = np.array(data, dtype="float32")
    labels = np.array(labels, dtype="float32")

    print(data.shape)
    print(labels.shape)

    (trainX, testX, trainY, testY) = train_test_split(data, labels,
                                                      test_size=0.20, stratify=labels, random_state=42)

    aug = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")

    # load the CNN, ensuring the head FC layer sets are
    # Change the model accordingly
    baseModel = tf.keras.applications.DenseNet201(weights="imagenet", include_top=False,
                            input_tensor=Input(shape=(128, 128, 3)))

    # construct the head of the model that will be placed on top of the
    # the base model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(64, activation="relu")(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(3, activation="softmax")(headModel)

    # place the head FC model on top of the base model (this will become
    # the actual model we will train)
    model = Model(inputs=baseModel.input, outputs=headModel)

    print(model.summary())

    # loop over all layers in the base model and freeze them so they will
    # *not* be updated during the first training process
    for layer in baseModel.layers:
        layer.trainable = False

    # compile our model
    print("[INFO] compiling model...")
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)

    #create a checkpoint
    checkpoint_path = "models/densenet201.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,)

    #load weights
    model.load_weights(checkpoint_path)

    model.compile(loss="binary_crossentropy", optimizer=opt,
                  metrics=["accuracy"])

    # train the head of the network
    print("[INFO] training head...")
    H = model.fit(
        aug.flow(trainX, trainY, batch_size=BS),
        steps_per_epoch=len(trainX) // BS,
        validation_data=(testX, testY),
        validation_steps=len(testX) // BS,
        epochs=EPOCHS,
        callbacks=[cp_callback])

    # make predictions on the testing set
    print("[INFO] evaluating network...")
    predIdxs = model.predict(testX, batch_size=BS)

    # for each image in the testing set we need to find the index of the
    # label with corresponding largest predicted probability
    predIdxs = np.argmax(predIdxs, axis=1)

    # show a nicely formatted classification report
    print(classification_report(testY.argmax(axis=1), predIdxs,
                                target_names=lb.classes_))

    # serialize the model to disk
    print("[INFO] saving mask detector model...")
    #model.save_weights('Nasnet_model')
    #model.save("Nasnet.model", save_format="h5")
    model.save_weights(checkpoint_path)
    model.save("saved_model/Densenet201")
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in H.history.items()]))
    df.to_csv('densenet201.csv', mode='a', header=False, index=False)

#autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_1")
#import sys
#sys.exit()
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_2")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_3")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_4")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_5")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_6")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_7")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_8")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_9")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_10")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_11")
autoAI(r"C:\Users\marka\OneDrive\Documents\Thesis\Datasets\Exp_Batch_12")
'''
# plot the training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("MobileNetV2.png")
'''