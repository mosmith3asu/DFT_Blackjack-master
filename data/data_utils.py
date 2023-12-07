import numpy as np
import matplotlib.pyplot as plt
import pandas

def load_data(fname):
    df = pandas.read_csv(fname)
    return df

def relabel_data(data):
    # print(data)
    # Remove practice
    data = data.loc[data['TimePressure'] != 10]
    N = data.shape[0]

    # Get 'TimePressure' condition
    time_constraints = data.loc[:, 'TimePressure'].to_numpy()
    time_pressure = []
    for t in time_constraints:
        if t == 5:  time_pressure.append('Low')
        elif t == 4:  time_pressure.append('Med')
        elif t == 3:  time_pressure.append('High')
    # print(np.mean(np.array(time_pressure)=='LowTP'))
    # print(np.mean(np.array(time_pressure) == 'MedTP'))
    # print(np.mean(np.array(time_pressure) == 'HighTP'))

    # Get 'PlayerHand' condition
    player_c1 = data.loc[:,'PlayerCard1'].to_numpy()
    player_c2 = data.loc[:,'PlayerCard2'].to_numpy()
    player_sum = player_c1+player_c2
    player_hand = []
    for hand_sum in player_sum:
        if   hand_sum in [12,13]: player_hand.append('Low')
        elif hand_sum in [14,15]: player_hand.append('Med')
        elif hand_sum in [16,17]: player_hand.append('High')
        elif hand_sum in [18,19]: player_hand.append('Most')
    # print(np.mean(np.array(player_hand)=='LowRisk'))
    # print(np.mean(np.array(player_hand) == 'MedRisk'))
    # print(np.mean(np.array(player_hand) == 'HighRisk'))
    # print(np.mean(np.array(player_hand) == 'MostRisk'))

    # Get 'DealerHand' condition
    dealer_c = data.loc[:, 'DealerCard'].to_numpy()
    dealer_hand = []
    for card in dealer_c:
        if   card in [2,3,4]:  dealer_hand.append('Low')
        elif card in [5,6,7]:  dealer_hand.append('Med')
        elif card in [8,9,10]: dealer_hand.append('High')
    # print(np.mean(np.array(dealer_hand)=='LowDiff'))
    # print(np.mean(np.array(dealer_hand) == 'MedDiff'))
    # print(np.mean(np.array(dealer_hand) == 'HighDiff'))

    # Create new dataframe
    response_times = data.loc[:, 'ResponseTime'].to_numpy()
    responses = data.loc[:, 'Response'].to_numpy()
    new_dict = {
        'TimePressure': time_pressure,
        'PlayerHand': player_hand,
        'DealerHand': dealer_hand,
        'ResponseTime': response_times,
        'Response': responses
    }
    new_data = pandas.DataFrame(data=new_dict)
    return new_data

def view_choice_selection(data,col=0, axs=None,has_legend=True,title_sz=11):
    if axs is None:
        fig,axs = plt.subplots(3,2,constrained_layout=True)

    r = 0
    c = col
    plt_type = 'Observed' if col==0 else 'Predicted'
    # Get data subset by dealer hand (plot #)
    for dealer_hand in ['Low','Med','High']:
        data_DH =  data.loc[data['DealerHand'] == dealer_hand]

        for TP in ['Low','Med','High']:
            d = data_DH.loc[data_DH['TimePressure'] == TP]

            # Get Risk-Level-Index (x-axis)
            risk_level = d.loc[:,'PlayerHand'].to_numpy()
            risk_level[risk_level == 'Low'] = 1
            risk_level[risk_level == 'Med'] = 2
            risk_level[risk_level == 'High'] = 3
            risk_level[risk_level == 'Most'] = 4

            # Get Probability of Gamble (y-axis)
            gamble = d.loc[:, 'Response'].to_numpy()
            gamble[gamble == 'y'] = 1
            gamble[gamble == 'n'] = 0

            # Get means
            unique_risk_levels = [1,2,3,4]; p_gamble = []
            for rl in unique_risk_levels:  p_gamble.append(np.mean(gamble[risk_level==rl]))

            # Plot
            axs[r, c].plot(unique_risk_levels, p_gamble,label=f'{TP} TP',marker='.')

        # Configure Plot Settings
        axs[r,c].set_title(f'{plt_type}, Dealer Card is {dealer_hand}',fontsize=title_sz)
        if c ==0: axs[r, c].set_ylabel(f'P(Gamble)')
        if r ==np.shape(axs)[0]-1: axs[r, c].set_xlabel(f'Risk Level')
        if has_legend:axs[r, c].legend()
        r +=1 # next plot
    return fig, axs

def view_response_time(data,col=0, axs=None,has_legend=True,title_sz=11):
    if axs is None:
        fig,axs = plt.subplots(3,2,constrained_layout=True)

    r = 0
    c = col
    plt_type = 'Observed' if col == 0 else 'Predicted'
    # Get data subset by dealer hand (plot #)
    for dealer_hand in ['Low','Med','High']:
        data_DH =  data.loc[data['DealerHand'] == dealer_hand]

        for TP in ['Low','Med','High']:
            d = data_DH.loc[data_DH['TimePressure'] == TP]

            # Get Risk-Level-Index (x-axis)
            risk_level = d.loc[:,'PlayerHand'].to_numpy()
            risk_level[risk_level == 'Low'] = 1
            risk_level[risk_level == 'Med'] = 2
            risk_level[risk_level == 'High'] = 3
            risk_level[risk_level == 'Most'] = 4

            # Get Response Time (y-axis)
            response_times = d.loc[:, 'ResponseTime'].to_numpy()

            # Get means
            unique_risk_levels = [1,2,3,4]; mean_response_times = []
            for rl in unique_risk_levels:  mean_response_times.append(np.mean(response_times[risk_level==rl]))

            # Plot
            axs[r, c].plot(unique_risk_levels, mean_response_times,label=f'{TP} TP',marker='.')

        # Configure Plot Settings
        axs[r,c].set_title(f'{plt_type}, Dealer Card is {dealer_hand}',fontsize=title_sz)
        if c ==0: axs[r, c].set_ylabel(f'Mean RT')
        if r ==np.shape(axs)[0]-1: axs[r, c].set_xlabel(f'Risk Level')
        if has_legend: axs[r, c].legend()
        r +=1 # next plot
    return fig,axs

def import_data():
    # Load Data ----------------------------
    FNAMES = [
        '../data/data_11-26-2023_10-57-10',
        # '../data/data_11-26-2023_16-42-26',
        '../data/data_12-04-2023_13-28-54',
        '../data/data_12-04-2023_13-37-46',
        '../data/data_12-04-2023_13-50-32'
    ]
    # fname = '../data/data_11-26-2023_10-57-10'
    data = load_data(FNAMES[0])
    for fname in FNAMES[1:]:
        data = data.append(load_data(fname))
    data = relabel_data(data)
    return data


def main():
    fname = 'data_11-26-2023_10-57-10'
    data = load_data(fname)
    data = relabel_data(data)
    axs_gamble = view_choice_selection(data)
    axs_responsetime = view_response_time(data)
    plt.show()
if __name__ =="__main__":
    main()