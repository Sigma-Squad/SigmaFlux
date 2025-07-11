import os
import re
import pandas as pd

def csv_creation(input_folder):
    output_folder = r"C:\Users\shivn\Downloads\pipeline\dataframes_output"
    os.makedirs(output_folder, exist_ok=True)

    # Updated regex to correctly match the formatted lines   # Change the pattern here

    row_pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*([A-Z]{2}\d{2}[A-Z]\d{3})\s*\|\s*(.*?)\s*\|"
        )


    # Step 1: Ask user for n
    n = int(input("Enter number of sign fields: "))


    sign_pattern = r'([^|]+)'       # each sign field: anything until next pipe

    # Join all parts
    pattern_parts = [
        r'(\d+)',                  # s.no
        r'([A-Z]{2}\d{2,})',       # roll
        r'([^|]+)'                 # name
    ]

    # Add n sign patterns
    pattern_parts.extend([sign_pattern] * n)

    # Combine with separator \s*\|\s*
    separator = r'\s*\|\s*'
    full_pattern = separator.join(pattern_parts)

    #print("Generated regex pattern:")
    #print(full_pattern)
       

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)

            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            extracted_data = []

            for line in lines:
                line = line.strip()

                # Skip separators or empty lines
                if line.startswith('---') or not line:
                    continue

                match = row_pattern.match(line)
                if match:

                # CHANGE HERE                              
                    try:
                        # Taking the first three are always sno, roll, name

                        sno, roll, name = match[0],match[1], match[2]

                        # The rest are the sign fields
                        sign_fields = [field.strip() for field in match[3:]]

                        # Append everything to extracted_data
                        extracted_data.append([
                            sno.strip(),
                            roll.strip(),
                            name.strip(),
                            *sign_fields   # unpack the list so each sign field is added as a separate column
                        ])
                    except Exception as e:
                        print("Error:", e)

            if extracted_data:
                column = ['S.No', 'Roll Number', 'Name'] + [f'Sign({i+1})' for i in range(n)]
                df = pd.DataFrame(extracted_data, columns= column)                                      #change here
                output_excel_path = os.path.join(output_folder, filename.replace(".txt", ".xlsx"))
                df.to_csv(output_excel_path, index=False)
                print(f"✅ Saved: {output_excel_path}")
            else:
                print(f"⚠️ No valid rows extracted from {filename}")

#csv_creation(r"C:\Users\shivn\Downloads\pipeline\ocr_output")
