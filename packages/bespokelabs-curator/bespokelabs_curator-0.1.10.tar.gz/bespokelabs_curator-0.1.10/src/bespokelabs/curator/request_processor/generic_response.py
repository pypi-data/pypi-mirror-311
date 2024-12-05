import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .generic_request import GenericRequest

"""A generic response model for LLM API requests.

Attributes:
    response_message: The main response content. Can be:
        - None when there are errors
        - str for non-structured output
        - Dict[str, Any] for structured output
    response_errors: List of error messages. None when there are no errors.
    raw_response: The raw response data from the API.
    raw_request: The raw request data. Will be None for BatchAPI requests.
    generic_request: The associated GenericRequest object.
    created_at: The datetime when the request was created.
    finished_at: The datetime when the request was finished.
    token_usage: Token usage information for the request.
    response_cost: The cost of the request in USD.
"""


class TokenUsage(BaseModel):
    """Token usage information for an API request.

    Attributes:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        total_tokens: Total number of tokens used
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class GenericResponse(BaseModel):
    response_message: Optional[Dict[str, Any]] | str = None
    response_errors: Optional[List[str]] = None
    raw_response: Optional[Dict[str, Any]]
    raw_request: Optional[Dict[str, Any]] = None
    generic_request: GenericRequest
    created_at: datetime.datetime
    finished_at: datetime.datetime
    token_usage: Optional[TokenUsage] = None
    response_cost: Optional[float] = None
