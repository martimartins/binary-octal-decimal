from typing import Union, Optional


def _int_2_base(__v: int, *, base: int) -> str:
    _previus: int = int(__v)
    _total = ""

    while _previus != 0:
        _total += str(_previus % base)
        _previus = _previus // base
    return _total[::-1]


def _base10(base: int, num: str) -> int:
    r"""Este method ira calcular um base x para base 10,

    ele ira passar por todos os items da :attr:`base` revertidos *reversed*
    e ira multiplicar o valor n por 2 elevado a posição do valor.

    Parametros
    ----------
    base: :class:`int`
        Base para qual num ira ser convertido
    num: :class:`int`
        Numero que ira ser convertido para base :attr:`base`

    Exemplo
    --------

    >>> 0b 1010101
            ╒═══════════╤═══════════╤═══════════╤═══════════╤═══════════╤═══════════╤═══════════╕
            │ 1         │ 0         │ 1         │ 0         │ 1         │ 0         │ 1         │
            ╞═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
            │ (1 * 2^6) │ (0 * 2^5) │ (1 * 2^4) │ (0 * 2^3) │ (1 * 2^2) │ (0 * 2^1) │ (1 * 2^0) │
            ╘═══════════╧═══════════╧═══════════╧═══════════╧═══════════╧═══════════╧═══════════╛
    Out[1]: 85


    >>> 0o 31
            ╒═══════════╤═══════════╕
            │ 3         │ 1         │
            ╞═══════════╪═══════════╡
            │ (3 * 8^1) │ (1 * 8^0) │
            ╘═══════════╧═══════════╛
    Out[1]: 25
    """
    return sum(int(x) * (base ** p) for p, x in enumerate(reversed(num)))


def _base8(base: int, num: Union[str, int]) -> str:
    r"""Este method ira calcular um base x para base 8,

    passando por cada item do numero revertido,
    e somar x multiplicado por 2 elevado a posição na string
    
    Parametros
    ----------
    base: :class:`int`
        Base para qual num ira ser convertido
    num: :class:`int`
        Numero que ira ser convertido para base :attr:`base`
        
    Exemplos
    --------
    Base 2:
        >>> 0b 11010100
            ╒═════════════╤═════════════╤═════════════╤═════════════╤═════════════╤═════════════╤═════════════╤═════════════╕
            │ 1           │ 1           │ 0           │ 1           │ 0           │ 1           │ 0           │ 0           │
            ╞═════════════╪═════════════╪═════════════╪═════════════╪═════════════╪═════════════╪═════════════╪═════════════╡
            │ (0 * (2^0)) │ (0 * (2^1)) │ (1 * (2^2)) │ (0 * (2^3)) │ (1 * (2^4)) │ (0 * (2^5)) │ (1 * (2^6)) │ (1 * (2^7)) │
            ╘═════════════╧═════════════╧═════════════╧═════════════╧═════════════╧═════════════╧═════════════╧═════════════╛
        
        Out[1]: 0o 212

    Base 10:
        >>> 212
            ╔═════════════════╦══════════════════════╗
            ║     Divisão     ║ Resto de divisão % 8 ║
            ╠═════════════════╬══════════════════════╣
            ║ 212 / 8 = 26.5  ║           4          ║ |\
            ║ 26  / 8 = 3.25  ║           2          ║   |> Revertido
            ║ 3   / 8 = 0.375 ║           3          ║ |/
            ╚═════════════════╩══════════════════════╝ 

        Out[1]: 0o 324
    """
    if base == 10:
        return "0o" + _int_2_base(num, base=8)
    elif base == 2:
        return f"0o{sum(int(x)*(2**p) for p, x in enumerate(reversed(num[2:])))}"


def _base2(base: int, num: Union[str, int]):
    r"""Este method ira calcular um base x para base 2"""
    if base == 10:
        return "0b" + _int_2_base(num, base=2)
    elif base == 8:
        return _base2(base=10, num=_base10(base=8, num=num[2:]))


def octal(data: Union[int, str]) -> Union[int, str]:
    if data.startswith("0o"):
        return _base10(base=8, num=data[2:])

    return _base8(base=10 if data.isnumeric() else 2, num=data)


def binary(data: Union[int, str]) -> Union[int, str]:
    if data.startswith("0b"):
        return _base10(base=2, num=data[2:])

    return _base2(base=8 if data.startswith("0o") else 10, num=data)


def decimal(data: Union[int, str]) -> Optional[Union[int, str]]:
    if data.isnumeric():
        return data

    if data.startswith("0o"):
        return _base10(base=8, num=data[2:])
    elif data.startswith("0b"):
        return _base10(base=2, num=data[2:])

    return None


if __name__ == "__main__":
    num = input("Escreva um valor Decimal / Octal / Binario: ")

    if num.isnumeric() or num[:2] in ("0o", "0b"):
        try:
            decimal = str(decimal(num))
            print("decimal", decimal)
            print(f"Binary  -> {binary(decimal)}")
            print(f"Octal   -> {octal(decimal)}")
            print(f"Decimal -> {decimal}")
        except KeyError as e:
            print(f"[ERROR] Parece que esse valor é invalido.")
    else:
        print(f"[ERROR] Parece que esse valor é invalido.")
