class DS:
    codes = [
        '''
import pandas as pd
from collections import Counter

# 1. Identify categorical and numerical variables
def identify_variable_types(df):
    categorical = df.select_dtypes(include=['object']).columns.tolist()
    numerical = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    return categorical, numerical

# 2. Create a contingency table
def create_contingency_table(data, cat_var1, cat_var2):
    pairs = [(row[cat_var1], row[cat_var2]) for _, row in data.iterrows()]
    counter = Counter(pairs)
    table = {}
    for (val1, val2), count in counter.items():
        if val1 not in table:
            table[val1] = {}
        table[val1][val2] = count
    return table

# 3. Calculate statistical measures
def calculate_mean(data):
    total = sum(data)
    return total / len(data)

def calculate_median(data):
    sorted_data = sorted(data)
    n = len(data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

def calculate_mode(data):
    freq = Counter(data)
    max_count = max(freq.values())
    modes = [key for key, count in freq.items() if count == max_count]
    return modes

def calculate_variance(data):
    mean = calculate_mean(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def calculate_std_dev(data):
    variance = calculate_variance(data)
    return variance ** 0.5

def calculate_quartile_range(data):
    sorted_data = sorted(data)
    n = len(data)
    q1 = sorted_data[n // 4]
    q3 = sorted_data[(3 * n) // 4]
    return q3 - q1

# 4. Categorize categorical variables
def categorize_categorical_variables(df, categorical_vars):
    categories = {}
    for var in categorical_vars:
        unique_values = df[var].nunique()
        if unique_values == 2:
            categories[var] = 'Binary'
        elif unique_values <= 10:
            categories[var] = 'Ordinal'
        else:
            categories[var] = 'Nominal'
    return categories

# Main program
  # Replace with your CSV file path
df = pd.read_csv("sample_data.csv")

# Identify variables
categorical_vars, numerical_vars = identify_variable_types(df)

# Contingency table
if len(categorical_vars) >= 2:
    contingency_table = create_contingency_table(df, categorical_vars[0], categorical_vars[1])
    print("\nContingency Table:")
    for key, sub_table in contingency_table.items():
        print(f"{key}: {sub_table}")
else:
    print("Not enough categorical variables for a contingency table.")

# Statistical measures for numerical variables
for num_var in numerical_vars:
    numerical_data = df[num_var].dropna().tolist()  # Remove NaN and convert to list
    numerical_data = [float(x) for x in numerical_data]  # Ensure all values are floats
    print(f"\nStatistics for numerical variable '{num_var}':")
    print(f"Mean: {calculate_mean(numerical_data)}")
    print(f"Median: {calculate_median(numerical_data)}")
    print(f"Mode: {calculate_mode(numerical_data)}")
    print(f"Variance: {calculate_variance(numerical_data)}")
    print(f"Standard Deviation: {calculate_std_dev(numerical_data)}")
    print(f"Quartile Range: {calculate_quartile_range(numerical_data)}")

# Categorical variable categorization
categories = categorize_categorical_variables(df, categorical_vars)
print("\nCategorization of categorical variables:")
for var, category in categories.items():
    print(f"{var}: {category}")
        ''',
        '''
# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Loading and Exploration
# Load the Iris dataset from a CSV file
df = pd.read_csv("iris.csv")  # Make sure you have iris.csv in your directory

# Display the first few rows of the dataset
print("Iris Dataset:")
display(df.head())

# Basic statistics for 'sepal length (cm)'
print("\nSummary Statistics for Sepal Length:")
sepal_length = df['sepal_length']
print(sepal_length.describe())

# 2. Selecting a Variable of Interest
# We are focusing on the "sepal length (cm)" variable
variable = 'sepal length (cm)'

# 3. Probability Mass Function (PMF)
# PMF visualization
pmf_data = sepal_length.value_counts(normalize=True).sort_index()
plt.figure(figsize=(8, 5))
plt.bar(pmf_data.index, pmf_data.values, color='skyblue', alpha=0.7, edgecolor='black')
plt.title('Probability Mass Function (PMF) - Sepal Length', fontsize=14)
plt.xlabel('Sepal Length (cm)', fontsize=12)
plt.ylabel('Probability', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 4. Probability Density Function (PDF
# PDF visualization
plt.figure(figsize=(8, 5))
sns.kdeplot(sepal_length, color='blue', fill=True, alpha=0.3)
plt.title('Probability Density Function (PDF) - Sepal Length', fontsize=14)
plt.xlabel('Sepal Length (cm)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 5. Cumulative Distribution Function (CDF)
# CDF computation and visualization
sorted_data = np.sort(sepal_length)
cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

plt.figure(figsize=(8, 5))
plt.plot(sorted_data, cdf, marker='o', linestyle='-', color='green', alpha=0.7)
plt.title('Cumulative Distribution Function (CDF) - Sepal Length', fontsize=14)
plt.xlabel('Sepal Length (cm)', fontsize=12)
plt.ylabel('Cumulative Probability', fontsize=12)
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.show()

# Results and Discussion
print("\nResults and Discussion:")
print("- The PMF for sepal length showed the relative frequency of different sepal lengths in the dataset.")
print("- The PDF for sepal length demonstrated the density, showing that most flowers have a sepal length around 5-6 cm.")
print("- The CDF for sepal length revealed cumulative probabilities, indicating the proportion of flowers below a specific sepal length.")
        ''',
        '''
import matplotlib.pyplot as plt
import numpy as np

# Generate random data from a uniform distribution
data = np.random.uniform(0, 1, 1000)

# Create a histogram
plt.hist(data, bins=20, density=True, alpha=0.6, color='g')

# Add titles and labels
plt.title("Uniform Distribution")
plt.xlabel("Values")
plt.ylabel("Frequency")

# Show the plot
plt.show()

# Generate random data from a normal distribution
data = np.random.normal(0, 1, 1000)

# Create a histogram
plt.hist(data, bins=20, density=True, alpha=0.6, color='b')

# Add titles and labels
plt.title("Normal Distribution")
plt.xlabel("Values")
plt.ylabel("Frequency")

# Display the plot
plt.show()

# Generate random data from an exponential distribution
data = np.random.exponential(1/0.5, 1000)

# Create a histogram
plt.hist(data, bins=20, density=True, alpha=0.6, color='r')

# Add titles and labels
plt.title("Exponential Distribution")
plt.xlabel("Values")
plt.ylabel("Frequency")

# Display the plot
plt.show()

# Generate random data from a binomial distribution
data = np.random.binomial(20, 0.3, 1000)

# Create a histogram
plt.hist(data, bins=range(0, 21), density=True, alpha=0.6, color='m', edgecolor='black')

# Add titles and labels
plt.title("Binomial Distribution")
plt.xlabel("Number of Successes")
plt.ylabel("Frequency")

# Display the plot
plt.show()

# Generate random data from a Poisson distribution
data = np.random.poisson(5, 1000)

# Create a histogram
plt.hist(data, bins=range(0, max(data) + 2), density=True, alpha=0.6, color='c', edgecolor='black')

# Add titles and labels
plt.title("Poisson Distribution")
plt.xlabel("Number of Events")
plt.ylabel("Frequency")

# Display the plot
plt.show()
        ''',
        '''
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load Titanic dataset
titanic_data = pd.read_csv('/content/Titanic-Dataset.csv')

# Display the first few rows, descriptive statistics, and missing values
print(titanic_data.head())
print(titanic_data.describe())
print(titanic_data.isnull().sum())

# Fill missing 'Age' values with the median
titanic_data['Age'] = titanic_data['Age'].fillna(titanic_data['Age'].median())

# Drop 'Cabin' column due to excessive missing values
titanic_data.drop(columns=['Cabin'], inplace=True)

# Fill missing 'Embarked' values with the mode
titanic_data['Embarked'] = titanic_data['Embarked'].fillna(titanic_data['Embarked'].mode()[0])

# Convert 'Sex' to numerical values
titanic_data['Sex'] = titanic_data['Sex'].map({'male': 0, 'female': 1})

# Convert 'Embarked' to numerical values using one-hot encoding
titanic_data = pd.get_dummies(titanic_data, columns=['Embarked'], drop_first=True)

# Drop 'Ticket' and 'Name' columns as they are not needed for analysis
titanic_data.drop(columns=['Ticket', 'Name'], inplace=True)

# Plot age distribution
plt.figure(figsize=(7, 4))
sns.histplot(titanic_data['Age'], bins=30, kde=True, color='blue')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Plot count of survival
plt.figure(figsize=(7, 4))
sns.countplot(x='Survived', data=titanic_data)
plt.title('Count of Survival')
plt.xlabel('Survived (0 = No, 1 = Yes)')
plt.ylabel('Count')
plt.show()

# Plot survival rate by passenger class
plt.figure(figsize=(7, 4))
sns.barplot(x='Pclass', y='Survived', data=titanic_data)
plt.title('Survival Rate by Passenger Class')
plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.show()

# Plot correlation matrix
plt.figure(figsize=(10, 8))
correlation_matrix = titanic_data.corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix')
plt.show()
        ''',
        '''
import pandas as pd
from scipy import stats
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target

# Select data for setosa and versicolor
setosa = iris_df[iris_df['species'] == 0]
versicolor = iris_df[iris_df['species'] == 1]

# Perform the two-sample t-test
t_stat, p_value = stats.ttest_ind(setosa['sepal length (cm)'], versicolor['sepal length (cm)'])

# Output the results of the t-test
print(f"T-statistic: {t_stat}, P-value: {p_value}")

# Perform one-way ANOVA
setosa_sepal_length = iris_df[iris_df['species'] == 0]['sepal length (cm)']
versicolor_sepal_length = iris_df[iris_df['species'] == 1]['sepal length (cm)']
virginica_sepal_length = iris_df[iris_df['species'] == 2]['sepal length (cm)']

f_stat, p_value = stats.f_oneway(setosa_sepal_length, versicolor_sepal_length, virginica_sepal_length)

# Output the results of ANOVA
print(f"F-statistic: {f_stat}, P-value: {p_value}")

# Categorize sepal width into narrow, medium, and wide
iris_df['sepal width category'] = pd.cut(
    iris_df['sepal width (cm)'],
    bins=[0, 2.8, 3.3, 4.5],
    labels=['narrow', 'medium', 'wide']
)

# Create a contingency table
contingency_table = pd.crosstab(iris_df['species'], iris_df['sepal width category'])

# Perform the chi-square test
chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# Output the results of the chi-square test
print(f"Chi-square statistic: {chi2_stat}, P-value: {p_value}")
        ''',
        '''
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE

# Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
data = pd.read_csv(url)

# Display the first few rows
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Fill missing values in 'Age' with the median
data['Age'].fillna(data['Age'].median(), inplace=True)

# Fill missing values in 'Embarked' with the mode
data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)

# Drop 'Cabin' as it has too many missing values
data.drop('Cabin', axis=1, inplace=True)
label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])

# Convert 'Embarked' column using One-Hot Encoding
data = pd.get_dummies(data, columns=['Embarked'], drop_first=True)

# Check the first few rows to verify encoding
print(data.head())
# Create 'FamilySize' feature
data['FamilySize'] = data['SibSp'] + data['Parch'] + 1

# Create 'IsAlone' feature
data['IsAlone'] = np.where(data['FamilySize'] == 1, 1, 0)

# Check the new features
print(data[['SibSp', 'Parch', 'FamilySize', 'IsAlone']].head())

# Standardize numerical features
scaler = StandardScaler()
data[['Age', 'Fare', 'FamilySize']] = scaler.fit_transform(data[['Age', 'Fare', 'FamilySize']])

# Check the scaled features
print(data[['Age', 'Fare', 'FamilySize']].head())

# Separate features (X) and target (y)
X = data.drop(['PassengerId', 'Name', 'Ticket', 'Survived'], axis=1)
y = data['Survived']

# Use SelectKBest to select top 5 features based on ANOVA F-test
selector = SelectKBest(score_func=f_classif, k=5)
X_new = selector.fit_transform(X, y)

# Display the scores of each feature
selected_features = pd.DataFrame({
    'Feature': X.columns,
    'Score': selector.scores_
}).sort_values(by='Score', ascending=False)
print(selected_features)

# Use RFE to select the top 5 features
model = LogisticRegression()
rfe = RFE(model, n_features_to_select=5)
fit = rfe.fit(X, y)

# Display selected features and their rankings
selected_features_rfe = pd.DataFrame({
    'Feature': X.columns,
    'Selected': fit.support_,
    'Ranking': fit.ranking_
}).sort_values(by='Ranking')
print(selected_features_rfe)

# Fit a Random Forest Classifier
model = RandomForestClassifier()
model.fit(X, y)

# Get feature importance
importances = model.feature_importances_

# Display the feature importance
feature_importance_rf = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)
print(feature_importance_rf)

# Apply PCA to reduce dimensions to 2
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Display explained variance ratio and the first 5 rows of the new components
print('Explained Variance Ratio:', pca.explained_variance_ratio_)
print('PCA Components:', X_pca[:5])
        ''',
        '''
import numpy as np
import pandas as pd

# Load the dataset
df = pd.read_csv('diabetes.csv')

# Display the first 10 rows
print(df.head(10))

# Display column names
print(df.columns)

# Check for null values
print(df.isnull().sum())

import matplotlib.pyplot as plt
import seaborn as sns

# Plot age distribution
plt.figure(figsize=(6, 6))
sns.histplot(df['Age'])
plt.title('Age Distribution', size=18)
plt.xlabel('Age', size=15)
plt.ylabel('Count', size=15)
plt.show()

# Plot age boxplot
sns.boxplot(df['Age'])
plt.title('Age Boxplot')
plt.show()

# Plot BMI distribution
df['BMI'].hist(bins=20)
plt.title('BMI Distribution')
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, square=True, cmap='RdBu', vmax=1, vmin=-1)
plt.title('Correlations Between Variables', size=18)
plt.xticks(size=13)
plt.yticks(size=13)
plt.show()

sns.scatterplot(data=df, x='Glucose', y='BMI', hue='Outcome', palette='coolwarm', s=100)
plt.title('Glucose vs BMI (Colored by Diabetes Outcome))
plt.xlabel('Glucose Level')
plt.ylabel('BMI')
plt.legend(title='Diabetes Outcome')

sns.scatterplot(data = df )
plt.show()

sns.scatterplot(data=df, x='BMI', y='Age')
plt.show()

import itertools

# Pairwise scatter plots for all columns
for x, y in itertools.permutations(df.columns, 2):
    sns.scatterplot(data=df, x=x, y=y)
    plt.show()
        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return DS.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(DS.codes)}."
