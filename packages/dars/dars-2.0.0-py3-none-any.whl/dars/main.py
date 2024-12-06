'''Входная точка бизнес-логии модуля'''

import os
import logging
import requests
import time
import re
import threading

import xml.dom.minidom

from concurrent import futures

from dars import (
        config,
        errors,
        getnsirequest,
        getpublicdocsrequest,
        getdocsbyreestrnumberrequest,
        getdocsbyorgregionrequest,
        models,
        s3_repo,
        utils,
        )

logger = logging.getLogger('dars')

REQUEST_RETRIES = 5

TRIM_REQUEST_LOG = 4096
TRIM_RESPONSE_LOG = 4096


class Client:
    '''Клинетский класс для доступа к бизнес-логике'''

    def __init__(self, settings: config.Settings):
        self.settings = settings
        self.repo = s3_repo.S3Repo(self.settings.s3)
        # --- индекс обработанных файлов
        self.filename_index = {}
        self.lock = threading.Lock()

    def getNsiRequest(self, **kwargs):
        '''Загрузить справочники НСИ'''
        self.params = models.GetNsiRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getnsirequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        for (_, url) in getnsirequest.extract_archive_info(response_text):
            self._process_response_link(url, upload=self.params.upload)

    def getDocsByReestrNumberRequest(self, **kwargs):
        '''Запрос архивов с документами по реестровому номеру'''
        self.params = models.GetDocsByReestrNumberRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getdocsbyreestrnumberrequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        # ---
        urls = getdocsbyreestrnumberrequest.extract_archive_info(
                response_text,
                )
        if not urls:
            return
        time.sleep(self.params.delay_before_download)
        for url in urls:
            self._process_response_link(url, upload=self.params.upload)

    def getDocsByOrgRegionRequest(self, **kwargs):
        '''Запрос архивов по региону заказчика и типу документа'''
        self.params = models.GetDocsByOrgRegionRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getdocsbyorgregionrequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        # ---
        urls = getdocsbyorgregionrequest.extract_archive_info(
                response_text,
                )
        if not urls:
            return
        time.sleep(self.params.delay_before_download)
        for url in urls:
            self._process_response_link(url, upload=self.params.upload)

    def getPublicDocsRequest(self, **kwargs):
        '''Загрузить публичные документы'''
        self.params = models.GetPublicDocsRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getpublicdocsrequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        # ---
        urls = getpublicdocsrequest.extract_archive_info(
                response_text,
                base=self.params.base
                )
        if not urls:
            return
        if self.params.jobs == 1:
            for url in urls:
                self._process_response_link(url, upload=self.params.upload)
        else:
            self.multiprocess_requests(
                    urls,
                    self.params.jobs,
                    self.params.upload
                    )

    def multiprocess_requests(
            self,
            urls: list[str],
            workers: int,
            upload: bool = True
            ):
        '''Обработать ссылки в мульти-процессном режиме

        Args:
            urls - список адресов для скачивания файлов
            workers - количество потоков
        '''
        with futures.ThreadPoolExecutor(max_workers=workers) as executor:
            for url in urls:
                executor.submit(self._process_response_link, url, upload)

    def _process_response_link(self, url: str, upload: bool = False):
        '''Обработать ссылку из СОИ

        Ссылка, полученная из СОИ, указывает на архив документов.
        Му получаем имя файла, проверяем наличие файла в ФС и S3,
        загружаем файл в S3

        Args:
            url - ссылка
            upload - выгружаем полученные файлы в S3
        '''
        filename = self._get_remote_filename(url)
        if not filename:
            return
        # --- проверяем на дублирование имени файла
        filename = self._correct_duplication(filename)
        # --- проверяем существование файла в S3 (только при условии,
        #     что файл надо выгружать в S3)
        if upload:
            if self.repo.exists(filename, prefix=self.params.prefix):
                logger.info(
                        '           %s уже существует, пропускаем.',
                        os.path.join(self.params.prefix, filename)
                        )
                return
        # --- проверяем существование файла в файловой системе
        download_dir = self.params.base_settings.download_dir
        file_path = os.path.join(download_dir, filename)
        if os.path.exists(file_path):
            pass
        else:
            # --- загружаем файл из СОИ в ФС
            self._download_file(url, file_path)
        # ---
        if not os.path.exists(file_path):
            logger.error(f'Ошибка сохранения файла {file_path}')
            return
        size = utils.humanize_size(os.path.getsize(file_path))
        logger.info('%10s %s/%s', size, self.params.prefix, filename)
        # --- выгружаем файл из ФС в S3
        if upload:
            self.repo.put_file(file_path, prefix=self.params.prefix)

    def _make_request(self, body: str) -> str:
        '''Выполнить запрос к СОИ

        Args:
            body - тело запроса
        Returns:
            Текст ответа
        '''
        logger.debug(
                'Выполнение запроса на %s',
                self.params.base_settings.url
                )
        logger.debug(utils.truncate_string(body, TRIM_REQUEST_LOG))
        response = self._make_repeated_request(
                'POST',
                url=self.params.base_settings.url,
                data=body,
                timeout=60
                )
        logger.debug('HTTP код ответа: %s', response.status_code)
        logger.debug(response.headers)
        logger.debug(
                utils.truncate_string(
                    xml.dom.minidom.parseString(response.text).toprettyxml(),
                    TRIM_RESPONSE_LOG
                    )
                )
        if response.status_code != 200:
            logger.error(
                    'СОИ вернул неожиданный статус ответа '
                    f'{response.status_code}'
                    )
            logger.error(response.text)
            return None
        return response.text

    def _download_file(self, url: str, file_path: str) -> str:
        '''Скачать файл

        Args:
            url - ссылка для скачивания
            file_path - полный путь к файлу
        Return:
            Полный путь файла в файловой системе
        raises:
            EisClientUnexpectedStatus - СОИ вернул не 200
        '''
        download_dir = os.path.dirname(file_path)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        # ---
        response = self._make_repeated_request(
                'GET',
                url=url,
                timeout=60
                )
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        raise errors.EisClientUnexpectedStatus(response.status_code)

    def _get_remote_filename(self, url: str) -> str:
        '''Получить имя файла без скачивания'''
        response = self._make_repeated_request(
                'HEAD',
                url=url,
                timeout=60
                )
        code = response.status_code
        if code != 200:
            logger.error(f'Неожиданный статус при запросе имени файла {code}')
            logger.error(response.text)
            logger.error(url)
            return None
        content_disposition = response.headers.get('content-disposition')
        if not content_disposition:
            logger.error(f'Ошибка при получении имени файла {url}')
            return None
        filename = content_disposition.split('=')[1][1:-1]
        return filename

    def _correct_duplication(self, filename: str) -> str:
        '''Скорректировать имя файла с учетом возможного дублирования

        В рамках одной сессии могут быть получены одинаковые имена файлов
        с различным содержанием. Необходимо вести учет обработанных файлов
        и индекс повторяемости. В случае дублирования, индекс увеличивается
        на единицу и добавляется в имя
        filename.zip
        filename_2.zip
        filename_3.zip
        '''
        with self.lock:
            index = self.filename_index.get(filename)
            if not index:
                self.filename_index[filename] = 1
                return filename
            index = index + 1
            self.filename_index[filename] = index
            base_name, extension = os.path.splitext(filename)
            new_filename = base_name + '_' + str(index).zfill(2) + extension
            return new_filename

    def _make_repeated_request(self, verb: str, **kwargs
                               ) -> requests.Response | None:
        '''Выполнить запрос с повтором при ошибке'''
        # --- выполняем подмену префикса, если задана соответствующая
        #     конфигурация
        if self.params.settings.url_prefix_substitution:
            for sub_item in self.params.settings.url_prefix_substitution:
                if kwargs['url'].startswith(sub_item['source']):
                    kwargs['url'] = re.sub(
                            '^' + sub_item['source'],
                            sub_item['dest'],
                            kwargs['url']
                            )
                    break
        # ---
        for _ in range(REQUEST_RETRIES):
            try:
                return requests.request(verb, **kwargs)
            except requests.exceptions.RequestException as e:
                logger.error(e)
                last_exception = e
                time.sleep(5)
        raise last_exception
