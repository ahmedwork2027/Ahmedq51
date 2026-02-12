import streamlit as st
from transformers import pipeline

st.title("تجربة نموذج Hugging Face")

user_input = st.text_input("أدخل نص للاستجابة:")

if user_input:
    # استخدام نموذج خفيف لتجنب مشاكل الذاكرة
    generator = pipeline("text-generation", model="distilgpt2")
    result = generator(user_input, max_length=50, num_return_sequences=1)
    
    st.write("الاستجابة:")
    st.write(result[0]['generated_text'])
