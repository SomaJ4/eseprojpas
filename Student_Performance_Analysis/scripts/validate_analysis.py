"""
Parts B-I validation script.
Run this to verify all statistical calculations, tests, and models work
before packaging into notebooks.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

BASE = r"d:\PAS\ese_project\Student_Performance_Analysis"
CLEAN = os.path.join(BASE, "data", "cleaned", "student_performance_cleaned.csv")
GRAPHS = os.path.join(BASE, "outputs", "graphs")
RESULTS = os.path.join(BASE, "outputs", "results")
os.makedirs(GRAPHS, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

df = pd.read_csv(CLEAN)
print("Loaded cleaned dataset:", df.shape)

# ===========================================================
# PART B — DESCRIPTIVE STATISTICS
# ===========================================================
print("\n========== PART B — DESCRIPTIVE STATISTICS ==========")

def describe_variable(series, label):
    vals = series.dropna().values
    mean_val   = np.mean(vals)
    median_val = np.median(vals)
    # mode: use pandas for numeric
    mode_val   = float(pd.Series(vals).mode().iloc[0])
    var_val    = np.var(vals, ddof=1)
    std_val    = np.std(vals, ddof=1)
    min_val    = np.min(vals)
    max_val    = np.max(vals)
    range_val  = max_val - min_val
    q1         = np.percentile(vals, 25)
    q2         = np.percentile(vals, 50)
    q3         = np.percentile(vals, 75)
    iqr        = q3 - q1
    print(f"\n--- {label} ---")
    print(f"  Mean              : {mean_val:.4f}")
    print(f"  Median (Q2)       : {median_val:.4f}")
    print(f"  Mode              : {mode_val:.4f}")
    print(f"  Variance (sample) : {var_val:.4f}")
    print(f"  Std Dev (sample)  : {std_val:.4f}")
    print(f"  Min               : {min_val:.4f}")
    print(f"  Max               : {max_val:.4f}")
    print(f"  Range             : {range_val:.4f}")
    print(f"  Q1 (25th pct)     : {q1:.4f}")
    print(f"  Q3 (75th pct)     : {q3:.4f}")
    print(f"  IQR (Q3 - Q1)     : {iqr:.4f}")
    return dict(mean=mean_val, median=median_val, mode=mode_val,
                variance=var_val, std=std_val, min=min_val, max=max_val,
                range=range_val, q1=q1, q2=q2, q3=q3, iqr=iqr)

stats_overall_att  = describe_variable(df["overall_attendance_pct"], "Overall Attendance %")
stats_lec_att      = describe_variable(df["lecture_attendance_pct"], "Lecture Attendance %")
stats_lab_att      = describe_variable(df["lab_attendance_pct"],     "Lab Attendance %")
stats_midterm      = describe_variable(df["midterm_marks"],           "Midterm Marks")
stats_final        = describe_variable(df["final_marks"],             "Final Marks")
stats_avg_quiz     = describe_variable(df["avg_quiz_marks"],          "Average Quiz Marks")
stats_prev_gpa     = describe_variable(df["previous_gpa"],            "Previous GPA")

# Save summary table
rows = []
for label, s in [("Overall Attendance %", stats_overall_att),
                 ("Lecture Attendance %", stats_lec_att),
                 ("Lab Attendance %",     stats_lab_att),
                 ("Midterm Marks",        stats_midterm),
                 ("Final Marks",          stats_final),
                 ("Avg Quiz Marks",       stats_avg_quiz),
                 ("Previous GPA",         stats_prev_gpa)]:
    row = {"Variable": label}
    row.update(s)
    rows.append(row)
desc_df = pd.DataFrame(rows).set_index("Variable").round(4)
desc_df.to_csv(os.path.join(RESULTS, "descriptive_statistics.csv"))
print("\nDescriptive statistics saved.")

# --- Attendance groups ---
def classify_attendance(pct):
    if pct < 50:
        return "Low"
    elif pct < 75:
        return "Moderate"
    else:
        return "High"

df["attendance_group"] = df["overall_attendance_pct"].apply(classify_attendance)
group_summary = df.groupby("attendance_group").agg(
    num_students   = ("student_id", "count"),
    mean_midterm   = ("midterm_marks", "mean"),
    mean_avg_quiz  = ("avg_quiz_marks", "mean")
).round(4)
print("\n--- Attendance Group Summary ---")
print(group_summary)
group_summary.to_csv(os.path.join(RESULTS, "attendance_group_summary.csv"))

# ===========================================================
# VISUALIZATIONS
# ===========================================================
print("\n========== VISUALIZATIONS ==========")

def save_fig(fname):
    path = os.path.join(GRAPHS, fname)
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"  Saved: {fname}")

# 1. Histogram — overall attendance
plt.figure(figsize=(8, 5))
plt.hist(df["overall_attendance_pct"], bins=15, color="steelblue", edgecolor="black")
plt.title("Distribution of Overall Attendance (%)")
plt.xlabel("Overall Attendance (%)")
plt.ylabel("Number of Students")
plt.tight_layout()
save_fig("hist_overall_attendance.png")

# 2. Histogram — midterm marks
plt.figure(figsize=(8, 5))
plt.hist(df["midterm_marks"], bins=15, color="darkorange", edgecolor="black")
plt.title("Distribution of Midterm Marks")
plt.xlabel("Midterm Marks (out of 30)")
plt.ylabel("Number of Students")
plt.tight_layout()
save_fig("hist_midterm_marks.png")

# 3. Histogram — average quiz marks
plt.figure(figsize=(8, 5))
plt.hist(df["avg_quiz_marks"], bins=15, color="mediumseagreen", edgecolor="black")
plt.title("Distribution of Average Quiz Marks")
plt.xlabel("Average Quiz Marks (out of 10)")
plt.ylabel("Number of Students")
plt.tight_layout()
save_fig("hist_avg_quiz_marks.png")

# 4. Box plot — midterm marks
plt.figure(figsize=(6, 6))
plt.boxplot(df["midterm_marks"].dropna(), patch_artist=True,
            boxprops=dict(facecolor="lightyellow", color="navy"),
            medianprops=dict(color="red"))
plt.title("Box Plot — Midterm Marks")
plt.ylabel("Midterm Marks (out of 30)")
plt.tight_layout()
save_fig("boxplot_midterm.png")

# 5. Box plot — midterm by attendance group
order = ["Low", "Moderate", "High"]
groups_data = [df[df["attendance_group"] == g]["midterm_marks"].values for g in order]
plt.figure(figsize=(8, 6))
plt.boxplot(groups_data, tick_labels=order, patch_artist=True,
            boxprops=dict(facecolor="lightblue", color="navy"),
            medianprops=dict(color="red"))
plt.title("Midterm Marks by Attendance Group")
plt.xlabel("Attendance Group")
plt.ylabel("Midterm Marks (out of 30)")
plt.tight_layout()
save_fig("boxplot_midterm_by_group.png")

# 6. Scatter — attendance vs midterm
plt.figure(figsize=(8, 6))
colors = {"Low": "red", "Moderate": "orange", "High": "green"}
for grp, color in colors.items():
    subset = df[df["attendance_group"] == grp]
    plt.scatter(subset["overall_attendance_pct"], subset["midterm_marks"],
                color=color, label=grp, alpha=0.6)
plt.title("Overall Attendance vs Midterm Marks")
plt.xlabel("Overall Attendance (%)")
plt.ylabel("Midterm Marks (out of 30)")
plt.legend(title="Attendance Group")
plt.tight_layout()
save_fig("scatter_attendance_vs_midterm.png")

# 7. Scatter — attendance vs avg quiz
plt.figure(figsize=(8, 6))
for grp, color in colors.items():
    subset = df[df["attendance_group"] == grp]
    plt.scatter(subset["overall_attendance_pct"], subset["avg_quiz_marks"],
                color=color, label=grp, alpha=0.6)
plt.title("Overall Attendance vs Average Quiz Marks")
plt.xlabel("Overall Attendance (%)")
plt.ylabel("Average Quiz Marks (out of 10)")
plt.legend(title="Attendance Group")
plt.tight_layout()
save_fig("scatter_attendance_vs_avg_quiz.png")

# 8. Bar chart — mean midterm by group
group_means = df.groupby("attendance_group")["midterm_marks"].mean().reindex(order)
plt.figure(figsize=(7, 5))
bars = plt.bar(order, group_means.values, color=["red","orange","green"], edgecolor="black")
for bar, val in zip(bars, group_means.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{val:.1f}", ha="center", va="bottom", fontsize=10)
plt.title("Mean Midterm Marks by Attendance Group")
plt.xlabel("Attendance Group")
plt.ylabel("Mean Midterm Marks (out of 30)")
plt.tight_layout()
save_fig("bar_mean_midterm_by_group.png")

# 9. Histogram — lab attendance
plt.figure(figsize=(8, 5))
plt.hist(df["lab_attendance_pct"], bins=10, color="mediumpurple", edgecolor="black")
plt.title("Distribution of Lab Attendance (%)")
plt.xlabel("Lab Attendance (%)")
plt.ylabel("Number of Students")
plt.tight_layout()
save_fig("hist_lab_attendance.png")

print("All graphs saved.")

# ===========================================================
# PART C — CONFIDENCE INTERVAL
# ===========================================================
print("\n========== PART C — CONFIDENCE INTERVAL ==========")
n = len(df["midterm_marks"])
x_bar = np.mean(df["midterm_marks"])
s = np.std(df["midterm_marks"], ddof=1)
df_t = n - 1
alpha = 0.05
t_crit = stats.t.ppf(1 - alpha/2, df=df_t)
se = s / np.sqrt(n)
margin_of_error = t_crit * se
ci_lower = x_bar - margin_of_error
ci_upper = x_bar + margin_of_error

print(f"  n                 = {n}")
print(f"  Sample Mean (x̄)  = {x_bar:.4f}")
print(f"  Std Dev (s)       = {s:.4f}")
print(f"  Degrees of Freedom= {df_t}")
print(f"  t-critical (95%)  = {t_crit:.4f}")
print(f"  Standard Error    = {se:.4f}")
print(f"  Margin of Error   = {margin_of_error:.4f}")
print(f"  95% CI            = ({ci_lower:.4f}, {ci_upper:.4f})")

ci_results = {
    "n": n, "mean": round(x_bar,4), "std_dev": round(s,4),
    "df": df_t, "t_critical": round(t_crit,4), "std_error": round(se,4),
    "margin_of_error": round(margin_of_error,4),
    "ci_lower_95": round(ci_lower,4), "ci_upper_95": round(ci_upper,4)
}
pd.Series(ci_results).to_csv(os.path.join(RESULTS, "confidence_interval_midterm.csv"), header=["Value"])
print("  CI results saved.")

# ===========================================================
# PART D — HYPOTHESIS TESTING
# ===========================================================
print("\n========== PART D — HYPOTHESIS TESTING ==========")

# --- Test 1: Welch's t-test: Low vs High attendance ---
low_group  = df[df["attendance_group"] == "Low"]["midterm_marks"].values
high_group = df[df["attendance_group"] == "High"]["midterm_marks"].values

print(f"\n  Low attendance  — n={len(low_group)}, mean={np.mean(low_group):.4f}")
print(f"  High attendance — n={len(high_group)}, mean={np.mean(high_group):.4f}")

t_stat, p_val = stats.ttest_ind(low_group, high_group, equal_var=False)
df_welch = (s**2/n + s**2/n)**2 / ((s**2/n)**2/(n-1) + (s**2/n)**2/(n-1))
# use scipy's output directly
print(f"  Welch's t = {t_stat:.4f}")
print(f"  p-value   = {p_val:.6f}")
alpha_test = 0.05
decision_t = "Reject H0" if p_val < alpha_test else "Fail to Reject H0"
print(f"  Decision  : {decision_t}")

t_test_results = {
    "group_low_n": len(low_group), "group_low_mean": round(np.mean(low_group),4),
    "group_high_n": len(high_group), "group_high_mean": round(np.mean(high_group),4),
    "t_statistic": round(t_stat,4), "p_value": round(p_val,6),
    "alpha": alpha_test, "decision": decision_t
}
pd.Series(t_test_results).to_csv(os.path.join(RESULTS, "ttest_low_vs_high.csv"), header=["Value"])

# --- Test 2: One-way ANOVA ---
moderate_group = df[df["attendance_group"] == "Moderate"]["midterm_marks"].values
f_stat, p_anova = stats.f_oneway(low_group, moderate_group, high_group)
print(f"\n  ANOVA F = {f_stat:.4f}, p = {p_anova:.6f}")
decision_anova = "Reject H0" if p_anova < alpha_test else "Fail to Reject H0"
print(f"  Decision: {decision_anova}")

# Levene test for equal variances
levene_stat, levene_p = stats.levene(low_group, moderate_group, high_group)
print(f"  Levene's test for equal variance: stat={levene_stat:.4f}, p={levene_p:.6f}")

anova_results = {
    "group_low_n": len(low_group), "group_low_mean": round(np.mean(low_group),4),
    "group_mod_n": len(moderate_group), "group_mod_mean": round(np.mean(moderate_group),4),
    "group_high_n": len(high_group), "group_high_mean": round(np.mean(high_group),4),
    "F_statistic": round(f_stat,4), "p_value": round(p_anova,6),
    "levene_stat": round(levene_stat,4), "levene_p": round(levene_p,6),
    "alpha": alpha_test, "decision": decision_anova
}
pd.Series(anova_results).to_csv(os.path.join(RESULTS, "anova_attendance_groups.csv"), header=["Value"])

# ===========================================================
# PART E — CORRELATION ANALYSIS
# ===========================================================
print("\n========== PART E — CORRELATION ANALYSIS ==========")

targets = ["midterm_marks", "avg_quiz_marks", "final_marks", "previous_gpa"]
for target in targets:
    r, p = stats.pearsonr(df["overall_attendance_pct"], df[target])
    print(f"  overall_attendance_pct vs {target:20s}: r={r:.4f}, p={p:.6f}")

corr_cols = ["overall_attendance_pct", "lecture_attendance_pct", "lab_attendance_pct",
             "avg_quiz_marks", "midterm_marks", "final_marks", "previous_gpa", "age"]
corr_matrix = df[corr_cols].corr(method="pearson").round(4)
corr_matrix.to_csv(os.path.join(RESULTS, "correlation_matrix.csv"))
print("\nCorrelation matrix saved.")
print(corr_matrix)

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            linewidths=0.5, vmin=-1, vmax=1)
plt.title("Pearson Correlation Heatmap")
plt.tight_layout()
save_fig("heatmap_correlation.png")

# ===========================================================
# PART F — SIMPLE LINEAR REGRESSION
# ===========================================================
print("\n========== PART F — SIMPLE LINEAR REGRESSION ==========")

X_simple = df[["overall_attendance_pct"]].values
y = df["midterm_marks"].values

X_tr, X_te, y_tr, y_te = train_test_split(X_simple, y, test_size=0.2, random_state=42)
print(f"  Train size: {len(X_tr)}, Test size: {len(X_te)}")

slr = LinearRegression()
slr.fit(X_tr, y_tr)
intercept_slr = slr.intercept_
coef_slr = slr.coef_[0]
print(f"  Intercept (b0): {intercept_slr:.4f}")
print(f"  Coefficient (b1): {coef_slr:.4f}")
print(f"  Regression equation: Midterm = {intercept_slr:.4f} + {coef_slr:.4f} * OverallAttendance%")

y_pred_slr = slr.predict(X_te)
mae_slr  = mean_absolute_error(y_te, y_pred_slr)
mse_slr  = mean_squared_error(y_te, y_pred_slr)
rmse_slr = np.sqrt(mse_slr)
r2_slr   = r2_score(y_te, y_pred_slr)
print(f"  MAE={mae_slr:.4f}, MSE={mse_slr:.4f}, RMSE={rmse_slr:.4f}, R2={r2_slr:.4f}")

# Actual vs Predicted plot
plt.figure(figsize=(8, 6))
plt.scatter(y_te, y_pred_slr, color="steelblue", alpha=0.7)
min_val = min(y_te.min(), y_pred_slr.min())
max_val = max(y_te.max(), y_pred_slr.max())
plt.plot([min_val, max_val], [min_val, max_val], "r--", label="Perfect prediction")
plt.title("Simple Linear Regression — Actual vs Predicted Midterm Marks")
plt.xlabel("Actual Midterm Marks")
plt.ylabel("Predicted Midterm Marks")
plt.legend()
plt.tight_layout()
save_fig("slr_actual_vs_predicted.png")

# Regression line plot
x_line = np.linspace(0, 100, 200).reshape(-1, 1)
y_line = slr.predict(x_line)
plt.figure(figsize=(8, 6))
plt.scatter(df["overall_attendance_pct"], df["midterm_marks"],
            color="steelblue", alpha=0.5, label="Observations")
plt.plot(x_line, y_line, color="red", linewidth=2, label="Regression line")
plt.title("Simple Linear Regression — Attendance vs Midterm Marks")
plt.xlabel("Overall Attendance (%)")
plt.ylabel("Midterm Marks (out of 30)")
plt.legend()
plt.tight_layout()
save_fig("slr_regression_line.png")

# ===========================================================
# PART G — MULTIPLE LINEAR REGRESSION
# ===========================================================
print("\n========== PART G — MULTIPLE LINEAR REGRESSION ==========")

feature_cols = ["overall_attendance_pct", "avg_quiz_marks", "previous_gpa", "age"]
X_multi = df[feature_cols].values
y_multi = df["midterm_marks"].values

X_tr_m, X_te_m, y_tr_m, y_te_m = train_test_split(X_multi, y_multi, test_size=0.2, random_state=42)
print(f"  Features: {feature_cols}")
print(f"  Train size: {len(X_tr_m)}, Test size: {len(X_te_m)}")

mlr = LinearRegression()
mlr.fit(X_tr_m, y_tr_m)
intercept_mlr = mlr.intercept_
coefs_mlr = mlr.coef_

print(f"  Intercept: {intercept_mlr:.4f}")
for fname, coef in zip(feature_cols, coefs_mlr):
    print(f"  {fname}: {coef:.4f}")

eq_parts = " + ".join([f"{c:.4f}*{f}" for f, c in zip(feature_cols, coefs_mlr)])
print(f"  Equation: Midterm = {intercept_mlr:.4f} + {eq_parts}")

y_pred_mlr = mlr.predict(X_te_m)
mae_mlr  = mean_absolute_error(y_te_m, y_pred_mlr)
mse_mlr  = mean_squared_error(y_te_m, y_pred_mlr)
rmse_mlr = np.sqrt(mse_mlr)
r2_mlr   = r2_score(y_te_m, y_pred_mlr)
print(f"  MAE={mae_mlr:.4f}, MSE={mse_mlr:.4f}, RMSE={rmse_mlr:.4f}, R2={r2_mlr:.4f}")

# Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_te_m, y_pred_mlr, color="darkorchid", alpha=0.7)
min_val = min(y_te_m.min(), y_pred_mlr.min())
max_val = max(y_te_m.max(), y_pred_mlr.max())
plt.plot([min_val, max_val], [min_val, max_val], "r--", label="Perfect prediction")
plt.title("Multiple Linear Regression — Actual vs Predicted Midterm Marks")
plt.xlabel("Actual Midterm Marks")
plt.ylabel("Predicted Midterm Marks")
plt.legend()
plt.tight_layout()
save_fig("mlr_actual_vs_predicted.png")

# ===========================================================
# PART H — MODEL EVALUATION TABLE
# ===========================================================
print("\n========== PART H — MODEL EVALUATION ==========")

eval_df = pd.DataFrame({
    "Metric": ["MAE", "MSE", "RMSE", "R²"],
    "Simple Linear Regression": [round(mae_slr,4), round(mse_slr,4), round(rmse_slr,4), round(r2_slr,4)],
    "Multiple Linear Regression": [round(mae_mlr,4), round(mse_mlr,4), round(rmse_mlr,4), round(r2_mlr,4)]
})
print(eval_df.to_string(index=False))
eval_df.to_csv(os.path.join(RESULTS, "model_evaluation_comparison.csv"), index=False)
print("  Evaluation table saved.")

# ===========================================================
# PART I — PREDICTIONS ON UNSEEN TEST DATA
# ===========================================================
print("\n========== PART I — PREDICTIONS ON UNSEEN DATA ==========")

# Use the SAME test set (y_te_m / X_te_m) — it was never seen during training
predictions_df = pd.DataFrame({
    "Actual_Midterm":          y_te_m,
    "SLR_Predicted":           y_pred_slr.round(4),
    "SLR_Error":               (y_te_m - y_pred_slr).round(4),
    "MLR_Predicted":           y_pred_mlr.round(4),
    "MLR_Error":               (y_te_m - y_pred_mlr).round(4),
})
predictions_df = predictions_df.reset_index(drop=True)
predictions_df.index.name = "Test_Index"
predictions_df.to_csv(os.path.join(RESULTS, "predictions_test_set.csv"))

print(predictions_df.head(10).to_string())
print("\n  All test predictions saved.")

print("\n========== VALIDATION COMPLETE ==========")
