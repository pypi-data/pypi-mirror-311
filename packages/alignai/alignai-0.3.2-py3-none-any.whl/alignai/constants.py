class EventTypes:
    SESSION_OPEN = "session_open"
    SESSION_CLOSE = "session_close"
    USER_RECOGNIZE = "user_recognize"
    MESSAGE_CREATE = "message_create"
    FEEDBACK_CREATE = "feedback_create"


ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
DEFAULT_ASSISTANT_ID = "DEFAULT"

FEEDBACK_THUMBS_UP = "thumbs_up"
FEEDBACK_THUMBS_DOWN = "thumbs_down"

FLUSH_INTERVAL_MS = 3000
FLUSH_BATCH_SIZE = 50
FLUSH_TIMEOUT_SECONDS = 5
MAX_BUFFER_SIZE = 200
API_MAX_RETIRES = 3

SERVER_BASE_URL = "https://api.impaction.ai"
