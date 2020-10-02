import matplotlib.pyplot as pltimport numpy as np # linear algebraimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)import kerasfrom keras.layers import Densefrom keras.models import Model,Sequentialfrom keras.optimizers import SGD,Adamfrom keras.utils import to_categoricalfrom keras.datasets import mnist(x_train, y_train), (x_test, y_test) = mnist.load_data()image_vector_size = 28*28x_train = x_train.reshape(x_train.shape[0], image_vector_size)x_test = x_test.reshape(x_test.shape[0], image_vector_size)num_classes = 10y_train = keras.utils.to_categorical(y_train, num_classes)y_test = keras.utils.to_categorical(y_test, num_classes)image_size = 784 # 28*28#Your 4 layers are killing model accuracy, accuracies-: 1 layer-.95, 2 layer- .87, 3 layer- .43, 4 layer- .114# Reduce to 2 or 3 layers for better performancemodel = Sequential()model.add(Dense(1000,activation='relu',input_shape=(image_size,)))model.add(Dense(1000,activation='relu'))model.add(Dense(500,activation='relu'))model.add(Dense(200,activation='relu'))model.add(Dense(10,activation='softmax'))model.summary()model.compile(optimizer='sgd',loss='categorical_crossentropy',metrics=['accuracy'])history = model.fit(x_train, y_train, batch_size=128, epochs=5, verbose=False, validation_split=.3)loss, accuracy  = model.evaluate(x_test, y_test, verbose=False)plt.plot(history.history['acc'])plt.plot(history.history['val_acc'])plt.title('model accuracy')plt.ylabel('accuracy')plt.xlabel('epoch')plt.legend(['training', 'validation'], loc='best')plt.show()print(loss)print(accuracy)