import unittest

from json_wrapper import JsonWrapper

json_str = """
{
    "products":[
        {
            "id":1,
            "title":"iPhone 9",
            "description":"An apple mobile which is nothing like apple",
            "price":549,
            "discountPercentage":12.96,
            "rating":4.69,
            "stock":94,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/1/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/1/1.jpg",
                "https://dummyjson.com/image/i/products/1/2.jpg",
                "https://dummyjson.com/image/i/products/1/3.jpg",
                "https://dummyjson.com/image/i/products/1/4.jpg",
                "https://dummyjson.com/image/i/products/1/thumbnail.jpg"
            ]
        },
        {
            "id":2,
            "title":"iPhone X",
            "description":"SIM-Free, Model A19211 6.5-inch Super Retina HD display with OLED technology ...",
            "price":899,
            "discountPercentage":17.94,
            "rating":4.44,
            "stock":34,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/2/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/2/1.jpg",
                "https://dummyjson.com/image/i/products/2/2.jpg",
                "https://dummyjson.com/image/i/products/2/3.jpg",
                "https://dummyjson.com/image/i/products/2/thumbnail.jpg"
            ]
        }
    ],
    "ids": [1,2,3],
    "total":100,
    "skip":0,
    "limit":5
}
"""


class TestMjson(unittest.TestCase):
    def test_loads(self):
        value = JsonWrapper.loads(json_str)
        self.assertIsInstance(value, JsonWrapper)

    def test_common_function_of_dict(self):
        value = JsonWrapper.loads(json_str)

        # get value by key directly
        self.assertEqual(value["total"], JsonWrapper(100))

        # length
        self.assertEqual(len(value["products"]), 2)

        # if key not existed, will raise KeyError
        with self.assertRaises(KeyError):
            value["not_existed_key"]

        # test get function
        self.assertIsNone(value.get("not_existed_key"))
        self.assertEqual(value.get("not_existed_key", "defalut_value"), "defalut_value")

        # iteration, only check keys because values are quite long
        keys = ["products", "total", "skip", "limit", "ids"]
        for k, _ in value.items():
            self.assertTrue(k in keys)
        self.assertEqual(len(keys), len(value.items()))

        # interation sub items
        for index, product in enumerate(value["products"]):
            self.assertEqual(JsonWrapper(index+1), product["id"])

    def test_common_function_of_list(self):
        value = JsonWrapper.loads(json_str)
        ids = value["ids"]
        self.assertEqual(ids[0], JsonWrapper(1))
        self.assertEqual(len(ids), 3)

    def test_get(self):
        value = JsonWrapper.loads(json_str)
        self.assertEqual(value.get("total"), JsonWrapper(100))
        self.assertEqual(value.get("not_existed_key", "AAA"), "AAA")

    def test_get_value(self):
        value = JsonWrapper.loads(json_str)
        self.assertEqual(value.get_value("total"), 100)
        self.assertEqual(value.get_value("not_existed_key", "AAA"), "AAA")

    def test_long_index_key(self):
        value = JsonWrapper.loads(json_str)
        self.assertEqual(value[["products", 0, "id"]], JsonWrapper(1))
        self.assertEqual(value[["products", 1, "title"]], JsonWrapper("iPhone X"))

        self.assertEqual(value.get(["products", 6, "title"], "iPhone XXX"), "iPhone XXX")

        for _, image in enumerate(value["products", 0, "images"]):
            self.assertTrue(image.startswith("https://dummyjson.com/image/i/products/1/"))

    # def test_find_by_key(self):
    #     value = JsonWrapper.loads(json_str)
    #     self.assertEqual(value.find_by_key("id"), [1, 2, 3, 4, 5])

    # def test_find_one_by_key(self):
    #     value = JsonWrapper.loads(json_str)
    #     self.assertEqual(value.find_one_by_key("id"), 1)

    # def test_get_value(self):
        value = JsonWrapper.loads(json_str)
        self.assertTrue(isinstance(value["products", 0, "images"], JsonWrapper))
        self.assertTrue(isinstance(value.get_value(["products", 0, "images"]), list))


if __name__ == '__main__':
    unittest.main()
