import streamlit as st
from transformers import pipeline

# استخدام التوكن الخاص بك
HF_TOKEN = "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"

st.title("تجربة Streamlit + HuggingFace")

st.write("أدخل نص لتوليد استجابة:")

user_input = st.text_area("نصك هنا:")

if st.button("توليد"):
    if user_input.strip() != "":
        generator = pipeline("text-generation", model="gpt2", use_auth_token=HF_TOKEN)
        result = generator(user_input, max_length=50, num_return_sequences=1)
        st.write(result[0]['generated_text'])
    else:
        st.warning("الرجاء إدخال نص أولاً!")