# main code

import os
import pre_processing_pipeline as pre_p         # importing preprocessing part
import ocr_code as ocr                          # importing the ocr part
import post_processing as post_p                # importing postprocessing part

def main():
    input_path = r"C:\Users\shivn\Downloads\pipeline\059.jpg"       # change the input path

    n = int(input("Enter dates: "))                                 # Input for number of date columns

    base, ext = os.path.splitext(input_path)

    output_path = f"{base}_proc{ext}"                               # Output path for preprocessed images
    
    pre_p.run_parallel_image_processing(input_path, output_path)    # Calling pre_processing
    ocr.ocr_reading(output_path,n)                                  # Calling llm model
                                         
    base, ext = os.path.splitext(output_path) 
    new_output_path = f"{base}.txt"

    post_p.excel_creation(new_output_path,n)                        # Calling post_processing

if __name__ == "__main__":
    main()
