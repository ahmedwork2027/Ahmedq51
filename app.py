import streamlit as st
from PIL import Image
import requests
from googleapiclient.discovery import build

st.set_page_config(page_title="تشخيص الصور المجهريّة البيطرية", layout="wide")

st.title("تشخيص الصور المجهريّة البيطرية 🐾🔬")
st.write("ارفع صورة مجهريّة للحصول على تحليل ونتائج بحث متعلقة بها.")

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)

    st.write("🔍 جاري البحث عن أمراض مشابهة على الإنترنت...")

    # تحويل الصورة إلى وصف نصي (تجريبي - يمكن تعديل)
    description = st.text_input("أدخل وصف مختصر للصورة (مثلاً: خلية دم مصابة بـ Brucella)")

    if description:
        # ==== إعداد Google Custom Search ====
        api_key = "YOUR_GOOGLE_API_KEY"        # ضع مفتاحك هنا
        cse_id = "YOUR_CUSTOM_SEARCH_ENGINE_ID" # ضع معرف محرك البحث المخصص هنا

        def google_search(query, api_key, cse_id, num=5):
            service = build("customsearch", "v1", developerKey=api_key)
            res = service.cse().list(q=query, cx=cse_id, num=num).execute()
            return res['items']

        try:
            results = google_search(description, api_key, cse_id)
            st.success("✅ تم العثور على نتائج:")
            for r in results:
                st.write(f"**{r['title']}**")
                st.write(r['link'])
                st.write(r['snippet'])
                st.write("---")
        except Exception as e:
            st.error(f"حدث خطأ أثناء البحث: {e}")
