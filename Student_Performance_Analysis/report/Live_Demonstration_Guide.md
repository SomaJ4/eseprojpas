# Live Demonstration Guide
## 5–7 Minute Viva Presentation Walkthrough
**Project:** Student Attendance and Internal Assessment Performance Analysis  
**Environment:** Jupyter Notebook / Python Virtual Environment (`.venv`)

---

## Preparation Before Starting
1. Open your terminal in `d:\PAS\ese_project\Student_Performance_Analysis\`.
2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\activate
   jupyter notebook
   ```
3. Have the following three notebooks open in separate browser tabs:
   - Tab 1: `notebooks/01_dataset_inspection.ipynb`
   - Tab 2: `notebooks/02_data_cleaning.ipynb`
   - Tab 3: `notebooks/03_statistical_analysis.ipynb`

---

## 7-Minute Step-by-Step Demonstration Script

### Minute 1: Dataset Overview & Schema Inspection
- **Notebook:** `01_dataset_inspection.ipynb`
- **Cells to Highlight:**
  - **Cell 3 & 5 (`df.head()` & `df.shape`):** Point out the $300$ observations and $16$ features.
  - **Cell 8 (`Missing Values`):** Show that `assignments_submitted` contains exactly $300$ missing values ($100\%$ null), while all other columns are complete.
  - **Cell 9 (`Duplicates`):** Demonstrate that there are $0$ duplicate rows.
- **Talking Point:** *"We obtained our fixed dataset from Kaggle by Muhammad Khubaib Ahmad. Inspection confirmed 300 rows and identified that `assignments_submitted` was completely empty, which guided our cleaning strategy."*

### Minute 2: Data Cleaning & Feature Engineering
- **Notebook:** `02_data_cleaning.ipynb`
- **Cells to Highlight:**
  - **Cell 4 (`df.drop`):** Show the clean dropping of `assignments_submitted`.
  - **Cell 8 (`Validation`):** Point out that attendance counts are strictly bounded ($\text{attended} \le \text{total}$).
  - **Cells 9, 10, 11, 12 (`Derived Features`):** Show the formulas for `lecture_attendance_pct`, `lab_attendance_pct`, `overall_attendance_pct`, and `avg_quiz_marks`.
  - **Cell 14 (`Saving`):** Emphasize that the clean dataset was saved to `data/cleaned/student_performance_cleaned.csv` without modifying the original raw file.
- **Talking Point:** *"We standardized attendance into percentages using safe zero-denominator logic and created a combined average quiz score across the three quizzes."*

### Minute 3: Descriptive Statistics & Custom Functions
- **Notebook:** `03_statistical_analysis.ipynb`
- **Cells to Highlight:**
  - **Cell 4 (`def compute_stats`):** Walk through the function definition. Point out `ddof=1` for sample variance and sample standard deviation, and `np.percentile` for $Q_1, Q_2, Q_3,$ and $\text{IQR}$.
  - **Cell 5 & 7 (`Summary Table & IQR`):** Show the mean midterm mark ($19.97$), median ($21.35$), and IQR ($13.20$).
  - **Cell 9 (`Attendance Groups`):** Show the breakdown into Low ($141$), Moderate ($101$), and High ($58$) attendance tiers.
- **Talking Point:** *"Here is our modular statistical function computing both central tendency and robust dispersion measures. The median midterm mark of 21.35 slightly exceeds the mean of 19.97."*

### Minute 4: Visualizations & Confidence Intervals
- **Notebook:** `03_statistical_analysis.ipynb`
- **Cells to Highlight:**
  - **Cell 14 & 15 (`Box Plot by Group & Scatter Plot`):** Display the box plot showing midterm marks across Low, Moderate, and High attendance groups.
  - **Cell 19 (`Confidence Interval`):** Walk through the $t$-distribution formula step-by-step:
    $$\text{CI} = \bar{x} \pm t_{0.025, 299} \times \frac{s}{\sqrt{n}} = 19.9690 \pm 0.9399 = [19.03,\; 20.91]$$
