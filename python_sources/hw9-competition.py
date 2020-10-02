import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from subprocess import check_output
import os, cv2, random
import numpy as np
import pandas as pd


from keras.models import Sequential
from keras.layers import Input, Dropout, Flatten, Convolution2D, MaxPooling2D, Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
from keras.utils import np_utils


TRAIN_DIR = '../input/train/'
TEST_DIR = '../input/test/'

ROWS = 64
COLS = 64
CHANNELS = 3

train_images = [TRAIN_DIR+i for i in os.listdir(TRAIN_DIR)] # use this for full dataset


test_images =  [TEST_DIR+i for i in os.listdir(TEST_DIR)]


def read_image(file_path):
    img = cv2.imread(file_path, cv2.IMREAD_COLOR) #cv2.IMREAD_GRAYSCALE
    return cv2.resize(img, (ROWS, COLS), interpolation=cv2.INTER_CUBIC)


def prep_data(images):
    count = len(images)
    data = np.ndarray((count, CHANNELS, ROWS, COLS), dtype=np.uint8)

    for i, image_file in enumerate(images):
        image = read_image(image_file)
        data[i] = image.T
        if i%250 == 0: print('Processed {} of {}'.format(i, count))
    
    return data

train = prep_data(train_images)
test = prep_data(test_images)

print("Train shape: {}".format(train.shape))
print("Test shape: {}".format(test.shape))

labels = []
for i in train_images:
    if 'dog' in i:
        labels.append(1)
    else:
        labels.append(0)

train = train.reshape(-1, 64,64,3)
test = test.reshape(-1, 64,64,3)
trainA= train.astype('float32')
testA= test.astype('float32')
trainA/= 255
testA/= 255
trainB=labels

validA= trainA[:3000,:,:,:]
validB=   trainB[:3000]
trainA= trainA[3001:20000,:,:,:]
trainB  = trainB[3001:20000]

print("Training matrix shape", trainA.shape)
print("Testing matrix shape", testA.shape)

model = Sequential()
model.add(Convolution2D(16, 3, 3, border_mode='same', input_shape=(ROWS, COLS, CHANNELS), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
                                 
model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])

model.fit(trainA, trainB,
          batch_size=128, nb_epoch=8,
          show_accuracy=True, verbose=1,
          validation_data=( validA, validB))
          
submission = model.predict_proba(testA, verbose=1)
test_id = range(1,12501)
predictions_df = pd.DataFrame({'id': test_id, 'label': submission[:,0]})

predictions_df.to_csv("submission.csv", index=False)



import pandas as pd 