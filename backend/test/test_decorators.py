import time

from backend import test
from backend.utils.decorators import retry


class TestRetryDecorator(test.TestCase):
    def test_success(self):
        @retry
        def success_func():
            return "Success!"

        result = success_func()
        self.assertEqual(result, "Success!")

    def test_retry(self):
        @retry
        def fail_func():
            raise ValueError("Failed")

        with self.assertRaises(Exception):
            fail_func()

    def test_retry_with_delay(self):
        start_time = time.time()

        @retry
        def delayed_fail_func():
            nonlocal start_time
            if time.time() - start_time < 1:
                raise ValueError("Failed")
            return "Success after delay!"

        result = delayed_fail_func()
        self.assertEqual(result, "Success after delay!")
