import csv

# Maximum and minimim allowed microwave frequency
MaxFrequency = 40.5
MinFrequency = 12.5

with open('dataset.csv'.'r') as file:
    dataset = list(csv.reader(file))

    feature_arr = dataset[0]
    data_arr = []

    for row_num in range(2, len(dataset)):
        data_arr.append(dataset[row_num])

    # check whether the frequency is in the given range
    freq_index = feature_arr.index("Frequency")
    for row in range(0, len(data_arr)):
        selected_link_frequency = data_arr[row][freq_index]
        if not (MinFrequency <= float(selected_link_frequency) <= MaxFrequency):
            del data_arr[row]
            continue

arr = feature_arr + data_arr

with open('filtered_dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(arr)
