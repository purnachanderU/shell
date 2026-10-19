def factorial(number):
    if number == 0:
        return 1
    else:
        return number * factorial(number - 1)
print(factorial(6))  # Example usage

def even(num):
    if num % 2 == 0:
        return True
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lists=list(filter(even, lst))
print(lists)

newnumbers = [1,0,2,5,6,9,10,0,5,4]
zeroslast = []
for i in newnumbers:
    if i!= 0:
        zeroslast.append(i)
for i in newnumbers:
    if i == 0:
        zeroslast.append(i)
print(zeroslast)