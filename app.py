import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

st.title("تطبيق دردشة ذكي 🤖")
st.write("اكتب رسالتك وسوف يجيب النموذج تلقائيًا:")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_model()

user_input = st.text_input("اكتب رسالتك هنا:")

if st.button("أرسل") and user_input.strip() != "":
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    st.success(response)
