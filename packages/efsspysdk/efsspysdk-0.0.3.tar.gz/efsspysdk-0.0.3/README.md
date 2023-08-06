# Lord of the Rings SDK

# Requiriments
Python >= 3.9

# Installation
To install this SDK, execute the following command in your terminal:

```bash
pip install efsspysdk
```

To use this SDK, you need an access token. Generate it by creating an account [here](https://the-one-api.dev/sign-up).

Once you have obtained your access token, set it as an environment variable in your terminal. In the project's root folder, execute the following command:

```bash
 source ./setup-token your-token-here
```

Alternatively, if you prefer or encounter any issues, manually export the environment variable:

```bash
export API_KEY=your-token-here
```

# How to use

The SDK provides two available agents: Movie for movie requests and Quote for quotes. In your code, import the desired agents from the previously installed package:

```python
from efsspysdk import Movie, Quote
```

## Movie agent
Regarding the Movie agent, it offers the following methods:

Method: `list()`
Response: Retrieves a list of all movies, including "The Lord of the Rings" and "The Hobbit" trilogies.
Example:

```python
movie = Movie()
movie.list()
```

or

```python
Movie().list()
```

Method: `get(movie-id)`
Response: Requests information for a specific movie.
Example:

```python
movie = Movie()
movie.get(movie_id)
```

or

```python
Movie().get(movie_id)
```

Method: `list_quotes(movie-id)`
Response: Requests all movie quotes for a specific movie (only working for the LotR trilogy).
Example:

```python
movie = Movie()
movie.list_quotes(movie_id)
```

or

```python
Movie().list_quotes(movie_id)
```


## Quote agent
The Quote agent provides the following methods:

Method: `list()`
Response: Retrieves a list of all movie quotes.
Example:

```python
quote = Quote()
quote.list()
```

or

```python
Quote().list()
```

Method: `get(movie-id)`
Response: Requests a list of all movie quotes for a specific movie.
Example:

```python
quote = Quote()
quote.get(movie-id)
```

or

```python
Quote().get(movie-id)
```

## Filters
In all methods, it is possible to filter only specific fields from the response JSON. To do this, you can include them as a list in the method call. For example:
```python
movie.list(['name', 'academyAwardNominations', 'academyAwardWins'])
```
This will return a list of movies with only the three attributes listed: name, academyAwardNominations, and academyAwardWins.

![example image](https://github.com/hatchways-community/ca1434b835654bed8ccf91f5b5e42a3b/blob/dev/images/list-filter.png)

Specifically for certain calls:
```python
quote.get('5cd96e05de30eff6ebccebd0', ['dialog'])
```
This will retrieve a specific quote with only the 'dialog' field included in the response.

![example image](https://github.com/hatchways-community/ca1434b835654bed8ccf91f5b5e42a3b/blob/dev/images/get-dialog.png)

Using these filters allows you to retrieve specific fields of interest, providing a more focused and efficient way of working with the data.

You can execute the unit tests by running the following command in the root directory of the repository:
```bash
pytest
```
This command will run the unit tests and provide feedback on their success or any encountered failures.

If you want to see an example, you can execute the script `example.py` in the root directory of this repository by running the following command:

```bash
python example.py
```

I hope you have a great experience! If you have any further questions, feel free to ask. 😊

```
Hello LibLab!

I hope you're doing well, my friend! My name is Emmanuel, and I'm thrilled to be participating in this test to become your new DevOps Engineer. I absolutely love challenges like this, and I'm always excited to give my best shot. Unfortunately, with the limited time of 6 hours, I couldn't take care of every detail as I usually do, such as complete unit testing, improving folder structure, and validating most parameters. However, I believe this test showcases my understanding of Python and SDKs.

If you're curious to see more, feel free to check out other projects on my GitHub and my LinkedIn page, where you can explore my journey so far (links are provided below)!
Best,
See ya soon!
```

[Linkedin](https://www.linkedin.com/in/emmanuel-felipe/)
[GitHub](https://github.com/EmmanuelFelipe)