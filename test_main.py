import re
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# def test_captcha():

#     # generate captcha
#     res = client.post("/generate_captcha/")
#     assert res.status_code == 200
#     captcha_id = re.sub("^inline; filename=\"|\.png\"$", "", res.headers["content-disposition"])
    
#     # send true captcha_id but wrong label
#     res = client.post("/validate_captcha_response/", json = {"captcha_id": captcha_id, "captcha_label": "fake"})
#     assert res.status_code == 403

#     # send wrong captcha_id and wrong label
#     res = client.post("/validate_captcha_response/", json = {"captcha_id": captcha_id + "fake", "captcha_label": "fake"})
#     assert res.status_code == 404


