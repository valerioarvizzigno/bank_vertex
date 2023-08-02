# GenAI FSI demo with Elastic Vector Search (ESRE) and Google's VertexAI
FS Demo with ESRE and Google's GenAI

Data source used:
- Your favourite bank website, web-crawled via Elastic Enterprise Search --> used for general information queries on elastibank_home.py
- Public bank contracts / documentations (see a pdf example in datasets folder) --> used for contract summarization/domain specific queries on elastibank_contract.py
- Credit card Transactions dataset (like the csv in the datasets folder) --> used for transaction analysis in elastibank_transcations.py


Queries for the elasticbank_home page:

- List the type of bank accounts you offer. Specify details for each of these

- list the account types you are offering in bullet points with their key features

- Do you offer car loans? If yes describe their rates and details

- What information do you need to properly support me in transaction dispute?

For the elasticbank_contract page:

- How much does it cost to receive a wire transfer in dollar from the US in my italian bank account?

- Please list all the related fees and clauses of transferring money from an US dollar bank account to an italian euro bank account

- Could you please list in bullet points the economic conditions for SEPA wire transfers?

for the elasticbank_transactions try those questions:

- Sum all of my spending in transportation last month and List all the related transactions in bullet points
- List with bullet points all the food and drink transactions. Underline the ones greater than 20 dollars
- Which transactions are food related? List them in bullet points
- Have I spent any money for drugs? If yes how much?
- What's the highest electricity bill I had? Can you please list all the information about this transaction?

Check valerioarvizzigno/homecraft_vertex repo for installation guide. It's the same for both