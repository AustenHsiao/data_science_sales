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
        self.df = pd.read_csv(dataset).drop(
            labels=["Unnamed: 0", "img"], axis=1)

    # Top 20 Average critic review scores by publisher
    # Displays barchart
    # If I dont do top 20 (or any smallish number), it looks like a mess
    def query1(self):
        query1  = self.df[["publisher", "critic_score", "user_score"]].\
                    groupby(["publisher"], as_index=False).\
                    mean().\
                    sort_values(by="critic_score", ascending=False).\
                    head(20)
        ax1     = sns.barplot(x="publisher", y="critic_score",
                    data=query1, palette="bright")
        for bar in ax1.patches:
                    ax1.annotate(format(bar.get_height(), '.2f'),
                         (bar.get_x() + bar.get_width() / 2,
                          bar.get_height()), ha='center', va='center',
                         size=11, xytext=(0, 8),
                         textcoords='offset points')
        plt.xticks(rotation=45)
        plt.yticks(range(0, 11))
        ax1.set(xlabel="Publisher", ylabel="Average Critic Score",
                title="Average Critic Score by Publisher")
        plt.savefig("AverageCriticScoreByPublisher.png", pad_inches=0)
        plt.show()


if __name__ == "__main__":
    Vis(DATAFILE).query1()
