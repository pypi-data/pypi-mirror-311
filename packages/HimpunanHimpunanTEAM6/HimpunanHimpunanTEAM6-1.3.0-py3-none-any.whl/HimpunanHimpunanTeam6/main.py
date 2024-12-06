class HimpunanHimpunanTEAM6:
    def __init__(self, *args):
        self.elements = list(set(args))

    def __repr__(self):
        return f"{{{', '.join(map(str, self.elements))}}}"

    def __len__(self):
        """Mengembalikan ukuran himpunan."""
        return len(self.elements)

    def __contains__(self, item):
        """Mengecek apakah elemen ada dalam himpunan."""
        return item in self.elements

    def __eq__(self, other):
        """Mengecek apakah dua himpunan sama."""
        return set(self.elements) == set(other.elements)

    def __le__(self, other):
        """Mengecek apakah himpunan ini subset dari himpunan lain."""
        return set(self.elements) <= set(other.elements)

    def __lt__(self, other):
        """Mengecek apakah himpunan ini proper subset dari himpunan lain."""
        return set(self.elements) < set(other.elements)

    def __ge__(self, other):
        """Mengecek apakah himpunan ini superset dari himpunan lain."""
        return set(self.elements) >= set(other.elements)

    def __floordiv__(self, other):
        """Mengecek apakah dua himpunan ekuivalen."""
        return set(self.elements) == set(other.elements)

    def __add__(self, other):
        """Menghitung gabungan dua himpunan."""
        return HimpunanHimpunanTEAM6(*(self.elements + other.elements))

    def __sub__(self, other):
        """Menghitung selisih dua himpunan."""
        return HimpunanHimpunanTEAM6(*(x for x in self.elements if x not in other.elements))

    def __truediv__(self, other):
        """Menghitung irisan dua himpunan."""
        return HimpunanHimpunanTEAM6(*(x for x in self.elements if x in other.elements))

    def __mul__(self, other):
        """Menghitung selisih simetris dua himpunan."""
        return HimpunanHimpunanTEAM6(*((set(self.elements) ^ set(other.elements))))

    def __pow__(self, other):
        """Menghitung hasil perkalian kartesian dua himpunan."""
        return HimpunanHimpunanTEAM6(*((x, y) for x in self.elements for y in other.elements))

    def __abs__(self):
        """Menghitung himpunan kuasa."""
        from itertools import chain, combinations

        def power_set(iterable):
            """Menghasilkan semua subset dari himpunan."""
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        return HimpunanHimpunanTEAM6(*power_set(self.elements))

    def ListKuasa(self):
        """Menampilkan semua subset yang mungkin dibuat dari himpunan."""
        from itertools import chain, combinations

        def power_set(iterable):
            """Menghasilkan semua subset dari himpunan."""
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        return list(power_set(self.elements))

    def Komplemen(self, universal_set):
        """Menghitung komplemen himpunan terhadap himpunan universal."""
        return HimpunanHimpunanTEAM6(*(x for x in universal_set.elements if x not in self.elements))

    def __iadd__(self, item):
        """Menambah elemen ke dalam himpunan."""
        if item not in self.elements:
            self.elements.append(item)
        return self

    def __isub__(self, item):
        """Menghapus elemen dari himpunan."""
        if item in self.elements:
            self.elements.remove(item)
        return self


# Contoh penggunaan
S = HimpunanHimpunanTEAM6(1, 2, 3, 4, 5, 6, 7, 8, 9)
h1 = HimpunanHimpunanTEAM6(1, 2, 3)
h2 = HimpunanHimpunanTEAM6(3, 4, 5)

print(len(h1))  # Output: 3
print(3 in h1)  # Output: True
print(h1 == h2)  # Output: False

h1 += 4  # Menambah elemen 4 ke h1
print(h1)  # Output: {1, 2, 3, 4}

h3 = h1 / h2  # Irisan
print(h3)  # Output: {3, 4}

h4 = h1 + h2  # Gabungan
print(h4)  # Output: {1, 2, 3, 4, 5}

h5 = h1 - h2  # Selisih
print(h5)  # Output: {1, 2}

h6 = h1.Komplemen(S)  # Komplemen
print(h6)  # Output: {5, 6, 7, 8, 9}

print(abs(h1))  # Himpunan kuasa
print(h1.ListKuasa())  # List himpunan kuasa
