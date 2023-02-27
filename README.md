
# Naruto-API

API who have info about the well know Naruto anime.
It contains infos about all sagas (Naruto, Naruto Shippuden, ..)


## Features

- Easy to use
- Reactive and fast
- Get infos about all the characters of the saga Naruto
- Get info about the categories of characters
- 2 languages (EN - FR)


## Installation

First, clone the repo locally

```bash
  cd naruto-api/
  pip install -r requirements.txt
  python manage.py character
  python manage.py categories
```

The last lines are to import the data\
Data is imported by scraping the famous fan wiki of Naruto (Thanks to Fandom wiki).

And finally : 

```bash
  python manage.py runserver
```


## API Reference

#### Get all characters (EN - FR)

```http
  GET /v1/{fr-en}/characters
```

#### Get one character (EN - FR)

```http
  GET /v1/{fr-en}/characters/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of the character |

#### Get all categories (FR)

```http
  GET /v1/fr/categories
```

#### Get one category (FR)

```http
  GET /v1/fr/categories/{id}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of the category |

