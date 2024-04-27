import pandas as pd
import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the HRV dataset
hrv_df = pd.read_csv("hrv_dataset.csv")

# Split the dataset into training and testing sets
X = hrv_df.drop(columns=["datasetId", "condition"])
y = hrv_df["condition"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier on the training set
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)


# Define a function to handle button click event
def predict_stress_level():
    # Get the new data point from the user input
    new_data_point_str = new_data_point_entry.get()
    new_data_point_list = new_data_point_str.split(",")
    new_data_point = []
    for val in new_data_point_list:
        try:
            new_data_point.append(float(val))
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            return

    # Create a DataFrame with the new data point as a single row
    new_data_point_df = pd.DataFrame([new_data_point], columns=X.columns)

    # Use the trained model to perform stress detection on the new data point
    predicted_stress_level = rfc.predict(new_data_point_df)[0]
    messagebox.showinfo("Result", f"Predicted stress level: {predicted_stress_level}")


# Create the GUI
root = tk.Tk()
root.geometry("300x300")
root.title("Stress Detector")

# Add a label for the user input
new_data_point_label = tk.Label(root, text="Enter new data point:")
new_data_point_label.pack()

# Add a text box for the user to input the new data point
new_data_point_entry = tk.Entry(root)
new_data_point_entry.pack()

# Add a button to trigger the stress level prediction
predict_button = tk.Button(root, text="Predict Stress Level", command=predict_stress_level)
predict_button.pack()

root.mainloop()
