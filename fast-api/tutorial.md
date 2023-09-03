# Banco de dados SQL (Relacional) Assíncrono com Encode/Databases

> Este tutorial é uma tradução do tutorial oficial do FastAPI, que pode ser encontrado em: <a href="https://fastapi.tiangolo.com/pt/how-to/async-sql-encode-databases/" class="external-link" target="_blank">SQL Databases</a>.

Você também pode usar <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases`</a> com o **FastAPI** para se conectar a bancos de dados usando `async` e `await`.

É compatível com:

* PostgreSQL
* MySQL
* SQLite

Neste exemplo, usaremos o **SQLite**, porque ele usa um único arquivo e o Python tem suporte integrado. Portanto, você pode copiar este exemplo e executá-lo como está.

Mais tarde, para sua aplicação de produção, você pode querer usar um servidor de banco de dados como o **PostgreSQL**.


> Você pode adotar ideias da seção sobre SQLAlchemy ORM ([Bancos de dados SQL (Relacionais)](https://fastapi.tiangolo.com/pt/tutorial/sql-databases/)), como usar funções utilitárias para executar operações no banco de dados, independentemente do seu código **FastAPI**. Esta seção não aplica essas ideias, para ser equivalente à contraparte em <a href="https://www.starlette.io/database/" class="external-link" target="_blank">Starlette</a>.

## Importe e configure o `SQLAlchemy`

* Importe o `SQLAlchemy`.
* Crie um objeto `metadata`.
* Crie uma tabela `notes` usando o objeto `metadata`.

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

> Observe que todo esse código é puro SQLAlchemy Core. `databases` ainda não está fazendo nada aqui.

## Importe e configure o `databases`

* Importe o `databases`.
* Crie um `DATABASE_URL`.
* Crie um objeto `database`.

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

> Se você estivesse se conectando a um banco de dados diferente (por exemplo, PostgreSQL), precisaria alterar o `DATABASE_URL`.

## Crie as tabelas

Neste caso, estamos criando as tabelas no mesmo arquivo Python, mas na produção, você provavelmente gostaria de criá-las com o Alembic, integrado com migrações, etc.

Aqui, esta seção seria executada diretamente, logo antes de iniciar sua aplicação **FastAPI**.

* Crie um `engine`.
* Crie todas as tabelas a partir do objeto `metadata`.

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

## Crie modelos

Crie modelos Pydantic para:

* Notas a serem criadas (`NoteIn`).
* Notas a serem retornadas (`Note`).

```Python hl_lines="31-33  36-39"
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

Ao criar esses modelos Pydantic, os dados de entrada serão validados, serializados (convertidos) e anotados (documentados).

Portanto, você poderá ver tudo isso na documentação interativa da API.

## Conecte e desconecte

* Crie sua aplicação `FastAPI`.
* Crie manipuladores de eventos para conectar e desconectar do banco de dados.

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

## Leia as notas

Crie a *função de operação de caminho* para ler as notas:

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

> Observe que, como nos comunicamos com o banco de dados usando `await`, a *função de operação de caminho* é declarada com `async`.

### Observe o `response_model=List[Note]`

Ele usa `typing.List`.

Isso documenta (e valida, serializa, filtra) os dados de saída, como uma `list` de `Note`s.

## Crie notas

Crie a *função de operação de caminho* para criar notas:

```python
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

```

> Observe que, como nos comunicamos com o banco de dados usando `await`, a *função de operação de caminho* é declarada com `async`.

### Sobre `{**note.dict(), "id": last_record_id}`
`note` é um objeto Pydantic `Note`.

`note.dict()` retorna um `dict` com seus dados, algo como:

```python
{
    "text": "Alguma nota",
    "completed": False,
}
```

mas não tem o campo `id`.

Então, criamos um novo `dict`, que contém os pares de chave-valor de `note.dict()` com:

```Python
{**note.dict()}
```

`**note.dict()` "desempacota" os pares de chave valor diretamente, então, `{**note.dict()}` seria, mais ou menos, uma cópia de `note.dict()`.
E então, estendemos esse `dict` de cópia, adicionando outro par de chave-valor: `"id": last_record_id`:

```Python
{**note.dict(), "id": last_record_id}
```

Então, o resultado final retornado seria algo como:

```Python
{
    "id": 1,
    "text": "Alguma nota",
    "completed": False,
}
```

## Verifique

Você pode copiar este código como está e ver a documentação em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Lá você pode ver toda a sua API documentada e interagir com ela:

<img src="src/image01.png">

## Mais informações

Você pode ler mais sobre <a href="https://github.com/encode/databases" class="external-link" target="_blank">`encode/databases` no GitHub page</a>.
