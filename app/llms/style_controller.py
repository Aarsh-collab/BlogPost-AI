from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def style_summarizer(user_prompt: str) -> dict:
    

    model = OllamaLLM(model="llama3.2")
    parser = JsonOutputParser()
    template = """
You are a style interpretation engine.

{format_instructions}

TASK
Your job is to extract structured writing instructions from a user’s natural language request.
You do NOT write content.
You do NOT explain anything.
You ONLY classify intent and return structured constraints.

GOAL
Produce a style specification that is internally consistent, non-contradictory, and directly usable by a downstream writing model without interpretation conflicts.

INPUT
- The user prompt may be vague, creative, emotional, or unstructured.
- Your task is to normalize it into a clean, machine-readable style specification.

OUTPUT REQUIREMENTS
- Output MUST be valid JSON
- Output MUST match the schema exactly
- Do NOT include extra fields
- Do NOT include prose, explanations, or comments
- If the user does not specify something, choose a reasonable default
- NEVER produce logically conflicting values

STYLE SCHEMA
Return a JSON object with the following fields:

{{
  "tone": "string",
  "length": "short | medium | long",
  "brand_voice": "string",
  "audience": "string",
  "narrative_mode": "first-person | third-person | neutral",
  "structure": "chronological | reverse_chronological | thematic | freeform",
  "constraints": []
}}

INTERPRETATION RULES (STRICT)

GENERAL CONSISTENCY
- NEVER output contradictory fields
- If two user instructions conflict, resolve them conservatively
- Prefer explicit user instructions over inferred ones
- When uncertain, choose the simpler or safer option

TONE
- Infer emotional tone from adjectives and framing
- Examples: nostalgic, professional, analytical, playful, authoritative, personal

LENGTH
- short: under 500 words
- medium: 600–1000 words
- long: 1200+ words

BRAND VOICE
- If a brand is named, infer its voice (e.g. Disney → magical, optimistic)
- If no brand is mentioned, use "neutral, informative"

AUDIENCE
- Infer from context (e.g. travelers, general public, professionals, enthusiasts)

NARRATIVE MODE (POINT OF VIEW)

- first-person IF AND ONLY IF the user explicitly implies personal experience
  using first-person ownership (e.g. "I", "my trip", "we went", "our visit")
- third-person ONLY when the user describes people or experiences WITHOUT self-reference
- neutral ONLY for informational or analytical requests

- If first-person language is present, narrative_mode MUST be "first-person"
- Narrative mode controls POV ONLY, never structure or ordering
- NEVER infer third-person when first-person language exists

STRUCTURE (ORDERING)
- chronological = beginning → end
- reverse_chronological = end → beginning
- thematic = grouped by idea
- freeform = natural flow
- Use reverse_chronological ONLY if explicitly requested (e.g. “start from the end”)
- Structure controls time/order ONLY
- Structure MUST NOT influence narrative_mode
- NEVER map "start from the end" to narrative_mode

CONSTRAINTS
- Extract explicit instructions only
- Do NOT restate defaults as constraints
- Do NOT introduce inferred constraints
- Examples:
  - "start from the end"
  - "focus on emotions"
  - "avoid technical details"
  - "no statistics"

DEFAULTS (SAFE FALLBACKS)
If not explicitly specified:
- tone: "professional"
- length: "medium"
- brand_voice: "neutral, informative"
- audience: "general public"
- narrative_mode: "neutral"
- structure: "chronological"
- constraints: empty list

FINAL VALIDATION (MANDATORY)
Before outputting:
- Verify narrative_mode and structure do not overlap in meaning
- Verify no field contradicts another field
- If narrative_mode is not one of: first-person, third-person, neutral → error
- If structure and narrative_mode overlap in meaning → error

USER PROMPT
{user_prompt}
        """

    prompt = ChatPromptTemplate.from_template(template, partial_variables={
        "format_instructions": parser.get_format_instructions()
    })
    chain = prompt | model | parser

    return chain.invoke({"user_prompt": user_prompt})
