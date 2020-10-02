#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.image as mpimg


# look to see where the input data is located

# In[ ]:


dir=r'/kaggle/input/100-bird-species'
dir_list=os.listdir(dir)
print (dir_list)


# Handy routine to print messages in RGB color

# In[ ]:


def print_in_color(txt_msg,fore_tupple,back_tupple,):
    #prints the text_msg in the foreground color specified by fore_tupple with the background specified by back_tupple 
    #text_msg is the text, fore_tupple is foregroud color tupple (r,g,b), back_tupple is background tupple (r,g,b)
    rf,gf,bf=fore_tupple
    rb,gb,bb=back_tupple
    msg='{0}' + txt_msg
    mat='\33[38;2;' + str(rf) +';' + str(gf) + ';' + str(bf) + ';48;2;' + str(rb) + ';' +str(gb) + ';' + str(bb) +'m' 
    print(msg .format(mat))


# Making a listing of the species names, training, test and validation file counts

# In[ ]:




train_dir=r'/kaggle/input/100-bird-species/train'
dir_list=os.listdir(train_dir)
print(len(dir_list))
msg='{0:8s}{1:4s}{2:^35s}{1:4s}{3:11s}{1:3s}{4:10s}{1:3s}{5:11s}{6}'
msg=msg.format('Class Id', ' ', 'Bird Species', 'Train Files','Test Files', 'Valid Files','\n')
print_in_color(msg, (255,0,0), (255,255,255))
species_list= sorted(os.listdir(train_dir))
for i, specie in enumerate (species_list):
    file_path=os.path.join(train_dir,specie)
    train_files_list=os.listdir(file_path)
    train_file_count=str(len(train_files_list))
    msg='{0:^8s}{1:4s}{2:^35s}{1:4s}{3:^11s}{1:3s}{4:^10s}{1:3s}{5:^11s}'
    msg=msg.format(str(i), ' ',specie, train_file_count,'5', '5')
    toggle=i% 2   
    if toggle==0:
        back_color=(255,255,255)
    else:
        back_color=(191, 239, 242)
    print_in_color(msg, (0,0,0), back_color)
#print('\33[0m')


# The code plot plots one image of each specie it takes about 20 seconds to complete

# In[ ]:


test_dir=r'/kaggle/input/100-bird-species/test'
classes=len(os.listdir(test_dir))
fig = plt.figure(figsize=(20,120))
if classes % 5==0:
    rows=int(classes/5)
else:
    rows=int(classes/5) +1
for row in range(rows):
    for column in range(5):
        i= row * 5 + column 
        if i>classes:
            break            
        specie=species_list[i]
        species_path=os.path.join(test_dir, specie)
        f_path=os.path.join(species_path, '1.jpg')        
        img = mpimg.imread(f_path)
        a = fig.add_subplot(rows, 5, i+1)
        imgplot=plt.imshow(img)
        a.axis("off")
        a.set_title(specie)	


# In[ ]:





# In[ ]:




