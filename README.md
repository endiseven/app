# Lab App FastApi - Characters Database

A very simple api to read, write and delete fictional characters at a database.

Initial Table:
```json
{
        "id": 1,
        "name": "Neo",
        "story": "Matrix"
    },
    {
        "id": 2,
        "name": "Frodo",
        "story": "Lord Of The Rings"
    },
    {
        "id": 3,
        "name": "Goku",
        "story": "Dragon Ball"
}
```

# How to test it

Download docker-compose.yml

With Docker installed in the system...

Run ``` docker-compose up ``` to download the already configured images of the FastApi and Mysql.

(fast Api might start before mysql database is completely running, in that case, just re run ``` docker-compose up ```)

Acces the server at:

```
http://localhost:8000/characters/
```

## Try something like:

#### Add a character
```
curl -X POST http://localhost:8000/characters/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Darth Vader","story":"Star Wars"}'\
```
#### Delete a character
```
curl -X DELETE http://localhost:8000/characters/"id"
```



