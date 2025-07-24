# main code

import pre_processing_pipeline as pre_p         # importing preprocessing part
import llm_code as ocr                          # importing the ocr part
import post_processing as post_p                # importing postprocessing part

def main(input_image,file_name,n):

    
    output_image = pre_p.run_parallel_image_processing(input_image)
    output_text = ocr.ocr_reading(output_image,n,file_name)

    df = post_p.excel_creation(output_text,n)

    return df