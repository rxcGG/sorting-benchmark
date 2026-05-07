import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sorting_algorithms import quick_sort, merge_sort
from benchmark import measure_performance

def main():
    sizes = [10000, 50000, 100000]
    data_types = ["random", "nearly_sorted"]
    algos = {"quick sort": quick_sort, "merge sort": merge_sort}
    all_results = []

    # запуск експериментів
    for size in sizes:
        for dtype in data_types:
            for name, func in algos.items():
                res = measure_performance(func, name, size, dtype)
                all_results.extend(res)

    # збереження результатів
    df = pd.DataFrame(all_results)
    df.to_csv("experiment_results.csv", index=False)

    # візуалізація
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('аналіз продуктивності алгоритмів', fontsize=16)

    # час
    sns.lineplot(ax=axes[0,0], data=df, x='size', y='time_sec', hue='algorithm', style='type', markers=True)
    axes[0,0].set_title('залежність часу від розміру')

    # боксплот
    sns.boxplot(ax=axes[0,1], data=df[df['size']==100000], x='type', y='time_sec', hue='algorithm')
    axes[0,1].set_title('статистичний розподіл часу (100к)')

    # пам'ять
    sns.barplot(ax=axes[1,0], data=df, x='size', y='memory_mb', hue='algorithm')
    axes[1,0].set_title('використання пам\'яті')

    # гістограма для merge sort
    sns.histplot(ax=axes[1,1], data=df[df['algorithm']=='merge sort'], x='time_sec', hue='size', kde=True)
    axes[1,1].set_title('розподіл часу для merge sort')

    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300)
    print("експеримент завершено. дані та графіки збережено.")

if __name__ == "__main__":
    main()