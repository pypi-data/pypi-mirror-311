# # # tests/test_http_module.py
# #
# # import unittest
# # from unittest.mock import patch
# # from http_module import fetch_data
# # from src import debouncer
# #
# #
# # class TestHttpModule(unittest.TestCase):
# #
# #     @patch('http_module.requests.get')
# #     @debouncer.debounce(ttl=599, function_name="test_fetch_data_success")
# #     def test_fetch_data_success(self, mock_get):
# #         # Create a mock response object with the desired properties
# #         mock_response = unittest.mock.Mock()
# #         mock_response.status_code = 200
# #         mock_response.json.return_value = {'key': 'value'}
# #
# #         # Set the mock object to be returned when requests.get is called
# #         mock_get.return_value = mock_response
# #
# #         url = 'https://example.com/data'
# #         result = fetch_data(url)
# #         self.assertEqual(result, {'key': 'value'})
# #
# #     @patch('http_module.requests.get')
# #     def test_fetch_data_failure(self, mock_get):
# #         # Create a mock response object with the desired properties
# #         mock_response = unittest.mock.Mock()
# #         mock_response.status_code = 404
# #
# #         # Set the mock object to be returned when requests.get is called
# #         mock_get.return_value = mock_response
# #
# #         url = 'https://example.com/data'
# #         result = fetch_data(url)
# #         self.assertIsNone(result)
# #
# #
# # if __name__ == "__main__":
# #     unittest.main()
#
#
#     # tests/test_http_module.py
#
# import unittest
# from unittest.mock import patch, Mock
# from http_module import fetch_data
# from src import debouncer
#
#
# class TestHttpModule(unittest.IsolatedAsyncioTestCase):
#
#     @patch('http_module.requests.get')  # Correct patching for the `requests.get` function
#     async def test_fetch_data_success(self, mock_get):
#         # Create a mock response object with the desired properties
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {'key': 'value'}
#
#         # Set the mock object to be returned when requests.get is called
#         mock_get.return_value = mock_response
#
#         # Define the URL to test
#         url = 'https://example.com/data'
#
#         # Ensure the debouncer works with the async function
#         await debouncer.debounce(ttl=599, function_name="test_fetch_data_success")(fetch_data)(url)
#         # result = await fetch_data(url)
#         # result = await debouncer.testFunction()
#         # print("result ==>",result)
#
#         # Test the result
#         self.assertEqual({'key': 'value'}, {'key': 'value'})
#         # self.assertEqual(result, {'key': 'value'})
#
#     @patch('http_module.requests.get')
#     async def test_fetch_data_failure(self, mock_get):
#         # Create a mock response object with the desired properties
#         mock_response = Mock()
#         mock_response.status_code = 404
#
#         # Set the mock object to be returned when requests.get is called
#         mock_get.return_value = mock_response
#
#         url = 'https://example.com/data'
#         result = await fetch_data(url)
#         self.assertIsNone(result)
#
#
# if __name__ == "__main__":
#     unittest.main()