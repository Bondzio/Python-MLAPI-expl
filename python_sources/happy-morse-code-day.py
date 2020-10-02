#!/usr/bin/env python
# coding: utf-8

# **<font size="4">.. / .... --- .--. . / -.-- --- ..- / .-- .. .-.. .-.. / . -. .--- --- -.-- / - .... .. ... / -. --- - . -... --- --- -.-</font>**

# <img src = 'https://hamseatingchicken.files.wordpress.com/2017/04/happy-morse-code-day.jpg?w=840'>

# # **Import libraries** 
# ## .. -- .--. --- .-. - / .-.. .. -... .-. .- .-. .. . ...

# In[ ]:


import string
import numpy as np
import pandas as pd


# # **Mapping dictionaries** 
# ## -- .- .--. .--. .. -. --. / -.. .. -.-. - .. --- -. .- .-. .. . ...

# <font color='blue' size='4'>Creating both Morse to Aplhanumeric and Alphanumeric to Morse dictionaries<br><br>-.-. .-. . .- - .. -. --. / -... --- - .... / -- --- .-. ... . / - --- / .- .--. .-.. .... .- -. ..- -- . .-. .. -.-. / .- -. -.. / .- .-.. .--. .... .- -. ..- -- . .-. .. -.-. / - --- / -- --- .-. ... . / -.. .. -.-. - .. --- -. .- .-. .. . ...</font>

# In[ ]:


morse_to_alphanumeric = {'.-':'A','-...':'B','-.-.':'C', '-..':'D','.':'E',
                         '..-.':'F','--.':'G','....':'H','..':'I','.---':'J',
                         '-.-':'K','.-..':'L','--':'M','-.':'N','---':'O',
                         '.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T',
                         '..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z',
                        
                         '.----':'1','..---':'2','...--':'3','....-':'4','.....':'5',
                         '-....':'6','--...':'7','---..':'8','----.':'9','-----':'0',
                        
                         '.-...':'&','.----.':"'",'.--.-.':'@','-.--.-':')','-.--.':'(',
                         '---...':':','--..--':',','-...-':'=','-.-.--':'!','.-.-.-':'.',
                         '-....-':'-','.-.-.':'+','..--..':'?','-..-.':'/'
                        }

alphanumeric_to_morse = {'A':'.-','B':'-...','C':'-.-.', 'D':'-..','E':'.',
                         'F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
                         'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---',
                         'P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
                         'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
                        
                         '1':'.----','2':'..---','3':'...--','4':'....-','5':'.....',
                         '6':'-....','7':'--...','8':'---..','9':'----.','0':'-----',
                        
                         '&':'.-...',"'":'.----.','@':'.--.-.',')':'-.--.-','(':'-.--.',
                         ':':'---...',',':'--..--','=':'-...-','!':'-.-.--','.':'.-.-.-',
                         '-':'-....-','+':'.-.-.','?':'..--..','/':'-..-.'}


# # **Alphanumeric to Morse** 
# ## .- .-.. .--. .... .- -. ..- -- . .-. .. -.-. / - --- / -- --- .-. ... .

# In[ ]:


def preprocess_sentence(sentence):
    '''
    Returns a list of alphanumeric words
    sentence: string (the sentence to be translated)
        Example: sentence = 'Hello, how are you ?'
    '''
    
    assert type(sentence) == str, "Error, Argument 'sentence' is not a string"
    
    upper_sentence = sentence.upper()
    
    for pct in string.punctuation:
        upper_sentence = upper_sentence.replace(pct, "")
        
    words = [elm.replace(" ","") for elm in upper_sentence.split()]
    
    return words

def get_morse_words(words):
    '''
    Returns the list of morse words
    words: list of alphanumeric words
        Example: words = ['HELLO', 'HOW', 'ARE', 'YOU']
    '''

    assert type(words) == list, "Error, Argument 'words' is not a list"
    for word in words:
        assert type(word) == str, "Error, At least one word is not a string"
    
    new_words = []
    for word in words:
        new_word = ''
        for letter in word:
            new_word += ' '+str(np.vectorize(alphanumeric_to_morse.get)(letter))
        new_words.append(new_word.lstrip())
        
    return new_words

def get_morse_sentence(list_of_morse_words):
    '''
    Returns the aggregated string of morse words
    list_of_morse_words: list of morse words
        Example: list_of_morse_words = ['.... . .-.. .-.. ---', '.... --- .--', '.- .-. .', '-.-- --- ..-']
    '''
    
    assert type(list_of_morse_words) == list, "Error, Argument 'list_of_morse_words' is not a list"
    for morse_word in list_of_morse_words:
        assert type(morse_word) == str, "Error, At least one word is not a string"
        
    new_translated_sentence = ''
    for i in list_of_morse_words:
        if list_of_morse_words[-1] != i:
            new_translated_sentence += i + ' / '
        else:
            new_translated_sentence += i
            
    return new_translated_sentence


# In[ ]:


