from datetime import datetime

start = datetime.now()

#for i in range(10):
    #print("Iteration:", i)
for i in range(10):
    print(f"Iteration: {i}, Square: {i**2}")

end = datetime.now()

difference = end - start

print("Execution time:", difference)