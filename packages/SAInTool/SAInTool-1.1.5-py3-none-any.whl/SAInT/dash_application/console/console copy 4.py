import io
import sys
import logging
from SAInT.dash_application.common.dash_functions import get_pressed_buttons

# Disable Flask's log messages
logging.getLogger('werkzeug').setLevel(logging.ERROR)

class StreamToBuffer(io.StringIO):
    """Helper class to capture writes to a stream (stdout/stderr) and store them in a chronological buffer."""
    def __init__(self, buffer, prefix, original_stream, color = "black"):
        super().__init__()
        self.buffer = buffer
        self.prefix = prefix
        self.original_stream = original_stream  # Original stdout or stderr
        self.color = color

    def write(self, message):
        #colored_message = f'<span style="color:{self.color}">{self.prefix}: {message}</span><br>' if self.color else f"{self.prefix}: {message}<br>"
        # Append the message to the combined buffer with a prefix indicating its source
        self.buffer.write(f"{self.prefix}: {message}")
        #self.buffer.write(colored_message)

        # Also write the message to the original stream
        self.original_stream.write(message)

    def flush(self):
        # Make sure flush works for both the buffer and the original stream
        self.buffer.flush()
        self.original_stream.flush()

class Console:
    def __init__(self):
        RED_COLOR = "red"  # HTML color for red
        BLUE_COLOR = "blue"  # HTML color for blue (if needed)

        self.buffer = io.StringIO()

        # Save original stdout and stderr to restore later if needed
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Capture stdout and stderr with StreamToBuffer
        self.stdout_buffer = StreamToBuffer(self.buffer, "[STDOUT]", self.original_stdout, BLUE_COLOR)
        self.stderr_buffer = StreamToBuffer(self.buffer, "[STDERR]", self.original_stderr, RED_COLOR)
        
        # Override sys.stdout and sys.stderr
        sys.stdout = self.stdout_buffer
        sys.stderr = self.stderr_buffer

    def clear(self):
        """Clear both the main buffer and individual stream buffers."""
        self.buffer.seek(0)
        self.buffer.truncate(0)

    def update(self):
        """Returns the combined chronological output of stdout and stderr."""
        changed_id = get_pressed_buttons()
        current_output = self.buffer.getvalue()

        if "clear_console_button.n_clicks" in changed_id:
            self.clear()
        return current_output

    def restore_streams(self):
        """Restore original stdout and stderr streams."""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
