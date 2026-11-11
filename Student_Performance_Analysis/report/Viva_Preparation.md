# Viva Voce Preparation Guide
## Probability and Statistics End-Semester Course Project
**Project Title:** Student Attendance and Internal Assessment Performance Analysis  
**Dataset:** Student Performance and Clustering Dataset (300 observations, 16 raw features)  
**Author:** Muhammad Khubaib Ahmad (Kaggle)

---

## Section A: Dataset & Preprocessing

### 1. What is the objective of this project?
The project investigates whether student class attendance (lectures and labs) and continuous internal assessments (quizzes) have a statistically significant relationship with midterm examination performance and whether midterm marks can be reliably predicted using linear regression models.

### 2. Why was this specific dataset selected?
The dataset provides individual-level attendance metrics (`lectures_attended`, `labs_attended`) alongside multiple internal assessments (`quiz1_marks`, `quiz2_marks`, `quiz3_marks`, `midterm_marks`) and cumulative metrics (`final_marks`, `previous_gpa`). With 300 observations, it comfortably satisfies the course project requirement of having at least 100 observations.

### 3. What is synthetic data, and why must we disclose it?
Synthetic data is artificially generated data created through computer simulation rather than measured from real-world subjects. We must disclose it to ensure scientific integrity: we cannot claim that our findings represent actual college students or make policy recommendations for real academic institutions based on simulated patterns.

### 4. What is sampling bias and does it apply here?
Sampling bias occurs when certain members of an intended population are systematically more likely to be selected than others, distorting the sample statistics. In this dataset, the data generation process is undocumented and lacks a formal sampling frame. Therefore, any generalization beyond this specific dataset would suffer from unquantified sampling bias.

### 5. Why did we drop the `assignments_submitted` column?
Inspection revealed that `assignments_submitted` was $100\%$ missing ($300$ out of $300$ cells were `NaN`). Imputing or using a completely blank column would introduce fabricated information into our analysis.

### 6. What feature engineering steps did you perform and why?
Four derived metrics were created:
- `lecture_attendance_pct`: $(\text{lectures\_attended} / 12) \times 100$
- `lab_attendance_pct`: $(\text{labs\_attended} / 6) \times 100$
- `overall_attendance_pct`: $((\text{lectures\_attended} + \text{labs\_attended}) / 18) \times 100$
- `avg_quiz_marks`: $(\text{quiz1} + \text{quiz2} + \text{quiz3}) / 3$
Converting raw counts into percentages standardizes attendance onto an interpretable $0-100\%$ scale, and averaging quizzes provides a single, robust continuous measure of ongoing academic effort.

---

## Section B: Descriptive Statistics

### 7. What are the mean, median, and mode of Midterm Marks in your project?
- **Mean:** $19.97$ marks (out of 30)
- **Median:** $21.35$ marks
- **Mode:** $30.00$ marks  
The median is higher than the mean, reflecting a slight left skew with a clustering of perfect scores ($30.0$) at the upper boundary.

