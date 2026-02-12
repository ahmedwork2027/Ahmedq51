import streamlit as st
from transformers import pipeline
from PIL import Image

st.title("مساعد التشخيص المبسط 🩺")
st.write("يمكنك كتابة الأعراض أو رفع صورة للحصول على تشخيص تقريبي.")

# -------------------
# قسم النصوص
# -------------------
st.header("تشخيص من الأعراض النصية")
symptoms = st.text_area("اكتب الأعراض هنا")

if st.button("تشخيص الأعراض"):
    if symptoms.strip() == "":
        st.warning("الرجاء إدخال الأعراض أولاً.")
    else:
        # نموذج نصوص من HuggingFace
        text_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = text_model(symptoms)
        st.success(f"تشخيص تقريبي: {result[0]['label']} (ثقة: {result[0]['score']:.2f})")

# -------------------
# قسم الصور
# -------------------
st.header("تشخيص من الصورة")
uploaded_file = st.file_uploader("ارفع صورة هنا (مثل الحيوان أو العينة)", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المرفوعة", use_column_width=True)

    if st.button("تشخيص الصورة"):
        # هنا يمكن دمج نموذج صور طبي
        st.info("حالياً مجرد نموذج تجريبي، لم يتم تحليل الصورة فعلياً.")
        st.success("تشخيص تقريبي من الصورة: محتمل أن يكون الحالة X أو Y")

st.write("---")
st.write("⚠️ ملاحظة: هذا التطبيق للتجربة فقط، لا يعتمد عليه للتشخيص النهائي. استشر الطبيب دائماً.")
