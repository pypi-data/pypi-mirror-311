'''
Работа с содержательной частью информационных пакетов
"Запрос формирования в ХД архивов с документами по реестровому номеру"
'''

import os
import uuid
import jinja2
import logging
import xml

from dars import (
        models,
        utils,
        xml as dxml,
        )

logger = logging.getLogger('dars')


def render(model: models.GetDocsByReestrNumberRequestModel) -> str:
    '''Сгенерировать тело запроса

    Аргументы:
        model - модель параметров команды
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates')
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=path))
    template = env.get_template('getdocsbyreestrnumberrequest.xml.j2')
    template.globals['now'] = utils.isonow
    template.globals['uuid'] = uuid.uuid4
    return template.render(context=model)


def extract_archive_info(xmlstring: str) -> list[str]:
    '''Извлечь ссылки для скачивания документов из архива

    Аргументы:
        xmlstring - xml-строка, содержащая
            пакет данных getDocsByReestrNumberResponse
    Результат:
        Список ссылок для скачивания
    '''
    try:
        obj = dxml.XmlObject(
                xmlstring,
                root_tag='Body/getDocsByReestrNumberResponse/dataInfo')
    except (xml.etree.ElementTree.ParseError, ValueError) as e:
        logger.error('Произошла ошибка при извлечении файла')
        logger.error(e)
        return []
    # ---
    info = []
    for el in obj.values('.'):
        urls = [url.text for url in obj.values('archiveUrl', root=el)]
        info.extend(urls)
    return info
