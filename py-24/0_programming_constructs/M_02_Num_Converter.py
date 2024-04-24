DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

to_symb = lambda n: DIGITS[n]
to_val = lambda n: DIGITS.index(n)


def cleanup_num(x: str, base: int) -> str | bool:
    """Returns a cleanly parsed num-string"""
    if x.count("0") == len(x):
        return "0"
    
    # Not zero, strip any preceding zeroes
    x = x.lstrip("0")

    # Validates base
    acceptable_digits = DIGITS[:base]
    for dgt in x:
        if dgt not in acceptable_digits:
            return False
        
    return x


def cross_convert(x: str, b1: int, b2: int) -> str:
    """Converts num-string x of base <b1> to num-string of base <b2>"""
    return "0" if x == "0" else den_to_any(any_to_den(x, b1), b2) 


def any_to_den(x: str, base: int) -> int:
    if len(x) == 0:
        return 0
    
    multi = base ** (len(x)-1)
    val = int(to_val(x[0]))
    return val * multi + any_to_den(x[1:], base)


def den_to_any(n: int, base: int) -> str:
    if n <= 0:
        return ""
    
    # Lowest-order digit shld be prepended
    symb = to_symb(n % base)
    return den_to_any(n // base, base) + symb


def main() -> None:
    progress = True
    print("Welcome to the UNIVERSAL COUNCIL™ Converter.", end="")
    while progress:
        print(f"\n{'-'*44}\n[1] ANY Base Conversion\n[2] Denary (10) -> Binary (2)\n[3] Binary -> Denary\n[4] Binary -> Octal (8) & Hex (16)\n[5] Octal -> Binary & Hex\n[6] Hex -> Binary & Octal\n[0] Quit\n\n* All followup inputs should be positive integers with digits exclusively to that base!")
        match input("> ").strip().upper():
            # Any base
            case "1":
                while True:
                    b1 = input("> Current Base (2-36): ").strip()
                    if b1.isdigit() and (2 <= (b1 := int(b1)) <= 36):
                        break
                    print("Please input a valid integer from 2 to 36.")
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, b1):
                        break
                    print(f"Please input a valid number of base-{b1}.")
                while True:
                    b2 = input("> Output Base (2-36): ").strip()
                    if b2 == b1:
                        print("Try converting to a different base.")
                        continue
                    elif b2.isdigit() and (2 <= (b2 := int(b2)) <= 36):
                        break
                    print("Please input a valid integer from 2 to 36.")
                res = cross_convert(n, b1, b2)
                print(f"\n⊱ Input, B-{b1}:{' '*(4-len(str(b1)))}{n}\n⊱ Output, B-{b2}:{' '*(3-len(str(b2)))}{res}\n")
            # Den -> Bin
            case "2":
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, 10):
                        n = int(n)
                        break
                    print(f"Please input a valid denary number.")
                res = den_to_any(n, 2) if n != "0" else "0"
                print(f"\n⊱ Input, B-10: {n}\n⊱ Output, B-2: {res}\n")
            # Bin -> Den
            case "3":
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, 2):
                        break
                    print(f"Please input a valid binary number.")
                res = any_to_den(n, 2)
                print(f"\n⊱ Input, B-2:   {n}\n⊱ Output, B-10: {res}\n")
            # Bin -> Oct + Hex
            case "4":
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, 2):
                        break
                    print(f"Please input a valid binary number.")
                res_o = cross_convert(n, 2, 8)
                res_h = cross_convert(n, 2, 16)
                print(f"\n⊱ Input, BIN:  {n}\n⊱ Output, OCT: {res_o}\n⊱ Output, HEX: {res_h}\n")
            # Oct -> Bin + Hex
            case "5":
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, 8):
                        break
                    print(f"Please input a valid octal number.")
                res_b = cross_convert(n, 8, 2)
                res_h = cross_convert(n, 8, 16)
                print(f"\n⊱ Input, OCT:  {n}\n⊱ Output, BIN: {res_b}\n⊱ Output, HEX: {res_h}\n")
            # Hex -> Bin + Oct
            case "6":
                while True:
                    n = input("> Number: ").strip().upper()
                    if n := cleanup_num(n, 16):
                        break
                    print(f"Please input a valid hexadecimal number.")
                res_b = cross_convert(n, 16, 2)
                res_o = cross_convert(n, 16, 8)
                print(f"\n⊱ Input, HEX:  {n}\n⊱ Output, BIN: {res_b}\n⊱ Output, OCT: {res_o}\n")
            # Quit
            case "0":
                print("\nThank you. See you another galaxy away!\n")
                progress = False
            # Quit but wrong letter
            case "O":
                print("\nInvalid command. Did you mean to quit? Input zero [0].")
            case "DEEZ NUTS" | "DEEZ NUTZ":
                print("\nDEEEEEEEEEEEEEEEEEZZZZZZZZZZZZZZZZZ NUTZZ\nThis is just an easter egg hidden in the corners of the galaxy.\n")
            case _:
                print("\nInvalid command. Try inputting [1] to [5].")


if __name__ == "__main__":
    main()