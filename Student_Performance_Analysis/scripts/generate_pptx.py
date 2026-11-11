"""
Script to generate the official academic PowerPoint presentation (12 slides)
using python-pptx with clean typography and embedded high-res graphs.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"d:\PAS\ese_project\Student_Performance_Analysis"
GRAPHS_DIR = os.path.join(BASE_DIR, "outputs", "graphs")
PPTX_PATH = os.path.join(BASE_DIR, "presentation", "Student_Attendance_Performance_Analysis.pptx")

os.makedirs(os.path.dirname(PPTX_PATH), exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
NAVY = RGBColor(24, 43, 73)
TEAL = RGBColor(16, 124, 130)
DARK_GRAY = RGBColor(50, 50, 50)
LIGHT_GRAY = RGBColor(245, 247, 250)
WHITE = RGBColor(255, 255, 255)
ACCENT_BLUE = RGBColor(41, 128, 185)

def add_header(slide, title_text, subtitle_text="Probability & Statistics Course Project"):
    # Header banner
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY
    banner.line.color.rgb = NAVY
    
    tf = banner.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(180, 205, 230)

blank_layout = prs.slide_layouts[6]

# ==========================================
# Slide 1: Title Slide
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.color.rgb = NAVY

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "Student Attendance & Internal Assessment Performance Analysis"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = WHITE

p = tf1.add_paragraph()
p.text = "An Empirical Probability and Statistics End-Semester Study"
p.font.size = Pt(20)
p.font.color.rgb = RGBColor(180, 210, 240)
p.space_after = Pt(40)

p = tf1.add_paragraph()
p.text = "Student Name: [Student Name Here]   |   Roll Number: [Roll Number Here]"
p.font.size = Pt(16)
p.font.color.rgb = WHITE

p = tf1.add_paragraph()
p.text = "Department: Computer Science / Information Technology"
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(200, 220, 240)

p = tf1.add_paragraph()
p.text = "Faculty Guide: [Faculty Guide / Course Instructor Name]"
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(200, 220, 240)

# ==========================================
# Slide 2: Problem Statement & Objectives
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "1. Problem Statement & Research Objectives")

tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
tf2 = tb2.text_frame
tf2.word_wrap = True

def add_bullet(tf, heading, text):
    p = tf.add_paragraph()
    p.text = heading + ": "
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY
    p.space_before = Pt(14)
    run = p.add_run()
    run.text = text
    run.font.bold = False
    run.font.size = Pt(15)
    run.font.color.rgb = DARK_GRAY

add_bullet(tf2, "Context", "In higher education, regular attendance and continuous formative assessments are conventionally assumed to drive examination performance.")
add_bullet(tf2, "Core Research Question", "Does higher attendance (lectures and labs) statistically translate into superior midterm examination scores in an empirical educational dataset?")
add_bullet(tf2, "Project Objectives", "")
tf2.add_paragraph().text = "   • Clean, validate, and engineer meaningful academic engagement metrics from raw records."
tf2.paragraphs[-1].font.size = Pt(14)
tf2.add_paragraph().text = "   • Compute rigorous descriptive statistics (mean, median, IQR) and construct a 95% Confidence Interval."
tf2.paragraphs[-1].font.size = Pt(14)
tf2.add_paragraph().text = "   • Formally test hypotheses via Welch's two-sample t-test and One-Way ANOVA across attendance groups."
tf2.paragraphs[-1].font.size = Pt(14)
tf2.add_paragraph().text = "   • Develop, evaluate, and benchmark Simple and Multiple Linear Regression models on unseen test data."
tf2.paragraphs[-1].font.size = Pt(14)

# ==========================================
# Slide 3: Dataset Description
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "2. Dataset Description & Specifications")

tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(6.0), Inches(5.6))
tf3 = tb3.text_frame
tf3.word_wrap = True
add_bullet(tf3, "Dataset Name", "Student Performance and Clustering Dataset")
add_bullet(tf3, "Author & Source", "Muhammad Khubaib Ahmad (Kaggle, DOI: 10.34740/kaggle/dsv/13489035)")
add_bullet(tf3, "License", "Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)")
add_bullet(tf3, "Observations", "300 rows (individual student records)")
add_bullet(tf3, "Raw Features", "16 features (demographics, assessments, attendance counts)")
add_bullet(tf3, "Methodological Note", "Synthetic/illustrative dataset with undocumented sampling. Findings reflect this dataset specifically and cannot be generalized to real college cohorts.")

# Add right-side table
rows, cols = 8, 2
left, top, width, height = Inches(7.2), Inches(1.5), Inches(5.3), Inches(5.2)
table_shape = s3.shapes.add_table(rows, cols, left, top, width, height)
table = table_shape.table
table.columns[0].width = Inches(2.8)
table.columns[1].width = Inches(2.5)

data_specs = [
    ("Metric / Feature", "Specification"),
    ("Total Observations", "300 Students"),
    ("Scheduled Lectures", "12 Fixed Sessions"),
    ("Scheduled Labs", "6 Fixed Sessions"),
    ("Quizzes Conducted", "3 Quizzes (Scale 0-10)"),
    ("Midterm Exam", "Scale 0-30 Marks"),
    ("Final Exam", "Scale 0-50 Marks"),
    ("Previous GPA", "Scale 0-4.0")
]
for r_idx, (c1, c2) in enumerate(data_specs):
    cell1, cell2 = table.cell(r_idx, 0), table.cell(r_idx, 1)
    cell1.text, cell2.text = c1, c2
    for cell in (cell1, cell2):
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r_idx == 0 else LIGHT_GRAY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(13 if r_idx == 0 else 12)
        p.font.bold = (r_idx == 0)
        p.font.color.rgb = WHITE if r_idx == 0 else DARK_GRAY

# ==========================================
# Slide 4: Data Preprocessing & Feature Engineering
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "3. Data Preprocessing & Feature Engineering")

tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(5.8))
tf4 = tb4.text_frame
tf4.word_wrap = True

add_bullet(tf4, "1. Missing Value Remediation", "Inspected null frequencies across all 16 features. assignments_submitted was entirely empty (300/300 nulls, 100%) and was dropped. Zero missing values remained in all other features.")
add_bullet(tf4, "2. Consistency Validation", "Verified that no student attended more sessions than scheduled (lectures <= 12, labs <= 6). Verified all marks fell within valid intervals (0 duplicates found).")
add_bullet(tf4, "3. Mathematical Feature Engineering", "")
tf4.add_paragraph().text = "   • Lecture Attendance % = (lectures_attended / 12) * 100"
tf4.paragraphs[-1].font.size = Pt(14)
tf4.add_paragraph().text = "   • Lab Attendance % = (labs_attended / 6) * 100"
tf4.paragraphs[-1].font.size = Pt(14)
tf4.add_paragraph().text = "   • Overall Attendance % = ((lectures_attended + labs_attended) / 18) * 100"
tf4.paragraphs[-1].font.size = Pt(14)
tf4.add_paragraph().text = "   • Average Quiz Marks = (quiz1_marks + quiz2_marks + quiz3_marks) / 3"
tf4.paragraphs[-1].font.size = Pt(14)
add_bullet(tf4, "4. Clean Dataset Storage", "Exported to data/cleaned/student_performance_cleaned.csv (300 rows x 19 columns) without altering the raw original CSV.")

# ==========================================
# Slide 5: Descriptive Statistics
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "4. Descriptive Statistical Analysis")

table_shape5 = s5.shapes.add_table(6, 6, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.2))
t5 = table_shape5.table
headers5 = ["Variable", "Mean", "Median", "Std Dev", "Range", "IQR (Q3-Q1)"]
rows5 = [
    ["Overall Attendance %", "50.69%", "50.00%", "23.28%", "100.00%", "38.89%"],
    ["Lecture Attendance %", "50.11%", "50.00%", "31.05%", "100.00%", "50.00%"],
    ["Lab Attendance %", "51.83%", "50.00%", "33.04%", "100.00%", "66.67%"],
    ["Midterm Marks (/30)", "19.97", "21.35", "8.27", "30.00", "13.20"],
    ["Average Quiz Marks (/10)", "6.20", "6.15", "1.28", "7.30", "1.68"],
]
for col_idx, h in enumerate(headers5):
    t5.cell(0, col_idx).text = h
    t5.cell(0, col_idx).fill.solid()
    t5.cell(0, col_idx).fill.fore_color.rgb = NAVY
    p = t5.cell(0, col_idx).text_frame.paragraphs[0]
    p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = WHITE

for r_idx, row in enumerate(rows5):
    for c_idx, val in enumerate(row):
        cell = t5.cell(r_idx + 1, c_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_GRAY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12); p.font.color.rgb = DARK_GRAY

tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(11.7), Inches(2.2))
tf5 = tb5.text_frame
tf5.word_wrap = True
add_bullet(tf5, "Key Takeaway", "Attendance spans the full theoretical spectrum (0% to 100%) with a mean of 50.69% and median of 50.00%.")
add_bullet(tf5, "Distributional Insight", "Midterm marks exhibit mild negative skew: median (21.35) exceeds mean (19.97), and IQR is 13.20 marks.")

# ==========================================
# Slide 6: Attendance Group Comparison
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "5. Attendance-Group Stratification & Visualization")

# Image on left
img_path6 = os.path.join(GRAPHS_DIR, "bar_mean_midterm_by_group.png")
if os.path.exists(img_path6):
    s6.shapes.add_picture(img_path6, Inches(0.8), Inches(1.4), width=Inches(5.5))

tb6 = s6.shapes.add_textbox(Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.5))
tf6 = tb6.text_frame
tf6.word_wrap = True
add_bullet(tf6, "Stratification Scheme", "Students partitioned into three distinct tiers based on overall attendance percentage:")
tf6.add_paragraph().text = "   • Low Attendance (< 50%): n = 141 students (47.0%)"
tf6.paragraphs[-1].font.size = Pt(13)
tf6.add_paragraph().text = "   • Moderate Attendance (50% to < 75%): n = 101 students (33.7%)"
tf6.paragraphs[-1].font.size = Pt(13)
tf6.add_paragraph().text = "   • High Attendance (>= 75%): n = 58 students (19.3%)"
tf6.paragraphs[-1].font.size = Pt(13)

add_bullet(tf6, "Group Performance Breakdown", "")
tf6.add_paragraph().text = "   • Low Attendance: Mean Midterm = 19.91 marks, Quiz = 6.26"
tf6.paragraphs[-1].font.size = Pt(13)
tf6.add_paragraph().text = "   • Moderate Attendance: Mean Midterm = 21.16 marks, Quiz = 6.10"
tf6.paragraphs[-1].font.size = Pt(13)
tf6.add_paragraph().text = "   • High Attendance: Mean Midterm = 18.04 marks, Quiz = 6.21"
tf6.paragraphs[-1].font.size = Pt(13)
add_bullet(tf6, "Counter-Intuitive Finding", "The High Attendance cohort achieved the lowest mean midterm mark (18.04), indicating an absence of the expected positive linear gradient.")

# ==========================================
# Slide 7: Confidence Interval & Hypothesis Testing
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "6. Inferential Statistics & Hypothesis Testing")

tb7_l = s7.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.6), Inches(5.8))
tf7_l = tb7_l.text_frame
tf7_l.word_wrap = True

add_bullet(tf7_l, "95% Confidence Interval for Midterm", "Parametric interval using Student's t-distribution:")
tf7_l.add_paragraph().text = "   Formula: CI = x̄ ± t_{α/2, df} * (s / √n)"
tf7_l.paragraphs[-1].font.size = Pt(13); tf7_l.paragraphs[-1].font.bold = True
tf7_l.add_paragraph().text = "   • Sample Mean (x̄) = 19.9690"
tf7_l.paragraphs[-1].font.size = Pt(12)
tf7_l.add_paragraph().text = "   • Std Dev (s) = 8.2722, n = 300, df = 299"
tf7_l.paragraphs[-1].font.size = Pt(12)
tf7_l.add_paragraph().text = "   • Critical t = 1.9679, Std Error = 0.4776"
tf7_l.paragraphs[-1].font.size = Pt(12)
tf7_l.add_paragraph().text = "   • Margin of Error = 0.9399"
tf7_l.paragraphs[-1].font.size = Pt(12)
tf7_l.add_paragraph().text = "   95% CI = [19.03, 20.91] Marks"
tf7_l.paragraphs[-1].font.size = Pt(14); tf7_l.paragraphs[-1].font.bold = True; tf7_l.paragraphs[-1].font.color.rgb = TEAL

tb7_r = s7.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.8))
tf7_r = tb7_r.text_frame
tf7_r.word_wrap = True

add_bullet(tf7_r, "Test 1: Welch's Two-Sample t-Test", "Comparing Low (<50%, n=141) vs High (>=75%, n=58) Attendance:")
tf7_r.add_paragraph().text = "   • H0: μ_Low = μ_High  vs  H1: μ_Low ≠ μ_High"
tf7_r.paragraphs[-1].font.size = Pt(12)
tf7_r.add_paragraph().text = "   • t = 1.3392,  p-value = 0.1838"
tf7_r.paragraphs[-1].font.size = Pt(13); tf7_r.paragraphs[-1].font.bold = True
tf7_r.add_paragraph().text = "   • Decision (α=0.05): Fail to Reject H0 (p > 0.05)"
tf7_r.paragraphs[-1].font.size = Pt(13); tf7_r.paragraphs[-1].font.color.rgb = ACCENT_BLUE

add_bullet(tf7_r, "Test 2: One-Way ANOVA", "Comparing means across all 3 attendance tiers:")
tf7_r.add_paragraph().text = "   • Levene's Test: W = 2.4612, p = 0.0871 (Equal variance holds)"
tf7_r.paragraphs[-1].font.size = Pt(12)
tf7_r.add_paragraph().text = "   • F-statistic = 2.6616,  p-value = 0.0715"
tf7_r.paragraphs[-1].font.size = Pt(13); tf7_r.paragraphs[-1].font.bold = True
tf7_r.add_paragraph().text = "   • Decision (α=0.05): Fail to Reject H0 (p > 0.05)"
tf7_r.paragraphs[-1].font.size = Pt(13); tf7_r.paragraphs[-1].font.color.rgb = ACCENT_BLUE

# ==========================================
# Slide 8: Correlation Findings
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "7. Correlation Analysis & Matrix")

img_path8 = os.path.join(GRAPHS_DIR, "heatmap_correlation.png")
if os.path.exists(img_path8):
    s8.shapes.add_picture(img_path8, Inches(0.8), Inches(1.3), width=Inches(5.6))

tb8 = s8.shapes.add_textbox(Inches(6.7), Inches(1.3), Inches(5.8), Inches(5.8))
tf8 = tb8.text_frame
tf8.word_wrap = True

add_bullet(tf8, "Pearson Correlation Coefficients (r)", "")
tf8.add_paragraph().text = "   • Overall Attendance vs Midterm: r = +0.0015 (p = 0.9790)"
tf8.paragraphs[-1].font.size = Pt(13); tf8.paragraphs[-1].font.bold = True
tf8.add_paragraph().text = "   • Overall Attendance vs Avg Quiz: r = -0.0357 (p = 0.5378)"
tf8.paragraphs[-1].font.size = Pt(13)
tf8.add_paragraph().text = "   • Overall Attendance vs Final Marks: r = +0.0343 (p = 0.5536)"
tf8.paragraphs[-1].font.size = Pt(13)
tf8.add_paragraph().text = "   • Overall Attendance vs Previous GPA: r = -0.0380 (p = 0.5125)"
tf8.paragraphs[-1].font.size = Pt(13)

add_bullet(tf8, "Interpretation of Relationships", "All linear correlation coefficients with attendance are near zero (|r| < 0.04) and statistically non-significant (p > 0.50).")
add_bullet(tf8, "Critical Statistical Principle", "Correlation measures linear association, not causation. In this synthetic dataset, linear association is completely absent.")

# ==========================================
# Slide 9: Regression Models & Equations
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "8. Regression Modelling (SLR & MLR)")

tb9_l = s9.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.6), Inches(5.8))
tf9_l = tb9_l.text_frame
tf9_l.word_wrap = True

add_bullet(tf9_l, "Model 1: Simple Linear Regression", "Bivariate model predicting Midterm from Attendance:")
tf9_l.add_paragraph().text = "   • Predictor (X): Overall Attendance %"
tf9_l.paragraphs[-1].font.size = Pt(13)
tf9_l.add_paragraph().text = "   • Split: 80% Train (n=240), 20% Test (n=60)"
tf9_l.paragraphs[-1].font.size = Pt(13)
tf9_l.add_paragraph().text = "   • Random Seed: random_state = 42"
tf9_l.paragraphs[-1].font.size = Pt(13)
tf9_l.add_paragraph().text = "   • Intercept (b0): 20.7955"
tf9_l.paragraphs[-1].font.size = Pt(13)
tf9_l.add_paragraph().text = "   • Slope (b1): -0.0157"
tf9_l.paragraphs[-1].font.size = Pt(13)
tf9_l.add_paragraph().text = "   Equation: Midterm = 20.7955 - 0.0157 * (Attendance %)"
tf9_l.paragraphs[-1].font.size = Pt(13); tf9_l.paragraphs[-1].font.bold = True; tf9_l.paragraphs[-1].font.color.rgb = TEAL

tb9_r = s9.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.8))
tf9_r = tb9_r.text_frame
tf9_r.word_wrap = True

add_bullet(tf9_r, "Model 2: Multiple Linear Regression", "Multivariate model incorporating academic history & demographics:")
tf9_r.add_paragraph().text = "   • Features: Attendance %, Avg Quiz, GPA, Age"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   • Fitted strictly on training set (No Data Leakage)"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   • Intercept: 24.8117"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   • Attendance % Coef: -0.0189"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   • Avg Quiz Marks Coef: -0.6408"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   • Previous GPA Coef: +0.0595, Age Coef: -0.0028"
tf9_r.paragraphs[-1].font.size = Pt(13)
tf9_r.add_paragraph().text = "   Equation: Midterm = 24.81 - 0.02(Att) - 0.64(Quiz) + 0.06(GPA) - 0.003(Age)"
tf9_r.paragraphs[-1].font.size = Pt(12); tf9_r.paragraphs[-1].font.bold = True; tf9_r.paragraphs[-1].font.color.rgb = TEAL

# ==========================================
# Slide 10: Model Evaluation & Predictions
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "9. Model Evaluation & Out-of-Sample Predictions")

# Table for metrics
t_s10 = s10.shapes.add_table(5, 3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(2.8)).table
t_s10.columns[0].width = Inches(1.8)
t_s10.columns[1].width = Inches(1.9)
t_s10.columns[2].width = Inches(1.9)

m_data = [
    ("Metric", "Simple Linear Reg", "Multiple Linear Reg"),
    ("MAE", "6.6292 Marks", "6.6987 Marks"),
    ("MSE", "64.3656", "67.1423"),
    ("RMSE", "8.0228 Marks", "8.1940 Marks"),
    ("R² Score", "-0.0198", "-0.0637")
]
for r_idx, row in enumerate(m_data):
    for c_idx, val in enumerate(row):
        cell = t_s10.cell(r_idx, c_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r_idx == 0 else (WHITE if r_idx % 2 == 1 else LIGHT_GRAY)
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12 if r_idx > 0 else 13)
        p.font.bold = (r_idx == 0 or c_idx == 0)
        p.font.color.rgb = WHITE if r_idx == 0 else DARK_GRAY

tb10_exp = s10.shapes.add_textbox(Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.7))
tf10_exp = tb10_exp.text_frame
tf10_exp.word_wrap = True
add_bullet(tf10_exp, "Understanding Negative R²", "R² < 0 indicates the regression equations perform worse than a naive horizontal benchmark predicting the training mean (ȳ_train).")
add_bullet(tf10_exp, "Model Comparison", "MLR performed worse than SLR (-0.0637 vs -0.0198): adding uncorrelated features introduced noise without explanatory power.")

# Table for predictions on right
t_p10 = s10.shapes.add_table(6, 4, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5)).table
t_p10.columns[0].width = Inches(1.2)
t_p10.columns[1].width = Inches(1.5)
t_p10.columns[2].width = Inches(1.5)
t_p10.columns[3].width = Inches(1.5)

p_sample = [
    ("Test Idx", "Actual (/30)", "SLR Pred", "MLR Pred"),
    ("Student 0", "23.10", "20.45", "20.83"),
    ("Student 1", "12.70", "20.27", "19.27"),
    ("Student 2", "22.80", "20.36", "19.57"),
    ("Student 3", "16.90", "20.45", "20.19"),
    ("Student 4", "25.40", "20.18", "20.75"),
]
for r_idx, row in enumerate(p_sample):
    for c_idx, val in enumerate(row):
        cell = t_p10.cell(r_idx, c_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r_idx == 0 else (WHITE if r_idx % 2 == 1 else LIGHT_GRAY)
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12 if r_idx > 0 else 13)
        p.font.bold = (r_idx == 0 or c_idx == 0)
        p.font.color.rgb = WHITE if r_idx == 0 else DARK_GRAY

# ==========================================
# Slide 11: Key Findings & Limitations
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "11. Analytical Findings & Methodological Limitations")

tb11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(5.8))
tf11 = tb11.text_frame
tf11.word_wrap = True

add_bullet(tf11, "1. Absence of Linear Association", "In this dataset, overall attendance does not correlate with midterm marks (r = +0.0015). Statistically, attendance accounts for none of the variance in test scores.")
add_bullet(tf11, "2. Hypothesis Testing Alignment", "Both Welch's two-sample t-test (p = 0.1838) and One-Way ANOVA (p = 0.0715) failed to reject the null hypothesis at alpha = 0.05, confirming lack of statistical significance across attendance groups.")
add_bullet(tf11, "3. Synthetic Data Architecture", "The dataset is synthetic/illustrative and demonstrates signs of independently simulated attributes rather than real behavioural human dynamics.")
add_bullet(tf11, "4. Methodological Boundaries", "Because sampling weights and collection mechanisms are undocumented, findings must not be generalized to real university populations.")
add_bullet(tf11, "5. Honest Scientific Reporting", "Authentic data science and statistics require reporting empirical findings transparently rather than manipulating data to force idealized relationships.")

# ==========================================
# Slide 12: Conclusion
# ==========================================
s12 = prs.slides.add_slide(blank_layout)
bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg12.fill.solid()
bg12.fill.fore_color.rgb = NAVY
bg12.line.color.rgb = NAVY

tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(5.0))
tf12 = tb12.text_frame
tf12.word_wrap = True

p = tf12.paragraphs[0]
p.text = "Conclusion & Course Project Synthesis"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = WHITE
p.space_after = Pt(25)

concl_bullets = [
    "Comprehensive PAS Implementation: Successfully executed the end-to-end curriculum pipeline—cleaning, EDA, t-distribution CI, Welch's t-test, ANOVA, Pearson correlation, and supervised linear regression.",
    "Rigorous Evaluation: Demonstrated that neither Simple nor Multiple Linear Regression could predict midterm marks effectively (R² = -0.02 and -0.06), outperforming by naive mean prediction.",
    "Scientific Integrity: Accurately identified and documented the synthetic nature of the dataset and avoided artificial data manipulation.",
    "Future Work with Real Data: Real-world academic data would likely exhibit positive attendance-performance dynamics (r ≈ 0.40) and benefit from non-linear and clustering methods."
]
for b in concl_bullets:
    p = tf12.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(220, 235, 250)
    p.space_after = Pt(14)

prs.save(PPTX_PATH)
print("PPTX generated successfully:", PPTX_PATH)

