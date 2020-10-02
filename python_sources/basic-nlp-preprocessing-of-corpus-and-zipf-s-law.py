#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import Counter
import matplotlib.pyplot as plt


# In[ ]:


def read_docu(file):
    
    all_words = []
    
    with open(file, "r", encoding = "utf-8") as input_file:
        for line in input_file:
            line = line.lower()
            line = line.strip().split()
            all_words += line
        return(all_words)


# In[ ]:


def word_counter(all_words):
    
    word_count = Counter()
    for word in all_words:
        word_count[word] += 1
    return(word_count.values())


# In[ ]:


def draw_zipian_curve(word_count):
    plt.plot(sorted(word_count, reverse = True), marker = "o")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("log(Rank)")
    plt.ylabel("log(Frequency)")
    plt.show()


# In[ ]:


def zipian_plot(file):
    word_corpus = read_docu(file)
    counts = word_counter(word_corpus)
    draw_zipian_curve(counts)


# In[ ]:


zipian_plot("../input/jobscommencement.txt")

