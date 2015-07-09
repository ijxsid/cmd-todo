import pytest
import sys, os
# HACK: To make lib accesible here.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import lib.utils as utils
import re

"""
This part consists of tests for utils.generate_unique_code aka gce.
"""
def test_gce_length():
    """
    the length of output of generate_unique_code should be equal to its argument.
    """
    assert len(utils.generate_unique_code(6)) == 6

def test_gce_instance():
    """
    The output of generate_unique_code should be an instance of 'str'.
    """
    assert isinstance(utils.generate_unique_code(5), str)

@pytest.fixture
def numerical_regex():
    regex = re.compile(r'[0-9]+')
    return regex
    

def test_gce_no_number(numerical_regex):
    """
    The output of generate_unique_code should not conatain any numbers.
    """
    code = utils.generate_unique_code()
    assert len(numerical_regex.findall(code)) == 0


    
    
