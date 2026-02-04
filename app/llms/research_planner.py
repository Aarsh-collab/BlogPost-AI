from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def research_planner(user_message: str,):
    

    model = OllamaLLM(model="llama3.2")
    parser = JsonOutputParser()
    template = """
        You are a research planning assistant.

        Your task is to decide WHAT should be researched, not to provide facts, analysis, or writing.

        Given a user request for a blog post, you must:
        - Identify the main research areas
        - Generate concrete search queries that would retrieve authoritative sources
        - Focus on reports, policy documents, industry analysis, and recent data

        Rules:
        - Do NOT write the blog.
        - Do NOT summarize facts.
        - Do NOT invent data.
        - Do NOT include opinions.
        - Do NOT explain your reasoning.
        - Output MUST be valid JSON.
        - Output ONLY the JSON, nothing else.

        User request:
        {user_message}

        Return JSON in the following exact format:

        {{
        "research_areas": [
            "string",
            "string"
        ],
        "search_queries": [
            "string",
            "string"
        ]
        }}
        """

    prompt = ChatPromptTemplate.from_template(template, partial_variables={
        "format_instructions": parser.get_format_instructions()})
    chain = prompt | model | parser

    return chain.invoke({"user_message": user_message})
