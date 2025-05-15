from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .AI_Doctor_Tools import custom_disease_info_search_google, custom_disease_info_search_tavily
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')


class AI_Doctor_Response:

    def __init__(self, blood_report: str, age: int, weight: float,
                 height: float, gander: str):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.blood_report = blood_report
        self.tools = [custom_disease_info_search_google,
                      custom_disease_info_search_tavily]
        self.prompt = PromptTemplate(
            input_variables=["blood_report"],
            template="""
        You are an experienced and knowledgeable medical doctor. You will be given a blood test report in JSON format. Your job is to analyze the report and provide a thorough, clear, and professional explanation.

        Blood Report:
        {blood_report}

        Your response should include the following sections:
        1. **Summary of Observations** – Identify and summarize key findings (e.g., abnormal values).
        2. **Possible Medical Interpretations** – What could these results indicate about the patient’s health?
        3. **Recommended Next Steps** – What actions or tests should the patient consider next?
        4. **Treatment Suggestions** – Suggest treatments or medications if applicable.
        5. **Prevention & Health Tips** – General advice on maintaining or improving health based on the report.

        Make sure the tone is compassionate, accurate, and easily understandable for a non-medical person.
        """
        )
        self.age = age
        self.weight = weight
        self.gander = gander
        self.height = height

    def ai_doctor_response(self):
        chain = self.prompt | self.model | StrOutputParser()
        response = chain.invoke({"blood_report": self.blood_report})
        return response

    def ai_doctor_agent(self):
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(
            llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro"),
            tools=self.tools,
            prompt=prompt
        )

        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True, handle_parsing_errors=True)
        response = agent_executor.invoke({"input": f"""
            You are an advanced AI medical assistant. Your task is to analyze 
            the provided blood test report in detail and help the user understand its implications.
            Here is the blood report information:
            {self.blood_report}

            Based on your medical knowledge and internet tools:
            1. Determine if the patient's blood report suggests a good or bad health condition. 
               Mention whether any results are abnormal and what they imply.
            2. Detect if the patient is showing symptoms or values indicating the 
               presence of a specific disease. Use both your existing knowledge and internet 
               search to make the diagnosis more accurate.
            3. If a disease or abnormality is detected, explain:
               - Why this might be happening (possible causes),
               - How it develops in the body (brief medical insight),
               - What can be done to cure or manage it (treatment options),
               - How it can be prevented in the future (preventive measures).
            4. Additionally, search and explain which diseases might be associated with 
               the findings in the blood report and include key references from trusted sources.

            Ensure your explanation is professional, easy to understand for non-medical individuals,
            and includes compassionate medical guidance.
        """})

        return response

    def ai_formatted_response(self):
        response1 = self.ai_doctor_response()
        response2 = self.ai_doctor_agent()

        format_prompt = PromptTemplate(
            input_variables=["response1",
                             "response2",
                             "height",
                             "weight",
                             "age",
                             "gander"],
            template="""
            You are a professional medical report formatter. Combine and format the 
            two AI-generated responses into a single well-structured Markdown output. 
            Preserve the meaningful content from both responses and organize them into 
            coherent sections. Use headings, bullet points, and bold text to enhance readability.
            ## 🧪 AI Analysis Based on Medical Knowledge
            {response1}
            ---
            ## 🌐 AI Medical Assistant With Internet Support
            {response2}
            ---
            ## ✅ Final Guidance
            - Carefully compare both analyses.
            - Pay close attention to any common insights or overlapping concerns.
            - Encourage the user to follow up with a healthcare provider for accurate diagnosis and personalized treatment.
            
            
            ## ✅ Finally Give the Patience a Complete detailed guideline on how to make himself 
            free and healthy from the disease. make me a proper list of things that the persons needs
            to do, food habit, exercise routine, health routine and suggest him extra tips as well.
            I mean make him a Complete routine which will take the patience from sick to fully fit.
            you must consider height : {height}ft, weight {weight}, age: {age}, gender: {gander} while
            giving your suggestion.
            """


        )

        chain = format_prompt | self.model | StrOutputParser()
        formatted_response = chain.invoke({
            "response1": response1,
            "response2": response2,
            "height": self.height,
            "weight": self.weight,
            "age": self.age,
            "gander": self.gander
        })

        return formatted_response
