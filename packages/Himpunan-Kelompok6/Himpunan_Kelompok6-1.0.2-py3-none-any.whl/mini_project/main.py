class HimpunanTEAM6:
    def _init_(self, *args):
        self.elements = list(set(args))

    def _repr_(self):
        return f"{{{', '.join(map(str, self.elements))}}}"

    def _len_(self):
        """Mengembalikan ukuran himpunan."""
        return len(self.elements)

    def _contains_(self, item):
        """Mengecek apakah elemen ada dalam himpunan."""
        return item in self.elements

    def _eq_(self, other):
        """Mengecek apakah dua himpunan sama."""
        return set(self.elements) == set(other.elements)

    def _le_(self, other):
        """Mengecek apakah himpunan ini subset dari himpunan lain."""
        return set(self.elements) <= set(other.elements)

    def _lt_(self, other):
        """Mengecek apakah himpunan ini proper subset dari himpunan lain."""
        return set(self.elements) < set(other.elements)

    def _ge_(self, other):
        """Mengecek apakah himpunan ini superset dari himpunan lain."""
        return set(self.elements) >= set(other.elements)

    def _floordiv_(self, other):
        """Mengecek apakah dua himpunan ekuivalen."""
        return set(self.elements) == set(other.elements)

    def _add_(self, other):
        """Menghitung gabungan dua himpunan."""
        return HimpunanTEAM6(*(self.elements + other.elements))

    def _sub_(self, other):
        """Menghitung selisih dua himpunan."""
        return HimpunanTEAM6(*(x for x in self.elements if x not in other.elements))

    def _truediv_(self, other):
        """Menghitung irisan dua himpunan."""
        return HimpunanTEAM6(*(x for x in self.elements if x in other.elements))

    def _mul_(self, other):
        """Menghitung selisih simetris dua himpunan."""
        return HimpunanTEAM6(*((set(self.elements) ^ set(other.elements))))

    def _pow_(self, other):
        """Menghitung hasil perkalian kartesian dua himpunan."""
        return HimpunanTEAM6(*((x, y) for x in self.elements for y in other.elements))

    def _abs_(self):
        """Menghitung himpunan kuasa."""
        from itertools import chain, combinations

        def power_set(iterable):
            """Menghasilkan semua subset dari himpunan."""
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        return HimpunanTEAM6(*power_set(self.elements))

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
        return HimpunanTEAM6(*(x for x in universal_set.elements if x not in self.elements))

    def _iadd_(self, item):
        """Menambah elemen ke dalam himpunan."""
        if item not in self.elements:
            self.elements.append(item)
        return self

    def _isub_(self, item):
        """Menghapus elemen dari himpunan."""
        if item in self.elements:
            self.elements.remove(item)
        return self


# Contoh penggunaan
S = HimpunanTEAM6(1, 2, 3, 4, 5, 6, 7, 8, 9)
h1 = HimpunanTEAM6(1, 2, 3)
h2 = HimpunanTEAM6(3, 4, 5)

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