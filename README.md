# Forum API

Projeto de MVP realizado para o curso de Pós graduação em Engenharia de Software da PUC-Rio - Pontifícia Universidade Católica do Rio de Janeiro.  


## Sumário

- [Objetivo](#objetivo)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Forum](#forum)
- [Configuração e Instalação](#configuração-e-instalação)
	- [Utilizando o Docker compose](#utilizando-o-docker-compose)
	- [Utilizando somente o Docker](#utilizando-somente-o-docker)
- [Desenvolvimento](#desenvolvimento)
- [Queries](#queries)
- [Mutations](#mutations)


## Objetivo

Com o objetivo de difundir o conhecimento aos direitos e deveres dos brasileiros, esse projeto vem a oferecer um pesquisador de texto completo para a Constituição Federal de 1988.  

Também oferece uma sessão de fórum para artigos e comentários, sendo assim uma troca de conhecimento entre os usuários.  

Esse projeto é um MVP e pretende evoluir para que, tanto o pesquisador de texto quanto a sessão de artigos, possam desenvolver novas funcionalidades que irão melhorar a busca de texto e ampliar a sessão do fórum, para que usuários possam trocar conhecimento respondendo a comentários existentes, inserir outros conteúdos além de texto.  

Esse é um sistema implementado em micro serviços, sendo esse componente chamado de `Forum API`. O serviço `MVP2 Backend APP` faz a integração de todos os serviços. Para maiores informações ver os repositórios de [MVP2 Backend APP](https://github.com/lucas-rodrigues0/mvp2_backend_app) e [Full Text Searcher API](https://github.com/lucas-rodrigues0/full_text_searcher_api)


## Tecnologias

- [Python](https://www.python.org/)
- [Flask-openapi3](https://luolingchun.github.io/flask-openapi3/v3.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Strawberry](https://strawberry.rocks/docs)
- [Docker](https://docs.docker.com/)
- [Docker compose](https://docs.docker.com/compose/)


## Arquitetura

O sistema é composto por três APIs e um serviço externo (Auth0). São chamados de:
- MVP2_BACKEND_APP
- FULL_TEXT_SEARCHER_API
- FORUM_API
- Auth0 (serviço externo de Autenticação de usuários)

Os detalhes das componentes 'MVP2 Backend APP' e 'Full Text Searcher API' estão descritos em seus respectivos documentos. Sendo aqui apenas referenciados para melhor compreensão.  
O fluxograma apresentado no documento de 'MVP2 Backend APP' mostra as relações entre os componentes.

Também é utilizado um container postgres para o sistema de banco de dados. São necessários dois databases distintos. Um para o Forum API e outro para o Full Text Searcher API.  

Para o desenvolvimento é utilizado o Docker compose para orquestrar a construção e a inicialização dos containers de cada serviço. Mas caso for subir os serviços sem o Docker Compose, subir primeiro o container do postgres, pois ele será necessário para a inicialização do serviço de Full Text Searcher API. Na sessão de instalação há mais informação.  

Para a utilização do Docker Compose é importante ficar atento a estrutura de diretório a ser montada, para o docker compose fazer o build das imagens necessárias.

O arquivo `docker-compose.yml` incluído no repositório de 'MVP2 Backend APP' segue as instruções para a seguinte estrutura de diretório: 

```
.
├── database/
├── full_text_searcher_api/
├── mvp2_backend_app/
├── forum_api/
│   ├── graphql_api/
│   │   ├── __init__.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   ├── helper/
│   │   │   ├── __init__.py
│   │   │   └── helper.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py
│   │   │   ├── article_model.py
│   │   │   └── comment_model.py
│   │   ├── resolvers/
│   │   │   ├── __init__.py
│   │   │   ├── article_resolver.py
│   │   │   └── comment_resolver.py
│   │   ├── scalars/
│   │   │   ├── __init__.py
│   │   │   ├── article_scalar.py
│   │   │   └── comment_scalar.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── mutation_schema.py
│   │       └── query_schema.py
│   ├── api.py
│   ├── init_api.py
│   ├── insert_mock_data.py
│   ├── logger.py
│   ├── README.md
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml
```

O diretório `database` é criado através do docker compose como volume do container do postgres. A estrutura dos diretórios dos serviços `mvp2 backend app` e `full text searcher api` são apresentados em seus respectivos documentos.
O arquivo de docker-compose.yml deverá estar no diretório raiz junto com os diretórios de todos os serviços para que a orquestração possa fazer o build das respectivas imagens. 

## Forum

O serviço é uma Api GraphQL que apresenta artigos publicados pelos usuários. Os artigos possuem um título e um conteúdo de texto.  
Os usuários podem inserir um comentário a qualquer artigo e podem inserir um novo comentário em resposta a outro comentário.   
Um comentário resposta não poderá ser inserido a outro comentário que já é uma resposta, ele poderá ser inserido como resposta ao comentário referente ao artigo, permitido apenas três níveis de postagens demonstrado a seguir.  
```
Artigo 1
    ├── Comentário 1
    |       ├── Comentário de Resposta 1
    |       └── Comentário de Resposta 2
    └── Comentário 2
            └── Comentário de Resposta 3
```
As atualizações e remoções tanto do artigo quanto do comentário só poderão ser feitas pelo próprio usuário que as inseriu no banco de dados.
Ao remover um artigo, todos os comentários relacionados a esse artigo também serão removidos.
Os retornos das queries de leitura buscam trazer a relação de comentários e respostas aos artigos. Representado os níveis de postagem dentro do objeto retornado para manter o relacionamento das postagens. Artigo > Comentário > Comentário Resposta.

O serviço utiliza a biblioteca Strawberry para implementar a camada GraphQL. A biblioteca disponibiliza uma interface gráfica para a documentação das queries e mutations existentes, assim como dos Schema types. Também disponibiliza na interface gráfica o GraphQL Explorer para realizar testes com a API. Para acessar a interface, navegar para a rota `/graphql` no navegador.

## Configuração e Instalação

As variáveis API_PORT e DEBUG são opcionais para o desenvolvimento. No App é sugerido utilizar a porta 4444, mas caso queira trocar, alterar esse valor pela  variável é possível, mas será necessário alterar as portas no Dockerfile e docker-compose para as portas serem expostas corretamente.
A variável Debug é apenas para o desenvolvimento da aplicação Flask. Ele permite que o Flask rode em debug mode, e é realizado o auto reload quando há alteração de código.

Para a conexão com o banco de dados é necessário inserir os valores corretos no `.env`. Os valores no arquivo `.env-example` são uma sugestão:
```
PG_DATABASE=<nome do database a ser criado>
PG_USER=<usuário postgres>
PG_PASSWORD=<senha postgres>
PG_HOST=<nome do container postgres criado>
PG_PORT=<porta exposta pelo container postgres>
```

### Utilizando o Docker compose
É necessário ter instalado o [Docker](https://docs.docker.com/engine/install/) e o [Docker Compose](https://docs.docker.com/compose/install/) para subir os serviços automaticamente.  

O arquivo `docker-compose.yml` deverá ser movido para a raiz do projeto com a estrutura de diretórios de todos os serviços montada conforme descrito na seção [Arquitetura](#arquitetura). 

É necessário criar os arquivos `.env` para cada serviço. O arquivo `.env-example` pode ser copiado e preenchido com os valores corretos.

Execute o comando para fazer o build das imagens Docker e inicializar os container na ordem necessária.
```
docker compose up -d
```

Depois que subir todos os containers, pode acessar o endereço do serviço MVP2 Backend APP em seu navegador
```
http://127.0.0.1:5000/
```

Para acessar somente esse serviço:
```
http://127.0.0.1:4444/
```
Será automaticamente redirecionado para o explorer GraphQL do Strawberry no endpoint `/graphql`.


### Utilizando somente o Docker

É necessário ter instalado o [Docker](https://docs.docker.com/engine/install/).

É necessário criar os arquivos `.env` para cada serviço. O arquivo `.env-example` pode ser copiado e preenchido com os valores corretos.

> [!NOTE]  
> Caso ainda não tenha feito esses passos ao subir os outros serviços.

Para subir o ambiente sem o docker compose é importante criar uma network para que os serviços possam se conectar entre si.
Para criar uma network do tipo bridge com o nome de `app-network` execute o comando:
```
docker network create -d bridge app-network
```

Caso já tenha criado algum container, tipo o container db, e queira conectar esse container a network app-network, execute o comando:
```
docker network connect app-network db
```

Depois de criada a network, vamos subir um container com o banco postgres. O container terá o nome de 'db', estará conectado a network criada, a senha do postgres e o volume para a persistência dos dados.
execute os comandos:
```
docker pull postgres
docker run --name db --network app-network -e POSTGRES_PASSWORD=postgres -v ./database/postgres:/var/lib/postgresql/data -d postgres
```

Depois de iniciado o container do postgres podemos subir os outros containers em qualquer ordem.  
Para iniciar o serviço Forum API, primeiro temos que fazer o build da imagem.
Estando no mesmo nível em que o Dockerfile do forum_api se encontra, executar o comando:
```
docker build -t forum-api .
```
depois de construída a imagem podemos executar o container com o comando:
```
docker run --name forum-api -p 4444:4444 --network app-network -d forum-api
```
Para subir os outros serviços veja as informações em seus respectivos documentos.
Depois de subir os outros serviços da mesma forma, podemos testar o acesso através do MVP2 Backend APP no navegador pelo endereço.
```
http://127.0.0.1:5000/
```

Para acessar somente esse serviço:
```
http://127.0.0.1:4444/
```
Será redirecionado para o explorer GraphQL do Strawberry no endpoint `/graphql`.

## Desenvolvimento

Para o desenvolvimento pode ser necessário alguns dados mockados de artigos, comentários e comentários resposta.  
O script `insert_mock_data.py` consegue inserir alguns dados falsos no banco de dados.
Para executar o script dentro do container, rode o comando no seu terminal:
```
docker exec -it forum-api python insert_mock_data.py
```


## Queries

- #### articles
Parâmetros: None  
Busca lista de Artigos existentes no banco de dados.  
Retorna lista de scalars Article.  

- #### article_by_id
Parâmetros: article_id  
Busca Artigo pelo ID do parâmetro article_id.  
Retorna scalar Article.

- #### articles_by_user_id
Parâmetros: user_id  
Busca lista de Artigos pelo id do usuário que os inseriu.  
Retorna lista de scalars Article.  

- #### articles_by_period
Parâmetros: initial_date, end_date  
Busca lista de Artigos dentro do período que foram inseridos indicado nos parâmetros
initial_date e end_date.  
Retorna lista de scalars Article.  

- #### comments
Parâmetros: None  
Busca lista de Comentários existentes no banco de dados.  
Retorna lista de scalars Comment.  

- #### comment_by_id
Parâmetros: comment_id  
Busca Comentário pelo ID do parâmetro comment_id.  
Retorna scalar Comment.

- #### comment_by_user_id
Parâmetros: user_id  
Busca lista de Comentários pelo id do usuário que os inseriu.  
Retorna lista de scalars Comment.  

- #### comments_by_period
Parâmetros: initial_date, end_date  
Busca lista de Comentários dentro do período que foram inseridos indicado nos parâmetros
initial_date e end_date.  
Retorna lista de scalars Comment.  


## Mutations

- #### add_article
Parâmetros: user_id, user_email, user_nickname, title, content  
Adiciona novo Artigo ao banco de dados  
Retorna scalar AddArticle  

- #### remove_article
Parâmetros: article_id, user_id  
Remove Artigo indicado no parâmetro article_id criado pelo usuário com ID user_id.  
O usuário tem que ser o mesmo que inseriu o artigo.  
Retorna mensagem  

- #### update_article
Parâmetros: article_id, user_id, title, content  
Atualiza title e/ou content de um Artigo indicado no parâmetro article_id pelo usuário com ID user_id.  
O usuário tem que ser o mesmo que inseriu o artigo.  
Retorna scalar AddArticle  

- #### add_comment
Parâmetros: user_id, user_email, user_nickname, article_id, content, is_reply, comment_reply  
Adiciona novo Comentário ao banco de dados.  
Os parâmetros is_reply, comment_reply são opcionais e deverão ser usados se o comentário for uma resposta a outro comentário.  
Retorna scalar AddComment  

- #### remove_comment
Parâmetros: comment_id, user_id  
Remove Comentário indicado no parâmetro comment_id criado pelo usuário com ID user_id.  
O usuário tem que ser o mesmo que inseriu o comentário.  
Retorna mensagem  

- #### update_comment
Parâmetros: comment_id, user_id, content  
Atualiza o content de um Comentário indicado no parâmetro comment_id pelo usuário com ID user_id.  
O usuário tem que ser o mesmo que inseriu o comentário.  
Retorna scalar AddComment  
