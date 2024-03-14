class Share:
    x = 0
class A(Share):
    def __init__(self, x) -> None:
        Share.x = x
class B(Share):
    def __init__(self) -> None:
        print(Share.x)

a = A(5)
b = B()