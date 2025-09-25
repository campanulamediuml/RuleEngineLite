import json
import os
import sys

from constant.const import MISC_PATH
from parser.compiler_parser import RuleEngine
from type_template.type_define import ConfigFile

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请提供规则文件名作为参数，例如: python main.py  rule1.json  dataset.data")
        sys.exit(1)
    rule_filename = sys.argv[1]
    dataset_filename = sys.argv[2]
    rule_full_filename = os.path.join(MISC_PATH, rule_filename)
    expr: ConfigFile = json.loads(open(rule_full_filename, 'r').read())
    engine = RuleEngine(expr['rules'], expr['data_keys'])
    dataset = open(dataset_filename, 'r').readline()
    while dataset:
        check_data = json.loads(dataset.strip())
        result = engine.check_expr(check_data)
        print("规则引擎计算结果:", result)
        dataset = open(dataset_filename, 'r').readline()
