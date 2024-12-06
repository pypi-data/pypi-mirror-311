class Himpunan_Team1:
    def __init__(self, *elemen):
        self.data = []
        for item in elemen:
            if item not in self.data:
                self.data.append(item)

    def __repr__(self):
        return f"Himpunan({', '.join(map(str, self.data))})"

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __eq__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return sorted(self.data) == sorted(other.data)

    def __le__(self, other):
        return all(item in other for item in self.data)

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return all(item in self for item in other)

    def __floordiv__(self, other):
        return self == other

    def __add__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*(self.data + [item for item in other.data if item not in self.data]))

    def __sub__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*[item for item in self.data if item not in other.data])

    def __truediv__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*[item for item in self.data if item in other.data])

    def __mul__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*(set(self.data).symmetric_difference(other.data)))

    def __pow__(self, other):
        if not isinstance(other, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*[(a, b) for a in self.data for b in other.data])

    def __abs__(self):
        subsets = [[]]
        for element in self.data:
            subsets += [subset + [element] for subset in subsets]
        return len(subsets)

    def ListKuasa(self):
        subsets = [[]]
        for element in self.data:
            subsets += [subset + [element] for subset in subsets]
        return [Himpunan_Team1(*subset) for subset in subsets]

    def Komplemen(self, semesta):
        if not isinstance(semesta, Himpunan_Team1):
            return NotImplemented
        return Himpunan_Team1(*[item for item in semesta.data if item not in self.data])

    def tambah(self, item):
        if item not in self.data:
            self.data.append(item)

    def hapus(self, item):
        if item in self.data:
            self.data.remove(item)