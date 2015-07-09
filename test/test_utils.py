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


"""
This part consists of tests for utils.remove_common_elements aka rce.
"""
@pytest.fixture
def two_similar_lists():
    return [10, 11, 12, 13, 14, 15, 16], [10, 11, 12, 13, 14, 15, 16]

def test_rce_two_similar_lists(two_similar_lists):
    """
    output of remove_common_elements for two similar lists should be two 
    empty lists.
    """
    lists = two_similar_lists
    list1, list2, _ = utils.remove_common_elements(lists[0], lists[1])
    assert list1 == []
    assert list2 == []    
    assert isinstance(list1, list)
    assert isinstance(list2, list)
    
    
@pytest.fixture
def two_disjoint_lists():
    return [10, 12, 14, 16, 18, 20, 22], [11, 13, 15, 17, 19, 21, 23, 25]
    
def test_rce_two_disjoint_lists(two_disjoint_lists):
    """
    output of remove_common_elements for two disjoint lists should be two 
    lists containing same elements as the input lists.
    """
    lists = two_disjoint_lists
    list1, list2, _ = utils.remove_common_elements(lists[0], lists[1])
    assert set(list1) == set(lists[0])
    assert set(list2) == set(lists[1])
    """
    the output lists must be disjoint too.
    """
    assert any([el in list1 for el in list2]) == False
    """
    output should be lists.
    """
    assert isinstance(list1, list)
    assert isinstance(list2, list)

@pytest.fixture
def two_intersecting_lists():
    return [10, 15, 17, 23, 18, 20, 22], [11, 13, 15, 18, 19, 21, 23, 22]

def test_rce_disjoint_output(two_intersecting_lists):
    """
    output of remove_common_elements for two dissimilar lists should be two 
    lists which won't have any common elements. aka output needs to be disjoint.
    """
    lists = two_intersecting_lists
    
    list1, list2, _ = utils.remove_common_elements(lists[0], lists[1])
    """
    the output lists must be disjoint too.
    """
    assert any([el in list1 for el in list2]) == False
    """
    output should be lists.
    """
    assert isinstance(list1, list)
    assert isinstance(list2, list)
    
    
@pytest.fixture
def three_similar_lists():
    return [10, 11, 12, 13, 14, 15, 16], [10, 11, 12, 13, 14, 15, 16], [10, 11, 12, 13, 14, 15, 16]

def test_rce_three_similar_lists(three_similar_lists):
    """
    output of remove_common_elements for three similar lists should be three 
    empty lists.
    """
    lists = three_similar_lists
    list1, list2, list3 = utils.remove_common_elements(lists[0], lists[1], lists[2])
    assert list1 == []
    assert list2 == []
    assert list3 == []    
    assert isinstance(list1, list)
    assert isinstance(list2, list)
    assert isinstance(list3, list)
    
    
@pytest.fixture
def three_dissimilar_lists():
    return [10, 12, 14, 16, 18, 20, 22], [11, 13, 15, 17, 19, 21, 23, 25], [1, 3, 5, 7, 9]
    
def test_rce_three_dissimilar_lists(three_dissimilar_lists):
    """
    output of remove_common_elements for three dissimilar lists should be three 
    lists containing same elements as the input lists.
    """
    lists = three_dissimilar_lists
    list1, list2, list3 = utils.remove_common_elements(lists[0], lists[1], lists[2])
    assert set(list1) == set(lists[0])
    assert set(list2) == set(lists[1])
    assert set(list3) == set(lists[2])
    assert isinstance(list1, list)
    assert isinstance(list2, list)
    assert isinstance(list3, list)
    
"""
this part consists of tests for utils.clean_foldername
"""
def test_clean_foldername_empty_string():
    """
    output for clean_foldername with empty string as input should be falsy, or
    more specifically, an empty string.
    """
    foldername = ''
    cleaned = utils.clean_foldername(foldername)
    
    assert not (cleaned)
    assert cleaned == ''

def test_clean_foldername_whitespace_string():
    """
    output for clean_foldername with white-spaced string as input should be falsy, or
    more specifically, an empty string.
    """
    foldername = '  \t'
    cleaned = utils.clean_foldername(foldername)
    
    assert not (cleaned)
    assert cleaned == ''
def test_clean_foldername_normal_string():
    """
    output for clean_foldername with normal string as input should not be falsy, 
    and equilavent to lower case version of input string with trailing and 
    leading whitespaces truncated.
    """
    foldername = '   Mi-Tiempo '
    cleaned = utils.clean_foldername(foldername)
    
    assert cleaned != ''
    assert cleaned == 'mi-tiempo'
    
def test_clean_foldername_special_chars_string():
    """
    output for clean_foldername with special character string as input should 
    not be falsy, and equilavent to lower case version of input string with 
    trailing and leading whitespaces truncated, also special characters remaining
    intact.
    """
    foldername = 'Mi-(Tiempo)& Tu tiem<.>po!'
    cleaned = utils.clean_foldername(foldername)
    
    assert cleaned != ''
    assert cleaned == 'mi-(tiempo)& tu tiem<.>po!'
