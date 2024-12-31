import os
import openai

# Get API key from file
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()

openai.api_key = api_key

# Create the prompt for a simple calculator
prompt = """Create a simple calculator program in Python that:
1. Has a command line interface
2. Supports basic operations (add, subtract, multiply, divide)
3. Keeps running until user chooses to exit
4. Handles basic error cases

Please provide the complete code."""

# Create OpenAI client
client = openai.OpenAI(api_key=api_key)

# Make the API call
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Save the generated code to calculator.py
print("Saving generated code to calculator.py...")
with open('calculator.py', 'w') as f:
    f.write(response.choices[0].message.content)
print("Done! You can now run: python calculator.py")
