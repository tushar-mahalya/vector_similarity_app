import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def MakeContColPlots(original_df, imputed_df=None):
    """
    Generate distribution plots for continuous columns in the original dataset and, if provided, the imputed dataset.

    Parameters:
    - original_df (pd.DataFrame): Original dataset.
    - imputed_df (pd.DataFrame, optional): Imputed dataset. Default is None.

    Returns:
    - Displayed distribution plots.
    """
    grid_specs = {'visible': True, 'which': 'both', 'linestyle': '--',
                  'color': 'lightgrey', 'linewidth': 0.75}
    title_specs = {'fontsize': 9, 'fontweight': 'bold', 'color': '#992600'}

    cont_cols = original_df.select_dtypes(include=[np.number]).columns.tolist()

    if imputed_df is not None:
        df = pd.concat([original_df[cont_cols].assign(Source='Original'),
                        imputed_df[cont_cols].assign(Source='Imputed')],
                       axis=0, ignore_index=True)
        col_palette = ['#0039e6', '#ff5500']
        num_cols = 3
    else:
        df = original_df[cont_cols].assign(Source='Original')
        col_palette = ['#0039e6']
        num_cols = 2

    fig, axes = plt.subplots(len(cont_cols), num_cols, figsize=(16, len(cont_cols) * 4.2),
                             gridspec_kw={'hspace': 0.35 if num_cols == 3 else 0.45,
                                          'wspace': 0.3,
                                          'width_ratios': [0.80, 0.20, 0.20] if num_cols == 3 else [0.80, 0.20]}
                             )

    for i, col in enumerate(cont_cols):
        ax = axes[i, 0]
        sns.kdeplot(data=df[[col, 'Source']], x=col, hue='Source',
                    palette=col_palette,
                    ax=ax, linewidth=2.1)
        ax.set_title(f"\n{col}", **title_specs)
        ax.grid(**grid_specs)
        ax.set(xlabel='', ylabel='')

        ax = axes[i, 1]
        sns.boxplot(data=df.loc[df.Source == 'Original', [col]], y=col, width=0.25,
                    color='#0039e6', saturation=0.90, linewidth=0.90,
                    fliersize=2.25,
                    ax=ax)
        ax.set(xlabel='', ylabel='')
        ax.set_title("Original", **title_specs)

        if imputed_df is not None:
            ax = axes[i, 2]
            sns.boxplot(data=df.loc[df.Source == 'Imputed', [col]], y=col, width=0.25, fliersize=2.25,
                        color='#ff5500', saturation=0.6, linewidth=0.90,
                        ax=ax)
            ax.set(xlabel='', ylabel='')
            ax.set_title("Imputed", **title_specs)

    plt.suptitle(f"Distribution Analysis\n", fontsize=20, fontweight='bold', y=0.89, x=0.50)
    plt.tight_layout()
    plt.show()