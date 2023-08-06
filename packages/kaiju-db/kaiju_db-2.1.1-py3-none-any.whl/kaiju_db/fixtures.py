"""DB fixtures."""

from pathlib import Path
from typing import Collection

from kaiju_db.sql_service import SQLService
from kaiju_tools.app import ContextableService
from kaiju_tools.encoding import load

__all__ = ['FixtureService']


class FixtureService(ContextableService):
    """Fixture service.

    It can load data from json files using SQLService interface.
    """

    def __init__(
        self,
        app,
        root_dir: str = './fixtures',
        fixtures: Collection[str] = None,
        empty_tables_only: bool = True,
        load_on_init: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param root_dir: fixtures base dir
        :param fixtures: list of fixtures (service names) to load, None - load all
        :param empty_tables_only: load only when the service table is empty
        :param load_on_init: load all fixtures on service init (when starting the app)
        :param logger: parent logger instance
        """
        super().__init__(app=app, logger=logger)
        self.root_dir = Path(root_dir).resolve()
        self.fixtures = fixtures
        self.empty_tables_only = empty_tables_only
        self.load_on_init = load_on_init

    async def init(self):
        if not self.root_dir.exists():
            self.logger.warn('Fixture path does not exist', root_dir=str(self.root_dir))
        if self.load_on_init:
            await self.load_all()

    async def load_all(self) -> None:
        """Load all fixtures in the root dir."""
        for path in self.root_dir.rglob('*.json'):
            if self.fixtures and path.stem not in self.fixtures:
                continue
            await self.load_fixture(path)

    async def load_fixture(self, path: Path) -> None:
        """Load a single service fixture.

        A file must be a JSON list with rows of data.
        """
        service_name = path.stem

        if service_name not in self.app.services:
            self.logger.debug('Cannot load fixture: no such service', fixture=service_name)
            return

        service = self.app.services[service_name]
        if not isinstance(service, SQLService):
            self.logger.debug('Cannot load fixture: not an SQLService interface', fixture=service_name)
            return

        if not path.exists() or not path.is_file():
            self.logger.debug('Cannot load fixture: file does not exist', fixture=service_name, filename=str(path))
            return

        if self.empty_tables_only:
            if await self._table_not_empty(service_name):
                self.logger.debug('Cannot load fixture: table is not empty', fixture=service_name)
                return

        data = load(path)
        if data:
            self.logger.info('Loading fixture', fixture=service_name, filename=str(path))
            await service.m_create(data=data, columns=[], on_conflict='do_nothing')

    async def _table_not_empty(self, service_name: str) -> bool:
        service = self.app.services[service_name]
        data = await service.list(limit=1, count=False)
        return bool(data['data'])
