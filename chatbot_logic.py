# Import necessary modules
import re
from langchain.llms import CTransformers
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask import session

# Initialize LangChain model and other necessary components
callback_manager = AsyncCallbackManager([AsyncCallbackHandler()])
callbacks = AsyncCallbackManager([StreamingStdOutCallbackHandler()])
config = {'max_new_tokens': 256, 'repetition_penalty': 1.1, 'temperature': 0.7, 'top_k': 50}
llm = CTransformers(model='TheBloke/orca_mini_v2_7B-GGML', config=config, model_type='llama',
                    callbacks_manager=callback_manager, verbose=True,
                    callbacks=callbacks)
template = """User: {input}\nAssistant: {output}"""
prompt = PromptTemplate(template=template, input_variables=["input", "output"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Function to process user messages using the chatbot
def process_user_message(user_input):
    # Flag to track user's choice
    user_choice = session.get('user_choice')

    if user_input.lower() == 'exit':
        return "Goodbye!"
    elif user_input.lower() == 'hi':
        session.pop('user_choice', None)  # Reset user choice
        return "Welcome to Lifelink bot. Enter 1 to perform disease prediction. Enter 2 to perform hospital recommendation. Enter 3 to perform Doctor recommendation. Enter 4 to get Donor details"
    elif user_choice is None:
        if user_input == '1':
            session['user_choice'] = 'disease_prediction'
            return "Enter the symptoms or disease name"
        elif user_input == '2':
            session['user_choice'] = 'hospital_recommendation_location'
            return "Enter the location or type '/location' to get your current location"
        elif user_input == '3':
            session['user_choice'] = 'doctor_recommendation_location'
            return "Enter the location or type '/location' to get your current location"
        elif user_input == '4':
            return "You can find donor details at the following link: <a href='https://www.friends2support.org/inner/news/searchresult.aspx' target='_blank'>List of Donors</a>"

        else:
            return "Invalid choice. Send 1 to perform disease prediction. Send 2 to perform hospital recommendation"
    elif user_choice == 'disease_prediction':
        response = llm_chain.invoke({'input': user_input, 'output': ""})
        return response['text']
    elif user_choice == 'hospital_recommendation_location':
        if user_input.strip().lower() == '/location':
            # Trigger location request logic here
            # For simplicity, let's assume the user grants permission and we get the location as 'current_location'
            user_input = 'current_location'
        session['location'] = user_input
        session['user_choice'] = 'hospital_recommendation_speciality'
        return "Enter the specialty (e.g., heart, kidney, etc.)"
    elif user_choice == 'hospital_recommendation_speciality':
        location = session.get('location')
        specialty = user_input
        session.pop('location', None)
        session.pop('user_choice', None)
        if location.lower() == 'current_location':
            # Here you can retrieve the user's current location and replace 'current_location' with the actual location
            location = "My Current Location"
        # Generate the Google search link based on location and specialty
        google_search_link = f"https://www.google.com/maps/search/{specialty}+hospitals+in+{location}"
        # Format the link as a clickable HTML anchor tag
        clickable_link = f'<a href="{google_search_link}" target="_blank">{specialty} hospitals in {location}</a>'
        return clickable_link
    elif user_choice == 'doctor_recommendation_location':
        if user_input.strip().lower() == '/location':
            # Trigger location request logic here
            # For simplicity, let's assume the user grants permission and we get the location as 'current_location'
            user_input = 'current_location'
        session['location'] = user_input
        session['user_choice'] = 'doctor_recommendation_speciality'
        return "Enter the specialty (e.g., heart, kidney, etc.)"
    elif user_choice == 'doctor_recommendation_speciality':
        location = session.get('location')
        specialty = user_input
        session.pop('location', None)
        session.pop('user_choice', None)
        if location.lower() == 'current_location':
            # Here you can retrieve the user's current location and replace 'current_location' with the actual location
            location = "My Current Location"
        # Generate the Google search link based on location and specialty
        google_search_link = f"https://www.google.com/maps/search/{specialty}+doctors+in+{location}"
        # Format the link as a clickable HTML anchor tag
        clickable_link = f'<a href="{google_search_link}" target="_blank">{specialty} doctors in {location}</a>'
        return clickable_link
