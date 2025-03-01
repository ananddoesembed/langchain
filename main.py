import os
import gradio

from langchain_core.output_parsers import StrOutputParser
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
         given a story {story} 
         1.I need you to create a narration , when speaks bt a person in normal pace which
         lasts under two minutes, story's key elements should stay the same
        """

    summary_prompt_template = PromptTemplate(input_variables=["story"], template=summary_template)

    # llm = ChatAnthropic(temperature=0,model_name="claude-3-7-sonnet-20250219",timeout=10,stop=["stop"],api_key=KEY)
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro", api_key=KEY)

    chain = summary_prompt_template | llm | StrOutputParser()

    chat = chain.invoke(input={"story": text})
    return chat


info = """
The lion (Panthera leo) is a large cat of the genus Panthera, native to Africa and India. It has a muscular, broad-chested body; a short, rounded head; round ears; and a dark, hairy tuft at the tip of its tail. It is sexually dimorphic; adult male lions are larger than females and have a prominent mane. It is a social species, forming groups called prides. A lion's pride consists of a few adult males, related females, and cubs. Groups of female lions usually hunt together, preying mostly on medium-sized and large ungulates. The lion is an apex and keystone predator.

The lion inhabits grasslands, savannahs, and shrublands. It is usually more diurnal than other wild cats, but when persecuted, it adapts to being active at night and at twilight. During the Neolithic period, the lion ranged throughout Africa and Eurasia, from Southeast Europe to India, but it has been reduced to fragmented populations in sub-Saharan Africa and one population in western India. It has been listed as Vulnerable on the IUCN Red List since 1996 because populations in African countries have declined by about 43% since the early 1990s. Lion populations are untenable outside designated protected areas. Although the cause of the decline is not fully understood, habitat loss and conflicts with humans are the greatest causes for concern.
"""

if __name__ == "__main__":
    print("Hello, World!")
    d = gradio.Interface(fn=ai_interaction, inputs=["text"], outputs=["text"])
    d.launch()