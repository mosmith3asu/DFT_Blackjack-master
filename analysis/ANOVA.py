import numpy as np
# import matplotlib.pyplot as plt
from data.data_utils import import_data
from analysis.DFT import DecisionFieldTheory
import pandas
import statsmodels.api as sm
from statsmodels.formula.api import ols


def ANOVA_response_time(data, caption = 'ANOVA: Observed Response Time'):
    # Perform ANOVA on Prediction Accuracy
    data = data.replace('y', 1).replace('n', 0)
    model = ols("""ResponseTime ~ C(PlayerHand) + C(DealerHand) + C(TimePressure) +
                     C(PlayerHand):C(DealerHand) + C(PlayerHand):C(TimePressure) + C(DealerHand):C(TimePressure) +
                     C(PlayerHand):C(DealerHand):C(TimePressure)""", data=data).fit()
    ANOVA = sm.stats.anova_lm(model, typ=2)
    print(f'\n\n ######### ANOVA: Response Time ##########')
    print(ANOVA.to_latex(na_rep='-', caption=caption, formatters={"name": str.upper}, float_format="{:.2f}".format))


def ANOVA_choice_probability(data, caption = 'ANOVA: Observed Choice Probability'):
     # Perform ANOVA on Prediction Accuracy
    data = data.replace('y',1).replace('n',0)
    model = ols("""Response ~ C(PlayerHand) + C(DealerHand) + C(TimePressure) +
                      C(PlayerHand):C(DealerHand) + C(PlayerHand):C(TimePressure) + C(DealerHand):C(TimePressure) +
                      C(PlayerHand):C(DealerHand):C(TimePressure)""", data=data).fit()
    ANOVA = sm.stats.anova_lm(model, typ=2)
    print(f'\n\n ######### ANOVA: Choice Probability ##########')
    print(ANOVA.to_latex(na_rep='-',caption=caption,formatters={"name": str.upper}, float_format="{:.2f}".format))

def ANOVA_accuracy(data, caption = 'ANOVA: DFT Choice Probability Accuracy (MSE)'):
    # Fit DFT -----------------------------
    DFT = DecisionFieldTheory()
    DFT.fit(data)

    # Calc MSE for each sample ---------------------
    data.insert(data.shape[1], "MSE", np.zeros(data.shape[0]), True)
    for index, row in data.iterrows():
        # Get sample condition
        i = ['Low', 'Med', 'High', 'Most'].index(row['PlayerHand'])
        j = ['Low', 'Med', 'High'].index(row['DealerHand'])
        k = ['Low', 'Med', 'High'].index(row['TimePressure'])

        # Get observed and predicted responses
        PrG_pred, RT = DFT.predict(i, j, k)
        PrG_obs = ['n', 'y'].index(row['Response'])
        MSE = (PrG_obs - PrG_pred) ** 2
        data.loc[index, 'MSE'] = MSE

    # Perform ANOVA on Prediction Accuracy
    model = ols("""MSE ~ C(PlayerHand) + C(DealerHand) + C(TimePressure) +
                      C(PlayerHand):C(DealerHand) + C(PlayerHand):C(TimePressure) + C(DealerHand):C(TimePressure) +
                      C(PlayerHand):C(DealerHand):C(TimePressure)""", data=data).fit()
    ANOVA = sm.stats.anova_lm(model, typ=2)

    # Format and print table
    print(f'\n\n ######### ANOVA: Accuracy ##########')
    print(ANOVA.to_latex(na_rep='-',caption=caption,formatters={"name": str.upper}, float_format="{:.2f}".format))
def main():
    # Load Data
    data = import_data()
    # print(data)
    ANOVA_choice_probability(data)
    ANOVA_response_time(data)
    ANOVA_accuracy(data)








    # print(ANOVA)
def subfun():
    pass


if __name__ == "__main__":
    main()
