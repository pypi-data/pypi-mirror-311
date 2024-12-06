from __future__ import annotations

import logging
import mmap
import re
from pathlib import Path
from typing import TextIO, Dict, List

import pandas as pd
import polars as pl

from haplo.logging import set_up_default_logger

logger = logging.getLogger(__name__)


def constantinos_kalapotharakos_file_handle_to_sqlite(file_contents: bytes | mmap.mmap, output_file_path: Path,
                                                      parameter_count: int = 11):
    set_up_default_logger()
    output_file_path.unlink(missing_ok=True)
    Path(str(output_file_path) + '-shm').unlink(missing_ok=True)
    Path(str(output_file_path) + '-wal').unlink(missing_ok=True)
    Path(str(output_file_path) + '-journal').unlink(missing_ok=True)
    value_iterator = re.finditer(rb"[^\s]+", file_contents)
    phase_amplitude_count = 64
    parameter_column_names = [f'parameter{index}' for index in range(parameter_count)]
    phase_amplitude_column_names = [f'phase_amplitude{index}' for index in range(phase_amplitude_count)]
    data_column_names = parameter_column_names + phase_amplitude_column_names
    list_of_dictionaries: List[Dict] = []
    data_frame = pl.from_dicts([], schema={name: pl.Float32 for name in data_column_names})
    count = 0
    while True:
        parameters = []
        try:
            parameters.append(float(next(value_iterator).group(0)))
        except StopIteration:
            break
        for _ in range(parameter_count - 1):
            parameters.append(float(next(value_iterator).group(0)))
        _ = float(next(value_iterator).group(0))  # Likelihood in Constantinos' output which has no meaning here.
        phase_amplitudes = []
        for _ in range(phase_amplitude_count):
            phase_amplitudes.append(float(next(value_iterator).group(0)))
        row_values = parameters + phase_amplitudes
        row_dictionary = {name: value for name, value in zip(data_column_names, row_values)}
        list_of_dictionaries.append(row_dictionary)
        count += 1
        if len(list_of_dictionaries) % 100000 == 0:
            logger.info(f'Processed {count} lines.')
            chunk_data_frame = pl.from_dicts(list_of_dictionaries,
                                             schema={name: pl.Float32 for name in data_column_names})
            chunk_data_frame.write_database('main', f'sqlite:///{output_file_path}', if_table_exists='append')
            list_of_dictionaries = []
    chunk_data_frame = pl.from_dicts(list_of_dictionaries, schema={name: pl.Float32 for name in data_column_names})
    chunk_data_frame.write_database('main', f'sqlite:///{output_file_path}', if_table_exists='append')


def arbitrary_constantinos_kalapotharakos_file_path_to_pandas(data_path: Path, columns_per_row: int,
                                                              skip_rows: int = 0, limit: int | None = None
                                                              ) -> pd.DataFrame:
    polars_data_frame = arbitrary_constantinos_kalapotharakos_file_handle_to_polars(
        data_path=data_path, columns_per_row=columns_per_row, skip_rows=skip_rows, limit=limit)
    pandas_data_frame = polars_data_frame.to_pandas()
    return pandas_data_frame


def arbitrary_constantinos_kalapotharakos_file_handle_to_polars(data_path: Path, columns_per_row: int,
                                                                skip_rows: int = 0, limit: int | None = None
                                                                ) -> pl.DataFrame:
    with data_path.open() as file_handle:
        file_contents = get_memory_mapped_file_contents(file_handle)
        return arbitrary_constantinos_kalapotharakos_file_contents_to_polars(
            file_contents, columns_per_row, skip_rows=skip_rows, limit=limit)


def arbitrary_constantinos_kalapotharakos_file_contents_to_polars(file_contents: bytes | mmap.mmap,
                                                                  columns_per_row: int, skip_rows: int = 0,
                                                                  limit: int | None = None) -> pl.DataFrame:
    set_up_default_logger()
    value_iterator = re.finditer(rb"[^\s]+", file_contents)
    list_of_dictionaries: List[Dict] = []
    data_frame = pl.from_dicts([], schema={str(index): pl.Float32 for index in range(columns_per_row)})
    count = 0
    while True:
        values = []
        try:
            values.append(float(next(value_iterator).group(0)))
        except StopIteration:
            break
        for _ in range(columns_per_row - 1):
            values.append(float(next(value_iterator).group(0)))
        if skip_rows > 0:
            skip_rows -= 1
            continue
        row_dictionary = {str(index): value for index, value in zip(range(columns_per_row), values)}
        list_of_dictionaries.append(row_dictionary)
        count += 1
        if limit is not None and count >= limit:
            break
        if len(list_of_dictionaries) % 100000 == 0:
            logger.info(f'Processed {count} lines.')
            chunk_data_frame = pl.from_dicts(list_of_dictionaries,
                                             schema={str(index): pl.Float32 for index in range(columns_per_row)})
            data_frame = data_frame.vstack(chunk_data_frame)
            list_of_dictionaries = []
    chunk_data_frame = pl.from_dicts(list_of_dictionaries,
                                     schema={str(index): pl.Float32 for index in range(columns_per_row)})
    data_frame = data_frame.vstack(chunk_data_frame)
    return data_frame


def get_memory_mapped_file_contents(file_handle: TextIO) -> mmap.mmap:
    file_fileno = file_handle.fileno()
    file_contents = mmap.mmap(file_fileno, 0, access=mmap.ACCESS_READ)
    return file_contents


def constantinos_kalapotharakos_format_file_to_sqlite(input_file_path: Path, output_file_path: Path,
                                                      parameter_count: int = 11) -> None:
    """
    Produces an SQLite database from a Constantinos Kalapotharakos format file. The expected input format includes
    11 parameters, 1 likelihood value (which is ignored), and 64 phase amplitude values for each entry.

    :param input_file_path: The Path to the Constantinos Kalapotharakos format file.
    :param output_file_path: The Path to the output SQLite database.
    """
    with input_file_path.open() as file_handle:
        file_contents = get_memory_mapped_file_contents(file_handle)
        constantinos_kalapotharakos_file_handle_to_sqlite(file_contents, output_file_path, parameter_count)


if __name__ == '__main__':
    constantinos_kalapotharakos_format_file_to_sqlite(
        Path('data/mcmc_vac_all_640m_A.dat'), Path('data/640m_rotated_parameters_and_phase_amplitudes.db'))
