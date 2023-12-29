import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from consts import corp_name, ratio_name, yaxis_not_percentage
from cal_ratio import cal_ratio
import os
from matplotlib.font_manager import FontProperties

if __name__ == '__main__':
    data = pd.read_excel('data.xlsx', sheet_name=None)
    font = FontProperties(fname=r"/Users/huing/Library/Fonts/SimHei.ttf", size=14)
    if not os.path.exists('output'):
        os.mkdir('output')
        
    for ratio_type, ratio_list in ratio_name.items():
        for ratio_name in ratio_list:
            # draw a bar chart for each ratio, all companies
            # 3 companies, 3 bars each year, 6 years
            # y axi use percentage 
            fig, ax = plt.subplots()
            ax.set_ylabel('Ratio')
            ax.set_title(ratio_name)
            ax.set_xticks(np.arange(6))
            ax.set_xticklabels(('2017', '2018', '2019', '2020', '2021', '2022'))
            if ratio_name not in yaxis_not_percentage:
                ax.yaxis.set_major_formatter('{x:.2%}')

            for idx, (corp_code, sheet) in enumerate(data.items()):
                corp_code = corp_code.split('-')[0]
                corp = corp_name[corp_code]
                ratios = cal_ratio(ratio_name, sheet)
                # Adjust the bar position for each company
                plt.bar(np.arange(6) -0.2 + 0.2 * idx, ratios, width=0.2, label=corp)
                # Add text on each bar
                for i in range(6):
                    if ratio_name in yaxis_not_percentage:
                        plt.text(i - 0.2 + 0.2 * idx, ratios[i], f'{ratios[i]:.2f}', ha='center', va='bottom', fontsize=3)
                    else:
                        plt.text(i - 0.2 + 0.2 * idx, ratios[i], f'{ratios[i]:.2%}', ha='center', va='bottom', fontsize=3)
            ax.legend(fontsize=5, prop=font)
            if not os.path.exists(f'output/{ratio_type}'):
                os.mkdir(f'output/{ratio_type}')
            # change dpi to get a better resolution
            plt.savefig(f'output/{ratio_type}/{ratio_name}.png', dpi=300)
