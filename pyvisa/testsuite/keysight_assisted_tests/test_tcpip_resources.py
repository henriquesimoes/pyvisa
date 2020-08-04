# -*- coding: utf-8 -*-
"""Test the TCPIP based resources.

"""
import copy

import pytest
from pyvisa import constants, errors

from . import require_virtual_instr
from .messagebased_resource_utils import (
    MessagebasedResourceTestCase,
    SRQMessagebasedResourceTestCase,
)


@require_virtual_instr
class TestTCPIPInstr(SRQMessagebasedResourceTestCase):
    """Test pyvisa against a TCPIP INSTR resource.

    """

    #: Type of resource being tested in this test case.
    #: See RESOURCE_ADDRESSES in the __init__.py file of this package for
    #: acceptable values
    RESOURCE_TYPE = "TCPIP::INSTR"

    #: Minimal timeout value accepted by the resource. When setting the timeout
    #: to VI_TMO_IMMEDIATE, Visa (Keysight at least) may actually use a
    #: different value depending on the values supported by the resource.
    MINIMAL_TIMEOUT = 1

    def test_io_prot_attr(self):
        """Test getting/setting the io prot attribute.

        We would need to spy on the transaction to ensure we are sending a
        string instead of using the lower level mechanism.

        """
        try:
            self.instr.read_stb()
            # XXX note sure what is the actual issue here
            with pytest.raises(errors.VisaIOError):
                self.instr.set_visa_attribute(
                    constants.VI_ATTR_IO_PROT, constants.IOProtocol.hs488
                )
            # self.instr.read_stb()
            # assert (
            #     self.instr.get_visa_attribute(constants.VI_ATTR_IO_PROT)
            #     == constants.IOProtocol.hs488
            # )
        finally:
            self.instr.set_visa_attribute(
                constants.VI_ATTR_IO_PROT, constants.IOProtocol.normal
            )


@require_virtual_instr
class TestTCPIPSocket(MessagebasedResourceTestCase):
    """Test pyvisa against a TCPIP SOCKET resource.

    """

    #: Type of resource being tested in this test case.
    #: See RESOURCE_ADDRESSES in the __init__.py file of this package for
    #: acceptable values
    RESOURCE_TYPE = "TCPIP::SOCKET"

    #: Minimal timeout value accepted by the resource. When setting the timeout
    #: to VI_TMO_IMMEDIATE, Visa (Keysight at least) may actually use a
    #: different value depending on the values supported by the resource.
    MINIMAL_TIMEOUT = 1


# Mark some tests as expected failure due to a bug in Glider
for meth_name in (
    "test_write_raw_read_bytes",
    "test_write_raw_read_raw",
    "test_write_read",
    "test_write_ascii_values",
    "test_write_binary_values",
    "test_read_ascii_values",
    "test_read_binary_values",
    "test_read_query_binary_values_invalid_header",
    "test_read_binary_values_unreported_length",
    "test_delay_in_query_ascii",
    "test_instrument_wide_delay_in_query_binary",
    "test_delay_args_in_query_binary",
    "test_no_delay_args_in_query_binary",
    "test_manual_async_read",
    "test_shared_locking",
    "test_exclusive_locking",
):
    setattr(
        TestTCPIPSocket,
        meth_name,
        # Copy since the mark is applied in-place
        pytest.mark.xfail(
            copy.deepcopy(getattr(MessagebasedResourceTestCase, meth_name))
        ),
    )
