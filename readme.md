# Basic Design
This project is a demonstration of Retrieval Augmented Generation (RAG). Retrieval-augmented generation is a technique 
used in natural language processing that combines the power of both retrieval-based models and generative models 
to enhance the quality and relevance of generated text. We first retrieve information relevant to a property from
the database. Then, the retrieved information is used as additional context for the generative model to answer
user's question.

By incorporating the retrieved information, the generative model can leverage the accuracy and specificity of the 
retrieval-based model to produce more relevant and accurate text. It helps the generative model to stay grounded 
in the available knowledge and generate text that aligns with the retrieved information.
## Technical Details
Considering the description provided earlier about the app (a simple RAG application), the lightweight and rapid 
development nature of both SQLite and Flask align well with the app's requirements.

We use SQLite for database and Flask for web app development. First of all, the script `create_db.py` should be 
executed to generate a SQLite database called `test.db`. It will contain the database `properties` containing
two columns `address`, the address of the property, and `description`, description of the property. By default, 
the database contains following record:

| address | description |
|---------|-------------|
|123 Main Street|A 3-bedroom house, the price is 568,000 dollars|

Then we launch the Flask app by executing script `app.py`.

The Flask app will take the POST operation from Postman or browser. The request body take the form:
````
{
"question": "How many rooms does the house at 123 Main Street have?"
}
````
The screenshot of Postman:
![postman](/postman.png)
The Flask application then parse the request body and extract the user's question. Then, the address is extracted 
from the question by regex pattern `\b[0-9]+\s([A-Z][A-Za-z]+)+(\s[A-Z][A-Za-z]+)*\b` i.e. an expression starting with
street number and street name starting with capital letters. This is in compliance with most address format.
The address is then queried in SQLite database and 
get the description for the address. Then we compose the prompt for OpenAI by combining the description of the
property and the user's question. Response from OpenAI api will be return and looks like:
````
{
"response": "The house at 123 Main Street has 3 bedrooms."
}
````

# Further Design
## Design for Scalability
The code is merely a demonstration of basic functionality. In production scenario, the throughput is much higher, possibly thousands of QPS. 
We must take measures to make the application highly scalable. Here are some strategies we can take:

### Load Balancing: 
Deploy multiple instances of Flask app and use a load balancer (like NGINX, HAProxy, or AWS Elastic Load Balancing)
to distribute incoming requests among these instances.

### Stateless Design: 
Ensure the Flask app to be stateless, which means it shouldn't rely on local cache or data storage. A stateless 
design makes it easier to scale horizontally.

### Database Scalability:

#### Connection Pooling: 
Use a connection pool to maintain and reuse database connections. 
#### Read Replicas: 
If most of the database operations are reads (which is the case here), consider using read replicas to distribute 
the load.
#### In-Memory Caching: 
Use caching solutions like Redis or Memcached to cache frequent database lookups or OpenAI API responses.

### Asynchronous Processing:
This application involves calling ChatGPT's API, which can be time-consuming and error-prone. It is necessary to 
use message queue to decouple the main app and api processing. Message queue like RabbitMQ and distributed task 
queue like Celery can be feasible solution. In high-concurrency scenarios, we can spawn multiple Celery workers 
across different machines to increase throughput. It also lets the main application remain responsive, even if 
the external API is slow or rate-limited.

## Fuzzy Search
The application involves two text processing phases. First of all, the address should be extracted from user's 
question. Second, the extracted address should be queried from the database to find its description. The basic 
design is using regex to extract the address and query database. This exact match is fine in the demo case, but
in real scenario, user's question may contain typo or other textual errors. Therefore, it is necessary to perform
 fuzzy search. 
### Address Extraction
#### 3rd Party Library
Libraries like `Spacy` or `NLTK` can help parse and identify named entities within text. When 
trained on the right datasets, they can identify addresses or address components with a higher accuracy rate than 
regex alone. Commercial platforms like Google's Cloud Natural Language API or Amazon Comprehend also offer entity 
extraction, which can sometimes recognize address components. Libraries like `usaddress` (for US addresses) can 
break down an address into its components, such as street number, street name, city, etc. This might not extract 
addresses from sentences, but if you have a probable address string, it can help in breaking it down.
#### Rule-based System 
For certain domains, there might be specific cues or patterns (e.g., "located at", "address is", etc.) that often 
precede or follow an address. A rule-based system can use these cues in conjunction with other methods to extract 
addresses.
#### Customed Model
If we have cumulated a substantial amount of data, we could consider training our own model to 
recognize and extract addresses from text. Deep learning architectures, especially those based on 
transformer models like BERT, have been successful in named entity recognition tasks.
### Database Query
#### Database Built-in Fuzzy Search
Many databases have built-in support for full-text search and fuzzy matching:
* PostgreSQL: It has the `pg_trgm` module which supports trigram-based search. Once you enable this module, we can use 
functions like similarity and operators like `%` to perform fuzzy matches.
* SQLite: The FTS (Full Text Search) extension in SQLite allows for full-text searches, which can approximate fuzzy
searching.
* MySQL: MySQL's `LIKE` and `ILIKE` can be used, but for more sophisticated fuzzy search, consider integrating with an
external service or library.
#### ElasticSearch
Elasticsearch is a distributed search engine that excels at full-text search. We can set up an Elasticsearch index
for addresses and then use its fuzzy query capabilities.