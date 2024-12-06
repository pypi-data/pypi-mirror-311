from datetime import (
        datetime,
        date,
        )

import csv
import os
import pathlib
from typing import Annotated

import typer
import pydantic

from dars import datastructs as ds
from dars import config as config_module
from dars import (
        __app_name__,
        __version__,
        cli_config,
        defaults,
        getnsirequest,
        getpublicdocsrequest,
        getdocsbyreestrnumberrequest,
        getdocsbyorgregionrequest,
        models,
        main as main_module,
        utils,
        )

app = typer.Typer()
app.add_typer(
        cli_config.app,
        name='config',
        help='Управление конфигурацией'
        )


CONFIG_PATH = os.path.join(
        typer.get_app_dir(__app_name__),
        config_module.CONFIG_FILENAME
        )


@app.command()
def getDocsByOrgRegionRequest(
        subsystem_type: Annotated[
            ds.SubsystemType,
            typer.Option(help='Тип подсистемы для отбора документов')
            ],
        document_type: Annotated[
            str,
            typer.Option(help='Тип документа'),
            ],
        region: Annotated[
            int,
            typer.Option(help='Регион по КЛАДР')
            ],
        target_date: Annotated[
            datetime,
            typer.Option(
                help='Задать дату отбора документов',
                formats=["%Y-%m-%d"]
                )
            ] = date.today().strftime('%Y-%m-%d'),
        timezone: Annotated[
            str,
            typer.Option(help='Смещение часового пояса')
            ] = defaults.TZ,
        reestr_number: Annotated[
            str | None,
            typer.Option(help='Реестровый номер в подсистеме')
            ] = None,
        base: Annotated[
            ds.Base,
            typer.Option(help='Закон (основание)')
            ] = defaults.BASE,
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        upload: Annotated[
            bool,
            typer.Option(
                help='Выгружать полученные данные в S3'
                )
            ] = True,
        delay_before_download: Annotated[
            int,
            typer.Option(help='Задержка перед загрузкой файлов из СОИ')
            ] = defaults.DELAY_BEFORE_DOWNLOAD,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Запрос архивов по региону заказчика и типу документа'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    # ---
    params = models.GetDocsByOrgRegionRequestModel(
            subsystem_type=subsystem_type,
            document_type=document_type,
            region=region,
            target_date=target_date,
            timezone=timezone,
            reestr_number=reestr_number,
            base=base,
            prefix=prefix,
            upload=upload,
            delay_before_download=delay_before_download,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getdocsbyorgregionrequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getDocsByOrgRegionRequest(**params.dict())


@app.command()
def getDocsByReestrNumberRequest(
        subsystem_type: Annotated[
            ds.SubsystemType,
            typer.Option(help='Тип подсистемы для отбора документов')
            ],
        reestr_number: Annotated[
            str,
            typer.Option(help='Реестровый номер в подсистеме')
            ],
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        upload: Annotated[
            bool,
            typer.Option(
                help='Выгружать полученные данные в S3'
                )
            ] = True,
        delay_before_download: Annotated[
            int,
            typer.Option(help='Задержка перед загрузкой файлов из СОИ')
            ] = defaults.DELAY_BEFORE_DOWNLOAD,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Запрос архивов с документами по реестровому номеру'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    # ---
    params = models.GetDocsByReestrNumberRequestModel(
            subsystem_type=subsystem_type,
            reestr_number=reestr_number,
            prefix=prefix,
            upload=upload,
            delay_before_download=delay_before_download,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getdocsbyreestrnumberrequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getDocsByReestrNumberRequest(**params.dict())


@app.command()
def getPublicDocsRequest(
        subsystemtype: Annotated[
            ds.SubsystemType,
            typer.Option(help='Тип подсистемы для отбора документов')
            ],
        regnum:  Annotated[
            list[str],
            typer.Option(
                help='Организации для отбора документов (код по СПЗ)',
                )
            ] = [],
        organizations_data: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к csv-файлу c кодами организаций (код по СПЗ) '
                'для 44-ФЗ или с ИНН / КПП для 223-ФЗ')
            ] = None,
        monthinfo: Annotated[
            datetime,
            typer.Option(
                help='Задать год и месяц отбора документов',
                formats=["%Y-%m"]
                )
            ] = None,
        exactdate: Annotated[
            datetime,
            typer.Option(
                help='Задать дату отбора документов',
                formats=["%Y-%m-%d"]
                )
            ] = None,
        todayinfo: Annotated[
            str,
            typer.Option(help='Задать период в течении суток. Пример: 0-6')
            ] = defaults.TODAY_INFO,
        offsettimezone: Annotated[
            str,
            typer.Option(help='Смещение часового пояса')
            ] = defaults.TZ,
        base: Annotated[
            ds.Base,
            typer.Option(help='Закон (основание)')
            ] = defaults.BASE,
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        upload: Annotated[
            bool,
            typer.Option(
                help='Выгружать полученные данные в S3'
                )
            ] = True,
        delay_before_download: Annotated[
            int,
            typer.Option(help='Задержка перед загрузкой файлов из СОИ')
            ] = defaults.DELAY_BEFORE_DOWNLOAD,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Получить публичные документы: планы-графики, закупки, контракты'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    regnums = []
    organizations = []
    # --- обрабатываем csv-файлик при наличии
    if organizations_data:
        with open(
                organizations_data,
                encoding='utf-8', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = list(reader)[1:]
            if base == ds.Base.FZ44:
                regnums = [row[0] for row in rows]
            elif base == ds.Base.FZ223:
                organizations = []
                for row in rows:
                    organizations.append({
                        'inn': utils.value_from_list(row, 0),
                        'kpp': utils.value_from_list(row, 1),
                        'ogrn': utils.value_from_list(row, 2)
                        })
    else:
        regnums = regnum
    # ---
    params = models.GetPublicDocsRequestModel(
            subsystemtype=subsystemtype,
            regnums=regnums,
            organizations=organizations,
            monthinfo=monthinfo,
            exactdate=exactdate,
            todayinfo=todayinfo,
            offsettimezone=offsettimezone,
            base=base,
            prefix=prefix,
            upload=upload,
            delay_before_download=delay_before_download,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getpublicdocsrequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getPublicDocsRequest(**params.dict())


@app.command()
def getNsiRequest(
        nsiCode: Annotated[
            str,
            typer.Option(
                help='Код справочника. Примеры: '
                'nsiAllList - справочник справочников, '
                'nsiOrganization - справочник организаций')
            ],
        nsiKind: Annotated[
            ds.NsiKind,
            typer.Option(
                help='Вид выгрузки: all - полная, inc - инкрементальнаяx')
            ] = defaults.NSI_KIND,
        base: Annotated[
            ds.Base,
            typer.Option(help='Закон (основание)')
            ] = defaults.BASE,
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        upload: Annotated[
            bool,
            typer.Option(
                help='Выгружать полученные данные в S3'
                )
            ] = True,
        delay_before_download: Annotated[
            int,
            typer.Option(help='Задержка перед загрузкой файлов из СОИ')
            ] = defaults.DELAY_BEFORE_DOWNLOAD,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Получить справочник'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    # ---
    params = models.GetNsiRequestModel(
            nsiCode=nsiCode,
            nsiKind=nsiKind,
            base=base,
            prefix=prefix,
            upload=upload,
            delay_before_download=delay_before_download,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getnsirequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getNsiRequest(**params.dict())


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} {__version__}')
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        '--version',
        '-v',
        help='Отобразить версию программы и выйти.',
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    # pylint: disable=unused-argument,missing-function-docstring
    return
