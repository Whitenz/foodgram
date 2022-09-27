from rest_framework import status
from rest_framework.response import Response


def add_subscribe_to_user(user_from, user_to, linked_model, serializer, errors):
    obj, created = linked_model.objects.get_or_create(user_from=user_from,
                                                      user_to=user_to)
    if user_from == user_to:
        return Response(data=errors.get('add_to_yourself'),
                        status=status.HTTP_400_BAD_REQUEST)

    if created:
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)

    return Response(data=errors.get('already_exists'),
                    status=status.HTTP_400_BAD_REQUEST)


def del_subscribe_to_user(user_from, user_to, linked_model, errors):
    obj = linked_model.objects.filter(user_from=user_from,
                                      user_to=user_to).first()
    if obj:
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data=errors.get('not_exist'),
                    status=status.HTTP_400_BAD_REQUEST)
