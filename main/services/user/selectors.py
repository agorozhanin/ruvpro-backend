from main.models import AppUser


def is_sub_user(user: AppUser) -> bool:
    return True if user.authority == 1 else False


def get_app_user_by_token(token: str):
    return AppUser.objects.filter(token_data=token).first()


def is_exist_user_phone(phone: str):
    return True if AppUser.objects.filter(phone=phone) else False


def get_app_user_by_id(id: int):
    return AppUser.objects.filter(id=id).first()
