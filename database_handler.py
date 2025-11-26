import datetime
import os
from typing import override

import sqlalchemy as sql
from sqlalchemy import DateTime, select

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    """
    ORM para la tabla 'datasets'.
    Almacena los metadatos y la ubicación de los archivos de datos en el disco.
    """

    __tablename__: str = "datasets"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True)

    # nombre del dataset, no del archivo
    # (ej: usario quiere que se identifique el dataset como "survey answers", con un archivo survey.csv)
    file_name: Mapped[str] = mapped_column(sql.String(255), nullable=False)
    # Ruta absoluta o relativa al archivo en el sistema de archivos del servidor
    file_route: Mapped[str] = mapped_column(sql.String, nullable=False, unique=True)
    file_type: Mapped[str] = mapped_column(sql.String(10), default="CSV")
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    @override
    def __repr__(self):
        return f"<Dataset(id={self.id}, nombre='{self.file_name}', path='{self.file_route}')>"


class CacheTable(Base):
    """
    Modelo del ORM para almacenar resultados de operaciones.

    Otras opciones eran:
        - valkey/redis (overkill)
        - hashmap (mucho ram, no tiene persistencia)
    """

    __tablename__: str = "operation_cache"

    id: Mapped[int] = mapped_column(sql.Integer, primary_key=True)

    # id del archivo en la otra tabla
    file_id: Mapped[int] = mapped_column(sql.Integer, nullable=False)

    # clave del cache con formato id:operation_name
    cache_key: Mapped[str] = mapped_column(sql.Text, nullable=False, unique=True)

    result: Mapped[str] = mapped_column(sql.Text, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )

    @override
    def __repr__(self):
        return f"<Cache(key='{self.cache_key}', result={self.result})>"


class DatabaseHandler:
    def __init__(self, should_echo: bool = False) -> None:
        self._engine: sql.Engine = sql.create_engine(
            f"sqlite:///{os.getcwd()}/.data/database.db", echo=should_echo
        )
        Base.metadata.create_all(self._engine)

    def get_file_route(self, id: int) -> str:
        """
        Funcion para obtener un archivo basado en su id de la base de datos.
        """

        with self._engine.connect() as conn:
            res = conn.execute(
                select(Dataset.file_route).where(Dataset.id == id)
            ).first()
            if res:
                return res[0]  # pyright: ignore[reportAny]
            else:
                raise Exception(f"El id {id} no existe en la base de datos.")


if __name__ == "__main__":
    test = DatabaseHandler(True)
    with test._engine.connect() as conn:  # pyright: ignore[reportPrivateUsage]
        # _ = conn.execute(insert(Dataset).values(file_name="test1", file_route="test2"))
        # conn.commit()
        res = conn.execute(select("*").select_from(Dataset)).fetchall()
        print(f"Result: {res}")