### 8. What is the difference between population variance and sample variance ($ddof=1$)?
Population variance ($\sigma^2$) divides the sum of squared deviations by $N$. Sample variance ($s^2$) divides by $n - 1$ (Bessel's correction). We use $n - 1$ because sample deviations around the sample mean $\bar{x}$ underestimate the true spread around the population mean $\mu$; dividing by $n - 1$ provides an unbiased estimator of $\sigma^2$.

### 9. What are Quartiles and the Interquartile Range (IQR)?
- **$Q_1$ (25th percentile):** $25\%$ of observations fall below this value ($14.23$ marks for midterm).
- **$Q_2$ (50th percentile / Median):** The midpoint ($21.35$ marks for midterm).
- **$Q_3$ (75th percentile):** $75\%$ of observations fall below this value ($27.43$ marks for midterm).
- **$\text{IQR} = Q_3 - Q_1$:** Measures the spread of the middle $50\%$ of the data ($13.20$ marks).

### 10. Why is the IQR preferred over the Range when assessing dispersion?
The full range ($\text{Max} - \text{Min}$) depends entirely on the two extreme values and is heavily distorted by outliers. The IQR ignores the top $25\%$ and bottom $25\%$, providing a robust measure of spread that remains stable even in the presence of extreme values.

### 11. What is an outlier and did you detect any in Midterm Marks?
An outlier is an observation that lies outside the interval $[Q_1 - 1.5 \times \text{IQR},\; Q_3 + 1.5 \times \text{IQR}]$. For midterm marks:
- Lower threshold: $14.225 - 1.5 \times 13.20 = -5.575$ (clamped at 0)
- Upper threshold: $27.425 + 1.5 \times 13.20 = 47.225$ (clamped at 30)
Because all midterm marks fall between $0$ and $30$, no statistical outliers were present under the $1.5 \times \text{IQR}$ rule.

---

## Section C: Inferential Statistics & Hypothesis Testing

### 12. What is a Confidence Interval?
A confidence interval gives an estimated range of values calculated from sample data that is likely to include an unknown population parameter. A $95\%$ confidence interval means that if we repeated the sampling procedure many times, $95\%$ of the constructed intervals would contain the true population mean.

### 13. What is the 95% Confidence Interval for mean Midterm Marks in your project?
The $95\%$ CI is **$[19.03,\; 20.91]$ marks**.  
With sample mean $\bar{x} = 19.97$, $s = 8.27$, $n = 300$, and $t_{0.025, 299} = 1.9679$, the standard error is $SE = 0.4776$ and margin of error is $E = 0.9399$.

### 14. Why did you use the Student's $t$-distribution instead of the standard normal ($Z$) distribution?
Although $n = 300$ is large, the true population standard deviation $\sigma$ is unknown and must be estimated using the sample standard deviation $s$. In formal probability and statistics, estimating $\sigma$ with $s$ strictly requires the $t$-distribution with $n - 1$ degrees of freedom.

### 15. What are a Null Hypothesis ($H_0$) and an Alternative Hypothesis ($H_1$)?
- **$H_0$ (Null Hypothesis):** Represents default skepticism—no effect, no difference, or no relationship ($\mu_1 = \mu_2$).
- **$H_1$ (Alternative Hypothesis):** The research claim that an effect or difference exists ($\mu_1 \neq \mu_2$).

### 16. What is a $p$-value and what does $\alpha = 0.05$ signify?
- **$\alpha$ (Significance Level):** The maximum acceptable probability of committing a Type I error (rejecting a true null hypothesis). We set $\alpha = 0.05$ ($5\%$).
- **$p$-value:** The probability of obtaining test results at least as extreme as the observed data, assuming $H_0$ is true. If $p \le \alpha$, we reject $H_0$; if $p > \alpha$, we fail to reject $H_0$.

### 17. What were the results of your independent-samples $t$-test?
We tested mean midterm scores between Low attendance students ($<50\%$, $n=141$, $\bar{x}=19.91$) and High attendance students ($\ge 75\%$, $n=58$, $\bar{x}=18.04$).
- Welch's $t$-statistic: $t = 1.3392$
- $p$-value: $0.1838$
- Decision: **Fail to Reject $H_0$** ($p > 0.05$). There is no statistically significant difference in mean midterm performance between low and high attendance students.

### 18. Why did you use Welch's $t$-test rather than Student's two-sample $t$-test?
Student's pooled $t$-test requires equal population variances ($\sigma_1^2 = \sigma_2^2$). Welch's $t$-test adjusts the degrees of freedom to account for potentially unequal variances and sample sizes ($n_1 = 141$ vs. $n_2 = 58$), avoiding inflated Type I error rates.

### 19. What was your One-Way ANOVA test and what did it conclude?
We tested equality of mean midterm marks across all three attendance groups (Low: $19.91$, Moderate: $21.16$, High: $18.04$).
- $F$-statistic: $2.6616$
- $p$-value: $0.0715$
- Decision: **Fail to Reject $H_0$** at $\alpha = 0.05$. Differences in midterm performance among the three attendance tiers are not statistically significant.

### 20. What is Levene's test and what did it show?
Levene's test assesses the ANOVA assumption of homogeneity of variance ($H_0: \sigma_1^2 = \sigma_2^2 = \sigma_3^2$). In our data, $W = 2.4612, p = 0.0871$. Since $p > 0.05$, the assumption of equal variances across attendance groups was not violated.

### 21. Does "Failing to Reject $H_0$" mean we proved the groups are identical?
No. In statistical hypothesis testing, we never "accept" or "prove" the null hypothesis. Failing to reject $H_0$ simply indicates that our sample does not provide sufficient empirical evidence to contradict the assumption of equal means at the chosen significance level.

---

## Section D: Correlation Analysis

### 22. What is Pearson's Correlation Coefficient ($r$)?
Pearson's $r$ measures the strength and direction of a linear relationship between two continuous variables on a scale from $-1.0$ (perfect negative) to $+1.0$ (perfect positive), with $0.0$ indicating no linear relationship.

### 23. What correlation did you find between overall attendance and midterm marks?
$r = +0.0015$ with $p = 0.9790$. This indicates that linear correlation between attendance and midterm scores in this dataset is essentially zero and statistically indistinguishable from chance.

### 24. Did overall attendance correlate with quizzes, GPA, or finals?
- With `avg_quiz_marks`: $r = -0.0357$ ($p = 0.5378$)
- With `previous_gpa`: $r = -0.0380$ ($p = 0.5125$)
- With `final_marks`: $r = +0.0343$ ($p = 0.5536$)  
All correlations with attendance were negligible ($|r| < 0.05$) and non-significant.

### 25. Explain the principle: "Correlation does not imply causation."
Even if two variables show a high correlation coefficient, that mathematical association does not prove that changes in one variable cause changes in the other. Both could be influenced by a lurking/confounding variable, or the correlation could be entirely coincidental. Furthermore, in our project, there is no correlation to begin with.

---

## Section E: Regression & Machine Learning

### 26. What is Simple Linear Regression (SLR)?
SLR models the relationship between a single continuous predictor ($X$) and a continuous target ($Y$) using a straight line: $\hat{Y} = b_0 + b_1 X$, where $b_0$ is the intercept and $b_1$ is the slope.

### 27. What is your Simple Linear Regression equation and what do the coefficients mean?
$$\widehat{\text{Midterm}} = 20.7955 - 0.0157 \times (\text{Overall Attendance \%})$$
- **Intercept ($b_0 = 20.7955$):** The theoretical expected midterm mark if a student had $0\%$ attendance.
- **Slope ($b_1 = -0.0157$):** For each $1\%$ increase in overall attendance, midterm marks decrease by an imperceptible $0.016$ marks.

### 28. What is Multiple Linear Regression (MLR) and what equation did you obtain?
MLR extends linear regression to multiple predictors: $\hat{Y} = b_0 + b_1 X_1 + b_2 X_2 + \dots + b_k X_k$.
$$\widehat{\text{Midterm}} = 24.8117 - 0.0189(\text{Att\%}) - 0.6408(\text{Quiz}) + 0.0595(\text{GPA}) - 0.0028(\text{Age})$$

### 29. Why did we use an 80:20 train/test split with `random_state=42`?
- **Train/Test Split:** $80\%$ of data ($n=240$) trains the model; $20\%$ ($n=60$) evaluates generalization on unseen observations.
- **`random_state=42`:** Fixes the pseudo-random number generator seed so that the dataset is partitioned identically every time, ensuring reproducibility.

### 30. What is data leakage and how did we prevent it?
Data leakage occurs when information from outside the training dataset (such as test set values or future outcomes like `final_marks`) is used to build or scale the model. We prevented it by fitting our regression models strictly on the $240$ training instances and excluding target-derived or post-midterm variables.

### 31. Define MAE, MSE, and RMSE.
- **MAE (Mean Absolute Error):** Average magnitude of absolute residuals: $\frac{1}{n} \sum |y_i - \hat{y}_i|$. ($6.63$ marks for SLR).
- **MSE (Mean Squared Error):** Average of squared residuals: $\frac{1}{n} \sum (y_i - \hat{y}_i)^2$. Penalizes large errors heavily ($64.37$ for SLR).
- **RMSE (Root Mean Squared Error):** Square root of MSE ($\sqrt{\text{MSE}}$). Expresses error in the original units of marks ($8.02$ marks for SLR).

### 32. What is $R^2$ (Coefficient of Determination)?
$R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$. On training data, it measures the proportion of variance in $Y$ explained by the independent variables. On unseen test data, it measures model performance relative to a baseline that predicts the training mean $\bar{y}_{\text{train}}$.

### 33. Why did your models produce a negative $R^2$ on the test set?
Our test $R^2$ values were **$-0.0198$ (SLR)** and **$-0.0637$ (MLR)**.  
A negative test $R^2$ occurs mathematically when the sum of squared errors from the model ($SS_{\text{res}}$) is greater than the sum of squared errors from simply guessing the training mean ($SS_{\text{tot}}$). It means the fitted regression plane performs worse than a simple horizontal benchmark line on unseen data.

### 34. Why did Multiple Regression perform worse than Simple Regression?
In our data, none of the predictors (`overall_attendance_pct`, `avg_quiz_marks`, `previous_gpa`, `age`) share a true linear relationship with `midterm_marks`. Adding uncorrelated predictors introduced extra parameter estimation variance without providing predictive signal, leading to poorer out-of-sample generalization.

---

## Section F: Project-Specific Synthesis

### 35. What is the single most important statistical takeaway from this project?
In this synthetic dataset, student attendance and internal assessments exhibit virtually zero correlation with midterm marks ($r = 0.0015$), and linear regression models fail to predict performance ($R^2 < 0$). Reporting this negative result honestly demonstrates statistical competence, as real statistical practice involves discovering what the data actually says rather than forcing expected outcomes.

### 36. If you were provided real college academic records, what would you expect to change?
In real educational data, class attendance and continuous assessment scores typically exhibit moderate-to-strong positive correlations ($r \approx 0.35 - 0.65$) with exam marks because active learning and practice reinforce concept mastery. Additionally, nonlinear models or clustering might uncover distinct student engagement archetypes that linear models miss.

