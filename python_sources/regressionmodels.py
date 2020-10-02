#=======================================================================
#Using Keras with tensorflow backend
#=======================================================================
import sys, csv
import numpy as np
import keras
import matplotlib.pyplot as plt
from keras import models
from keras import layers
from keras.utils.np_utils import to_categorical

debug = 1

def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

def Regression_DistrictCrimes():
    Train_Data_List = []
    Train_Target_List = []

    with	open('../input/crime_by_district_rt.csv',	'r')	as	f:
        reader	=	csv.DictReader(f,	delimiter=',')
        for	row	in	reader:
            Murder	=	float(row["Murder"])
            Assault_on_women    =   float(row["Assault on women"])
            Kidnapping_and_Abduction  =	float(row["Kidnapping and Abduction"])
            Dacoity	=	float(row["Dacoity"])
            Robbery	=	float(row["Robbery"])
            Arson	=	float(row["Arson"])
            Hurt	=	float(row["Hurt"])
            POA	    =	float(row["Prevention of atrocities (POA) Act"])
            PCR	    =	float(row["Protection of Civil Rights (PCR) Act"])
            Other	=	float(row["Other Crimes Against SCs"])
        
            Train_Data_List.append([Murder, Assault_on_women, Kidnapping_and_Abduction, Dacoity, Robbery, Arson, Hurt, POA, PCR])
            Train_Target_List.append(Other)

    if debug != 0:
        print("=======================Training data=======================")
        print(Train_Data_List)
        print("=========================Test data=========================")
        print(Train_Target_List)


    #=======================================================================
    #Convert the data into 2D Tensors
    #=======================================================================

    train_data =  np.array(Train_Data_List);
    train_targets = np.array(Train_Target_List);

    if debug != 0:
        print("===========================================================")
        print("========================2D tensors=========================")
        print("===========================================================")
        print("=======================Training data=======================")
        print(train_data)
        print(train_data.shape)
        print("=========================Test data=========================")
        print(train_targets)
        print(train_targets.shape)

    #=======================================================================
    #Normalize the training and test data
    #=======================================================================

    mean = train_data.mean(axis=0)
    train_data -= mean
    std = train_data.std(axis=0)
    train_data /= std

    #=======================================================================
    #Deep learning regression model architecture as a function
    #=======================================================================

    def build_model():
        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1))
        model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
        return model


    #=======================================================================
    #Training and save the validation logs at each fold
    #=======================================================================

    k = 4
    num_val_samples = len(train_data) // k
    num_epochs = 1000
    all_mae_histories = []
    for i in range(k):
        print('processing fold #', i)
    
        val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
        val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]
    
        partial_train_data = np.concatenate([train_data[:i * num_val_samples], train_data[(i + 1) * num_val_samples:]], axis=0)
        partial_train_targets = np.concatenate([train_targets[:i * num_val_samples], train_targets[(i + 1) * num_val_samples:]], axis=0)
    
        model = build_model()
        history = model.fit(partial_train_data, partial_train_targets, validation_data=(val_data, val_targets), epochs=num_epochs, batch_size=500, verbose=0)
    
        mae_history = history.history['val_mean_absolute_error']
        all_mae_histories.append(mae_history)


    #model = build_model()
    #model.fit(train_data, train_targets,epochs=num_epochs, batch_size=32, verbose=0)
    #model.save('mpc.h5')

    #=======================================================================
    #Calucate and store the mean MAE for each fold
    #=======================================================================

    average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

    #=======================================================================
    #Plot the validation scores using matplotlib
    #=======================================================================

    #plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
    #plt.xlabel('Epochs')
    #plt.ylabel('Validation MAE')
    #plt.show()

    smooth_mae_history = smooth_curve(average_mae_history[10:])
    
    plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
    plt.xlabel('Epochs')
    plt.ylabel('Validation MAE')
    plt.show()

def Regression_StateCrimes():
    Train_Data_List = []
    Train_Target_List = []

    with	open('../input/crime_by_state_rt.csv',	'r')	as	f:
        reader	=	csv.DictReader(f,	delimiter=',')
        for	row	in	reader:
            Murder	=	float(row["Murder"])
            Assault_on_women    =   float(row["Assault on women"])
            Kidnapping_and_Abduction  =	float(row["Kidnapping and Abduction"])
            Dacoity	=	float(row["Dacoity"])
            Robbery	=	float(row["Robbery"])
            Arson	=	float(row["Arson"])
            Hurt	=	float(row["Hurt"])
            POA	    =	float(row["Prevention of atrocities (POA) Act"])
            PCR	    =	float(row["Protection of Civil Rights (PCR) Act"])
            Other	=	float(row["Other Crimes Against SCs"])
        
            Train_Data_List.append([Murder, Assault_on_women, Dacoity, Robbery, Arson, Hurt, POA, PCR, Other])
            Train_Target_List.append(Kidnapping_and_Abduction)
    if debug != 0:
        print("=======================Training data=======================")
        print(Train_Data_List)
        print("=========================Test data=========================")
        print(Train_Target_List)


    #=======================================================================
    #Convert the data into 2D Tensors
    #=======================================================================

    train_data =  np.array(Train_Data_List);
    train_targets = np.array(Train_Target_List);

    if debug != 0:
        print("===========================================================")
        print("========================2D tensors=========================")
        print("===========================================================")
        print("=======================Training data=======================")
        print(train_data)
        print(train_data.shape)
        print("=========================Test data=========================")
        print(train_targets)
        print(train_targets.shape)

    #=======================================================================
    #Normalize the training and test data
    #=======================================================================

    mean = train_data.mean(axis=0)
    train_data -= mean
    std = train_data.std(axis=0)
    train_data /= std

    #=======================================================================
    #Deep learning regression model architecture as a function
    #=======================================================================

    def build_model():
        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1))
        model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
        return model


    #=======================================================================
    #Training and save the validation logs at each fold
    #=======================================================================

    k = 4
    num_val_samples = len(train_data) // k
    num_epochs = 200
    all_mae_histories = []
    for i in range(k):
        print('processing fold #', i)
    
        val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
        val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]
    
        partial_train_data = np.concatenate([train_data[:i * num_val_samples], train_data[(i + 1) * num_val_samples:]], axis=0)
        partial_train_targets = np.concatenate([train_targets[:i * num_val_samples], train_targets[(i + 1) * num_val_samples:]], axis=0)
    
        model = build_model()
        history = model.fit(partial_train_data, partial_train_targets, validation_data=(val_data, val_targets), epochs=num_epochs, batch_size=100, verbose=0)
    
        mae_history = history.history['val_mean_absolute_error']
        all_mae_histories.append(mae_history)


    #model = build_model()
    #model.fit(train_data, train_targets,epochs=num_epochs, batch_size=32, verbose=0)
    #model.save('mpc.h5')

    #=======================================================================
    #Calucate and store the mean MAE for each fold
    #=======================================================================

    average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

    #=======================================================================
    #Plot the validation scores using matplotlib
    #=======================================================================

    #plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
    #plt.xlabel('Epochs')
    #plt.ylabel('Validation MAE')
    #plt.show()

    smooth_mae_history = smooth_curve(average_mae_history[10:])
    
    plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
    plt.xlabel('Epochs')
    plt.ylabel('Validation MAE')
    plt.show()
    
Regression_StateCrimes()
