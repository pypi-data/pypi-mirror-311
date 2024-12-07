import re

class FieldValidator:
    # class to validate fields related to vehicle and user details.

    @staticmethod
    def validate_license_plate(license_plate_number: str, country_code='IE') -> bool:
        # Validate License Plate format based on country code. Default country is 'IE' (Ireland).
        # You can easily add support for more countries here.
        
        if country_code == 'IE':
            # Ireland License Plate Formats:
            # 1. Old format: 1234567 (Alphanumeric, 7 characters)
            # 2. New format: ABC-1234 or ABC 1234 (Alphanumeric, with or without hyphen, 7 to 9 characters)

            # Pattern for old format: 7 alphanumeric characters (no hyphen)
            old_pattern = r'^[A-Z0-9]{7}$'
            # Pattern for new format: 3 letters + hyphen + 4 digits (e.g., ABC-1234 or ABC 1234)
            new_pattern = r'^[A-Z]{3}-\d{4}$|^[A-Z]{3} \d{4}$'
            
            # Return True if it matches either the old format or the new format
            return bool(re.match(old_pattern, license_plate_number)) or bool(re.match(new_pattern, license_plate_number))

        elif country_code == 'IN':
            # India: License plate format e.g., KA-01-1234 (State Code-District Code-Vehicle Number)
            pattern = r'^[A-Z]{2}-\d{2}-\d{4}$'
            return bool(re.match(pattern, license_plate_number))

        # Invalid for unsupported country codes
        return False
    
    @staticmethod
    def validate_vehicle_number(vehicle_number: str, country_code='IE') -> bool:
        # Validate Vehicle Number format (Default: Ireland).
        # Ireland format: XX-XX-1234 (e.g., AB-01-1234)
        # India format: XX-XX-AB-1234 (e.g., KA-01-AB-1234)
        # You can easily add support for more countries here.

        if country_code == 'IE':
            # Format: Two uppercase letters, hyphen, two digits, another hyphen, and 4-digit number.
            pattern_ireland = r'^[A-Z]{2}-\d{2}-\d{4}$'
            return bool(re.match(pattern_ireland, vehicle_number))

        elif country_code == 'IN':
            # Format: Two uppercase letters, two digits, two uppercase letters, and 4-digit number.
            pattern_india = r'^[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}$'
            return bool(re.match(pattern_india, vehicle_number))

        # Invalid for unsupported country codes
        return False

    @staticmethod
    def validate_phone_number(phone_number: str, country_code='IE') -> bool:
        # Validate phone number format based on country code. Default country code is 'IE' (Ireland).
        # Valid Irish phone number +353123456789 or 0123456789
        # Valid Indian phone number +911234567890 or 0123456789
        # You can easily add support for more countries here.
        
        if country_code == 'IE':
            # Ireland: Phone number format starts with +353 or 0, followed by 9 digits
            pattern = r'^\+353\d{9}$|^0\d{9}$'
            return bool(re.match(pattern, phone_number))

        elif country_code == 'IN':
            # India: Phone number format starts with +91 or 0, followed by 10 digits
            pattern = r'^\+91\d{10}$|^0\d{10}$'
            return bool(re.match(pattern, phone_number))

        # Default: Invalid for unsupported country codes
        return False

    @staticmethod
    def validate_full_name(full_name: str) -> bool:
        #Validate that the full name contains only alphabetic characters and spaces.
        # A valid name should only contain letters and spaces, and each part should start with a capital letter.
        pattern = r'^[A-Z][a-z]*([ ]+[A-Z][a-z]*)*$'
        return bool(re.match(pattern, full_name))

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
