import numpy as np
import matplotlib.pyplot as plt

heights_path = "report/deformation2_cm.csv"     # load spring heights in cm
forces_path = "report/fsr_data_N.csv"           # load forces in N

height_data = np.genfromtxt(heights_path, delimiter=',')
forces_data = np.genfromtxt(forces_path, delimiter=',')

deformation_data = 3.2 - height_data
deformation_data = deformation_data / 100       # convert to m

# Perform linear regression to find the line of best fit
coefficients = np.polyfit(deformation_data, forces_data, 1)
slope, intercept = coefficients

# Generate the line of best fit
line_of_best_fit = np.poly1d(coefficients)

# Plot the original data, best-fit curve, and interpolated data
plt.scatter(deformation_data, forces_data, label='Force vs Deformation', marker='x', color='blue')
plt.plot(deformation_data, line_of_best_fit(deformation_data), label=f'Line of Best Fit: y = {slope:.2f}x + {intercept:.2f}', color='red')

plt.xlabel('Force (N)')
plt.ylabel('Spring Deformation (m)')
plt.legend()
plt.title('Best-Fit Line for Spring Stiffness Measurements')
plt.show()
