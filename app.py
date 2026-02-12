import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

st.title("تطبيق دردشة ذكي 🤖")
st.write("اكتب رسالتك وسوف يجيب النموذج تلقائيًا:")

# تحميل النموذج
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_model()

# إدخال المستخدم
user_input = st.text_input("اكتب رسالتك هنا:")

if st.button("أرسل"):
    if user_input.strip() != "":
        with st.spinner("جارٍ تجهيز الرد..."):
            response = generator(user_input, max_length=100, do_sample=True, top_k=50, top_p=0.95)
            st.success(response[0]['generated_text'])
    else:
        st.warning("الرجاء كتابة نص قبل الضغط على أرسل!")
