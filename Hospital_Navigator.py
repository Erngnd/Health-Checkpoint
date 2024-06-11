import tkinter as tk
from tkinter import messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import time

# Downloads NLTK data files (only need to run this once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to preprocess the input complaint using NLP
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]  # Removes punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming and Lemmatization
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokens = [stemmer.stem(word) for word in tokens]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return tokens

# Function to map symptoms to hospital departments
def get_department(complaint):
    tokens = preprocess_text(complaint)
    
    rules = {
         "Anesthesiology": ["pain", "surgery", "anesthesia"],
        "Cardiology": ["chest", "pain", "heart", "palpitation", "shortness of breath", "fatigue", "dizziness", "swelling"],
        "Dermatology": ["rash", "itch", "skin", "acne", "eczema", "psoriasis", "mole", "lesion"],
        "Emergency Medicine": ["severe", "pain", "trauma", "sudden", "difficulty breathing", "chest pain"],
        "Endocrinology": ["fatigue", "weight", "urination", "thirst", "hair loss", "temperature"],
        "Family Medicine": ["general", "routine", "preventive", "non-specific"],
        "Gastroenterology": ["stomach", "pain", "digest", "abdominal", "bloat", "diarrhea", "constipation", "heartburn", "nausea", "vomiting", "stool"],
        "Geriatrics": ["memory", "mobility", "incontinence", "frailty"],
        "Hematology": ["bruising", "bleeding", "fatigue", "pallor", "infections", "lymph nodes"],
        "Infectious Disease": ["fever", "chills", "sweats", "cough", "weight loss", "rash", "travel"],
        "Internal Medicine": ["chronic", "hypertension", "diabetes", "fatigue"],
        "Medical Genetics": ["genetic", "birth defect", "developmental", "features"],
        "Nephrology": ["swelling", "urine", "blood pressure", "fatigue"],
        "Neurology": ["headache", "seizure", "numbness", "tingling", "weakness", "dizziness", "balance", "memory"],
        "Obstetrics and Gynecology (OB/GYN)": ["period", "pelvic", "pregnancy", "menopause"],
        "Oncology": ["weight loss", "fatigue", "lump", "skin", "pain"],
        "Ophthalmology": ["vision", "eye", "pain", "redness", "floaters", "double vision", "loss"],
        "Orthopedics": ["joint", "pain", "back", "fracture", "sprain", "arthritis", "muscle", "motion"],
        "Otolaryngology (ENT)": ["ear", "hearing", "sinus", "throat", "dizziness", "snoring", "voice"],
        "Pediatrics": ["child", "fever", "cough", "rash", "growth", "developmental"],
        "Physical Medicine and Rehabilitation (PM&R)": ["chronic pain", "mobility", "recovery", "injury", "muscle"],
        "Psychiatry": ["depression", "anxiety", "mood", "sleep", "hallucinations", "suicidal"],
        "Pulmonology": ["cough", "shortness of breath", "wheezing", "chest pain", "respiratory"],
        "Rheumatology": ["joint pain", "swelling", "stiffness", "fatigue", "autoimmune", "muscle"],
        "Surgery": ["surgical", "appendicitis", "hernia", "trauma", "cancer"],
        "Urology": ["urinary", "blood", "pelvic pain", "erectile", "incontinence"]

    }
    
    department_scores = {department: 0 for department in rules}
    
    start_time = time.time()  # Record start time
    
    for symptom in tokens:
        for department, keywords in rules.items():
            if symptom in keywords:
                department_scores[department] += 1
    
    end_time = time.time()  # Record end time
    execution_time = end_time - start_time  # Calculate execution time
    
    most_matched_department = max(department_scores, key=department_scores.get)
    
    return most_matched_department, execution_time

# Function to handle the submit button click event
def on_submit():
    complaint = complaint_entry.get()
    if not complaint:
        messagebox.showwarning("Input Error", "Please enter your symptoms or complaint.")
        return

    department, execution_time = get_department(complaint)
    result_label.config(text=f"Based on your symptoms, you should visit the {department} department.")
    performance_label.config(text=f"Execution Time: {execution_time:.6f} seconds")

# Initializes the main application window
root = tk.Tk()
root.title("Hospital Appointment System")

# Creates and place the complaint label and entry
complaint_label = tk.Label(root, text="Please describe your symptoms or complaint:")
complaint_label.pack(pady=10)
complaint_entry = tk.Entry(root, width=50)
complaint_entry.pack(pady=5)

# Creates and place the submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Creates and place the result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Creates and place the performance label
performance_label = tk.Label(root, text="")
performance_label.pack(pady=5)

# Starts the Tkinter event loop
root.mainloop()

