from langchain.llms import CTransformers

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
callback_manager = AsyncCallbackManager([AsyncCallbackHandler()])
callbacks = AsyncCallbackManager([StreamingStdOutCallbackHandler()])

#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

config = {'max_new_tokens': 256, 'repetition_penalty': 1.1, 'temperature': 0.7, 'top_k': 50}
# Initialize LangChain model
llm = CTransformers(model='TheBloke/orca_mini_v2_7B-GGML', config=config, model_type='llama',
                    callbacks_manager=callback_manager, verbose=True,
                    callbacks=callbacks)

# Define a template for conversation prompts
template = """User: {input}

Assistant: {output}"""

prompt = PromptTemplate(template=template, input_variables=["input", "output"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

def chatbot():
    print("Welcome to the Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = llm_chain.invoke({'input': user_input, 'output': ""})
        print("Chatbot:", response['text'])


# Start the chatbot
chatbot()
