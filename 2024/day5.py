from day import Day
from input_parser import InputParser
import math


class Day5(Day):
    @property
    def title(self):
        return "Print Queue"

    @property
    def input_parser(self):
        return UpdateManualParser()

    @property
    def example_input(self):
        return """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    @property
    def expected_results(self):
        return {
            "task1_example": 143,
            "task1": 6267,
            "task2_example": 123,
            "task2": 5184
        }

    def task1(self, input):
        rules = input[0]
        updates = input[1]

        valid_updates, _ = self.filter_valid_updates(updates, rules)

        return self.calculate_answer(valid_updates)

    def task2(self, input):
        rules = input[0]
        updates = input[1]

        _, invalid_updates = self.filter_valid_updates(updates, rules)

        corrected_updates = []

        def swap(update: list, index):
            orig = update.pop(index)
            update.insert(index + 1, orig)
            return update
        
        def patch_update(update, errors):
            # print("🔥", update, errors)
            corrected_update = update
            for swap_index in errors:
                corrected_update = swap(update, swap_index)
            # print("🔥🔥", corrected_update)

            success, failed = self.filter_valid_updates([corrected_update], rules)

            if len(success) > 0:
                # print("✅ update fixes")
                corrected_updates.append(corrected_update)
            else:
                # print("❌ still wrong", failed[0][0])
                patch_update(failed[0][0], failed[0][1])

        for update, errors in invalid_updates:
            # print("\n\n\n")
            patch_update(update, errors)

        return self.calculate_answer(corrected_updates)
    
    def filter_valid_updates(self, updates, rules):
        def find_rules(num, dir):
            index = 0 if dir == ">" else 1
            return list(filter(lambda x: x[index] == num, rules))
        
        valid = []
        invalid = []

        for update in updates:
            update_valid = True
            invalid_indexes = []

            for idx, num in enumerate(update):
                before_valid = True
                if idx > 0:
                    before_rules = list(map(lambda x: x[0], find_rules(num, "<")))
                    for bnum in update[:idx - 1]:
                        if bnum not in before_rules:
                            before_valid = False
                            break

                after_valid = True
                if idx < len(update) - 1:
                    after_rules = list(map(lambda x: x[1], find_rules(num, ">")))
                    for anum in update[idx + 1:]:
                        if anum not in after_rules:
                            after_valid = False
                            break

                if before_valid and after_valid:
                    # print(f"✅ {num} is correct")
                    pass
                else:
                    update_valid = False
                    # print(f"❌ {num} is incorrect")
                    invalid_indexes.append(idx)
                
            if update_valid:
                valid.append(update)
            else:
                invalid.append((update, invalid_indexes))

        return valid, invalid

    def calculate_answer(self, updates):
        return sum([update[math.floor(len(update) / 2)] for update in updates])

class UpdateManualParser(InputParser):
    def parse(self, input):
        rules = []
        updates = []

        for line in input:
            if "|" in line:
                rules.append(list(map(lambda x: int(x), line.split("|"))))
            elif "," in line:
                updates.append(list(map(lambda x: int(x), line.split(","))))

        return rules, updates
