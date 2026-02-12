import streamlit as st
from PIL import Image
import pandas as pd
from transformers import pipeline

# ---- التوكن الخاص بك ----
HF_TOKEN = "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"

# ---- اختيار اللغة ----
language = st.sidebar.selectbox("اختر اللغة / Select Language", ["English", "العربية"])

texts = {
    "English": {
        "title": "Veterinary AI Diagnostic Tool 🐄🐑🐖🐔🐎🐶🐱",
        "enter_symptoms": "Enter symptoms separated by commas (e.g., fever, lethargy, anemia):",
        "upload_image": "Upload an image of the affected animal or sample",
        "diagnose_btn": "Diagnose",
        "no_input": "Please enter symptoms or upload an image.",
        "diagnosis": "Diagnosis & Treatment:",
        "processing": "Analyzing image and symptoms..."
    },
    "العربية": {
        "title": "أداة التشخيص البيطرية بالذكاء الاصطناعي 🐄🐑🐖🐔🐎🐶🐱",
        "enter_symptoms": "أدخل الأعراض مفصولة بفواصل (مثال: حمى, كسل, فقر الدم):",
        "upload_image": "ارفع صورة للحيوان المصاب أو العينة",
        "diagnose_btn": "تشخيص",
        "no_input": "الرجاء إدخال الأعراض أو رفع صورة.",
        "diagnosis": "التشخيص والعلاج:",
        "processing": "جاري تحليل الصورة والأعراض..."
    }
}

t = texts[language]
st.title(t["title"])

# ---- إدخال المستخدم ----
user_symptoms = st.text_input(t["enter_symptoms"])
uploaded_file = st.file_uploader(t["upload_image"], type=["jpg","jpeg","png"])

# ---- قاعدة بيانات أولية موسعة لكل الحيوانات ----
disease_db = {
    "Brucellosis": ["fever","abortion","swelling","lethargy"],
    "Theileriosis": ["fever","anemia","icterus","lymph node enlargement"],
    "Babesiosis": ["fever","hemoglobinuria","anemia","lethargy"],
    "Avian Influenza": ["coughing","sneezing","drop in egg production","diarrhea"],
    "Foot and Mouth Disease": ["blisters","lameness","fever","salivation"],
    "Canine Distemper": ["cough","fever","vomiting","diarrhea","lethargy"],
    "Feline Panleukopenia": ["vomiting","diarrhea","fever","lethargy"],
    # يمكنك إضافة المزيد من الأمراض حسب الحاجة
}

arabic_names = {
    "Brucellosis":"البروسيلا",
    "Theileriosis":"الثايليريوسيس",
    "Babesiosis":"البابيسيوسس",
    "Avian Influenza":"إنفلونزا الطيور",
    "Foot and Mouth Disease":"مرض الحمى القلاعية",
    "Canine Distemper":"داء الكلاب المعدي",
    "Feline Panleukopenia":"داء القطط النزلي"
}

arabic_treatments = {
    "Brucellosis":"استشر البروتوكول البيطري لعلاج البروسيلا",
    "Theileriosis":"استشر البروتوكول البيطري لعلاج الثايليريوسيس",
    "Babesiosis":"استشر البروتوكول البيطري لعلاج البابيسيوسس",
    "Avian Influenza":"استشر البروتوكول البيطري لعلاج إنفلونزا الطيور",
    "Foot and Mouth Disease":"استشر البروتوكول البيطري لعلاج الحمى القلاعية",
    "Canine Distemper":"استشر البروتوكول البيطري لعلاج داء الكلاب المعدي",
    "Feline Panleukopenia":"استشر البروتوكول البيطري لعلاج داء القطط النزلي"
}

# ---- تحميل نموذج Hugging Face لتحليل الصور ----
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="your-huggingface-vet-model", use_auth_token=HF_TOKEN)

model = load_model()

# ---- تحليل التشخيص ----
if st.button(t["diagnose_btn"]):
    if not user_symptoms and not uploaded_file:
        st.warning(t["no_input"])
    else:
        st.info(t["processing"])
        results = []

        # ---- تحليل الأعراض النصية ----
        if user_symptoms:
            symptoms_list = [s.strip().lower() for s in user_symptoms.split(",")]
            for disease, symptoms in disease_db.items():
                matched = len(set(symptoms_list) & set([s.lower() for s in symptoms]))
                score = matched / len(symptoms)
                if score > 0:
                    results.append({
                        "Disease": arabic_names[disease] if language=="العربية" else disease,
                        "Confidence": round(score*100,2),
                        "Treatment": arabic_treatments[disease] if language=="العربية" else "Refer to veterinary treatment protocols"
                    })

        # ---- تحليل الصورة بواسطة AI ----
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            preds = model(image)
            for pred in preds:
                disease_name = pred['label']
                confidence = pred['score']*100
                results.append({
                    "Disease": arabic_names.get(disease_name, disease_name) if language=="العربية" else disease_name,
                    "Confidence": round(confidence,2),
                    "Treatment": arabic_treatments.get(disease_name,"Refer to veterinary treatment protocols") if language=="العربية" else "Refer to veterinary treatment protocols"
                })

        # ---- عرض النتائج ----
        if results:
            st.subheader(t["diagnosis"])
            df = pd.DataFrame(results).sort_values(by="Confidence", ascending=False)
            st.table(df)
        else:
            st.info("No clear diagnosis. Please consult a veterinarian.")
