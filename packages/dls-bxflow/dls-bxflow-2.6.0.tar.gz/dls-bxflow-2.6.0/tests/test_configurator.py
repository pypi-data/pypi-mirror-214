import asyncio
import logging
import multiprocessing
import os

import pytest
import yaml
from dls_multiconf_lib.constants import ThingTypes as MulticonfThingTypes

# Exceptions.
from dls_multiconf_lib.exceptions import NotFound

# Utilities.
from dls_utilpack.describe import describe

# Configurator.
from dls_bxflow_lib.bx_configurators.bx_configurators import BxConfigurators

# Environment variables with some extra functionality.
from dls_bxflow_lib.envvar import Envvar

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestConfiguratorDirectGood:
    def test(self, constants, logging_setup, output_directory):
        """ """

        # This is the configuration which the ConfiguratorTester will check.
        configuration = {
            "output_directory": "${output_directory}",
            "multi": {"level1": {"level2": "value_at_level2"}},
            "key_to_remove": "value_to_remove",
        }

        # Write the yaml file target to load.
        yaml_filename = f"{output_directory}/configuration.yml"
        with open(yaml_filename, "w") as yaml_stream:
            yaml.dump(
                configuration, yaml_stream, default_flow_style=False, sort_keys=False
            )

        # This is the object type we want to run the test on.
        specification = {
            "type": MulticonfThingTypes.YAML,
            "type_specific_tbd": {"filename": yaml_filename},
        }

        # Run the test in a coroutine.
        GoodConfiguratorDirectTester().main(constants, specification, output_directory)


# ----------------------------------------------------------------------------------------
class TestConfiguratorDirectBad:
    def test(self, constants, logging_setup, output_directory):
        """ """

        # Run the bad tests in a coroutine.
        BadConfiguratorDirectTester("RuntimeError", "does not contain keyword").main(
            constants, {}, output_directory
        )
        BadConfiguratorDirectTester("RuntimeError", "unable to instantiate").main(
            constants,
            {"type": MulticonfThingTypes.YAML},
            output_directory,
        )

        # Another yaml file.
        bad_yaml_filename = f"{output_directory}/configuration.bad.yml"
        specification = {
            "type": MulticonfThingTypes.YAML,
            "type_specific_tbd": {"filename": bad_yaml_filename},
        }

        BadConfiguratorDirectTester("RuntimeError", "unable to read").main(
            constants,
            specification,
            output_directory,
        )

        with open(bad_yaml_filename, "w") as yaml_stream:
            yaml_stream.write("a: - some non-yaml stuff")

        BadConfiguratorDirectTester("RuntimeError", "unable to parse").main(
            constants,
            specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class TestGoodConfigurationEnv:
    def test(self, constants, logging_setup, output_directory):
        """ """

        good_config = f"{output_directory}/good_config1.yaml"
        with open(good_config, "w") as stream:
            stream.write("")

        os.makedirs(f"{output_directory}/good_data_dir1")

        # ---------------------------------------------------
        environ = {
            Envvar.BXFLOW_CONFIGFILE: good_config,
        }
        GoodConfigurationEnvTester().main(constants, environ, output_directory)


# ----------------------------------------------------------------------------------------
class TestBadConfigurationEnv:
    def test(self, constants, logging_setup, output_directory):
        """ """

        # Run the bad tests in a coroutine.

        BadConfigurationEnvTester("RuntimeError", "BXFLOW_CONFIGFILE is not set").main(
            constants,
            {},
            output_directory,
        )

        BadConfigurationEnvTester("RuntimeError", "does_not_exist.yaml").main(
            constants,
            {
                Envvar.BXFLOW_CONFIGFILE: "does_not_exist.yaml",
            },
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class Base:
    """
    This is a base class for tests which use BxContext.
    """

    def main(self, constants, specification, output_directory):
        """
        This is the main program which calls the test using asyncio.
        """

        multiprocessing.current_process().name = "main"

        failure_message = None
        try:
            # Run main test in asyncio event loop.
            asyncio.run(
                self._main_coroutine(constants, specification, output_directory)
            )

        except Exception as exception:
            logger.exception(
                "unexpected exception in the test method", exc_info=exception
            )
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)


# ----------------------------------------------------------------------------------------
class GoodConfiguratorDirectTester(Base):
    """
    Class to test any type of configurator.
    """

    async def _main_coroutine(self, constants, specification, output_directory):
        """ """

        # Build the object of the type we want to test.
        bx_configurator = BxConfigurators().build_object(specification)

        # Perform symbol replacement.
        bx_configurator.substitute({"output_directory": output_directory})

        # Remove top level key of this name.
        bx_configurator.remove(["key_to_remove"])

        # Get the current dict representation of the configuration.
        current = await bx_configurator.load()

        # Check the symbol has been replaced.
        assert current["output_directory"] == output_directory

        # Check the key has been removed.
        assert "key_to_remove" not in current

        # Extract multilevel value.
        value = bx_configurator.require("multi.level1.level2")
        assert value == "value_at_level2"

        # Check a good error on non-existence of key.
        with pytest.raises(NotFound):
            value = bx_configurator.require("multi.level1.level3")

        # Check a good error on non-existence of key.
        with pytest.raises(NotFound):
            value = bx_configurator.require("multi.level1.level2.level3")

        # Substitute in token.
        value = bx_configurator.resolve("${output_directory}/${multi.level1.level2}")
        assert value == f"{output_directory}/value_at_level2"


# ----------------------------------------------------------------------------------------
class BadConfiguratorDirectTester(Base):
    """
    Class to test any type of configurator.
    """

    def __init__(self, expected_exception_type, expected_message_snippet):
        self.__expected_exception_type = expected_exception_type
        self.__expected_message_snippet = expected_message_snippet

    async def _main_coroutine(self, constants, specification, output_directory):
        """ """

        got_exception = None
        try:
            # Build the object of the type we want to test.
            bx_configurator = BxConfigurators().build_object(specification)

            # Load the configuration fromt the source provider.
            await bx_configurator.load()

            logger.info(describe("loaded yaml", bx_configurator.get_current()))
        except Exception as exception:
            got_exception = exception

        got_exception_type = type(got_exception).__name__

        assert got_exception_type == self.__expected_exception_type
        assert self.__expected_message_snippet in str(got_exception)


# ----------------------------------------------------------------------------------------
class GoodConfigurationEnvTester(Base):
    """
    Class to test any type of configurator.
    """

    async def _main_coroutine(self, constants, environ, output_directory):
        """ """

        # Define the configuration source.
        BxConfigurators().build_object_from_environment(environ=environ)


# ----------------------------------------------------------------------------------------
class BadConfigurationEnvTester(Base):
    """
    Class to test any type of configurator.
    """

    def __init__(self, expected_exception_type, expected_message_snippet):
        self.__expected_exception_type = expected_exception_type
        self.__expected_message_snippet = expected_message_snippet

    async def _main_coroutine(self, constants, environ, output_directory):
        """ """

        got_exception = None
        try:

            # Define the configuration source.
            BxConfigurators().build_object_from_environment(environ=environ)

        except Exception as exception:
            # logger.error("expected error", exc_info=exception)
            got_exception = exception

        got_exception_type = type(got_exception).__name__

        assert got_exception_type == self.__expected_exception_type
        assert self.__expected_message_snippet in str(got_exception)
