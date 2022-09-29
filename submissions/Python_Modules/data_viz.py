#Reads queries and creates dataframes from results of querying the database
#Plots are created from datframes and stored in PDF

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def plot_heatmap(query: str, db: object):
    #Query databse and save in dataframe
    df = db.query_to_df(query)
    f, ax = plt.subplots(figsize=(7, 7))
    #Use dataframe for correlation heatmap
    sns.heatmap(df.select_dtypes(['number']).corr(), annot=True, cmap='magma')
    f.suptitle('Correlation Heatmap of Audio Features', fontsize=18, fontweight='bold')
    plt.xticks(rotation=45, fontsize='5.5')
    plt.yticks(fontsize='5.5')
    return f


def plot_violin(query: str, db: object):
    df = db.query_to_df(query)
    #Divide follower column into 5 quantiles and plot on violin graph
    df['follower_qnt'], cut_bin = pd.qcut(df['followers'], q=5, labels=['Q1','Q2','Q3','Q4','Q5'], retbins=True)
    f, ax = plt.subplots(figsize=(8, 8))
    # Show each distribution with both violins and points
    sns.violinplot(x="follower_qnt", y='energy', data=df, inner="box", palette="flare", cut=2, linewidth=3)
    #Adjust graph settings
    sns.despine(left=True)
    f.suptitle('Song Energy by Follower Quantile', fontsize=18, fontweight='bold')
    ax.set_xlabel("Follower Quantiles", size=16, alpha=0.7)
    ax.set_ylabel("Energy", size=16, alpha=0.7)
    return f



def plot_box(query: str, db: object):
    #Query database and store in dataframe
    #Then uses dataframe for boxplot
    df = db.query_to_df(query)
    f, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=df, x='genre', y='danceability',palette='flare')

    #Adjust graph setting
    f.suptitle('Song Danceability Distirbution by Genre', fontsize=18, fontweight='bold')
    ax.set_xlabel("Genres",size = 10,alpha=0.7)
    ax.set_ylabel("Danceability",size = 16,alpha=0.7)
    label=df['genre'].unique().tolist()
    x = np.arange(len(label))
    plt.xticks(ticks=x, labels=label, rotation=50, fontsize='7.5')
    return f

def save_plots(query_1: str, query_2: str, query_3: str, db: object):
    #Create figures for each plot and then save all figures to pdf
    fig_heat = plot_heatmap(query_1, db)
    fig_bow = plot_box(query_2, db)
    fig_violin = plot_violin(query_3, db)

    import matplotlib.backends.backend_pdf
    pdf = matplotlib.backends.backend_pdf.PdfPages("./visualization.pdf")
    for fig in range(1, plt.gcf().number + 1):
        pdf.savefig(fig)
    pdf.close()
    return [fig_heat, fig_bow, fig_violin]
