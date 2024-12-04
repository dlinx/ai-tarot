from langchain_google_genai  import ChatGoogleGenerativeAI
import os
import pinecone
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

f = open('tarotdata.json',)
tarotdata = json.load(f)

def getCardInterpretation(card):
    return '''Card name: {}
    Card suite: {}
    Card Description: {}
    Card interpretation: {}
    '''.format(tarotdata[card]['name'],tarotdata[card]['suite'],tarotdata[card]['description'],
    tarotdata[card]['interpretation'])

def generateAIResponse(userQuestion, selectedCards ):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    past = getCardInterpretation(selectedCards[0])
    present =getCardInterpretation(selectedCards[1])
    challenge =getCardInterpretation(selectedCards[2])
    advice =getCardInterpretation(selectedCards[3])
    outcome =getCardInterpretation(selectedCards[4])

    # Load the vector store
    systemPrompt='''You are an AI-powered fortune-teller specializing in tarot card readings. Your role is to:
    Understand the user's question or concern to establish the reading's focus.
    Use the 5 tarot cards chosen by the user to provide insightful guidance.
    Interpret each card in its position (e.g., past, present, challenge, advice, outcome) while relating it to the user's question.
    Offer clear, empathetic, and meaningful advice based on the tarot's symbolism and themes.
    Avoid making absolute predictions about the future; instead, focus on possibilities, personal growth, and self-reflection.
    Provide context for each card, including its traditional meaning and how it connects to the user's inquiry.
    Use inclusive, sensitive language that respects diverse beliefs and values.
    Your objective is to empower users to make informed decisions and gain deeper insights through the tarot.
    ====================================================================================
    Here is the Past card:
    {}
    ====================================================================================
    Here is the Present card:
    {}
    ====================================================================================
    Here is the Challenge card:
    {}
    ====================================================================================
    Here is the Advice card:
    {}
    ====================================================================================
    Here is the Outcome card:
    {}
    ====================================================================================
    The user question is:
    {}
    ====================================================================================
    Answer the user question based on provided tarot card data.
    '''.format(past, present, challenge,advice,outcome, userQuestion)

    response = llm.invoke(systemPrompt)

    return response.content
answer = generateAIResponse("When will I get new job?",[0,1,2,3,4])
print(answer)