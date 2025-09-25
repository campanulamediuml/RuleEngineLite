import random
from typing import List

from parser.compiler_parser import RuleEngine
from type_template.type_define import TypeDataKey


class ExprTest:
    def __init__(self):
        self.dataset = {
            "k1": random.uniform(0, 100),
            "k2": random.uniform(0, 100),
            "k3": random.uniform(0, 100),
            "k4": random.uniform(0, 100),
            "k5": random.uniform(0, 100),
        }
        self.data_keys: List[TypeDataKey] = ["k1", "k2", "k3", "k4", "k5"]

    def run(self):
        expr = "{%s} + {%s} > 100" % (2, 3)
        rule_engine = RuleEngine([expr], self.data_keys)
        result = rule_engine.check_expr(self.dataset)
        if result[0] == (self.dataset.get(self.data_keys[2]) + self.dataset.get(self.data_keys[3]) > 100):
            print("测试通过")

        expr2 = "({%s} + {%s}) * {%s} / {%s} - {%s} < 50" % (0, 1, 2, 3, 4)
        rule_engine2 = RuleEngine([expr2], self.data_keys)
        result2 = rule_engine2.check_expr(self.dataset)
        if result2[0] == (
                (self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * self.dataset.get(
                self.data_keys[2]) / self.dataset.get(self.data_keys[3]) - self.dataset.get(self.data_keys[4]) < 50):
            print("测试通过")

        expr3 = "({%s} + {%s}) * ({%s} - {%s}) / %s >= 0" % (0, 1, 2, 3, 4)
        rule_engine3 = RuleEngine([expr3], self.data_keys)
        result3 = rule_engine3.check_expr(self.dataset)
        if result3[0] == ((self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * (
                self.dataset.get(self.data_keys[2]) - self.dataset.get(self.data_keys[3])) / 4 >= 0):
            print("测试通过")

        expr4 = "({%s} + {%s}) * ({%s} - {%s}) / %s == 0 ||  ({%s} + {%s}) * ({%s} - {%s}) / %s > 0" % (
        0, 1, 2, 3, 4, 0, 1, 2, 3, 4)
        rule_engine4 = RuleEngine([expr4], self.data_keys)
        result4 = rule_engine4.check_expr(self.dataset)
        if result4[0] == (((self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * (
                self.dataset.get(self.data_keys[2]) - self.dataset.get(self.data_keys[3])) / 4 == 0) or (
                                  (self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * (
                                  self.dataset.get(self.data_keys[2]) - self.dataset.get(self.data_keys[3])) / 4 > 0)):
            print("测试通过")

        expr5 = "({%s} + {%s}) * ({%s} - {%s}) / %s == 0 &&  ({%s} + {%s}) * ({%s} - {%s}) / %s > 0" % (
            0, 1, 2, 3, 4, 0, 1, 2, 3, 4)
        rule_engine5 = RuleEngine([expr5], self.data_keys)
        result5 = rule_engine5.check_expr(self.dataset)
        if result5[0] == (((self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * (
                self.dataset.get(self.data_keys[2]) - self.dataset.get(self.data_keys[3])) / 4 == 0) and (
                                  (self.dataset.get(self.data_keys[0]) + self.dataset.get(self.data_keys[1])) * (
                                  self.dataset.get(self.data_keys[2]) - self.dataset.get(self.data_keys[3])) / 4 > 0)):
            print("测试通过")


if __name__ == '__main__':
    expr_test = ExprTest()
    expr_test.run()
