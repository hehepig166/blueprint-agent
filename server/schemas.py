from enum import Enum


class Stage(Enum):
    GENERATE_QUERY = "generate_query"
    SEARCH = "search"
    ANALYZE = "analyze"
