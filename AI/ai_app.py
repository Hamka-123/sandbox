from google import genai
import pathlib
import json

client = genai.Client()

MODEL = "gemini-3.5-flash-lite"

LIMIT = 10
ROLE = "system architect"
FORMAT = "JSON"
# OBJECT = "programing languages"
OBJECT = "ascii file types"
KEYS = ['rank', 'object', 'popularity_score', 'description']

FILE = "file_types.json"

PROMPT = f"""
You are {ROLE}.
Get the {LIMIT} most popular {OBJECT}.
Sort it by DESC by rank of popularity
Return result in clear {FORMAT} format with keys: {KEYS}
"""

interaction = client.interactions.create(
        model=MODEL,
        input=PROMPT
    )
print(interaction.output_text)

# Clean markdown code blocks
raw_text = interaction.output_text.strip()
if raw_text.startswith("```json"):
    raw_text = raw_text[7:]
if raw_text.endswith("```"):
    raw_text = raw_text[:-3]
raw_text = raw_text.strip()

# Parse text into a Python object and save it cleanly
data = json.loads(raw_text)

with open(pathlib.Path(__file__).parent/f"{FILE}", 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)