import pandas as pd
import csv
from tkinter import Tk, filedialog

def process_csv(file_path):
    # Read the CSV file with a semicolon delimiter
    df = pd.read_csv(file_path, delimiter=';', decimal=',')

    # Create an empty dictionary to store counts for each unique combination of length, width, height, and material
    result_counts = {}

    # Iterate over each row in the original DataFrame
    for index, row in df.iterrows():
        # Split the 'Length (mm)' values by comma
        length_values = str(row['Length (mm)']).split(',')
        
        # Split the 'Width (mm)' values by comma
        width_values = str(row['Width (mm)']).split(',')

        # Get the 'Height (mm)' value
        height = str(row['Height (mm)'])

        # Get the 'Material' value
        material = str(row['Material'])

        # Iterate over the split values (using zip to iterate over both lists simultaneously)
        for length, width in zip(length_values, width_values):
            # Strip any leading or trailing spaces
            length = length.strip()
            width = width.strip()

            # Check if the values are numeric before trying to convert
            if length and width and width.replace('.', '', 1).isdigit():
                length = "{:,.3f}".format(float(length)).replace(',', 'temp').replace('.', ',').replace('temp', '.')
                width = "{:,.3f}".format(float(width)).replace(',', 'temp').replace('.', ',').replace('temp', '.')
                key = (material, length, width, height)
                result_counts[key] = result_counts.get(key, 0) + 1

    # Save the result to a new CSV file with right-aligned columns and specified column widths
    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        
        # Write the header with specified column widths
        csv_writer.writerow(['Material'.rjust(15), 'Length (mm)'.rjust(15), 'Width (mm)'.rjust(15), 'Height (mm)'.rjust(15), 'Count'.rjust(15)])
        
        # Write the rows with right-aligned values and commas for thousands
        for (material, length, width, height), count in result_counts.items():
            formatted_material = material.rjust(15)
            formatted_length = length.rjust(15)
            formatted_width = width.rjust(15)
            formatted_height = height.rjust(15)
            formatted_count = "{:,}".format(count).rjust(15)
            csv_writer.writerow([formatted_material, formatted_length, formatted_width, formatted_height, formatted_count])

def select_csv():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
    
    if file_path:
        process_csv(file_path)

# Call the select_csv function to choose and process a CSV file
select_csv()
