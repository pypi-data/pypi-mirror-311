class LinkerBot:
    """A simple SDK class with two utility methods."""
    
    def calculate_sum(self, a: int, b: int) -> int:
        """Calculate the sum of two numbers.
        
        Args:
            a (int): First number
            b (int): Second number
            
        Returns:
            int: Sum of the two numbers
        """
        return a + b
    
    def generate_greeting(self, name: str) -> str:
        """Generate a greeting message for the given name.
        
        Args:
            name (str): Name to include in the greeting
            
        Returns:
            str: Personalized greeting message
        """
        return f"Hello, {name}!"
