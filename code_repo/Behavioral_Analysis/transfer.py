def transfer(array):
    for data in array:
        data.append(data.copy()[1])
    return array

if __name__ == '__main__':
    print(transfer([[3923,3958],[3959,4019],[4020,4095]]))