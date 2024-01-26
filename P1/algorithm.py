from timeit import timeit
import random



def alghorithm(arr):
    n = len(arr)
    y = 0

    for i in range(n):
        if arr[i] == 0:
            for j in range(i, n):
                y += 1
                k = n
                while k > 0:
                    k = k // 3
                    y += 1  
        elif arr[i] == 1:
            for m in range(i, n):
                y += 1
                for l in range(m, n):
                    for t in range(n, 0, -1):
                        for z in range(n, 0, -t):
                            y += 1
        else:
            y += 1
            p = 0
            while p < n:
                for j in range(p ** 2 - 1):
                    y += 1
                p += 1
    return y


num = [0, 1, 2]
arr = []

sample_arr = [2,2,2,2,2]


exec_counts = [1, 5] + list(range(10, 151, 10))


def execution(arr, n, case, exec_count= None):
    if case == "best":
        arr = [0] * n

        best_time = timeit(lambda: alghorithm(arr), number=1)
        # format the time 4 decimal places
        print(f"Case: {case} Size: {n} Elapsed Time (s): {best_time:.10f}") 
    if case == "worst":
        arr = [1] * n
        worst_time = timeit(lambda: alghorithm(arr), number=1)
        print(f"Case: {case} Size: {n} Elapsed Time (s): {worst_time:.10f}")
    if case == "average":
        exec_times = []
        print("Average Times: ", end="")
        for _ in range(exec_count):
            arr = [random.choice(num) for i in range(n)]
            average_time = timeit(lambda: alghorithm(arr), number=1)
            print(f"{average_time:.10f}", end=" ")
            exec_times.append(average_time)
        print()
        print(f"Case: {case} Size: {n} Elapsed Time (s): {sum(exec_times)/len(exec_times):.10f}")
            
return_value = alghorithm(sample_arr)
for n in exec_counts:
    execution(arr, n, "best")
    execution(arr, n, "worst")
    execution(arr, n, "average", exec_count=10)
    print()


