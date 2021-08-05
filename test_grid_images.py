import pytest
from dtypes.simpleImage import SimpleImage
from utils.constants import constants

@pytest.fixture
def config():
    return constants().default_options

def test_grid_image_1(config):

    img_dic = {
                "img_path": "edge_poresity.png",
                'id':'tester-1',
                "pass": False,
                'img_name': '',
                "fail_reason": [],
                "largest_pore": 0,
                "porosity": 0,
                "avg_pore": 0,
                "out_path": './job-data/test-cases',
                "num_violated": 0,
                "violated_pores": [],
            }
    
    