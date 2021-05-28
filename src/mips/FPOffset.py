class FPOffset:
    """
    Holds the frame pointer offset. This is used to update the references after the function has been generated,
    because we don't know the frame pointer offset beforehand.
    """

    def __init__(self, index):
        self.value = None
        self.index = index

    def set_value(self, value):
        self.value = value

    def get_value(self):
        assert self.value is not None, "The frame pointer offset has not yet been given a literal value"
        return self.value
