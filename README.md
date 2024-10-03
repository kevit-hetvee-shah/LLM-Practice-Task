**Question 1:** You need to develop an application that includes APIs to accomplish the following tasks:
Scrape the content of
this [PDF](https://adminkevit-my.sharepoint.com/personal/darshit_mehta_botprosolutions_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fdarshit%5Fmehta%5Fbotprosolutions%5Fcom%2FDocuments%2Fgenerative%20AI%2FKevit%2FKevit%20Employee%20Handbook%2Epdf&parent=%2Fpersonal%2Fdarshit%5Fmehta%5Fbotprosolutions%5Fcom%2FDocuments%2Fgenerative%20AI%2FKevit&ga=1)
and crawl the website [kevit.io](https://kevit.io/) using an API.
Create another API that retrieves and provides answers based on the extracted data from both the PDF and the website.

Expected outcomes:

1. Build a Flask or FastAPI application with APIs to store and retrieve the data.
2. Use Google models to implement Retrieval-Augmented Generation (RAG).
3. When answers are sourced from the website, include the website's URL in the response using an anchor tag.
4. Ensure the responses are designed to behave like Kevit's AI Assistant by utilizing effective prompt engineering
   techniques.
5. Ensure the bot doesn't answer questions outside the defined scope.

**Question 2:** Using the existing application, create an additional endpoint to scrape YouTube videos (around 12) from
the [Ranveer Brar website](https://ranveerbrar.com/), and have the bot provide answers based on the scraped content.

Expected outcomes:

1. Build a Flask or FastAPI application that includes APIs for storing and retrieving the data.
2. Use Google models to implement Retrieval-Augmented Generation (RAG).
3. When the answer requires step-by-step instructions, ensure the bot delivers it in that format.
4. Include the YouTube video link in the response using an anchor tag.
5. Employ prompt engineering to make the bot behave like a "Recipe Master."
6. Ensure the bot doesn't answer questions outside the defined scope.
