# import numpy as np

# def remove_identical_successive_elements(input_array):
#     input_array = input_array.tolist()
#     result_array = []
#     previous_element = None

#     for element in input_array:
#         if element != previous_element:
#             result_array.append(element)
#         previous_element = element

#     result_array = np.array(result_array)
#     return result_array

# # Example usage:
# input_array = np.array([0, 1, 3, 3])
# output_array = remove_identical_successive_elements(input_array)
# print(input_array)
# print(output_array)  # Output: [0 1 3]

# import numpy as np

# def add_noise_to_array(arr, noise_level=0.01):
#     """
#     Add random noise to all elements of a NumPy array.

#     Parameters:
#     - arr: NumPy array
#         The input array to which noise will be added.
#     - noise_level: float, optional
#         The standard deviation of the noise to be added. Default is 0.01.

#     Returns:
#     - noisy_arr: NumPy array
#         The array with noise added to each element.
#     """
#     noise = np.random.normal(0, noise_level, arr.shape)
#     noisy_arr = arr + noise
#     return noisy_arr

# # Example usage:
# original_array = np.array([1, 2, 3, 4])
# noisy_array = add_noise_to_array(original_array, noise_level=0.1)
# print("Original array:", original_array)
# print("Noisy array:", noisy_array)

from tft_bot.helpers.click_helpers import move_to

move_to(100.2, 300.2)
