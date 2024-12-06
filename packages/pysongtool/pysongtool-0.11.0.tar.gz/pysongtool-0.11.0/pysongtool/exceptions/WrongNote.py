class WrongNote(Exception):
    def __init__(self,root_note: str):
        self.message = f"""
        {root_note} is not a valid note\n
        use only standard and sharp notes (e.g. C,C#)
        """
    
    def __str__(self):
        return self.message