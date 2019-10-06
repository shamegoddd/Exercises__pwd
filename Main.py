#3117008744 刘志豪
#3117008747 谭万钏
#参考 https://github.com/threeworld/Auto-Generate-Expression/blob/master/exp_generate.py
import re, os
from random import randint
from fractions import Fraction
from goto import with_goto
import check
import argparse

def opt():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", dest = "need", help = "生成数量")
    parser.add_argument("-r", dest = "range", help = "生成范围")
    parser.add_argument("-e", dest = "e_file", help = "练习文件" )
    parser.add_argument("-a", dest = "a_file", help = "答案文件" )

    args = parser.parse_args()
    return args

class EA_gen():

    def __init__(self):
        self.gen_need = 10
        self.gen_range = 10

    def gen(self):
        f = open('./exercise.txt', 'a+')
        f2 = open('./answer.txt', 'a+')
        f.seek(0)
        f2.seek(0)
        f.truncate()
        f2.truncate()
        count = 0
        while True:
            try:
                elist, answer = self.gen_combine()
            except Exception as e:
                # print(e)
                continue      # 临时作处理：当0位除数 和 负数情况
            if check.check(elist, e_file='./exercise.txt', a_file='./answer.txt') == True:      # True表示检查后无重复
                f.write(' '.join(elist) + ' =\n')
                f2.write(answer + '\n')
                count += 1
                if count == self.gen_need:
                    break
        f.close()
        f2.close()

    def gen_combine(self):
        nums_operatior = randint(1, 3)  # 不超过3个运算符
        # brackets = [0,1,2,3,4]    #括号
        bracket = 0
        n1 = self.gen_num()
        op1 = self.gen_operator()
        n2 = self.gen_num()
        elist = [n1, op1, n2]
        if nums_operatior >= 2:     # 两步运算以上
            op2 = self.gen_operator()
            n3 = self.gen_num()
            elist.append(op2)
            elist.append(n3)
            bracket = randint(0,2)
            if nums_operatior == 3:     # 三步运算
                op3 = self.gen_operator()
                n4 = self.gen_num()
                elist.append(op3)
                elist.append(n4)
                bracket = randint(0,4)

        if bracket != 0:      # 插入括号
            elist = self.__bracket_insert(elist, bracket)

        answer = self.__get_answer(elist, bracket)
        if re.search('-', answer):
            raise Exception("Negative")     # 有负号就报错

        return elist, answer

    def __get_answer(self, elist, bracket):
        nlist = []
        olist = []
        flist = []
        for i in elist:
            if re.match(r'\+|-|x|÷', i):
                if i ==  '÷': i = '/'       # 除号转换
                if i ==  'x': i = '*'       # 乘号转换
                olist.append(i)
            elif re.match(r'\d+', i): nlist.append(i)
            else: pass
        for j in nlist:
            if re.search(r"'", j):
                f1, f2 = j.split("'")
                fraction = Fraction(f1) + Fraction(f2)
                flist.append(fraction)
            else: flist.append(Fraction(j))

        # print(olist, nlist, flist)
        answer = None

        if bracket == 0:
            if len(olist) == 1:
                answer = eval("flist[0] %s flist[1]" % (olist[0]))
            if len(olist) == 2:
                answer = eval("flist[0] %s flist[1] %s flist[2]" % (olist[0], olist[1]))
            if len(olist) == 3:
                answer = eval ('flist[0] %s flist[1] %s flist[2] %s flist[3]'%(olist[0], olist[1], olist[2]))
        if bracket == 1:
            if len(olist) == 2:
                answer = eval("(flist[0] %s flist[1]) %s flist[2]" % (olist[0], olist[1]))
            if len(olist) == 3:
                answer = eval('(flist[0] %s flist[1]) %s flist[2] %s flist[3]' % (olist[0], olist[1], olist[2]))
        if bracket == 2:
            if len(olist) == 2:
                answer = eval("flist[0] %s (flist[1] %s flist[2])" % (olist[0], olist[1]))
            if len(olist) == 3:
                answer = eval('flist[0] %s (flist[1] %s flist[2]) %s flist[3]' % (olist[0], olist[1], olist[2]))
        if bracket == 3:
            answer = eval ('flist[0] %s flist[1] %s (flist[2] %s flist[3])'%(olist[0], olist[1], olist[2]))
        if bracket == 4:
            answer = eval ('(flist[0] %s flist[1]) %s (flist[2] %s flist[3])'%(olist[0], olist[1], olist[2]))
        return str(answer)

    def __bracket_insert(self, elist, bracket):
        if bracket == 1:
            elist.insert(0, '(')
            elist.insert(4, ')')
        if bracket == 2:
            elist.insert(2, '(')
            elist.insert(6, ')')
        if bracket == 3:
            elist.insert(4, '(')
            elist.insert(8, ')')
        if bracket == 4:
            elist.insert(0, '(')
            elist.insert(4, ')')
            elist.insert(6, '(')
            elist.insert(10, ')')
        return elist
        # 1:(NoN)oNoN；
        # 2:No(NoN)oN；
        # 3:NoNo(NoN)；
        # 4:(NoN)o(NoN):

    def gen_operator(self):
        operators = ['+', '-', 'x', '÷']
        return operators[randint(0,len(operators) - 1)]

    def gen_num(self):
        #是否用真分数
        flag_is_rf = randint(0,1)
        if flag_is_rf is 1:
            n = self.gen_fraction()
        else: n =str(randint(0, self.gen_range - 1))
        return n    # 返回的是str

    def gen_fraction(self):
        denominator = randint(2, self.gen_range)
        numerator = randint(1, denominator - 1)
        random_attach = randint(0, 1)
        real_fraction = str(Fraction(numerator, denominator))
        # 调用fraction方法生成真分数
        if random_attach != 0:
            real_fraction = str(random_attach) + "'" + real_fraction
        return real_fraction

def main():
    args = opt()
    # print(args)
    if args.range and args.need:
        ea = EA_gen()
        ea.gen_need = int(args.need)
        ea.gen_range = int(args.range)
        ea.gen()

if __name__ == '__main__':
    main()

