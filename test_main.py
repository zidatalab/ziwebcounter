import re
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_1_test_status():
    '''
    Checks if DB connection is established
    '''
    res = client.get("/")
    assert res.status_code == 200
    
# def test_2_test_view_without_img():
#     '''
#     Checks if View can be submitted
#     '''
#     res = client.get("/view/testname/data?pageid=/builtest.html")
#     assert res.status_code == 200

# def test_3_test_view_with_img():
#     '''
#     Checks if View can be submitted
#     '''
#     res = client.get("/view/testname/counter.png?pageid=/builtest.html")
#     print(res)
#     assert res.status_code == 200