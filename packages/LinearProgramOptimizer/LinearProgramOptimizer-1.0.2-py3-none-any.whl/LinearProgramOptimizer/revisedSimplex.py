import numpy as np


def optimize(c, A, b, n=None, verbose=False):
    """

    :param c: An array of the coefficents of the objective function
    :param A: A square array of the coefficents of the LHS of the constraints 'must be <='
    :param b: An array of the coefficients of the RHS of the constraints 'must be <= '
    :param n: number of variables
    :return:
    """
    # defining the non-basic obj func coefficients
    cn = np.array(c).reshape(-1, 1)
    b = np.array(b).reshape(-1, 1)
    num_constr = b.shape[0]

    # defining the basic obj func coefficients
    cb = np.zeros(num_constr)

    if n == None:
        n = cn.shape[0]

    B = np.eye(num_constr)

    # defining the initial Nobasic array
    N = np.array(A)

    # defining the basic and non basic variables

    xb = np.array([i for i in range(n + 1, n + n + 1)])
    xn = np.array([i for i in range(1, n + 1)])

    i = 1
    while True:
        B_inverse = np.linalg.inv(B)  # Calculate the inverse of matrix B

        xb_prime = np.dot(B_inverse, b)  # Calculate xb_prime by multiplying B_inverse with b
        z_prime = np.dot(cb.T, xb_prime)  # Calculate the objective function value z_prime

        rc = cn.T - np.dot(np.dot(cb.T, B_inverse), N)  # Calculate the reduced cost vector rc
        if verbose:
            print(f'\nNumber {i} iteration')
            print('Reduced Cost', rc)

        i += 1

        if rc[rc > 0].size == 0:
            if verbose:
                print('No more positive reduced costs. Termination criteria met.')
            break
        else:
            entering_N = np.where(rc == [max(rc[rc > 0])])[1][
                0]  # Determine the index of the entering variable in the non-basic set
            if verbose:
                print('Entering variable:', xn[entering_N])

            aj = N[:, entering_N:entering_N + 1]  # Select the column of the entering variable from matrix N
            dividing = np.dot(B_inverse, aj)  # Calculate the dividing values for the ratio test

            f = xb_prime / dividing  # Calculate the ratios f
            if np.isnan(min(f[f > 0])).all():

                if verbose:
                    print('No finite positive ratios. Problem is unbounded.')
                break
            else:
                leaving_B = np.where(f == [min(f[f > 0])])[0][
                    0]  # Determine the index of the leaving variable in the basic set
                if verbose:
                    print('Leaving variable:', xb[leaving_B])

                # Update the entering and leaving variables in the basis
                a, v = np.copy(cn[entering_N]), np.copy(cb[leaving_B])
                j, k = np.copy(xn[entering_N]), np.copy(xb[leaving_B])
                xn[entering_N], xb[leaving_B] = k, j

                # Update the entering and leaving variables in the cost coefficient vectors
                cn[entering_N], cb[leaving_B] = v, a

                # Update the entering and leaving variables in the matrix B and N
                a = np.copy(B[:, leaving_B:leaving_B + 1])
                v = np.copy(N[:, entering_N:entering_N + 1])
                B[:, leaving_B:leaving_B + 1], N[:, entering_N:entering_N + 1] = v, a

    optimal = {}
  
    xb = list(xb)
    for variable in xb:
        if variable <= n:
            optimal[f'X{variable}'] = xb_prime[xb.index(variable)]

    optimal['obj function'] = z_prime

    if verbose:
        print(optimal)
    return optimal



