# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "aa8e1fcd-d154-aae2-5fd3-caadd56eeda5"
      },
      "source": [
        "# **Hey Kagglers, this is meant to be a fun little visualization tutorial using the [Seaborn](https://stanford.edu/~mwaskom/software/seaborn/index.html) library and [Alberto Barradas'](https://www.kaggle.com/abcsds) [Pok\u00e9mon dataset](https://www.kaggle.com/abcsds/pokemon).**  \n",
        "# Whether you're following along or just skimming through, thanks for checking it out!"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "a457b656-ffb0-418e-da7b-d22ff08f87dd"
      },
      "source": [
        "----------"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "bd1ffbd7-c1f6-0925-ffc5-fee8c97d5b4e"
      },
      "source": [
        "# Notebook Prep"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "b836a0f8-f833-27b6-cc2d-f9c5e0e5d7e2"
      },
      "source": [
        "First, let's import the packages we'll be using in this kernel. "
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "_cell_guid": "c4b6100a-de4f-c692-338e-1ada42ef014a"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "dab853f1-e7bf-6e8f-20aa-941eee604ab7"
      },
      "source": [
        "----------"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "e77a08d6-d4e1-bcdb-53ae-6cf7d8e6192b"
      },
      "source": [
        "# Data Import"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "5ab24889-6938-7ab5-d5b7-c8a351562e97"
      },
      "source": [
        "Now, let's [read](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html) in the data with Pandas.  \n",
        "If you're working in something other than a Kaggle notebook, be sure to change the file location."
      ]
    },
    {
      "cell_type": "code",
   
      "metadata": {
        "_cell_guid": "9234dcce-62d9-7344-7541-cf882c3de233"
      },
      "outputs": [],
      "source": [
        "pkmn = pd.read_csv('../input/Pokemon.csv')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "84ac0503-7481-850d-e506-cadd9e942c5b"
      },
      "source": [
        "Using the [head](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.head.html) method, let's take a peak at the data."
      ]
    },
    {
      "cell_type": "code",
      
      "metadata": {
        "_cell_guid": "b8c15db5-9758-9830-d3b4-b6946d8655ab"
      },
      "outputs": [],
      "source": [
        "pkmn.head()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "884419e0-0107-bd55-c1b7-00385c90f6eb"
      },
      "source": [
        "We've got a pretty simple format here! There's the Pok\u00e9mon number, name, their type(s), their different stat values, and a convenient Total variable."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "ed7da440-4443-acfa-974b-7d0e94842840"
      },
      "source": [
        "## Update Aug 30 2016:  \n",
        "I just realized that Generation and Legendary variables were added to the dataset.  \n",
        "I'm going to add a step here to drop the variables so that the rest of the code works as it did originally.  \n",
        "Apologies to anyone who forked the notebook and had trouble following along!"
      ]
    },
    {
      "cell_type": "code",
    
      "metadata": {
        "_cell_guid": "831272ec-2117-b94f-beec-1c65db3c22e1"
      },
      "outputs": [],
      "source": [
        "pkmn = pkmn.drop(['Generation', 'Legendary'],1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "eae383af-c58d-0b7b-a66c-bcc3efedc7d9"
      },
      "source": [
        "----------"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "57762535-8ec4-a4ee-d112-c2af2bd28de3"
      },
      "source": [
        "# Plots with Seaborn"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "3d335caf-994d-ad13-fb17-1e770f388cfe"
      },
      "source": [
        "To start things off, let's just make a [scatterplot](https://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.jointplot.html) based on two variables from the data set.  \n",
        "I'll use HP and Attack in this example, but feel free to do something different!"
      ]
    },
    {
      "cell_type": "code",
     
      "metadata": {
        "_cell_guid": "2b8ccc61-1459-b36d-114e-92a068f765d6"
      },
      "outputs": [],
      "source": [
        "sns.jointplot(x=\"HP\", y=\"Attack\", data=pkmn);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "fe626279-5c5c-cde0-c7d5-eb0a163d83d0"
      },
      "source": [
        "Nothing *too* informative here, but we can definitely see why the Seaborn library is so popular. With one short line of code, we get this really nice looking plot!"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "9d6d9ed8-3f32-e966-1c68-9902a1eca265"
      },
      "source": [
        "Now let's see if we can make something a little bit prettier. How about a distribution of all six stats? We could even group it further using Pok\u00e9mon type!  \n",
        "This might seem a little ambitious, but let's take it one step at a time."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "c6e5441e-e2be-1c43-8bbb-cc3023854a2f"
      },
      "source": [
        "For starters, let's see if we can make a basic [box and whisker plot](https://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.boxplot.html) of a single variable."
      ]
    },
    {
      "cell_type": "code",
   
      "metadata": {
        "_cell_guid": "07facb7b-caa6-1ef0-3793-939a20068523"
      },
      "outputs": [],
      "source": [
        "sns.boxplot(y=\"HP\", data=pkmn);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "254d88fc-1efe-a4ed-1aba-31d41f82beb4"
      },
      "source": [
        "Cool! Not too hard.  \n",
        "Now let's see if we can get all of the stats in there."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "0fdda5bd-884a-e051-b5d0-b71b091580cb"
      },
      "source": [
        "As it turns out, if you don't specify an x or y argument, Seaborn will give you a plot for each numeric variable. Handy!"
      ]
    },
    {
      "cell_type": "code",
  
      "metadata": {
        "_cell_guid": "6558458c-f368-d749-416f-cac342e13f73"
      },
      "outputs": [],
      "source": [
        "sns.boxplot(data=pkmn);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "9d7e8485-0fd2-07fd-5ac3-4c60e4dc067e"
      },
      "source": [
        "Since the # variable doesn't make sense here, let's drop it from the table.  \n",
        "Total can be dropped as well, since we didn't originally want to include it and it's on a much larger scale."
      ]
    },
    {
      "cell_type": "code",
  
      "metadata": {
        "_cell_guid": "0072de2f-259e-a0f4-0a8d-2a76ca8fbf39"
      },
      "outputs": [],
      "source": [
        "pkmn = pkmn.drop(['Total', '#'],1)"
      ]
    },
    {
      "cell_type": "code",
    
      "metadata": {
        "_cell_guid": "b270b182-9f1a-65a0-dad7-cb8281f20199"
      },
      "outputs": [],
      "source": [
        "sns.boxplot(data=pkmn);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "ffcd6b60-8ccb-07be-4b47-77bebdb40dc9"
      },
      "source": [
        "Alright, now all that's left is to include Pok\u00e9mon type in this visualization.  \n",
        "One way to do this would be switch the graph to a [swarmplot](https://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.swarmplot.html) and color code the points by type."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "c75dabb0-6fe6-7ea4-0d51-07b853885d8f"
      },
      "source": [
        "Trying to use the swarmplot function with the \"hue\" argument is going to give us some errors if we don't transform our data a bit though. The Seaborn website provides an example using Pandas' [melt](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.melt.html) function, so we'll give that a try!"
      ]
    },
    {
      "cell_type": "code",
     
      "metadata": {
        "_cell_guid": "3262cbd4-8ba8-43f7-b682-481faa2bc93e"
      },
      "outputs": [],
      "source": [
        "pkmn = pd.melt(pkmn, id_vars=[\"Name\", \"Type 1\", \"Type 2\"], var_name=\"Stat\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "31c977b8-fe2f-3d33-5268-919297309c66"
      },
      "source": [
        "So now our plot looks like this:"
      ]
    },
    {
      "cell_type": "code",
    
      "metadata": {
        "_cell_guid": "de9bc08b-e517-6cde-39a9-d244d8c3c0d1"
      },
      "outputs": [],
      "source": [
        "pkmn.head()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "eba4eda2-fd2f-faf9-e51f-670bbf7dc387"
      },
      "source": [
        "The head method doesn't really do this transformation justice, but our dataset now has 4800 rows up from 800!  \n",
        "So let's go ahead and run this plot function!"
      ]
    },
    {
      "cell_type": "code",
    
      "metadata": {
        "_cell_guid": "87cb3c9d-392d-6d4a-185d-8b560e87c2c9"
      },
      "outputs": [],
      "source": [
        "sns.swarmplot(x=\"Stat\", y=\"value\", data=pkmn, hue=\"Type 1\");"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "3451d27d-6080-91af-99b0-69f772a93df0"
      },
      "source": [
        "Oh geez. That's uh... something.  \n",
        "I think we've got some cleaning up to do."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "5a0ac6fe-caaa-eba5-ee3e-e638760b0ad4"
      },
      "source": [
        "Using a few Seaborn and Matplotlib functions, we can adjust how our plot looks.  \n",
        "On each line below, we will:   \n",
        "- [Make the plot larger](http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure)  \n",
        "- [Adjust the y-axis](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.ylim)  \n",
        "- Organize the point distribution by type  and make the individual points larger  \n",
        "- [Move the legend out of the way](http://matplotlib.org/users/legend_guide.html#legend-location)"
      ]
    },
    {
      "cell_type": "code",
     
      "metadata": {
        "_cell_guid": "252e7841-91dd-f74f-c6d4-83889438362d"
      },
      "outputs": [],
      "source": [
        "plt.figure(figsize=(12,10))\n",
        "plt.ylim(0, 275)\n",
        "sns.swarmplot(x=\"Stat\", y=\"value\", data=pkmn, hue=\"Type 1\", split=True, size=7)\n",
        "plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "06ce4f37-6124-d0a2-0161-07b607862169"
      },
      "source": [
        "Alright! This is looking better!  \n",
        "For our final touch, we'll change the background to white and create a custom color palette that corresponds to each Pok\u00e9mon type.  \n",
        "We'll use the Seaborn [color_palette](https://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.color_palette.html) function and a [with](https://www.python.org/dev/peps/pep-0343/) statement to accomplish this."
      ]
    },
    {
      "cell_type": "code",
   
      "metadata": {
        "_cell_guid": "1f33654f-026d-de70-7d1e-9ee10d3fe7a5"
      },
      "outputs": [],
      "source": [
        "sns.set_style(\"whitegrid\")\n",
        "with sns.color_palette([\n",
        "    \"#8ED752\", \"#F95643\", \"#53AFFE\", \"#C3D221\", \"#BBBDAF\",\n",
        "    \"#AD5CA2\", \"#F8E64E\", \"#F0CA42\", \"#F9AEFE\", \"#A35449\",\n",
        "    \"#FB61B4\", \"#CDBD72\", \"#7673DA\", \"#66EBFF\", \"#8B76FF\",\n",
        "    \"#8E6856\", \"#C3C1D7\", \"#75A4F9\"], n_colors=18, desat=.9):\n",
        "    plt.figure(figsize=(12,10))\n",
        "    plt.ylim(0, 275)\n",
        "    sns.swarmplot(x=\"Stat\", y=\"value\", data=pkmn, hue=\"Type 1\", split=True, size=7)\n",
        "    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.);"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "75a4a5f5-83fc-a6e3-4cc2-a88ab4b7557f"
      },
      "source": [
        "Now things are looking pretty good!"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "_cell_guid": "e144adff-5f9a-1665-2c47-0958b4357e3f"
      },
      "source": [
        "So that's the end of the tutorial for now, but feel free to keep going on your own.  \n",
        "You can try using a smaller sample of Pok\u00e9mon types, find a way to incorporate the Type 2 variable somehow, or make a different kind of plot entirely!  \n",
        "If you find anything cool, let me know! I'd love to see what everyone else comes up with!  \n",
        "Thanks again for reading!"
      ]
    }
  ],
  "metadata": {
    "_change_revision": 0,
   
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.5.2"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}

# Any results you write to the current directory are saved as output.