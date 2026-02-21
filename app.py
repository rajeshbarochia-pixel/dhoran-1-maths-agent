import streamlit as st
from google import genai
from pypdf import PdfReader
import os

# Page setup
st.set_page_config(page_title="ધોરણ-૧ ગણિત એજન્ટ", page_icon="🧮")
st.title("🎓 ધોરણ-૧ ગણિત એજન્ટ")
st.markdown("---")

# PDF Load
@st.cache_resource
def load_pdf_data(file_path):
    if not os.path.exists(file_path):
        return None
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

pdf_content = load_pdf_data("ekam_ganit.pdf")

# Sidebar
with st.sidebar:
    st.header("સેટિંગ્સ")
    api_key = st.text_input("Gemini API Key નાખો:", type="password")
    st.info("નોંધ: આ એજન્ટ ફક્ત આપેલ PDF માંથી જ જવાબ આપશે.")

# Main Logic
if pdf_content:
    if api_key:
        client = genai.Client(api_key=api_key)

        user_input = st.text_input("તમારો પ્રશ્ન પૂછો:")

        if user_input:
            prompt = f"""
            તમે ધોરણ 1 ના બાળકો માટેના ગણિત શિક્ષક છો.
            ફક્ત નીચેના Context પરથી જ જવાબ આપો.
            જો જવાબ ન મળે તો કહો: 'માફ કરશો, આ માહિતી તમારા પુસ્તકમાં નથી.'

            Context:
            {pdf_content}

            પ્રશ્ન:
            {user_input}
            """

            with st.spinner("વિચારી રહ્યો છું..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt
                    )
                    st.success("જવાબ:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"ભૂલ આવી: {e}")
    else:
        st.warning("કૃપા કરીને API Key નાખો.")
else:
    st.error("ekam_ganit.pdf ફાઇલ મળી નથી.")

st.markdown("---")
st.caption("Powered by Gemini 2.0")
