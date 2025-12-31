class SafetyGuard:
    """Specialist agent for enforcing safety policies."""

    def validate_read_only(self, cypher: str) -> bool:
        """Validates that query contains only read operations."""
        forbidden = ["CREATE", "DELETE", "MERGE", "SET ", "REMOVE", "DROP", "DETACH"]
        upper = cypher.upper()
        return not any(kw in upper for kw in forbidden)

    # TODO check NemoGard and Llamagard
