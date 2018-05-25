class RuleError(RuntimeError):
    def __init__(self, reason):
        RuntimeError.__init__(self, reason)


class BorrowingExceededError(RuleError):
    def __init__(self):
        RuleError.__init__(self, "Number is borrowing books exceeded.")


class AlreadyBorrowedError(RuleError):
    def __init__(self):
        RuleError.__init__(self, "The book has already been borrowed.")