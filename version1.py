#Version 1 creates a LLM model where the user is continously asked for the ticker symbol of the stock they are interested in and 
#the current price of that specific stock is outputted. This continues on until the user is done and terminated the bot.
import os
import openai
from openai import OpenAI
import tiktoken
import yfinance as yf
#key  = "OPENAI API KEY"

#standard completion from openai stating model, temperature and token
def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(messages=messages,model=model)
    '''
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    '''
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


#gets the current price of any stock whose information is stored in yfinance
def get_current_stock_price(company_name):
    # Convert company name to stock ticker symbol
    company_ticker = yf.Ticker(company_name)

    # Get most recent data for the stock
    current_data = company_ticker.history(period="1d")

    # Extract current stock value (closing price)
    current_stock_value = current_data["Close"].iloc[-1]

    return current_stock_value

#continously asks user for ticker symbols for current stock prices until user is done asking
while True:

    company_name_prompt = "Please enter the ticker symbol of a company whose stock price you want to know:"
    #print(company_name_prompt)
    company_name = input(str(generate_response(company_name_prompt)) + " ")

    if company_name.lower() == "exit":
        print("Goodbye!")
        break

    try:
        current_price = get_current_stock_price(company_name)
        response = f"The current stock price of {company_name} is ${current_price:.2f}."
    except:
        if (len(company_name) == 0) or (len(company_name) > 4):
            response = f"Please enter a valid company ticker symbol for {company_name}. For instance, the company ticker symbol for Google is 'GOOG'."
        else:
            response = f"Sorry, I couldn't retrieve the stock price for {company_name}. Please make sure the company ticker symbol is correct."

    print(response)