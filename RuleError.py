class RuleError(RuntimeError):
    def __init__(self, reason):
        RuntimeError.__init__(self, reason)
