from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
	user_token = {}
	refresh_token = RefreshToken.for_user(user)
	user_token["username"] = user.username
	user_token["access_token"] = str(refresh_token.access_token)
	user_token["refresh_token"] = str(refresh_token)
	return user_token