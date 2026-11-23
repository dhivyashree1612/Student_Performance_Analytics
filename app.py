import pandas as pd

# Load the dataset
df = pd.read_csv("data/students.csv")

# Calculate total marks
subjects = ["Maths", "Science", "English", "Computer"]

df["Total"] = df[subjects].sum(axis=1)

# Calculate average
df["Average"] = df[subjects].mean(axis=1)

# Assign grades
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

# Display data
print(df)

# Class average
print("\nClass Average:", df["Average"].mean())

# Topper
topper = df.loc[df["Total"].idxmax()]
print("\nTopper:", topper["Name"])

# Subject averages
print("\nSubject Averages:")
print(df[subjects].mean())