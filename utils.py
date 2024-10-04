import json

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_analysis_to_file(analysis, filename='text_analysis.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for key, value in analysis.items():
            file.write(f"{key}: {value}\n")

def save_analysis_to_json(analysis, filename='text_analysis.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(analysis, file, indent=4)
