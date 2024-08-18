import os
from langchain_community.document_loaders import PyPDFLoader

def pdf_to_txt(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_filename)
            
            try:
                # Load PDF
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()
                
                # Extract text from all pages
                full_text = '\n'.join([page.page_content for page in pages])
                
                # Write text to file
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(full_text)
                
                print(f"Converted {filename} to {txt_filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

