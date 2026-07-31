# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### 2026-07-31
- `fix`: fix missing `Request` parameter on the stats endpoint, required for rate limiting
- `feat`: add rate limiting to API endpoints, with documentation of the chosen limits
- `deploy`: application deployed to production on Render
- `docs`: update changelog
- `feat`: add duplicate URL checking before creation

### 2026-07-30
- `docs`: update documentation
- `feat`: add URL stats endpoint and centralize short_code lookup in the service layer
- `test`: add automated tests for base62 encoding and URL creation service
- `docs`: add updated requirements file
- `docs`: add project documentation in English and Portuguese (README)
- `feat`: add shorten and redirect endpoints (`POST /shorten`, `GET /{short_code}`)
- `chore`: update `.gitignore`
- `chore`: configure Alembic for schema migrations
- `feat`: add URL model with `sqlite_autoincrement` support
- `feat`: add database connection setup (engine, session, declarative base)

### 2026-07-29
- `chore`: add initial dependencies (FastAPI, Uvicorn)
- `chore`: initial project structure
- `chore`: initial `.gitignore`