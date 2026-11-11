"""
Part A - Data Cleaning and Feature Engineering
Validates all cleaning logic before notebook creation.
"""
import pandas as pd
import numpy as np
import os

BASE = r"d:\PAS\ese_project\Student_Performance_Analysis"
ORIG = os.path.join(BASE, "data", "original", "student_performance.csv")
CLEAN_DIR = os.path.join(BASE, "data", "cleaned")
CLEAN_PATH = os.path.join(CLEAN_DIR, "student_performance_cleaned.csv")

os.makedirs(CLEAN_DIR, exist_ok=True)

# --- Load ---
df = pd.read_csv(ORIG)
print("Original shape:", df.shape)
print("Original columns:", list(df.columns))

# --- Drop assignments_submitted (100% NaN) ---
df = df.drop(columns=["assignments_submitted"])
print("\nAfter dropping assignments_submitted:", df.shape)

# --- Check remaining missing ---
print("\nRemaining missing values:")
print(df.isnull().sum())

# --- Check duplicates ---
print("\nDuplicate rows:", df.duplicated().sum())

# --- Validate ranges ---
print("\n--- Range validation ---")
# Marks ranges
print("quiz1_marks:       ", df["quiz1_marks"].min(), "to", df["quiz1_marks"].max())
print("quiz2_marks:       ", df["quiz2_marks"].min(), "to", df["quiz2_marks"].max())
print("quiz3_marks:       ", df["quiz3_marks"].min(), "to", df["quiz3_marks"].max())
print("midterm_marks:     ", df["midterm_marks"].min(), "to", df["midterm_marks"].max())
print("final_marks:       ", df["final_marks"].min(), "to", df["final_marks"].max())
print("previous_gpa:      ", df["previous_gpa"].min(), "to", df["previous_gpa"].max())

# Attendance counts
print("lectures_attended: ", df["lectures_attended"].min(), "to", df["lectures_attended"].max())
print("total_lectures:    ", df["total_lectures"].unique())
print("labs_attended:     ", df["labs_attended"].min(), "to", df["labs_attended"].max())
print("total_lab_sessions:", df["total_lab_sessions"].unique())

# Check no student attended more lectures than total
invalid_lec = (df["lectures_attended"] > df["total_lectures"]).sum()
invalid_lab = (df["labs_attended"] > df["total_lab_sessions"]).sum()
print(f"\nInvalid lecture attendance (attended > total): {invalid_lec}")
print(f"Invalid lab attendance (attended > total): {invalid_lab}")

# --- Feature engineering ---
# Avoid division by zero (though total_lectures and total_lab_sessions are fixed constants)
df["lecture_attendance_pct"] = np.where(
    df["total_lectures"] > 0,
    (df["lectures_attended"] / df["total_lectures"]) * 100,
    0.0
)

df["lab_attendance_pct"] = np.where(
    df["total_lab_sessions"] > 0,
    (df["labs_attended"] / df["total_lab_sessions"]) * 100,
    0.0
)

df["overall_attendance_pct"] = np.where(
    (df["total_lectures"] + df["total_lab_sessions"]) > 0,
    ((df["lectures_attended"] + df["labs_attended"]) /
     (df["total_lectures"] + df["total_lab_sessions"])) * 100,
    0.0
)

df["avg_quiz_marks"] = (df["quiz1_marks"] + df["quiz2_marks"] + df["quiz3_marks"]) / 3

print("\n--- Derived columns preview ---")
print(df[["lecture_attendance_pct","lab_attendance_pct","overall_attendance_pct","avg_quiz_marks"]].describe().round(2))

# --- Save ---
df.to_csv(CLEAN_PATH, index=False)
print(f"\nCleaned dataset saved: {CLEAN_PATH}")
print("Cleaned shape:", df.shape)
print("Columns:", list(df.columns))

