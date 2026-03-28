def taylor_e_x_1(x,n):
    sum = 1.0
    for i in range(n,0,-1):
        sum = 1 + x*sum/i
    return sum

def taylor_e_x_2(x,n):
    sum = 1.0
    for i in range(1,n+1):
        sum = sum + x**i/factorial(i)
    return sum


def factorial(n):
    for i in range(n-1,0,-1):
        n = n*i
    return n


if __name__ == "__main__":
    print("Primera función: ", taylor_e_x_1(4,10))
    print("Segunda función: ", taylor_e_x_2(4,10))
    print("Valor de e^4: ", 54.598150033144236)