"""
Text generators for SynGen.

This module provides generators for various text data types
such as emails, phone numbers, addresses, and names.
"""

import numpy as np
import random
import string
from typing import Dict, Any, List


class TextGenerator:
    """Generator for text data types."""
    
    def __init__(self):
        """Initialize the text generator."""
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna",
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
        ]
        
        self.domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
            "icloud.com", "protonmail.com", "mail.com", "yandex.com", "zoho.com"
        ]
        
        self.street_names = [
            "Main", "Oak", "Pine", "Elm", "Cedar", "Maple", "Washington", "Lake", "Hill",
            "Park", "Spring", "North", "South", "East", "West", "River", "Forest", "Meadow",
            "Sunset", "Sunrise", "Valley", "Mountain", "Ocean", "Beach", "Garden", "Plaza"
        ]
        
        self.street_types = [
            "Street", "Avenue", "Road", "Boulevard", "Drive", "Lane", "Court", "Place",
            "Way", "Circle", "Terrace", "Highway", "Expressway", "Freeway"
        ]
        
        self.cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
            "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
            "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
            "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit"
        ]
        
        self.states = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
            "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
            "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
            "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
    
    def generate_emails(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate email addresses."""
        emails = []
        
        for _ in range(n_samples):
            # Generate name
            first_name = random.choice(self.first_names).lower()
            last_name = random.choice(self.last_names).lower()
            
            # Generate email format
            format_type = parameters.get('format', 'first.last')
            
            if format_type == 'first.last':
                email = f"{first_name}.{last_name}"
            elif format_type == 'firstlast':
                email = f"{first_name}{last_name}"
            elif format_type == 'first_last':
                email = f"{first_name}_{last_name}"
            elif format_type == 'first':
                email = first_name
            else:
                email = f"{first_name}.{last_name}"
            
            # Add random numbers
            if parameters.get('add_numbers', False):
                email += str(random.randint(1, 999))
            
            # Add domain
            domain = random.choice(self.domains)
            email = f"{email}@{domain}"
            
            emails.append(email)
        
        return np.array(emails)
    
    def generate_phones(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate phone numbers."""
        phones = []
        format_type = parameters.get('format', 'us')
        
        for _ in range(n_samples):
            if format_type == 'us':
                # US format: (XXX) XXX-XXXX
                area_code = random.randint(200, 999)
                prefix = random.randint(200, 999)
                line_number = random.randint(1000, 9999)
                phone = f"({area_code}) {prefix}-{line_number}"
            elif format_type == 'international':
                # International format: +1-XXX-XXX-XXXX
                country_code = random.randint(1, 99)
                area_code = random.randint(10, 999)
                prefix = random.randint(100, 999)
                line_number = random.randint(1000, 9999)
                phone = f"+{country_code}-{area_code}-{prefix}-{line_number}"
            else:
                # Simple format: XXX-XXX-XXXX
                area_code = random.randint(100, 999)
                prefix = random.randint(100, 999)
                line_number = random.randint(1000, 9999)
                phone = f"{area_code}-{prefix}-{line_number}"
            
            phones.append(phone)
        
        return np.array(phones)
    
    def generate_addresses(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate street addresses."""
        addresses = []
        
        for _ in range(n_samples):
            # Generate house number
            house_number = random.randint(1, 9999)
            
            # Generate street name
            street_name = random.choice(self.street_names)
            street_type = random.choice(self.street_types)
            
            # Generate city and state
            city = random.choice(self.cities)
            state = random.choice(self.states)
            
            # Generate zip code
            zip_code = random.randint(10000, 99999)
            
            # Format address
            address = f"{house_number} {street_name} {street_type}, {city}, {state} {zip_code}"
            addresses.append(address)
        
        return np.array(addresses)
    
    def generate_names(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate full names."""
        names = []
        format_type = parameters.get('format', 'first_last')
        
        for _ in range(n_samples):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            
            if format_type == 'first_last':
                name = f"{first_name} {last_name}"
            elif format_type == 'last_first':
                name = f"{last_name}, {first_name}"
            elif format_type == 'first_middle_last':
                middle_name = random.choice(self.first_names)
                name = f"{first_name} {middle_name} {last_name}"
            else:
                name = f"{first_name} {last_name}"
            
            names.append(name)
        
        return np.array(names)
    
    def generate_strings(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate random strings."""
        strings = []
        
        min_length = parameters.get('min_length', 5)
        max_length = parameters.get('max_length', 15)
        use_letters = parameters.get('use_letters', True)
        use_numbers = parameters.get('use_numbers', True)
        use_special = parameters.get('use_special', False)
        
        # Build character set
        chars = ""
        if use_letters:
            chars += string.ascii_letters
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation
        
        if not chars:
            chars = string.ascii_letters
        
        for _ in range(n_samples):
            length = random.randint(min_length, max_length)
            string_value = ''.join(random.choice(chars) for _ in range(length))
            strings.append(string_value)
        
        return np.array(strings) 