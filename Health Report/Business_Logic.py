import pandas as pd
import json
from Blood_Report import Blood_Report_PDF_Handler
from AI_Doctor.AI_Doctor_Response import AI_Doctor_Response
from dotenv import load_dotenv
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from textwrap import wrap
import os

load_dotenv()

os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_CSE_ID'] = os.getenv('GOOGLE_CSE_ID')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')


def Blood_Report_Analyser(file_path: str, age: int, gander: str, weight: float, height: float):
    blood_report_analyser = Blood_Report_PDF_Handler.PDFHandler(file_path=file_path)
    analysed_report = blood_report_analyser.Extract_Information()
    ai_doctor = AI_Doctor_Response(blood_report=analysed_report, age=age,
                                   gander=gander, weight=weight, height=height)
    return ai_doctor.ai_formatted_response()
    # return df


def generate_files(input_text: str) -> tuple[str, str]:
    # Create output directory
    output_dir = "output_files"
    os.makedirs(output_dir, exist_ok=True)

    # Set file paths
    pdf_path = os.path.join(output_dir, "diabetes_report.pdf")
    md_path = os.path.join(output_dir, "diabetes_report.md")

    # --- Create Markdown File ---
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(input_text)

    # --- Create PDF File ---
    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    width, height = LETTER
    margin = 50
    y = height - margin
    line_height = 14
    font_size = 12
    c.setFont("Helvetica", font_size)

    wrapped_lines = []
    for line in input_text.splitlines():
        if line.strip() == "":
            wrapped_lines.append("")  # Add blank lines for spacing
        else:
            wrapped_lines.extend(wrap(line, width=90))  # Wrap lines

    for line in wrapped_lines:
        if y <= margin:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", font_size)
        c.drawString(margin, y, line)
        y -= line_height

    c.save()

    return pdf_path, md_path


if __name__ == '__main__':
    response = Blood_Report_Analyser(
        file_path="blood_report.pdf",
        age=22,
        gander="Male",
        weight=61.0,
        height=5.6
    )
    print(response)
    # pdf_path, md_path = generate_files(response['output'])
