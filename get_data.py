from typing import Dict

from modal import Stub, web_endpoint

stub = Stub()


@stub.function()
@web_endpoint(method="POST")
def square(item: Dict):
    # print({"img": item['img_url'], "choices": item['choices']})
    print(item)
    return "Worked!"
