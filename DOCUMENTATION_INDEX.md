# ReWear Documentation Index (Updated)

Last updated: March 31, 2026

## Start Here

1. `README.md` - project setup and usage
2. `PROJECT_COMPLETE.md` - current completion and verification status
3. `DELIVERABLES.md` - inventory of shipped components

## Architecture and Design

- `SYSTEM_ARCHITECTURE.md` - high-level architecture and component design
- `QUICK_REFERENCE.md` - shortcuts, common commands, quick API lookup

## API and Backend

- `docs/API_DOCUMENTATION.md` - endpoint reference and examples
- `backend/app.py` - app factory and security-sensitive boot config
- `backend/models/models.py` - active MongoEngine schema
- `backend/routes/` - route handlers by domain

## Deployment and Operations

- `docs/DEPLOYMENT_GUIDE.md` - deployment strategy and production setup
- `docs/TROUBLESHOOTING.md` - known issues and remedies

## What Changed in the Latest Update

- Documentation corrected from legacy SQL/SQLAlchemy language to current MongoDB/MongoEngine implementation
- Endpoint behavior updated to reflect current contracts
- Runtime verification status added: 59/59 smoke checks passed
- Exchange flow notes updated (offer-item selector behavior)
- Security hardening notes added (CORS/JWT/authz)

## Current Test Status

- Backend endpoint smoke checks: 59 passed, 0 failed
- JS and Python syntax validation: passing for modified modules

## Recommended Reading Order for New Developers

1. `README.md`
2. `SYSTEM_ARCHITECTURE.md`
3. `docs/API_DOCUMENTATION.md`
4. `docs/DEPLOYMENT_GUIDE.md`
5. `docs/TROUBLESHOOTING.md`

## Core Project Paths

- Backend: `backend/`
- Frontend: `frontend/`
- Documentation: `docs/` + root markdown files

