#3117008744 刘志豪
#3117008747 谭万钏
#参考 https://github.com/threeworld/Auto-Generate-Expression/blob/master/exp_generate.py
import re, os
import check
import argparse

def opt():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", dest = "nums", help = "生成数量" )
    parser.add_argument("-r", dest = "range", help = "生成范围" )
    parser.add_argument("-e", dest = "e_file", help = "练习文件" )
    parser.add_argument("-a", dest = "a_file", help = "答案文件" )

    args = parser.parse_args()
    return args

class EA_gen():
    def __init__(self):
        self.need = 1
        self.gen_range = 10

    def gen(self, need, range):
        self.need = need
        self.gen_range = range



def main():
    args = opt()
    print(args)
    ea = EA_gen()
    if args.range:
        ea.gen_range  = args.range
    if args.nums:
        ea.need  = args.nums

    print(ea.gen_range, ea.need)


    Formula = ['1', '+', '1' ]
    file = 'exercise.txt'
    answer = 2
    flag = check.check(list, answer, file)


if __name__ == '__main__':
    main()