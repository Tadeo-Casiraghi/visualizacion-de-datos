import matplotlib.pyplot as plt


def custom_scale(value):
    return 1 - 1/(value + 1)
    
x = [val/100 for val in range(101)] + [val for val in range(50, 101)]
y = [custom_scale(value) for value in x]

plt.plot(x, y)
plt.xlabel('Original value')
plt.ylabel('Transformed value')
plt.title('Custom scaling function')
plt.show()