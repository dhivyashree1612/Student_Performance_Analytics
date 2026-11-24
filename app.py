import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/students.csv")

df = load_data()

subjects = ["Maths", "Science", "English", "Computer"]

# ---------------- DATA ANALYSIS ----------------
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    elif avg >= 50:
        return "E"
    else:
        return "F"

df["Grade"] = df["Average"].apply(calculate_grade)
df["Result"] = df["Average"].apply(
    lambda x: "Pass" if x >= 50 else "Fail"
)

# ---------------- TITLE ----------------
st.title("🎓 Student Performance Analytics System")
st.markdown("### Academic performance analysis and student insights")

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Dashboard Filters")

departments = ["All"] + sorted(df["Department"].unique().tolist())

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)

search_name = st.sidebar.text_input("Search Student Name")

# Filter department
if selected_department == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Department"] == selected_department].copy()

# Filter name
if search_name:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search_name, case=False, na=False)
    ]

# ---------------- KPI METRICS ----------------
if not filtered_df.empty:

    total_students = len(filtered_df)
    class_average = filtered_df["Average"].mean()
    pass_percentage = (
        (filtered_df["Result"] == "Pass").sum()
        / total_students
    ) * 100

    topper = filtered_df.loc[
        filtered_df["Average"].idxmax()
    ]["Name"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", total_students)
    col2.metric("Class Average", f"{class_average:.2f}%")
    col3.metric("Pass Percentage", f"{pass_percentage:.2f}%")
    col4.metric("Top Performer", topper)

    st.divider()

    # ---------------- SUBJECT ANALYSIS ----------------
    st.subheader("📊 Subject Performance Analysis")

    subject_avg = filtered_df[subjects].mean()

    fig1, ax1 = plt.subplots()
    subject_avg.plot(kind="bar", ax=ax1)

    ax1.set_title("Average Marks by Subject")
    ax1.set_ylabel("Average Marks")
    ax1.set_xlabel("Subjects")
    ax1.set_ylim(0, 100)

    plt.xticks(rotation=0)
    st.pyplot(fig1)
    plt.close(fig1)

    # ---------------- GRADE DISTRIBUTION ----------------
    st.subheader("📈 Grade Distribution")

    grade_counts = filtered_df["Grade"].value_counts().reindex(
        ["A", "B", "C", "D", "E", "F"],
        fill_value=0
    )

    fig2, ax2 = plt.subplots()
    grade_counts.plot(kind="bar", ax=ax2)

    ax2.set_title("Number of Students in Each Grade")
    ax2.set_xlabel("Grade")
    ax2.set_ylabel("Number of Students")

    st.pyplot(fig2)
    plt.close(fig2)

    st.divider()

    # ---------------- STUDENT TABLE ----------------
    st.subheader("📋 Student Performance Details")

    display_columns = [
        "Student_ID", "Name", "Department",
        "Maths", "Science", "English", "Computer",
        "Total", "Average", "Grade", "Result", "Attendance"
    ]

    st.dataframe(
        filtered_df[display_columns].sort_values(
            by="Average", ascending=False
        ),
        use_container_width=True
    )

    # ---------------- STUDENTS NEEDING SUPPORT ----------------
    st.subheader("⚠️ Students Needing Academic Support")

    weak_students = filtered_df[
        (filtered_df["Average"] < 50)
        | (filtered_df["Attendance"] < 75)
    ]

    if not weak_students.empty:
        st.dataframe(
            weak_students[[
                "Student_ID", "Name", "Department",
                "Average", "Attendance", "Result"
            ]],
            use_container_width=True
        )
    else:
        st.success("No students requiring support in the selected data.")

    # ---------------- DEPARTMENT ANALYSIS ----------------
    st.subheader("🏫 Department Performance")

    department_avg = df.groupby("Department")["Average"].mean()

    fig3, ax3 = plt.subplots()
    department_avg.plot(kind="bar", ax=ax3)

    ax3.set_title("Average Performance by Department")
    ax3.set_xlabel("Department")
    ax3.set_ylabel("Average Marks")
    ax3.set_ylim(0, 100)

    plt.xticks(rotation=0)
    st.pyplot(fig3)
    plt.close(fig3)

    # ---------------- DOWNLOAD DATA ----------------
    st.subheader("⬇️ Download Analyzed Data")

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Student Analytics CSV",
        data=csv_data,
        file_name="student_analytics.csv",
        mime="text/csv"
    )

else:
    st.warning("No students found for the selected filters.")

# ---------------- FOOTER ----------------
st.divider()
st.caption("Student Performance Analytics System | Python | Pandas | Streamlit")