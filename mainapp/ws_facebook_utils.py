from users.models import CustomUser

def retrieve_instagram_user_id(user):
    user_instance = CustomUser.objects.get(email=user.email)
    return user_instance.instagram_user_id


