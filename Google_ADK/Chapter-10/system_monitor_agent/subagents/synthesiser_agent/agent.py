from google.adk.agents import LlmAgent
from dotenv import load_dotenv

load_dotenv()


system_report = LlmAgent(
    model='gemini-2.0-flash-001',
    name='SynthesiserAgent',
    instruction="""You are a System Report Synthesizer.

        Your task is to create a comprehensive system health report by combining information from:
        - CPU information: {cpu_info}
        - Memory information: {memory_info}
        - Disk information: {disk_info}

        Create a well-formatted report with:
        1. An executive summary at the top with overall system health status
        2. Sections for each component with their respective information
        3. Recommendations based on any concerning metrics

        Use markdown formatting to make the report readable and professional.
        Highlight any concerning values and provide practical recommendations.
        """,
    description="Synthesizes all system information into a comprehensive report",
)
