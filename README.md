# Fast Query Store :zap:

## Running locally
You need `python`, `git`, `docker` and `docker-compose` to run this project.

### Setup
```
git clone <repository-url>
cd fast-query-store
cp env.example .env
source .env
```
#### Install dependencies
```
python -m venv env
source env/bin/activate

pip install -r requirements.txt
```

#### Export config variables
**fast-query-store** will look for a `.json` file containing the queries information. The environment variable `queries_file_path` tells where this file is located.
```
export queries_file_path=/path/to/queries.json
```

Example of **queries.json** file
```json
{
    "slug-1": {
        "query": "SELECT * FROM table_1",
        "db_url": "postgresql:///..."
    },
    "slug-2": {
        "query": "SELECT COUNT(1) FROM table_1",
        "db_url": "sqlite:///..."
    },
    "slug-3": {
        "query": "SELECT * FROM table_3",
        "db_url": "${DATABASE_URL}"
    }
}
```
**Note:** It is also possible to set the `db_url` with a enviroment variable.

#### Running it
```
export queries_file_path=queries.json
uvicorn app.main:app --workers 2 --host 0.0.0.0 --port 8000
```

### Getting available query slugs
```
GET http://localhost:8000/
```

```http
HTTP/1.1 200 OK
content-length: 73
content-type: application/json
date: Fri, 14 May 2021 12:47:37 GMT
server: uvicorn

{
    "slugs": [
        "slug-1",
        "slug-2",
        "slug-3"
    ]
}
```

### Executing a query

```
GET http://localhost:8000/query/slug-1
```

```http
HTTP/1.1 200 OK
content-length: 151
content-type: application/json
date: Fri, 14 May 2021 12:53:09 GMT
server: uvicorn

{
    "result_set": [
        {
            "name": "Cheese",
            "price": 9.99,
            "product_no": 1
        },
        {
            "name": "Bread",
            "price": 1.99,
            "product_no": 2
        },
        {
            "name": "Milk",
            "price": 2.99,
            "product_no": 3
        }
    ]
}
```

## Running the tests
```
pip install -r requirements-development.txt
source .env
docker-compose f docker-compose.yml up -d
pytest -v
```
