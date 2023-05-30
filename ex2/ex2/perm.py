from typing import TypeGuard


def perm_mutate_inversion(perm: tuple[int], i: int, j: int) -> tuple[int]:
    assert i != j
    if i < j:
        return perm[:i] + perm[i + 1 : j : -1] + perm[j + 1 :]
    else:
        tmp = (perm[i + 1 :] + perm[:j])[::-1]
        return tmp[:j] + perm[j + 1 : i] + tmp[j + 1 :]


def perm_crossover_pmx(p0: tuple[int], p1: tuple[int], i: int, j: int) -> tuple[int]:
    assert i != j
    i, j = min(i, j), max(i, j)
    pc = i * (None,) + p0[i:j] + ((len(p0) - j) * (None,))
    uncopied = p1[i:j]
    for l, item in enumerate(uncopied):
        if item in pc:
            continue
        newpos = p1.index(p0[l + i])
        if pc[newpos] is not None:
            newpos = p1.index(pc[newpos])
        assert pc[newpos] is not None
        pc = pc[:newpos] + (item,) + pc[newpos + 1 :]
    for item in p1:
        if item in pc:
            continue
        pos = pc.index(None)
        pc = pc[:pos] + (item,) + pc[pos + 1 :]

    def is_int_tuple(val: tuple[int | None]) -> TypeGuard[tuple[int]]:
        return all(x is not None for x in val)

    assert is_int_tuple(pc)
    return pc
