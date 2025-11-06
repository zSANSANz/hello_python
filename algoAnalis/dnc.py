def binary_search(arr, target, left, right):
    if left > right:
        return -1  # elemen tidak ditemukan

    mid = (left + right) // 2  # bagi dua (Divide)

    if arr[mid] == target:  # ditemukan (Conquer)
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)  # cari di kiri
    else:
        return binary_search(arr, target, mid + 1, right)  # cari di kanan

# Contoh penggunaan
data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23

hasil = binary_search(data, target, 0, len(data) - 1)
if hasil != -1:
    print(f"Elemen {target} ditemukan pada indeks {hasil}")
else:
    print("Elemen tidak ditemukan")
