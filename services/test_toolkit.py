from phi.tools import Toolkit
from phi.utils.log import logger


class CustomStringTools(Toolkit):
    def __init__(self, my_custom_string: str):
        super().__init__(name="CustomStringToolkit")
        self.register(self.get_my_custom_string)

        self.my_custom_string = my_custom_string

        logger.info(
            f"Custom String Toolkit Initialized, Custom String: {self.my_custom_string}"
        )

    def update_custom_string(self, custom_string):
        """
        Useful method to update the custom string
        """

        logger.info(f"Custom String Toolkit - update_custom_string: {custom_string}")

        self.my_custom_string = custom_string

    def get_my_custom_string(self):
        """
        Useful method to get the current value of the custom string
        """

        logger.info(
            f"Custom String Toolkit - get_my_custom_string: {self.my_custom_string}"
        )

        return self.my_custom_string
