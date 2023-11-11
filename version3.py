#Version 3 contains a model that asks the user what information they desire about any stock and then tells the user that information.
#This model has an actual input field for the user to fill out and is more user-friendly.
import os
import openai
from openai import OpenAI
import tiktoken
import yfinance as yf
import yahoo_fin.stock_info as si
#key  = "OPENAI API KEY"

#completion from openai stating model, temperature and token
def get_completion(prompt, model="gpt-3.5-turbo"): #This is a more one turn conversation
    messages = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key = key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

#method to geenrate the response with the given prompt, instructions given on what GPT's role is and how to interact
def generate_response(prompt):
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
        messages=[{"role": "system", "content": """
        You are a stock catalog assistant for stock infomation.
        Respond in a friendly and helpful tone, with very concise answers.
        Make sure to ask the user relevant follow up questions."""},
        {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

#gets the information of any company which is then fed into the GPT model to read
def get_info(company_name):
    quote_table = si.get_quote_table(company_name, dict_result=False)
    return quote_table

#gets the user's inquiry on any stock and any information on that stock and outputs in proper conversational form.
while True:
    company_name_prompt = "Please enter the ticker symbol of a company whose stock price you want to know:"
    #print(company_name_prompt)
    company_name = input(generate_response(company_name_prompt) + " ")

    if company_name.lower() == "exit":
        print("Goodbye!")
        break

    company_info_prompt = "What would you like to know?"
    #print(company_info_prompt)
    company_info = input(generate_response(company_info_prompt) + " ")

    target_text = get_info(company_name)

    prompt = f"""
    The output from pdf and subsequent regex processing is delimited in triple quotes.
    Describe the {company_info} of the stock in sentence form.
    ### {target_text} ###.

    """

    response = get_completion(prompt)
    print(response)



#double checking the yfinance information with the table regarding the current stock written down
quote_table1 = si.get_quote_table("dell", dict_result=False)
print(quote_table1)