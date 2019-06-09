from plague import Plague
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os


def FuzzyController(infectionStatus):

    infectedPercentage = np.arange(0, 1.1, 0.1)
    controlVariable = np.arange(-0.15, 0.16, 0.03)


    # Generate fuzzy membership functions
    prcnt_lo = fuzz.trapmf(infectedPercentage, [0, 0, 0.3, 0.6])
    prcnt_md = fuzz.trimf(infectedPercentage, [0.3, 0.6, 0.8])
    prcnt_hi = fuzz.trapmf(infectedPercentage, [0.6, 0.8, 1, 1])

    effect_lo = fuzz.trimf(controlVariable, [-0.15, -0.15, 0])
    effect_md = fuzz.trimf(controlVariable, [-0.15, 0, 0.15])
    effect_hi = fuzz.trimf(controlVariable, [0, 0.15, 0.15])

    # Visualize the membership functions
    '''
    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 9))

    ax0.plot(infectedPercentage, prcnt_lo, 'b', linewidth=1.5, label='Low')
    ax0.plot(infectedPercentage, prcnt_md, 'g', linewidth=1.5, label='Normal')
    ax0.plot(infectedPercentage, prcnt_hi, 'r', linewidth=1.5, label='High')
    ax0.set_title('Infection Percentage')
    ax0.legend()

    ax1.plot(controlVariable, effect_lo, 'b', linewidth=1.5, label='Small')
    ax1.plot(controlVariable, effect_md, 'g', linewidth=1.5, label='Medium')
    ax1.plot(controlVariable, effect_hi, 'r', linewidth=1.5, label='Large')
    ax1.set_title('Control Variable')
    ax1.legend()

    for ax in (ax0, ax1):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig('sets.png')
    '''
    # Apply the rules
    # interp_membership used for float points
    prcnt_level_lo = fuzz.interp_membership(infectedPercentage, prcnt_lo, infectionStatus)
    prcnt_level_md = fuzz.interp_membership(infectedPercentage, prcnt_md, infectionStatus)
    prcnt_level_hi = fuzz.interp_membership(infectedPercentage, prcnt_hi, infectionStatus)

    # Apply the rules
    # if percentage is low, then control variable must be high, otherwise vice versa
    control_activation_lo = np.fmin(prcnt_level_lo, effect_hi)
    control_activation_md = np.fmin(prcnt_level_md, effect_md)
    control_activation_hi = np.fmin(prcnt_level_hi, effect_lo)

    # Visualize
    if draw == 1:
        controlvar = np.zeros_like(controlVariable)
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.fill_between(controlVariable, controlvar, control_activation_lo, facecolor='b', alpha=0.7)
        ax0.plot(controlVariable, effect_lo, 'b', linewidth=0.5, linestyle='--', )
        ax0.fill_between(controlVariable, controlvar, control_activation_md, facecolor='g', alpha=0.7)
        ax0.plot(controlVariable, effect_md, 'g', linewidth=0.5, linestyle='--')
        ax0.fill_between(controlVariable, controlvar, control_activation_hi, facecolor='r', alpha=0.7)
        ax0.plot(controlVariable, effect_hi, 'r', linewidth=0.5, linestyle='--')
        ax0.set_title('Control variable membership activity')

        # Turn off top/right axes
        for ax in (ax0,):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.savefig('membership_activity.png')


    # Aggregate all three output membership functions together
    aggregated = np.fmax(control_activation_lo,
                         np.fmax(control_activation_md, control_activation_hi))

    # Calculate defuzzified result
    control_variable = fuzz.defuzz(controlVariable, aggregated, 'centroid')
    controller_activation = fuzz.interp_membership(controlVariable, aggregated, control_variable)  # for plot

    # Visualize this by uncommenting following lines
    if draw == 1:
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.plot(controlVariable, effect_lo, 'b', linewidth=0.5, linestyle='--', )
        ax0.plot(controlVariable, effect_md, 'g', linewidth=0.5, linestyle='--')
        ax0.plot(controlVariable, effect_hi, 'r', linewidth=0.5, linestyle='--')
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
        plt.savefig('aggregated.png')


    return control_variable

control_variable = 0
plague = Plague()
infectRate = np.ones([30, 1])
enable = 0
plague_cost_dummy = 0
draw = 1
for i in range(0, 200):


    plague.spreadPlague(control_variable)
    infectionStatus, effectiveInfectionRate = plague.checkInfectionStatus()
    control_variable = FuzzyController(infectionStatus)
    draw = 0
    p = plague.infected_percentage_curve_[-1]
    q = plague.infection_rate_curve_[-1]
    plague_cost_dummy = plague_cost_dummy + q
    infectRate[i % 30] = abs(control_variable)
    if np.amax(infectRate) < 0.003 and enable == 0:
        point_ss = i
        plague_cost = plague_cost_dummy
        enable = 1



plague.viewPlague(point_ss, plague_cost)




