🇧🇷 [Português](README.pt-br.md) | 🇺🇸 English

# URL Shortener API

*Created by Marlon Ern — [LinkedIn](https://www.linkedin.com/in/marlon-ern-731bb1102/) · [GitHub](https://github.com/MarlonErn)*

## Live Demo

The application is available in production:
🔗 https://url-shortener-8ret.onrender.com

Interactive documentation (Swagger): https://url-shortener-8ret.onrender.com/docs

> ⚠️ Hosted on Render's free tier — the service "goes to sleep" after
> a period of inactivity (the initial request may take a few
> seconds to respond), and data is reset whenever the service
> restarts, as the free environment lacks persistent storage.

## About

A URL shortening REST API, built as a study project for a technical
portfolio. The system receives a long URL, generates a unique short
code, and redirects access to the original destination, counting
clicks on each redirect.

The project was developed with a focus on consistent data modeling,
schema versioning through migrations, and clear separation of
responsibilities across layers (models, schemas, services, and
routers) — an organization pattern inspired by real corporate
environments.

Among the project's technical decisions is the generation of short
codes through numeric conversion to base62, with a deliberate
adjustment to the database's initial identifier to guarantee a
minimum character length from the very first record (detailed in the
"Technical Decisions" section).

## Tech Stack

- **Python 3.14.3** — main language of the project
- **FastAPI** — web framework used to build the REST API
- **SQLAlchemy** — ORM used for data modeling and database access
- **Alembic** — schema versioning control (migrations)
- **Pydantic v2** — input/output data validation and serialization
- **SQLite** — database used in the development environment
- **Uvicorn** — ASGI server used to run the application

## Architecture

The project follows a layered separation of responsibilities, inspired by patterns used in corporate environments:

```
app/
├── main.py          # Application entry point, registers the routers
├── database.py       # Database connection setup (engine, session, declarative base)
├── models/           # Database table representation (SQLAlchemy)
├── schemas/           # API input/output contracts (Pydantic)
├── services/          # Business logic, isolated from routes
└── routers/           # API endpoints, organized by resource
```

**Why this separation:**

- **`models`** represents the database — what physically exists in the tables.
- **`schemas`** represents the API contracts — what the client sends and receives, which isn't always the same as what exists in the database (for example, the client never sends `id` or `created_at` when creating a URL).
- **`services`** concentrates the business logic (such as short code generation), keeping routers lean and focused only on orchestrating request → service → response.
- **`routers`** exposes the HTTP endpoints, delegating all real logic to the service layer.

This division makes maintenance and testing easier: each layer can be understood, changed, or tested in isolation, without a change in one forcing changes in the others.

## Getting Started

### Prerequisites

- Python 3.14.3
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MarlonErn/url-shortener.git
cd url-shortener
```

2. Create and activate the virtual environment:
```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### Database setup

Apply the migrations to create the database structure:
```bash
alembic upgrade head
```

### Running the application

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.
Interactive documentation (Swagger) is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

> 💡 To interactively explore all endpoints, with the ability to test
> requests directly from the browser, access the Swagger documentation
> at `/docs` after running the application.

### `POST /shorten`

Creates a new shortened URL.

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

Redirects to the original URL matching the given code, and increments the click counter.

**Example:** `GET /baaaa`

**Behavior:**
- If the `short_code` exists → redirects (`302`) to the `original_url`
- If it doesn't exist → returns `404` with an error message

**Response (404, when not found):**
```json
{
  "detail": "Short URL not found"
}
```

## Technical Decisions

### Why FastAPI instead of Flask or Django

FastAPI was chosen for its native typing via Pydantic (which enforces
explicit data contracts), automatic documentation via Swagger, and
for being a framework strongly adopted in data/API contexts, aligned
with this project's scope. Django was ruled out for bringing
unnecessary features for a small, focused API (its own ORM, admin
panel, template system).

### Short code generation via base62

Instead of generating random codes or hashes, the project uses an
incremental counter (the table's own auto-incremented `id`) converted
to base62. This approach removes the need to check for collisions on
every generation, since the database `id` guarantees uniqueness by
nature.

### Temporary placeholder during URL creation

The `short_code` column is defined as required and unique
(`nullable=False`, `unique=True`), but its value can only be
calculated **after** the record is inserted into the database — since
it depends on the auto-incremented `id` generated on insert.

To work around this circular dependency, the creation flow first
inserts the record with a unique temporary value, generated via
`uuid4`, avoiding any conflict with the `unique=True` constraint even
in the case of concurrent calls. After obtaining the `id` generated by
the database, the real `short_code` is calculated via base62 and the
record is updated in a second transaction.

### Minimum size of the generated code

Since the base62 conversion is proportional to the numeric value of
the `id`, the first records would generate 1-character codes (e.g.
`id=1` → `"b"`). To avoid this, the initial value of the
auto-increment sequence was adjusted via migration to `14,776,335` —
the last value representable with 4 characters in base62 — ensuring
every generated code has at least 5 characters from the very first
record.

### Use of `sqlite_autoincrement`

By default, SQLite doesn't maintain a sequence control table
(`sqlite_sequence`) unless the column is explicitly declared with
`AUTOINCREMENT`. This configuration was required to allow the manual
adjustment of the sequence's initial value, described above.

### Rate limiting on endpoints

To protect the API against abuse and excessive use, the `slowapi`
library was adopted, identifying each client by IP address and
applying per-minute request limits.

Limits were calibrated differently depending on the endpoint type:

- **`POST /shorten`**: limited to `10/minute`. Since creating URLs
  is an infrequent action for a legitimate user, a stricter limit
  here doesn't hurt normal usage, while reducing the risk of mass
  record creation (each call performs two database transactions,
  making this the most expensive endpoint in the system).
- **`GET /{short_code}` and `GET /{short_code}/stats`**: limited to
  `60/minute`. A more permissive limit is necessary here, since
  redirection is the product's core purpose — a popular link may
  receive a high, legitimate volume of accesses in a short time, and
  an overly strict limit would block real users.

It's worth noting that the limit is applied per IP and per route,
not per specific `short_code` — meaning it protects against a single
client overloading the server, but does not limit how many times an
individual link can be accessed in total.

## Known Limitations

### Window between commits during URL creation

As described in the "Temporary placeholder during URL creation"
section, the creation process performs two separate transactions: one
to obtain the auto-incremented `id`, and another to persist the real
`short_code`. Between these two operations, there's a small window of
time where the record exists in the database with a placeholder value
instead of the final code.

In a low-traffic environment (such as this portfolio project), this
window is irrelevant in practice. In a production scenario with high
concurrent request volume, this approach could be replaced by a
strategy that avoids the intermediate state — for example, reserving
the `id` before the full insert, or using a single transaction with
code generation independent of the database's auto-increment.

### No duplicate URL check

Currently, the system doesn't check whether an `original_url` has
already been shortened before — every call to `POST /shorten` always
creates a new record and a new code, even if the destination URL is
identical to an existing one. A future improvement would be to query
the database before creation and reuse the already-generated code,
when applicable.

### Local database environment

The project uses SQLite as its database, suitable for development and
demonstration purposes. A real production version would likely
require migration to a more robust database (e.g. PostgreSQL),
especially considering the use of `sqlite_autoincrement`, which is a
dialect-specific configuration.

## Next Steps

- [ ] Add automated tests (pytest), covering the base62 encoding logic
      and the URL creation flow
- [ ] Implement duplicate URL checking before creation
- [ ] Add a `GET /{short_code}/stats` endpoint, returning the URL's
      data (including clicks) without triggering the redirect
- [ ] Migrate the database to PostgreSQL for the production environment
- [ ] Deploy the application (Render/Railway) with a public demo link
- [ ] Add basic rate limiting to protect the creation endpoint against
      abuse and/or excessive use