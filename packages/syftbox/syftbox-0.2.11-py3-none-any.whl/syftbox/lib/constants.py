from pathlib import Path

# Default port for the SyftBox client
DEFAULT_PORT = 8080

# Default SyftBox cache server URL for the client
DEFAULT_SERVER_URL = "https://syftbox.openmined.org"

# Default configuration directory for the client
DEFAULT_CONFIG_DIR = Path(Path.home(), ".syftbox")

# Default configuration file path for the client
DEFAULT_CONFIG_PATH = Path(DEFAULT_CONFIG_DIR, "config.json")

# Default logs directory for the client
DEFAULT_LOGS_DIR = Path(DEFAULT_CONFIG_DIR, "logs")

# Default data directory for the client
DEFAULT_DATA_DIR = Path(Path.home(), "SyftBox")

# Permissions file name
PERM_FILE = "_.syftperm"

SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"
