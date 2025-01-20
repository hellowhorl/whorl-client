class Config:
  """Configuration class for managing URL settings.

    This class stores configuration values used throughout the application,
    particularly the base URL for GitHub raw content delivery.

    Attributes
    ----------
    values : dict
        Dictionary containing configuration key-value pairs
        
        Current keys:
            - URL: Base URL for GitHub raw content
    """

  values = {
    "URL": "https://cdn.githubraw.com/term-world/world-additions/main/"
  }
