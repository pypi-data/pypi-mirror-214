![GitHub Repo stars](https://img.shields.io/github/stars/drhosseinjavedani/fuzzylearn) ![GitHub forks](https://img.shields.io/github/forks/drhosseinjavedani/fuzzylearn) ![GitHub language count](https://img.shields.io/github/languages/count/drhosseinjavedani/fuzzylearn) ![GitHub repo size](https://img.shields.io/github/repo-size/drhosseinjavedani/fuzzylearn) ![GitHub](https://img.shields.io/github/license/drhosseinjavedani/fuzzylearn)![PyPI - Downloads](https://img.shields.io/pypi/dd/fuzzylearn) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fuzzylearn) 

# FuzzyLearn

FuzzyLearn is a new estimator for creating classification and regression estimators using fuzzy set concept. Some of it classes use [Optuna](https://optuna.readthedocs.io/en/stable/index.html) and [Ray tune Scikit-Learn API](https://docs.ray.io/en/latest/tune/api_docs/sklearn.html) to tune most of its hyper-parameters.


### Installation

FuzzyLearn package is available on PyPI and can be installed with pip:

```sh
pip install fuzzylearn
```

#### Example 1: Adult Dataset (Use FuzzyLearn as a Classifier)

```
from fuzzylearn.classification.fast.fast import FLClassifier
from sklearn.metrics import classification_report,confusion_matrix,f1_score,roc_auc_score
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from category_encoders import OrdinalEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import time
from sklearn.model_selection import train_test_split
import ray

urldata = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
# column names
col_names = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "label",
]
# read data
data = pd.read_csv(urldata, header=None, names=col_names, sep=",")
# use sample of 1000 rows of data only
data = data.sample(20000)
data.head()

data.loc[data["label"] == "<=50K", "label"] = 0
data.loc[data["label"] == " <=50K", "label"] = 0

data.loc[data["label"] == ">50K", "label"] = 1
data.loc[data["label"] == " >50K", "label"] = 1

data["label"] = data["label"].astype(int)

# Train test split

X = data.loc[:, data.columns != "label"]
y = data.loc[:, data.columns == "label"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, stratify=y["label"], random_state=42
)


int_cols = X_train.select_dtypes(include=["int"]).columns.tolist()
float_cols = X_train.select_dtypes(include=["float"]).columns.tolist()
cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()


print('int_cols')
print(int_cols)
print('float_cols')
print(float_cols)
print('cat_cols')
print(cat_cols)


pipeline =Pipeline([
            # int missing values imputers
            ('intimputer', MeanMedianImputer(
                imputation_method='median', variables=int_cols)),
            # category missing values imputers
            ('catimputer', CategoricalImputer(variables=cat_cols)),
            #
            ('catencoder', OrdinalEncoder()),


 ])

X_train = pipeline.fit_transform(X_train,y_train)
X_test = pipeline.transform(X_test)


start_time = time.time()
model = FLClassifier(number_of_intervals=5,fuzzy_type="triangular",fuzzy_cut=0.3,threshold=0.7,metric = 'euclidean')
model.fit(X=X_train,y=y_train,X_valid=None,y_valid=None)
print("--- %s seconds for training ---" % (time.time() - start_time))

start_time = time.time()
y_pred = model.predict(X=X_test)
print("--- %s seconds for prediction ---" % (time.time() - start_time))

print("classification_report :")
print(classification_report(y_test, y_pred))
print("confusion_matrix : ")
print(confusion_matrix(y_test, y_pred))
print("roc_auc_score : ")
print(roc_auc_score(y_test, y_pred))
print("f1_score : ")
print(f1_score(y_test, y_pred))


```

#### Example 2: Adult Dataset (Use FuzzyLearn as a Classifier with Optuna optimization engine)

```
from fuzzylearn.classification.fast.optimum import FLOptunaClassifier 
from sklearn.metrics import classification_report,confusion_matrix,f1_score,roc_auc_score
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from category_encoders import OrdinalEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import time
from sklearn.model_selection import train_test_split
import zipfile
import urllib.request


urldata = "https://archive.ics.uci.edu/static/public/2/adult.zip"
adult_data = 'fuzzylearn/data/adult.zip'
try:
    urllib.request.urlretrieve(urldata, adult_data)
except:
    print('error!')
with zipfile.ZipFile('fuzzylearn/data/adult.zip', 'r') as zip_ref:
    zip_ref.extractall('fuzzylearn/data/adult')
folder_path = 'fuzzylearn/data/adult/'
dataset_filename = 'adult.data'
#df = pd.read_csv(folder_path + dataset_filename)


# column names
col_names = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "label",
]
# read data
data = pd.read_csv(folder_path + dataset_filename, header=None, names=col_names, sep=",")
# use sample of 1000 rows of data only
data = data.sample(1000)
data.head()

data.loc[data["label"] == "<=50K", "label"] = 0
data.loc[data["label"] == " <=50K", "label"] = 0

data.loc[data["label"] == ">50K", "label"] = 1
data.loc[data["label"] == " >50K", "label"] = 1

data["label"] = data["label"].astype(int)

# Train test split

X = data.loc[:, data.columns != "label"]
y = data.loc[:, data.columns == "label"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, stratify=y["label"], random_state=42
)


int_cols = X_train.select_dtypes(include=["int"]).columns.tolist()
float_cols = X_train.select_dtypes(include=["float"]).columns.tolist()
cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()


print('int_cols')
print(int_cols)
print('float_cols')
print(float_cols)
print('cat_cols')
print(cat_cols)

pipeline_steps = []
if len(int_cols) > 0 :
  # append int missing values imputers
  pipeline_steps.append(('intimputer', MeanMedianImputer(
                imputation_method='median', variables=int_cols)))
if len(float_cols) > 0 :
  # append float missing values imputers
  pipeline_steps.append(('floatimputer', MeanMedianImputer(
                imputation_method='mean', variables=float_cols)))
if len(cat_cols) > 0 :
  # append cat missing values imputers
  pipeline_steps.append(('catimputer', CategoricalImputer(variables=cat_cols)))
  # encode categorical variables
  pipeline_steps.append(('catencoder', OrdinalEncoder()))


pipeline =Pipeline(pipeline_steps)

X_train = pipeline.fit_transform(X_train,y_train)
X_test = pipeline.transform(X_test)


start_time = time.time()
model = FLOptunaClassifier(optimizer = "optuna",metrics_list=['cosine','manhattan'],fuzzy_type_list=['simple','triangular'],fuzzy_cut_range=[0.05,0.45],number_of_intervals_range=[5,14],threshold_range=[0.1,12.0], error_measurement_metric= 'f1_score(y_true, y_pred, average="weighted")',n_trials=100)
model.fit(X=X_train,y=y_train,X_valid=None,y_valid=None)
print("--- %s seconds for training ---" % (time.time() - start_time))
start_time = time.time()
y_pred = model.predict(X=X_test)
print("--- %s seconds for prediction ---" % (time.time() - start_time))

print("classification_report :")
print(classification_report(y_test, y_pred))
print("confusion_matrix : ")
print(confusion_matrix(y_test, y_pred))
print("roc_auc_score : ")
print(roc_auc_score(y_test, y_pred))
print("f1_score : ")
print(f1_score(y_test, y_pred))


```
#### Example 3: Adult Dataset (Use FuzzyLearn as a Classifier with Optuna optimization engine and Ray integrated.)

```
from fuzzylearn.classification.fast.optimum import FLOptunaClassifier 
from sklearn.metrics import classification_report,confusion_matrix,f1_score,roc_auc_score
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from category_encoders import OrdinalEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import time
from sklearn.model_selection import train_test_split
import zipfile
import urllib.request


urldata = "https://archive.ics.uci.edu/static/public/2/adult.zip"
adult_data = 'fuzzylearn/data/adult.zip'
try:
    urllib.request.urlretrieve(urldata, adult_data)
except:
    print('error!')
with zipfile.ZipFile('fuzzylearn/data/adult.zip', 'r') as zip_ref:
    zip_ref.extractall('fuzzylearn/data/adult')
folder_path = 'fuzzylearn/data/adult/'
dataset_filename = 'adult.data'
#df = pd.read_csv(folder_path + dataset_filename)


# column names
col_names = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "label",
]
# read data
data = pd.read_csv(folder_path + dataset_filename, header=None, names=col_names, sep=",")
# use sample of 1000 rows of data only
data = data.sample(1000)
data.head()

data.loc[data["label"] == "<=50K", "label"] = 0
data.loc[data["label"] == " <=50K", "label"] = 0

data.loc[data["label"] == ">50K", "label"] = 1
data.loc[data["label"] == " >50K", "label"] = 1

data["label"] = data["label"].astype(int)

# Train test split

X = data.loc[:, data.columns != "label"]
y = data.loc[:, data.columns == "label"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, stratify=y["label"], random_state=42
)


int_cols = X_train.select_dtypes(include=["int"]).columns.tolist()
float_cols = X_train.select_dtypes(include=["float"]).columns.tolist()
cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()


print('int_cols')
print(int_cols)
print('float_cols')
print(float_cols)
print('cat_cols')
print(cat_cols)

pipeline_steps = []
if len(int_cols) > 0 :
  # append int missing values imputers
  pipeline_steps.append(('intimputer', MeanMedianImputer(
                imputation_method='median', variables=int_cols)))
if len(float_cols) > 0 :
  # append float missing values imputers
  pipeline_steps.append(('floatimputer', MeanMedianImputer(
                imputation_method='mean', variables=float_cols)))
if len(cat_cols) > 0 :
  # append cat missing values imputers
  pipeline_steps.append(('catimputer', CategoricalImputer(variables=cat_cols)))
  # encode categorical variables
  pipeline_steps.append(('catencoder', OrdinalEncoder()))


pipeline =Pipeline(pipeline_steps)

X_train = pipeline.fit_transform(X_train,y_train)
X_test = pipeline.transform(X_test)


start_time = time.time()
model = FLOptunaClassifier(optimizer = "optuna_ray",metrics_list=['cosine','manhattan'],fuzzy_type_list=['simple','triangular'],fuzzy_cut_range=[0.05,0.45],number_of_intervals_range=[5,14],threshold_range=[0.1,12.0], error_measurement_metric= 'f1_score(y_true, y_pred, average="weighted")',n_trials=100)
model.fit(X=X_train,y=y_train,X_valid=None,y_valid=None)
print("--- %s seconds for training ---" % (time.time() - start_time))
start_time = time.time()
y_pred = model.predict(X=X_test)
print("--- %s seconds for prediction ---" % (time.time() - start_time))

print("classification_report :")
print(classification_report(y_test, y_pred))
print("confusion_matrix : ")
print(confusion_matrix(y_test, y_pred))
print("roc_auc_score : ")
print(roc_auc_score(y_test, y_pred))
print("f1_score : ")
print(f1_score(y_test, y_pred))




```
There are some more examples available in the [examples](https://github.com/drhosseinjavedani/fuzzylearn/tree/main/fuzzylearn/examples) webpage. 

#### License
Licensed under the [BSD 2-Clause](https://opensource.org/licenses/BSD-2-Clause) License.