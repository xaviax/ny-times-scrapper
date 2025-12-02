from dataclasses import dataclass

@dataclass
class ScrapeRequest:
    search_term: str
    pages: int
    user_id : str | None = None