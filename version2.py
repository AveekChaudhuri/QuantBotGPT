import os
import openai
import tiktoken
import yfinance as yf
import yahoo_fin.stock_info as si
#openai.api_key  = "OPENAI API KEY"

#standard completion from openai stating model, temperature and token
def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

#method to geenrate the response with the given prompt, instructions given on what GPT's role is and how to interact
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
        messages=[{"role": "system", "content": """
        You are a stock catalog assistant for stock infomation.
        Respond in a friendly and helpful tone, with very concise answers.
        Make sure to ask the user relevant follow up questions."""},
        {"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()

#gets the information of any company which is then fed into the GPT model to read
def get_info(company_name):
    quote_table = si.get_quote_table(company_name, dict_result=False)
    return quote_table

target_text = get_info("dell")

def get_completion(prompt, model="gpt-3.5-turbo"): #This is a more one turn conversation
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

#prompting for GPT to understand its role and give the desired output with the quote table received from target_text
prompt = f"""
The output from pdf and subsequent regex processing is delimited in triple quotes.
Describe the day's highest stock price of the stock in sentence form.
### {target_text} ###.

"""
response = get_completion(prompt)
print(response)

#double checking the yfinance information with the table regarding the current stock written down
quote_table1 = si.get_quote_table("dell", dict_result=False)
print(quote_table1)