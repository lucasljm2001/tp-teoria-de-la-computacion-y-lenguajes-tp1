def taylor_e_x_horner(x,n):
    sum = 1.0
    for i in range(n,0,-1):
        sum = 1 + x*sum/i
    return sum

def taylor_e_x_naive(x,n):
    sum = 1.0
    for i in range(1,n+1):
        sum = sum + x**i/factorial(i)
    return sum

def taylor_e_x_optmizada(x, n_terms):
    result = 1.0  # Primer término de e^x para i=0
    term = 1.0
    for i in range(1, n_terms):
        # Actualización lineal del término
        term *= (x / i) #
        result += term
    return result


def factorial(n):
    for i in range(n-1,0,-1):
        n = n*i
    return n




if __name__ == "__main__":
    print("Horner: ", taylor_e_x_horner(4,10))
    print("Naive: ", taylor_e_x_naive(4,10))
    print("Iterativa optimizada: ", taylor_e_x_optmizada(4,10))
    print("Valor de e^4: ", 54.598150033144236)