import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.serv_info import SERV_NAME
from main.const_data.template_errors import *
from main.models import *
from main.parsers import *


@method_decorator(csrf_exempt, name='dispatch')
class UploadFile(View):
    def post(self, request):
        token = get_token(request)
        need_user = AppUser.objects.filter(token_data=token).first()
        if need_user:
            files = request.FILES
            if 'file' in files:
                avatar = files['file']

                need_user.avatar = avatar
                need_user.save(update_fields=['avatar'])
                output_data = {
                    'path': str(need_user.avatar.url),
                    'baseURL': SERV_NAME
                }
                return JsonResponse(output_data, status=200)
            else:
                return JsonResponse(NO_FILE_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsView(View):
    def get(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)

            if need_user.authority == 1:
                roles = Role.objects.filter(author_id=need_user)

                serialized_data = serialize('python', roles)

                count_of_instance = roles.count()

                instance_output_list_of_dicts = list(dict())
                for i in range(count_of_instance):

                    id = serialized_data[i]['pk']
                    fields_dict = serialized_data[i]['fields']
                    fields_dict['id'] = id

                    if fields_dict['percentage'] is None:
                        instance_output_list_of_dicts.append({'id': id,
                                                              'name': fields_dict['name'],
                                                              'description': fields_dict['description'],
                                                              'color': fields_dict['color'],
                                                              'amount': fields_dict['amount']
                                                              })

                    if fields_dict['amount'] is None:
                        instance_output_list_of_dicts.append({'id': id,
                                                              'name': fields_dict['name'],
                                                              'description': fields_dict['description'],
                                                              'color': fields_dict['color'],
                                                              'percentage': fields_dict['percentage']
                                                              })
                roles_dict = {
                    "roles": instance_output_list_of_dicts
                }

                output_data = roles_dict

                return JsonResponse(output_data, status=200)
            else:
                output_data = {'roles': {}}

                return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def post(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            if AppUser.objects.get(token_data=token).authority == 1:
                post_body = json.loads(request.body)

                author_id = AppUser.objects.get(token_data=token)

                name = post_body.get('name')
                description = post_body.get('description')
                color = post_body.get('color')
                percentage = post_body.get('percentage')
                amount = post_body.get('amount')

                if percentage is not None and amount is not None:
                    return JsonResponse(DUPLICATION_AMOUNT_PERCENTAGE_DATA, status=404)

                elif percentage is not None and amount is None:
                    data_to_create = {
                        'name': name,
                        'description': description,
                        'color': color,
                        'percentage': percentage,
                        'amount': None,
                        'author_id': author_id
                    }
                    new_role = Role.objects.create(**data_to_create)
                    data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'percentage': new_role.percentage,
                    }
                    return JsonResponse(data, status=200)

                elif amount is not None and percentage is None:
                    data_to_create = {
                        'name': name,
                        'description': description,
                        'color': color,
                        'percentage': None,
                        'amount': amount,
                        'author_id': author_id,
                    }
                    new_role = Role.objects.create(**data_to_create)
                    data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'amount': new_role.amount,
                    }
                    return JsonResponse(data, status=200)

            else:
                return JsonResponse(USER_NOT_A_SUB_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def patch(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)

            patch_body = json.loads(request.body)
            name = patch_body.get('name')
            email = patch_body.get('email')
            phone = patch_body.get('phone')
            # avatar = patch_body.get('avatar')
            bio = patch_body.get('bio')
            authority = patch_body.get('authority')

            social_list = patch_body.get('social')

            if social_list is not None:
                for i in range(len(social_list)):
                    name_social = social_list[i]['name']
                    url = social_list[i]['url']

                    social_network = SocialNetwork.objects.get(name=name_social)

                    if not Social.objects.filter(user_id=need_user, social_network_id=social_network):
                        Social.objects.create(user_id=need_user, social_network_id=social_network, url=url)

                    else:
                        social_instance = Social.objects.get(user_id=need_user, social_network_id=social_network)
                        social_instance.url = url
                        social_instance.save(update_fields=['url'])

            fields_to_update = []

            if name is not None:
                need_user.name = name
                fields_to_update.append('name')

            if email is not None:
                if not AppUser.objects.filter(email=email):
                    need_user.email = email
                    fields_to_update.append('email')

                else:
                    if need_user.email != email:
                        return JsonResponse(USER_EXIST_EMAIL, status=404)

            if phone is not None:
                if not AppUser.objects.filter(phone=phone):
                    need_user.phone = phone
                    fields_to_update.append('phone')
                else:
                    return JsonResponse(USER_EXIST_PHONE, status=404)

            # if avatar is not None:
            #     need_user.avatar = File(avatar)
            #     fields_to_update.append('avatar')

            if bio is not None:
                need_user.bio = bio
                fields_to_update.append('bio')

            if authority is not None:
                need_user.authority = authority
                need_user.save(update_fields=['authority'])
                # fields_to_update.append('authority')

            need_user.save(update_fields=fields_to_update)

            socials_user = Social.objects.filter(user_id=need_user)

            serialized_data = serialize('python', socials_user)

            instance_output_list_of_dicts = []
            for social_network in serialized_data:
                fields_dict = social_network['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network_id']).name,
                    'url': fields_dict['url']

                })

            avatar = None if not need_user.avatar else SERV_NAME + str(need_user.avatar.url)

            data = {
                'id': need_user.id,
                'name': need_user.name,
                'email': need_user.email,
                'phone': need_user.phone,
                'avatar': avatar,
                'bio': need_user.bio,
                'social': instance_output_list_of_dicts,
                'authority': need_user.authority
            }
            return JsonResponse(data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def delete(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            AppUser.objects.get(token_data=token).delete()

            return JsonResponse(DELETE_SUCCESS_DATA, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def get(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)

            avatar = None if not need_user.avatar else SERV_NAME + str(need_user.avatar.url)

            socials_user = Social.objects.filter(user_id=need_user)

            serialized_data = serialize('python', socials_user)

            count_of_instance = socials_user.count()

            instance_output_list_of_dicts = []
            for i in range(count_of_instance):
                fields_dict = serialized_data[i]['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network_id']).name,
                    'url': fields_dict['url']

                })

            data = {
                'id': need_user.id,
                'name': need_user.name,
                'email': need_user.email,
                'phone': need_user.phone,
                'avatar': avatar,
                'bio': need_user.bio,
                'social': instance_output_list_of_dicts,
                'authority': need_user.authority,
            }

            return JsonResponse(data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class UserViewForIndexInEnd(View):
    def patch(self, request, role_id):
        token = get_token(request)

        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)

            if Role.objects.filter(id=role_id):
                role_instance = Role.objects.get(id=role_id)

                if role_instance.author_id == user:

                    patch_body = json.loads(request.body)
                    name = patch_body.get('name')
                    description = patch_body.get('description')
                    color = patch_body.get('color')
                    percentage = patch_body.get('percentage')
                    amount = patch_body.get('amount')

                    if name is not None:
                        if role_instance.is_base:
                            return JsonResponse(FORBIDDEN_CHANGE_BASE_ROLE_NAME, status=404)

                        else:
                            role_instance.name = name
                            role_instance.save(update_fields=['name'])

                    if description is not None:
                        role_instance.description = description
                        role_instance.save(update_fields=['description'])

                    if color is not None:
                        role_instance.color = color
                        role_instance.save(update_fields=['color'])

                    if percentage is not None and amount is not None:
                        return JsonResponse(DUPLICATION_AMOUNT_PERCENTAGE_DATA, status=404)

                    elif percentage is not None and amount is None:
                        if role_instance.amount is not None:
                            role_instance.amount = None
                        role_instance.percentage = percentage
                        role_instance.save(update_fields=['amount', 'percentage'])

                    elif amount is not None and percentage is None:
                        if role_instance.percentage is not None:
                            role_instance.percentage = None
                        role_instance.amount = amount
                        role_instance.save(update_fields=['amount', 'percentage'])

                    if role_instance.percentage is not None:
                        data = {
                            'id': role_instance.id,
                            'name': role_instance.name,
                            'description': role_instance.description,
                            'color': role_instance.color,
                            'percentage': role_instance.percentage
                        }
                        return JsonResponse(data, status=200)

                    if role_instance.amount is not None:
                        data = {
                            'id': role_instance.id,
                            'name': role_instance.name,
                            'description': role_instance.description,
                            'color': role_instance.color,
                            'amount': role_instance.amount
                        }
                        return JsonResponse(data, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def delete(self, request, role_id):
        token = get_token(request)
        user = AppUser.objects.filter(token_data=token).first()

        if user:
            if Role.objects.filter(id=role_id):
                role_to_delete = Role.objects.get(id=role_id)

                if role_to_delete.author_id == user:
                    role_to_delete.delete()

                    return JsonResponse(DELETE_SUCCESS_DATA, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePhone(View):
    def post(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)
            post_body = json.loads(request.body)
            phone = post_body.get('phone')

            if not AppUser.objects.filter(phone=phone):
                need_user.phone = phone
                need_user.save(update_fields=['phone'])
                return JsonResponse(SUCCESS_CHANGE_PHONE, status=200)
            else:
                return JsonResponse(USER_EXIST_PHONE, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)