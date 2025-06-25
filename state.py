from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps


class State(TypedDict):
    """
    Shared state schema for the multi-agent customer support system.
    This structure tracks the evolving context passed between agents during a workflow.
    """
    customer_id: str  # Retrieved after account verification

    messages: Annotated[List[AnyMessage], add_messages]  # Aggregated message history

    loaded_memory: str  # User preferences from long-term memory

    remaining_steps: RemainingSteps  # Limits agent loop depth
