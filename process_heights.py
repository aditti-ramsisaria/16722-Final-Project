import numpy as np
import matplotlib.pyplot as plt

def find_line_equation(point1, point2):
    """
    Find the equation of a line given two data points in the form: y = mx + b.

    Parameters:
    - point1 (tuple or list): The first data point (x1, y1).
    - point2 (tuple or list): The second data point (x2, y2).

    Returns:
    - tuple: A tuple (slope, y-intercept) representing the equation of the line.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the slope (m)
    slope = (y2 - y1) / (x2 - x1)

    # Calculate the y-intercept (b) using one of the data points
    intercept = y1 - slope * x1

    return slope, intercept

def interpolate_new_point(new_x, line_equation):
    """
    Interpolate a new data point on the line given its x-coordinate.

    Parameters:
    - new_x (float): The x-coordinate of the new data point.
    - line_equation (tuple): The line equation in the form (slope, y-intercept).

    Returns:
    - float: The y-coordinate of the interpolated point.
    """
    slope, intercept = line_equation
    new_y = slope * new_x + intercept
    return new_y

def linear_interpolation(point1, point2, num_points=20):
    """
    Linearly interpolate between two points to create a vector of specified length.

    Parameters:
    - point1 (tuple or list): The first data point (x, y).
    - point2 (tuple or list): The second data point (x, y).
    - num_points (int): The length of the resulting vector.

    Returns:
    - numpy.ndarray: A 1D array representing the linearly interpolated vector.
    """
    x_values = np.linspace(point1[0], point2[0], num_points)
    y_values = np.linspace(point1[1], point2[1], num_points)
    interpolated_vector = np.column_stack((x_values, y_values))
    return interpolated_vector


csv_file_path = 'report/deformation2.csv'
data = np.genfromtxt(csv_file_path, delimiter=',')

point1 = (369, 3.2)
point2 = (226, 1.8)
slope, intercept = find_line_equation(point1, point2)

height_cm = []

for pixel_value in data:
    height = interpolate_new_point(pixel_value, (slope, intercept))
    height_cm.append([height])
    print(height)

# # Example usage:
# point1 = (3.2, 369)
# point2 = (1.8, 226)

# result = linear_interpolation(point1, point2, num_points=20)
# pixel_values = result[:, 1]

file_path = "report/deformation2_cm.csv"

# # Save with headers
np.savetxt(file_path, height_cm, delimiter=',', comments='')

# Plot the original data, best-fit curve, and interpolated data
plt.scatter(data, height_cm, label='Interpolated Deformation Data', marker='x', color='blue')

plt.xlabel('Spring Height (px)')
plt.ylabel('Spring Height (cm)')
plt.legend()
plt.title('Best-Fit Line and Interpolated Data for Deformation Measurements')
plt.show()
