import asyncio
import copy
import logging
from typing import Dict, List, Optional

from dls_normsql.constants import CommonFieldnames
from dls_utilpack.describe import describe

from xchembku_api.models.crystal_well_droplocation_model import (
    CrystalWellDroplocationModel,
)
from xchembku_lib.crystal_plate_objects.crystal_plate_objects import CrystalPlateObjects
from xchembku_lib.datafaces.direct_base import DirectBase

logger = logging.getLogger(__name__)


class DirectCrystalWellDroplocations(DirectBase):
    """ """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification=None):

        # Lock allows only one coroutine to acquire it at a time.
        self.__upsert_lock = asyncio.Lock()

    # ----------------------------------------------------------------------------------------
    async def upsert_crystal_well_droplocations_serialized(
        self,
        records: List[Dict],
        only_fields: Optional[List[str]] = None,
        why=None,
    ) -> Dict:
        # We are being given json, so parse it into models.
        models = [CrystalWellDroplocationModel(**record) for record in records]
        # Return the method doing the work.
        return await self.upsert_crystal_well_droplocations(
            models,
            only_fields=only_fields,
            why=why,
        )

    # ----------------------------------------------------------------------------------------
    async def __add_confirmed_microns(self, model_dict: Dict, why=None) -> None:

        if why is not None:
            why = f"[CONFMIC] {why}"

        # Input model not updating confirmed target?
        if (
            "confirmed_target_x" not in model_dict
            or "confirmed_target_y" not in model_dict
        ):
            return

        from xchembku_api.models.crystal_well_filter_model import CrystalWellFilterModel

        filter = CrystalWellFilterModel(anchor=model_dict["crystal_well_uuid"])

        # Get the well record.
        crystal_well_models = await self.fetch_crystal_wells_needing_droplocation(
            filter,
            why=f"(crystal well for adding confirmed microns) {why}",
        )

        if len(crystal_well_models) == 0:
            raise RuntimeError(
                "database integrity error: no crystal well for droplocation upsert"
            )
        crystal_well_model = crystal_well_models[0]
        crystal_well_model.confirmed_target_x = model_dict["confirmed_target_x"]
        crystal_well_model.confirmed_target_y = model_dict["confirmed_target_y"]

        crystal_plate_object = CrystalPlateObjects().build_object(
            {"type": crystal_well_model.crystal_plate_thing_type}
        )

        x, y = crystal_plate_object.compute_drop_location_microns(
            crystal_well_model.dict()
        )

        logger.debug(f"{why} x is {x}, y is {y}")

        model_dict["confirmed_microns_x"] = x
        model_dict["confirmed_microns_y"] = y

    # ----------------------------------------------------------------------------------------
    async def upsert_crystal_well_droplocations(
        self,
        models: List[CrystalWellDroplocationModel],
        only_fields: Optional[List[str]] = None,
        why=None,
    ) -> Dict:
        """
        Caller provides the crystal well droplocation record with the fields to be updated.

        We don't insert for the same crystal_well_uuid twice.

        TODO: Find more efficient way to upsert_crystal_well_droplocations in batch.
        """

        if why is None:
            why = "upsert_crystal_well_droplocations"

        inserted_count = 0
        updated_count = 0

        # Loop over all the models to be upserted.
        for model in models:
            # Need to lock because of possible long time between query and eventual insert, user might double-click to send two droplocations quite quickly.
            # TODO: Reconsider direct_crystal_well_droplocations upsert logic to be tolerant of multiple processes possibly doing concurrent insert.
            # TODO: Add unit test for concurrent direct_crystal_well_droplocations upsert.
            async with self.__upsert_lock:
                model_dict = copy.deepcopy(model.dict())

                # Find any existing record for this model object.
                records = await self.query(
                    "SELECT * FROM crystal_well_droplocations WHERE crystal_well_uuid = ?",
                    subs=[model.crystal_well_uuid],
                    why=why,
                )

                if len(records) > 0:
                    logger.debug(
                        describe(
                            "crystal_well_droplocation record before update", records[0]
                        )
                    )
                    # Make a copy of the model record and remove some fields not to update.
                    model_dict.pop(CommonFieldnames.UUID)
                    model_dict.pop(CommonFieldnames.CREATED_ON)
                    if only_fields is not None:
                        for field in list(model_dict.keys()):
                            if field not in only_fields:
                                model_dict.pop(field)

                    # Convert confirmed target to microns and store in the dict.
                    await self.__add_confirmed_microns(model_dict, why=why)

                    # Don't update the crystal_well_uuid since it is used as the key.
                    if "crystal_well_uuid" in model_dict:
                        model_dict.pop("crystal_well_uuid")

                    result = await self.update(
                        "crystal_well_droplocations",
                        model_dict,
                        "(crystal_well_uuid = ?)",
                        subs=[model.crystal_well_uuid],
                        why=why,
                    )
                    updated_count += result.get("count", 0)

                    # Find any existing record for this model object.
                    records = await self.query(
                        "SELECT * FROM crystal_well_droplocations WHERE crystal_well_uuid = ?",
                        subs=[model.crystal_well_uuid],
                        why=why,
                    )
                    logger.debug(
                        describe(
                            "crystal_well_droplocation record after update", records[0]
                        )
                    )

                else:

                    # Convert confirmed target to microns and store in the dict.
                    await self.__add_confirmed_microns(model_dict, why=why)

                    await self.insert(
                        "crystal_well_droplocations",
                        [model_dict],
                        why=why,
                    )
                    inserted_count += 1

        return {
            "updated_count": updated_count,
            "inserted_count": inserted_count,
        }
