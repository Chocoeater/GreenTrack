from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для получения JWT токена.

    Добавляет email, username, user_id в payload токена
    и обновляет last_login после успешного входа.
    """
    @classmethod
    def get_token(cls, user):
        """
        Генерирует токен с добавленным полем email.

        Parameters
        ----------
        user : User
            Пользователь, для которого создается токен.

        Returns
        -------
        RefreshToken
            JWT токен пользователя.
        """
        token = super().get_token(user)

        token["user_id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["timezone"] = user.timezone

        return token