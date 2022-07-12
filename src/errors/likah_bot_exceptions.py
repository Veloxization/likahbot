"""Houses the custom errors for LikahBot"""

class NotDefined(Exception):
    """Called when a necessary parameter is not defined"""

    def __init__(self, missing_param: str):
        """Create a new NotDefined exception
        Args:
            missing_param: The parameter missing"""

        self.missing_param = missing_param
        self.message = f"The method is missing a necessary parameter: {missing_param}"
        super().__init__(self.message)
