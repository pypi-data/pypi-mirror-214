import string
import random

def generate_otp(length, characters):
    """
    Generates a random OTP of the specified length using the given characters.
    """
    return ''.join(random.choice(characters) for i in range(length))

def generate_numeric_otp(length):
    """
    Generates a random numeric OTP of the specified length.
    """
    return generate_otp(length, string.digits)

def generate_alphabetic_otp(length):
    """
    Generates a random alphabetic OTP of the specified length.
    """
    return generate_otp(length, string.ascii_letters)

def generate_alphanumeric_otp(length):
    """
    Generates a random alphanumeric OTP of the specified length.
    """
    return generate_otp(length, string.digits + string.ascii_letters)

# Example usage
if __name__ == '__main__':
    length = int(input("Enter the length of the OTP: "))
    otp_type = input("Enter 'n' for numeric, 'a' for alphabetic, or 'an' for alphanumeric OTP: ")

    if otp_type == 'n':
        otp = generate_numeric_otp(length)
    elif otp_type == 'a':
        otp = generate_alphabetic_otp(length)
    elif otp_type == 'an':
        otp = generate_alphanumeric_otp(length)
    else:
        print("Invalid input. Please enter 'n', 'a', or 'an'.")
        exit()

    print(f"Your OTP is: {otp}")