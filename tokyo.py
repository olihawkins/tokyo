# -*- coding: utf-8 -*-
# Module: tokyo.py
# About: Simulate distribution of dice outcomes in King Of Tokyo
# Notes:
#
# To get font names for use with seaborn/matplotlib on Windows ...
#   
#   import matplotlib.font_manager as fm
#   flist = fm.findSystemFonts(fontpaths=None, fontext='ttf')
#   names = [fm.FontProperties(fname=fname).get_name() for fname in flist]
#
# To use nice system fonts on MacOS convert system font files from dfont to 
# ttf with fondu in ~/Library/Fonts/ and clear matplotlib's font cache, see:
# https://gist.github.com/alexrudy/a7982903a2fb2ab0dde3


# Imports --------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Functions ------------------------------------------------------------------

def max_outcome_for_face(dice=6, rolls=3):

    """ Simulates an outcome for the maximum number of one face.

    Rolls the given number of dice a given number of times and counts how 
    many of the dice show the target face after each roll, assuming the 
    player keeps every target face after every roll.
    """

    hits = 0
    outcome = [0] * rolls

    for roll in range(rolls):

        # Get a random number from one to six for each dice
        results = np.random.randint(1, 7, size=dice)
        
        # Count the number of ones: a one is a hit
        numhits = np.count_nonzero(results == 1)
        
        # Add to hits and remove a dice for each hit
        hits = hits + numhits
        dice = dice - numhits 

        # Store the hits after each roll
        outcome[roll] = hits

    return outcome


def max_outcomes_for_face(dice=6, rolls=3, sims=100000):

    """ Simulates outcomes for the maximum number of one face.

    Simulates the maximum outcomes for one face the given number of times and
    returns the outcomes of the simulations as a DataFrame for analysis.

    Runs one hundred thousand simulations by default, which with the other
    default settings takes around 1.5 seconds on a 2015 13 inch MBP. One 
    million simulations takes around 15 seconds, and ten million takes around
    two and a half minutes. Times increase with more dice and rolls.
    """

    if sims < 1:
        raise ValueError('Number of simulations must be greater than zero.')

    outcomes = []
    colnames = ['r{0}'.format(i + 1) for i in range(rolls)]
    
    for s in range(sims):

        outcome = max_outcome_for_face(dice, rolls)
        outcomes.append(outcome)

    outcomes = np.asarray(outcomes)
    outcomes = pd.DataFrame(outcomes, columns=colnames)
    
    return outcomes


def summarise_counts(outcomes):

    """ Summarises frequency counts from max_outcomes_for_face. """

     # Build a dictionary for counts
    counts = {}

    # Get the counts
    for c in outcomes.columns:
        counts['c{0}'.format(c[1:])] = outcomes[c].value_counts().sort_index()

    # Convert to dataframe
    counts = pd.DataFrame(counts)

    # Fill missing values and cast to int
    for c in counts.columns:
        counts[c] = counts[c].fillna(0.0).astype(int)

    return counts


def summarise_percentages(outcomes):

    """ Summarises percentages from max_outcomes_for_face. """

    # Build a dictionary of percentages
    percentages = {}

    # Get summary of counts
    counts = summarise_counts(outcomes)

    # Calculate percentages and return as dataframe
    for c in counts.columns:
        percentages['p{0}'.format(c[1:])] = counts[c] / sum(counts[c])

    return pd.DataFrame(percentages)


def percentage_labels(percentages):

    """ Creates a dataframe of string labels for the given percentages. """

    # Build a dictionary of labels
    labels = {}

    # Generate the labels and return as dataframe
    for c in percentages.columns:
        labels['l{0}'.format(c[1:])] = \
            ['{:.1f}'.format(p * 100) for p in percentages[c]]

    return pd.DataFrame(labels)


def save_heatmap(
    data, labels, filename, title, cmap, 
    vmin=None,  vmax=None, width=12, height=19):

    """ Saves a heatmap of the summary data. """

    # Create labels for columns
    data.columns = \
        ['Roll {0}'.format(i + 1) for i in range(len(data.columns))]

    # Turn off interactive plotting
    plt.ioff()

    # Set the font
    sns.set(font='Helvetica Neue', font_scale=2.5)

    # Plot the heatmap
    fig = plt.figure()
    fig.suptitle('Percentage of outcomes with N faces', weight='bold')

    ax = sns.heatmap(
        data, cmap=cmap, vmin=vmin, 
        vmax=vmax, annot=labels, fmt='')

    ax.set_title(title)
    fig.add_subplot(ax)
    fig.set_size_inches(width, height, False)
    fig.savefig(filename, bbox_inches='tight', pad_inches=0.5)
    plt.close(fig)


def run_analysis():

    """ Do the analysis. 

    By default this is set up to run ten million simulations for each of two
    scenarios and it takes around eight minutes to run. Reduce the number of 
    simulations to generate output more quickly, but with less precision.
    """

    o64 = max_outcomes_for_face(dice=6, rolls=4, sims=10000000)
    p64 = summarise_percentages(o64)
    l64 = percentage_labels(p64)
    
    save_heatmap(
        p64, l64, 'tokyo-heatmap-64', '6 dice, 4 rolls', 
        cmap='YlGnBu', vmin=0.0, vmax=0.4,width=12, height=16.2)

    o74 = max_outcomes_for_face(dice=7, rolls=4, sims=10000000)
    p74 = summarise_percentages(o74)
    l74 = percentage_labels(p74)
    
    save_heatmap(
        p74, l74, 'tokyo-heatmap-74', '7 dice, 4 rolls', 
        cmap='YlOrRd', vmin=0.0, vmax=0.4, width=12, height=18.2)

    return(p64, p74)
