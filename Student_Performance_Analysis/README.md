# Student Attendance and Internal Assessment Performance Analysis

## Project Title
Student Attendance and Internal Assessment Performance Analysis

## Problem Definition
This project investigates whether attendance (lectures and lab sessions) and continuous internal assessment scores (quizzes) have a statistically significant and predictive relationship with a student's examination performance (specifically midterm marks) and overall academic standing. Using descriptive statistics, parametric confidence intervals, hypothesis testing (Welch's t-test and One-way ANOVA), Pearson correlation analysis, and linear regression modelling (Simple and Multiple), we rigorously evaluate these relationships.

---

## Final Deliverables & Package Structure

```
Student_Performance_Analysis/
├── data/
│   ├── original/                                  # Pristine raw downloads
│   │   ├── student-performance-and-clustering-dataset.zip
│   │   ├── student_dropout_behavior_dataset.csv
│   │   └── student_performance.csv
│   └── cleaned/                                   # Processed CSV for modeling
│       └── student_performance_cleaned.csv
├── notebooks/                                     # Fully executed Jupyter Notebooks
│   ├── 01_dataset_inspection.ipynb                # Initial verification & sanity check
│   ├── 02_data_cleaning.ipynb                     # Cleaning & feature engineering
│   └── 03_statistical_analysis.ipynb              # Complete stats, tests & regression models
├── outputs/
│   ├── graphs/                                    # 13 publication-grade figures
│   │   ├── bar_mean_midterm_by_group.png
│   │   ├── boxplot_midterm.png
│   │   ├── boxplot_midterm_by_group.png
│   │   ├── heatmap_correlation.png
│   │   ├── hist_avg_quiz_marks.png
│   │   ├── hist_lab_attendance.png
│   │   ├── hist_midterm_marks.png
│   │   ├── hist_overall_attendance.png
│   │   ├── mlr_actual_vs_predicted.png
│   │   ├── scatter_attendance_vs_avg_quiz.png
│   │   ├── scatter_attendance_vs_midterm.png
│   │   ├── slr_actual_vs_predicted.png
│   │   └── slr_regression_line.png
│   └── results/                                   # All tabular artifacts
│       ├── anova_attendance_groups.csv
│       ├── attendance_group_summary.csv
│       ├── confidence_interval_midterm.csv
│       ├── correlation_matrix.csv
│       ├── descriptive_statistics.csv
│       ├── model_evaluation_comparison.csv
│       ├── pearson_correlation_attendance.csv
│       ├── predictions_test_set.csv
│       └── ttest_low_vs_high.csv
├── presentation/
│   └── Student_Attendance_Performance_Analysis.pptx # 12-slide clean academic presentation
├── report/
│   ├── Student_Attendance_Performance_Analysis_Report.pdf # 16-page formal academic report
│   ├── Viva_Preparation.md                        # 36 comprehensive viva questions & answers
│   └── Live_Demonstration_Guide.md                # 5–7 minute walkthrough script with cell mapping
├── requirements.txt                               # Verified dependencies
└── README.md                                      # Project documentation
```

---

## Dataset Information

| Field | Value |
|---|---|
| **Dataset name** | Student Performance and Clustering Dataset |
| **Kaggle URL** | https://www.kaggle.com/datasets/muhammadkhubaibahmad/student-performance-and-clustering-dataset |
| **Dataset author** | Muhammad Khubaib Ahmad |
| **DSV identifier** | https://www.kaggle.com/dsv/13489035 |
| **License** | CC BY-SA 4.0 — Free to use, share, and adapt with attribution |
| **Citation** | Muhammad Khubaib Ahmad, "Student Performance and Clustering Dataset", 2025, Kaggle. DOI: https://doi.org/10.34740/kaggle/dsv/13489035 |
| **Observations** | 300 students |
| **Original Features** | 16 features |
| **Cleaned Features** | 19 features (after dropping unpopulated column & engineering 4 derived features) |

