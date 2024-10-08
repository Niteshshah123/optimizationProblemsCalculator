import numpy as np
import sympy as sp
import pandas as pd

# Define the symbolic variables
a = int(input("Please enter the number of variable min 2 and max 4: "))
if a == 2:
    x1, x2 = sp.symbols('x1 x2')

    # Define the function
    f_expr = input("Enter the function containing x1 and x2 variables only: ")
    f = sp.lambdify((x1, x2), sp.sympify(f_expr), 'numpy')

    # Given values
    X1 = list(map(int, input("Enter the initial values of x1 and x2 separated by space: ").strip().split()))
    X1 = np.array(X1)
    delx1 = float(input("Enter the value of delta x1: "))
    delx2 = float(input("Enter the value of delta x2: "))
    ep = float(input("Enter the value of epsilon: "))

    # Hooke-Jeeves search algorithm
    rsl = []
    for i in range(20):
        # Explanatory move in x1 direction
        A = np.array([X1[0] - delx1, X1[1]])
        B = np.array([X1[0] + delx1, X1[1]])
        fminus = f(A[0], A[1])
        ff = f(X1[0], X1[1])
        fplus = f(B[0], B[1])
        x_vector = [A, X1, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x2 direction
        A = np.array([xmin[0], xmin[1] - delx2])
        B = np.array([xmin[0], xmin[1] + delx2])
        fminus = f(A[0], A[1])
        ff = f(xmin[0], xmin[1])
        fplus = f(B[0], B[1])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]
        A = xmin

        # Pattern search
        if np.array_equal(X1, A):
            delx1 /= 2
            delx2 = delx1 / 2
            if delx1 <= ep:
                n = i
                print(f'The optimal solution is X2 =[{X1[0]};{X1[1]}]')
                break
        else:
            # Pattern move
            S = A - X1  # Calculate direction

            # To calculate lambda
            df_dx1 = sp.diff(f_expr, x1)
            df_dx2 = sp.diff(f_expr, x2)
            d2f_dx1x1 = sp.diff(df_dx1, x1)
            d2f_dx2x2 = sp.diff(df_dx2, x2)
            d2f_dx1x2 = sp.diff(df_dx1, x2)
            d2f_dx2x1 = sp.diff(df_dx2, x1)
            H = sp.Matrix([[d2f_dx1x1, d2f_dx1x2], [d2f_dx2x1, d2f_dx2x2]])
            delf = sp.Matrix([df_dx1, df_dx2])
            delfA = delf.subs([(x1, A[0]), (x2, A[1])])
            S_mat = sp.Matrix(S)
            lambda_val = -delfA.dot(S_mat) / (S_mat.dot(H * S_mat))

            # New point
            X2 = np.array(A + lambda_val * S, dtype=float)
            rsl.append([i, X1.copy(), A.copy(), S, float(lambda_val), X2.copy()])

            # Check optimality
            delfX2 = delf.subs([(x1, X2[0]), (x2, X2[1])])
            if delfX2[0] == 0 and delfX2[1] == 0:
                n = i
                print(f'The optimal solution is X2 =[{X2[0]};{X2[1]}]')
                break
            else:
                X1 = X2

    # Create a result table
    Variables = ['k', 'Initial value', 'Explanatory move', 'Direction S', 'lambda', 'Pattern move']
    Resl = pd.DataFrame(rsl, columns=Variables)
    print(Resl)

    # Optimal value
    fopt = f(X2[0], X2[1])
    print(f'Optimal value of x=[{X2[0]}; {X2[1]}]')
    print(f'Optimal value of f(x)={fopt}')

