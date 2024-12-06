class HimpunanTeam6:
    def _init_(self, *args):
        """Membuat objek HimpunanTeam6 baru dengan elemen unik."""
        self.data = list(set(args))  # Hindari elemen duplikat

    def _repr_(self):
        """Mengembalikan representasi string dari HimpunanTeam6."""
        return f"{{{', '.join(map(str, sorted(self.data)))}}}"  # Output terurut untuk konsistensi

    def _len_(self):
        """Mengembalikan jumlah elemen dalam HimpunanTeam6."""
        return len(self.data)

    def _contains_(self, item):
        """Memeriksa apakah item ada di dalam HimpunanTeam6."""
        return item in self.data

    def _eq_(self, other):
        """Memeriksa apakah dua HimpunanTeam6 sama."""
        return set(self.data) == set(other.data)

    def _le_(self, other):
        """Memeriksa apakah HimpunanTeam6 ini adalah subset dari HimpunanTeam6 lain."""
        return set(self.data).issubset(set(other.data))

    def _lt_(self, other):
        """Memeriksa apakah HimpunanTeam6 ini adalah proper subset dari HimpunanTeam6 lain."""
        return set(self.data) < set(other.data)

    def _ge_(self, other):
        """Memeriksa apakah HimpunanTeam6 ini adalah superset dari HimpunanTeam6 lain."""
        return set(self.data).issuperset(set(other.data))

    def _floordiv_(self, other):
        """Memeriksa apakah dua HimpunanTeam6 ekuivalen."""
        return set(self.data) == set(other.data)

    def _add_(self, other):
        """Menggabungkan dua HimpunanTeam6."""
        return HimpunanTeam6(*(set(self.data) | set(other.data)))

    def _sub_(self, other):
        """Menghitung selisih antara dua HimpunanTeam6."""
        return HimpunanTeam6(*(set(self.data) - set(other.data)))

    def _truediv_(self, other):
        """Menghitung irisan antara dua HimpunanTeam6."""
        return HimpunanTeam6(*(set(self.data) & set(other.data)))

    def _mul_(self, other):
        """Menghitung selisih simetris antara dua HimpunanTeam6."""
        return HimpunanTeam6(*(set(self.data) ^ set(other.data)))

    def _pow_(self, other):
        """Menghitung hasil Cartesian Product antara dua HimpunanTeam6."""
        return HimpunanTeam6(*[(x, y) for x in self.data for y in other.data])

    def _abs_(self):
        """Menghitung jumlah subset (himpunan kuasa)."""
        return 2 ** len(self.data)

    def ListKuasa(self):
        """Menghasilkan daftar semua subset dari HimpunanTeam6."""
        from itertools import chain, combinations
        subsets = chain.from_iterable(combinations(self.data, r) for r in range(len(self.data) + 1))
        return [set(subset) for subset in subsets]

    def Komplemen(self, universal):
        """Menghitung komplemen dari HimpunanTeam6 terhadap himpunan semesta."""
        return HimpunanTeam6(*(set(universal.data) - set(self.data)))

    def add(self, item):
        """Menambahkan elemen ke dalam HimpunanTeam6."""
        if item not in self.data:
            self.data.append(item)

    def remove(self, item):
        """Menghapus elemen dari HimpunanTeam6."""
        if item in self.data:
            self.data.remove(item)


# Contoh penggunaan kelas Himpunan
S = HimpunanTeam6(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)  # Himpunan semesta
h1 = HimpunanTeam6(1, 2, 3)  # Himpunan pertama
h2 = HimpunanTeam6(3, 4, 5)  # Himpunan kedua

# Menampilkan jumlah elemen dalam h1
print(len(h1))  # Output: 4

# Memeriksa apakah elemen ada di h1
print(3 in h1)  # Output: True

# Memeriksa apakah h1 dan h2 sama
print(h1 == h2)  # Output: False

# Menambahkan elemen ke h1
h1.add(4)
print(h1)  # Output: {1, 2, 3, 4}

# Irisan antara h1 dan h2
h3 = h1 / h2
print(h3)  # Output: {3, 4}

# Gabungan antara h1 dan h2
h4 = h1 + h2
print(h4)  # Output: {1, 2, 3, 4, 5}

# Selisih antara h1 dan h2
h5 = h1 - h2
print(h5)  # Output: {1, 2}

# Komplemen dari h1 terhadap S
h6 = h1.Komplemen(S)
print(h6)  # Output: {5, 6, 7, 8, 9, 10}

# Jumlah subset (himpunan kuasa) dari h1
print(abs(h1))  # Output: 16 (2^4 subset)

# Menampilkan semua subset dari h1
print(h1.ListKuasa())