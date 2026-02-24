import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.decomposition import PCA

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. Load RNA-Seq data
expression_df = pd.read_csv(
    "EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp (1).tsv",
    sep="\t",
    index_col=0,
    low_memory=False
)
expression_df.columns = [col[:12] for col in expression_df.columns]  # barcode kısalt
expression_df = expression_df.loc[:, expression_df.columns.duplicated() == False]  # tekrarları at
expression_df = expression_df.T
expression_df.index.name = "Sample"

# 2. Read metadata file
metadata_df = pd.read_excel("TCGA-CDR-SupplementalTableS1.xlsx", engine="openpyxl")
metadata_df = metadata_df[["bcr_patient_barcode", "type"]]
metadata_df.columns = ["Sample", "CancerType"]

# 3. Merge datasets
merged_df = pd.merge(metadata_df, expression_df, on="Sample")
print(f"Birleşik veri şekli: {merged_df.shape}")

# 4. Check for missing data
missing = merged_df.isnull().sum().sum()
print(f"Toplam eksik veri: {missing}")
merged_df = merged_df.dropna()

# 5. Separate target and features
X = merged_df.drop(columns=["Sample", "CancerType"])
y = merged_df["CancerType"]

# 6. Label encoding
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 7. Normalization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 8. Feature selection - Variance Thresholding
selector = VarianceThreshold(threshold=0.01)
X_var = selector.fit_transform(X_scaled)
print(f"Varyans seçimi sonrası boyut: {X_var.shape}")

# 9. SelectKBest (ANOVA) - Top 500 genes
selector2 = SelectKBest(score_func=f_classif, k=500)
X_selected = selector2.fit_transform(X_var, y_encoded)
print(f"SelectKBest sonrası boyut: {X_selected.shape}")

# 10. PCA Visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_selected)

plt.figure(figsize=(10, 8))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=le.inverse_transform(y_encoded), palette="tab10")
plt.title("PCA ile Kanser Türleri Görselleştirme")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.show()

# 11. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_selected, y_encoded, test_size=0.2, random_state=42)

# 12. Model definitions
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'Neural Network': MLPClassifier(max_iter=500, random_state=42)
}

# 13. Model comparison and cross-validation
model_results = []

for name, model in models.items():
    # Cross-validation scores
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    mean_cv_score = cv_scores.mean()
    std_cv_score = cv_scores.std()
    
    # Model training and testing
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    model_results.append({
        'Model': name,
        'CV Score (Mean)': mean_cv_score,
        'CV Score (Std)': std_cv_score,
        'Train Score': train_score,
        'Test Score': test_score
    })

# Convert results to DataFrame and display
results_df = pd.DataFrame(model_results)
results_df = results_df.sort_values('Test Score', ascending=False)
print("\nModel Karşılaştırma Tablosu:")
print(results_df.to_string(index=False))

# Select the best model
best_model_name = results_df.iloc[0]['Model']
best_model = models[best_model_name]
print(f"\nEn iyi model: {best_model_name}")

# 14. Evaluate the best model
final_model = best_model
final_model.fit(X_train, y_train)
y_pred = final_model.predict(X_test)

print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_[np.unique(y_test)]))
print("Test Accuracy:", accuracy_score(y_test, y_pred))

# 15. Confusion Matrix
plt.figure(figsize=(12, 8))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 16. Feature Importance (Top 20 gen)
if hasattr(final_model, 'feature_importances_'):
    importances = final_model.feature_importances_
    indices = np.argsort(importances)[-20:]
    feature_names = np.array(X.columns)[selector.get_support()][selector2.get_support()][indices]

    plt.figure(figsize=(10, 8))
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), feature_names)
    plt.title("Feature Importances (Top 20)")
    plt.tight_layout()
    plt.show()
elif hasattr(final_model, 'coef_'):
    # Feature coefficients for Logistic Regression
    coef = final_model.coef_[0]
    indices = np.argsort(np.abs(coef))[-20:]
    feature_names = np.array(X.columns)[selector.get_support()][selector2.get_support()][indices]

    plt.figure(figsize=(10, 8))
    plt.barh(range(len(indices)), coef[indices])
    plt.yticks(range(len(indices)), feature_names)
    plt.title("Feature Coefficients (Top 20)")
    plt.tight_layout()
    plt.show()
else:
    print("\nFeature importance visualization is not available for this model.")
