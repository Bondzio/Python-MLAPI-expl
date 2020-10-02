# You can write R code here and then click "Run" to run it on our platform

# library(readr)

# # The competition datafiles are in the directory ../input
# # Read competition data files:
# train <- read_csv("../input/train.csv")
# test <- read_csv("../input/test.csv")

# # Write to the log:
# cat(sprintf("Training set has %d rows and %d columns\n", nrow(train), ncol(train)))
# cat(sprintf("Test set has %d rows and %d columns\n", nrow(test), ncol(test)))

# Generate output files with write_csv(), plot() or ggplot()
# Any files you write to the current directory get shown as outputs
import numpy
from sklearn.decomposition import PCA
from sklearn.svm import SVC

COMPONENT_NUM = 35

print('Read training data...')
with open('../input/train.csv', 'r') as reader:
    reader.readline()
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(int, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

print('Reduction...')
train_label = numpy.array(train_label)
train_data = numpy.array(train_data)
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)

print('Train SVM...')
svc = SVC()
svc.fit(train_data, train_label)

print('Read testing data...')
with open('../input/test.csv', 'r') as reader:
    reader.readline()
    test_data = []
    for line in reader.readlines():
        pixels = list(map(int, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = numpy.array(test_data)
test_data = pca.transform(test_data)
predict = svc.predict(test_data)

print('Saving...')
with open('predict.csv', 'w') as writer:
    writer.write('"ImageId","Label"\n')
    count = 0
    for p in predict:
        count += 1
        writer.write(str(count) + ',"' + str(p) + '"\n')