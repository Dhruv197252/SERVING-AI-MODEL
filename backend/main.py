from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import torch

app = FastAPI()


# CORS Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Route

@app.get("/")
def home():

    return {
        "message": "AI NLP Playground API Running"
    }


# Sentiment Analysis Model

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1
)


# Text Generation Model

classifier_text_generation = pipeline(
    "text-generation",
    model="distilgpt2",
    device=-1
)


# Named Entity Recognition Model

classifier_ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",
    device=-1
)


# Request Body Schema

class TextInput(BaseModel):
    text: str


# Sentiment Analysis Endpoint

@app.post("/sentiment")
def sentiment(data: TextInput):

    result = classifier(data.text)

    return {

        "input": data.text,
        "prediction": result

    }


# Text Generation Endpoint

@app.post("/generate")
def generate(data: TextInput):

    result = classifier_text_generation(

        data.text,

        max_length=50,

        num_return_sequences=1

    )

    return {

        "input": data.text,
        "prediction": result

    }


# Named Entity Recognition Endpoint

@app.post("/ner")
def ner(data: TextInput):

    result = classifier_ner(data.text)

    formatted_result = []

    for item in result:

        formatted_result.append({

            "word": item["word"],
            "entity": item["entity_group"],
            "score": float(item["score"])

        })

    return {

        "input": data.text,
        "prediction": formatted_result

    }