# Sistema de Locadora de Filmes

## Instalação

### 1. Clonar o projeto

```bash
git clone URL_DO_REPOSITORIO
cd projeto-flask
```

### 2. Criar a virtual environment

No Windows:

```powershell
python -m venv venv
```

Ative a virtual environment:

```powershell
.\venv\Scripts\activate
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

```text
(venv) PS C:\...\projeto-flask>
```

### 3. Instalar as dependências

Com a virtual environment ativada:

```powershell
pip install -r requirements.txt
```

## Configuração do banco de dados

O projeto utiliza **MySQL** como banco de dados.

É necessário ter o MySQL instalado e em execução. O banco pode ser criado utilizando o MySQL Workbench.

### 4. Criar o banco

No MySQL Workbench, execute:

```sql
CREATE DATABASE locadora;
```

Para verificar:

```sql
SHOW DATABASES;
```

O banco `locadora` deverá aparecer na lista.

### 5. Configurar as variáveis de ambiente

Na raiz do projeto, crie um arquivo chamado `.env`.

Utilize o `.env.example` como referência.

Exemplo:

```env
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost/locadora
```

Substitua `SUA_SENHA` pela senha do usuário `root` do seu MySQL.

Exemplo:

```env
DATABASE_URL=mysql+pymysql://root:marcelha@localhost/locadora
```

> O arquivo `.env` não deve ser enviado para o Git, pois pode conter informações sensíveis, como a senha do banco de dados.

## Configuração das tabelas

As migrations do projeto já estão versionadas no Git dentro da pasta `migrations/`.

Por isso, após clonar o projeto, **não é necessário executar `flask db init` nem `flask db migrate`**.

### 6. Aplicar as migrations

Execute:

```powershell
flask db upgrade
```

Esse comando aplica as migrations existentes ao banco `locadora` e cria as tabelas necessárias.

Para verificar no MySQL:

```sql
USE locadora;

