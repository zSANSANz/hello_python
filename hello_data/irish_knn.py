import Orange

# load dataset iris
data = Orange.data.Table("iris")

# bagi data training & test
train, test = data[:100], data[100:]

# pakai algoritma kNN
learner = Orange.classification.KNNLearner()
classifier = learner(train)

# uji keakuratan
predictions = [classifier(instance) for instance in test]
print("Prediksi:", predictions[:5])
