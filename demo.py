import openai
import ast
import json
import os
from typing_extensions import override
from instructions import instructions
from functions import zero_shot_predict

client = openai.OpenAI(
    api_key = "COPY-API-KEY-HERE"
)

def create_assistant(name="", instructions="", model="gpt-4-turbo", tools=None, debug=False):
    assistant_file_path = "assistant.json"
    assistant_json = []
    # load existing assistant json
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            assistant_json = json.load(file)
            for assistant_data in assistant_json:
                assistant_name = assistant_data["assistant_name"]
                if assistant_name == name:
                    assistant_id = assistant_data["assistant_id"]
                    if debug:
                        print("Loading existing Assistant ID")
                    if debug:
                        print("Assistant ID: ", assistant_id)
                    return assistant_id

    # create Assistant
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools
    )

    assistant_id = assistant.id
    assistant_name = assistant.name
    
    # save Assistant info
    assistant_json.append(
        {
            "assistant_name": assistant_name,
            "assistant_id": assistant_id
        }
    )
    with open(assistant_file_path, "w", encoding="utf-8") as file:
        json.dump(assistant_json, file, ensure_ascii=False, indent=4)
        print("New Assistant info saved")
        
    return assistant_id

DEBUG = False

assistant_id = create_assistant(
    name="iBioFAB co-pilot",
    instructions=instructions,
    model="gpt-4-turbo",
    tools=[
        {
            "type": "file_search"
        },
        # {
        #     "type": "code_interpreter"
        # },
        {
            "type": "function",
            "function": {
                "name": "get-protein-zero-shot",
                "description": "Obtain user input protein for improvement and for zero-shot prediction",
                "parameters": {
                "type": "object",
                "properties": {
                    "protein_name":{
                    "type": "string",
                    "description": "The name of the user input protein"
                    }
                },
                "required": ["protein_name"]
                }
            }
        }
        # {
        #     "type": "function", add more funtions here
        # },
    ],
    debug=DEBUG
)

funcs = [zero_shot_predict]

assistant = client.beta.assistants.update(
  assistant_id=assistant_id
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      'content': input("How can I help?")
    }
  ]
)

thread_id = thread.id
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant_id,
)

if run.status == 'completed':
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  if DEBUG:
    print(messages)
  print(messages.data[0].content[0].text.value)
else:
  if DEBUG:
    print(run.status)
 
  tool_outputs = []
  
  for tool in run.required_action.submit_tool_outputs.tool_calls:
    if tool.function.name == "get-protein-zero-shot":
      try:
        args = ast.literal_eval(tool.function.arguments)
        zero_shot_predict(args['protein_name'])
        tool_outputs.append({
          "tool_call_id": tool.id,
          "output": "success"
        })
      except:
        tool_outputs.append({
          "tool_call_id": tool.id,
          "output": "failed"
        })
    # elif tool.function.name == 'add more functions here'
    else:
      pass
  
  # Submit all tool outputs at once after collecting them in a list
  if tool_outputs:
    try:
      run = client.beta.threads.runs.submit_tool_outputs_and_poll(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
      )
      if DEBUG:
        print("Tool outputs submitted successfully.")
    except Exception as e:
      print("Failed to submit tool outputs:", e)
  else:
    print("No tool outputs to submit.")
  
  if run.status == 'completed':
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    print(messages.data[0].content[0].text.value)
  else:
    print('not completed')