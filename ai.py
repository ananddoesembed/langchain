import os

from langchain_core.output_parsers import  CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

KEY = SecretStr(os.getenv("KEY"))
if KEY is None:
    KEY = ""

def ai_interaction(text):
    summary_template = """
         given a hindu god name {name} 
         1.I need you to create 5 interesting facts. Begin directly with the first fact, without any introductory statement.
         2. Your response should be a list of items separated by commas.
        Do NOT number your items or use any prefixes like '1.', 'a)', etc.
        For example, write 'apple, banana, orange' NOT '1. apple, 2. banana, 3. orange'.
        Each item should be a simple phrase with no numbering or bullets.
        """

    summary_prompt_template = PromptTemplate(input_variables=["name"], template=summary_template)

    # llm = ChatAnthropic(temperature=0,model_name="claude-3-7-sonnet-20250219",timeout=10,stop=["stop"],api_key=KEY)
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro", api_key=KEY)

    chain = summary_prompt_template | llm | CommaSeparatedListOutputParser()

    chat = chain.invoke(input={"name": text})
    return chat


def edit_output(original_output, edit_instructions,voices):
    print(voices)
    """Function to edit the previously generated output"""
    # This is a placeholder - replace with your actual editing logic
    if not original_output:
        return "No original output to edit. Please generate output first."

    # Simple example: if edit instruction is "reverse", reverse the string
    if edit_instructions.lower() == "reverse":
        # Extract just the part after "Generated output: "
        content = original_output.replace("Generated output: ", "")
        return f"Edited output: {content[::-1]}"
    # If edit instruction is "lowercase", convert to lowercase
    elif edit_instructions.lower() == "lowercase":
        content = original_output.replace("Generated output: ", "")
        return f"Edited output: {content.lower()}"
    # Default behavior - append the edit instructions
    else:
        return f"Edited output: {original_output} [{edit_instructions}]"