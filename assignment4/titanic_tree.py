import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

CRITERION = "entropy"              #"gini" or "entropy"

# Load data from the csv
df = pd.read_csv('titanic.csv')

# Select the features and target
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target = 'Survived'

data = df[features + [target]].copy()

# Add in the missing data with the medians
data['Age'] = data['Age'].fillna(data['Age'].median())
data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])
data['Fare'] = data['Fare'].fillna(data['Fare'].median())

# Convert sex into binary
le_sex = LabelEncoder()
data['Sex'] = le_sex.fit_transform(data['Sex'])  # female=0, male=1

le_emb = LabelEncoder()
data['Embarked'] = le_emb.fit_transform(data['Embarked'])

X = data[features]
y = data[target]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42, stratify=y)

# Tune hyperparameters
param_grid = {
    'max_depth': [3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [1, 5, 10, 20],
    'criterion': [CRITERION]
}

base_tree = DecisionTreeClassifier(random_state=42)
grid = GridSearchCV(base_tree, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

best_tree = grid.best_estimator_
print("Best params:", grid.best_params_)
print("Best CV accuracy:", grid.best_score_)

# Use test set
y_pred = best_tree.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)
print("\nTest accuracy:", test_acc)
print("\nClassification report:\n", classification_report(y_test, y_pred, target_names=['Died', 'Survived']))
print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))

# Calculate feature importances
importances = pd.Series(best_tree.feature_importances_, index=features).sort_values(ascending=False)
print("\nFeature importances:\n", importances)

# Plot tree
plt.figure(figsize=(20, 10))
plot_tree(best_tree, feature_names=features, class_names=['Died', 'Survived'],
          filled=True, rounded=True, fontsize=8, max_depth=3)
plt.title(f"Titanic Survival Decision Tree (Test Accuracy: {test_acc:.2%}, Criterion {CRITERION})")
plt.tight_layout()
plt.savefig(f'titanic_tree_{CRITERION}.png', dpi=150, bbox_inches='tight')
print("\nTree plot saved.")

# Plot the feature importance
plt.figure(figsize=(8, 5))
importances.plot(kind='barh', color='steelblue')
plt.xlabel('Importance')
plt.title(f'Feature Importance ({CRITERION}) - Titanic Survival Decision Tree')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f'feature_importance_{CRITERION}.png', dpi=150, bbox_inches='tight')
print("Feature importance plot saved.")

# Save results summary to text
with open(f'results_summary_{CRITERION}.txt', 'w') as f:
    f.write(f"Criterion: {CRITERION}")
    f.write(f"Best hyperparameters for: {grid.best_params_}\n")
    f.write(f"Best CV accuracy: {grid.best_score_:.4f}\n")
    f.write(f"Test accuracy: {test_acc:.4f}\n\n")
    f.write("Classification report:\n")
    f.write(classification_report(y_test, y_pred, target_names=['Died', 'Survived']))
    f.write("\nFeature importances:\n")
    f.write(importances.to_string())
