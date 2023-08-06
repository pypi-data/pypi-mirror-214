import logging
from typing import Optional

# Base class for the tester.
from tests.base import Base

# Types which the CrystalPlateObjects factory can use to build an instance.
from xchembku_api.crystal_plate_objects.constants import (
    ThingTypes as CrystalPlateObjectThingTypes,
)

# Client context creator.
from xchembku_api.datafaces.context import Context as XchembkuDatafaceClientContext

# Object managing datafaces.
from xchembku_api.datafaces.datafaces import xchembku_datafaces_get_default
from xchembku_api.models.crystal_plate_filter_model import CrystalPlateFilterModel
from xchembku_api.models.crystal_plate_model import CrystalPlateModel

# Crystal plate objects factory.
from xchembku_lib.crystal_plate_objects.crystal_plate_objects import CrystalPlateObjects

# Server context creator.
from xchembku_lib.datafaces.context import Context as XchembkuDatafaceServerContext

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestCrystalPlateDirectSqlite:
    """
    Test dataface interface by direct call.
    """

    def test(
        self,
        constants,
        logging_setup,
        output_directory,
    ):
        configuration_file = "tests/configurations/direct_sqlite.yaml"
        CrystalPlateTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class TestCrystalPlateDirectMysql:
    """
    Test dataface interface by direct call.
    """

    def test(
        self,
        constants,
        logging_setup,
        output_directory,
    ):
        configuration_file = "tests/configurations/direct_mysql.yaml"
        CrystalPlateTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class TestCrystalPlateServiceSqlite:
    """
    Test dataface interface through network interface.
    """

    def test(
        self,
        constants,
        logging_setup,
        output_directory,
    ):
        """ """

        configuration_file = "tests/configurations/service_sqlite.yaml"
        CrystalPlateTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class TestCrystalPlateServiceMysql:
    """
    Test dataface interface through network interface.
    """

    def test(
        self,
        constants,
        logging_setup,
        output_directory,
    ):
        """ """

        configuration_file = "tests/configurations/service_mysql.yaml"
        CrystalPlateTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class CrystalPlateTester(Base):
    """
    Class to test the dataface droplocation-related endpoints.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """
        # Get the multiconf from the testing configuration yaml.
        multiconf = self.get_multiconf()

        # Load the multiconf into a dict.
        multiconf_dict = await multiconf.load()

        # Reference the dict entry for the xchembku dataface.
        xchembku_dataface_specification = multiconf_dict[
            "xchembku_dataface_specification"
        ]

        # Make the server context.
        xchembku_server_context = XchembkuDatafaceServerContext(
            xchembku_dataface_specification
        )

        # Make the client context.
        xchembku_client_context = XchembkuDatafaceClientContext(
            xchembku_dataface_specification
        )

        # Start the xchembku server context which includes the direct or network-addressable service.
        async with xchembku_server_context:
            # Start the matching xchembku client context.
            async with xchembku_client_context:
                await self.__run_the_test(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_the_test(self, constants, output_directory):
        """ """

        # Reference the dataface object which the context has set up as the default.
        dataface = xchembku_datafaces_get_default()

        visit = "cm00001-1"
        models = []
        models.append(
            CrystalPlateModel(
                formulatrix__plate__id=10,
                barcode="xyz1",
                visit=visit,
            )
        )
        models.append(
            CrystalPlateModel(
                formulatrix__plate__id=20,
                barcode="xyz2",
                visit=visit,
            )
        )
        models.append(
            CrystalPlateModel(
                formulatrix__plate__id=30,
                barcode="xyz3",
                visit=visit,
            )
        )

        await dataface.upsert_crystal_plates(models)

        # Check the filtered queries.
        await self.__check(
            dataface,
            CrystalPlateFilterModel(),
            3,
            "all",
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=2),
            2,
            "limit",
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=1, direction=1),
            1,
            "earliest",
            formulatrix__plate__id=10,
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=1, direction=-1),
            1,
            "latest",
            formulatrix__plate__id=30,
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(uuid=models[1].uuid),
            1,
            "by uuid",
            formulatrix__plate__id=20,
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(barcode=models[2].barcode),
            1,
            "by barcode",
            formulatrix__plate__id=30,
        )
        await self.__check(
            dataface,
            CrystalPlateFilterModel(
                from_formulatrix__plate__id=models[0].formulatrix__plate__id
            ),
            2,
            "from plate_id",
            formulatrix__plate__id=20,
        )

        # ------------------------------------------------------------------------------------
        # Create an object to be upserted.
        upserted_model = CrystalPlateModel(
            formulatrix__plate__id=40,
            barcode="xyz4",
            visit=visit,
            thing_type=CrystalPlateObjectThingTypes.SWISS3,
        )

        # First upsert is an insert.
        await dataface.upsert_crystal_plates([upserted_model])
        upserted_models = await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=1, direction=-1),
            1,
            "upsert insert",
            formulatrix__plate__id=40,
        )
        assert upserted_models[0].uuid == upserted_model.uuid
        created_on = upserted_models[0].created_on

        # Again, with no change, so should not insert.
        await dataface.upsert_crystal_plates([upserted_model])
        upserted_models = await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=1, direction=-1),
            1,
            "upsert insert",
            formulatrix__plate__id=40,
        )
        assert upserted_models[0].uuid == upserted_model.uuid
        assert upserted_models[0].created_on == created_on

        # Again, this time changing visit.
        upserted_model.visit = visit + "1"
        await dataface.upsert_crystal_plates([upserted_model])
        upserted_models = await self.__check(
            dataface,
            CrystalPlateFilterModel(limit=1, direction=-1),
            1,
            "upsert insert",
            formulatrix__plate__id=40,
        )

        assert upserted_models[0].uuid == upserted_model.uuid
        assert upserted_models[0].created_on == created_on
        assert upserted_models[0].visit == upserted_model.visit

        # Make sure that the model which came out of the database can be instantiated.
        specification = {"type": upserted_models[0].thing_type}
        crystal_plate_model = CrystalPlateObjects().build_object(specification)
        assert crystal_plate_model.get_well_count() == 288

        # TODO: Move testing of drop location in microns out of test_crystal_plate.py and into its own test file.
        # Cook up a fake crystal well so we can use the plate to convert drop location to microns.
        crystal_well_dict = {
            "well_centroid_x": 100,
            "well_centroid_y": 101,
            "confirmed_target_x": 150,
            "confirmed_target_y": 51,
        }

        # Let the plate decide how to convert pixels into microns.
        x_microns, y_microns = crystal_plate_model.compute_drop_location_microns(
            crystal_well_dict
        )
        assert x_microns == int(0.5 + 2.837 * 50)
        assert y_microns == int(0.5 + 2.837 * -50)

    # ----------------------------------------------------------------------------------------

    async def __check(
        self,
        dataface,
        filter: CrystalPlateFilterModel,
        expected: int,
        note: str,
        formulatrix__plate__id: Optional[int] = None,
    ):
        """ """

        crystal_plate_models = await dataface.fetch_crystal_plates(filter)

        assert len(crystal_plate_models) == expected, note

        if formulatrix__plate__id is not None:
            assert (
                crystal_plate_models[0].formulatrix__plate__id == formulatrix__plate__id
            ), f"{note} formulatrix__plate__id"

        return crystal_plate_models
