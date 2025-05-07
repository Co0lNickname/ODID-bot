HELLO_TEXT = (
    '''
    Привет! Нажми на кнопку "Бросок" для определения хода
    '''
)

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
