    #TeddyW - Duplicate test file for experimentations
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from scripts.add import load_json

    #test trial fn to verify working files
def test_trial():
    assert isinstance(4,int)

    #actual test
def test_load_json():
  response = load_json()
  assert isinstance(response, dict)
  assert response.get("Teddy Waweru") =="Table Tennis"
