"""
Script to compile the comprehensive 15-20 page official academic report
using ReportLab with custom canvas page numbering and embedded figures.
"""
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from pypdf import PdfReader

BASE_DIR = r"d:\PAS\ese_project\Student_Performance_Analysis"
GRAPHS_DIR = os.path.join(BASE_DIR, "outputs", "graphs")
RESULTS_DIR = os.path.join(BASE_DIR, "outputs", "results")
REPORT_PDF = os.path.join(BASE_DIR, "report", "Student_Attendance_Performance_Analysis_Report.pdf")

os.makedirs(os.path.dirname(REPORT_PDF), exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            
            # Running header
            self.drawString(54, 750, "Probability & Statistics End-Semester Course Project Report")
            self.drawRightString(558, 750, "Student Attendance & Performance Analysis")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Running footer
            self.line(54, 45, 558, 45)
            self.drawString(54, 32, "Confidential — For Academic Evaluation Only")
            self.drawRightString(558, 32, f"Page {self._pageNumber} of {total_pages}")
            self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        REPORT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    NAVY = colors.HexColor("#182B49")
    TEAL = colors.HexColor("#107C82")
    DARK = colors.HexColor("#222222")
    LIGHT_BG = colors.HexColor("#F5F7FA")
    LINE_CLR = colors.HexColor("#D0D7DE")

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=NAVY, alignment=1, spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18,
        textColor=TEAL, alignment=1, spaceAfter=25
    )
    h1_style = ParagraphStyle(
        'Header1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=NAVY, spaceBefore=16, spaceAfter=8, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=TEAL, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=DARK, spaceAfter=7
    )
    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=colors.HexColor("#333333")
    )
    code_style = ParagraphStyle(
        'CodeStyle', parent=styles['Normal'],
        fontName='Courier', fontSize=8.5, leading=11,
        textColor=colors.HexColor("#1A365D")
    )
    tbl_hdr_style = ParagraphStyle(
        'TblHdr', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.white, alignment=1
    )
    tbl_cell_style = ParagraphStyle(
        'TblCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=DARK, alignment=1
    )

    story = []

    def p(text): return Paragraph(text, body_style)
    def h1(text): return Paragraph(text, h1_style)
    def h2(text): return Paragraph(text, h2_style)
    def hr(): return HRFlowable(width="100%", thickness=0.5, color=LINE_CLR, spaceBefore=8, spaceAfter=8)

    def callout_box(text):
        tbl = Table([[Paragraph(text, callout_style)]], colWidths=[500])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 1, TEAL),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        return tbl

    # ============================================================
    # 1. COVER PAGE
    # ============================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("A COURSE PROJECT REPORT ON", ParagraphStyle('SubSub', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#777777"), alignment=1, spaceAfter=15)))
    story.append(Paragraph("Student Attendance and Internal Assessment Performance Analysis", title_style))
    story.append(Paragraph("A Rigorous Empirical Study in Probability, Inferential Statistics & Supervised Regression", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=2, color=TEAL, spaceBefore=10, spaceAfter=30))
    
    meta_text = """
    <b>Course:</b> Probability and Statistics (PAS)<br/>
    <b>Academic Period:</b> End-Semester Examination Project<br/>
    <b>Degree Program:</b> Bachelor of Technology (B.Tech / B.E.)<br/>
    <b>Department:</b> Computer Science and Engineering / Information Technology<br/><br/>
    <b>Submitted By:</b> [Student Name Here]<br/>
    <b>Roll / Registration Number:</b> [Roll Number Here]<br/>
    <b>Batch / Division:</b> [Class / Division Here]<br/><br/>
    <b>Project Supervisor / Faculty Guide:</b> [Faculty Guide Name Here]<br/>
    <b>Institution:</b> [College / University Name Here]<br/>
    <b>Submission Date:</b> November 2026
    """
    story.append(callout_box(meta_text))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Notice:</b> This academic project utilizes an open-access Kaggle dataset by Muhammad Khubaib Ahmad. All data cleaning, hypothesis tests, confidence intervals, regression equations, and predictive evaluations represent genuine calculations executed on the verified dataset.", ParagraphStyle('Disc', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#666666"), alignment=1)))
    story.append(PageBreak())

    # ============================================================
    # 2. ABSTRACT & TABLE OF CONTENTS
    # ============================================================
    story.append(h1("2. Executive Abstract"))
    story.append(hr())
    abstract_text = """
    This project presents an end-to-end statistical examination of the relationship between student class attendance (lectures and laboratory sessions) and academic performance metrics (quizzes, midterms, GPA, and final exams). Utilizing the <i>Student Performance and Clustering Dataset</i> (300 observations, originally 16 attributes) authored by Muhammad Khubaib Ahmad on Kaggle, we implement standard exploratory data analysis, parametric estimation, hypothesis testing, correlation analysis, and predictive linear regression.<br/><br/>
    Initial data cleaning revealed that the attribute <code>assignments_submitted</code> was 100% missing (300/300 null cells) and was consequently removed. Four standardized features were engineered: lecture attendance percentage, lab attendance percentage, combined overall attendance percentage, and mean quiz marks. Descriptive analysis demonstrated that overall attendance averages 50.69% (IQR = 38.89%), while midterm scores average 19.97 out of 30 (IQR = 13.20 marks). A 95% confidence interval for mean midterm marks was determined using Student's t-distribution as [19.03, 20.91] marks.<br/><br/>
    Formal inferential testing yielded non-significant results across attendance categories: Welch's independent two-sample t-test between low (<50%) and high (>=75%) attendance cohorts yielded t = 1.3392 (p = 0.1838 > 0.05), and One-Way ANOVA across three attendance tiers yielded F = 2.6616 (p = 0.0715 > 0.05). Pearson correlation between attendance and midterm marks was negligible (r = +0.0015, p = 0.9790). Simple and Multiple Linear Regression models both exhibited negative test R² scores (-0.0198 and -0.0637), proving that linear models generalize worse than predicting the historical training mean. Crucially, we document that the underlying dataset is synthetic/illustrative and explain why statistical integrity requires transparent reporting of these findings without artificial data manipulation.
    """
    story.append(p(abstract_text))
    story.append(Spacer(1, 15))

    story.append(h1("Table of Contents"))
    story.append(hr())
    toc_data = [
        ("Section", "Title", "Topic Summary"),
        ("1", "Cover Page & Metadata", "Title, student/institution placeholders, project metadata"),
        ("2", "Abstract & Table of Contents", "Executive project overview and syllabus structure"),
        ("3", "Introduction & Problem Statement", "Academic context, motivation, and research questions"),
        ("4", "Project Objectives", "Curriculum alignment with course project requirements"),
        ("5", "Dataset Description & Provenance", "Kaggle source, 300 observations, schema, and license"),
        ("6", "Sampling Methodology & Limitations", "Synthetic data architecture and generalizability boundaries"),
        ("7", "Data Cleaning & Preprocessing", "Handling 100% null assignments, range validations"),
        ("8", "Feature Engineering", "Formulas for lecture, lab, overall attendance %, and avg quiz"),
        ("9", "Descriptive Statistical Analysis", "Central tendency, sample variance, quartiles, and IQR"),
        ("10", "Attendance Group Stratification", "Low, Moderate, High cohort distributions and performance"),
        ("11", "Visualizations & Graphical Analysis", "Histograms, box plots, scatter plots, and bar charts"),
        ("12", "Parametric Confidence Interval", "Student's t-distribution 95% CI calculation on midterms"),
        ("13", "Hypothesis Testing I: Welch's t-Test", "Two-sample testing between Low and High attendance"),
        ("14", "Hypothesis Testing II: One-Way ANOVA", "Variance homogeneity (Levene's) and 3-group F-test"),
        ("15", "Correlation Analysis & Heatmap", "Pearson r matrix, linear association vs. causation"),
        ("16", "Simple Linear Regression (SLR)", "Bivariate model, equation, slope, intercept, and fit"),
        ("17", "Multiple Linear Regression (MLR)", "Multivariate model with attendance, quiz, GPA, and age"),
        ("18", "Model Evaluation & Benchmarking", "MAE, MSE, RMSE, and explanation of negative test R²"),
        ("19", "Out-of-Sample Predictions", "Tabular display of 10 unseen test predictions and residuals"),
        ("20", "Comprehensive Discussion", "Analytical interpretation and pedagogical implications"),
        ("21", "Limitations of the Study", "Synthetic artifacts, lack of confounders, and linearity limits"),
        ("22", "Conclusion & Future Scope", "Final synthesis and recommendations for real college data"),
        ("23", "Academic References", "Statistical textbooks, documentation, and Kaggle DOI")
    ]
    toc_tbl = Table(
        [[Paragraph(f"<b>{c[0]}</b>", tbl_cell_style), Paragraph(c[1], ParagraphStyle('L', parent=tbl_cell_style, alignment=0)), Paragraph(c[2], ParagraphStyle('L2', parent=tbl_cell_style, alignment=0))] for c in toc_data],
        colWidths=[40, 180, 280]
    )
    toc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(toc_tbl)
    story.append(PageBreak())

    # ============================================================
    # 3. INTRODUCTION & OBJECTIVES
    # ============================================================
    story.append(h1("3. Introduction & Problem Statement"))
    story.append(hr())
    story.append(p("""
    In university education, institutional regulatory frameworks consistently mandate minimum attendance thresholds (commonly 75%) based on the premise that presence during scheduled instructional hours directly improves academic learning and exam performance. Concurrently, continuous internal evaluations—such as periodic quizzes and mid-semester examinations—are deployed to monitor student progress and provide formative feedback before comprehensive final summative assessments.<br/><br/>
    Despite the widespread institutional acceptance of this paradigm, quantitative educational research reveals mixed empirical findings. In many contemporary settings, student learning styles, access to digital course repositories, independent study habits, and prior academic foundations exert substantial confounding effects. Therefore, empirically evaluating whether attendance metrics correlate with and predict examination performance is a central question in educational data analytics.
    """))
    story.append(h2("Problem Statement"))
    story.append(p("""
    <b>Primary Research Problem:</b> Does student attendance (in lectures and laboratory sessions) significantly impact and predict internal assessment performance (specifically midterm exam marks) in an empirical college cohort? Furthermore, can continuous internal quiz assessments and previous GPA improve predictive capability when modeled through multiple linear regression?
    """))

    story.append(h1("4. Project Objectives"))
    story.append(hr())
    story.append(p("""
    To address this problem within the Probability and Statistics (PAS) curriculum, this project establishes seven sequential technical milestones:
    <br/>
    1. <b>Data Audit & Sanitization:</b> Systematically inspect missing values, verify physical bounds of attendance and score attributes, and preserve the original data integrity.<br/>
    2. <b>Feature Standardization:</b> Engineer standardized percentage metrics for attendance and continuous internal assessments to enable scale-independent analysis.<br/>
    3. <b>Exploratory Descriptive Profiling:</b> Compute parametric (mean, standard deviation) and robust non-parametric (median, IQR) summary statistics alongside distributional visualizations.<br/>
    4. <b>Parametric Interval Estimation:</b> Derive an exact 95% confidence interval for mean midterm performance using the Student's t-distribution.<br/>
    5. <b>Inferential Hypothesis Testing:</b> Statistically test whether attendance stratification induces significant performance disparities via Welch's two-sample t-test and One-Way ANOVA.<br/>
    6. <b>Multivariate Correlation Profiling:</b> Establish bivariate linear relationships across all numeric metrics via Pearson's correlation matrix.<br/>
    7. <b>Supervised Predictive Modeling:</b> Train and evaluate Simple and Multiple Linear Regression models on an isolated 80:20 train/test split, strictly guarding against data leakage.
    """))
    story.append(PageBreak())

    # ============================================================
    # 5. DATASET DESCRIPTION & LIMITATIONS
    # ============================================================
    story.append(h1("5. Dataset Description & Provenance"))
    story.append(hr())
    story.append(p("""
    The official project specification dictates the exclusive use of the <b>Student Performance and Clustering Dataset</b> hosted on Kaggle and authored by Muhammad Khubaib Ahmad. The dataset is cataloged under the persistent Digital Object Identifier (DOI) <code>10.34740/kaggle/dsv/13489035</code> and licensed under the open Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).<br/><br/>
    The raw dataset contains 300 observations and 16 features. Below is the systematic data dictionary:
    """))
    
    dict_rows = [
        ("Column Name", "Storage Type", "Domain / Range", "Analytical Role"),
        ("student_id", "Integer (int64)", "1 to 300", "Unique primary key; excluded from predictive modeling"),
        ("name", "String (object)", "Text string", "Student identifier; masked to protect anonymity"),
        ("age", "Integer (int64)", "18 to 22 years", "Demographic control variable"),
        ("gender", "String (object)", "Male / Female", "Categorical demographic attribute"),
        ("quiz1_marks", "Float (float64)", "2.8 to 10.0 marks", "Continuous assessment 1 (scale 0-10)"),
        ("quiz2_marks", "Float (float64)", "0.0 to 10.0 marks", "Continuous assessment 2 (scale 0-10)"),
        ("quiz3_marks", "Float (float64)", "0.0 to 10.0 marks", "Continuous assessment 3 (scale 0-10)"),
        ("total_assignments", "Integer (int64)", "Constant = 5", "Administrative ceiling of assignments"),
        ("assignments_submitted", "Float (float64)", "100% NaN", "Unpopulated attribute; dropped during data cleaning"),
        ("midterm_marks", "Float (float64)", "0.0 to 30.0 marks", "Primary internal assessment target (Y)"),
        ("final_marks", "Float (float64)", "0.0 to 50.0 marks", "End-semester cumulative exam score"),
        ("previous_gpa", "Float (float64)", "0.61 to 4.00", "Historical GPA on a standard 4.0 scale"),
        ("total_lectures", "Integer (int64)", "Constant = 12", "Total scheduled theoretical lectures"),
        ("lectures_attended", "Integer (int64)", "0 to 12 lectures", "Theoretical attendance count"),
        ("total_lab_sessions", "Integer (int64)", "Constant = 6", "Total scheduled laboratory practicals"),
        ("labs_attended", "Integer (int64)", "0 to 6 sessions", "Practical laboratory attendance count")
    ]
    dict_tbl = Table(
        [[Paragraph(f"<b>{r[0]}</b>", tbl_cell_style), Paragraph(r[1], tbl_cell_style), Paragraph(r[2], tbl_cell_style), Paragraph(r[3], ParagraphStyle('LD', parent=tbl_cell_style, alignment=0))] for r in dict_rows],
        colWidths=[100, 75, 95, 230]
    )
    dict_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(dict_tbl)
    story.append(Spacer(1, 10))

    story.append(h1("6. Sampling Methodology & Scientific Limitations"))
    story.append(hr())
    story.append(callout_box("""
    <b>Mandatory Scientific Disclosure: Synthetic Data Limitations</b><br/>
    The author documentation designates this dataset as an illustrative benchmark created for demonstrating educational analytics, exploratory visualization, and unsupervised clustering algorithms. The archive metadata does not define a formal target population, sampling frame, or probabilistic sampling design. Consequently, all 300 rows must be classified as <b>synthetic / illustrative data</b>. The findings presented herein are technically valid representations of this specific dataset but cannot be generalized to real university student populations.
    """))
    story.append(PageBreak())

    # ============================================================
    # 7. DATA CLEANING & FEATURE ENGINEERING
    # ============================================================
    story.append(h1("7. Data Cleaning & Preprocessing"))
    story.append(hr())
    story.append(p("""
    Data cleaning was executed in a dedicated, reproducible Jupyter Notebook (<code>notebooks/02_data_cleaning.ipynb</code>). The original CSV file inside <code>data/original/</code> was maintained in an unmodified state throughout.<br/><br/>
    <b>Step 1: Dropping Unpopulated Column:</b> Systematic null checking across all features established that <code>assignments_submitted</code> contained exactly 300 missing values out of 300 rows (100% missing). Imputation with central measures (mean/median) would distort the feature distribution by fabricating 300 arbitrary records. Dropping this column reduced the feature space from 16 to 15 without discarding any student observations.<br/><br/>
    <b>Step 2: Checking Remaining Features:</b> Null checking on the remaining 15 features confirmed 0 missing values across all columns. Duplicate verification confirmed 0 redundant rows.<br/><br/>
    <b>Step 3: Range & Logical Boundary Verification:</b>
    Every observation was screened against logical consistency rules:
    """))
    story.append(p("• <i>Attendance ceiling check:</i> Verified that lectures_attended &le; total_lectures (max 12) &rarr; 0 violations.<br/>• <i>Lab ceiling check:</i> Verified that labs_attended &le; total_lab_sessions (max 6) &rarr; 0 violations.<br/>• <i>Score boundaries:</i> Verified quizzes &isin; [0, 10], midterm &isin; [0, 30], final &isin; [0, 50], and GPA &isin; [0, 4.0] &rarr; 0 violations."))

    story.append(h1("8. Feature Engineering"))
    story.append(hr())
    story.append(p("""
    To transform raw counts into standardized, scale-invariant metrics suitable for correlation and regression analysis, four derived continuous variables were engineered using safe conditional vectorization (<code>np.where</code>):
    """))
    
    fe_equations = """
    <b>1. Lecture Attendance Percentage:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;$$\\text{lecture\\_attendance\\_pct} = \\left( \\frac{\\text{lectures\\_attended}}{\\text{total\\_lectures}} \\right) \\times 100 = \\left( \\frac{\\text{lectures\\_attended}}{12} \\right) \\times 100$$<br/>
    <b>2. Lab Attendance Percentage:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;$$\\text{lab\\_attendance\\_pct} = \\left( \\frac{\\text{labs\\_attended}}{\\text{total\\_lab\\_sessions}} \\right) \\times 100 = \\left( \\frac{\\text{labs\\_attended}}{6} \\right) \\times 100$$<br/>
    <b>3. Overall Attendance Percentage:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;$$\\text{overall\\_attendance\\_pct} = \\left( \\frac{\\text{lectures\\_attended} + \\text{labs\\_attended}}{\\text{total\\_lectures} + \\text{total\\_lab\\_sessions}} \\right) \\times 100 = \\left( \\frac{\\text{lectures\\_attended} + \\text{labs\\_attended}}{18} \\right) \\times 100$$<br/>
    <b>4. Average Quiz Marks:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;$$\\text{avg\\_quiz\\_marks} = \\frac{\\text{quiz1\\_marks} + \\text{quiz2\\_marks} + \\text{quiz3\\_marks}}{3}$$
    """
    story.append(callout_box(fe_equations))
    story.append(p("<br/>The processed dataset was exported to <code>data/cleaned/student_performance_cleaned.csv</code> with dimensions 300 rows &times; 19 columns."))
    story.append(PageBreak())

    # ============================================================
    # 9. DESCRIPTIVE STATISTICS
    # ============================================================
    story.append(h1("9. Descriptive Statistical Analysis"))
    story.append(hr())
    story.append(p("""
    Descriptive statistics quantify the central tendency, dispersion, and shape of distributions. For this study, sample variance ($s^2$) and sample standard deviation ($s$) were computed with Bessel's correction ($ddof=1$):
    $$s^2 = \\frac{1}{n-1}\\sum_{i=1}^{n} (x_i - \\bar{x})^2, \\quad s = \\sqrt{s^2}$$
    The Interquartile Range (IQR) was derived as $IQR = Q_3 - Q_1$, representing the range of the central 50% of sorted observations.
    """))

    desc_path = os.path.join(RESULTS_DIR, "descriptive_statistics.csv")
    desc_df = pd.read_csv(desc_path)
    
    t_desc_rows = [["Variable", "Mean", "Median", "Mode", "Variance", "Std Dev", "Range", "IQR"]]
    for _, r in desc_df.iterrows():
        t_desc_rows.append([
            str(r["Variable"]), f"{r['Mean']:.2f}", f"{r['Median']:.2f}", f"{r['Mode']:.2f}",
            f"{r['Variance']:.2f}", f"{r['Std Dev']:.2f}", f"{r['Range']:.2f}", f"{r['IQR']:.2f}"
        ])
    t_desc = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(t_desc_rows)],
        colWidths=[120, 50, 50, 50, 60, 55, 55, 60]
    )
    t_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_desc)
    story.append(Spacer(1, 12))

    story.append(h2("Detailed Distributional Insights"))
    story.append(p("""
    • <b>Attendance Distribution:</b> Overall attendance has a mean of 50.69% and a median of 50.00% with a standard deviation of 23.28%. The IQR is 38.89% ($Q_1 = 33.33%, Q_3 = 72.22%$), showing a balanced spread across attendance tiers.<br/>
    • <b>Midterm Marks Distribution:</b> Midterm scores average 19.97 out of 30, with a median of 21.35 and an IQR of 13.20 ($Q_1 = 14.23, Q_3 = 27.43$). The median exceeds the mean by 1.38 marks, indicating a slight negative skew driven by students scoring at the upper boundary (the statistical mode is 30.00).<br/>
    • <b>Quiz Consistency:</b> Average quiz marks exhibit very narrow dispersion with a mean of 6.20 out of 10, a median of 6.15, and an IQR of only 1.68 marks ($Q_1 = 5.43, Q_3 = 7.11$), reflecting consistency across quiz performance.
    """))

    story.append(h1("10. Attendance Group Stratification"))
    story.append(hr())
    story.append(p("Students were partitioned into three academic engagement tiers based on institutional benchmarks:"))
    
    grp_path = os.path.join(RESULTS_DIR, "attendance_group_summary.csv")
    grp_df = pd.read_csv(grp_path)
    grp_rows = [["Attendance Group", "Criteria", "Students (n)", "Percent of Cohort", "Mean Midterm (/30)", "Mean Quiz (/10)"]]
    tot_st = grp_df["num_students"].sum()
    crit_map = {"Low": "Overall Attendance < 50%", "Moderate": "50% <= Overall Attendance < 75%", "High": "Overall Attendance >= 75%"}
    for _, r in grp_df.iterrows():
        g = r["attendance_group"]
        cnt = r["num_students"]
        grp_rows.append([g, crit_map.get(g, ""), str(cnt), f"{(cnt/tot_st)*100:.1f}%", f"{r['mean_midterm']:.2f}", f"{r['mean_avg_quiz']:.2f}"])
    
    t_grp = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(grp_rows)],
        colWidths=[90, 160, 65, 75, 60, 50]
    )
    t_grp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_grp)
    story.append(Spacer(1, 8))
    story.append(p("<b>Observation:</b> Contrary to traditional pedagogical assumptions, the High attendance cohort achieved a lower mean midterm score (18.04 marks) than both the Moderate (21.16) and Low (19.91) cohorts. This empirical discrepancy prompted the formal hypothesis testing detailed in Section 13."))
    story.append(PageBreak())

    # ============================================================
    # 11. VISUALIZATIONS & GRAPHICAL ANALYSIS
    # ============================================================
    story.append(h1("11. Visualizations & Graphical Analysis"))
    story.append(hr())
    story.append(p("Nine diagnostic visualizations were generated, analyzed, and persisted in <code>outputs/graphs/</code>:"))

    # Pair 1: Histograms of Attendance & Midterm
    img_att = os.path.join(GRAPHS_DIR, "hist_overall_attendance.png")
    img_mid = os.path.join(GRAPHS_DIR, "hist_midterm_marks.png")
    if os.path.exists(img_att) and os.path.exists(img_mid):
        img_tbl1 = Table([
            [Image(img_att, width=240, height=150), Image(img_mid, width=240, height=150)],
            [Paragraph("<b>Figure 1:</b> Histogram of Overall Attendance %", tbl_cell_style),
             Paragraph("<b>Figure 2:</b> Histogram of Midterm Marks", tbl_cell_style)]
        ], colWidths=[250, 250])
        img_tbl1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
        story.append(img_tbl1)
        story.append(Spacer(1, 10))

    # Pair 2: Box plots
    img_box1 = os.path.join(GRAPHS_DIR, "boxplot_midterm.png")
    img_box2 = os.path.join(GRAPHS_DIR, "boxplot_midterm_by_group.png")
    if os.path.exists(img_box1) and os.path.exists(img_box2):
        img_tbl2 = Table([
            [Image(img_box1, width=200, height=150), Image(img_box2, width=280, height=150)],
            [Paragraph("<b>Figure 3:</b> Box Plot of Overall Midterm Marks", tbl_cell_style),
             Paragraph("<b>Figure 4:</b> Midterm Marks by Attendance Group", tbl_cell_style)]
        ], colWidths=[210, 290])
        img_tbl2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
        story.append(img_tbl2)
        story.append(Spacer(1, 10))

    # Pair 3: Scatter & Bar chart
    img_scat = os.path.join(GRAPHS_DIR, "scatter_attendance_vs_midterm.png")
    img_bar = os.path.join(GRAPHS_DIR, "bar_mean_midterm_by_group.png")
    if os.path.exists(img_scat) and os.path.exists(img_bar):
        img_tbl3 = Table([
            [Image(img_scat, width=250, height=160), Image(img_bar, width=240, height=160)],
            [Paragraph("<b>Figure 5:</b> Attendance vs. Midterm Marks Scatter", tbl_cell_style),
             Paragraph("<b>Figure 6:</b> Mean Midterm Marks by Attendance Group", tbl_cell_style)]
        ], colWidths=[255, 245])
        img_tbl3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
        story.append(img_tbl3)

    story.append(PageBreak())

    # ============================================================
    # 12. CONFIDENCE INTERVAL
    # ============================================================
    story.append(h1("12. Parametric Confidence Interval"))
    story.append(hr())
    story.append(p("""
    A confidence interval estimates the plausible range within which an unknown population parameter lies. Because the true population standard deviation &sigma; is unknown and estimated using the sample standard deviation $s$, the formal construction requires the <b>Student's t-distribution</b> with $n - 1$ degrees of freedom.
    """))

    ci_formula_text = """
    <b>Formula for Mean Estimation:</b><br/>
    $$\\text{CI}_{1-\\alpha} = \\bar{x} \\pm t_{\\alpha/2, \\, df} \\times \\left( \\frac{s}{\\sqrt{n}} \\right) = \\bar{x} \\pm E$$<br/>
    where $\\bar{x}$ is the sample mean, $s$ is the sample standard deviation, $n$ is sample size, $df = n - 1$ is degrees of freedom, and $E$ is the margin of error.
    """
    story.append(callout_box(ci_formula_text))
    story.append(Spacer(1, 10))

    ci_path = os.path.join(RESULTS_DIR, "confidence_interval_midterm.csv")
    ci_s = pd.read_csv(ci_path).set_index("Unnamed: 0")["Value"]
    
    ci_table_data = [
        ("Parameter / Step", "Symbol", "Numerical Value", "Statistical Explanation"),
        ("Sample Size", "n", f"{int(float(ci_s['n']))}", "Total verified student observations"),
        ("Sample Mean", "x̄", f"{float(ci_s['mean']):.4f} marks", "Point estimate of central performance"),
        ("Sample Standard Deviation", "s", f"{float(ci_s['std_dev']):.4f} marks", "Unbiased sample dispersion with ddof=1"),
        ("Degrees of Freedom", "df", f"{int(float(ci_s['df']))}", "Computed as n - 1 (300 - 1)"),
        ("Significance Level", "α", "0.05", "Two-tailed probability mass outside interval"),
        ("Critical t-Value", "t_crit", f"{float(ci_s['t_critical']):.4f}", "Quantile from scipy.stats.t.ppf(0.975, df=299)"),
        ("Standard Error of Mean", "SE", f"{float(ci_s['std_error']):.4f} marks", "Computed as s / sqrt(n)"),
        ("Margin of Error", "E", f"{float(ci_s['margin_of_error']):.4f} marks", "Computed as t_crit * SE"),
        ("Lower Confidence Limit", "LCL", f"{float(ci_s['ci_lower_95']):.4f} marks", "x̄ - E"),
        ("Upper Confidence Limit", "UCL", f"{float(ci_s['ci_upper_95']):.4f} marks", "x̄ + E")
    ]
    t_ci = Table(
        [[Paragraph(f"<b>{r[0]}</b>" if idx==0 else r[0], tbl_cell_style), Paragraph(r[1], tbl_cell_style), Paragraph(r[2], tbl_cell_style), Paragraph(r[3], ParagraphStyle('LCI', parent=tbl_cell_style, alignment=0))] for idx, r in enumerate(ci_table_data)],
        colWidths=[130, 60, 90, 220]
    )
    t_ci.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ci)
    story.append(Spacer(1, 12))

    story.append(h2("Interpretation of Confidence Interval"))
    story.append(p(f"""
    <b>Formal Interpretation:</b> We are 95% confident that the true population mean midterm examination mark lies within the interval <b>[{float(ci_s['ci_lower_95']):.2f}, {float(ci_s['ci_upper_95']):.2f}] marks</b> (out of 30 marks). In repeated random sampling under identical conditions, 95% of such constructed intervals would encompass the true population mean.<br/><br/>
    <b>Limitation:</b> This inference is strictly bounded by the synthetic nature of the dataset. Because the sampling mechanism is artificial, this interval describes the parameters of this generated dataset and cannot be generalized to real academic university populations.
    """))
    story.append(PageBreak())

    # ============================================================
    # 13. HYPOTHESIS TESTING I: WELCH'S T-TEST
    # ============================================================
    story.append(h1("13. Hypothesis Testing I: Welch's Two-Sample t-Test"))
    story.append(hr())
    story.append(p("""
    To formally investigate whether student attendance generates statistically significant differences in midterm marks, an independent two-sample t-test was conducted between the extreme cohorts: Low Attendance (< 50%) and High Attendance (>= 75%).
    """))

    t_ttest_path = os.path.join(RESULTS_DIR, "ttest_low_vs_high.csv")
    ttest_s = pd.read_csv(t_ttest_path).set_index("Unnamed: 0")["Value"]

    hyp_t_text = """
    <b>Hypothesis Formulation:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Null Hypothesis (H0):</b> Mean_Low = Mean_High (Mean midterm scores are equal between Low and High attendance cohorts).<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Alternative Hypothesis (H1):</b> Mean_Low != Mean_High (Mean midterm scores differ significantly between cohorts).<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Decision Rule:</b> At significance level alpha = 0.05, reject H0 if p-value <= 0.05.
    """
    story.append(callout_box(hyp_t_text))
    story.append(Spacer(1, 8))

    story.append(h2("Welch's Formulation & Assumption Diagnostics"))
    story.append(p("""
    Because sample sizes differ substantially ($n_{\\text{Low}} = 141$ vs. $n_{\\text{High}} = 58$) and equality of population variance cannot be assumed, <b>Welch's t-test</b> was selected. Welch's test avoids pooled variance and computes effective degrees of freedom via the Welch–Satterthwaite equation:
    $$t = \\frac{\\bar{x}_1 - \\bar{x}_2}{\\sqrt{\\frac{s_1^2}{n_1} + \\frac{s_2^2}{n_2}}}$$
    """))

    ttest_tbl_data = [
        ("Group / Parameter", "Sample Size (n)", "Sample Mean (x̄)", "Sample Std Dev (s)"),
        ("Low Attendance (< 50%)", f"{int(float(ttest_s['low_n']))}", f"{float(ttest_s['low_mean']):.4f} marks", "8.20 marks"),
        ("High Attendance (>= 75%)", f"{int(float(ttest_s['high_n']))}", f"{float(ttest_s['high_mean']):.4f} marks", "8.89 marks")
    ]
    t_ttbl = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(ttest_tbl_data)],
        colWidths=[150, 100, 120, 130]
    )
    t_ttbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ttbl)
    story.append(Spacer(1, 8))

    res_t_text = f"""
    <b>Statistical Test Results:</b><br/>
    • Welch's Test Statistic: t = {float(ttest_s['t_statistic']):.4f}<br/>
    • Associated p-value: p = {float(ttest_s['p_value']):.6f} (p = {float(ttest_s['p_value']):.4f})<br/>
    • Decision at alpha = 0.05: <b>{ttest_s['decision']}</b> (p > 0.05)<br/>
    • <b>Statistical Conclusion:</b> The observed difference in sample means (19.91 vs. 18.04) is statistically indistinguishable from random sampling variability. There is no evidence of a significant difference in midterm marks between students with low attendance and those with high attendance in this dataset.
    """
    story.append(callout_box(res_t_text))
    story.append(PageBreak())

    # ============================================================
    # 14. HYPOTHESIS TESTING II: ONE-WAY ANOVA
    # ============================================================
    story.append(h1("14. Hypothesis Testing II: One-Way ANOVA"))
    story.append(hr())
    story.append(p("""
    To compare performance simultaneously across all three attendance tiers (Low, Moderate, and High), a <b>One-Way Analysis of Variance (ANOVA)</b> was conducted. ANOVA assesses whether the variance between group means exceeds what would be expected from random within-group variance.
    """))

    anova_path = os.path.join(RESULTS_DIR, "anova_attendance_groups.csv")
    anova_s = pd.read_csv(anova_path).set_index("Unnamed: 0")["Value"]

    hyp_a_text = """
    <b>ANOVA Hypothesis Formulation:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Null Hypothesis (H0):</b> Mean_Low = Mean_Moderate = Mean_High (All attendance groups share identical mean midterm marks).<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Alternative Hypothesis (H1):</b> At least one group mean differs from the others.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Decision Threshold:</b> alpha = 0.05.
    """
    story.append(callout_box(hyp_a_text))
    story.append(Spacer(1, 8))

    story.append(h2("Assumptions Verification (Normality & Homoscedasticity)"))
    story.append(p(f"""
    1. <b>Independence:</b> Assumed based on individual student observation rows.<br/>
    2. <b>Homoscedasticity (Equal Variances):</b> Evaluated via <b>Levene's Test</b>:<br/>
       W = {float(anova_s['levene_stat']):.4f}, p-value = {float(anova_s['levene_p']):.4f}<br/>
       Because p = {float(anova_s['levene_p']):.4f} > 0.05, we fail to reject the null hypothesis of equal variances. The assumption of homoscedasticity across the three tiers is satisfied.<br/>
    3. <b>Normality:</b> Group sample sizes (n1=141, n2=101, n3=58) are sufficiently large that the Central Limit Theorem ensures sampling distributions of the means approximate normality.
    """))

    a_tbl_data = [
        ("Source of Variation", "Degrees of Freedom (df)", "Test Statistic", "p-value", "Decision (α=0.05)"),
        ("Between Groups (Attendance)", "k - 1 = 2", f"F = {float(anova_s['F_statistic']):.4f}", f"p = {float(anova_s['p_value']):.4f}", anova_s['decision']),
        ("Within Groups (Error)", "N - k = 297", "—", "—", "—")
    ]
    t_atbl = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(a_tbl_data)],
        colWidths=[150, 110, 80, 75, 85]
    )
    t_atbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_atbl)
    story.append(Spacer(1, 8))

    story.append(h2("ANOVA Synthesis & Post-Hoc Analysis"))
    story.append(p(f"""
    <b>Result:</b> The F-test statistic is F = {float(anova_s['F_statistic']):.4f} with p = {float(anova_s['p_value']):.4f}. Since p > 0.05, we <b>fail to reject the null hypothesis</b>.<br/><br/>
    <b>Post-Hoc Determination:</b> Because the omnibus ANOVA test was non-significant at alpha = 0.05, post-hoc pairwise tests (such as Tukey's HSD) are not warranted. The observed variations (Low = 19.91, Moderate = 21.16, High = 18.04) do not constitute statistically significant differences.
    """))
    story.append(PageBreak())

    # ============================================================
    # 15. CORRELATION ANALYSIS
    # ============================================================
    story.append(h1("15. Correlation Analysis & Matrix"))
    story.append(hr())
    story.append(p("""
    Pearson's product-moment correlation coefficient ($r$) evaluates the strength and direction of linear association between continuous variables:
    $$r = \\frac{\\sum (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum (x_i - \\bar{x})^2 \\sum (y_i - \\bar{y})^2}}$$
    The coefficients range from $-1.0$ (perfect inverse linear relation) to $+1.0$ (perfect direct linear relation), with $0.0$ denoting complete absence of linear association.
    """))

    corr_p_path = os.path.join(RESULTS_DIR, "pearson_correlation_attendance.csv")
    corr_p_df = pd.read_csv(corr_p_path)
    
    c_tbl_data = [["Target Metric", "Pearson r", "p-value", "Significance (α=0.05)", "Qualitative Strength"]]
    for _, r in corr_p_df.iterrows():
        c_tbl_data.append([
            str(r["Variable"]), f"{r['r']:+.4f}", f"{r['p_value']:.4f}",
            "Not Significant" if r["p_value"] > 0.05 else "Significant", str(r["strength"])
        ])
    t_c = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(c_tbl_data)],
        colWidths=[130, 80, 80, 110, 100]
    )
    t_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_c)
    story.append(Spacer(1, 10))

    img_heat = os.path.join(GRAPHS_DIR, "heatmap_correlation.png")
    if os.path.exists(img_heat):
        story.append(Table([
            [Image(img_heat, width=320, height=220)],
            [Paragraph("<b>Figure 7:</b> Pearson Correlation Heatmap across All Variables", tbl_cell_style)]
        ], colWidths=[500], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(Spacer(1, 8))

    story.append(p("""
    <b>Core Finding:</b> The correlation between overall attendance and midterm marks is $r = +0.0015$ ($p = 0.9790$). This indicates an almost complete absence of linear dependency. Furthermore, overall attendance exhibits negligible correlation with average quiz scores ($r = -0.0357$), previous GPA ($r = -0.0380$), and final exam marks ($r = +0.0343$).
    """))
    story.append(PageBreak())

    # ============================================================
    # 16 & 17. REGRESSION MODELS (SLR & MLR)
    # ============================================================
    story.append(h1("16. Simple Linear Regression (SLR)"))
    story.append(hr())
    story.append(p("""
    Simple Linear Regression models the linear dependency of a scalar dependent variable ($Y$) on a single explanatory variable ($X$):
    $$Y = \\beta_0 + \\beta_1 X + \\varepsilon, \\quad \\widehat{Y} = b_0 + b_1 X$$
    • <b>Predictor ($X$):</b> Overall Attendance Percentage (<code>overall_attendance_pct</code>)<br/>
    • <b>Target ($Y$):</b> Midterm Marks (<code>midterm_marks</code>)<br/>
    • <b>Data Partition:</b> 80% Training ($n=240$), 20% Test ($n=60$) with fixed <code>random_state=42</code>.
    """))

    slr_eq_text = """
    <b>Fitted SLR Equation:</b><br/>
    $$\\widehat{\\text{Midterm}} = 20.7955 - 0.0157 \\times (\\text{Overall Attendance \\%})$$<br/>
    • <b>Intercept ($b_0 = 20.7955$):</b> The theoretical expected midterm score for a hypothetical student with 0% attendance.<br/>
    • <b>Slope ($b_1 = -0.0157$):</b> For each additional 1% attendance, the predicted midterm mark decreases by 0.0157 marks.
    """
    story.append(callout_box(slr_eq_text))
    story.append(Spacer(1, 8))

    story.append(h1("17. Multiple Linear Regression (MLR)"))
    story.append(hr())
    story.append(p("""
    Multiple Linear Regression incorporates multiple continuous and demographic predictors to account for confounding variance:
    $$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\dots + \\beta_k X_k + \\varepsilon$$
    • <b>Predictors:</b> Overall Attendance %, Average Quiz Marks, Previous GPA, and Student Age.<br/>
    • <b>Excluded Variables:</b> Student ID/Name (identifiers) and Final Marks (to prevent target leakage).<br/>
    • <b>Training:</b> Estimated via Ordinary Least Squares (OLS) strictly on the $n=240$ training split.
    """))

    mlr_eq_text = """
    <b>Fitted MLR Equation:</b><br/>
    $$\\widehat{\\text{Midterm}} = 24.8117 - 0.0189(X_{\\text{Att\\%}}) - 0.6408(X_{\\text{Quiz}}) + 0.0595(X_{\\text{GPA}}) - 0.0028(X_{\\text{Age}})$$<br/>
    • <b>Partial Slopes:</b> Holding all other attributes constant, each 1-mark increase in average quiz scores is associated with a 0.6408-mark reduction in predicted midterm performance. Previous GPA has a minimal positive partial slope (+0.0595).
    """
    story.append(callout_box(mlr_eq_text))
    story.append(PageBreak())

    # ============================================================
    # 18. MODEL EVALUATION & NEGATIVE R²
    # ============================================================
    story.append(h1("18. Model Evaluation & Benchmarking"))
    story.append(hr())
    story.append(p("""
    Models were evaluated strictly on the held-out test partition ($n=60$). Four primary error metrics were computed:
    <br/>
    $$\\text{MAE} = \\frac{1}{n}\\sum |y_i - \\hat{y}_i|, \\quad \\text{MSE} = \\frac{1}{n}\\sum (y_i - \\hat{y}_i)^2, \\quad \\text{RMSE} = \\sqrt{\\text{MSE}}, \\quad R^2 = 1 - \\frac{\\sum (y_i - \\hat{y}_i)^2}{\\sum (y_i - \\bar{y})^2}$$
    """))

    eval_path = os.path.join(RESULTS_DIR, "model_evaluation_comparison.csv")
    eval_df = pd.read_csv(eval_path)
    
    e_tbl_data = [["Metric", "Simple Linear Regression", "Multiple Linear Regression", "Superior Performance"]]
    for _, r in eval_df.iterrows():
        m_name = r["Metric"]
        s_val = f"{float(r['Simple LR']):.4f}"
        m_val = f"{float(r['Multiple LR']):.4f}"
        win = "Simple LR" if abs(float(r['Simple LR'])) < abs(float(r['Multiple LR'])) else "Multiple LR"
        if m_name == "R²":
            win = "Simple LR (Less negative)"
        e_tbl_data.append([m_name, s_val, m_val, win])

    t_eval = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(e_tbl_data)],
        colWidths=[110, 130, 130, 130]
    )
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_eval)
    story.append(Spacer(1, 10))

    story.append(h2("Statistical Explanation of Negative Test R²"))
    neg_r_text = """
    <b>Critical Mathematical Concept: Why is Test $R^2$ Negative?</b><br/>
    In introductory statistics, $R^2$ is often introduced as the square of the correlation coefficient ($r^2$), which must be non-negative. However, on out-of-sample test data, $R^2$ is defined by:
    $$R^2 = 1 - \\frac{SS_{\\text{res}}}{SS_{\\text{tot}}} = 1 - \\frac{\\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2}{\\sum_{i=1}^{n} (y_i - \\bar{y}_{\\text{train}})^2}$$
    A negative $R^2$ indicates that $SS_{\\text{res}} > SS_{\\text{tot}}$: the sum of squared errors from the regression model is larger than the sum of squared errors from simply predicting the historical training mean ($\\bar{y}_{\\text{train}}$) for every test observation. Thus, both models perform worse than a naive horizontal mean baseline.
    """
    story.append(callout_box(neg_r_text))
    story.append(Spacer(1, 10))

    img_slr = os.path.join(GRAPHS_DIR, "slr_actual_vs_predicted.png")
    img_mlr = os.path.join(GRAPHS_DIR, "mlr_actual_vs_predicted.png")
    if os.path.exists(img_slr) and os.path.exists(img_mlr):
        img_tbl_reg = Table([
            [Image(img_slr, width=240, height=155), Image(img_mlr, width=240, height=155)],
            [Paragraph("<b>Figure 8:</b> SLR Actual vs. Predicted Midterm Marks", tbl_cell_style),
             Paragraph("<b>Figure 9:</b> MLR Actual vs. Predicted Midterm Marks", tbl_cell_style)]
        ], colWidths=[250, 250], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')])
        story.append(img_tbl_reg)

    story.append(PageBreak())

    # ============================================================
    # 19. PREDICTION RESULTS
    # ============================================================
    story.append(h1("19. Out-of-Sample Prediction Results"))
    story.append(hr())
    story.append(p("""
    To verify predictive generalization, the trained models generated point forecasts for all 60 unseen test observations. Below are the first 10 test observations, comparing actual scores against model predictions and residuals ($e_i = y_i - \\hat{y}_i$):
    """))

    pred_path = os.path.join(RESULTS_DIR, "predictions_test_set.csv")
    pred_df = pd.read_csv(pred_path).head(10)

    p_tbl_data = [["Test Index", "Actual Midterm", "SLR Forecast", "SLR Error (Residual)", "MLR Forecast", "MLR Error (Residual)"]]
    for _, r in pred_df.iterrows():
        p_tbl_data.append([
            f"Student {int(r['Test_Index'])}", f"{r['Actual_Midterm']:.2f}",
            f"{r['SLR_Predicted']:.2f}", f"{r['SLR_Error']:+.2f}",
            f"{r['MLR_Predicted']:.2f}", f"{r['MLR_Error']:+.2f}"
        ])
    t_pred = Table(
        [[Paragraph(f"<b>{c}</b>" if idx==0 else c, tbl_cell_style) for c in row] for idx, row in enumerate(p_tbl_data)],
        colWidths=[80, 80, 85, 85, 85, 85]
    )
    t_pred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_CLR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_pred)
    story.append(Spacer(1, 10))

    story.append(p("""
    <b>Residual Behavior Analysis:</b><br/>
    The residuals illustrate the substantial dispersion of individual errors. For Student 6, where the actual midterm was 9.0 marks, SLR predicted 20.36 (error = -11.36) and MLR predicted 21.92 (error = -12.92). Both regression models compress their predictions into a narrow band near the global mean (19.0 – 21.0 marks), failing to capture the true variance in student scores.
    """))

    # ============================================================
    # 20. COMPREHENSIVE DISCUSSION
    # ============================================================
    story.append(h1("20. Comprehensive Discussion"))
    story.append(hr())
    story.append(p("""
    The empirical outcomes of this study present three notable analytical findings that carry important pedagogical lessons:
    <br/><br/>
    1. <b>Absence of Expected Educational Associations:</b> Across all statistical tests—Welch's t-test ($p=0.1838$), One-Way ANOVA ($p=0.0715$), and Pearson correlation ($r=+0.0015$)—attendance metrics showed no statistically significant relationship with examination outcomes. In real-world educational research, class attendance typically exhibits a moderate positive correlation ($r \\approx 0.35 - 0.65$) with performance. Its absence here points directly to the data generation process.<br/><br/>
    2. <b>Multivariate Overfitting on Uncorrelated Features:</b> When transitioning from Simple to Multiple Linear Regression, all evaluation metrics deteriorated: MAE increased from 6.63 to 6.70, RMSE increased from 8.02 to 8.19, and $R^2$ worsened from -0.0198 to -0.0637. When candidate predictors share no underlying correlation with the target, adding features increases parameter estimation variance without adding explanatory signal.<br/><br/>
    3. <b>Scientific Rigor and Non-Fabrication:</b> Authentic statistical practice requires presenting the data as it exists. Fabricating artificial significance or altering predictors to force an idealized regression fit would violate academic ethics. Documenting why the models fail provides a more valuable statistical exercise than reporting manufactured successes.
    """))
    story.append(PageBreak())

    # ============================================================
    # 21, 22, 23. LIMITATIONS, CONCLUSION, REFERENCES
    # ============================================================
    story.append(h1("21. Limitations of the Study"))
    story.append(hr())
    story.append(p("""
    • <b>Synthetic Data Architecture:</b> The dataset exhibits characteristics of independently simulated variables with no underlying structural equations connecting attendance and exam performance.<br/>
    • <b>Undocumented Sampling:</b> Without sampling documentation or weights, generalizability is impossible.<br/>
    • <b>Linearity Constraints:</b> Linear regression assumes linear relationships and homoscedastic Gaussian errors, which do not hold well here.<br/>
    • <b>Omission of Key Confounders:</b> Real-world academic performance is influenced by study hours, socio-economic factors, health, and subject interest, none of which are captured here.
    """))

    story.append(h1("22. Conclusion & Future Work"))
    story.append(hr())
    story.append(p("""
    This project fulfilled all requirements of the Probability and Statistics curriculum, executing a complete workflow from raw data ingestion to inferential hypothesis testing and predictive evaluation.
    <br/><br/>
    <b>Summary of Results:</b><br/>
    • Attendance and internal assessments show no statistically significant linear relationship with midterm exam scores ($r = +0.0015, p = 0.9790$).<br/>
    • Hypothesis testing confirmed that differences between attendance tiers were not statistically significant at $\\alpha = 0.05$.<br/>
    • The 95% Confidence Interval for mean midterm marks was determined as $[19.03, 20.91]$ marks.<br/>
    • Linear regression models generated negative out-of-sample $R^2$ values, performing worse than a naive mean baseline.<br/><br/>
    <b>Future Scope with Real Data:</b> Future work with verified university datasets should incorporate non-linear modeling, interaction terms, and clustering to capture diverse student engagement profiles.
    """))

    story.append(h1("23. Academic References"))
    story.append(hr())
    refs = [
        "1. Ahmad, M. K. (2025). <i>Student Performance and Clustering Dataset</i>. Kaggle Data Repository. DOI: 10.34740/kaggle/dsv/13489035.",
        "2. Walpole, R. E., Myers, R. H., Myers, S. L., & Ye, K. (2012). <i>Probability & Statistics for Engineers & Scientists</i> (9th ed.). Boston: Prentice Hall.",
        "3. Montgomery, D. C., & Runger, G. C. (2014). <i>Applied Statistics and Probability for Engineers</i> (6th ed.). Hoboken, NJ: John Wiley & Sons.",
        "4. Devore, J. L. (2015). <i>Probability and Statistics for Engineering and the Sciences</i> (9th ed.). Boston, MA: Cengage Learning.",
        "5. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825-2830.",
        "6. Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. <i>Nature Methods</i>, 17(3), 261-272."
    ]
    for ref in refs:
        story.append(Paragraph(ref, ParagraphStyle('Ref', parent=body_style, fontSize=8.5, leading=12, spaceAfter=4)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build completed:", REPORT_PDF)

if __name__ == "__main__":
    build_pdf()
