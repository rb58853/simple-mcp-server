import logging
import logging.handlers
from pathlib import Path


def setup_logger() -> logging.Logger:
    """Configure logging for the MCP server with log rotation."""
    logger = logging.getLogger("supabase-mcp")

    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define a consistent log directory in the user's home folder
    log_dir = Path.home() / ".local" / "share" / "supabase-mcp"
    log_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Define the log file path
    log_file = log_dir / "mcp_server.log"

    # Create a rotating file handler
    # - Rotate when log reaches 5MB
    # - Keep 3 backup files
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )

    # Create formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(message)s", datefmt="%y/%m/%d %H:%M:%S")

    # Add formatter to file handler
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Set level
    logger.setLevel(logging.DEBUG)

    return logger


logger = setup_logger()