
a = []
for i in range(10):
    def func():
        print(i)
    a.append(func)

# a放入了每个函数，而i又是全局的，所以打印出来的都是9
a[6]()
print(i)

b= []
for x in range(6):
    b.append(x)

print(b[3])

c = {'x':'y'}
d = 7

b.append(d)
print(b)
d = 8
print(b)

b.append(c)
print(b)
c['x']='z'
print(b)  # 对应b来说,c不属于基础类型，所以他存的是对象引用，
            # 当c引用的对象值发生了变化，b中的也会发生变化
c = {'x','f'}
print(b)    # 而当c的引用指向了另一个对象，就和b没有半毛钱关系了，
            # 即使这时c怎么改变，b中也不会变化