from datetime import datetime
import typing


def truncate_string(s: str, size: int, suffix: str = '...') -> str:
    '''Образать строу до заданного размера и добавить суффикс'''
    if not s:
        return s
    if len(s) > size:
        return s[:size] + '...'
    return s


def isonow():
    '''Текщая дата и время в формате iso-8601 с часовым поясом'''
    return datetime.now().astimezone().isoformat()


def humanize_size(num, suffix='B'):
    '''Человекочитаемый размер в байтах

    См. https://stackoverflow.com/a/15485265
    '''
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f'{num:3.1f} {unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f} Yi{suffix}'


# @see https://stackoverflow.com/a/68249066/4498602
def value_from_list(target_list: list,
                    index: int,
                    default_value: typing.Any = None
                    ) -> typing.Any:
    '''Получить значение по индексу или значение по умолчанию'''
    try:
        return target_list[index]
    except IndexError:
        return default_value
