import os
import re
import pandas as pd

def excel_creation(input_file, n):

    base_pattern = r"^\|\s*(\d+)\s*\|\s*([A-Z0-9]+)\s*\|\s*(.*?)\s*\|"          # basic patternfor sno , roll and name
    date_pattern = r"\s*(Present|Absent)?\s*\|"                                 # Pattern for date
    full_pattern = base_pattern + (date_pattern * n)
    pattern = re.compile(full_pattern)                                          # Full pattern

    extracted_data = []

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # Skip separator lines or empty lines
        if line.startswith('---') or not line:
            continue

        match = pattern.match(line)
        if match:
            try:
                sno = match.group(1)
                roll = match.group(2)
                name = match.group(3)
                sign_fields = [field.strip() if field else '' for field in match.groups()[3:]]

                extracted_data.append([
                    sno.strip(),
                    roll.strip(),
                    name.strip(),
                    *sign_fields
                ])
            except Exception as e:
                print("Error:", e)

    base, ext = os.path.splitext(input_file)

    output_path = f"{base}.xlsx"

    if extracted_data:
        columns = ['S.No', 'Roll Number', 'Name'] + [f'Date {i+1}' for i in range(n)]   # Columns heading in dataframe
        df = pd.DataFrame(extracted_data, columns=columns)
        df.to_excel(output_path, index=False)
        print(f"✅ Saved: {output_path}")
    else:
        print("⚠️ No valid rows extracted from the file.")


