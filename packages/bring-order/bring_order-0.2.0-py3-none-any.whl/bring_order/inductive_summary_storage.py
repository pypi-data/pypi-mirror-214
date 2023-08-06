import uuid

class InductiveSummary:
    """ Class that stores data from the inductive analysis
    """
    def __init__(self):
        self.summaries = []

    def add(self,id, cell_number, data):
        self.summaries.append({'id':id,'cell_number':cell_number, 'data': data })
