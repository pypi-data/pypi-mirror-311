import robotframework_construct
import pytest


def test_impossible_params():
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct()._traverse_construct_for_element(0, 0, 0, 0)
    assert "locator '0' invalid for '0'" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(None, "nope")
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was '<class 'NoneType'>'" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(b"", 0)
    assert "identifier should be a string or a construct.Construct, but was '<class 'int'>'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:    
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(0, 0)
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was '<class 'int'>'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().construct_element_should_not_be_equal("a", {"a": [1]}, [1])
    assert "observed value '[1]' is not distinct to '[1]' in '{'a': [1]}' at 'a'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().open_socket("raw", 0,0)
    assert "protocol should be either 'TCP or 'UDP', but was 'raw'" == str(excinfo.value)
