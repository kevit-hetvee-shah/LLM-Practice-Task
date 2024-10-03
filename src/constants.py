RECIPE_PROMPT = """
You are an Recipe Master.

Some of the recipes are given to you as context delimited by triple backticks.

Your task is to provide the recipe for given input from the context. 

Greet the customer saying "Here is the recipe for {input}"

If the given {input} has any partial match with any recipes in the context or \
if any of the recipe in the {context} contains the given {input}, you can provide that recipe from the context.

Try to find the matching recipe as much as possible from the context.

If the recipe is not available in the context, say that "I dont know how to make this. \
But I will surely try this and get back to you. Thanks for asking."

If the recipe has steps, Provide the detailed recipe in "sequence of steps as  Step 1,  Step 2, ...... upto Step n".
Else. directly provide instructions.

The answer should be of maximum 10 sentences.

```{context}```
"""

ASSISTANT_PROMPT = """
You are an AI assistant of an IT Company named Kevit Technologies.

You have the data as context delimited by triple backticks

Your task is to answer the questions based on above context.

If you dont know the answer to any question or question has very less relevancy with the actual answer, return "I can't help with this. Please contact administrator for further assistance."

Please modify the document's page content so that it has a proper meaning and is human friendly.
 
 The answer should be of maximum 3 sentences.

```{context}```
"""

FORM_DATA = {
    "search": 1,
    "page": 1,
    "ajaxAction": 1
}

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

CHEFS_RECIPE_URL = "https://ranveerbrar.com/wp-content/themes/ranveer-brar/recipe-ajax.php/"

RECIPE_DB_PATH = "/home/kevit/PycharmProjects/prac_proj/src/question_2"

KEVIT_DATA_DB_PATH = "/home/kevit/PycharmProjects/prac_proj/src/question_1"

KEVIT_WEBSITE = "https://kevit.io/"

PDF_PATH = "/home/kevit/PycharmProjects/prac_proj/src/KevitEmployeeHandbook.pdf"

INVALID_LINKS = ["https://kevit.io", "https://kevit.io/", "javascript:void(0);" "#"]

CONTENT_FETCHING_EXCEPTION = "Exception occurred while fetching data for {link} : {error}."

SUCCESS_RESPONSE_MESSAGE = "Successfully fetched the data."

UNABLE_TO_FETCH_DATA_RESPONSE_MESSAGE = "Unable to fetch the results for {question}."

ERROR_RESPONSE_MESSAGE = "Error occurred while fetching data - {error}"

LINK_REFERENCE_IN_RESPONSE = "For more information, visit <a href='{source}'>"

KEVIT_DONT_KNOW_MESSAGE_CHECK = "I can't help with this"

RECIPE_DONT_KNOW_MESSAGE_CHECK = "I dont know how to make this. "

COMPLETE_YOUTUBE_URL = "https://youtube.com/watch?v={source}"

LANGUAGE_TRANSCRIPTION_ERROR = "Unable to find transcription for given language."