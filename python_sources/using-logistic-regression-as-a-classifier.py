#!/usr/bin/env python
# coding: utf-8

# # <center> Machine Learning </center>
# # <center> Recognizing Iris flowers </center>
# # <center> Using Multinomial Logistic Regression as a Classifier </center>

# # 1. Introduction
# 
# <p style="text-align: justify;">This first homework has to do with the classical problem of recognizing different species of Iris flowers relying on the [Iris flower dataset](https://en.wikipedia.org/wiki/Iris_flower_data_set).</p>
# 
# <p style="text-align: justify;">The Iris flower data set or Fisher's Iris data set is a multivariate data set introduced by [Ronald Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher) in his 1936 paper *"The use of multiple measurements in taxonomic problems as an example of linear discriminant analysis"*.</p>
# 
# * The data set consists of 50 samples from each of three species of Iris (*Iris setosa*, *Iris virginica* and *Iris versicolor*). 
# * Four features were measured from each sample, the length and the width of the sepals and petals, in centimeters. 
# * Based on the combination of these four features, Fisher developed a linear discriminant model to distinguish the species from each other.
# 
# Similarly, we will use this homework to get you familiarized with `numpy` and `scikit-learn`.

# <div class="container-fluid">
#   <div class="row">
#       <div class="col-md-2" align='center'>
#       </div>
#       <div class='col-md-8' align='center'>
#            <img src='https://s3.amazonaws.com/assets.datacamp.com/blog_assets/iris-machinelearning.png' />
#       </div>
#       <div class="col-md-2" align='center'></div>
#   </div>
# </div>

# ## Python Libraries 
# 
# In the first place, Let's define some libraries to help us in the manipulation the data set, such as `numpy`, `matplotlib`, `seaborn` and `scikit-learn`. 

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import seaborn

seaborn.set(style='whitegrid'); seaborn.set_context('talk')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

from sklearn.datasets import load_iris
iris_data = load_iris()


# ## An analysis about the problem 
# 
# Before, It is necessary define some things about problem. First, We have 4-inputs related each ``y`` output. Our number of instances is equal to 150 samples (50 in each of three classes to classification).
# * **The x inputs are arranged as follows:** 
#      - For $x[0]$ : Sepal Width in cm
#      - For $x[1]$ : Sepal Length in cm
#      - For $x[2]$ : Petal Width in cm
#      - For $x[3]$ : Petal Length in cm
#      
# * **The y outputs are arranged as follows:**
#      - $if$ $y = 0$, $then$: Iris-Setosa
#      - $if$ $y = 1$, $then$: Iris-Versicolour 
#      - $if$ $y = 2$, $then$: Iris-Virginica
#      
# * ** Algorithms used in this work:**
#      - An Artificial Neural Network called **Multilayer Perceptron**
#      - An Logistic Regression called **Multinomial Logistic Regression**
#      
#  

# In[ ]:


print(iris_data['DESCR'])


# In[ ]:


n_samples, n_features = iris_data.data.shape

def Show_Diagram(x_label,y_label,title):
    plt.figure(figsize=(10,4))
    plt.scatter(iris_data.data[:,x_label], iris_data.data[:,y_label], c=iris_data.target, cmap=cm.viridis)
    plt.xlabel(iris_data.feature_names[x_label]); plt.ylabel(iris_data.feature_names[y_label]); plt.title(title)
    plt.colorbar(ticks=([0, 1, 2]));plt.show();x_label = 2;y_label=3;title='Petal'

Show_Diagram(0,1,'Sepal')
Show_Diagram(2,3,'Petal')


# ## Separate and analyze our iris data-set 
# 
# It is here that we will select our samples to train and test the algorithms. 
# 
# #### 80% training and 20% test
# <div class="container-fluid">
#   <div class="row">
#       <div class="col-md-2" align='center'>
#       </div>
#       <div class='col-md-8' align='center'>
#       </div>
#       <div class="col-md-2" align='center'></div>
#   </div>
# </div>

# In[ ]:


random.seed(123)

def separate_data():
    ""
    A = iris_dataset[0:40]
    tA = iris_dataset[40:50]
    B = iris_dataset[50:90]
    tB = iris_dataset[90:100]
    C = iris_dataset[100:140]
    tC = iris_dataset[140:150]
    train = np.concatenate((A,B,C))
    test =  np.concatenate((tA,tB,tC))
    return train,test

