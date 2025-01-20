import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Κατέβασμα απαραίτητων πόρων NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Φόρτωση δεδομένων JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Προεπεξεργασία κειμένου
def preprocess_text(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'[^\w\s-]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in tokens])

# Προεπεξεργασία δεδομένων dataset
def preprocess_dataset(dataset):
    for entry in dataset:
        for key in entry:
            if isinstance(entry[key], str):
                entry[key] = preprocess_text(entry[key])
    return dataset

# Αποθήκευση δεδομένων σε JSON
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Εκτέλεση
input_file = 'pah_wikp_combo.json'
output_file = 'pah_wikp_combo_pro.json'

raw_data = load_json(input_file)
processed_data = preprocess_dataset(raw_data)
save_json(processed_data, output_file)

print(f"DONE {output_file}")
