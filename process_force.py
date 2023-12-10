import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Hyperbolic model
def hyperbola(x, a, b, c):
    return a / (x + b) + c

# Exponential decay function
def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

# Function to find the best-fit polynomial curve
def find_best_fit(x, y, degree):
    coefficients = np.polyfit(x, y, degree)
    return np.poly1d(coefficients)

# Function to interpolate data using the best-fit curve
def interpolate_data(x, fit_curve):
    return fit_curve(x)

csv_file_path = 'report/fsr_data2.csv'
data = np.genfromtxt(csv_file_path, delimiter=',')
data = data[1 :]

x = np.array([250, 1000, 6000, 30000])
y = np.array([100, 10, 1, 0.2])

# Improved initial guess
initial_guess = (max(y), 0.1, min(y))

# Constrain parameters (optional, adjust as needed)
bounds = (0, [np.inf, np.inf, np.inf])

# Fit the exponential decay function to the data
params, covariance = curve_fit(hyperbola, x, y, p0=initial_guess, bounds=bounds)

# Extract the parameters
a, b, c = params

# Generate fitted curve
fitted_curve = hyperbola(data, a, b, c)

file_path = "report/fsr_data_N.csv"

# # Save with headers
np.savetxt(file_path, fitted_curve, delimiter=',', comments='')

# Plot the original data, best-fit curve, and interpolated data
plt.scatter(x, y, label='Ground Truth Reference Data (Adafruit)')
plt.scatter(data, fitted_curve, label='Interpolated Hyperbola Data', marker='x', color='blue')

plt.xlabel('FSR Resistance (ohms)')
plt.ylabel('Measured Force (N)')
plt.legend()
plt.title('Best-Fit Curve and Interpolated Data for Force Measurements')
plt.show()