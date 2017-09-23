import tensorflow as tf
import numpy as np
import pandas as pd
import json
import csv

def main():
    #["fancy", "casual"]
    articles = '[{"type": "shorts", "color": "blue", "style": "fancy"}, {"type": "jeans", "color": "blue", "style": "fancy"}]' #weather, #"outfits.json"
    testArticles = '[{"type": "pants", "color": "green", "style": "fancy"}, {"type": "jeans", "color": "black", "style": "fancy"}]' #weather, #"outfits.json"
    parsedArticles = json.loads(articles)
    parsedTestArticles = json.loads(testArticles)
    print(parsedArticles)
    f = csv.writer(open("articles.csv", "wb+"))
    print(csv.list_dialects())
    f.writerow(["type", "color", "style"])
    for i in range(0, parsedArticles.__len__()):
        #print(parsedArticles[0]["type"])
        f.writerow(parsedArticles[i]['type']) #, parsedArticles[1], parsedArticles[2]])
        f.writerow(parsedArticles[i]['color'])
        f.writerow(parsedArticles[i]['style'])

    training = tf.contrib.learn.datasets.base.load_csv_without_header("articles.csv", np.int, np.float32)#int) string_

    for i in range(0, parsedArticles.__len__()):
        print("article 0 color is: "+ parsedArticles[0]['color'])

    feature_columns = [tf.feature_column.numeric_column("x", shape=[4])]
    #sparse1 = sparse_column_with_hash_bucket()
    classifier = tf.estimator.DNNClassifier(feature_columns = feature_columns, hidden_units=[10,20,10], n_classes = 3, model_dir="~/Desktop/closet")
    #[1024, 512, 256]

    train_input = tf.estimator.inputs.pandas_input_fn(x=np.array(training.data), y=np.array(training.target), num_epochs=3, shuffle=True)
    #{"x": np.array(training.data)}
    classifier.train(input_fn=train_input, steps=2000)

    predict_input = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(parsedArticles)}, num_epochs=1, shuffle=False) #cant we use the same data for now?

#convert back good outfits to json
    predictions = list(classifier.predict(input_fn=predict_input))
    #def input_train():
        #classifier.train(input_fn=input_train, steps=100)

    #def input_eval():
        #classifier.evaluate(input_fn=input_eval, steps=10)

    #def input_predict:
       # prediction = classifier.predict(input_fn=input_predict)

if __name__ == '__main__':
    main()