train_porcent = 80 # Train
test_porcent = 20 # Test
iris_dataset = np.column_stack((iris_data.data,iris_data.target.T)) #Join X and Y
iris_dataset = list(iris_dataset)
random.shuffle(iris_dataset)

train_file , test_file = separate_data()

train_X = np.array([k[:4] for k in train_file])
train_y = np.array([k[4] for k in train_file])
test_X = np.array([k[:4] for k in test_file])
test_y = np.array([k[4] for k in test_file])


# ## Show training samples

# In[ ]:


plt.figure(figsize=(10,10));plt.subplot(2,2,3)
plt.scatter(train_X[:,0],train_X[:,1],c=train_y,cmap=cm.viridis)
plt.xlabel(iris_data.feature_names[0]); plt.ylabel(iris_data.feature_names[1]) 

plt.subplot(2,2,4);plt.scatter(train_X[:,2],train_X[:,3],c=train_y,cmap=cm.viridis)
plt.xlabel(iris_data.feature_names[2]); plt.ylabel(iris_data.feature_names[3])


# In[ ]:


import pandas
from pandas.plotting import scatter_matrix


dataset = pandas.read_csv('../input/iris/Iris.csv')
scatter_matrix(dataset, alpha=0.5, figsize=(20, 20))
plt.show()


# In[ ]:


dataset.hist(alpha=0.5, figsize=(20, 20), color='green')
plt.show()


# ## Show test samples

# In[ ]:


plt.figure(figsize=(10,10));plt.subplot(2,2,1)
plt.scatter(test_X[:,0],test_X[:,1],c=test_y,cmap=cm.viridis)
plt.xlabel(iris_data.feature_names[0]); plt.ylabel(iris_data.feature_names[1]) 

plt.subplot(2,2,2);plt.scatter(test_X[:,2],test_X[:,3],c=test_y,cmap=cm.viridis)
plt.xlabel(iris_data.feature_names[2]); plt.ylabel(iris_data.feature_names[3])


# # Multinomial Logistic Regression (Softmax Regression)
# 
# <p style="text-align: justify;"> In statistics, multinomial logistic regression is a classification method that generalizes logistic regression to multiclass problems, i.e. with more than two possible discrete outcomes. This is a model used to predict the probabilities of the different possible outcomes of a categorically distributed dependent variable, given a set of independent variables (which may be real-valued, binary-valued, categorical-valued).</p>
# 
# <p style="text-align: justify;"> **Multinomial logistic regression ** is known by a variety of other names, including polytomous LR, multiclass LR, softmax regression, multinomial logit, maximum entropy (MaxEnt) classifier, conditional maximum entropy
# model.</p>
# 
# <p style="text-align: justify;"> ** More information about it: [Softmax Regression](https://en.wikipedia.org/wiki/Multinomial_logistic_regression)** </p> 
# 
# 
# 

# ## How does Multinomial logistic classifier work?
# 
# <img src="https://i2.wp.com/dataaspirant.com/wp-content/uploads/2017/03/Multinomial-Logistic-Classifier-compressor.jpg?resize=690%2C394">
# ### Step 1. Get Z value
# <p style="text-align: justify;"> First, Let's get Z value :
# $\text Z = \sum_{i=0}^n w_i x_i\, = w_0 x_0 + w_1 x_1 + w_2 x_2 + ... + w_n x_n $</p>
# 
# ### Step 2. Cost Function J
# <p style="text-align: justify;">  It is function that we need to minimize, which it is calculated as follow:</p>
# $$\text J(W) = \frac{1}{n} \sum_{i=0}^n H(T_i, O_i) $$
# 
# where, $ H(T_i, O_i)$ or cross-entropy is defined as: 
# $$\text H(T_i, O_i) = - \sum_{n} T_i \cdot log(O_i) $$
# 
# ### Step 3. Softmax Function 
# <img src="https://deepnotes.io/public/images/softmax.png">
# <p style="text-align: justify;">The softmax function is used in various ** multiclass classification methods **, such as multinomial logistic regression, multiclass linear discriminant analysis, naive Bayes classifiers, and artificial neural networks.</p>
# $$ p(y = j | x) = \frac{e^{z.T}}{\sum_{i = 1}^n {e^{z.T}}} $$
# 
# ### Step 4. Learn using Gradient Descent 
# 
# <img src="https://thumbs.gfycat.com/AngryInconsequentialDiplodocus-size_restricted.gif">
# <p style="text-align: justify;"> To this work, the implementation Softmax Regression using gradient descent that It is defined as: $ W_{ij} = W_{ij} - \gamma \cdot \nabla_{Wj}J(W) $ </p>Where :
# $ \nabla_{Wj} J(W) $ is **cost derivative** defined as:
# $$ \nabla_{Wj} J(W) = -\frac{1}{n} \sum_{i = 0}^n (X^{(i)} (T_i - O_i))$$

