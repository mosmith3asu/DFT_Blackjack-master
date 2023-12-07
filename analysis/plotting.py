import math

import pandas

from data.data_utils import load_data,relabel_data,view_choice_selection,view_response_time, import_data
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class DecisionFieldTheory():
    def __init__(self):
        """
        theta:  magnitude of the inhibitory threshold
        d:  mean change in preference at each state
        (theta/d): travel time equals distance divided by rate of travel.
        """
        self.theta = 0 # magnitude of the inhibitory threshold
        self.d = 0 # mean change in preference at each state
        self.d_ijk = np.zeros([4,3,3])  # mean change in preference at each state
        self.theta_ijk = np.zeros([4,3,3])  # magnitude of the inhibitory threshold

    def predict(self,risk_level, computer_card_level, time_pressure):
        """
        :param risk_level: i(i = 1, 2,3,4)
        :param computer_card_level: (j = 1,2,3)
        :param time_pressure: (k = 0,1,2).
        PrG: probability of choosing to gamble
        ET: expected response time
        :return:
        """
        d = self.d_ijk[risk_level,computer_card_level,time_pressure]
        theta = self.theta_ijk[risk_level,computer_card_level,time_pressure]
        PrG = 1/(1 + np.exp(-2*theta*d))
        ET = (theta/d)*(2*PrG-1)
        return PrG, ET

    def fit_advanced(self, dec_data):
        def obj_fun(params, data):
            """
            :param params: [a,theta,p]
            :param data: [risk_level, gambles,RT]
            :return: objective: MSE
            """
            a,theta,p = params
            MSE = np.zeros(4)
            for i in range(4):
                this_d = -a * (i - 1.5)  # d = -a * (i - 1 + s)

                # Calculate Errors
                PrG_pred = 1 / (1 + np.exp(-2 * theta * this_d))
                gambles_obs = data[np.where(data[:, 0] == i), 1]
                this_MSE = np.mean(np.power(gambles_obs - PrG_pred, 2))
                MSE[i] = this_MSE
            return np.mean(MSE)


            # Individual Effect
            # p = .42
            # Ps = []
            # for s in [-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5]:
            #     val = (math.factorial(6) / (math.factorial(2 * s + 3) * math.factorial(3 - 2 * s))) * pow(p,
            #                                                                                               2 * s + 3) * pow(
            #         1 - p, 3 - 2 * s)
            #     Ps.append(val)

            # PrG_pred = 1 / (1 + np.exp(-2 * theta * d))
            # PrG_obs = data[:, 0]
            # # Predicted times are only proportional to observed times
            # # ET_pred = (theta / d) * (2 * PrG_pred - 1)
            # # RT_obs = data[:,1]
            # # RT_obj = RT_obs/np.sum(RT_obs)
            #
            # MSE = np.mean(np.power(PrG_obs - PrG_pred, 2))
            # return MSE
        # -------------------------------------
        # a: shared
        # data = [i,PrG,RT]
        # x = [a,theta,p]

        for j, computer_hand in enumerate(['Low', 'Med', 'High']):
            for k, time_pressure in enumerate(['Low', 'Med', 'High']):
                this_data = dec_data
                # this_data = this_data.loc[dec_data['PlayerHand'] == risk_level]
                this_data = this_data.loc[this_data['DealerHand'] == computer_hand]
                this_data = this_data.loc[this_data['TimePressure'] == time_pressure]

                # Get observed gambles
                gambles = this_data.loc[:, 'Response'].to_numpy()
                gambles[gambles == 'y'] = 1
                gambles[gambles == 'n'] = 0
                PrG_obs = np.mean(gambles)

                # Get response times
                response_times = this_data.loc[:, 'ResponseTime'].to_numpy()
                ET_obs = np.mean(response_times)

                # Get risk levels
                RL_obs = this_data.loc[:,'PlayerHand'].to_numpy()
                RL_obs[RL_obs == 'Low'] = 0
                RL_obs[RL_obs == 'Med'] = 1
                RL_obs[RL_obs == 'High'] = 2
                RL_obs[RL_obs == 'Most'] = 3

                # MLE
                data = np.vstack([RL_obs,gambles, response_times]).T
                result = minimize(obj_fun, [0.842,0.955,0.42], args=(data))
                a_star, theta_star,p_star = result['x']

    def fit(self,dec_data):
        def obj_fun(params,data):
            """
            :param params: [d,theta]
            :param data: [gambles,RT]
            :return: objective: MSE
            """
            d,theta = params
            PrG_pred = 1 / (1 + np.exp(-2 * theta * d))
            PrG_obs = data[:, 0]
            # Predicted times are only proportional to observed times
            # ET_pred = (theta / d) * (2 * PrG_pred - 1)
            # RT_obs = data[:,1]
            # RT_obj = RT_obs/np.sum(RT_obs)

            MSE = np.mean(np.power( PrG_obs- PrG_pred,2))
            return MSE

        for i, risk_level in enumerate(['Low','Med','High','Most']):
            for j, computer_hand in enumerate(['Low', 'Med', 'High']):
                for k, time_pressure in enumerate(['Low', 'Med', 'High']):
                    this_data = dec_data
                    this_data = this_data.loc[this_data['PlayerHand'] == risk_level]
                    this_data = this_data.loc[this_data['DealerHand'] == computer_hand]
                    this_data = this_data.loc[this_data['TimePressure'] == time_pressure]

                    # Get observed gambles
                    gambles = this_data.loc[:, 'Response'].to_numpy()
                    gambles[gambles == 'y'] = 1
                    gambles[gambles == 'n'] = 0
                    PrG_obs = np.mean(gambles)

                    # Get response times
                    response_times = this_data.loc[:, 'ResponseTime'].to_numpy()
                    ET_obs = np.mean(response_times)

                    # MLE
                    data = np.vstack([gambles, response_times]).T
                    result = minimize(obj_fun, [-0.001,0.955], args=(data))
                    d_star,theta_star   = result['x']

                    self.d_ijk[i,j,k] = d_star
                    self.theta_ijk[i, j, k] = theta_star


    def old_fit(self):
        """
        Seven params
            d_ijk: mean change in preference under
                    risk level i(i = 1, 2,3,4)
                    computer card level} (j = 1,2,3)
                    time pressure condition k (k = 0,1,2).
            a: effect of risk level estimated from choice data (proportional to risk level)
            cj: effect of the computer card level (c1 = 2.85,c2=2.92,c3=3.14)
            Sl: random effect (Sl<0: more risk seeking; Sl>0: more risk averse)
                    binomial distribution across {-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5}
                    with a parameter p = .42 (estimated from the choice data)
                    prob of Sl: P[S, = s] = [(6!)/(2s + 3)!(3 - 2s)!] p2s + 3(1 - p)(3 - 1).
        Sol: mimized the sum of squared deviations between the predicted and the observed choice probabilities
        :return:
        """
        a = 0.842
        c = [2.85,2.92,3.14]
        for i in [1,2,3,4]:
            for j in [1,2,3]:
                k = 1 # fix time pressure to be present
                d_ijk = (1 - k) * c[j]- a * (i - 3.5)

        # d_ijkl= (1-k)*cj-a*(i-3.5+Sl)


