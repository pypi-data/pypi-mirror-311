def ml(num):
    if num == 1:
        print("""#exercise 1.1
import pandas as pd
col_list=["id","first","last","gender","Marks","selected"]
df = pd.read_csv("ex1.csv")
print(df)
mean1 = df['Marks'].mean()
sum1 = df['Marks'].sum()
max1 = df['Marks'].max()
min1 = df['Marks'].min()
count1 = df['Marks'].count()
median1 = df['Marks'].median()
sd1 = df['Marks'].std()
var1 = df['Marks'].var()
print('Mean Marks\n' + str(mean1))
print('Sum of the Marks\n' + str(sum1))
print('Maximum of the marks\n' + str(max1))
print('Minimum of the marks\n' + str(min1))
print('Count of the marks\n' + str(count1))
print('Standard deviation of the marks\n' + str(sd1))
print('Variance of the marks\n' + str(var1))
print('End of Summary \n\n\n')
print(df.shape)
print(df.head(5))
print(df.describe())

#exercise1.2
import pandas as pd
from matplotlib import pyplot as plt
col_list=['id','name','gender','physics','chemistry','maths','biology','language','selected']
df = pd.read_csv('marks.csv')
print(df)


marks_scored = df['physics'].hist()
plt.title('Histogram for Physics Marks')
plt.xlabel('Physics Marks')
plt.ylabel('Frequency of Physics Marks')
plt.show()

marks1 = df['physics'].values.tolist()
chemistry1 = df['chemistry'].values.tolist()
print (chemistry1)
plt.scatter(chemistry1,marks1,alpha=0.5)
plt.title('Scatter plot chemistry vs physics')
plt.xlabel('Chemistry')
plt.ylabel('Physics')
plt.show()

df.plot.box(title="Box and whisker plot of Marks", grid=False)
plt.show()

sums = df.selected.groupby(df.gender).sum()
plt.pie(sums,labels=sums.index);
plt.show()""")

    elif num == 2:
        print("""import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
df=pd.read_csv("ex2.csv")
df
print(df.head(5))
print(df.describe())
print(df.shape)


X=df.iloc[:,1:-1].values
y=df.iloc[:,4].values
print(X)
print(y)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20)

scaler=StandardScaler()
scaler.fit(X_train)
X_train=scaler.transform(X_train)
X_test=scaler.transform(X_test)

classifier=KNeighborsClassifier(n_neighbors=3)
classifier.fit(X_train,y_train)
y_pred=classifier.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred)) 
print([9.1,85,8])
input_data = np.array([9.1, 85, 8]).reshape(1, -1)
pred = classifier.predict(input_data)
print(pred) 
""")

    elif num == 3:
        print("""#exercise 3
#linear regression
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.datasets import make_regression
X,y = make_regression(n_samples = 50,n_features=1,noise=0.1)
plt.scatter(X,y,color='green')
plt.title('Regression among X and y')
plt.xlabel('X - axis - X')
plt.ylabel('Y- Dependent - y')
regr = linear_model.LinearRegression()
regr.fit(X,y)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)
print('\nThe Regression Equation is',regr.coef_,'* X +',regr.intercept_)
# Fit the model for the given data
pred = regr.predict(X)
plt.plot(X,pred)
# Compute Adjusted R squared Error
print("\nAdjusted R Squared for Regression model:",regr.score(X,y))

-------------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
salesdata = {'week': [1,2,3,4,5],
'sales': [1.2,1.8,2.6,3.2,3.8]
}
df = pd.DataFrame(salesdata,columns=['week','sales'])

plt.scatter(df['week'], df['sales'], color='green')
plt.title('Regression among week and sales')
plt.xlabel('X - axis - Week')
plt.ylabel('Y- Dependent - Sales')


X = df[['week']]
y = df['sales']
regr = linear_model.LinearRegression()
regr.fit(X,y)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)
print('\nThe Regression Equation is',regr.coef_,'* X+',regr.intercept_)
pred = regr.predict(X)
plt.plot(X,pred)
print("\nAdjusted R Squared for Regression model:",regr.score(X,y))

-------------------------------------------------------

# ex 3 multiple regression 
from sklearn import linear_model
from sklearn.datasets import make_regression
print("Multiple regression \n\n")
# Multiple Regression
# Create random dataset with 2 features. Dataset has 50 samples with noise 0.1.
X,y = make_regression(n_samples = 50,n_features=2,noise=0.1)
regr = linear_model.LinearRegression()
regr.fit(X,y)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)
# Compute Adjusted R squared Error
print("\nAdjusted R Squared for Regression model:",regr.score(X,y))
""")
    elif num == 4:
        print("""# ex4 adaboost

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

db = pd.read_csv("diabetes.csv")

X = db.iloc[:, 0:8]
y = db.iloc[:, 8].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)
rf_predictions = rf_classifier.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_predictions)
print(f"Random Forest Accuracy: {rf_accuracy:.4f}")

adaboost_classifier = AdaBoostClassifier(n_estimators=50, random_state=42, algorithm='SAMME')
adaboost_classifier.fit(X_train, y_train)
adaboost_predictions = adaboost_classifier.predict(X_test)
adaboost_accuracy = accuracy_score(y_test, adaboost_predictions)
print(f"AdaBoost Accuracy: {adaboost_accuracy:.4f}")""")

    elif num == 5:
        print("""#ex5 knn clustering
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, silhouette_score

data = 'KMEANS.csv'
df = pd.read_csv(data)
df.shape
df.head()

df.drop(['status_id','status_published'], axis=1, inplace=True)
df.info()
df.head()
df.isnull().sum()
df.drop(['Column1','Column2','Column3','Column4'], axis=1, inplace=True)
df.info()
df.describe()

X = df
y = df['status_type']
le = LabelEncoder()
X['status_type'] = le.fit_transform(X['status_type'])
y = le.transform(y)
ms = MinMaxScaler()
X = ms.fit_transform(X)
X = pd.DataFrame(X, columns=df.columns)
kmeans = KMeans(n_clusters=8, random_state=0)
labels = kmeans.fit_predict(X)
accuracy = accuracy_score(y, labels)
print(f'Accuracy: {accuracy}')
score = silhouette_score(X, labels)
print(f'Silhouette Score: {score}')""")

    elif num == 6:
        print("""#ex6 missing values 
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

df = pd.read_csv('KMEANS.csv')

missing_per_column = df.isnull().sum()
total_missing = df.isnull().sum().sum()
print('Missing values per column:\n', missing_per_column)
print('\nTotal missing values', total_missing)

df.replace(' ', np.nan, inplace=True)
df.replace('#', np.nan, inplace=True)

numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Step 2: Non-numeric columns - Fill missing values with mode
non_numeric_columns = df.select_dtypes(include=['object']).columns
for column in non_numeric_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

# Alternative fill strategies (forward fill and backward fill as fallbacks)
df.ffill(inplace=True)
df.bfill(inplace=True)

# Transform categorical to numerical using Label Encoder
label_encoder = LabelEncoder()
for column in non_numeric_columns:
    df[column] = label_encoder.fit_transform(df[column].astype(str))

# Normalize numerical columns
# Step 1: Standard Scaling
scaler = StandardScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Step 2: Min-Max Scaling (overwrite Standard Scaling if needed)
minmax_scaler = MinMaxScaler()
df[numeric_columns] = minmax_scaler.fit_transform(df[numeric_columns])

print("\nFinal Processed DataFrame:")
print(df)
df = df.dropna(axis=1,inplace=True)
print(df)""")