# ## Implementation Multinomial logistic (Softmax Regression)
# 
# 
# <div class="container-fluid">
#   <div class="row">
#       <div class="col-md-2" align='center'>
#       </div>
#       <div class='col-md-8' align='center'>
#       </div>
#       <div class="col-md-2" align='center'></div>
#   </div>
# </div>
# 

# In[ ]:


from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin

class Multinomial_Regression(BaseEstimator, ClassifierMixin): 
    def __init__(self, X, y,params=None):     
        if (params == None):
            self.learningRate = 0.005                  # Learning Rate
            self.max_epoch = 3000                      
        else:
            self.learningRate = params['LearningRate']
            self.max_epoch = params['Epoch'] # Epochs
           
        self.weight = np.array([[0.1,0.2,0.3],
                               [0.1,0.2,0.3],
                               [0.1,0.2,0.3],
                               [0.1,0.2,0.3]])
    pass

    def cost_derivate_gradient(self,n,Ti,Oi, X):
        result = -(np.dot(X.T,(Ti - Oi)))/n   
        return result 

    def function_cost_J(self,n,Ti,Oi):
        result = -(np.sum(Ti * np.log(Oi)))/n 
        return result
    
    def one_hot_encoding(self,Y):
        OneHotEncoding = []
        encoding = []
        for i in range(len(Y)):
            if(Y[i] == 0): encoding = np.array([1,0,0]) #Class 1, if y = 0
            elif(Y[i] == 1): encoding = np.array([0,1,0]) #Class 2, if y = 1
            elif(Y[i] == 2): encoding = np.array([0,0,1]) #Class 3, if y = 2

            OneHotEncoding.append(encoding)
        return OneHotEncoding
    
    def accuracy_graphic(self, answer_graph):
        labels = 'Hits', 'Faults'
        sizes = [96.5, 3.3]
        explode = (0, 0.14)
        fig1, ax1 = plt.subplots()
        ax1.pie(answer_graph, explode=explode, colors=['green','red'], labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()

    def softmax(self,z):
        soft = (np.exp(z).T / np.sum(np.exp(z),axis=1)).T 
        return soft
    
    def show_probability(self, arrayProbability):
        print("Probability: [ Class 0 ,  Class 1 , Class 2 ]")
        
        arrayTotal = []
        for k in arrayProbability:
            k[0] = "%.3f" % k[0]
            k[1] = "%.3f" % k[1]
            k[2] = "%.3f" % k[2]
            arrayTotal.append(k)
            
        id_ = 0
        for k in arrayTotal:
            prob0 = k[0] * 100
            prob1 = k[1] * 100
            prob2 = k[2] * 100
            id_ += 1
            string = "         {}:  {}%,   {}%,   {}%".format(id_, "%.3f" % prob0, 
                                                                   "%.3f" % prob1, 
                                                                   "%.3f" % prob2)
            print(string)
        
    def predict(self, X,y):
        acc_set = acc_vers = acc_virg = 0
        v_resp = []
        n = len(y)
        Z = np.matmul(X, self.weight)
        Oi = self.softmax(Z)
        prevision = np.argmax(Oi,axis=1)
        self.show_probability(Oi)
        print("")
        procent = sum(prevision == y)/n
        print(" ID-Sample  | Class Classification |  Output |   Hoped output  ")  
        for i in range(len(prevision)):
            if(prevision[i] == 0): print(" id :",i,"          | Iris-Setosa        |  Output:",prevision[i],"   |",y[i])
            elif(prevision[i] == 1): print(" id :",i,"          | Iris-Versicolour   |  Output:",prevision[i],"   |",y[i])
            elif(prevision[i] == 2): print(" id :",i,"          | Iris-Virginica     |  Output:",prevision[i],"   |",y[i])
                
        for i in range(len(prevision)):
            if((prevision[i] == y[i])and(prevision[i] == 0)):acc_set+=1
            elif((prevision[i] == y[i])and(prevision[i] == 1)):acc_vers+=1
            elif((prevision[i] == y[i])and(prevision[i] == 2)):acc_virg+=1
               
        correct = procent * 100
        incorrect = 100 - correct
        v_resp.append(correct)
        v_resp.append(incorrect)
        self.accuracy_graphic(v_resp)
        return "%.2f"%(correct), acc_set, acc_vers, acc_virg

    def show_err_graphic(self,v_epoch,v_error):
        plt.figure(figsize=(9,4))
        plt.plot(v_epoch, v_error, "m-")
        plt.xlabel("Number of Epoch")
        plt.ylabel("Error")
        plt.title("Error Minimization")
        plt.show()

    def fit(self,X,y):
        v_epochs = []
        totalError = []
        epochCount = 0
        n = len(X)
        gradientE = []
        while(epochCount < self.max_epoch):
            Ti = self.one_hot_encoding(y)
            Z = np.matmul(X,self.weight)
            Oi = self.softmax(Z)
            erro = self.function_cost_J(n,Ti,Oi)
            gradient = self.cost_derivate_gradient(n,Ti,Oi,X)
            self.weight = self.weight - self.learningRate * gradient
            if(epochCount % 100 == 0):
                totalError.append(erro)
                gradientE.append(gradient)
                v_epochs.append(epochCount)
                print("Epoch ",epochCount," Total Error:", "%.4f" % erro)
            
            epochCount += 1
        
        self.show_err_graphic(v_epochs,totalError)
        return self


# ## "Training" with Softmax and Gradient Descent
# 
# <img src="https://i0.wp.com/dataaspirant.com/wp-content/uploads/2017/03/Multinomial-Logistic-Regression-model.jpg?resize=690%2C394">
# 

# In[ ]:


arguments = {'Epoch':6000, 'LearningRate':0.005}
SoftmaxRegression = Multinomial_Regression(train_X,train_y,arguments)
SoftmaxRegression.fit(train_X,train_y)


# ##  Accuracy and precision the Multinomial Regression

# In[ ]:


acc_test,test_set,test_vers,test_virg = SoftmaxRegression.predict(test_X,test_y)
print("Hits - Porcent (Test): ", acc_test,"% hits")


# ## Score Iris-Flowers dataset

# In[ ]:


n_set = 0;n_vers = 0;n_virg = 0;
for i in range(len(test_y)):
    if(test_y[i] == 0):n_set+=1
    elif(test_y[i] == 1):n_vers+=1
    elif(test_y[i] == 2):n_virg+=1
        
ac_set = (test_set/n_set)*100
ac_vers = (test_vers/n_vers)*100
ac_virg = (test_virg/n_virg)*100
print("- Acurracy Iris-Setosa:","%.2f"%ac_set, "%")
print("- Acurracy Iris-Versicolour:","%.2f"%ac_vers, "%")
print("- Acurracy Iris-Virginica:","%.2f"%ac_virg, "%")
ig, ax = plt.subplots()
names = ["Setosa","Versicolour","Virginica"]
x1 = [2.0,4.0,6.0]
plt.bar(x1[0], ac_set,color='orange')
plt.bar(x1[1], ac_vers,color='g')
plt.bar(x1[2], ac_virg,color='purple',label='Iris-Virginica')
plt.ylabel('Scores %')
plt.xticks(x1, names)
plt.title('Scores by iris flowers - M.Logistic Regression')
plt.show()


# ## References
# 
# **[1]** BROWNLEE, Jason. ** Overfitting and Underfitting With Machine Learning Algorithms(2016)**. Site: [Machine Learning Mastery](https://machinelearningmastery.com/)
# 
# 

# Other examples on my Github: https://github.com/vitorglemos/MultilayerPerceptron/
