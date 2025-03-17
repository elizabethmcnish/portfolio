from splitwise import Splitwise, SplitwiseException, SplitwiseError
from dotenv import load_dotenv
import os

load_dotenv()


consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
api_key = os.getenv("API_KEY")

# TODO:
# 1. Fix pagenation (only 20 lines of data returned)
# 2. Use Airflow to orchestrate tables


class Client:
    def __init__(self):
        self.sObj = Splitwise(consumer_key=consumer_key, consumer_secret=consumer_secret, api_key=api_key)
        self.current = self.sObj.getCurrentUser()

    def get_user_groups(self) -> list[dict]:
        try:
            groups = self.sObj.getGroups()
            indices = range(len(groups) - 1)

            groups_list = []
            for i in indices:
                name = groups[i].getName()
                id = groups[i].getId()

                groups_list.append(
                    {
                        "id": id,
                        "name": name,
                    }
                )

        except SplitwiseException as e:
            res = e._message
            raise SplitwiseError(res)

        return groups_list

    def get_group_expenses_by_name(self, name: str) -> list[dict]:
        groups_list = self.get_user_groups()

        group_id = [item.get("id") for item in groups_list if item["name"] == name][0]

        try:
            expenses = self.sObj.getExpenses(
                group_id=group_id, visible=True, limit=500
            )  # Do not include deleted expenses

            expenses_list = []
            for item in expenses:
                expenses_list.append(
                    {
                        "id": item.getId(),
                        "createdBy": item.getCreatedBy().getFirstName(),
                        "createdOn": item.getCreatedAt(),
                        "description": item.getDescription(),
                        "repayments": [
                            {
                                "amount": i.getAmount(),
                                "to": self.sObj.getUser(id=i.getToUser()).getFirstName(),
                                "from": self.sObj.getUser(id=i.getFromUser()).getFirstName(),
                            }
                            for i in item.getRepayments()
                        ],
                        "cost": item.getCost(),
                    }
                )

        except SplitwiseException as e:
            res = e._message
            raise SplitwiseError(res)

        return expenses_list
