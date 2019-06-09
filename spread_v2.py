from plague import Plague
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os


def FuzzyController(infectionStatus, effectiveInfectionRate):

    infectedPercentage = np.arange(0, 1.1, 0.1)
    effectivePercentage = np.arange(-1, 1.1, 0.1)
    controlVariable = np.arange(-0.15, 0.16, 0.01)


    # Generate fuzzy membership functions
    prcnt_1 = fuzz.trapmf(infectedPercentage, [0, 0, 0.3, 0.6])
    prcnt_2 = fuzz.trimf(infectedPercentage, [0.3, 0.6, 0.8])
    prcnt_3 = fuzz.trapmf(infectedPercentage, [0.6, 0.8, 1, 1])

    prcnt_effect_1 = fuzz.trimf(effectivePercentage, [-1, -1, 0])
    prcnt_effect_2 = fuzz.trimf(effectivePercentage, [-1, 0, 1])
    prcnt_effect_3 = fuzz.trimf(effectivePercentage, [0, 1, 1])

    effect_1 = fuzz.trapmf(controlVariable, [-0.15, -0.15, -0.1, -0.05])
    effect_2 = fuzz.trimf(controlVariable, [-0.1, -0.05, 0])
    effect_3 = fuzz.trimf(controlVariable, [-0.05, 0, 0.05])
    effect_4 = fuzz.trimf(controlVariable, [0, 0.05, 0.1])
    effect_5 = fuzz.trapmf(controlVariable, [0.05, 0.1, 0.15, 0.16])

    # Visualize the membership functions
    '''
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(infectedPercentage, prcnt_1, 'b', linewidth=1.5, label='Low')
    ax0.plot(infectedPercentage, prcnt_2, 'g', linewidth=1.5, label='Normal')
    ax0.plot(infectedPercentage, prcnt_3, 'r', linewidth=1.5, label='High')
    ax0.set_title('Infection Percentage')
    ax0.legend()

    ax1.plot(effectivePercentage, prcnt_effect_1, 'b', linewidth=1.5, label='Small')
    ax1.plot(effectivePercentage, prcnt_effect_2, 'g', linewidth=1.5, label='Medium')
    ax1.plot(effectivePercentage, prcnt_effect_3, 'r', linewidth=1.5, label='Large')
    ax1.set_title('Effective Infection Rate')
    ax1.legend()

    ax2.plot(controlVariable, effect_1, 'b', linewidth=1.5, label='1')
    ax2.plot(controlVariable, effect_2, 'g', linewidth=1.5, label='2')
    ax2.plot(controlVariable, effect_3, 'r', linewidth=1.5, label='3')
    ax2.plot(controlVariable, effect_4, color='purple', linewidth=1.5, label='4')
    ax2.plot(controlVariable, effect_5, color='yellow', linewidth=1.5, label='5')
    ax2.set_title('Control Variable')
    ax2.legend()

    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    # plt.show()
    plt.savefig('sets_part2.png')
    '''
    # Apply the rules
    # interp_membership used for float points
    prcnt_level_1 = fuzz.interp_membership(infectedPercentage, prcnt_1, infectionStatus)
    prcnt_level_2 = fuzz.interp_membership(infectedPercentage, prcnt_2, infectionStatus)
    prcnt_level_3 = fuzz.interp_membership(infectedPercentage, prcnt_3, infectionStatus)

    effect_prcnt_level_1 = fuzz.interp_membership(effectivePercentage, prcnt_effect_1, effectiveInfectionRate)
    effect_prcnt_level_2 = fuzz.interp_membership(effectivePercentage, prcnt_effect_2, effectiveInfectionRate)
    effect_prcnt_level_3 = fuzz.interp_membership(effectivePercentage, prcnt_effect_3, effectiveInfectionRate)

    # if infected percentage + effective infection rate is low, then control variable must be high, otherwise vice versa
    activerule1 = np.fmax(np.fmin(prcnt_level_3, effect_prcnt_level_3), np.fmin(prcnt_level_2, effect_prcnt_level_3))
    activerule2 = np.fmax(np.fmin(prcnt_level_3, effect_prcnt_level_2), np.fmin(prcnt_level_1, effect_prcnt_level_3))
    activerule3 = np.fmin(prcnt_level_2, effect_prcnt_level_2)
    activerule4 = np.fmax(np.fmin(np.fmin(prcnt_level_3, effect_prcnt_level_1), np.fmin(prcnt_level_2, effect_prcnt_level_1)),
                          np.fmin(prcnt_level_1, effect_prcnt_level_2))
    activerule5 = np.fmin(prcnt_level_1, effect_prcnt_level_1)

    control_activation_1 = np.fmin(activerule1, effect_1)
    control_activation_2 = np.fmin(activerule2, effect_2)
    control_activation_3 = np.fmin(activerule3, effect_3)
    control_activation_4 = np.fmin(activerule4, effect_4)
    control_activation_5 = np.fmin(activerule5, effect_5)

    # Visualize by uncommenting
    if draw == 1:
        controlvar = np.zeros_like(controlVariable)
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.fill_between(controlVariable, controlvar, control_activation_1, facecolor='b', alpha=0.7)
        ax0.plot(controlVariable, effect_1, 'b', linewidth=0.5, linestyle='--', )
        ax0.fill_between(controlVariable, controlvar, control_activation_2, facecolor='g', alpha=0.7)
        ax0.plot(controlVariable, effect_2, 'g', linewidth=0.5, linestyle='--')
        ax0.fill_between(controlVariable, controlvar, control_activation_3, facecolor='r', alpha=0.7)
        ax0.plot(controlVariable, effect_3, 'r', linewidth=0.5, linestyle='--')
        ax0.fill_between(controlVariable, controlvar, control_activation_4, facecolor='r', alpha=0.7)
        ax0.plot(controlVariable, effect_4, 'purple', linewidth=0.5, linestyle='--')
        ax0.fill_between(controlVariable, controlvar, control_activation_5, facecolor='r', alpha=0.7)
        ax0.plot(controlVariable, effect_5, 'yellow', linewidth=0.5, linestyle='--')
        ax0.set_title('Control variable membership activity')

        # Turn off top/right axes
        for ax in (ax0,):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.savefig('membership_activity_part2_last.png')

    # Aggregate all three output membership functions together
    aggregated = np.fmax(np.fmax(control_activation_1, control_activation_2),
                         np.fmax(np.fmax(control_activation_3, control_activation_4), control_activation_5))

    # Calculate defuzzified result
    control_variable = fuzz.defuzz(controlVariable, aggregated, 'centroid')
    controller_activation = fuzz.interp_membership(controlVariable, aggregated, control_variable)  # for plot

    # Visualize this by uncommenting following lines
    if draw == 1:
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.plot(controlVariable, effect_1, 'b', linewidth=0.5, linestyle='--', )
        ax0.plot(controlVariable, effect_2, 'g', linewidth=0.5, linestyle='--')
        ax0.plot(controlVariable, effect_3, 'r', linewidth=0.5, linestyle='--')
        ax0.plot(controlVariable, effect_4, 'purple', linewidth=0.5, linestyle='--')
        ax0.plot(controlVariable, effect_5, 'yellow', linewidth=0.5, linestyle='--')
        ax0.fill_between(controlVariable, controlvar, aggregated, facecolor='Orange', alpha=0.7)
        ax0.plot([control_variable, control_variable], [0, controller_activation], 'k', linewidth=1.5, alpha=0.9)
        ax0.set_title('Aggregated membership and result (line)')

        # Turn off top/right axes
        for ax in (ax0,):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.savefig('aggregated_part2_last.png')

    return control_variable


control_variable = 0
plague = Plague()
infectRate = np.ones([30, 1])
enable = 0
plague_cost_dummy = 0
draw = 0
for i in range(0, 200):

    plague.spreadPlague(control_variable)
    infectionStatus, effectiveInfectionRate = plague.checkInfectionStatus()
    if i == 199:
        draw = 1
    control_variable = FuzzyController(infectionStatus, effectiveInfectionRate)
    p = plague.infected_percentage_curve_[-1]
    q = plague.infection_rate_curve_[-1]
    plague_cost_dummy = plague_cost_dummy + q
    infectRate[i % 30] = abs(control_variable)
    print(infectRate)
    if np.amax(infectRate) < 0.003 and enable == 0:
        point_ss = i
        plague_cost = plague_cost_dummy
        enable = 1

plague.viewPlague(point_ss, plague_cost)


