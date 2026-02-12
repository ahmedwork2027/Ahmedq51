import streamlit as st
from transformers import pipeline
from PIL import Image

st.title("مساعد تشخيص الأمراض الميكروبية البيطرية 🐄🐑🐐")
st.write("أدخل الأعراض أو ارفع صورة للحصول على تشخيص تقريبي.")

# ----------- قسم النصوص -----------
st.header("تشخيص من الأعراض")
symptoms = st.text_area("أدخل وصف الأعراض هنا")

if st.button("تشخيص الأعراض"):
    if symptoms.strip() == "":
        st.warning("الرجاء إدخال الأعراض أولاً.")
    else:
        # نموذج نصوص مخصص (يمكنك تغييره لنموذج بيطري إذا وجد)
        text_model = pipeline("text-generation", model="google/flan-t5-small")  
        prompt = f"Given the following veterinary symptoms, provide the most likely microbial disease:\n{symptoms}"
        diagnosis = text_model(prompt, max_length=150, do_sample=False)[0]['generated_text']
        st.success(f"تشخيص تقريبي: {diagnosis}")

# ----------- قسم الصور -----------
st.header("تشخيص من الصورة")
uploaded_file = st.file_uploader("ارفع صورة للعينة أو الحيوان المصاب", type=["jpg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المرفوعة", use_column_width=True)

    if st.button("تشخيص الصورة"):
        st.info("نموذج الصور لم يتم تدريبه بعد على الأمراض البيطرية.")
        st.success("تشخيص تقريبي: احتمالية الإصابة بمرض ميكروبي محدد (تجريبي)")

st.write("---")
st.write("⚠️ هذا التطبيق للتجربة فقط، لا يعتمد عليه للتشخيص النهائي. استشر طبيب بيطري مختص دائماً.")