- **Talking Point:** *"We computed a 95% confidence interval for mean midterm marks using the t-distribution. We are 95% confident that the true population mean lies between 19.03 and 20.91 marks."*

### Minute 5: Hypothesis Testing (Welch's $t$-test & ANOVA)
- **Notebook:** `03_statistical_analysis.ipynb`
- **Cells to Highlight:**
  - **Cell 22 (`Levene's Test`):** Show $W = 2.4612, p = 0.0871$, verifying equal variance across groups.
  - **Cell 23 (`Welch's t-test`):** Point out $t = 1.3392, p = 0.1838 > 0.05 \rightarrow$ Fail to reject $H_0$.
  - **Cell 25 (`One-Way ANOVA`):** Point out $F = 2.6616, p = 0.0715 > 0.05 \rightarrow$ Fail to reject $H_0$.
- **Talking Point:** *"Both Welch's t-test comparing Low vs High attendance and One-Way ANOVA across all three groups failed to reject the null hypothesis at alpha = 0.05. Attendance differences did not produce statistically significant differences in midterm marks."*

### Minute 6: Correlation & Linear Regression
- **Notebook:** `03_statistical_analysis.ipynb`
- **Cells to Highlight:**
  - **Cell 27 & 29 (`Correlation Table & Heatmap`):** Show $r = +0.0015$ between overall attendance and midterm marks.
  - **Cell 32 (`SLR Training & Equation`):** Show $\widehat{\text{Midterm}} = 20.7955 - 0.0157 \times (\text{Attendance \%})$.
  - **Cell 38 (`MLR Training & Equation`):** Show the multivariable equation with quiz marks, GPA, and age.
- **Talking Point:** *"Pearson correlation was essentially zero (r = 0.0015). Both the Simple and Multiple Regression models were fitted strictly on an 80% training split with fixed random seed 42."*

### Minute 7: Model Evaluation, Unseen Predictions & Conclusion
- **Notebook:** `03_statistical_analysis.ipynb`
- **Cells to Highlight:**
  - **Cell 40 & 41 (`Model Evaluation Table & Negative R²`):**
    - SLR: $\text{RMSE} = 8.0228,\; R^2 = -0.0198$
    - MLR: $\text{RMSE} = 8.1940,\; R^2 = -0.0637$
  - **Cell 42 (`Unseen Predictions`):** Display the 10 out-of-sample predictions and actual residuals on the test set.
- **Talking Point:** *"When evaluated on unseen test data, both models produced negative R² values. In statistics, this is an honest and meaningful finding: predicting the training mean outperforms the linear models, proving that attendance does not linearly predict exam performance in this synthetic dataset."*

---

## Quick Reference Summary Table for Live Viva

| Metric / Test | Project Value | Viva Explanation |
|---|---|---|
| **Sample Size ($n$)** | $300$ | Exceeds minimum requirement of $100$ |
| **Midterm Mean $\pm$ Std** | $19.97 \pm 8.27$ | Out of 30 marks total |
| **95% Confidence Interval** | $[19.03,\; 20.91]$ | $t$-distribution with $df = 299$ |
| **Welch's $t$-test** | $t = 1.3392, p = 0.1838$ | Low vs High attendance: Fail to Reject $H_0$ |
| **One-Way ANOVA** | $F = 2.6616, p = 0.0715$ | 3 Attendance tiers: Fail to Reject $H_0$ |
| **Pearson Correlation ($r$)** | $r = +0.0015, p = 0.9790$ | Virtually zero linear relationship |
| **SLR Equation** | $\hat{y} = 20.7955 - 0.0157 x$ | $x =$ Overall Attendance % |
| **MLR Equation** | $\hat{y} = 24.81 - 0.02x_1 - 0.64x_2 + 0.06x_3 - 0.003x_4$ | Predictors: Attendance, Quiz, GPA, Age |
| **Test $R^2$ (SLR / MLR)** | $-0.0198$ / $-0.0637$ | Baseline mean prediction outperforms regression |

