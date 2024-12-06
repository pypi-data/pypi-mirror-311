##
##

import time
import logging
from typing import List, Union
from restfull.restapi import NotFoundError, UnprocessableEntityError
from pytoolbase.retry import retry
from libcapella.project import CapellaProject
from libcapella.logic.database import Database

logger = logging.getLogger('libcapella.database')
logger.addHandler(logging.NullHandler())


class CapellaDatabase(object):

    def __init__(self, project: CapellaProject, database: Union[str, None] = None):
        self._endpoint = f"{project.endpoint}/{project.id}/clusters"
        self.rest = project.rest
        self.project = project
        self.database_name = database if database else project.org.config.database_name
        if self.database_name:
            self.database = self.get_by_name(self.database_name)
        else:
            self.database = None

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def id(self):
        if not self.database:
            return None
        return self.database.id

    @property
    def this(self) -> Database:
        return self.database

    def refresh(self):
        self.database = self.get(self.database.id)

    def list(self) -> List[Database]:
        result = self.rest.get_paged(self._endpoint,
                                     total_tag="totalItems",
                                     pages_tag="last",
                                     per_page_tag="perPage",
                                     per_page=50,
                                     cursor="cursor",
                                     category="pages").validate().json_list()
        logger.debug(f"database list: found {result.size}")
        return [Database.create(r) for r in result.as_list]

    def get(self, database_id: str) -> Union[Database, None]:
        if not database_id:
            return None
        endpoint = f"{self._endpoint}/{database_id}"
        try:
            result = self.rest.get(endpoint).validate().as_json().json_object()
            return Database.create(result.as_dict)
        except NotFoundError:
            return None

    def get_by_name(self, name: str) -> Union[Database, None]:
        result = self.rest.get_paged(self._endpoint,
                                     total_tag="totalItems",
                                     pages_tag="last",
                                     per_page_tag="perPage",
                                     per_page=50,
                                     cursor="cursor",
                                     category="pages").validate().filter("name", name).list_item(0)
        if not result:
            return None
        return Database.create(result)

    @retry(retry_count=5, factor=0.001, allow_list=(UnprocessableEntityError,))
    def create(self, database: Database):
        if self.database_name:
            database.name = self.database_name
        config = database.as_dict_striped
        logger.debug(f"creating database {database.name}:\n{config}")
        database_id = self.rest.post(self._endpoint, config).validate().as_json().json_key("id")
        database.id = database_id
        self.database = database

    def wait(self, state, retry_count: int = 90):
        if not self.database:
            return True
        for retry_number in range(retry_count + 1):
            check = self.get(self.database.id)
            logger.debug(f"Checking cluster state {check.currentState if check else None} with state {state}")
            if check and check.currentState != state:
                return True
            elif not check:
                return True
            else:
                if retry_number == retry_count:
                    return False
                logger.debug(f"Waiting for cluster {self.database.name} to reach state {state}")
                time.sleep(10)

    def delete(self):
        if self.database.id:
            endpoint = f"{self._endpoint}/{self.database.id}"
            self.rest.delete(endpoint)
