from django.utils.crypto import get_random_string

def seed_generator(length=81, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ9'):
	return get_random_string(length, allowed_chars)