from promptflow.core import tool, Prompty

# load and execute prompty
path_to_prompty =  "basic_chat.prompty"
flow = Prompty.load(path_to_prompty)

# execute the flow as function
result = flow(question=question)
print(result)

