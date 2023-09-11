import json
import random
from json import JSONDecodeError
from typing import Type

from users.models import User


class ManageScroll:
    def __init__(self, user_id: User.id):
        self.user_id = int(user_id)

    def _get_dict_user_from_file(self) -> dict:
        with open('operations/cells.json', 'r') as f:
            try:
                data = json.load(f)
                result = None
                for dict_obj in data['data']:
                    if dict_obj.get('user_id') == self.user_id:
                        result = dict_obj
                        return result
            except JSONDecodeError:

                return self._create_json()

    def _create_json(self):
        user = {'user_id': self.user_id,
                'round_id': 1,
                'cells': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

        with open('operations/cells.json', 'w') as f:
            json.dump({'data': [user]}, f)
            return user

    @staticmethod
    def _get_full_data() -> dict:
        with open('operations/cells.json', 'r') as f:
            data = json.load(f)
            return data

    def get_random_cell(self) -> int | str | Type[Exception]:
        user_dict = self._get_dict_user_from_file()
        data = self._get_full_data()
        data_val = data['data']

        with open('operations/cells.json', 'w') as f:
            if not user_dict:
                user_dict = {'user_id': self.user_id,
                             'round_id': 1,
                             'cells': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

                data_val.append(
                    {'user_id': self.user_id,
                     'round_id': 1,
                     'cells': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                )
            try:
                index_obj = data_val.index(user_dict)
                random_cell = random.choice(data_val[index_obj]['cells'])
                indx_rndm_cll = data_val[index_obj]['cells'].index(random_cell)
                data_val[index_obj]['cells'].pop(indx_rndm_cll)
                json.dump(data, f)
                return random_cell
            except IndexError:
                data_val[index_obj]['round_id'] = data_val[index_obj]['round_id'] + 1
                data_val[index_obj]['cells'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                json.dump(data, f)
                return 11
            except Exception:
                return Exception
