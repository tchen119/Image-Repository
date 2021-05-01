import unittest
from db_tool import add_user, get_user_balance, get_image_filepath, get_inventory_quantity, get_images_from_user, get_image_price, get_image_quantity, get_marketplace_images, set_image_to_user, set_balance, set_image_to_quantity, add_image, remove_image, remove_tables, make_datebase

class TestShopify(unittest.TestCase):

    def test_image_properties(self):
        remove_tables()
        make_datebase()
        add_user('default', 100)
        add_image('test.jpg', 0, 3, 1)
        self.assertEqual(get_image_filepath(1), 'test.jpg')
        self.assertEqual(get_image_quantity(1), 1)
        self.assertEqual(get_image_price(1), 3)

    def test_image_properties_none(self):
        remove_tables()
        make_datebase()
        add_user('default', 100)
        add_image('test.jpg', 0, 3, 1)
        self.assertEqual(get_image_filepath(2), '')

    def test_user_properties(self):
        remove_tables()
        make_datebase()
        add_user('default', 100)
        self.assertEqual(get_user_balance(0), 100)

    def test_get_images(self):
        remove_tables()
        make_datebase()
        add_user('default', 100)
        self.assertEqual(get_images_from_user(0), {})

        add_image('test.jpg', 0, 3, 1)
        add_image('test2.jpg', 0, 10, 3)
        self.assertEqual(get_images_from_user(0), 
            {1: {'filepath': 'test.jpg', 'price': 3.0, 'quantity': 1}, 2: {'filepath': 'test2.jpg', 'price': 10.0, 'quantity': 3}})

    def test_get_marketplace(self):
        remove_tables()
        make_datebase()
        add_user('default', 100)
        add_image('test.jpg', 0, 3, 1)
        add_image('test2.jpg', 1, 10, 3)
        self.assertEqual(get_marketplace_images(0), {2: {'filepath': 'test2.jpg', 'price': 10.0, 'quantity': 3}})
        
if __name__ == '__main__':
    unittest.main()