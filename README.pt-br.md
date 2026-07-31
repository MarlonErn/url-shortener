🇧🇷 Português | 🇺🇸 [English](README.md)

# URL SHORTENER API

*Criado por Marlon Ern — [Linkedin](https://www.linkedin.com/in/marlon-ern-731bb1102/) · [Github](https://github.com/MarlonErn)*

## Demonstração ao Vivo

A aplicação está disponível em produção:
🔗 https://url-shortener-8ret.onrender.com

Documentação interativa (Swagger): https://url-shortener-8ret.onrender.com/docs

> ⚠️ Hospedado no free tier do Render — o serviço "dorme" após
> período de inatividade (o primeiro acesso pode demorar alguns
> segundos para responder) e os dados são reiniciados a cada
> reinicialização do serviço, já que o ambiente gratuito não
> possui disco persistente.

## Sobre
Uma API REST de encurtamento de URLs, construída como projeto de
estudo para portfólio técnico. O sistema recebe uma URL longa, gera
um código curto único e redireciona o acesso para o destino original,
contabilizando cliques a cada redirecionamento.

O projeto foi desenvolvido com foco em modelagem de dados consistente,
versionamento de schema via migrations, e separação clara de
responsabilidades entre camadas (models, schemas, services e routers) —
um padrão de organização inspirado em ambientes corporativos reais.

Entre as decisões técnicas do projeto está a geração de códigos curtos
via conversão numérica para base62, com um ajuste deliberado no
identificador inicial do banco para garantir um tamanho mínimo de
caracteres desde o primeiro registro (detalhado na seção
"Decisões Técnicas").

## Sobre o Desenvolvimento

Este projeto foi desenvolvido em aproximadamente 3h30min a 4h30min de
trabalho efetivo, distribuídas ao longo de 3 dias. Uma IA (Claude)
foi utilizada como apoio de estudo, orientando as etapas técnicas e
explicando os conceitos envolvidos — porém, todo o código foi
digitado manualmente, garantindo melhor compreensão do projeto e
validação prática de cada etapa do desenvolvimento.

## Stack Utilizada

- **Python 3.14.3** — linguagem principal do projeto
- **FastAPI** — framework web para construção da API REST
- **SQLAlchemy** — ORM utilizado para modelagem e acesso ao banco de dados
- **Alembic** — controle de versionamento de schema (migrations)
- **Pydantic v2** — validação e serialização de dados de entrada/saída
- **SQLite** — banco de dados utilizado no ambiente de desenvolvimento
- **Uvicorn** — servidor ASGI utilizado para rodar a aplicação

## Arquitetura

O projeto segue uma separação de responsabilidades em camadas, inspirada em padrões usados em ambientes corporativos:
```
app/
├── main.py # Ponto de entrada da aplicação, registra os routers
├── database.py # Configuração de conexão com o banco (engine, sessão, base declarativa)
├── models/ # Representação das tabelas do banco (SQLAlchemy)
├── schemas/ # Contratos de entrada/saída da API (Pydantic)
├── services/ # Lógica de negócio, isolada das rotas
└── routers/ # Endpoints da API, organizados por recurso
```
**Por que essa separação:**

- **`models`** representa o banco de dados — o que existe fisicamente nas tabelas.
- **`schemas`** representa os contratos da API — o que o cliente envia e recebe, que nem sempre é igual ao que existe no banco (por exemplo, o cliente nunca envia `id` ou `created_at` ao criar uma URL).
- **`services`** concentra a lógica de negócio (como a geração do código curto), mantendo os routers enxutos e focados apenas em orquestrar requisição → serviço → resposta.
- **`routers`** expõe os endpoints HTTP, delegando toda a lógica real para a camada de serviço.

Essa divisão facilita manutenção e testes: cada camada pode ser entendida, alterada ou testada isoladamente, sem que uma mudança em uma força mudanças nas outras.

## Como Começar

### Pré-requisitos

- Python 3.14.3
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/MarlonErn/url-shortener.git
cd url-shortener
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Configuração do banco de dados

Aplique as migrations para criar a estrutura do banco:
```bash
alembic upgrade head
```

### Executando a aplicação

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em `http://127.0.0.1:8000`.
A documentação interativa (Swagger) fica em `http://127.0.0.1:8000/docs`.

## Endpoints da API

> 💡 Para explorar interativamente todos os endpoints, com a
> possibilidade de testar requisições diretamente pelo navegador,
> acesse a documentação Swagger em `/docs` após rodar a aplicação.


### `POST /shorten`

Cria uma nova URL encurtada.

**Request:**
```json
{
  "original_url": "https://www.exemplo.com/pagina-teste"
}
```

**Response (200):**
```json
{
  "short_code": "baaaa",
  "original_url": "https://www.exemplo.com/pagina-teste",
  "created_at": "2026-07-29T23:50:00",
  "clicks": 0
}
```

---

### `GET /{short_code}`

Redireciona para a URL original correspondente ao código informado, e incrementa o contador de cliques.

**Exemplo:** `GET /baaaa`

**Comportamento:**
- Se o `short_code` existir → redireciona (`302`) para a `original_url`
- Se não existir → retorna `404` com mensagem de erro

**Response (404, quando não encontrado):**
```json
{
  "detail": "Short URL not found"
}
```

## Decisões Técnicas

### Por que FastAPI em vez de Flask ou Django

FastAPI foi escolhido pela tipagem nativa via Pydantic (que obriga
contratos de dados explícitos), documentação automática via Swagger,
e por ser um framework fortemente adotado em contextos de dados/APIs,
alinhado ao escopo deste projeto. Django foi descartado por trazer
recursos desnecessários para uma API pequena e focada (ORM próprio,
admin panel, sistema de templates).

### Geração de códigos curtos via base62

Ao invés de gerar códigos aleatórios ou hashes, o projeto utiliza um
contador incremental (o próprio `id` autoincrementado da tabela)
convertido para base62. Essa abordagem elimina a necessidade de checar
colisões a cada geração, já que o `id` do banco garante unicidade por
natureza.

### Placeholder temporário na criação de URLs

A coluna `short_code` é definida como obrigatória e única
(`nullable=False`, `unique=True`), mas seu valor só pode ser calculado
**depois** que o registro é inserido no banco — já que depende do `id`
autoincrementado gerado na inserção.

Para contornar essa dependência circular, o fluxo de criação insere o
registro inicialmente com um valor temporário único, gerado via
`uuid4`, evitando qualquer conflito com a constraint `unique=True`
mesmo em caso de chamadas concorrentes. Após obter o `id` gerado pelo
banco, o `short_code` real é calculado via base62 e o registro é
atualizado com uma segunda transação.

### Tamanho mínimo do código gerado

Como a conversão para base62 é proporcional ao valor numérico do `id`,
os primeiros registros gerariam códigos de 1 caractere (ex: `id=1` →
`"b"`). Para evitar isso, o valor inicial da sequência de autoincremento
foi ajustado via migration para `14.776.335` — o último valor
representável com 4 caracteres em base62 — garantindo que todo código
gerado tenha no mínimo 5 caracteres desde o primeiro registro.

### Uso de `sqlite_autoincrement`

Por padrão, o SQLite não mantém uma tabela de controle de sequência
(`sqlite_sequence`) a menos que a coluna seja declarada explicitamente
com `AUTOINCREMENT`. Essa configuração foi necessária para permitir o
ajuste manual do valor inicial da sequência, descrito acima.

### Rate limiting nos endpoints

Para proteger a API contra abuso e uso excessivo, foi adotada a
biblioteca `slowapi`, que identifica cada cliente pelo endereço IP e
aplica limites de requisições por minuto.

Os limites foram calibrados de forma diferente por tipo de endpoint:

- **`POST /shorten`**: limite de `10/minuto`. Como a criação de URLs
  é uma ação pouco frequente para um usuário legítimo, um limite
  mais restritivo aqui não prejudica o uso normal, enquanto reduz o
  risco de criação em massa de registros (cada chamada realiza duas
  transações no banco, tornando esse endpoint o mais custoso do
  sistema).
- **`GET /{short_code}` e `GET /{short_code}/stats`**: limite de
  `60/minuto`. Um limite mais permissivo é necessário aqui, já que
  redirecionamento é o propósito central do produto — um link
  popular pode receber um volume alto e legítimo de acessos em pouco
  tempo, e um limite muito restritivo bloquearia usuários reais.

É importante notar que o limite é aplicado por IP e por rota, não
por `short_code` específico — ou seja, ele protege contra um mesmo
cliente sobrecarregando o servidor, mas não limita quantas vezes um
link individual pode ser acessado no total.

## Limitações Conhecidas

### Janela entre commits na criação de URLs

Como descrito na seção "Placeholder temporário na criação de URLs",
o processo de criação realiza duas transações separadas: uma para
obter o `id` autoincrementado, e outra para persistir o `short_code`
real. Entre essas duas operações, existe uma pequena janela de tempo
em que o registro existe no banco com um valor de placeholder em vez
do código final.

Em um ambiente de baixo tráfego (como este projeto de portfólio), essa
janela é irrelevante na prática. Em um cenário de produção com alto
volume de requisições concorrentes, essa abordagem poderia ser
substituída por uma estratégia que evite o estado intermediário —
por exemplo, reservando o `id` antes da inserção completa, ou
utilizando uma transação única com geração de código independente
do autoincremento do banco.

### ~~Ausência de verificação de URLs duplicadas

Atualmente, o sistema não verifica se uma `original_url` já foi
encurtada anteriormente — cada chamada a `POST /shorten` sempre gera
um novo registro e um novo código, mesmo que a URL de destino seja
idêntica a uma já existente. Uma futura melhoria seria consultar o
banco antes da criação e reaproveitar o código já gerado, quando
aplicável.~~

### Ambiente de banco de dados local

O projeto utiliza SQLite como banco de dados, adequado para
desenvolvimento e demonstração. Uma versão em produção real
provavelmente exigiria migração para um banco mais robusto (ex:
PostgreSQL), especialmente considerando o uso de `sqlite_autoincrement`,
que é uma configuração específica desse dialeto.

## Próximos Passos

- [x] Adicionar testes automatizados (pytest), cobrindo a lógica de
      codificação base62 e o fluxo de criação de URLs
- [x] Implementar verificação de URLs duplicadas antes da criação
- [x] Adicionar endpoint `GET /{short_code}/stats`, retornando os
      dados da URL (incluindo cliques) sem disparar o redirecionamento
- [ ] Migrar o banco de dados para PostgreSQL em ambiente de produção
- [x] Deploy da aplicação (Render) com link público de demonstração
- [x] Adicionar rate limiting básico para proteger o endpoint de criação
      contra abuso e/ou uso excessivo