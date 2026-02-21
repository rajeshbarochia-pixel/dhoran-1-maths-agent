import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# ----------------------------
# 1️⃣ Page Setup
# ----------------------------
st.set_page_config(page_title="ધોરણ-૧ ગણિત એજન્ટ", page_icon="🧮")

st.title("🎓 ધોરણ-૧ ગણિત એજન્ટ")
st.markdown("---")

# ----------------------------
# 2️⃣ PDF Load Function
# ----------------------------
@st.cache_resource
def load_pdf_data(file_path):
    if not os.path.exists(file_path):
        return None
    
    reader = PdfReader(file_path)
    full_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    return full_text


# PDF file name (GitHub માં હોવી જોઈએ)
pdf_content = load_pdf_data("ekam_ganit.pdf")


# ----------------------------
# 3️⃣ Sidebar - API Key
# ----------------------------
with st.sidebar:
    st.header("સેટિંગ્સ")
    api_key = st.text_input("Gemini API Key નાખો:", type="password")
    st.info("નોંધ: આ એજન્ટ ફક્ત આપેલ PDF માંથી જ જવાબ આપશે.")


# ----------------------------
# 4️⃣ Main Logic
# ----------------------------
if pdf_content:

    if api_key:

        try:
            # Gemini Configure
            genai.configure(api_key=api_key)

            # Model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # User Input
            user_input = st.text_input(
                "તમારો પ્રશ્ન પૂછો:",
                placeholder="દા.ત. આ પાઠમાં કઈ કઈ વસ્તુઓ ગણવાની છે?"
            )

            if user_input:

                prompt = f"""
                તમે ધોરણ 1 ના બાળકો માટેના એક આદર્શ ગણિત શિક્ષક છો.
                તમારે ફક્ત નીચે આપેલા 'Context' પરથી જ જવાબ આપવો.
                જો જવાબ Context માં ન હોય તો કહો:
                'માફ કરશો, આ માહિતી તમારા પુસ્તકમાં નથી.'

                Context:
                {pdf_content}

                પ્રશ્ન:
                {user_input}
                """

                with st.spinner("વિચારી રહ્યો છું..."):

                    response = model.generate_content(prompt)

                    st.success("જવાબ:")
                    st.write(response.text)

        except Exception as e:
            st.error(f"ભૂલ આવી: {e}")

    else:
        st.warning("ચેટ શરૂ કરવા માટે કૃપા કરીને API Key નાખો.")

else:
    st.error("❌ 'ekam_ganit.pdf' ફાઇલ મળી નથી. GitHub માં upload કરો.")


st.markdown("---")
st.caption("Powered by Gemini AI | Streamlit Cloud")
