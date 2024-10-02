from typing import Union
from random import randint
from datetime import datetime

EQUATIONS: list = []
STRFTIME: str = '%a %Y-%m-%d, %H:%M:%S'

'''HELPER FUNCTIONS'''

def factorization(n: int) -> list:
    """Order sqrt n, returns list of prime factors"""
    if n <= 1:
        return []
    
    factors: list = []
    
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # n must be odd at this point, can focus on odd factors from 3 up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    
    # Adds remaining prime factor
    if n > 2:
        factors.append(n)
    
    return factors


def sqrt_int(n: int) -> Union[int, int]:
    """Factorises n, then returns sqrt root and radicand as tuple"""
    # Prime number
    factors = factorization(n)
    if len(factors) == 1:
        return (1, n)
    
    # Tally up the factors
    counter = dict()
    for i in factors:
        counter[i] = counter.get(i, 0) + 1

    # Get product of repeated factors
    square, radicand = 1, 1
    for k, v in counter.items():
        if v // 2 > 0:
            square *= (k ** (v // 2))
        if v % 2 == 1:
            radicand *= (k ** (v % 2))
    
    return square, radicand


def calc_gcd(a: int, b: int) -> int:
    """Euclidean algorithm, GCD(A, B) = GCD(B, A mod B)"""
    if b == 0:
        return a
    return calc_gcd(b, a % b)
    

'''CLASSES'''
class Rational:
    """A rational number of form P/Q"""
    def __init__(self, numerator: int, denominator: int=1):
        self._numerator = numerator
        self._denominator = denominator
        self.simplify_frac()
    
    def get_value(self) -> float:
        return self._numerator / self._denominator
    def get_numerator(self) -> int:
        return self._numerator
    def get_denominator(self) -> int:
        return self._denominator
    
    def simplify_frac(self) -> Union[int, int]:
        """Returns simple numerator and denominator"""
        gcd = calc_gcd(self.get_numerator(), self.get_denominator())
        return self.get_numerator() // gcd, self.get_denominator() // gcd
    
    def __str__(self) -> str:
        num, den = self.simplify_frac()
        if den == 1:
            return str(num)
        return f"({num}/{den})"
    
    "Arithmetic methods"
    def __add__(self, other: 'Rational') -> 'Rational':
        num1, den1 = self.simplify_frac()
        num2, den2 = other.simplify_frac()
        return Rational(num1 * den2 + num2 * den1, den1 * den2)
    
    def __sub__(self, other: 'Rational') -> 'Rational':
        num1, den1 = self.simplify_frac()
        num2, den2 = other.simplify_frac()
        return Rational(num1 * den2 - num2 * den1, den1 * den2)
    
    def __mul__(self, other: 'Rational') -> 'Rational':
        num1, den1 = self.simplify_frac()
        num2, den2 = other.simplify_frac()
        return Rational(num1 * num2, den1 * den2)
    
    def __truediv__(self, other: 'Rational') -> 'Rational':
        # Flip a fraction, then multiply accordingly
        num1, den1 = self.simplify_frac()
        num2, den2 = other.simplify_frac()
        return Rational(num1 * den2, den1 * num2)
    
    def __neg__(self) -> 'Rational':
        return Rational(-self.get_numerator(), self.get_denominator())
    
    "Comparison methods"
    def __eq__(self, other: 'Rational') -> bool:
        return self.get_value() == other.get_value()
    def __gt__(self, other: 'Rational') -> bool:
        return self.get_value() > other.get_value()
    def __lt__(self, other: 'Rational') -> bool:
        return self.get_value() < other.get_value()
    
    "Special methods"
    def get_sqrt(self) -> str:
        num, den = self.simplify_frac()
        numsquare, numrad = sqrt_int(num)
        densquare, denrad = sqrt_int(den)

        # √(a^2b)/√(c^2d) = a√(bd)/cd
        real = Real(
            numsquare,
            densquare * denrad, 
            numrad * denrad
        )
        return real


class Real(Rational):
    """Real number with a numerator, denominator=1, and a radicand below sqrt sign=1"""
    def __init__(self, numerator: int, denominator: int=1, radicand: int=1):
        super().__init__(numerator, denominator)
        self._radicand = radicand
        self.simplify_frac()
    
    def get_value(self) -> float:
        return self._numerator / self._denominator * (self._radicand ** 0.5)
    def get_radicand(self) -> int:
        return self._radicand
    
    def __str__(self) -> str:
        # May contain a whole or rational coefficient, or a radical
        num, den = self.simplify_frac() 
        s = str(num) if den == 1 else f"({num}/{den})"
        if self._radicand > 1:
            s += f"\u221A{self._radicand}"
        return s
    
    @staticmethod
    def from_str(s: str) -> 'Real':
        """Converts string-like expression to Real number"""
        # (a/b)√c, a√c, √c, a/b, a
        s = s.strip().replace("√", "|")
        if s == "": return None
        try:
            real = Real(int(s))
            return real
        except ValueError:
            pass
        if "|" in s:
            num, rad = s.split("|")
            real = Real(int(num), 1, int(rad))
            if "/" in num:
                num = num.replace("(", "").replace(")", "")
                num, den = num.split("/")
                real = Real(int(num), int(den), int(rad))
        elif "/" in s:
            s = s.replace("(", "").replace(")", "")
            num, den = s.split("/")
            real = Real(int(num), int(den))
        else:
            return None
        try:
            real += Real(0)
            return real
        except:
            return None
    
    "Arithmetic methods"
    def unload(self, other: 'Real') -> tuple:
        """Unloads the values of two Real numbers"""
        num1, den1 = self.simplify_frac()
        num2, den2 = other.simplify_frac()
        rad1, rad2 = self.get_radicand(), other.get_radicand()
        return num1, den1, rad1, num2, den2, rad2

    def __neg__(self) -> 'Real':
        return Real(-self.get_numerator(), self.get_denominator(), self.get_radicand())
    
    def __add__(self, other: 'Real') -> 'Real':
        # a/b √x + c/d √x = ((ad + cb) / (bd)) * √x
        # TODO
        if self.get_radicand() == other.get_radicand():
            num1, den1, rad1, num2, den2 = self.unload(other)[:-1]
            return Real(num1 * den2 + num2 * den1, den1 * den2, rad1)
        
        return RealSeq(self, other)
        
    def __sub__(self, other: 'Real') -> 'Real':
        # TODO
        if self.get_radicand() == other.get_radicand():
            num1, den1, rad1, num2, den2 = self.unload(other)[:-1]
            return Real(num1 * den2 - num2 * den1, den1 * den2, rad1)
        
        return RealSeq(self, -other)
    
    def __mul__(self, other: 'Real') -> 'Real':
        num1, den1, rad1, num2, den2, rad2 = self.unload(other)
        return Real(num1 * num2, den1 * den2, rad1 * rad2)
    
    def __truediv__(self, other: 'Real') -> 'Real':
        # (n1*d2) / (d1*n2*r2) * sqrt(r1*r2)
        num1, den1, rad1, num2, den2, rad2 = self.unload(other)
        return Real(num1 * den2, den1 * num2 * rad2, rad1 * rad2)
    

class RealSeq:
    def __init__(self, *reals: Real):
        self._reals: list = list(reals)

    def __str__(self) -> str:
        for idx, r in enumerate(self._reals):
            # Adds real, or else subtracts its absolute
            if idx == 0:
                s = str(r)
            else:
                s += (" + " + str(r)) if r.get_value() > 0 else (" - " + str(-r))
        return s
    
    def get_value(self) -> float:
        return sum([r.get_value() for r in self._reals])
    

class QuadraticEquation:
    def __init__(self, a: Real, b: Real, c: Real):
        self._a = a
        self._b = b
        self._c = c

    def __str__(self) -> str:
        a = str(self._a)
        b = str(self._b)
        a = a if a != "1" else ""
        b = b if b != "1" else ""
        return f"{a}x^2 + {b}x + {self._c} = 0"
    
    def has_roots(self, return_delta=False) -> bool:
        """Uses discriminant b^2 - 4ac to determine if roots exist"""
        delta = self._b.get_value() ** 2 - 4 * self._a.get_value() * self._c.get_value()
        return delta >= 0 if not return_delta else delta

    def root_finder(self, comments: bool=False) -> tuple[Real | str]:
        """Completes the square to return roots, or explanation"""
        # Abort if no roots
        delta = self.has_roots(return_delta=True)
        if delta < 0:
            return None
        
        step: int = 0
        s: str = f"Solving following equation using complete the square method\n{self}\n"
        A, B, C = self._a, self._b, self._c

        def add_comment(i: str):
            nonlocal step, s
            step += 1
            s += f"Step {step}: {i}\n"

        RHS = -C

        # Step 1 - Divide by a
        if A.get_value() != 1:
            B /= A
            RHS /= A
            A = Real(1)
            add_comment(f"Divide value of a across the equation.\nx^2 + {self._b}x = {RHS}")
        
        # Step 2 - Add (b/2)^2 to both sides
        half_b = B / Real(2)
        half_b_squared = half_b * half_b
        RHS += half_b_squared
        add_comment(f"Add square of b/2 to both sides.\nx^2 + {B}x + {half_b_squared} = {RHS}")

        # Step 3 - Complete the square
        add_comment(f"Complete the square.\n(x + {half_b})^2 = {RHS}")

        # Step 4 - Square root both sides
        # Step 5 - Solve for x
        RHS = RHS.get_sqrt()
        if delta != 0:
            RHS_2 = -RHS
            add_comment(f"Square root both sides.\nx + {half_b} = {RHS} or x + {half_b} = {RHS_2}")
            x1: Real = RHS-half_b
            x2: Real = RHS_2-half_b
            add_comment(f"Solve for x.\nx = {x1} or x = {x2}")
        else:
            add_comment(f"Square root both sides.\nx + {half_b} = {RHS}")
            x1: Real = -half_b
            add_comment(f"Solve for x.\nx = {x1}")

        # Return comments, or else roots
        return s if comments else ((x1, x2) if delta != 0 else [x1])
    
    def get_roots(self) -> str:
        """Returns roots of a QE"""
        if (roots := self.root_finder()) is None: return None
        elif len(roots) == 1: return str(roots[0])
        return str(tuple([str(r) for r in roots])).replace("'", '')
    
    def get_roots_values(self) -> tuple[float]:
        """Returns direct values of roots of a QE"""
        if (roots := self.root_finder()) is None: return None
        elif len(roots) == 1: return roots[0].get_value()
        return tuple([r.get_value() for r in roots])

    def complete_sq(self) -> str:
        """Gives commented completion"""
        return self.root_finder(comments=True)
    
    @staticmethod
    def get_eqn_from_str(eq: str) -> 'QuadraticEquation':
        """Converts string of ax^2 + bx + c = 0 to a valid QuadraticEquation class"""
        eq = eq.strip().lower().replace(" ", "")
        if not eq.endswith("=0"): return None
        parameters = eq.split("+")
        if len(parameters) != 3: return None

        # Extracts a, b, c
        lst = []
        for param in parameters:
            param = param.replace("x2", "x^2").replace("x^2","").replace("x","").replace("=0","")
            if len(param) == 0 or param is None:
                param = "1"
            real = Real.from_str(param)
            if not real: return None
            lst.append(real)
        
        return QuadraticEquation(*lst)
    
    @staticmethod
    def gen_random_eqn() -> 'QuadraticEquation':
        params: list[Real] = []
        for _ in range(3):
            elem = Real(0)
            while elem.get_value() == 0:
                elem = Real(
                    randint(-randint(18,25), randint(18,25)),
                    randint(1, randint(9,11))
                )
            params.append(elem)
        
        return QuadraticEquation(*params)
    

class Color:
    _ = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
        

'''MAIN'''

def help_screen():
    print(f"{Color.YELLOW}<-- Quadratics Calculator -->")
    print("1. Key in new equation")
    print("2. Recall equations")
    print("3. Solve equation with roots")
    print("4. Solve equation via completing the square")
    print("5. Download equations in memory, save solutions to file")
    print("6. Generate a series of random equations and save to a file")
    print("7. Read from file, solve all equations, save solutions to another file")
    print("8. Help Screen")
    print(f"9. Exit{Color._}")

def main():
    no_equation = lambda: print(f"{Color.BLUE}[!] No equations in memory.{Color._}")
    try:
        help_screen()
        while True:
            try:
                option = int(input (f"{Color.YELLOW}>{Color._} Select a function: ").strip())
                if not (1 <= option <= 9):
                    raise ValueError
            except ValueError:
                print(f"{Color.RED}[!] {Color._}", end="")
                continue
            match option:
                # Enter expression
                case 1:
                    eqn = input(f"{Color.YELLOW}> Enter a quadratic equation (ax^2 + bx + c = 0): {Color._}").strip()
                    if (qe := QuadraticEquation.get_eqn_from_str(eqn)) is None:
                        print(f"{Color.RED}[!] Invalid equation. {Color._}")
                        continue
                    EQUATIONS.append(qe)
                    print(f"{Color.GREEN}[+] Equation added successfully!{Color._}")

                # Recall equations
                case 2:
                    if not EQUATIONS:
                        no_equation()
                        continue
                    for idx, eq in enumerate(EQUATIONS):
                        print(f"{Color.BLUE}[{idx+1}] {eq}{Color._}")

                # Solve equation with roots, or complete square
                case 3 | 4:
                    N: int = len(EQUATIONS)
                    if N == 0:
                        no_equation()
                        continue
                    # Receive user input on index
                    try:
                        n = int(input (f"{Color.YELLOW}>{Color._} Give an equation index: ").strip())
                        if not (0 <= (n := n-1) < N):
                            raise ValueError
                    except ValueError:
                        print(f"{Color.RED}[!] Invalid input.{Color._}")
                        continue
                    eq = EQUATIONS[n]
                    if not eq.has_roots():
                        print(f"{Color.RED}[+] No roots found.{Color._}")
                        continue

                    # Print roots, or print complete square
                    if option == 3:
                        print(f"{Color.GREEN}[+] Root(s) of {eq}: {eq.get_roots()}\nRoot(s) in exact value: {eq.get_roots_values()}{Color._}")
                    else:
                        print(f"{Color.GREEN}[+] {eq.complete_sq()}{Color._}")

                # Download equations into memory
                case 5:
                    if not EQUATIONS:
                        no_equation()
                        continue
                    
                    s: str = ""
                    for idx, eqn in enumerate(EQUATIONS):
                        idx += 1
                        s += f"Equation {idx}: {eqn}\n{'Roots':>8} {idx}: {str(eqn.get_roots()).replace('√', '|')}\n\n"

                    with open("equations.txt", "w") as f:
                        f.write(f"{datetime.now().strftime(STRFTIME)}\n")
                        f.write(s)
                    
                    print(f"{Color.GREEN}[+] Downloaded equations and roots from memory to 'equations.txt'{Color._}")

                # Generate random equations
                case 6:
                    try:
                        n = int(input (f"{Color.YELLOW}>{Color._} No. of equations to generate (max 99): ").strip())
                        if not (0 <= n <=99):
                            raise ValueError
                    except ValueError:
                        print(f"{Color.RED}[!] Invalid input.{Color._}")
                        continue
                    
                    s: str = "\n".join([str(QuadraticEquation.gen_random_eqn()) for _ in range(n)])
                    with open("equations.txt", "w") as f:
                        f.write(f"{datetime.now().strftime(STRFTIME)}\n")
                        f.write(s)
                    
                    print(f"{Color.GREEN}[+] Generated {n} equations, saved to 'equations.txt'{Color._}")
                
                # Read from file, solve all equations
                case 7:
                    try:
                        with open("equations.txt", "r") as f:
                            lines = f.readlines()
                            if len(lines) < 1:
                                raise FileNotFoundError
                    except FileNotFoundError:
                        print(f"{Color.RED}[!] 'equations.txt' invalid.{Color._}")
                        continue

                    # Interpret equations, solve them
                    s: list[QuadraticEquation] = [QuadraticEquation.get_eqn_from_str(eqn.strip()) for eqn in lines]
                    s = "\n".join([str(qe.get_roots()) for qe in s if qe])

                    if len(s.strip()) == 0:
                        print(f"{Color.RED}[!] No valid equations solved.{Color._}")
                        continue

                    with open("solutions.txt", "w") as f:
                        f.write(f"{datetime.now().strftime(STRFTIME)}\n")
                        f.write(s)
                    
                    print(f"{Color.GREEN}[+] Solved equations, saved to 'solutions.txt'{Color._}")
                        
                case 8:
                    help_screen()
                case 9:
                    raise EOFError
    except BaseException:
        print(f"{Color._}\nExiting... Thank you.\n")
        return


main()