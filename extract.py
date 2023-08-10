from collections import Counter
from name import s
#s = [item.decode('utf-8') for item in s]

import matplotlib.pyplot as plt
def plot_industry_frequency(stock_list):
    
    
    frequency_counter = Counter(stock_list).most_common()
    
    # 获取元素和对应的频率
    elements, frequencies = zip(*frequency_counter[:10])

    print(elements)
    
    
    
    # 绘制频率图
    plt.bar(elements, frequencies)

    # 绘制行业频率图
    plt.title('Stock Industry Frequency')
    plt.xlabel('Industry')
    plt.ylabel('Frequency')
    plt.savefig('/Users/wanting/Desktop/1111.png')


plot_industry_frequency(s)