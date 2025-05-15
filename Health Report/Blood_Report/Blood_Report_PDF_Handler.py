from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import pdfplumber
import os

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')


def extract_information_from_file(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


class PDFHandler:
    def __init__(self, file_path):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.prompt = PromptTemplate(
            input_variables=["report_text"],
            template="""
                You are a medical AI assistant trained to read and extract structured data from blood test reports.

                Given the following blood report text, extract the most relevant medical information. Include:

                1. Patient Name (if available)
                2. Age / Sex (if available)
                3. Test Date (if available)
                4. List of blood test components with:
                    - Test Name (e.g., Hemoglobin, WBC Count, etc.)
                    - Measured Value
                    - Normal Reference Range (if present)
                    - Unit (if available)
                5. Flag abnormal values clearly (e.g., HIGH/LOW)
                6. Doctor’s Notes or Interpretation (if present)

                Respond in the following structured format:
                ```json
                {{
                  "PatientName": "...",
                  "Age": "...",
                  "Sex": "...",
                  "Date": "...",
                  "Tests": [
                    {{
                      "TestName": "...",
                      "Value": "...",
                      "Unit": "...",
                      "ReferenceRange": "...",
                      "Flag": "NORMAL/HIGH/LOW"
                    }},
                    ...
                  ],
                  "DoctorNotes": "..."
                }}
                ```
                Text to extract from:
                {report_text}
            """
        )
        self.file_path = file_path

    def Extract_Information(self):
        text = extract_information_from_file(self.file_path)
        chain = self.prompt | self.model | StrOutputParser()
        response = chain.invoke({"report_text": text})
        print(response)
        return response


if __name__ == "__main__":
    report_path = "/Users/sadi_/Coding/Langchain AI Agent/Health Report/blood_report.pdf"
    handler = PDFHandler(file_path=report_path)
    extracted_info = handler.Extract_Information()
    print("Extracted Information: ")
    print(extracted_info)
