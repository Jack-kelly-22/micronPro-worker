import pytest
from utils import area_utils
from skimage.draw import disk

"""this file tests various funtions in the area_utils helper file"""

@pytest.fixture
def test_data():
    return {
        "test_area": set([(0,0),(1,1),(2,2),(3,3)]),
        "test_circle": set([(0,0)]),
        "fail_circle": set([(0,0),(1,0)]),
        "empty_circle": set(),
        "area_box" : set((i,j) for i in range(10) for j in range(10)),
        "test_middle" : (5,5) 
    }


def test_check_circle(test_data):
    assert area_utils.check_circle(test_data["test_circle"],test_data["test_area"]) == True
    assert area_utils.check_circle(test_data["fail_circle"],test_data["test_area"]) == False

def test_check_circle_empty(test_data):
    """verify check_circle works"""
    assert area_utils.check_circle(test_data["empty_circle"],test_data["test_area"]) == True


def test_try_circle(test_data):
    """tests try_circle with small circle"""
    r,coord  = area_utils.try_circle(test_data["area_box"],test_data["test_middle"],1)
    print(r,coord)
    assert r==6
    assert coord==(5,5)
    
def test_largest_circle(test_data): 
    print(len(test_data["area_box"]))
    coord,r = area_utils.get_largest_circle_in_region(test_data["area_box"],max = 3,centroid=(49,50))
    assert r == 6
    assert coord == (5,5)
