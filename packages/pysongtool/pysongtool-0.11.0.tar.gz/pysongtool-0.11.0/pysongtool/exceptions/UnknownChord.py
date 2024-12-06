class UnknownChord(Exception):
    def __init__(self,root_note: str,chord:str):
        self.message = f"""
        {root_note}{chord} is not a valid chord for now
        """
    
    def __str__(self):
        return self.message