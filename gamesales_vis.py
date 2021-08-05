import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# QUESTIONS TO ANSWER:
# 1. Average review scores by publisher
# 2. Sales by genre and/or platform
# 3. Sales vs. critic score for each title

DATAFILE = 'vgchartz-6_23_2020.csv'
plt.rcParams.update({'font.size': 7})


class Vis:
    # 1 Parameter:  filename (as csv)
    # Reads CSV into dataframe, stored in object
    def __init__(self, dataset):
        self.df = pd.read_csv(dataset).drop(columns=["Unnamed: 0", "img"])
    # Creates a barchart that contains average critic score by publisher for publishers with number of titles >= thresh
    # Also creates a "bubble chart" that shows critic scores by publisher where bubble size is number of titles >= thresh

    def query1(self, thresh=0):
        # AVERAGE CRITIC SCORE BY PUBLISHER (BAR)
        count = self.df[["publisher", "critic_score", "user_score"]].\
            groupby(["publisher"], as_index=False).\
            size()
        average = self.df[["publisher", "critic_score"]].\
            groupby(["publisher"], as_index=False).\
            mean().\
            dropna()
        query1 = pd.merge(average, count, how='left', on="publisher")
        query1_filtered = query1[query1["size"] > thresh].reset_index().drop(columns="index")
        ax1 = sns.barplot(x="publisher", y="critic_score", data=query1_filtered.head(20), palette="bright")
        for bar in ax1.patches:
            ax1.annotate(format(bar.get_height(), '.2f'),\
                (bar.get_x() + bar.get_width() / 2,bar.get_height()),\
                ha='center',\
                va='center',\
                size=11,\
                xytext=(0, 8),\
                textcoords='offset points')
        plt.xticks(rotation=45)
        plt.yticks(range(0, 11))
        ax1.set(xlabel="Publisher", ylabel="Average Critic Score", title="Average Critic Score by Publisher")
        plt.title(f"Critic Scores by Publisher (>={thresh} titles)")
        plt.tight_layout()
        plt.show(block=True)

        # AVERAGE CRITIC SCORE BY PUBLISHER (BUBBLE)
        ax2 = sns.scatterplot(x="publisher", y="size", size="critic_score", data=query1_filtered.head(20), sizes=(50, 500), hue="critic_score")
        plt.xticks(rotation=45)
        plt.title(f"Critic Scores by Publisher (>={thresh} titles)")
        plt.tight_layout()
        plt.show(block=True)

    # Creates a list of months-years in the format: YYYY-mm. I'm sure theres some library that does this.. 
    # Returns a list to use as tick labels
    def __createTimeRange(self, startDate, endDate):
        startYear, startMonth   = startDate.split('-')
        endYear, endMonth       = endDate.split('-')
        ii = int(startMonth)
        ticks                   = []
        #return [f"{str(i)}-{str(ii % 13)}" 
        for i in range(int(startYear), int(endYear)+1):
            while ii <= 12:
                if f"{str(i)}-{str(ii)}" == endDate:
                    ticks.append(endDate)
                    return ticks
                ticks.append(f"{str(i)}-{str(ii)}")
                ii += 1
            ii = 1
        return ticks

    # Creates a piechart that contains total sales for each genre where the total sales are >= thresh. For values under 52, the graph looks bad because the text is smashed together,
    # one way to handle this is to use a legend but because there are so many slices to the pie, including a legend adds to cognitive load. Recommended thresh=50
    # ALSO creates a line graph of sales by platform over time. Shows one of the pitfalls to using sns/plt/pd-- theres no good way to connect non-adjacent data points.
    def query2(self, thresh=0, startDate="1970-01", endDate="2100-01"):
        # SALES BY GENRE (PIE)
        sales = self.df[["genre", "total_sales"]].\
            dropna().groupby(["genre"], as_index=False).\
            sum().\
            sort_values("total_sales")
        filtered_sales = sales[sales["total_sales"] >= thresh]
        sum = filtered_sales.sum()["total_sales"]
        fracs = [(float(i)/sum) *100 for i in filtered_sales["total_sales"].to_list()]
        plt.pie(fracs, labels=filtered_sales["genre"].to_list(), radius=1, labeldistance=1.05, autopct='%1.1f%%')
        plt.title(f"Sales by Genre (>={thresh} sales in millions)")
        plt.tight_layout()
        plt.show(block=True)

        # SALES BY MONTH PER PLATFORM (LINE)
        sales_by_month  = self.df[["total_sales", "console", "release_date"]].dropna(how="any")
        sales_by_month["release_date"] = pd.to_datetime(sales_by_month["release_date"], format="%Y-%m", errors="coerce")
        filter_months   = sales_by_month.set_index("release_date").loc[startDate:endDate].to_period("M")
        sales_data      = filter_months.groupby([pd.Grouper(freq="M"), "console"]).sum().reset_index()
        sns.catplot(x="release_date", y="total_sales", hue="console", kind="point", data=sales_data)
        #labels          = self.__createTimeRange(startDate, endDate)
        plt.xticks(rotation=45)#, ticks=np.arange(len(labels)), labels=labels)
        plt.title(f"Sales by Console between {startDate} and {endDate}")
        plt.tight_layout()
        plt.show(block=True)

        # SALES BY MONTH PER GENRE (LINE) - copy and pasted
        sales_by_month  = self.df[["total_sales", "genre", "release_date"]].dropna(how="any")
        sales_by_month["release_date"] = pd.to_datetime(sales_by_month["release_date"], format="%Y-%m", errors="coerce")
        filter_months   = sales_by_month.set_index("release_date").loc[startDate:endDate].to_period("M")
        sales_data      = filter_months.groupby([pd.Grouper(freq="M"), "genre"]).sum().reset_index()
        sns.catplot(x="release_date", y="total_sales", hue="genre", data=sales_data)
        plt.xticks(rotation=45)
        plt.title(f"Sales by Genre between {startDate} and {endDate}")
        plt.tight_layout()
        plt.show(block=True)

if __name__ == "__main__":
    #Vis(DATAFILE).query1(thresh=200)
    Vis(DATAFILE).query2(thresh=50, startDate='1970-01', endDate='1990-01')
