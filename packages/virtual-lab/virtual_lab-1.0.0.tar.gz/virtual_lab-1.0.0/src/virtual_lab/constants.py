"""Holds constants."""

MODEL_TO_INPUT_PRICE_PER_TOKEN = {
    "gpt-3.5-turbo": 0.5 / 10**6,
    "gpt-4o": 5 / 10**6,
    "gpt-4o-2024-05-13": 5 / 10**6,
    "gpt-4o-2024-08-06": 2.5 / 10**6,
}

MODEL_TO_OUTPUT_PRICE_PER_TOKEN = {
    "gpt-3.5-turbo": 1.5 / 10**6,
    "gpt-4o": 15 / 10**6,
    "gpt-4o-2024-05-13": 15 / 10**6,
    "gpt-4o-2024-08-06": 10 / 10**6,
}

CONSISTENT_TEMPERATURE = 0.2
CREATIVE_TEMPERATURE = 0.8

PUBMED_TOOL_NAME = "pubmed_search"
PUBMED_TOOL_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": PUBMED_TOOL_NAME,
        "description": "Get full text biomedical and life sciences articles from PubMed Central. "
        "Recommended use: either query for 1 specific article by title or query for 3 articles by topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to use to search PubMed Central for scientific articles. "
                    "More specific search queries are more likely to return relevant articles.",
                },
                "num_articles": {
                    "type": "integer",
                    "enum": [1, 2, 3],
                    "description": "The number of articles to return from the search query.",
                },
            },
            "required": ["query", "num_articles"],
        },
    },
}
