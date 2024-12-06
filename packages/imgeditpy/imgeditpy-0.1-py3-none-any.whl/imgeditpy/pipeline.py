from functools import reduce


def compose(f, g):
    return lambda x: f(g(x))


def pipeline(image, *args):
    return reduce(compose, args)(image)
