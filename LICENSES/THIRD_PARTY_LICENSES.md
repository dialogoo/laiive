# Third-Party Licenses

This project includes and depends on the following open source libraries:

## Development Tools

Used via pre-commit hooks for code quality and security:

- **pre-commit** (MIT) - https://github.com/pre-commit/pre-commit
- **pre-commit-hooks** (MIT) - https://github.com/pre-commit/pre-commit-hooks
- **ruff-pre-commit** (MIT) - https://github.com/astral-sh/ruff-pre-commit
- **mypy** (MIT) - https://github.com/python/mypy
- **detect-secrets** (Apache-2.0) - https://github.com/Yelp/detect-secrets
- **sqlfluff** (MIT) - https://github.com/sqlfluff/sqlfluff
- **commitizen** (MIT) - https://github.com/commitizen-tools/commitizen

## Runtime Dependencies

### Frontend Service
- **streamlit** (Apache-2.0) - https://github.com/streamlit/streamlit
- **pydantic** (MIT) - https://github.com/pydantic/pydantic
- **pydantic-settings** (MIT) - https://github.com/pydantic/pydantic-settings

### Scraper Service
- **scrapy** (BSD-3-Clause) - https://github.com/scrapy/scrapy
- **pandas** (BSD-3-Clause) - https://github.com/pandas-dev/pandas
- **psycopg2-binary** (LGPL-3.0-or-later) - https://github.com/psycopg/psycopg2
- **loguru** (MIT) - https://github.com/Delgan/loguru
- **rapidfuzz** (MIT) - https://github.com/maxbachmann/RapidFuzz
- **pydantic** (MIT) - https://github.com/pydantic/pydantic
- **pydantic-settings** (MIT) - https://github.com/pydantic/pydantic-settings

### Retriever Service
- **fastapi** (MIT) - https://github.com/tiangolo/fastapi
- **uvicorn** (BSD-3-Clause) - https://github.com/encode/uvicorn
- **sqlalchemy** (MIT) - https://github.com/sqlalchemy/sqlalchemy
- **asyncpg** (Apache-2.0) - https://github.com/MagicStack/asyncpg
- **pgvector** (PostgreSQL License) - https://github.com/pgvector/pgvector-python
- **openai** (Apache-2.0) - https://github.com/openai/openai-python
- **loguru** (MIT) - https://github.com/Delgan/loguru
- **pydantic** (MIT) - https://github.com/pydantic/pydantic
- **pydantic-settings** (MIT) - https://github.com/pydantic/pydantic-settings

---

## License Compatibility

All dependencies listed above are compatible with our Apache-2.0 license:

- **MIT, BSD-3-Clause, Apache-2.0, PostgreSQL License**: Fully compatible permissive licenses
- **LGPL-3.0-or-later** (`psycopg2-binary`): Compatible when dynamically linked (as it is with Python packages)

## Notes

All third-party software is used in compliance with their respective licenses. Full license texts are available in the linked repositories.

**Dynamic Linking**: LGPL-3.0 licensed components are dynamically linked as Python packages, which means they do not impose copyleft requirements on the entire project.
