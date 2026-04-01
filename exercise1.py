import time
import gmpy2
import sys


def fib_iter(n: int) -> int:
    if n < 0: 
        raise ValueError
    
    n1 = 0
    n2 = 1
    p = 0

    for i in range(n):
        p = n2
        n2 = n1 + n2
        n1 = p

    return n1
    


def mat_mul(A: tuple[int, int, int, int],
            B: tuple[int, int, int, int]) -> tuple[int, int, int, int]:

    C = (
        A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3], A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3]
    )
    
    return C


def mat_pow(M: tuple[int, int, int, int], n: int) -> tuple[int, int, int, int]:

    if n < 0: 
        raise ValueError

    R = (1, 0, 0, 1)
    while n > 0:
        if n % 2 == 1: R = mat_mul(R, M)
        M = mat_mul(M, M)
        n = n >> 1

    return R


def fib_matrix(n: int) -> int:


    if n < 0: 
        raise ValueError

    A = (1, 1, 1, 0)
    return mat_pow(A,n)[1]
    


def main() -> None:
    n = int(input("Value of n: "))

    if n < 0: 
        raise ValueError

    start = time.perf_counter()
    f1 = fib_iter(n)
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    f2 = fib_matrix(n)
    t2 = time.perf_counter() - start

    start = time.perf_counter()
    f3 = gmpy2.fib(n)
    t3 = time.perf_counter() - start



    print(f"fib_iter:   {t1:.6f} s")
    print(f"fib_matrix: {t2:.6f} s")
    print(f"gmpy2.fib:  {t3:.6f} s")

    print("Number of digits:")
    print("fib_iter:",   len(str(f1)))
    print("fib_matrix:", len(str(f2)))
    print("gmpy2.fib:",  len(str(f3)))



    with open("fib_iter.txt", "w") as f:
        f.write(str(f1))

    with open("fib_matrix.txt", "w") as f:
        f.write(str(f2))

    with open("fib_gmpy2.txt", "w") as f:
        f.write(str(f3))


if __name__ == "__main__":
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    main()
