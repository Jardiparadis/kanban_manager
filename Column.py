class Column:
    """
    color : the color of the column, by default white 
    """
    def __init__(self, title, task_list, header_color, body_color):
        self.title = title
        self.task_list = task_list
        self.header_color = header_color
        self.body_color = body_color
        self.rect = None