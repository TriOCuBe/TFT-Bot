import numpy as np

def remove_identical_successive_elements(input_array):
    input_array = input_array.tolist()
    result_array = []
    previous_element = None

    for element in input_array:
        if element != previous_element:
            result_array.append(element)
        previous_element = element

    result_array = np.array(result_array)
    return result_array

# Example usage:
input_array = np.array([0, 1, 3, 3])
output_array = remove_identical_successive_elements(input_array)
print(input_array)
print(output_array)  # Output: [0 1 3]
