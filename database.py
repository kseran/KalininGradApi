from sqlalchemy import create_engine, MetaData

from databases import Database


class ContDateBase:
    def __init__(self):
        """класс управления бд"""
        self._DATABASE_URL: str = "sqlite:///./test.db"
        self._engine: create_engine = create_engine(self._DATABASE_URL)
        self._metadata: MetaData = MetaData()
        self._database: Database = Database(self._DATABASE_URL)

    def get_engine(self):
        return self._engine

    def get_metadata(self):
        return self._metadata

    def get_database(self):
        return self._database
