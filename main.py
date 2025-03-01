import os

from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from  langchain_ollama import ChatOllama
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

info ="""
The lion (Panthera leo) is a large cat of the genus Panthera, native to Africa and India. It has a muscular, broad-chested body; a short, rounded head; round ears; and a dark, hairy tuft at the tip of its tail. It is sexually dimorphic; adult male lions are larger than females and have a prominent mane. It is a social species, forming groups called prides. A lion's pride consists of a few adult males, related females, and cubs. Groups of female lions usually hunt together, preying mostly on medium-sized and large ungulates. The lion is an apex and keystone predator.

The lion inhabits grasslands, savannahs, and shrublands. It is usually more diurnal than other wild cats, but when persecuted, it adapts to being active at night and at twilight. During the Neolithic period, the lion ranged throughout Africa and Eurasia, from Southeast Europe to India, but it has been reduced to fragmented populations in sub-Saharan Africa and one population in western India. It has been listed as Vulnerable on the IUCN Red List since 1996 because populations in African countries have declined by about 43% since the early 1990s. Lion populations are untenable outside designated protected areas. Although the cause of the decline is not fully understood, habitat loss and conflicts with humans are the greatest causes for concern.
"""
KEY = SecretStr(os.getenv("KEY"))
if KEY is None:
    KEY=""
if __name__ == "__main__":
    print("Hello, World!")

    summary_template = """
     given the information {information} about an animal
     1.I need you to create a summary
     2. A fact about the animal
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"],template=summary_template)

    # llm = ChatAnthropic(temperature=0,model_name="claude-3-7-sonnet-20250219",timeout=10,stop=["stop"],api_key=KEY)
    llm = ChatOllama(temperature=0,model="deepseek-r1:14b",num_gpu=1)

    chain = summary_prompt_template | llm

    chat = chain.invoke(input={"information":info})
    print(chat)
