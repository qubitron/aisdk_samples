import os
from promptflow.core import AzureOpenAIModelConfiguration

# Initialize Azure OpenAI Connection
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
)

# Run built-in evaluator on a single input row
from promptflow.evals.evaluators import RelevanceEvaluator

relevance_eval = RelevanceEvaluator(model_config)
relevance_score = relevance_eval(
    answer="The Alpine Explorer Tent is the most waterproof.",
    context="From the our product list,"
    " the alpine explorer tent is the most waterproof."
    " The Adventure Dining Table has higher weight.",
    question="Which tent is the most waterproof?",
)
# relevance_score: 5.0

# custom evaluator
from promptflow.client import load_flow

# load apology evaluatorfrom prompty
apology_eval = load_flow(source="apology.prompty", model={"configuration": model_config})

result = apology_eval(
    question="What is the capital of France?", answer="Paris"
)

# result: {'apology': 0}


from promptflow.evals.evaluate import evaluate

result = evaluate(
    data="data.jsonl",
    evaluators={
        "relevance": relevance_eval,
        "violence": violence_eval,
        "answer_length": answer_length,
        "apology": apology_eval
    },
    # column mapping
    evaluator_config={
        "default": {
            "ground_truth": "${data.truth}"
        }
    }
)