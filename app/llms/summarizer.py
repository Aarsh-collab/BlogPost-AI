from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def summarizer(website_text: str) -> dict:
    

    model = OllamaLLM(model="llama3.2")
    parser = JsonOutputParser()
    template = """
    {format_instructions}
        You are a research summarization engine.

        Your task:
        - Read the following website text
        - Extract ONLY factual information
        - Ignore references, citations, author lists, navigation text, and filler

        Return a JSON object with the following structure:

        {{
        "key_points": [
            "Concise factual statements (1–2 sentences each)"
        ],
        "statistics": [
            {{
            "label": "short description of the metric",
            "value": "number with units if available"
            }}
        ],
        "themes": [
            "high-level topics covered in the text"
        ]
        }}

        Rules:
        - Do NOT write prose
        - Do NOT add explanations
        - Do NOT invent facts
        - If a section has no data, return an empty list
        - Output MUST be valid JSON

        Website text:
        {website_text}
        """

    prompt = ChatPromptTemplate.from_template(template, partial_variables={
        "format_instructions": parser.get_format_instructions()
    })
    chain = prompt | model | parser

    return chain.invoke({"website_text": website_text})
