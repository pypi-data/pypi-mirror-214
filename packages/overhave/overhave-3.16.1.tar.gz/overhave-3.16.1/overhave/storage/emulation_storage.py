import abc
import logging
import socket
from typing import cast

import sqlalchemy as sa
import sqlalchemy.orm as so
from pydantic.tools import parse_obj_as

from overhave import db
from overhave.entities.settings import OverhaveEmulationSettings
from overhave.storage import EmulationRunModel
from overhave.utils import get_current_time

logger = logging.getLogger(__name__)


class EmulationStorageError(Exception):
    """Base Exception for :class:`EmulationStorage`."""


class NotFoundEmulationError(EmulationStorageError):
    """Exception for situation without saved emulation.."""


class AllPortsAreBusyError(EmulationStorageError):
    """Exception for situation when all ports are busy."""


class IEmulationStorage(abc.ABC):
    """Abstract class for emulation runs storage."""

    @staticmethod
    @abc.abstractmethod
    def create_emulation_run(emulation_id: int, initiated_by: str) -> EmulationRunModel:
        pass

    @abc.abstractmethod
    def get_requested_emulation_run(self, emulation_run_id: int) -> EmulationRunModel:
        pass

    @abc.abstractmethod
    def set_emulation_run_status(self, emulation_run_id: int, status: db.EmulationStatus) -> None:
        pass

    @abc.abstractmethod
    def set_error_emulation_run(self, emulation_run_id: int, traceback: str) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_emulation_runs_by_test_user_id(test_user_id: int) -> list[EmulationRunModel]:
        pass


class EmulationStorage(IEmulationStorage):
    """Class for emulation runs storage."""

    def __init__(self, settings: OverhaveEmulationSettings):
        self._settings = settings

    @staticmethod
    def create_emulation_run(emulation_id: int, initiated_by: str) -> EmulationRunModel:
        with db.create_session() as session:
            emulation_run = db.EmulationRun(emulation_id=emulation_id, initiated_by=initiated_by)
            session.add(emulation_run)
            session.flush()
            return EmulationRunModel.from_orm(emulation_run)

    @staticmethod
    def _get_emulation_run(session: so.Session, emulation_run_id: int) -> db.EmulationRun:
        emulation_run = session.get(db.EmulationRun, emulation_run_id)
        if isinstance(emulation_run, db.EmulationRun):
            return emulation_run
        raise NotFoundEmulationError(f"Not found emulation run with ID {emulation_run_id}!")

    def _get_next_port(self, session: so.Session) -> int:
        runs_with_allocated_ports = (  # noqa: ECE001
            session.query(db.EmulationRun)
            .filter(db.EmulationRun.port.isnot(None))
            .order_by(db.EmulationRun.id.desc())
            .limit(len(self._settings.emulation_ports))
            .all()
        )
        allocated_sorted_runs = sorted(
            runs_with_allocated_ports,
            key=lambda t: t.changed_at,
        )

        allocated_ports = {run.port for run in allocated_sorted_runs}
        logger.debug("Allocated ports: %s", allocated_ports)
        not_allocated_ports = set(self._settings.emulation_ports).difference(allocated_ports)
        logger.debug("Not allocated ports: %s", not_allocated_ports)
        if not_allocated_ports:
            for port in not_allocated_ports:
                if self._is_port_in_use(port):
                    continue
                return port
            logger.debug("All not allocated ports are busy!")
        for run in allocated_sorted_runs:
            if self._is_port_in_use(cast(int, run.port)):
                continue
            return cast(int, run.port)
        raise AllPortsAreBusyError("All ports are busy - could not find free port!")

    def _is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self._settings.emulation_bind_ip, port)) == 0

    def get_requested_emulation_run(self, emulation_run_id: int) -> EmulationRunModel:
        with db.create_session() as session:
            emulation_run = self._get_emulation_run(session, emulation_run_id)
            emulation_run.status = db.EmulationStatus.REQUESTED
            emulation_run.port = self._get_next_port(session)
            emulation_run.changed_at = get_current_time()
            return EmulationRunModel.from_orm(emulation_run)

    def set_emulation_run_status(self, emulation_run_id: int, status: db.EmulationStatus) -> None:
        with db.create_session() as session:
            session.execute(
                sa.update(db.EmulationRun)
                .where(db.EmulationRun.id == emulation_run_id)
                .values(status=status, changed_at=get_current_time())
            )

    def set_error_emulation_run(self, emulation_run_id: int, traceback: str) -> None:
        with db.create_session() as session:
            emulation_run = self._get_emulation_run(session, emulation_run_id)
            emulation_run.status = db.EmulationStatus.ERROR
            emulation_run.traceback = traceback
            emulation_run.changed_at = get_current_time()

    @staticmethod
    def get_emulation_runs_by_test_user_id(test_user_id: int) -> list[EmulationRunModel]:
        with db.create_session() as session:
            emulation_ids_query = (
                session.query(db.Emulation)
                .with_entities(db.Emulation.id)
                .filter(db.Emulation.test_user_id == test_user_id)
                .scalar_subquery()
            )
            emulation_runs = (
                session.query(db.EmulationRun).where(db.EmulationRun.emulation_id.in_(emulation_ids_query)).all()
            )
            return parse_obj_as(list[EmulationRunModel], emulation_runs)
