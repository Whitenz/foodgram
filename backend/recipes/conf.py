# имя поля ошибки при ошибочном запросе к методу "favorite"
name_of_error_field = 'errors'
# словарь с описанием возможных ошибок при запросе к методу "favorite"
favorite_errors = {
    'already_exists': {
        name_of_error_field: 'Вы уже добавили этот рецепт в избранное.'
    },
    'not_exist': {
        name_of_error_field: 'Вы не добавляли этот рецепт в избранное.'
    },
}