> **Synthetic vs. Real Data Limitation:**
> The dataset author describes this dataset as a lightweight educational benchmark intended for unsupervised clustering and exploratory data analysis. The raw file inside the Kaggle archive is named `student_dropout_behavior_dataset.csv`. No evidence indicates that these 300 observations represent real-world college students or were gathered via probabilistic random sampling. **All findings must be interpreted strictly within this illustrative context and cannot be generalized to real academic populations.**

---

## Summary of Empirical Findings

### 1. Summary Statistics
- **Overall Attendance:** Mean = $50.69\%$, Median = $50.00\%$, $IQR = 38.89\%$ (spread from $0\%$ to $100\%$).
- **Midterm Marks:** Mean = $19.97 / 30$, Median = $21.35$, Std Dev = $8.27$, $IQR = 13.20$.
- **Average Quiz Marks:** Mean = $6.20 / 10$, Median = $6.15$, Std Dev = $1.28$, $IQR = 1.68$.
- **Previous GPA:** Mean = $2.81 / 4.0$, Median = $2.80$, Std Dev = $0.73$, $IQR = 0.99$.

### 2. 95% Confidence Interval for Mean Midterm Marks
$$\bar{x} \pm t_{\alpha/2, df} \times \frac{s}{\sqrt{n}} = 19.9690 \pm 1.9679 \times \frac{8.2722}{\sqrt{300}} = [19.0291,\; 20.9089]$$
- **Interpretation:** We are $95\%$ confident that the true population mean midterm mark lies between **$19.03$ and $20.91$ marks**.

### 3. Hypothesis Testing Results
- **Welch's Two-Sample $t$-test (Low vs. High Attendance):**
  - Low group mean: $19.91$ ($n=141$); High group mean: $18.04$ ($n=58$).
  - $t = 1.3392$, $p = 0.1838$ ($p > 0.05$).
  - **Decision:** **Fail to Reject $H_0$**. There is no statistically significant difference in midterm scores between students with low attendance and those with high attendance.
- **One-Way ANOVA (Low, Moderate, High Attendance):**
  - Group Means: Low = $19.91$, Moderate = $21.16$, High = $18.04$.
  - $F = 2.6616$, $p = 0.0715$ ($p > 0.05$).
  - **Decision:** **Fail to Reject $H_0$** at the $5\%$ significance level. The differences among the attendance tiers are not statistically significant.

### 4. Correlation Analysis
- `overall_attendance_pct` vs. `midterm_marks`: $r = +0.0015$ ($p = 0.9790$) — **Virtually zero linear association**.
- `overall_attendance_pct` vs. `avg_quiz_marks`: $r = -0.0357$ ($p = 0.5378$) — Negligible.
- `overall_attendance_pct` vs. `final_marks`: $r = +0.0343$ ($p = 0.5536$) — Negligible.
- `overall_attendance_pct` vs. `previous_gpa`: $r = -0.0380$ ($p = 0.5125$) — Negligible.
- **Principle:** Correlation does not imply causation. In this synthetic dataset, linear association between attendance and exam marks is nonexistent.

### 5. Regression Models and Evaluation

#### Simple Linear Regression (SLR)
$$\widehat{\text{Midterm}} = 20.7955 - 0.0157 \times (\text{Overall Attendance \%})$$

#### Multiple Linear Regression (MLR)
$$\widehat{\text{Midterm}} = 24.8117 - 0.0189 \times (\text{Attendance \%}) - 0.6408 \times (\text{Avg Quiz}) + 0.0595 \times (\text{GPA}) - 0.0028 \times (\text{Age})$$

#### Test Set Performance Comparison ($n = 60$, 80:20 Split, `random_state=42`)
| Metric | Simple Linear Regression | Multiple Linear Regression |
|---|---|---|
| **MAE** | $6.6292$ | $6.6987$ |
| **MSE** | $64.3656$ | $67.1423$ |
| **RMSE** | $8.0228$ | $8.1940$ |
| **$R^2$** | **$-0.0198$** | **$-0.0637$** |

- **Understanding Negative $R^2$:** Both models yield negative test $R^2$ values, indicating that predicting the historical training mean ($\bar{y}_{\text{train}}$) provides smaller squared prediction errors than the regression equations. Adding uncorrelated predictors in MLR increased variance, resulting in worse test performance.
