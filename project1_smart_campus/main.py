import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans


class Student:
    def __init__(self, student_id, name, department):
        self.student_id = student_id
        self.name = name
        self.department = department


class Facility:
    def __init__(self, facility_name, capacity, location, facility_type):
        self.facility_name = facility_name
        self.capacity = capacity
        self.location = location
        self.facility_type = facility_type

    def show_info(self):
        print(self.facility_name, "-", self.location, "- capacity:", self.capacity)


class UsageRecord:
    def __init__(self, facility_name, day, time, students, previous_usage, capacity):
        self.facility_name = facility_name
        self.day = day
        self.time = time
        self.students = students
        self.previous_usage = previous_usage
        self.capacity = capacity

    def occupancy_percentage(self):
        return (self.students / self.capacity) * 100


class DemandPredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.best_model_name = None
        self.best_model = None
        self.results = {}

    def prepare_data(self, df):
        data = df.copy()
        cat_cols = ["Facility", "Day", "Time", "Department"]
        for col in cat_cols:
            le = LabelEncoder()
            data[col + "_enc"] = le.fit_transform(data[col])
            self.encoders[col] = le

        target_le = LabelEncoder()
        data["Demand_enc"] = target_le.fit_transform(data["Demand_Level"])
        self.encoders["Demand_Level"] = target_le

        feature_cols = ["Facility_enc", "Day_enc", "Time_enc", "Department_enc",
                         "Students", "Previous_Usage", "Occupancy_Percentage"]
        X = data[feature_cols]
        y = data["Demand_enc"]
        return X, y

    def train_all(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7)

        knn = KNeighborsClassifier(n_neighbors=5)
        nb = GaussianNB()
        dt = DecisionTreeClassifier(max_depth=6, random_state=7)
        rf = RandomForestClassifier(n_estimators=100, random_state=7)

        model_list = {"KNN": knn, "Naive Bayes": nb, "Decision Tree": dt, "Random Forest": rf}

        for name, model in model_list.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            acc = accuracy_score(y_test, pred)
            self.results[name] = round(acc * 100, 2)
            self.models[name] = model

        self.best_model_name = max(self.results, key=self.results.get)
        self.best_model = self.models[self.best_model_name]
        return self.results

    def predict_demand(self, facility, day, time, department, students, previous_usage, capacity):
        occ = (students / capacity) * 100
        f_enc = self.encoders["Facility"].transform([facility])[0]
        d_enc = self.encoders["Day"].transform([day])[0]
        t_enc = self.encoders["Time"].transform([time])[0]
        dep_enc = self.encoders["Department"].transform([department])[0]

        row = [[f_enc, d_enc, t_enc, dep_enc, students, previous_usage, occ]]
        pred_num = self.best_model.predict(row)[0]
        pred_label = self.encoders["Demand_Level"].inverse_transform([pred_num])[0]
        return pred_label


class ReportGenerator:
    def __init__(self, df, model_results, best_model_name):
        self.df = df
        self.model_results = model_results
        self.best_model_name = best_model_name

    def print_summary(self):
        print("\n===== SMART CAMPUS REPORT =====")
        print("Total records analyzed:", len(self.df))
        print("\nModel Accuracy Comparison:")
        for name, acc in self.model_results.items():
            print(name, ":", acc, "%")
        print("\nBest Performing Model:", self.best_model_name)
        print("\nDemand level distribution:")
        print(self.df["Demand_Level"].value_counts())

    def recommendation(self, demand_level):
        if demand_level == "High":
            return "Additional resources may be required. Consider extending hours or adding capacity."
        elif demand_level == "Medium":
            return "Monitor usage closely, resources are sufficient for now."
        else:
            return "Facility is under-utilized, resources can be reallocated elsewhere."


def clean_and_engineer(df):
    df = df.drop_duplicates()
    df = df.dropna()

    df["Occupancy_Percentage"] = (df["Students"] / df["Capacity"]) * 100
    df["Usage_Rate"] = df["Students"] - df["Previous_Usage"]
    df["Peak_Hour"] = df["Time"].apply(lambda t: 1 if t in ["10 AM", "1 PM", "2 PM"] else 0)
    df["Previous_Day_Usage"] = df["Previous_Usage"]

    weekly_avg = df.groupby("Facility")["Students"].mean()
    df["Average_Weekly_Usage"] = df["Facility"].map(weekly_avg)

    return df


