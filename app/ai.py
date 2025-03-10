import random
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import ast
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
import random
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_core.output_parsers import JsonOutputParser
import json

from json import JSONDecodeError
from langchain_openai import AzureChatOpenAI
import re


class AI:
    SAMPLE_TOPICS = [
        "The future of AI",
        "Machine Learning breakthroughs",
        "Technology trends",
        "Coding tips",
        "Innovation in tech"
    ]

    @staticmethod
    def safe_json_parse(response):
        try:
            # First attempt: Standard JSON extraction
            json_str = re.search(r'\{.*\}', response, re.DOTALL).group(0)
            return json.loads(json_str)
        except (AttributeError, JSONDecodeError):
            # Fallback: Manual sanitization
            sanitized = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', response)
            return json.loads(sanitized)
        except Exception as e:
            print(f"Critical parse error: {str(e)}")
            return {"title": "", "content": "", "hashtags": []}

    @staticmethod
    def generate_tweet(title, hashtag="", content=""):
        """Generates a tweet using the Gemini 2.0 Flash model with contextual search."""
       

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=200,
            timeout=None,
            max_retries=2,
        )
        # llm = AzureChatOpenAI(
        #         azure_endpoint= azure_endpoint,
        #         api_key= api_key,
        #         api_version=api_version,
        #         azure_deployment=deployment_name
        #     )
        
        if not title:
            title = random.choice(AI.SAMPLE_TOPICS)
        
        wikipedia = WikipediaAPIWrapper(
            top_k_results=5,
            doc_content_chars_max=1000,
            wiki_client=None
        )

        tools = [
            Tool(
                name="WikipediaSearch",
                func=lambda q: wikipedia.run(q).replace("{", "{{").replace("}", "}}"),
                description="CRUCIAL for factual verification. REQUIRED when content empty."
            )
        ]

        
        prompt = ChatPromptTemplate.from_template(
            template="""
    You are an expert social media strategist specialized in crafting viral and engaging tweets on trending topics.
    You are provided with:
    - Topic: {title}
    - Hashtag(s): {hashtag}
    - Content: {content}

    **Task:**
    1. If additional context is needed to understand the topic, use the Wikipedia Search tool to fetch relevant details.
    2. Generate a compelling tweet that is engaging, human-like, and has viral potential. If the content is missing, create the tweet solely based on the title.
    3. Refine and expand the provided hashtags for maximum engagement (do not include hashtags within the tweet content).
    4. Return your result strictly in the following JSON format (without any additional text):
    5. you are restricted to write the whole content in 150 charactors only. 
    {{
        "title": "<Generated title>",
        "content": "<Generated tweet content>",
        "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]
    }}

    **Important:**
    - Always use the Wikipedia Search tool if you require additional context about the topic.
    - Do not provide any explanations outside of the JSON output.
    """
        )
        
        
        # agent = initialize_agent(
        #     tools=tools, 
        #     llm=llm, 
        #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        #     verbose=True,
        #     handle_parsing_errors=True
        # )
        chain = prompt | llm | JsonOutputParser()
        # prompt.format(title=title, hashtag=hashtag, content=content)
        response = chain.invoke({"title":title,"hashtag":hashtag,"content":content})
        # response = agent.run(prompt.format(title=title, hashtag=hashtag, content=content))
        print("Agent raw response:", response)
        
        # json_match =AI.safe_json_parse(response)
        # print("json match: ",json_match)
        return response
        # if json_match:
        #     print("JSON MATCH:")
        #     return json.loads(json_match.group(0))
        # else:
        #     return {"title": "", "content": "", "hashtags": []}