SHOW TABLES;
```

A tabela `clientes` deverá estar presente.

Para verificar sua estrutura:

```sql
DESCRIBE clientes;
```

A tabela deverá possuir os campos:

```text
id
nome
cpf
email
telefone
```

## Executar a aplicação

### 7. Iniciar o servidor

Com a virtual environment ativada:

```powershell
python run.py
```

A aplicação será iniciada em:

```text
http://127.0.0.1:5000
```

## Testando a API

Os endpoints podem ser testados utilizando ferramentas como Postman, Insomnia ou Thunder Client.

### Health Check

Verifica se a aplicação está funcionando:

```http
GET http://127.0.0.1:5000/health
```

Resposta:

```json
{
    "status": "ok"
}
```

Status:

```text
200 OK
```

---

# API de Clientes

A API possui operações de criação, consulta, atualização e remoção de clientes.

## Criar cliente

```http
POST http://127.0.0.1:5000/api/clientes
```

Body:

```json
{
    "nome": "Guilherme",
    "cpf": "12345678901",
    "email": "guilherme@email.com",
    "telefone": "41999999999"
}
```

Resposta esperada:

```json
{
    "id": 1,
    "nome": "Guilherme",
    "cpf": "12345678901",
    "email": "guilherme@email.com",
    "telefone": "41999999999"
}
```

Status:

```text
201 Created
```

## Listar clientes

```http
GET http://127.0.0.1:5000/api/clientes
```

Resposta:

```json
[
    {
        "id": 1,
        "nome": "Guilherme",
        "cpf": "12345678901",
        "email": "guilherme@email.com",
        "telefone": "41999999999"
    }
]
```

Status:

```text
200 OK
```

## Buscar cliente por ID

```http
GET http://127.0.0.1:5000/api/clientes/1
```

Resposta:

```json
{
    "id": 1,
    "nome": "Guilherme",
    "cpf": "12345678901",
    "email": "guilherme@email.com",
    "telefone": "41999999999"
}
```

Status:

```text
200 OK
```

## Atualizar cliente — PUT

O `PUT` substitui os dados do cliente. Todos os campos obrigatórios devem ser enviados.

```http
PUT http://127.0.0.1:5000/api/clientes/1
```

Body:

```json
{
    "nome": "Guilherme Sanchez",
    "cpf": "12345678901",
    "email": "guilherme.sanchez@email.com",
    "telefone": "41988888888"
}
```

Status:

```text
200 OK
```

## Atualizar cliente — PATCH

O `PATCH` permite alterar apenas os campos desejados.

```http
PATCH http://127.0.0.1:5000/api/clientes/1
```

Body:

```json
{
    "telefone": "41977777777"
}
```

Status:

```text
200 OK
```

## Remover cliente

```http
DELETE http://127.0.0.1:5000/api/clientes/1
```

Resposta:

```json
{
    ""
}
```

Status:

```text
204 NO CONTENT
```

# API de Categorias

A API possui operações de criação, consulta, atualização e remoção de categorias.

## Criar categoria

```http
POST http://127.0.0.1:5000/api/categorias
```

Body:

```json
{
    "nome": "Ficção Científica",
}
```

Resposta esperada:

```json
{
    "id": 1,
    "nome": "Ficção Científica"
}
```

Status:

```text
201 Created
```

## Listar categorias

```http
GET http://127.0.0.1:5000/api/categorias
```

Resposta:

```json
[
    {
        "id": 1,
        "nome": "Ficção Científica"
    }
]
```

Status:

```text
200 OK
```

## Buscar categoria por ID

```http
GET http://127.0.0.1:5000/api/categorias/1
```

Resposta:

```json
{
    "id": 1,
    "nome": "Ficção Científica"
}
```

Status:

```text
200 OK
```

## Atualizar categoria — PUT

O `PUT` substitui os dados da categorias. Todos os campos obrigatórios devem ser enviados.

```http
PUT http://127.0.0.1:5000/api/categorias/1
```

Body:

```json
{
    "nome": "Ação"
}
```

Status:

```text
200 OK
```

## Atualizar categoria — PATCH

O `PATCH` permite alterar apenas os campos desejados.

```http
PATCH http://127.0.0.1:5000/api/categorias/1
```

Body:

```json
{
    "nome": "Aventura"
}
```

Status:

```text
200 OK
```

## Remover categoria

```http
DELETE http://127.0.0.1:5000/api/categorias/1
```

Resposta:

```json
{
    ""
}
```

Status:

```text
204 NO CONTENT
```

# Tratamento de erros

As API's possuem tratamentos centralizados de erros através do arquivo `errors.py`.

## Erro de validação — 422

Exemplo de payload inválido:

```json
{
    "nome": "G",
    "cpf": "123",
    "email": "email-invalido",
    "telefone": "123"
}
```

Resposta:

```json
{
    "code": 422,
    "name": "Unprocessable Entity",
    "description": "Falha na validação do payload.",
    "errors": {
        "nome": [
            "Length must be between 2 and 100."
        ]
    }
}
```

Status:

```text
422 Unprocessable Entity
```

## Cliente não encontrado — 404

```http
GET http://127.0.0.1:5000/api/clientes/9999
```

Resposta:

```json
{
    "code": 404,
    "name": "RecursoNaoEncontrado",
    "description": "Cliente 9999 não encontrado."
}
```

Status:

```text
404 Not Found
```

## CPF duplicado — 409

Ao tentar cadastrar um cliente utilizando um CPF que já está cadastrado:

```json
{
    "nome": "Outro Cliente",
    "cpf": "12345678901",
    "email": "outro@email.com",
    "telefone": "41966666666"
}
```

Resposta:

```json
{
    "code": 409,
    "name": "RegraDeNegocio",
    "description": "CPF já cadastrado."
}
```

Status:

```text
409 Conflict
```

## E-mail duplicado — 409

Ao tentar cadastrar um cliente utilizando um e-mail que já está cadastrado:

```json
{
    "nome": "Outro Cliente",
    "cpf": "98765432100",
    "email": "guilherme@email.com",
    "telefone": "41966666666"
}
```

Resposta:

```json
{
    "code": 409,
    "name": "RegraDeNegocio",
    "description": "E-mail já cadastrado."
}
```

Status:

```text
409 Conflict
```

# Resumo dos endpoints

| Método | Endpoint              | Descrição                        | Status |
| ------ | --------------------- | -------------------------------- | ------ |
| GET    | `/health`             | Verifica o funcionamento da API  | 200    |
| GET    | `/api/clientes`       | Lista todos os clientes          | 200    |
| GET    | `/api/clientes/{id}`  | Busca um cliente por ID          | 200    |
| POST   | `/api/clientes`       | Cria um novo cliente             | 201    |
| PUT    | `/api/clientes/{id}`  | Substitui os dados do cliente    | 200    |
| PATCH  | `/api/clientes/{id}`  | Atualiza parcialmente o cliente  | 200    |
| DELETE | `/api/clientes/{id}`  | Remove um cliente                | 200    |
| GET    | `/api/categorias`     | Lista todas as categorias        | 200    |
| GET    | `/api/categorias/{id}`| Busca uma categoria por ID       | 200    |
| POST   | `/api/categorias`     | Cria uma nova categria           | 201    |
| PUT    | `/api/categorias/{id}`| Substitui os dados da categoria  | 200    |
| PATCH  | `/api/categorias/{id}`| Atualiza parcialmente a categoria| 200    |
| DELETE | `/api/categorias/{id}`| Remove uma categoria             | 200    |

## Fluxo para executar o projeto após o clone

Em resumo:

```text
git clone
    ↓
cd projeto
    ↓
python -m venv venv
    ↓
.\venv\Scripts\activate
    ↓
pip install -r requirements.txt
    ↓
CREATE DATABASE locadora
    ↓
criar arquivo .env
    ↓
flask db upgrade
    ↓
python run.py
    ↓
testar as APIs
```

> **Observação:** `flask db init` e `flask db migrate` são comandos utilizados durante o desenvolvimento para criar e gerar novas migrations. Como as migrations atuais já estão versionadas no Git, quem apenas clonar e executar o projeto deve utilizar `flask db upgrade`.