def numpy_stats(df):
    students_array = df["Students"].to_numpy()
    print("\n===== NUMPY STATISTICS (Students count) =====")
    print("Mean:", np.mean(students_array))
    print("Max:", np.max(students_array))
    print("Min:", np.min(students_array))
    print("Std Dev:", round(np.std(students_array), 2))

    normalized = (students_array - np.min(students_array)) / (np.max(students_array) - np.min(students_array))
    df["Students_Normalized"] = normalized
    return df


def make_visualizations(df):
    plt.figure(figsize=(8, 5))
    daily = df.groupby("Day")["Students"].sum().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    daily.plot(kind="bar", color="teal")
    plt.title("Daily Facility Usage")
    plt.ylabel("Total Students")
    plt.tight_layout()
    plt.savefig("daily_usage.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    weekly_trend = df.groupby("Day")["Students"].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    weekly_trend.plot(kind="line", marker="o", color="orange")
    plt.title("Weekly Usage Trend")
    plt.ylabel("Average Students")
    plt.tight_layout()
    plt.savefig("weekly_trend.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    peak = df.groupby("Peak_Hour")["Students"].mean()
    peak.plot(kind="bar", color=["gray", "crimson"])
    plt.title("Peak Hour Analysis")
    plt.xticks([0, 1], ["Non Peak", "Peak"], rotation=0)
    plt.tight_layout()
    plt.savefig("peak_hour_analysis.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    facility_comp = df.groupby("Facility")["Students"].mean().sort_values()
    facility_comp.plot(kind="barh", color="purple")
    plt.title("Facility Comparison (Avg Students)")
    plt.tight_layout()
    plt.savefig("facility_comparison.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    corr_data = df[["Students", "Previous_Usage", "Occupancy_Percentage", "Usage_Rate"]].corr()
    sns.heatmap(corr_data, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    sns.countplot(data=df, x="Demand_Level", hue="Demand_Level", order=["Low", "Medium", "High"], palette="Set2", legend=False)
    plt.title("Demand Distribution")
    plt.tight_layout()
    plt.savefig("demand_distribution.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    sns.scatterplot(data=df, x="Students", y="Occupancy_Percentage", hue="Demand_Level")
    plt.title("Usage vs Occupancy")
    plt.tight_layout()
    plt.savefig("usage_vs_occupancy.png")
    plt.close()

    plt.figure(figsize=(9, 5))
    dept_facility = df.groupby(["Department", "Facility"])["Students"].mean().unstack()
    sns.heatmap(dept_facility, cmap="YlGnBu")
    plt.title("Department vs Facility Usage")
    plt.tight_layout()
    plt.savefig("department_vs_facility.png")
    plt.close()

    print("\nAll visualizations saved as PNG files.")


def run_kmeans(df):
    features = df[["Students", "Previous_Usage", "Occupancy_Percentage"]]
    kmeans = KMeans(n_clusters=3, random_state=7, n_init=10)
    df["Usage_Cluster"] = kmeans.fit_predict(features)

    cluster_summary = df.groupby("Usage_Cluster")["Occupancy_Percentage"].mean().sort_values()
    cluster_order = list(cluster_summary.index)
    labels = ["Low-usage facilities", "Regular-usage facilities", "Peak-demand facilities"]

    cluster_names = {}
    for i, cluster_id in enumerate(cluster_order):
        cluster_names[cluster_id] = labels[i]

    df["Cluster_Name"] = df["Usage_Cluster"].map(cluster_names)

    print("\n===== K-MEANS USAGE SEGMENTATION =====")
    print(df.groupby("Cluster_Name")["Occupancy_Percentage"].mean())
    return df


def main():
    df = pd.read_csv("facility_usage.csv")
    df = clean_and_engineer(df)
    df = numpy_stats(df)
    make_visualizations(df)

    predictor = DemandPredictor()
    X, y = predictor.prepare_data(df)
    results = predictor.train_all(X, y)

    df = run_kmeans(df)

    report = ReportGenerator(df, results, predictor.best_model_name)
    report.print_summary()

    print("\n===== FINAL APPLICATION =====")
    facility = "Computer Lab"
    day = "Monday"
    time = "2 PM"
    department = "CSE"
    students = 210
    previous_usage = 190
    capacity = 200

    prediction = predictor.predict_demand(facility, day, time, department, students, previous_usage, capacity)
    print("Facility:", facility)
    print("Day:", day, "| Time:", time)
    print("Expected Students:", students)
    print("Previous Usage:", previous_usage)
    print("Predicted Demand:", prediction.upper())
    print("Recommendation:", report.recommendation(prediction))


if __name__ == "__main__":
    main()
