# имя поля ошибки при ошибочном запросе к методу "subscribe"
name_of_error_field = 'errors'
# словарь с описанием возможных ошибок при запросе к методу "subscribe"
subscription_errors = {
    'add_to_yourself': {
        name_of_error_field: 'Нельзя оформить подписку на себя.'
    },
    'already_exists': {
        name_of_error_field: 'Вы уже оформили подписку на этого пользователя.'
    },
    'not_exist': {
        name_of_error_field: 'Вы не подписаны на этого пользователя.'
    },
}
