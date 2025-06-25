from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

# Initialize long-term memory store for persistent data between conversations
# This store will hold user-specific data, such as music preferences, across different sessions.
in_memory_store = InMemoryStore()

# Initialize checkpointer for short-term memory within a single thread/conversation
# This checkpointer saves the state of a specific conversational thread, allowing the graph to be paused and resumed.
# Needed for human-in-the-loop verification.
checkpointer = MemorySaver()
