import logging
import openai
import os

from dotenv import load_dotenv
from mwclient import Site
from langchain import OpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


load_dotenv()
logging.basicConfig(level=logging.WARNING)

# OpenAI
llm = OpenAI(
    model_name="gpt-4",
    openai_api_key=os.environ['OPENAI_API_KEY']
)
system_message_prompt = SystemMessagePromptTemplate.from_template("Your job is to convert HTML input documents into mediawiki markdown format, not regular markdown format. It's very important that you replace all html tags with their mediawiki markdown equivalent. Don't forget to convert things like center tags and especially tables. Before you send your output make sure you take a second or third pass ensuring all tags have been replaced and the mediawiki markdown is valid and complete, and no content has been lost in the conversion process. Only return the mediawiki markdown output, nothing else.")

# MW client
user_agent = "BME/llm-mediawiki-rev/0.0.1 (jonathon@bme.com)"
site = Site('wiki.bme.com',
    clients_useragent=user_agent,
    path='/',
)
site.login(os.environ['WIKI_USER'],os.environ['WIKI_PASSWORD'])

# Main loop (pages)
for page in site.allpages():
    print(f"--- {page.name}")

    text = page.text()

    # Get GPT to convert this page
    if text.startswith('<html'):
        print(len(text))
        if len(text) <= 30000:
            human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )
            chain = LLMChain(
                llm=llm,
                prompt=chat_prompt,
            )
            response = chain.run(text)

            # Update page
            if page.can("edit"):
                page.edit(response, 'Page conversion via llm-mediawiki-rev -jwm')
                print("Editing done...")
                print("----")
        else:
            print("Page probably contains too many tokens, skipping...")
    else:
        print("Page is not HTML format, skipping...")
        print("----")
