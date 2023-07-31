def find_nearest_number(list_of_lists, x):
    # 将所有列表中的元素展平成一个列表
    flattened_list = [num for sublist in list_of_lists for num in sublist]

    # 按与 x 的距离对列表中的元素进行排序
    flattened_list.sort(key=lambda num: abs(num - x))

    # 返回距离 x 最近的数
    return flattened_list[0]
