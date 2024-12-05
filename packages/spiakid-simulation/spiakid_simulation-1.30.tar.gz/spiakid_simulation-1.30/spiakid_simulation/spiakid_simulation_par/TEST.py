import multiprocessing as mp
import numpy as np

def para2(i):
    lol = np.linspace(0,1,1000000)
    return(i-1)

def para(args):
    a, l = args
    # print('done', flush = True)
    return(a+l)

l = np.linspace(1,10,1000)
a = np.linspace(1,5,1000)
args = []

for j in range(len(a)):
    args.append([a[j],l[j]])
print(len(args))
with mp.Pool(processes=2) as pool:
    res = pool.map(para, args)
    pool.close()
    pool.join()


# from multiprocessing import Pool

# def f(x):
#     return x*x

# if __name__ == '__main__':
#     with Pool(processes=5) as p:
#         print(p.map(para, l))