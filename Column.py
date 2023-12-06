
class Column:
    """
    color : the color of the column, by default white 
    """
    def __init__(self, title, task_list, color=(255, 255, 255)):
        self.title = title
        self.task_list = task_list
        self.color = color
