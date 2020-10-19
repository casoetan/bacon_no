# Brief Explanation

Requires Python version 3.8.6

## The application tools

- FastAPI for the API Service framework

- SQLAlchemy as an ORM for queries

- SQLite as the database backend

- UVICorn for running the application

- Poetry for installing dependencies

## Folder structure

- `bacon_number/`

  - `api.py`: API service
  - `graph.py`: Fetches data from the database, parses it and stores parsed data in-memory
  - `models.py`: Database structure and model

- `dataset/`: CSV Data from Kaggle is stored here

- `process_data.py`: Reads the kaggle `csv` files, parses and stores in an `SQLite` database named `bacon.sql`

- `pyproject.toml`, `poetry.lock`: Poetry generated files

- `.env.example`: Stores sample environment variables. A default is specified

## Running the project

- Download and extract [Kaggle dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) into the dataset directory

- Install [Poetry](https://python-poetry.org/). Installation instruction for
different systems available [Poetry Installation](https://python-poetry.org/docs/#installation)
  - If using unix like system including macOS:
    - `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

- To install application dependencies run
  - `poetry install`

- To setup application database and import credits / actors data into the database, run
  - `python process_data.py`

- To start the application run
  - `uvicorn bacon_number.api:app`

## Browsing the application

- Go to `http://127.0.0.1:8000/actors/Pierce` to get artist whose name has the word `Pierce`.

- API endpoint returns at most 10 records. Select the ID of one of the records.

- As an example if we select the ID for Pierce Brosnan (`517`), we can find out his degree / bacon number by navigating to
  - `http://127.0.0.1:8000/degrees/517`

- If we want to compare Pierce Brosman (`517`) to Tom Hanks (`31`). Navigate to

  - `http://127.0.0.1:8000/degrees/517?degrees_to=31`
