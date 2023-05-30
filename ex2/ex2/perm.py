from typing import TypeGuard


def perm_mutate_inversion(perm: tuple[int], i: int, j: int) -> tuple[int]:
    assert i != j
    if i < j:
        l, m, r = perm[:i], perm[i : j + 1], perm[j + 1 :]
        tmp = m[::-1]
        res = l + tmp + r
    else:
        l, m, r = perm[: j + 1], perm[j + 1 : i], perm[i:]
        tmp = (r + l)[::-1]
        res = tmp[len(r) :] + m + tmp[: len(r)]
    assert len(res) == len(perm), (perm, i, j)
    return res


def perm_crossover_pmx(p0: tuple[int], p1: tuple[int], i: int, j: int) -> tuple[int]:
    assert i != j
    i, j = min(i, j), max(i, j)
    pc = i * (None,) + p0[i : j + 1] + ((len(p0) - j - 1) * (None,))
    uncopied = p1[i : j + 1]
    # print(f"uncopied: {uncopied}")
    for l, item in enumerate(uncopied):
        # print(pc)
        # print(f"placing {item}")
        if item in pc:
            # print(f"    already exists")
            continue
        newpos = p1.index(p0[l + i])
        # print(f"    attempting pos {newpos}")
        while pc[newpos] is not None:
            # print(f"    already occupied by {pc[newpos]}")
            newpos = p1.index(pc[newpos])
            # print(f"    attempting + pos {newpos}")
        assert pc[newpos] is None
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
