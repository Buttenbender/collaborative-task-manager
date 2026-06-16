# Collaborative Task Manager
## Autores
- João Büttenbender
- Eduardo Razera
- Diogo Belotto
## Visão Geral
### Objetivo do Sistema
O Collaborative Task Manager é uma API RESTful desenvolvida para o gerenciamento colaborativo
de tarefas entre usuários. O sistema permite que equipes criem, editem, atribuam e acompanhem
tarefas de forma estruturada, oferecendo funcionalidades complementares como controle de permissões
por papéis, comentários em tarefas e integração com o Google Calendar.
### Contexto de Uso
A API destina-se a times e equipes que necessitam de uma solução centralizada para organização
e acompanhamento de tarefas. Por meio de requisições HTTP, clientes externos - como aplicações
web, mobile ou ferramentas de integração - podem interagir com o sistema para:

- Gerenciar usuários e seus perfis com controle de acesso por papéis (Administrador, Usuário e Convidado)
- Criar e atribuir tarefas com datas, responsáveis e status de acompanhamento
- Controlar o ciclo de vida das tarefas (pendente, em andamento, concluida)
- Registrar comentários vinculados a tarefas específicas
- Sincronizar tarefas com o Google Calendar por meio de integração OAuth 2.0
- Aplicar restrições de acesso de acordo com o papel do usuário no sistema

Toda a comunicação com a API é protegida por autenticação via token JWT, garantindo que apenas
usuários autenticados possam realizar operações.
### Instruções de Instalação
#### Pré-requisitos
- Python 3.11+
- Docker Desktop
- Git
#### Instalação com Docker
1. Clonar o repositório
```
git clone https://github.com/Buttenbender/collaborative-task-manager.git
cd collaborative-task-manager
```
2. Configurar as variáveis de ambiente

Copie o arquivo `.env.example` e renomeie para `.env`, preenchendo os valores:
```
cp .env.example .env
```
```
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@db:3306/collaborative_task_manager
SECRET_KEY=SUA_CHAVE_SECRETA
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MYSQL_ROOT_PASSWORD=SUA_SENHA
MYSQL_DATABASE=collaborative_task_manager
GOOGLE_CLIENT_ID=SEU_CLIENT_ID
GOOGLE_CLIENT_SECRET=SEU_CLIENT_SECRET
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```
3. Subir os containers
```
docker-compose up --build
```
4. Inserir os dados iniciais
```
docker exec -it collaborative_task_manager_db mysql -u root -p
```
Execute os seguintes comandos SQL:
```
USE collaborative_task_manager;

INSERT INTO roles (name) VALUES ('admin'), ('user'), ('guest');
INSERT INTO statuses (name) VALUES ('pending'), ('in_progress'), ('done');
```
5. Acessar a documentação da API

Acesse `http://localhost:8000/docs` no navegador

## Decisões Arquiteturais
### Linguagem e Framework - Python com FastAPI
O Python foi escolhido pela sua leitura fácil, grande quantidade de bibliotecas e ampla
adoção no desenvolvimento de APIs. O FastAPI foi adotado como framework por ser moderno, 
de alto desempenho e por gerar automaticamente a documentação iterativa via Swagger/OpenAPI.
A integração nativa com Pydantic garante a validação de dados de entrada e saída da API.
### Banco de Dados - MySQL
O MySQL foi escolhido por ser um banco de dados relacional maduro, com suporte consolidado para
integridade referencial, chaves estrangeiras e transações ACID. A natureza relacional do domínio - 
onde usuários, tarefas, comentários, papéis e status possuem relacionamentos bem definidos - favorece
o uso de um banco estruturado.
### Arquitetura - Clean Architecture
A Clean Architecture foi adotada por promover a separação clara de responsabilidades entre as camadas
da aplicação, isolando regras de negócio de detalhes de infraestrutura. A organização segue quatro camadas:
Domain (entidades e interfaces), Use Cases (casos de uso), Adapters (controllers e schemas) e Infraestructure 
(repositórios, banco de dados e serviços externos).
### Modelagem de Papéis e Status como Entidades
Os papéis de usuários e os status de tarefas foram implementados como tabelas dedicadas (`roles` e `statuses`) 
em vez de ENUMs, tornando o sistema mais extensível sem necessidade de alterações estruturais no banco.
### Requisitos Complementares Escolhidos
**Requisito 1 - Google Calendar:** Tarefas com data e hora são sincronizadas automaticamente como eventos do Google
Calendar do usuário via OAuth 2.0 com PKCE, sendo removidas do calendário ao deletar a tarefa.

**Requisito 5 - Permissões por Papéis:** Administradores têm acesso irrestrito; Usuários gerenciam apenas seus próprios
recursos; Convidados têm acesso somente a leitura.

**Requisito 6 - Comentários em Tarefas:** Implementação do sub-recurso `/tasks/{id}/comments`, permitindo a criação, 
leitura e exclusão de comentários vinculados a tarefas e usuários.

## Modelagem de Dados
<img width="1012" height="782" alt="Collaborative Task Manager - Logic Model" src="https://github.com/user-attachments/assets/58805e5c-1e07-491c-bb10-f427c3eb4211" />

