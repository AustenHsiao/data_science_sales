import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# QUESTIONS TO ANSWER:
# 1. Average review scores by publisher
# 2. Sales by genre
# 3. User scores by platform-- will be changed

DATAFILE = 'vgchartz-6_23_2020.csv'
plt.rcParams.update({'font.size': 7})

class Vis:
    # 1 Parameter:  filename (as csv)
    # Reads CSV into dataframe, stored in object
    def __init__(self, dataset):
        self.df = pd.read_csv(dataset).drop(columns=["Unnamed: 0", "img"])

    # Creates a barchart that contains average critic score by publisher for publishers with number of titles >= thresh
    def query1(self, thresh=0):
        count               = self.df[["publisher", "critic_score", "user_score"]].\
                              groupby(["publisher"], as_index=False).\
                              size()
        average             = self.df[["publisher", "critic_score"]].\
                              groupby(["publisher"], as_index=False).\
                              mean().\
                              dropna()
        query1              = pd.merge(average, count, how='left', on="publisher")
        query1_filtered     = query1[query1["size"] > thresh].reset_index().drop(columns="index")
        ax1                 = sns.barplot(x="publisher", y="critic_score",
                              data=query1_filtered.head(20), palette="bright")
        for bar in ax1.patches:
            ax1.annotate(format(bar.get_height(), '.2f'),
            (bar.get_x() + bar.get_width() / 2,
            bar.get_height()), ha='center', va='center',
            size=11, xytext=(0, 8),
            textcoords='offset points')
        plt.xticks(rotation=45)
        plt.yticks(range(0, 11))
        ax1.set(xlabel="Publisher", ylabel="Average Critic Score", title="Average Critic Score by Publisher")
        plt.title("Critic Scores by Publisher")
        plt.tight_layout()
        plt.show(block=True)
        ax2                 = sns.scatterplot(x="publisher", y="size", size="critic_score", data=query1_filtered.head(20), sizes=(50, 200), hue="critic_score")
        plt.xticks(rotation=45)
        plt.title("Critic Scores by Publisher")
        plt.tight_layout()
        plt.show(block=True)
        
    # Creates a piechart that contains total sales for each genre where the total sales are >= thresh. For values under 52, the graph looks bad because the text is smashed together,
    # one way to handle this is to use a legend but because there are so many slices to the pie, including a legend adds to cognitive load. Recommended thresh=50
    def query2(self, thresh=0):
        sales = self.df[["genre", "total_sales"]].dropna().groupby(["genre"], as_index=False).sum().sort_values("total_sales")
        plt.pie(x="total_sales", labels="genre", radius=1, labeldistance=1.05, data=sales[sales["total_sales"] >= thresh])
        plt.title("Sales by Genre")
        plt.tight_layout()
        plt.show(block=True)

if __name__ == "__main__":
    Vis(DATAFILE).query1(thresh=200)
    Vis(DATAFILE).query2(thresh=50)
