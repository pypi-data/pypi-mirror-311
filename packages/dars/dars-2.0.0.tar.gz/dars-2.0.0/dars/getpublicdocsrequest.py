'''
Работа с содержательной частью информационных пакетов
запроса публичных документов
'''

import os
import uuid
import jinja2
import logging
import xml

from dars import datastructs as ds
from dars import (
        models,
        utils,
        xml as dxml,
        )

logger = logging.getLogger('dars')


def render(model: models.GetPublicDocsRequestModel) -> str:
    '''Сгенерировать тело запроса публичных документов

    Аргументы:
        model - модель параметров команды
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates')
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=path))
    if model.base == ds.Base.FZ44:
        template = env.get_template('getpublicdocsrequest44.xml.j2')
    elif model.base == ds.Base.FZ223:
        template = env.get_template('getpublicdocsrequest223.xml.j2')
    else:
        raise NotImplementedError
    template.globals['now'] = utils.isonow
    template.globals['uuid'] = uuid.uuid4
    return template.render(context=model)


def extract_archive_info(xmlstring: str,
                         base: ds.Base = ds.Base.FZ44
                         ) -> list[str]:
    '''Извлечь документы организаций

    Аргументы:
        xmlstring - xml-строка, содержащая пакет данных getPublicDocsRequest
    Результат:
        Список ссылок для скачивания
    '''
    try:
        obj = dxml.XmlObject(xmlstring, root_tag='Body/getPublicDocsResponse')
    except (xml.etree.ElementTree.ParseError, ValueError) as e:
        logger.error('Произошла ошибка при извлечении файла')
        logger.error(e)
        logger.error(xmlstring)
        return []
    # ---
    if base == ds.Base.FZ44:
        info_path = 'dataInfo/orgzanizations44DocsInfo/orgzanization44DocsInfo'
    elif base == ds.Base.FZ223:
        info_path = 'dataInfo/orgzanizations223DocsInfo/orgzanization223DocsInfo'  # noqa
    else:
        raise NotImplementedError
    info = []
    for el in obj.values(info_path):
        urls = [url.text for url in obj.values('archiveUrl', root=el)]
        info.extend(urls)
    return info
