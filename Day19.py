import re
import string
import numpy as np

# with open('Day19SampleInput.txt') as f:
with open('Day19Input.txt') as f:
    data = f.read()

workflows, ratings = data.strip('\n').split('\n\n')
workflows = workflows.split('\n')
ratings = ratings.split('\n')

class Workflow():
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules
        self.rules_list = []

        rules_list = rules.split(',')
        for rule in rules_list:
            # The "else" part of the workflow rules
            if ':' not in rule:
                destination_workflow = rule
                self.rules_list.append({'destination_workflow': destination_workflow})
                continue

            rule_details, destination_workflow = rule.split(':')
            # Assumption that variable is always one of 'x', 'm', 'a', 's' (well, a single character anyway)
            variable_for_comparison = rule_details[0]
            # Assuming one of '>', '<'
            comparison_operator = rule_details[1]
            comparison_number = rule_details[2:]
            self.rules_list.append({'variable_for_comparison': variable_for_comparison,
                                    'comparison_operator': comparison_operator,
                                    'comparison_number': comparison_number,
                                    'destination_workflow': destination_workflow})

    def apply_rules(self, input):
        # input = {'x': '787', 'm': '2655', 'a': '1222', 's': '2876'}
        for rule in self.rules_list:
            # Rules with no conditions to apply
            if 'variable_for_comparison' not in rule:
                return rule['destination_workflow']

            # if 'comparison_number'
            if eval(input[rule['variable_for_comparison']]
                    + rule['comparison_operator']
                    + rule['comparison_number']):
                return rule['destination_workflow']


workflows_dict = {}
for workflow in workflows:
    workflow_name, workflow_rules = workflow.split('{')  # x[:x.find('{')]
    workflow_rules = workflow_rules.strip('}')

    workflows_dict[workflow_name] = Workflow(workflow_name, workflow_rules)


ratings_list = []
for rating in ratings:
    temp = rating[1:-1].split(',')
    ratings_list.append({})
    for part_rating in temp:
        ratings_list[-1][part_rating[0]] = part_rating[2:]


def run_workflows(rating, workflows):
    next_workflow_name = 'in'
    while next_workflow_name not in ['A', 'R']:
        next_workflow_name = workflows[next_workflow_name].apply_rules(rating)

    if next_workflow_name == 'A':
        parts_sum = sum([int(i) for i in rating.values()])
        print(rating, parts_sum)
        return parts_sum
    return 0


total_part_sum = 0
for rating in ratings_list:
    total_part_sum += run_workflows(rating, workflows_dict)

print(f"Total: {total_part_sum}")
