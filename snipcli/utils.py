import pyperclip
import logging

logger = logging.getLogger(__name__)

def copy_to_clipboard(text: str) -> None:
    """
    Copies the given text to the system clipboard using pyperclip.

    Provides cross-platform clipboard support. If a clipboard mechanism
    is not found or an error occurs (e.g., missing dependencies like xclip/xsel
    on Linux), a warning will be logged, and the operation will fail silently
    to the caller.

    Args:
        text: The string to be copied to the clipboard.
    """
    try:
        pyperclip.copy(text)
        logger.debug("Successfully copied text to clipboard.")
    except pyperclip.PyperclipException as e:
        logger.warning(
            f"Failed to copy text to clipboard: {e}. "
            "Please ensure you have a clipboard mechanism installed and accessible "
            "(e.g., xclip/xsel on Linux, or ensure your display server is running)."
        )
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.error(
            f"An unexpected error occurred while attempting to copy to clipboard: {e}",
            exc_info=True
        )