import streamlit as st
from PIL import Image
import pandas as pd

# ---- إعدادات اللغة ----
language = st.sidebar.selectbox("اختر اللغة / Select Language", ["English", "العربية"])

# ---- قاعدة بيانات الأمراض ----
diseases = [
    {
        "name_en": "Brucellosis",
        "name_ar": "البروسيلا",
        "symptoms_en": ["fever", "abortion", "swelling", "lethargy"],
        "symptoms_ar": ["حمى", "إجهاض", "تورم", "كسل"],
        "treatment_en": "Antibiotics under veterinary supervision",
        "treatment_ar": "المضادات الحيوية تحت إشراف طبيب بيطري"
    },
    {
        "name_en": "Theileriosis",
        "name_ar": "ثايليريوسيس",
        "symptoms_en": ["fever", "anemia", "icterus", "lymph node enlargement"],
        "symptoms_ar": ["حمى", "فقر الدم", "اصفرار", "تضخم الغدد اللمفاوية"],
        "treatment_en": "Buparvaquone injection, supportive care",
        "treatment_ar": "حقن بوبارفاكون، دعم علاج مساعد"
    },
    {
        "name_en": "Babesiosis",
        "name_ar": "بابيسيوسس",
        "symptoms_en": ["fever", "hemoglobinuria", "anemia", "lethargy"],
        "symptoms_ar": ["حمى", "وجود الهيموغلوبين في البول", "فقر الدم", "كسل"],
        "treatment_en": "Imidocarb injection, fluid therapy",
        "treatment_ar": "حقن إيميدوكارب، معالجة بالسوائل"
    },
    # يمكن إضافة المزيد
]

# ---- النصوص حسب اللغة ----
texts = {
    "English": {
        "title": "Veterinary Microbial Disease Diagnostic Tool 🐄🧫",
        "enter_symptoms": "Enter the symptoms separated by commas (e.g., fever, lethargy, anemia):",
        "upload_image": "Upload an image of the affected animal or sample",
        "diagnose_btn": "Diagnose",
        "warning": "Please enter symptoms or upload an image to get diagnosis.",
        "possible_diagnoses": "Possible Diagnoses:",
        "no_match": "No matching disease found in the database. Please consult a veterinarian."
    },
    "العربية": {
        "title": "أداة تشخيص الأمراض الميكروبية البيطرية 🐄🧫",
        "enter_symptoms": "أدخل الأعراض مفصولة بفواصل (مثال: حمى, كسل, فقر الدم):",
        "upload_image": "ارفع صورة للحيوان المصاب أو العينة",
        "diagnose_btn": "تشخيص",
        "warning": "الرجاء إدخال الأعراض أو رفع صورة للحصول على التشخيص.",
        "possible_diagnoses": "التشخيصات المحتملة:",
        "no_match": "لم يتم العثور على مرض مطابق في قاعدة البيانات. يرجى استشارة طبيب بيطري."
    }
}

t = texts[language]

# ---- واجهة التطبيق ----
st.title(t["title"])
user_symptoms = st.text_input(t["enter_symptoms"])
uploaded_file = st.file_uploader(t["upload_image"], type=["jpg", "jpeg", "png"])

if st.button(t["diagnose_btn"]):
    if not user_symptoms and not uploaded_file:
        st.warning(t["warning"])
    else:
        # ---- معالجة الأعراض ----
        user_symptoms_list = [s.strip().lower() for s in user_symptoms.split(",")]

        results = []
        for disease in diseases:
            symptoms = disease["symptoms_en"] if language == "English" else disease["symptoms_ar"]
            matched = len(set(user_symptoms_list) & set([s.lower() for s in symptoms]))
            score = matched / len(symptoms)
            if score > 0:
                results.append({
                    "Disease": disease["name_en"] if language == "English" else disease["name_ar"],
                    "Match Score": round(score * 100, 2),
                    "Treatment": disease["treatment_en"] if language == "English" else disease["treatment_ar"]
                })

        if results:
            st.subheader(t["possible_diagnoses"])
            df = pd.DataFrame(results).sort_values(by="Match Score", ascending=False)
            st.table(df)
        else:
            st.info(t["no_match"])

        # ---- عرض الصورة ----
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
