from tkinter import *
from sympy import *
from sympy.core.sympify import kernS
from functions import parabolic_interpolation


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TheApp(Frame, metaclass=Singleton):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.current_row = 0  # row number
        self.current_col = 0  # column number
        self.function1 = StringVar()
        self.function2 = StringVar()
        self.u1 = StringVar()
        self.u2 = StringVar()
        # precision
        self.e = StringVar()
        self.answer = Label(self, text="")
        self.init_ui()

    def init_ui(self):
        self.parent.title("4")
        # first function entry block

        Label(self, text="Введите первую функцию: ").grid(row=self.current_row,
                                                          column=self.current_col, columnspan=2, sticky=W)
        self.current_row += 1
        self.current_col = 0

        function1_frame = Frame(self)
        function1_frame.grid(row=self.current_row, column=self.current_col)
        function1_frame_row = 0
        function1_frame_col = 0

        Label(function1_frame, text="f1(x1, x2)=").grid(row=function1_frame_row, column=function1_frame_col)
        function1_frame_col += 1

        Entry(function1_frame, textvar=self.function1, width=25).grid(row=function1_frame_row,
                                                                      column=function1_frame_col)
        function1_frame_col += 1

        Label(function1_frame, text=" -> min").grid(row=function1_frame_row, column=function1_frame_col)
        self.current_row += 1
        self.current_col = 0

        # second function entry block

        Label(self, text="Введите вторую функцию: ").grid(row=self.current_row,
                                                          column=self.current_col, columnspan=2, sticky=W)
        self.current_row += 1

        function2_frame = Frame(self)
        function2_frame.grid(row=self.current_row, column=self.current_col)
        function2_frame_row = 0
        function2_frame_col = 0

        Label(function2_frame, text="f2(x1, x2)=").grid(row=function2_frame_row, column=function2_frame_col)
        function2_frame_col += 1

        Entry(function2_frame, textvar=self.function2, width=25).grid(row=function2_frame_row,
                                                                      column=function2_frame_col)
        function2_frame_col += 1

        Label(function2_frame, text=" -> min").grid(row=function2_frame_row, column=function2_frame_col)
        self.current_row += 1
        self.current_col = 0

        # goal function block

        Label(self, text="Введите параметры целевой функции и точность: ").grid(row=self.current_row,
                                                                                column=self.current_col, sticky=W)
        self.current_row += 1

        goal_function = Frame(self)
        goal_function.grid(row=self.current_row, column=self.current_col, sticky=W)
        goal_function_row = 0
        goal_function_col = 0

        Label(goal_function, text="Φ(x)= ").grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Entry(goal_function, textvar=self.u1, width=4).grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Label(goal_function, text=" f1(x)+ ").grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Entry(goal_function, textvar=self.u2, width=4).grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Label(goal_function, text=" f2(x), ").grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Label(goal_function, text="e= ").grid(row=goal_function_row, column=goal_function_col)
        goal_function_col += 1

        Entry(goal_function, textvar=self.e, width=4).grid(row=goal_function_row, column=goal_function_col)
        self.current_row += 1
        self.current_col = 0

        Button(self, text="Решить", command=self.optimize).grid(row=self.current_row, column=self.current_col,
                                                                columnspan=4)
        self.current_row += 1
        self.current_col = 0

        self.pack()

    def optimize(self):
        f1 = kernS(self.function1.get())
        f2 = kernS(self.function2.get())
        u1 = kernS(self.u1.get())
        u2 = kernS(self.u2.get())
        e = float(self.e.get())
        # d lambda
        dl = 0.5

        f = (u1*f1 + u2*f2).expand()
        print(f)

        # let's begin

        # preparations

        x1, x2 = symbols("x1 x2")
        # direction vector
        ej = [0, 0]
        # initial approximations for solution matrix and value
        X = [1, 1]
        F = f.subs({x1: X[0], x2: X[1]})
        print("F " + str(F))
        # optimal solution matrix and value, set as initial ones
        opt_X = X
        opt_F = F

        while True:
            # step 3
            # checking if precision conditions met

            j = 0
            while j < len(X):
                # step 2
                # repeating this cycle for each direction toward each variable (x1, ..., xn)

                # step 1
                # optimizing initially approximated solution matrix toward current direction

                # changing vector direction according to current argument
                ej[j] = 1
                print("ej " + str(ej))
                # setting approximations for optimals
                X = opt_X
                F = opt_F

                # forming 3 points for parabola approximation
                # Y - points, lam - points for parabola, P - f(Yi)
                Y = []
                lam = []
                P = []
                # first point is current point
                Y.append(X)
                lam.append(0)
                print("Y " + str(Y[0][0]) + " " + str(Y[0][1]))
                P.append(f.subs({x1: Y[0][0], x2: Y[0][1]}))
                # second point is current point + offset dl in ej direction
                Y.append([X[0] + dl * ej[0], X[1] + dl * ej[1]])
                lam.append(dl)
                P.append(f.subs({x1: Y[1][0], x2: Y[1][1]}))
                # third point is chosen according to first 2
                if P[0] < P[1]:
                    Y.append([X[0] - dl * ej[0], X[1] - dl * ej[1]])
                    lam.append(-1 * dl)
                    P.append(f.subs({x1: Y[2][0], x2: Y[2][1]}))
                else:
                    Y.append([X[0] + 2 * dl * ej[0], X[1] + 2 * dl * ej[1]])
                    lam.append(2 * dl)
                    P.append(f.subs({x1: Y[2][0], x2: Y[2][1]}))

                # setting new lambda
                print("lam " + str(lam))
                print("P " + str(P))
                opt_l = parabolic_interpolation(lam, P)
                print("dl " + str(dl))
                # getting new optimal solution matrix and value
                opt_X = [X[0] + opt_l * ej[0], X[1] + opt_l * ej[1]]
                opt_F = f.subs({x1: opt_X[0], x2: opt_X[1]})
                print("opt_F " + str(opt_F))

                # resetting direction
                ej[j] = 0
                j += 1

            if (sqrt((opt_X[0]-X[0])**2+(opt_X[1]-X[1])**2) <= e) or (abs(opt_F - F) <= e):
                # if precision conditions are met, then optimals are found
                break
            else:
                continue
        # rounding to one-thousandth for output
        for i in range(0, len(opt_X)):
            opt_X[i] = round(opt_X[i], 3)
        opt_F = round(opt_F, 3)
        answer_string = "Оптимальное значение достигнуто \nв точке " + str(opt_X) + " и равно " + str(opt_F)
        self.answer.configure(text=answer_string)
        self.answer.grid(row=self.current_row, column=self.current_col, columnspan=4)


def main():
    root = Tk()
    # root.geometry("300x300")  # get rid of this at the end
    TheApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
