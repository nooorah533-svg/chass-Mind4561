import streamlit as st
import google.generativeai as genai
import time

# إعدادات الصفحة
st.set_page_config(page_title="Gemini Dashboard", layout="wide")

# إعداد الجلسة (Session State) لتخزين الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- القائمة الجانبية (Sidebar) للتحكم ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("أدخل مفتاح API الخاص بك", type="password")
    model_choice = st.selectbox("اختر إصدار النموذج", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temp = st.slider("درجة الحرارة (Creativity)", 0.0, 1.0, 0.7)
    
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# --- قسم الإحصائيات (Metrics) ---
st.title("🚀 Gemini AI Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("عدد الرسائل", len(st.session_state.messages))
col2.metric("النموذج النشط", model_choice)
col3.metric("الحالة", "متصل" if api_key else "في انتظار المفتاح")

---

# --- منطقة الشات ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
    if not api_key:
        st.error("يرجى إدخال API Key في القائمة الجانبية أولاً!")
    else:
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # إعداد Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_choice)
        
        # عرض رد جيمني مع تأثير الكتابة
        with st.chat_message("assistant"):
            response = model.generate_content(prompt, generation_config={"temperature": temp})
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
