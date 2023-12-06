
class Task:
    def __init__(self, title, description, creator, assignee,
                 creation_date, theoric_completion_date="", completion_date="",
                 label="", priority="", status="", rect=None):
        self.title = title
        self.description = description
        self.creator = creator
        self.assignee = assignee
        self.creation_date = creation_date
        self.theoric_completion_date = theoric_completion_date
        self.completion_date = completion_date
        self.label = label
        self.priority = priority
        self.status = status
        self.rect = rect 
        self.moving = False # drag&drop
    
