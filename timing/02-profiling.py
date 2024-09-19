import profile

print("Let's check where time goes into this code")
print("-"*79)
# recurse fibbocini style
def fib(n):
    if n==0 :
        return 0
    elif n ==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def fib_seq(n):
    seq=list()
    if n > 0:
        seq.extend(fib_seq(n-1))
    seq.append(fib(n))
    return seq

if __name__ == "__main__":
    profile.run("print(fib_seq(30));print()")