if __name__ == "__main__":
    # main()
    # p = .42
    # Ps = []
    # for s in [-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5]:
    #     val = (math.factorial(6)/(math.factorial(2*s+3)*math.factorial(3-2*s)))*pow(p,2*s+3)*pow(1-p,3-2*s)
    #     Ps.append(val)
    # print(Ps)
    title_sz = 11

    #
    # # Load Data ----------------------------
    # FNAMES = [
    #     '../data/data_11-26-2023_10-57-10',
    #     # '../data/data_11-26-2023_16-42-26',
    #     '../data/data_12-04-2023_13-28-54',
    #     '../data/data_12-04-2023_13-37-46',
    #     '../data/data_12-04-2023_13-50-32'
    # ]
    # # fname = '../data/data_11-26-2023_10-57-10'
    # data = load_data(FNAMES[0])
    # for fname in FNAMES[1:]:
    #     data = data.append(load_data(fname))
    # data = relabel_data(data)
    # print(data)
    data = import_data()
    # Plot Observed Data -------------------
    fig_gamble,axs_gamble = view_choice_selection(data,col=0,has_legend=False)
    fig_responsetime, axs_responsetime = view_response_time(data,col=0,has_legend=False)

    # Fit DFT -----------------------------
    DFT = DecisionFieldTheory()
    DFT.fit(data)
    MSEijk = np.zeros([4,3,3])
    # DFT.fit_advanced(data)
    # Predict DFT -------------------------
    plt_type = 'Predicted'
    for j, computer_hand in enumerate(['Low', 'Med', 'High']):
        for k, time_pressure in enumerate(['Low', 'Med', 'High']):
            PrG = np.zeros(4)
            RT = np.zeros(4)

            for i, risk_level in enumerate(['Low', 'Med', 'High', 'Most']):
                PrG[i],RT[i] = DFT.predict(i,j,k)


                df_obs = data.loc[(data['PlayerHand'] == risk_level) &
                                  (data['DealerHand'] == computer_hand) &
                                  (data['TimePressure'] == time_pressure)]

                responses = df_obs['Response'].to_numpy()
                responses[responses == 'y'] = 1
                responses[responses == 'n'] = 0

                PrG_obs = np.mean(responses)
                MSEijk[i,j,k] = (PrG[i] - PrG_obs)**2


            risk_levels = np.arange(4)
            axs_gamble[j, 1].plot(risk_levels,PrG,label=f'{time_pressure} TP',marker='.')
            axs_responsetime[j, 1].plot(risk_levels, RT, label=f'{time_pressure} TP',marker='.')

            axs_gamble[j, 1].set_title(f'{plt_type}, Dealer Card is {computer_hand}',fontsize=title_sz)
            axs_responsetime[j, 1].set_title(f'{plt_type}, Dealer Card is {computer_hand}',fontsize=title_sz)
            axs_gamble[j, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
            axs_responsetime[j, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if j == np.shape(axs_responsetime)[0] - 1:
            axs_gamble[j, 1].set_xlabel(f'Risk Level')
            axs_responsetime[j, 1].set_xlabel(f'Risk Level')

    for j, computer_hand in enumerate(['Low', 'Med', 'High']):
        print(f'\nComputer hand is {computer_hand}')
        print(MSEijk[:, j, :])



    # axs_gamble = view_choice_selection(data,col=1,axs=axs_gamble)
    # axs_responsetime = view_response_time(data,col=1,axs=axs_responsetime)
    # plt.rcParams.update({'axes.titlesize': 'small','figure.titlesize': 'small'})
    fig_gamble.savefig('Fig_Gambles')
    fig_responsetime.savefig('Fig_ResponseTimes')
    plt.show()