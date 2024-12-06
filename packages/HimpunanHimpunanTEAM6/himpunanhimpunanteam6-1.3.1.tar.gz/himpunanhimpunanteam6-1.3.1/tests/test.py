from HimpunanHimpunanTeam6 import HimpunanHimpunanTEAM6

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