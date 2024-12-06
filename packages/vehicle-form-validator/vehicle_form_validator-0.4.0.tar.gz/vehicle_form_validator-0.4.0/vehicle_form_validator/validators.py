import re

class FieldValidator:
    # class to validate fields related to vehicle and user details.
    @staticmethod
    def validate_vehicle_type(vehicle_type: str) -> bool:
        # Validate vehicle type, you can add additonal types in future
        valid_types = ['car', 'truck', 'motorcycle', 'bus', 'van', 'bike', 'cycle', 'train']
        return vehicle_type.lower() in valid_types

    @staticmethod
    def validate_vehicle_make(vehicle_make: str) -> bool:
        # Validate vehicle make, it must contain only alphabetic characters
        return vehicle_make.isalpha()

    @staticmethod
    def validate_vehicle_model(vehicle_model: str) -> bool:
        # Validate vehicle model, is a non-empty string and within length limits
        return 1 <= len(vehicle_model) <= 20

    @staticmethod
    def validate_license_plate(license_plate_number: str, country_code='IE') -> bool:
        # Validate license plate format based on country code
        # Default country code is 'IE' for Ireland if not provided
        # You can easily add additional countrys in future
        if country_code == 'IE':
            # Ireland, License plates may be alphanumeric, 7-9 characters long and must contain atleast one "-" (hyphen)
            pattern = r'^(?=.*-)[A-Za-z0-9-]{7,9}$'
            return bool(re.match(pattern, license_plate_number))
        
        elif country_code == 'UK':
            # UK: License plates have format like ABC 1234 or AB12 CDE
            pattern = r'^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$|^[A-Z]{3}\s?[0-9]{3}$'
            return bool(re.match(pattern, license_plate_number))
        
        elif country_code == 'US':
            # US: License plates may contain 1-7 alphanumeric characters (e.g., ABC 1234, or 123 ABC)
            pattern = r'^[A-Za-z0-9]{1,7}$'
            return bool(re.match(pattern, license_plate_number))

        # Default: Invalid for unsupported country codes
        return False

    @staticmethod
    def validate_phone_number(phone_number: str, country_code='IE') -> bool:
        # Validate phone number format based on country code
        # Default country code is 'IE' for Ireland if not provided
        # You can easily add additional countrys in future
        if country_code == 'IE':
            # Ireland: Phone number format starts with +353 or 0, followed by 9 digits
            pattern = r'^\+353\d{9}$|^0\d{9}$'
            return bool(re.match(pattern, phone_number))
        
        elif country_code == 'UK':
            # UK: Phone number format starts with +44 or 0, followed by 10 digits
            pattern = r'^\+44\d{10}$|^0\d{10}$'
            return bool(re.match(pattern, phone_number))
        
        elif country_code == 'US':
            # US: Phone number format starts with +1 or 1, followed by 10 digits
            pattern = r'^\+1\d{10}$|^1\d{10}$'
            return bool(re.match(pattern, phone_number))

        # Default: Invalid for unsupported country codes
        return False

    @staticmethod
    def validate_email(email: str) -> bool:
        # Validate email using a regex pattern
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password(password: str, confirm_password: str) -> tuple:
        # Validate password according to certain criteria
        # Returns a tuple (is_valid, message)
        # You can add customized checks in the future

        # Check password length (min 8 characters)
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        
        # Check if the password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter."
        
        # Check if the password contains at least one digit
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit."
        
        # Check if the password contains at least one special character (optional)
        special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/~"
        if not any(char in special_characters for char in password):
            return False, "Password must contain at least one special character."

        # Check if password and confirm password match
        if password != confirm_password:
            return False, "Passwords do not match."

        return True, "Password is valid."

    @staticmethod
    def validate_full_name(full_name: str) -> bool:
        #Validate that the full name contains only alphabetic characters and spaces.
        # A valid name should only contain letters and spaces, and each part should start with a capital letter.
        pattern = r'^[A-Z][a-z]*([ ]+[A-Z][a-z]*)*$'
        return bool(re.match(pattern, full_name))