import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# ૧. પેજ સેટઅપ
st.set_page_config(page_title="ગણિત શિક્ષક - ધોરણ ૧", page_icon="🧮")

st.title("🎓 ધોરણ-૧ ગણિત એજન્ટ")
st.markdown("---")

# ૨. PDF માંથી ડેટા લોડ કરવો (કાયમી ફાઇલ)
@st.cache_resource  # આનાથી વારંવાર PDF લોડ નહીં કરવી પડે
def load_pdf_data(file_path):
    if not os.path.exists(file_path):
        return None
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

# તમારી PDF ફાઇલનું નામ અહીં લખો
pdf_content = load_pdf_data("ekam_ganit.pdf")

# ૩. સાઇડબારમાં API Key
with st.sidebar:
    st.header("સેટિંગ્સ")
    api_key = st.text_input("Gemini API Key નાખો:", type="password")
    st.info("નોંધ: આ એજન્ટ ફક્ત આપેલ PDF માંથી જ જવાબ આપશે.")

# ૪. મુખ્ય લોજિક
if pdf_content:
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_input("તમારો પ્રશ્ન પૂછો:", placeholder="દા.ત. આ પાઠમાં કઈ કઈ વસ્તુઓ ગણવાની છે?")

        if user_input:
            # એજન્ટ માટે કડક સૂચનાઓ
            prompt = f"""
            તમે ધોરણ 1 ના બાળકો માટેના એક આદર્શ ગણિત શિક્ષક છો. 
            તમારે ફક્ત નીચે આપેલા 'Context' ના આધારે જ જવાબ આપવાનો છે.
            જો જવાબ 'Context' માં ન હોય, તો કહો કે 'માફ કરશો, આ માહિતી તમારા પુસ્તકમાં નથી'.
            
            Context: {pdf_content}
            પ્રશ્ન: {user_input}
            """

            with st.spinner("વિચારી રહ્યો છું..."):
                try:
                    response = model.generate_content(prompt)
                    st.success("જવાબ:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"ભૂલ આવી: {e}")
    else:
        st.warning("ચેટ શરૂ કરવા માટે કૃપા કરીને સાઇડબારમાં તમારી API Key નાખો.")
else:
    st.error("ભૂલ: 'ekam_ganit.pdf' ફાઇલ મળી નથી. ખાતરી કરો કે તમે ફાઇલ અપલોડ કરી છે.")

st.markdown("---")
st.caption("Powered by Gemini AI | GitHub પ્રોજેક્ટ માટે તૈયાર")