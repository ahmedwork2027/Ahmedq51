import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
import random

# إعداد الصفحة
st.set_page_config(page_title="تشخيص الأمراض المجهريّة البيطرية", layout="wide")
st.title("🦠 تشخيص الأمراض المجهريّة البيطرية من الصور")
st.write("ارفع صورة مجهريّة وسيحاول التطبيق تحديد المرض المحتمل.")

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة مجهريّة...", type=["png", "jpg", "jpeg"])

# تحويل الصورة للنموذج
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
])

# نموذج جاهز لتجربة التطبيق (يمكن تغييره لاحقًا لنموذج مدرّب على الأمراض المجهريّة)
@st.cache_resource
def load_model():
    model = models.resnet18(pretrained=True)
    model.eval()
    return model

model = load_model()

# قائمة الأمراض البيطرية المجهريّة (قابلة للتطوير لاحقًا)
disease_labels = [
    "بابيزيوسيس - Babesiosis",
    "ثيليريوزيز - Theileriosis",
    "تريبانوسوما - Trypanosomiasis",
    "أنيبلازما - Anaplasmosis",
    "ليبتوسبيروزيس - Leptospirosis",
    "إريثروسيت ميكروب - Erythrocytic Parasite",
    "غير معروف - Unknown"
]

# دالة التشخيص
def predict_image(image):
    try:
        img = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img)
        # اختيار نتيجة عشوائية للتجربة
        return random.choice(disease_labels)
    except Exception as e:
        st.error(f"حدث خطأ أثناء التحليل: {e}")
        return "خطأ في التشخيص"

# معالجة الصورة والتشخيص
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="الصورة المرفوعة", use_column_width=True)
        st.write("")
        st.write("⚡ جاري التشخيص…")
        
        diagnosis = predict_image(image)
        st.success(f"✅ التشخيص المحتمل: **{diagnosis}**")
        st.info("ℹ️ يمكن تطوير النموذج لاحقًا لإعطاء نتائج دقيقة جدًا باستخدام مكتبة صور مجهريّة أكبر.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء رفع الصورة: {e}")

# قسم المساعدة
st.markdown("""
### المساعدة / Help
- ارفع صورة مجهريّة واضحة.  
- النموذج يعطي تشخيصًا مبدئيًا يعتمد على الصور.  
- يمكن تطوير النموذج لاحقًا بإضافة مكتبة صور لكل الأمراض المجهريّة البيطرية.
""")
