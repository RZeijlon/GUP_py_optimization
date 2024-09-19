"""
script explain how e can use and measure timing into python code
"""
import timeit

def old_fashion(n)->list:
    i = 0
    result = list()
    while i< n:
        result.append(str(i))
        i +=1
    return result

def modern_function(n):
    return list(map(str,range(n)))

if __name__ == "__main__":
    setup_old ="""
def old_fashion(n)->list:
    i = 0
    result = list()
    while i< n:
        result.append(str(i))
        i +=1
    return result
"""
    stmt_old = "old_fashion(1_000_000)"
    #timing_for_old_fashion = timeit.timeit(setup=setup_old,stmt=stmt_old,number=100)
    #print(f"Time to old fashion is = {timing_for_old_fashion}")

    setup_modern = """
def modern_function(n):
    return list(map(str,range(n)))
"""
    stmt_modern = "modern_function(1_000_000)"
    #timing_for_modern_function = timeit.timeit(setup=setup_modern,stmt=stmt_modern,number=100)
    #print(f"Time to old fashion is = {timing_for_modern_function}")
    timing_for_modern_function_r_5 = timeit.repeat(setup=setup_modern,stmt=stmt_modern,number=100,repeat = 5)
    print(f"Time to old fashion is = {timing_for_modern_function_r_5}")