## Fluxo de Requisição e Exemplos
### Autenticação
Todos os endpoints, exceto `POST /users` e `POST /auth/login`, requerem autenticação via token JWT. O token
deve ser enviado no header `Authorization` no formato `Bearer <token>`.
### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "joao@email.com",
  "password": "Password123"
}
```
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
### Usuários
#### Criar Usuário
```
POST /users
Content-Type: application/json

{
  "name": "João Büttenbender",
  "email": "joao@email.com",
  "password": "Password123",
  "role_id": 1
}
```
```
{
  "id": 1,
  "name": "João Büttenbender",
  "email": "joao@email.com",
  "role_id": 1,
  "created_at": "2026-06-14T21:00:00"
}
```
#### Desativar Usuário (soft delete)
```
DELETE /users/1/deactivate
Authorization: Bearer <token>
```
```
204 No Content
```
### Tarefas
#### Criar Tarefa
```
POST /tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Implementar autenticação",
  "description": "Implementar JWT na API",
  "due_date": "2026-07-01T10:00:00",
  "status_id": 1,
  "assigned_to": 1
}
```
```
{
  "id": 1,
  "title": "Implementar autenticação",
  "description": "Implementar JWT na API",
  "due_date": "2026-07-01T10:00:00",
  "status_id": 1,
  "calendar_event_id": "8fndu9iabeg45l3cbai3vtfsrk",
  "owner_id": 1,
  "assigned_to": 1,
  "created_at": "2026-06-14T21:00:00"
}
```
#### Listar Tarefas com Filtros
```
GET /tasks?status_id=1&assigned_to=1
Authorization: Bearer <token>
```
### Comentários
#### Criar Comentário
```
POST /tasks/1/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Tarefa concluída com sucesso!"
}
```
```
{
  "id": 1,
  "content": "Tarefa concluída com sucesso!",
  "task_id": 1,
  "user_id": 1,
  "created_at": "2026-06-14T21:00:00"
}
```
### Google Calendar
#### Autorizar Integração
Acessar diretamente no navegador, subindo `{user_id}` pelo ID do usuário autenticado:
```
http://localhost:8000/auth/google/authorize?user_id={user_id}
```
Após a autorização, todas as tarefas criadas com `due_date` serão automaticamente sincronizadas
com o Google Calendar do usuário.

### Sistema de Permissões

| Endpoint                         | Admin                       | User                       | Guest |
|----------------------------------|-----------------------------|----------------------------|-------|
| `POST /tasks`                    | ✅ Qualquer `assigned_to`   | ✅ Apenas para si mesmo    | ❌ |
| `PUT /tasks/{id}`                | ✅ Qualquer tarefa          | ✅ Apenas suas tarefas     | ❌ |
| `DELETE /tasks/{id}`             | ✅ Qualquer tarefa          | ✅ Apenas suas tarefas     | ❌ |
| `GET /tasks`                     | ✅                          | ✅                         | ✅ |
| `POST /tasks/{id}/comments`      | ✅                          | ✅                         | ❌ |
| `DELETE /tasks/{id}/comments/{id}` | ✅ Qualquer comentário    | ✅ Apenas seus comentários | ❌ |
| `GET /tasks/{id}/comments`       | ✅                          | ✅                         | ✅ |

## Configuração e Deploy
### Variáveis de Ambiente
O projeto utiliza um arquivo `.env` para configuração. As variáveis disponíveis são:

| Variável                        | Descrição                                         |
|---------------------------------|---------------------------------------------------|
| `DATABASE_URL`                  | URL de conexão com o banco de dados               |
| `SECRET_KEY`                    | Chave secreta para assinatura dos tokens JWT      |
| `ALGORITHM`                     | Algoritmo de assinatura JWT (padrão: HS256)       |
| `ACCESS_TOKEN_EXPIRE_MINUTES`   | Tempo de expiração do token em minutos            |
| `MYSQL_ROOT_PASSWORD`           | Senha do MySQL (utilizada pelo Docker)            |
| `MYSQL_DATABASE`                | Nome do banco de dados (utilizado pelo Docker)    |
| `GOOGLE_CLIENT_ID`              | Client ID do projeto no Google Cloud Console      |
| `GOOGLE_CLIENT_SECRET`          | Client Secret do projeto no Google Cloud Console  |
| `GOOGLE_REDIRECT_URI`           | URI de direcionamento OAuth do Google             |

Para gerar uma `SECRET_KEY` segura, execute:
```
python -c "import secrets; print(secrets.token_hex(32))"
```
### Deploy com Docker
O projeto está configurado para rodar em containers Docker com dois serviços: a API e o banco de dados 
MySQL. O arquivo `docker-compose.yml` define a configuração completa dos serviços, incluindo healthcheck 
para garantir que a API só suba após o banco estar pronto.

Para subir o ambiente
```
docker-compose up --build
```
Para parar sem perder os dados:
```
docker-compose down
```
Para parar e apagar todos os dados:
```
docker-compose down -v
```
### Integração com o Google Calendar
Para habilitar a integração com o Google Calendar, é necessário:
1. Criar um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ativar a **Google Calendar API**
3. Criar credenciais OAuth 2.0 do tipo **Web Application**
4. Adicionar `http://localhost:8000/auth/google/callback` como URI de redirecionamento autorizado
5. Copiar o `client_id` e `client_secret` para o `.env`

Cada usuário que deseja utilizar a integração deve autorizar o acesso acessando:
```
http://localhost:8000/auth/google/authorize?user_id={id_do_usuario}
```
