# Random OTP Generator

The `random-otp` package is a Python library for generating random OTPs of various types. It can generate numeric, alphabetic, or alphanumeric OTPs of a specified length.

## Installation

You can install `random-otp` using `pip`:

sh
pip install random-otp
## Usage

To use `random-otp`, you can import the `generate_numeric_otp`, `generate_alphabetic_otp`, and `generate_alphanumeric_otp` functions from the `random_otp.generator` module:

python
from random_otp.generator import generate_numeric_otp, generate_alphabetic_otp, generate_alphanumeric_otp

numeric_otp = generate_numeric_otp(6) # generates a 6-digit numeric OTP
alphabetic_otp = generate_alphabetic_otp(8) # generates an 8-character alphabetic OTP
alphanumeric_otp = generate_alphanumeric_otp(10) # generates a 10-character alphanumeric OTP
Alternatively, you can use the command line interface provided by the `random-otp-generator` script. To generate an OTP, run:

sh
random-otp-generator
You will be prompted to enter the length and type of OTP you want to generate.

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.