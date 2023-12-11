import random
from string import ascii_uppercase, digits

def generate_unique_code(size=10, chars=ascii_uppercase+digits):
	return "".join(random.choice(chars) for _ in range(size))