elif a == 3:
    x1, x2, x3 = sp.symbols('x1 x2 x3')

    # Define the function
    f_expr = input("Enter the function containing x1, x2 and x3 variables only: ")
    f = sp.lambdify((x1, x2, x3), sp.sympify(f_expr), 'numpy')

    # Given values
    X1 = list(map(int, input("Enter the initial values of x1, x2, x3 separated by space: ").strip().split()))
    X1 = np.array(X1)
    delx1 = float(input("Enter the value of delta x1: "))
    delx2 = float(input("Enter the value of delta x2: "))
    delx3 = float(input("Enter the value of delta x3: "))
    ep = float(input("Enter the value of epsilon: "))

    # Hooke-Jeeves search algorithm
    rsl = []
    for i in range(20):
        # Explanatory move in x1 direction
        A = np.array([X1[0] - delx1, X1[1], X1[2]])
        B = np.array([X1[0] + delx1, X1[1], X1[2]])
        fminus = f(A[0], A[1], A[2])
        ff = f(X1[0], X1[1], X1[2])
        fplus = f(B[0], B[1], B[2])
        x_vector = [A, X1, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x2 direction
        A = np.array([xmin[0], xmin[1] - delx2, xmin[2]])
        B = np.array([xmin[0], xmin[1] + delx2, xmin[2]])
        fminus = f(A[0], A[1], A[2])
        ff = f(xmin[0], xmin[1], xmin[2])
        fplus = f(B[0], B[1], B[2])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x3 direction
        A = np.array([xmin[0], xmin[1], xmin[2] - delx3])
        B = np.array([xmin[0], xmin[1], xmin[2] + delx3])
        fminus = f(A[0], A[1], A[2])
        ff = f(xmin[0], xmin[1], xmin[2])
        fplus = f(B[0], B[1], B[2])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]
        A = xmin

        # Pattern search
        if np.array_equal(X1, A):
            delx1 /= 2
            delx2 = delx1 / 2
            delx3 = delx1 / 2
            if delx1 <= ep:
                n = i
                print(f'The optimal solution is X2 =[{X1[0]};{X1[1]};{X1[2]}]')
                break
        else:
            # Pattern move
            S = A - X1  # Calculate direction

            # To calculate lambda
            df_dx1 = sp.diff(f_expr, x1)
            df_dx2 = sp.diff(f_expr, x2)
            df_dx3 = sp.diff(f_expr, x3)
            d2f_dx1x1 = sp.diff(df_dx1, x1)
            d2f_dx2x2 = sp.diff(df_dx2, x2)
            d2f_dx3x3 = sp.diff(df_dx3, x3)
            d2f_dx1x2 = sp.diff(df_dx1, x2)
            d2f_dx1x3 = sp.diff(df_dx1, x3)
            d2f_dx2x3 = sp.diff(df_dx2, x3)
            d2f_dx2x1 = sp.diff(df_dx2, x1)
            d2f_dx3x1 = sp.diff(df_dx3, x1)
            d2f_dx3x2 = sp.diff(df_dx3, x2)
            H = sp.Matrix([[d2f_dx1x1, d2f_dx1x2, d2f_dx1x3],
                           [d2f_dx2x1, d2f_dx2x2, d2f_dx2x3],
                           [d2f_dx3x1, d2f_dx3x2, d2f_dx3x3]])
            delf = sp.Matrix([df_dx1, df_dx2, df_dx3])
            delfA = delf.subs([(x1, A[0]), (x2, A[1]), (x3, A[2])])
            S_mat = sp.Matrix(S)
            lambda_val = -delfA.dot(S_mat) / (S_mat.dot(H * S_mat))

            # New point
            X2 = np.array(A + lambda_val * S, dtype=float)
            rsl.append([i, X1.copy(), A.copy(), S, float(lambda_val), X2.copy()])

            # Check optimality
            delfX2 = delf.subs([(x1, X2[0]), (x2, X2[1]), (x3, X2[2])])
            if delfX2[0] == 0 and delfX2[1] == 0 and delfX2[2] == 0:
                n = i
                print(f'The optimal solution is X2 =[{X2[0]};{X2[1]};{X2[2]}]')
                break
            else:
                X1 = X2

    # Create a result table
    Variables = ['k', 'Initial value', 'Explanatory move', 'Direction S', 'lambda', 'Pattern move']
    Resl = pd.DataFrame(rsl, columns=Variables)
    print(Resl)

    # Optimal value
    fopt = f(X2[0], X2[1], X2[2])
    print(f'Optimal value of x=[{X2[0]}; {X2[1]}; {X2[2]}]')
    print(f'Optimal value of f(x)={fopt}')

