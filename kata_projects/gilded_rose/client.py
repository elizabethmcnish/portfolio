from datetime import date, timedelta
from utils import ITEMS

# Value decreases by 50p every day (as base)
base_degredation_rate = 0.5
MAX_ITEM_VALUE = 50


# TODO: schedule runs to ensure these values update a midnight every night
class Item:
    """

    This class defines an "Item" in the Gilded Rose shop.

    Properties:
        name: name of the item, which must be in the pre-set items list
        stock_date: date object when the item was stocked
        sell_by_date: date object when the item will go out of date
        original_value: the value of the item when it was first stocked

    """

    # Importing list of items at the shop
    items_list = ITEMS

    def __init__(self, name: str, stock_date: date, sell_by_date: date, original_value: float):
        assert original_value > 0, "Original value of the item must be more than 0"
        assert original_value < MAX_ITEM_VALUE, "Original value of the item must be less than 50"

        self.stock_date = stock_date  # When the item was originally stocked
        self.sell_by_date = sell_by_date
        self.current_date = date.today()
        self.sell_days = (self.sell_by_date - self.current_date).days

        self._name = None
        self.name = name
        self.original_value = original_value
        self.current_value = original_value  # Initially set to the "original value"

        # TODO: change this back to "None"
        self.last_updated_date = date.today() - timedelta(days=2)  # Initially set to None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value not in self.items_list:
            raise ValueError(f"Invalid name '{value}'. Must be one of {self.items_list}")
        self._name = value

    def log_last_updated_date(self):

        # Updated the "last_updated_date" property when function is called
        self.last_updated_date = self.current_date

    def update_value(self) -> float:
        """

        When this method is called, it will attempt to update the value of the item
        depending on the length of time between stock_date / last_updated_date and the current_time.

        As a general rule, the value of the item degrades daily, based on the base_degration_rate.

        """
        print(f"Running update for item: {self._name}")
        sell_days = self.sell_days
        current_value = self.current_value

        # If the item has not been updated before, degrade the value from the stock_date
        if self.last_updated_date is None:
            start_time = self.stock_date
            # time_difference = (self.current_date - self.stock_date).days
        else:
            start_time = self.last_updated_date

        time_difference = (self.current_date - start_time).days
        print(f"time difference {time_difference}")

        # If the current date has passed when the item was last updated, run an update
        if self.current_date > self.last_updated_date:
            print("Current date later than last updated date. Running update.")
            # If the sell_by_date has not been passed
            if sell_days > 0:
                print("Sell by date has not passed.")
                new_value = current_value - (base_degredation_rate * time_difference)
            else:
                print("Sell by date has passed.")
                # If sell by date has past, value degrades twice as fast
                time_difference_to_sell_by = (self.sell_by_date - start_time).days
                time_difference_after_sell_by = (self.current_date - self.sell_by_date).days
                new_value = current_value - (
                    (base_degredation_rate * time_difference_to_sell_by)
                    + (base_degredation_rate * time_difference_after_sell_by * 2)
                )

        # Value of aged brie increases overtime
        if self._name == "Aged Brie":
            new_value = current_value + (base_degredation_rate * time_difference)

        # Ensure that the value of the item is in the range 0 - 50
        new_value = max(0, min(MAX_ITEM_VALUE, new_value))
        assert 0 <= new_value <= MAX_ITEM_VALUE, f"Item value: {new_value} is out of the set range (0 - 50)"

        # Update "last_updated_date" property to current_date
        self.log_last_updated_date()
        self.current_value = new_value
        print(f"Value successfully updated to: {self.current_value}")

        return self.current_value
