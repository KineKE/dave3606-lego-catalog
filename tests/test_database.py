from app.database import Database

def test_database_raises_exception_if_session_is_not_active(session_configured):
    db