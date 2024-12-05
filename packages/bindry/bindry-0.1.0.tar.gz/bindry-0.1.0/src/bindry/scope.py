class Scope:
    """
    Defines the lifecycle scope for components in the Dependency Injection system.

    Attributes:
        SINGLETON: A single instance is shared across the application.
        PROTOTYPE: A new instance is created for each request.
    """

    SINGLETON = "singleton"
    PROTOTYPE = "prototype"
