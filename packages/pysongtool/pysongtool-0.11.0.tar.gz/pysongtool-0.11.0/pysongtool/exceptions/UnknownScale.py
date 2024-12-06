class WrongScale(Exception):
    def __init__(self,root_note: str, scale_name: str):
        self.message = f"""
        {root_note}{scale_name} is not a valid scale\n
        use only standard and sharp notes (e.g. C,C#)
        """
    
    def __str__(self):
        return self.message