#! /usr/bin/env python3

"""
szabstractfactory_abstract.py is the abstract class for all implementations of szabstractfactory.
"""


from abc import ABC, abstractmethod
from typing import Any

from .szconfig_abstract import SzConfigAbstract
from .szconfigmanager_abstract import SzConfigManagerAbstract
from .szdiagnostic_abstract import SzDiagnosticAbstract
from .szengine_abstract import SzEngineAbstract
from .szhelpers import construct_help
from .szproduct_abstract import SzProductAbstract

# Metadata

__all__ = ["SzAbstractFactoryAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-09-23"
__updated__ = "2024-09-23"

# -----------------------------------------------------------------------------
# SzAbstractFactoryAbstract
# -----------------------------------------------------------------------------


class SzAbstractFactoryAbstract(ABC):
    """
    SzAbstractFactoryAbstract is the definition of the Senzing Python API
    SzAbstractFactory implementations.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def create_config(self, **kwargs: Any) -> SzConfigAbstract:
        """
        The `create_config` method creates a new implementation of an `SzConfigAbstract` object.

        Args:

        Returns:
            SzConfigAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_configmanager(self, **kwargs: Any) -> SzConfigManagerAbstract:
        """
        The `create_configmanager` method creates a new implementation of an `SzConfigManagerAbstract` object.

        Args:

        Returns:
            SzConfigManagerAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_configmanager.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_configmanager.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_diagnostic(self, **kwargs: Any) -> SzDiagnosticAbstract:
        """
        The `create_diagnostic` method creates a new implementation of an `SzDiagnosticAbstract` object.

        Args:

        Returns:
            SzDiagnosticAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_diagnostic.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_diagnostic.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_engine(self, **kwargs: Any) -> SzEngineAbstract:
        """
        The `create_engine` method creates a new implementation of an `SzEngineAbstract` object.

        Args:

        Returns:
            SzEngineAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_engine.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_engine.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_product(self, **kwargs: Any) -> SzProductAbstract:
        """
        The `create_product` method creates a new implementation of an `SzProductAbstract` object.

        Args:

        Returns:
            SzProductAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_product.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_product.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        """
        The `reinitialize` method reinitializes the Senzing objects using a specific configuration
        identifier. A list of available configuration identifiers can be retrieved using
        `szconfigmanager.get_configs`.

        Args:
            config_id (int): The configuration ID used for the initialization

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzError: config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/reinitialize.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def help(self, method_name: str = "") -> str:
        """
        Return the help for a particular message.

        Args:
            method_name (str): The name of the method. (e.g. "init"). If empty, a list of methods and descriptions is returned.

        Returns:
            str: The Help information about the requested method
        """
        return construct_help(self, method_name=method_name)
