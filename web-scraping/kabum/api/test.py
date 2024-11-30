from pprint import pprint
from time import sleep



class Tester():
    def __init__(self):
        self.count = 0
        self.data = {
            "level_1_key_1": {
                "level_2_key_1": {
                    "level_3_key_1": {},
                    "level_3_key_2": {}
                },
                "level_2_key_2": {
                    "level_3_key_3": {},
                    "level_3_key_4": {}
                }
            },
            "level_1_key_2": {
                "level_2_key_3": {
                    "level_3_key_5": {},
                    "level_3_key_6": {}
                }
            }
        }

    def _categories(self, cat, parent):
        print(f"\n======== {parent} ========\n")
        if cat != {}:
            parent_id = self.count
            for k, v in cat.items():
                self.count = self.count + 1
                with open("test.txt", 'a') as f:
                    f.write(f"{self.count} - {k} - {parent_id if self.count > 1 else 'null'}\n")
                self._categories(v, k)
                
    def categories(self):
        with open("test.txt", 'w') as f:
            f.write(f"")
        self._categories(self.data, "/")
        
Tester().categories()