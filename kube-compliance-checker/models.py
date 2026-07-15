class Finding:
    def __init__(self, namespace, pod, container, standard, rule_id, severity, observed, expected):
        self.namespace = namespace
        self.pod = pod
        self.container = container
        self.standard = standard
        self.rule_id = rule_id
        self.severity = severity
        self.observed = observed
        self.expected = expected