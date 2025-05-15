import streamlit as st
from Business_Logic import *


st.title("Health Report")
st.subheader("Your Personal AI Doctor Guides You to Health")

col1, col2 = st.columns([1, 2])
with col1:
    pdf_uploader = st.file_uploader("Upload a PDF", type="pdf")
with col2:
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        weight = st.number_input("Weight (kg)", min_value=0.0, step=5.0, value=40.0)
        gander = st.radio("Gender", ["Male", "Female"])
    with col2_2:
        age = st.number_input("Age", min_value=0, max_value=120, value=10)
        height = st.slider("Height (ft)", min_value=2.0, max_value=10.0, step=0.1, value=5.0)

if st.button("Analyze"):
    if pdf_uploader and weight > 0 and height > 0 and age > 0 and gander:
        # 1) save upload to a temp file
        tmp_path = "temp_report.pdf"
        with open(tmp_path, "wb") as f:
            f.write(pdf_uploader.read())

        # 2) run your analyzer
        resp = Blood_Report_Analyser(
            file_path=tmp_path,
            age=int(age),
            gander=gander,
            weight=float(weight),
            height=float(height),
        )

        # 3) show the AI’s text
        st.markdown("### AI Doctor’s Recommendations")
        with st.expander("Here is the response"):
            st.markdown(resp)

        # 4) generate PDF + MD and offer downloads
        pdf_path, md_path = generate_files(resp)
        with open(pdf_path, "rb") as f_pdf, open(md_path, "r", encoding="utf-8") as f_md:
            st.download_button("Download PDF Report", f_pdf, file_name="health_report.pdf")
            st.download_button("Download Markdown", f_md,  file_name="health_report.md")
    else:
        st.warning("Please make sure to provide all required inputs: PDF file, age, gender, weight, and height.")