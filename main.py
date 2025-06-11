import os
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask import Flask, request, jsonify
import whisper
os.environ["AZURE_OPENAI_API_KEY"] = "11APLu6CZtZnYvxroeo8CHAacCt9wDXCb7miKIFwTsgB3bnK5SJGJQQJ99BEACYeBjFXJ3w3AAABACOGYqeV"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aiplanetllm.openai.azure.com/"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "gpt-4o"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-12-01-preview"
# os.environ["AZURE_OPENAI_API_VERSION"] = "2024-11-20"
os.environ["SPEECH_KEY"] ="G86doTy0u0vyRxeblaG69zbSCUbQXLHdeSokDqdFh4kaxVGFzGSQJQQJ99BEACYeBjFXJ3w3AAAYACOG48Be"
os.environ["ENDPOINT"] = "https://eastus.api.cognitive.microsoft.com/"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "gpt-4o"
os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.environ.get("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.environ.get("AZURE_OPENAI_API_VERSION")

app = Flask(__name__)


@app.route("/generate_script",methods=["POST"])
def generate_script():
    # Get form data
    prompt = request.form.get("prompt")  # prompt as form field
    voiceover_file = request.files.get("file")  # file input

    if not voiceover_file or not prompt:
        return jsonify({"error": "Missing prompt or file"}), 400


    voiceover_file.save("./audio/temp.mp3")


    voiceover = speech_to_text("./audio/temp.mp3")


    python_script = generate_script(prompt_text=prompt, voiceover_text=voiceover)


    write_file(python_script)
    try:
        os.system("manim -pql generated.py ConceptScene")
        video_path = "media/videos/generated/1080p60/ConceptScene.mp4"
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({
        "transcription": voiceover,
        "script": python_script,
        "script_written": True
    })


def speech_to_text(speech):
    model = whisper.load_model("base")
    result = model.transcribe(speech)
    return result["text"]


def generate_script(prompt_text, voiceover_text):
    # Initialize embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint="https://aiplanetllm.openai.azure.com/",
        deployment="text-embedding-ada-002",
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        openai_api_version="2023-05-15"
    )

    # Initialize the LLM
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        model="gpt-4o"
    )

    PROMPT_TEMPLATE = """
You are an expert Python developer and Manim animation script writer.

Your task is to generate a complete and executable Manim script that visually illustrates the provided concept. You will be given:

1. A **conceptual prompt** – describing what should be visualized.
2. A **voiceover script** – the narration that will play during the animation.

### Requirements:
- Output **only valid Python code** — no markdown, no extra explanation, no labels like "```python" and make sure your script doesn't require any external svg's or something.
- The script must include:
  - Necessary imports (e.g., `from manim import *`)
  - A class that inherits from `Scene` (e.g., `class ConceptScene(Scene):`)
  - Step-by-step animations that visually reflect the voiceover narration.
  - Helpful comments explaining each step.
  - Educational use of shapes, text, arrows, and movement to clearly convey the concept.
- Synchronize the animations to flow with the **voiceover narration**.
- Ensure it's visually engaging and suitable for educational purposes.

---

Here is the **conceptual prompt**:
{prompt}

Here is the **voiceover narration**:
{voiceover}

Now, generate the full Manim script:
"""


    PROMPT = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["prompt", "voiceover"]
    )

    # Load QA chain
    qa_chain = LLMChain(
        llm=llm,
        prompt=PROMPT,
        verbose=True
    )

    # Invoke LLM
    response = qa_chain.invoke({
        "prompt": prompt_text,
        "voiceover": voiceover_text
    })

    return response["text"]

def write_file(script):
    try:
        with open("generated.py","w+") as fileObj:
            fileObj.write(script)
        return True
    except Exception as e:
        return False





if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000)