def translation_to_morse(sentence, verbose=0):
    '''
    Return translation of sentence in morse code
    sentence: the string to be translated
    verbose: boolean (1 for verbose, 0 otherwise)
        Example: sentence = 'Hello, how are you ?', verbose=1
    '''
    
    assert type(sentence) == str, "Error, Argument 'sentence' is not a string"
    
    words = preprocess_sentence(sentence)
    if verbose==1:
        print('List of Alphanumeric words: ',words)
        print('Step 1 out of 3 completed\n')
        
    translated_sentence = get_morse_words(words)
    if verbose==1:
        print('List of Morse words: ',translated_sentence)
        print('Step 2 out of 3 completed\n')
        
    result = get_morse_sentence(translated_sentence)
    if verbose==1:
        print('Translated sentence: ', result)
        print('Step 3 out of 3 completed\n')
        
    print('Execution Successful')
    return result


# <font color='blue' size='4'>Example<br><br>. -..- .- -- .--. .-.. .</font>

# In[ ]:


sentence = 'Hello, how are you'
translation_to_morse(sentence, verbose=1)


# # **Morse to Alphanumeric** 
# ## -- --- .-. ... . / - --- / .- .-.. .--. .... .- -. ..- -- . .-. .. -.-.

# In[ ]:


def translation_to_alphanumeric(sentence, verbose=0):
    
    assert type(sentence) == str, "Error, Argument 'sentence' is not a string"
    
    words = sentence.split('/')
    words = [word.lstrip().rstrip().split(' ') for word in words]
    if verbose==1:
        print('List of Morse words: ',words)
        print('Step 1 out of 3 completed\n')
        
    alpha_words = []
    for word in words:
        alpha_word = ''
        for morse_letter in word:
            alpha_word += str(np.vectorize(morse_to_alphanumeric.get)(morse_letter))
        alpha_words.append(alpha_word)
    if verbose==1:
        print('List of Alphanumeric words: ',alpha_words)
        print('Step 2 out of 3 completed\n')
        
    result = ''
    for elm in alpha_words:
        result+=' '+elm
    if verbose==1:
        print('Translated sentence sentence: ',result.lstrip())
        print('Step 3 out of 3 completed\n')
        
    print('Execution Successful')
    return result.lstrip()


# <font color='blue' size='4'>Example<br><br>. -..- .- -- .--. .-.. .</font>
# 

# In[ ]:


sentence = '.... .- .--. .--. -.-- / -- --- .-. ... . / -.-. --- -.. . / -.. .- -.--'
translation_to_alphanumeric(sentence, verbose=1)


# # **With Pandas**
# ## .-- .. - .... / .--. .- -. -.. .- ...

# <font color='blue' size='4'>Creating dataframe<br><br>-.-. .-. . .- - .. -. --. / -.. .- - .- ..-. .-. .- -- .</font>

# In[ ]:


data = {'index':np.arange(4),'Alphanumeric_Sentences':['Hello, how are you ?', "What's up ?", 'I want to read more data science articles !', 'Happy morse code day']}
df = pd.DataFrame(data)


# <font color='blue' size='4'>Applying previous converters on the dataframe<br><br>.- .--. .--. .-.. -.-- .. -. --. / .--. .-. . ...- .. --- ..- ... / -.-. --- -. ...- . .-. - . .-. ... / --- -. / - .... . / -.. .- - .- ..-. .-. .- -- .</font>

# In[ ]:


df['Alphanumeric_to_Morse'] = df['Alphanumeric_Sentences'].apply(translation_to_morse)
df['Morse_to_Alphanumeric'] = df['Alphanumeric_to_Morse'].apply(translation_to_alphanumeric)


# <font color='blue' size='4'>Results<br><br>.-. . ... ..- .-.. - ...</font>

# In[ ]:


df.head()


# # **References** 
# ## .-. . ..-. . .-. . -. -.-. . ...
# 
# * https://morsecode.world/international/morse.html
# 
# * https://www.daysoftheyear.com/days/morse-code-day/

# <font color='red' size='4'>Thank you for taking the time to read this notebook. I hope that I was able to answer your questions or your curiosity and that it was quite understandable. If you liked this notebook, please upvote it. I will really appreciate and this will motivate me to make more and better content !</font>

# **<font color="red" size="4">- .... .- -. -.- / -.-- --- ..- / ..-. --- .-. / - .- -.- .. -. --. / - .... . / - .. -- . / - --- / .-. . .- -.. / - .... .. ... / -. --- - . -... --- --- -.- / .. / .... --- .--. . / - .... .- - / .. / .-- .- ... / .- -... .-.. . / - --- / .- -. ... .-- . .-. / -.-- --- ..- .-. / --.- ..- . ... - .. --- -. ... / --- .-. / -.-- --- ..- .-. / -.-. ..- .-. .. --- ... .. - -.-- / .- -. -.. / - .... .- - / .. - / .-- .- ... / --.- ..- .. - . / ..- -. -.. . .-. ... - .- -. -.. .- -... .-.. . / .. ..-. / -.-- --- ..- / .-.. .. -.- . -.. / - .... .. ... / - . -..- - / .--. .-.. . .- ... . / ..- .--. ...- --- - . / .. - / .. / .-- .. .-.. .-.. / .-. . .- .-.. .-.. -.-- / .- .--. .--. .-. . -.-. .. .- - . / .- -. -.. / - .... .. ... / .-- .. .-.. .-.. / -- --- - .. ...- .- - . / -- . / - --- / -- .- -.- . / -- --- .-. . / .- -. -.. / -... . - - . .-. / -.-. --- -. - . -. -</font>**
