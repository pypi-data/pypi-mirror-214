import logging

from bs4 import BeautifulSoup

# API constants.
from dls_servbase_api.constants import Keywords as ProtocoljKeywords
from dls_servbase_lib.datafaces.context import Context as DlsServbaseDatafaceContext

# Utilities.
from dls_utilpack.describe import describe

# Things xchembku provides.
from xchembku_api.datafaces.context import Context as XchembkuDatafaceClientContext
from xchembku_api.datafaces.datafaces import xchembku_datafaces_get_default
from xchembku_lib.datafaces.context import Context as XchembkuDatafaceServerContext

# Client context creator.
from echolocator_api.guis.context import Context as GuiClientContext

# Object managing gui
from echolocator_api.guis.guis import echolocator_guis_get_default

# GUI constants.
from echolocator_lib.guis.constants import Commands, Cookies, Keywords

# Server context creator.
from echolocator_lib.guis.context import Context as GuiServerContext

# Base class for the tester.
from tests.base import Base

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestReportPlates:
    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/service.yaml"
        ReportPlatesTester().main(
            constants,
            configuration_file,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class ReportPlatesTester(Base):
    """
    Class to test the gui fetch_image endpoint.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """

        multiconf = self.get_multiconf()
        multiconf_dict = await multiconf.load()

        # Reference the dict entry for the xchembku dataface.
        xchembku_dataface_specification = multiconf_dict[
            "xchembku_dataface_specification"
        ]

        # Make the xchembku server context.
        xchembku_server_context = XchembkuDatafaceServerContext(
            xchembku_dataface_specification
        )
        # Make the xchembku client context.
        xchembku_client_context = XchembkuDatafaceClientContext(
            xchembku_dataface_specification
        )

        servbase_dataface_specification = multiconf_dict[
            "dls_servbase_dataface_specification"
        ]
        servbase_dataface_context = DlsServbaseDatafaceContext(
            servbase_dataface_specification
        )

        gui_specification = multiconf_dict["echolocator_gui_specification"]
        # Make the server context.
        gui_server_context = GuiServerContext(gui_specification)

        # Make the client context.
        gui_client_context = GuiClientContext(gui_specification)

        # Start the client context for the remote access to the xchembku.
        async with xchembku_client_context:
            # Start the server context xchembku which starts the process.
            async with xchembku_server_context:
                async with servbase_dataface_context:
                    # Start the gui client context.
                    async with gui_client_context:
                        # And the gui server context which starts the coro.
                        async with gui_server_context:
                            await self.__run_part1(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_part1(self, constants, output_directory):
        """ """
        # Reference the xchembku object which the context has set up as the default.
        xchembku = xchembku_datafaces_get_default()

        await self.__request_initial()

        crystal_wells = []

        # Inject some wells.
        crystal_wells.append(await self.inject(xchembku, False, False))
        crystal_wells.append(await self.inject(xchembku, True, True))
        crystal_wells.append(await self.inject(xchembku, True, False))
        crystal_wells.append(await self.inject(xchembku, True, True))
        crystal_wells.append(await self.inject(xchembku, True, True))
        crystal_wells.append(await self.inject(xchembku, True, False))

        await self.__request_all(crystal_wells)

    # ----------------------------------------------------------------------------------------

    async def __request_initial(self):
        """ """

        request = {
            ProtocoljKeywords.ENABLE_COOKIES: [
                Cookies.PLATE_LIST_UX,
            ],
            Keywords.COMMAND: Commands.REPORT_PLATES,
            "visit_filter": self.visit,
        }

        response = await echolocator_guis_get_default().client_protocolj(
            request, cookies={}
        )

        logger.debug(describe("first fetch_image response", response))

        soup = BeautifulSoup(response["html"], "html.parser")

        # Find the table element.
        table = soup.find("table")

        # Count the number of rows in the table.
        row_count = len(table.find_all("tr"))

        # The table contains only the header and no data rows.
        assert row_count == 1 + 0

    # ----------------------------------------------------------------------------------------

    async def __request_all(self, crystal_wells):
        """ """

        request = {
            ProtocoljKeywords.ENABLE_COOKIES: [
                Cookies.PLATE_LIST_UX,
            ],
            Keywords.COMMAND: Commands.REPORT_PLATES,
            "visit_filter": self.visit,
        }

        response = await echolocator_guis_get_default().client_protocolj(
            request, cookies={}
        )

        logger.debug(describe("fetch_plate_list response", response))

        soup = BeautifulSoup(response["html"], "html.parser")

        # Find the table element.
        table = soup.find("table")

        # Count the number of rows in the table.
        rows = table.find_all("tr")

        # Assert that the row count is equal to the expected value.
        assert len(rows) == 1 + 1

        # Check the first row's contents.
        row = rows[1]
        row.find_all(class_="T_collected_count")[0].get_text() == "6"
        row.find_all(class_="T_chimped_count")[0].get_text() == "5"
        row.find_all(class_="T_undecided_count")[0].get_text() == "2"
        row.find_all(class_="T_undecided_crystals_count")[0].get_text() == "2"
        row.find_all(class_="T_decided_count")[0].get_text() == "3"
        row.find_all(class_="T_exported_count")[0].get_text() == "0"
        row.find_all(class_="T_usable_unexported_count")[0].get_text() == "3"
