class Config:
    """Configuration class for managing URL settings.
    
    This class stores configuration values used throughout the application,
    particularly the base URL for GitHub raw content delivery.

    :ivar values: Dictionary containing configuration key-value pairs
    :type values: dict
    
    **Configuration Keys**:
        * URL: Base URL for GitHub raw content delivery
    """

    values = {
      "URL": "https://cdn.githubraw.com/term-world/world-additions/main/"
    }
