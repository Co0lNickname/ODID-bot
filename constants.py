class BotTexts:
    class NotInGroupMessages:
        HELLO_TEXT = (
            "👋 Бот предназначен для групповых чатов, поэтому нельзя использовать его в личных сообщениях."
        )

    class DuringPlayMessages:
        CONFIRM_PARTICIPATION_TEXT = "❕Подтверди, чтобы стать участником игры"
        CONFIRMED_PARTICIPATION_TEXT = "✅ {player}, теперь ты участник игры"
        ALREADY_CONFIRMED_TEXT = "❌ {player}, ты уже стал участником игры"
        NOBODY_CONFIRMED_TEXT = "❌ Никто не подтвердил участие!"
        ALREADY_THROW_TEXT = "❌ Вы уже кидали {throw}"

    class MiddlewaresTexts:
        class AdminCheck:
            NO_RULES_ADD_IT_TEXT = "⚠️ У бота нет прав на удаление сообщений. Пожалуйста, добавьте эти права."
            NO_ADMIN_RULES_TEXT = "🚫 У бота нет прав администратора."
            ERROR_DURING_RULES_CHECK_TEXT = "❌ Ошибка при проверке прав доступа."

        class EnsureStarted:
            CONFIRM_PARTICIPATION_FIRST_TEXT = (
                "⚠️ Сначала нужно подтвердить участие и дождаться окончания расчета (/finish)."
            )


class LoggingMessages:
    class AdminCheck:
        ERROR_DURING_SEND_WARNING = "Ошибка при попытке отправить предупреждение: {error}"
        ERROR_DURING_RULES_CHECK = "Ошибка при проверке прав: {error}"


throw_actions = (
    'О/1', 'ДИ/1', 'Д/1',
    'О/2',' ДИ/2', 'Д/2',
    'О/3', 'ДИ/3', 'Д/3',
    'О/4', 'ДИ/4', 'Д/4',
    'О/5', 'ДИ/5', 'Д/5',
    'О/6', 'ДИ/6', 'Д/6'
)


class InvalidPlayersCountException(Exception):
    _msg = 'Ой-ой. Что-то не так с количеством игроков. Проверьте, что количество игроков от 2 до 6 человек'

    def __init__(self):
        super().__init__(self._msg)

    @property
    def msg(self):
        return self._msg


def get_throw_actions_for_players_count(players_count: int) -> tuple[str]:
    if not (2 <= players_count <= 6):
        raise InvalidPlayersCountException()

    return throw_actions[:(3 * players_count)]
