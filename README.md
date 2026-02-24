# 🧬 Multi-Class Classification of Cancer Types using TCGA Pan-Cancer RNA-Seq Data

This repository contains a high-performance bioinformatics pipeline designed to classify various cancer types using genomic data. The project is based on a technical paper authored by **Sümeyye Bakırdal**.

---

## 📄 Technical Paper (Original in Turkish)
The full research paper is available in this repository: `Technical_Paper_Cancer_Classification.pdf`.

> **Note:** While the full text is in Turkish, the methodology, experimental results, and key visualizations are summarized below in English for international review.

---

## 🧬 Project Overview
Accurate molecular classification of cancer is vital for personalized medicine. This study utilizes **RNA-Seq gene expression profiles** from the **The Cancer Genome Atlas (TCGA) Pan-Cancer Atlas** to predict cancer types based on molecular signatures.

### 🛠️ Key Methodologies
* **Data Integration:** Merging RNA-Seq expression data with **TCGA-CDR (Clinical Data Resource)**.
* **Feature Engineering:** Variance thresholding and **SelectKBest (ANOVA F-test)** for biomarker selection.
* **Dimensionality Reduction:** **PCA** for high-dimensional data visualization.
* **Model Benchmarking:** Comparative analysis of Logistic Regression, Random Forest, SVM, and Neural Networks.

---

## 📊 Experimental Results & Findings
The models were validated using **5-fold cross-validation**.

| Model | Peak Accuracy | Status |
| :--- | :--- | :--- |
| **Logistic Regression** | **94.6%** | ✅ Best Model |
| Random Forest | 94.5% | ✅ High Stability |
| SVM | 93.32% | ✅ Robust |

### 📈 Visualizations
* **PCA Plots:** To visualize how cancer types cluster in a 2D space.
* **Confusion Matrices:** Detailed evaluation of precision and recall for each category.

---

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have the following Python libraries installed:
`pandas`, `numpy`, `scikit-learn`, `seaborn`, `matplotlib`

### 💻 Execution
1. Clone the repository.
2. Ensure the TCGA datasets are in the project directory.
3. Run the main script:
   ```bash
   python cancer_classification.py
 
