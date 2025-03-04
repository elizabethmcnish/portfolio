# Unit tests for Kata project using PyTest modules

# 1st test: test update_value() method is working as it should
# 2nd test:

from client import Item
from datetime import date, timedelta


def test():
    # initialise instances of different items
    # last_updated_date is manually set to two days ago in the client
    brie_item = Item(
        name="Aged Brie",
        stock_date=date.today() - timedelta(days=4),
        sell_by_date=(date.today() + timedelta(days=4)),
        original_value=30,
    )
    chocolate_item = Item(
        name="Chocolate",
        stock_date=date.today() - timedelta(days=4),
        sell_by_date=(date.today() - timedelta(days=2)),
        original_value=2,
    )

    # testing update_value() method for brie
    updated_value = brie_item.update_value()
    print(f"Brie item last updated date: {brie_item.last_updated_date}")

    expected_value = 31

    assert updated_value == expected_value

    # testing update_value method for chocolate
    updated_value = chocolate_item.update_value()
    print(f"Chocolate item last updated date: {chocolate_item.last_updated_date}")

    expected_value = 0

    assert updated_value == expected_value

    # update sell_by_date to be yesterday, this should affect the value of the brie
    brie_item.sell_by_date = date.today() - timedelta(days=1)

    updated_value = brie_item.update_value()
    print(f"Brie item last updated date: {brie_item.last_updated_date}")

    expected_value = 31

    assert updated_value == expected_value

    # test when sell_by_date has past
    new_chocolate_item = Item(
        name="Chocolate",
        stock_date=date.today() - timedelta(days=4),
        sell_by_date=(date.today() - timedelta(days=2)),
        original_value=20,
    )

    updated_value = new_chocolate_item.update_value()
    print(f"New chocolate item last updated date: {new_chocolate_item.last_updated_date}")

    expected_value = 18

    assert updated_value == expected_value
