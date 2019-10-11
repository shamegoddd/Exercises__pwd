import os, re


def check(list,answer , e_file , a_file):
    #读取文件
    efile=open(e_file,"r")
    afile=open(a_file,"r")
    #定义一个list用来存储具有相同结果的式子
    salist = []
    #先判断库中是否有相同的结果
    i=0
    j=0
    for aline in afile.readlines():
        answer=answer.strip()
        realanswer=aline.split(':')[1]
        realanswer=realanswer.strip()
        if answer == realanswer:
            i+=1
            for eline in efile.readline():
                j+=1
                if j == i :
                    #提取出式子
                    eline=eline.split(':')[1]
                    eline=eline.split('=')[0]
                    salist.append(eline.strip())
                    break


    return (not isSame(list,salist))


    return True


#都是先判断字符串是否一样，运算符是否一样，数字是否一样
#对于只有一个运算符的,先判断运算符是否一样，若一样再判断数字是否完全一样
'''对于有两个运算符的，若以上都一样，则有以下几种情况：
    1.(NoN)oN
    2.No(NoN)
    3.NoNoN
    将他们每个元素放入list中
        1.若list长度均为6(无括号情况)：
           若两个式子都是list1[1]==list2[1] AND list1[3]==list2[3]：
                if list1[0]=list2[4] and list1[2]=list2[2]:
                    return True
                else 
                    return False
            else :
                reurn False
        2.若list1长度为6list2长度为8：
            若list2[0]='(':
                if list1[1]等于list2[1]或list2[3]
                    reutnr True 
                else
                    return False
        3.若list1长度为8，list2长度为6：
            若list1[0]='(':
                if list2[1]等于list1[1]或list1[3]
                    reutnr True 
                else
                    return False
        4.若长度均为8：
            判断括号中的数字是否一样即可
    
    对于三个运算符的情况，由于种类较多，若以上都一样，则返回TRUE，否则返回False
'''
def isSame (list,salist):
    numlist1=''.join(list).split('+|-|*|/|(|)')
    #运算符个数
    ops1=''.join(list).split('+|-')
    for string in salist:
        if numlist1 == string:
            return True
        else :
            #判断数字是否一样
            numlist2=string.split('+|-|*|/|(|)')
            if len(numlist1)!=len(numlist2):
                return False
            else :
                for i  in numlist1 :
                    if i in numlist2:
                        continue
                    else :
                        return False
                #判断运算符个数是否一样
                if (len(list)-len(numlist1)) != (len(string)-len(numlist2)):
                    return False
                else:

                    if len(list)==6 and len(salist)==6:
                        if list[0]==string[4] and string[2]==list[2] :
                            if list[0]==salist[4] and list[2]==salist[2]:
                                return True
                            else:
                                return False
                        else:
                            return False

                    if len(list) == 6 and len(salist) == 8:
                        if salist[0] == '(':
                            if list[1]==salist[1] or list[1]==salist[3]:
                                return True

                            else:
                                return False
                    if len(list)==8 and len(salist)==6 :
                        if list[0] == '(':
                            if salist[1]==list[1] or salist[1]==list[3]:
                                return True

                            else:
                                return False

                    if  len(list)==8 and len(salist)==8:
                        return True



if __name__ == '__main__':
    check(['1','+','1'], 2 , './exercise.txt' , './answer.txt')