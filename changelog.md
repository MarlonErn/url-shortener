# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### 2026-07-30
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