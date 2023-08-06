from lime_trader.models.errors import Error


class ApiError(Exception):
    """
    Exception thrown if error is returned from API
    """

    def __init__(self, error: Error):
        """
        Args:
            error: Error object containing details returned from API
        """
        self.error = error
        super().__init__()

    def __repr__(self):
        return self.error

    def __str__(self):
        return str(self.error)
