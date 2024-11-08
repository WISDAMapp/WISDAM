# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2024 Martin Wieser.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
# ==============================================================================


import logging
from pathlib import Path
from multiprocessing import Process, Queue
from queue import Empty

from PySide6.QtCore import SignalInstance

from ai.mad_seaforg import MADSeafrog
from ai.generic_csv import GenericCSV
from ai.base_class import BaseAIClass
from ai.import_objects import process_detections_to_ai_detections, process_ai_detections_to_objects

from WISDAMcore.mapping.base_class import MappingBase

logger = logging.getLogger(__name__)


class WISDAMAi:
    """Class which manages the use of different AI workflows. To add a new AI workflow implement a class following
    the baseAiClass and add Class to ai_class_list"""

    def __init__(self):
        self.ai_class_list = [GenericCSV(), MADSeafrog()]
        self.ai_type_current = BaseAIClass()

    def get_input_names(self):

        return [input_types.name for input_types in self.ai_class_list]

    def get_current_name(self):

        return self.ai_type_current.name

    def set_ai_class(self, name: str):
        for ai_class in self.ai_class_list:
            if ai_class.name == name:
                self.ai_type_current = ai_class

    def run_ai_single_folder(self, db_path: Path, image_folder: Path, path_images_input_original: Path | None,
                             output_folder: Path, user: str,
                             progress_callback: SignalInstance | None = None, **kwargs) -> bool:

        success = False

        detections = self.ai_type_current.run(db_path, image_folder, output_folder,
                                              user, path_images_input_original, progress_callback=progress_callback,
                                              **kwargs)
        logger.info("AI process finished")
        if detections:
            logger.info("\nStart import results")
            success = process_detections_to_ai_detections(db_path, user,
                                                          self.ai_type_current.name,
                                                          detections, progress_callback)

        return success

    def run_ai_all_folders(self, db_path: Path, image_folders: list[Path], output_folder: Path, user: str,
                           progress_callback: SignalInstance | None = None, **kwargs) -> bool:
        """Runs all image folders in a sequence of single folders"""
        success = False
        for idx, img_folder in enumerate(image_folders):
            output_folder_current = output_folder / str(idx)

            success = self.ai_type_current.run(db_path, img_folder, output_folder_current,
                                               user, progress_callback=progress_callback, **kwargs)

            if not success:
                return success

        return success

    def load_ai_result_filesystem(self, db_path: Path, path_to_data: Path,
                                  user: str, progress_callback: SignalInstance | None = None, **kwargs) -> bool:

        success = False
        detections = self.ai_type_current.parse_from_path(path_to_data, **kwargs)

        logger.info("Parsing done - start import")
        if detections:

            queue = Queue()
            p = Process(target=process_detections_to_ai_detections, args=(db_path, user,
                                                                          self.ai_type_current.name,
                                                                          detections, queue))
            p.start()
            while p.is_alive():
                try:
                    msg = queue.get(timeout=1)
                except Empty:
                    continue
                if msg[0] == "progress":
                    progress_callback.emit(msg[1])
                elif msg[0] == "error":
                    logger.error(msg[2])
                    raise msg[1]
                elif msg[0] == "finished":
                    success = msg[1]
                    if success:
                        logger.info(msg[2], extra={"finished": True})
                    else:
                        logger.warning(msg[2])
                    # break

            p.join()
            msg = None
            try:
                msg = queue.get(timeout=1)
            except Empty:
                pass
            if msg is not None:
                if msg[0] == "progress":
                    progress_callback.emit(msg[1])
                elif msg[0] == "error":
                    raise msg[1]
                elif msg[0] == "finished":
                    success = msg[1]

        return success


def import_ai_detections_to_objects(db_path: Path, user: str, mapper: MappingBase | None, path_to_proj_dir: Path,
                                    progress_callback: SignalInstance | None = None, **kwargs) -> bool:
    success = False

    mapper_dict = None
    if mapper is not None:
        mapper_dict = mapper.param_dict

    queue = Queue()
    p = Process(target=process_ai_detections_to_objects, args=(db_path, user,
                                                               mapper_dict, path_to_proj_dir, queue))
    p.start()
    while p.is_alive():
        try:
            msg = queue.get(timeout=1)
        except Empty:
            continue
        if msg[0] == "progress":
            progress_callback.emit(msg[1])
        elif msg[0] == "error":
            logger.error(msg[2])
            raise msg[1]
        elif msg[0] == "finished":
            success = msg[1]
            if success:
                logger.info(msg[2], extra={"finished": True})
            else:
                logger.warning(msg[2])
            # break

    p.join()
    msg = None
    try:
        msg = queue.get(timeout=1)
    except Empty:
        pass
    if msg is not None:
        if msg[0] == "progress":
            progress_callback.emit(msg[1])
        elif msg[0] == "error":
            raise msg[1]
        elif msg[0] == "finished":
            success = msg[1]

    return success