elif a == 4:
    import numpy as np
    import sympy as sp
    import pandas as pd

    # Define the symbolic variables
    x1, x2, x3, x4 = sp.symbols('x1 x2 x3 x4')

    # Define the function
    f_expr = input("Enter the function containing x1, x2, x3, and x4 variables only: ")
    f = sp.lambdify((x1, x2, x3, x4), sp.sympify(f_expr), 'numpy')

    # Given values
    X1 = list(map(int, input("Enter the initial values of x1, x2, x3, x4 separated by space: ").strip().split()))
    X1 = np.array(X1)
    delx1 = float(input("Enter the value of delta x1: "))
    delx2 = float(input("Enter the value of delta x2: "))
    delx3 = float(input("Enter the value of delta x3: "))
    delx4 = float(input("Enter the value of delta x4: "))
    ep = float(input("Enter the value of epsilon: "))

    # Hooke-Jeeves search algorithm
    rsl = []
    for i in range(20):
        # Explanatory move in x1 direction
        A = np.array([X1[0] - delx1, X1[1], X1[2], X1[3]])
        B = np.array([X1[0] + delx1, X1[1], X1[2], X1[3]])
        fminus = f(A[0], A[1], A[2], A[3])
        ff = f(X1[0], X1[1], X1[2], X1[3])
        fplus = f(B[0], B[1], B[2], B[3])
        x_vector = [A, X1, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x2 direction
        A = np.array([xmin[0], xmin[1] - delx2, xmin[2], xmin[3]])
        B = np.array([xmin[0], xmin[1] + delx2, xmin[2], xmin[3]])
        fminus = f(A[0], A[1], A[2], A[3])
        ff = f(xmin[0], xmin[1], xmin[2], xmin[3])
        fplus = f(B[0], B[1], B[2], B[3])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x3 direction
        A = np.array([xmin[0], xmin[1], xmin[2] - delx3, xmin[3]])
        B = np.array([xmin[0], xmin[1], xmin[2] + delx3, xmin[3]])
        fminus = f(A[0], A[1], A[2], A[3])
        ff = f(xmin[0], xmin[1], xmin[2], xmin[3])
        fplus = f(B[0], B[1], B[2], B[3])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]

        # Explanatory move in x4 direction
        A = np.array([xmin[0], xmin[1], xmin[2], xmin[3] - delx4])
        B = np.array([xmin[0], xmin[1], xmin[2], xmin[3] + delx4])
        fminus = f(A[0], A[1], A[2], A[3])
        ff = f(xmin[0], xmin[1], xmin[2], xmin[3])
        fplus = f(B[0], B[1], B[2], B[3])
        x_vector = [A, xmin, B]
        f_vector = [fminus, ff, fplus]
        min_index = np.argmin(f_vector)
        xmin = x_vector[min_index]
        A = xmin

        # Pattern search
        if np.array_equal(X1, A):
            delx1 /= 2
            delx2 = delx1 / 2
            delx3 = delx1 / 2
            delx4 = delx1 / 2
            if delx1 <= ep:
                n = i
                print(f'The optimal solution is X2 =[{X1[0]};{X1[1]};{X1[2]};{X1[3]}]')
                break
        else:
            # Pattern move
            S = A - X1  # Calculate direction

            # To calculate lambda
            df_dx1 = sp.diff(f_expr, x1)
            df_dx2 = sp.diff(f_expr, x2)
            df_dx3 = sp.diff(f_expr, x3)
            df_dx4 = sp.diff(f_expr, x4)
            d2f_dx1x1 = sp.diff(df_dx1, x1)
            d2f_dx2x2 = sp.diff(df_dx2, x2)
            d2f_dx3x3 = sp.diff(df_dx3, x3)
            d2f_dx4x4 = sp.diff(df_dx4, x4)
            d2f_dx1x2 = sp.diff(df_dx1, x2)
            d2f_dx1x3 = sp.diff(df_dx1, x3)
            d2f_dx1x4 = sp.diff(df_dx1, x4)
            d2f_dx2x3 = sp.diff(df_dx2, x3)
            d2f_dx2x4 = sp.diff(df_dx2, x4)
            d2f_dx2x1 = sp.diff(df_dx2, x1)
            d2f_dx3x1 = sp.diff(df_dx3, x1)
            d2f_dx3x2 = sp.diff(df_dx3, x2)
            d2f_dx3x4 = sp.diff(df_dx3, x4)
            d2f_dx4x1 = sp.diff(df_dx4, x1)
            d2f_dx4x2 = sp.diff(df_dx4, x2)
            d2f_dx4x3 = sp.diff(df_dx4, x3)
            H = sp.Matrix([[d2f_dx1x1, d2f_dx1x2, d2f_dx1x3, d2f_dx1x4],
                           [d2f_dx2x1, d2f_dx2x2, d2f_dx2x3, d2f_dx2x4],
                           [d2f_dx3x1, d2f_dx3x2, d2f_dx3x3, d2f_dx3x4],
                           [d2f_dx4x1, d2f_dx4x2, d2f_dx4x3, d2f_dx4x4]])
            delf = sp.Matrix([df_dx1, df_dx2, df_dx3, df_dx4])
            delfA = delf.subs([(x1, A[0]), (x2, A[1]), (x3, A[2]), (x4, A[3])])
            S_mat = sp.Matrix(S)
            lambda_val = -delfA.dot(S_mat) / (S_mat.dot(H * S_mat))

            # New point
            X2 = np.array(A + lambda_val * S, dtype=float)
            rsl.append([i, X1.copy(), A.copy(), S, float(lambda_val), X2.copy()])

            # Check optimality
            delfX2 = delf.subs([(x1, X2[0]), (x2, X2[1]), (x3, X2[2]), (x4, X2[3])])
            if delfX2[0] == 0 and delfX2[1] == 0 and delfX2[2] == 0 and delfX2[3] == 0:
                n = i
                print(f'The optimal solution is X2 =[{X2[0]};{X2[1]};{X2[2]};{X2[3]}]')
                break
            else:
                X1 = X2

    # Create a result table
    Variables = ['k', 'Initial value', 'Explanatory move', 'Direction S', 'lambda', 'Pattern move']
    Resl = pd.DataFrame(rsl, columns=Variables)
    print(Resl)

    # Optimal value
    fopt = f(X2[0], X2[1], X2[2], X2[3])
    print(f'Optimal value of x=[{X2[0]}; {X2[1]}; {X2[2]}; {X2[3]}]')
    print(f'Optimal value of f(x)={fopt}')



