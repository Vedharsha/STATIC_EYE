import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog
import tkinter as tk
import random

# Function to simulate vulnerability analysis (mock data)
def analyze_vulnerabilities():
    vulnerabilities = {
        "SQL Injection": random.randint(0, 10),
        "XSS": random.randint(0, 10),
        "Insecure Storage": random.randint(0, 10),
        "Weak Authentication": random.randint(0, 10),
        "Broken Access Control": random.randint(0, 10)
    }
    return vulnerabilities

# Function to create and display bar chart
def generate_bar_chart(vulnerabilities):
    plt.figure(figsize=(8, 6))
    
    # Data for bar chart
    categories = list(vulnerabilities.keys())
    counts = list(vulnerabilities.values())
    
    # Plotting bar chart
    plt.bar(categories, counts, color=['skyblue', 'green', 'red', 'orange', 'purple'])
    plt.title('Vulnerability Report')
    plt.xlabel('Vulnerability Type')
    plt.ylabel('Count')

    # Save the chart as an image file
    plt.tight_layout()
    chart_file = 'vulnerability_report.png'
    plt.savefig(chart_file)
    
    return chart_file

# Function to download the image report
def download_report(image_path):
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png")])
    if file_path:
        with open(image_path, 'rb') as img_file:
            with open(file_path, 'wb') as out_file:
                out_file.write(img_file.read())

# Function to display GUI
def show_gui(vulnerabilities):
    root = Tk()
    root.title("Vulnerability Report")
    root.geometry("300x200")

    label = Label(root, text="Vulnerability Report Generated!", font=('Helvetica', 12))
    label.pack(pady=20)

    # Button to download the report
    download_button = Button(root, text="Download Report", command=lambda: download_report(chart_file))
    download_button.pack(pady=10)

    # Display the window
    root.mainloop()

# Main function to run the vulnerability analysis and generate report
def main():
    # Step 1: Analyze vulnerabilities (dynamic count)
    vulnerabilities = analyze_vulnerabilities()

    # Step 2: Generate and save a bar chart from the analysis
    chart_file = generate_bar_chart(vulnerabilities)

    # Step 3: Display the GUI for user interaction
    show_gui(vulnerabilities)

# Run the main function
if __name__ == "__main__":
    main()
