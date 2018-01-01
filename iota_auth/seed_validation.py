from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class IotaSeedValidator:

	def __init__(self, exact_length=81):
		self.exact_length = exact_length

	def validate(self, password, user=None):
		# Check if length is less than 81 Characters
		if len(password) < self.exact_length:
			raise ValidationError(
				_("This seed must contain at least %(exact_length)d characters. The entered seed is to short"),
				code='password_too_short',
				params={'exact_length': self.exact_length},
				)
		# Check if length is greater than 81 Characters
		if len(password) > self.exact_length:
			raise ValidationError(
				_("This seed must contain exactly %(exact_length)d characters. The entered seed is to long"),
				code='password_too_long',
				params={'exact_length': self.exact_length},
				)
		# Check if any of the characters are lower case
		for char in password:
			if char.islower():
				raise ValidationError(
					_("This seed must contain all upper case Latin characters."),
					code='password_contains_lower_case',
					)
		# Check if any of the characters are digits 0-8
		banned_digits = ['0','1','2','3','4','5','6','7','8']
		for digit in banned_digits:
			if digit in password:
				raise ValidationError(
					_("This seed can only contain the letter 9, please remove all letters 0 to 8."),
					code='password_contains_forbidden_digits',
					)
		# Check the password contains a 9
		approved_digit = ['9']
		if approved_digit[0] not in password:
			raise ValidationError(
				_("This seed must contain the letter 9 at least once."),
				code='password_does_not_contains_nine',
				)		

	def get_help_text(self):
		if self.code == 'password_too_short':
			return _("Your password must contain exactly %(exact_length)d characters." % {'exact_length': self.exact_length})
		elif self.code == 'password_too_long':
			return _("This seed must contain exactly %(exact_length)d characters. The entered seed is to long" % {'exact_lenght':self.exact_length})
		elif self.code == 'password_contains_lower_case':
			return _("This seed must contain all upper case Latin characters.")
		else:
			return _("This seed must contain the letter 9 at least once.")