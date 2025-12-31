from typing import Literal, Optional, Tuple
from openai import OpenAI
from config import settings
from .agents.db_query_agent import DBQueryAgent
from .agents.safety_guard import SafetyGuard

class Orchestrator:

    CONVERSATION_SYSTEM_PROMPT = """You are a helpful assistant specialized in helping users search for live music events in a Neo4j database.

Your role:
1. Help users find live music events by understanding their preferences (date, location, genre, artist, venue, etc.)
2. When a query is executed, provide clear, natural language responses based on the results
3. If results are empty, suggest alternative search criteria
4. Be conversational, friendly, and helpful

Database Schema:
{schema}
"""

    OUT_OF_SCOPE_RESPONSE = """I'm a live music events search assistant. I help you find concerts, shows, and performances.

I can help you search for events by:
- Date and time (e.g., "events this weekend", "shows on Friday night")
- Location (e.g., "concerts in Portland", "events in NYC")
- Genre (e.g., "jazz concerts", "rock shows")
- Artist or band name
- Venue name
- Any combination of the above

How can I help you find live music events today?"""

    def __init__(self, schema: str):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.db_agent = DBQueryAgent(schema)
        self.safety_guard = SafetyGuard()
        self.schema = schema
        self._conversation_prompt = self.CONVERSATION_SYSTEM_PROMPT.format(schema=schema)

    def decide_action(
        self,
        user_message: str,
        conversation_history: Optional[list] = None
    ) -> Literal["QUERY_DB", "NEEDS_INFO", "OUT_OF_SCOPE"]:
        """Decides what action to take based on user message."""
        history_context = ""
        if conversation_history:
            history_context = "\n\nConversation history:\n"
            for msg in conversation_history:
                history_context += f"{msg.role}: {msg.content}\n"

        decision_prompt = f"""You are analyzing a user message for a live music events search assistant.
{history_context}
Current user message: "{user_message}"

Determine the intent and respond with ONE of these options:
1. "OUT_OF_SCOPE" - If the message is NOT about searching for live music events
2. "NEEDS_INFO" - If the message IS about live music events but is missing critical information
3. "QUERY_DB" - If the message IS about live music events AND has enough information to search

Important: Consider conversation history. If user says "same dates" or "there", look at history.

Respond with ONLY one word: OUT_OF_SCOPE, NEEDS_INFO, or QUERY_DB"""

        response = self.client.chat.completions.create(
            model=settings.conversation_model,
            messages=[{"role": "user", "content": decision_prompt}],
            temperature=0,
            max_tokens=20,
        )

        decision = response.choices[0].message.content.strip().upper()

        if "OUT_OF_SCOPE" in decision:
            return "OUT_OF_SCOPE"
        elif "NEEDS_INFO" in decision:
            return "NEEDS_INFO"
        else:
            return "QUERY_DB"

    def execute_query(self, user_message: str) -> tuple[Optional[str], Optional[list]]:
        """Orchestrates query execution through specialists."""
        # Generate query via DB Query Agent
        cypher = self.db_agent.generate_cypher(user_message)

        # Safety check via Safety Guard
        if not self.safety_guard.validate_read_only(cypher):
            raise ValueError("Query contains write operations")

        # Execute query
        results = self.db_agent.execute_query(cypher)

        return cypher, results

    def generate_response(
        self,
        action: str,
        user_message: str,
        conversation_history: Optional[list] = None,
        cypher: Optional[str] = None,
        results: Optional[list] = None
    ) -> Tuple[str, Optional[str], Optional[list], bool, bool]:
        """
        Generate natural language response based on action.
        Returns: (response_text, cypher, results, used_query, needs_more_info)
        """
        if action == "OUT_OF_SCOPE":
            return (
                self.OUT_OF_SCOPE_RESPONSE,
                None,
                None,
                False,
                False
            )

        elif action == "NEEDS_INFO":
            guidance_prompt = f"""The user wants to search for live music events but their request is missing important information.

User message: "{user_message}"

Provide a friendly, helpful response that:
1. Acknowledges their interest in finding events
2. Asks for the missing information (date, location, genre, artist, or venue)
3. Gives examples of what information would be helpful

Be conversational and helpful."""

            guidance_response = self.client.chat.completions.create(
                model=settings.conversation_model,
                messages=[{"role": "user", "content": guidance_prompt}],
                temperature=0.7,
            )

            return (
                guidance_response.choices[0].message.content.strip(),
                None,
                None,
                False,
                True
            )

        elif action == "QUERY_DB":
            # Build conversation context
            messages = [{"role": "system", "content": self._conversation_prompt}]
            if conversation_history:
                for msg in conversation_history:
                    messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": user_message})

            # Format results for LLM
            results_summary = f"Query executed successfully. Found {len(results) if results else 0} event(s)."
            if results:
                sample_results = results[:5] if len(results) > 5 else results
                results_summary += f"\n\nEvent details:\n{str(sample_results)}"
                if len(results) > 5:
                    results_summary += f"\n\n(Showing 5 of {len(results)} total events)"
            else:
                results_summary += "\n\nNo events found matching your criteria. Try adjusting your search."

            # Add query context to conversation
            messages.append({
                "role": "assistant",
                "content": f"I searched the database and found these results:\n{results_summary}",
            })

            # Generate natural language response
            response = self.client.chat.completions.create(
                model=settings.conversation_model,
                messages=messages,
                temperature=0.7,
            )

            return (
                response.choices[0].message.content.strip(),
                cypher,
                results,
                True,
                False
            )

        # Fallback
        return ("I'm not sure how to help with that.", None, None, False, False)
