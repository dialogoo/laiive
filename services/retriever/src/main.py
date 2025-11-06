from src.config import settings
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.ollama import Ollama
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import LLM
from pydantic import BaseModel, ValidationError
from typing import Optional
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from loguru import logger
import json


class DataRange(BaseModel):
    start: str
    end: str


class SQLFilter(BaseModel):
    date_range: Optional[DataRange] = None
    place: Optional[str] = None


today = date.today()

# Create async engine
engine = create_async_engine(settings.postgres_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def llm_factory() -> LLM:
    logger.info(f"Initializing LLM provider: {settings.llm_provider}")

    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        return OpenAI(
            api_key=settings.openai_api_key,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
        )

    elif settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required when using Anthropic provider"
            )
        return Anthropic(
            api_key=settings.anthropic_api_key,
            model=settings.llm_model,  # e.g., "claude-3-5-sonnet-20241022"
            temperature=settings.llm_temperature,
        )

    elif settings.llm_provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when using Gemini provider")
        return Gemini(
            api_key=settings.gemini_api_key,
            model=settings.llm_model,  # e.g., "gemini-1.5-pro", "gemini-1.5-flash"
            temperature=settings.llm_temperature,
        )

    elif settings.llm_provider == "ollama":
        return Ollama(
            model=settings.llm_model,  # e.g., "llama2", "mistral"
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


llm = llm_factory()


async def get_response(message: str, filters_info: Optional[SQLFilter] = None) -> str:
    """Simple version: just pass the user message to the LLM"""
    logger.info(f"Processing message: {message}")

    # Build a simple prompt
    prompt = f"""You are a helpful assistant for musical life events.
        Today is {today}.
        User question: {message}
        Please provide a helpful response."""

    try:
        # Call the LLM
        response = llm.complete(prompt)
        logger.info("Successfully got LLM response")
        return response.text
    except Exception as e:
        logger.error(f"Error calling LLM: {e}", exc_info=True)
        return f"Sorry, I encountered an error: {str(e)}"

    def format_date_range(date_range: DataRange) -> str:
        return "event_date >= :start_date AND event_date <= :end_date"

    def format_place_filter(place: str) -> str:
        return "place_city ILIKE :place_pattern"  # TODO

    def build_query(filters_info: SQLFilter) -> tuple[str, dict]:
        base_query = "SELECT * FROM events"
        conditions = []
        params = {}

        if filters_info.date_range:
            date_condition = format_date_range(filters_info.date_range)
            conditions.append(date_condition)
            params["start_date"] = filters_info.date_range.start
            params["end_date"] = filters_info.date_range.end

        if filters_info.place:
            place_condition = format_place_filter(filters_info.place)
            conditions.append(place_condition)
            params["place_pattern"] = f"%{filters_info.place}%"

        if conditions:
            query = f"{base_query} WHERE {' AND '.join(conditions)}"
        else:
            query = base_query

        logger.info(f"Generated SQL query: {query}")
        return query, params

    async def query_db(filters_info: SQLFilter) -> str:
        try:
            query = build_query(filters_info)
            async with AsyncSessionLocal() as session:
                result = await session.execute(sqlalchemy.text(query))
                rows = result.fetchall()
                return str([dict(row._mapping) for row in rows])
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            return f"Error querying database: {str(e)}"

    filtered_events = await query_db(filters_info)

    prompt = f"""
    You are a helpful assistant that can answer questions about musical life events.
    You will be given the location and date range of dates that the user is interested in.
    You will be given a list of filtered events from the events database.
    You need to answer to the user given information in the message.

    Today is {today}
    The user message is: {message}
    The filtered events are: {filtered_events}
    The filters are: {filters_info}

    IMPORTANT: If the user asks for a "list" or "all" events, show ALL available events from the filtered results.
    Do not limit yourself to just 2-3 events unless specifically asked.
    Format the response as a clear list with all relevant details for each event.

    Answer the user message based on the filtered events.
    The answer should be in the same language as the user message.
    """


def get_sql_filters(message: str) -> SQLFilter:
    prompt = f"""
    Analyze the following user message and extract specific information for database filtering.

    User message: "{message}"

    Please extract and format the following information:

    1. DATE_RANGE: If a date range is mentioned, format as ["YYYY-MM-DD", "YYYY-MM-DD"]
    2. PLACE: If a location, city, or address is mentioned

    Examples:
    - "Show me events in New York from 2024-01-15 to 2024-01-20" → date_range: ["2024-01-15", "2024-01-20"], place: "New York"
    - "What's happening in London this week?" → place: "London"
    - "What can I do in Paris?" → place: "Paris"

    Return your response as a JSON object with only the fields that are present in the message.
    If a field is not mentioned, omit it from the JSON response.
    """

    try:
        response = llm.complete(prompt)
        logger.debug(f"Raw LLM response: {response.text}")

        filter_data = json.loads(response.text.strip())

        # Validate expected structure
        if not isinstance(filter_data, dict):
            raise ValueError(f"Expected dict, got {type(filter_data)}")

        # Convert date strings to date objects
        date_range = None
        if filter_data.get("date_range"):
            if (
                not isinstance(filter_data["date_range"], list)
                or len(filter_data["date_range"]) != 2
            ):
                raise ValueError(
                    f"Invalid date_range format: {filter_data['date_range']}"
                )
            start_date = datetime.strptime(
                filter_data["date_range"][0], "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                filter_data["date_range"][1], "%Y-%m-%d"
            ).date()
            date_range = (start_date, end_date)

        sql_filter = SQLFilter(
            date_range=date_range,
            place=filter_data.get("place"),
        )
        logger.info(f"SQL filters: {sql_filter}")
        return sql_filter

    except json.JSONDecodeError as e:
        logger.error(
            f"Failed to parse LLM response as JSON: {e}. Response: {response.text[:200]}"
        )
        return SQLFilter()
    except (ValueError, KeyError, ValidationError) as e:
        logger.error(f"Invalid filter data structure: {e}. Data: {filter_data}")
        return SQLFilter()
    except Exception as e:
        logger.error(f"Unexpected error extracting SQL filters: {e}", exc_info=True)
    return SQLFilter()
