#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Test cases for click_cli State"""

import unittest

from osducli.click_cli import State


class ClickCliStateTests(unittest.TestCase):
    """Test cases for test_click_cli State"""

    def test_init(self):
        """Test the init method"""
        state = State()

        self.assertEqual(state.debug, False)
        self.assertEqual(state.config_path, None)
        self.assertEqual(state.config, None)
        self.assertEqual(state.output, None)
        self.assertEqual(state.jmes, None)

    def test_user_friendly_mode(self):
        """Test the init method"""
        state = State()

        user_friendly = state.is_user_friendly_mode()
        self.assertTrue(user_friendly)

    def test_user_friendly_mode_output_set(self):
        """Test the init method"""
        state = State()
        state.output = "json"

        user_friendly = state.is_user_friendly_mode()
        self.assertFalse(user_friendly)


if __name__ == "__main__":
    import nose2

    nose2.main()
