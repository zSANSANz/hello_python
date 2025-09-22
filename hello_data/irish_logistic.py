import Orange

# load dataset iris
data = Orange.data.Table("iris")

# bagi data training & test
train, test = data[:100], data[100:]

# pakai Logistic Regression
learner = Orange.classification.LogisticRegressionLearner()
classifier = learner(train)

# uji prediksi
for d in test[:5]:
    pred = classifier(d)
    print(f"Asli: {d.get_class()} → Prediksi: {pred}")
