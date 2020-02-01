# flask-api-with-docker-db
API em flask utilizando container docker para executar uma instância do PostgreSQL

#### Criando container docker do PostgreSQL 

* docker run --name database -e POSTGRES_PASSWORD= password -p 5432:5432 -d postgres

#### Configuração do banco de dados com SQLAlchemy

* USER_DB = POSTGRES_USER
* PASSWORD_DB = POSTGRES_PW
* URL_DB = POSTGRES_URL
* DB = POSTGRES_DB
* DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'

* app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
