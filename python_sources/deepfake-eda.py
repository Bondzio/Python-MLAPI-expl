#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.set_option('display.max_colwidth', -1)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
import json
from collections import defaultdict
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().system('pip install /kaggle/input/mtcnn-package/mtcnn-0.1.0-py3-none-any.whl;')
from mtcnn import MTCNN
from skimage.metrics import structural_similarity


# ## Train/Test Split Ratio in Public Validation Set

# In[ ]:


train_files, test_files = [], []
train_exts, test_exts = defaultdict(int), defaultdict(int)

for dirname, _, filenames in os.walk('/kaggle/input/deepfake-detection-challenge/'):
    for filename in filenames:
        if ('train' in dirname):
            train_exts[filename.split('.')[1]] += 1
            train_files.append(os.path.join(dirname, filename))
        elif ('test' in dirname):
            test_exts[filename.split('.')[1]] += 1
            test_files.append(os.path.join(dirname, filename))

print(f'we have {train_exts["mp4"]} training samples: {train_exts.items()}')
print(f'we have {test_exts["mp4"]} testing samples: {test_exts.items()}')

train_files = sorted(train_files)
test_files = sorted(test_files)


# In[ ]:


metadata_df = pd.read_json('/kaggle/input/deepfake-detection-challenge/train_sample_videos/metadata.json').T
display(metadata_df.head())
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = [f'{k} ({metadata_df["label"].value_counts()[k]} samples)' for k in metadata_df['label'].value_counts().keys()]
sizes = dict(metadata_df['label'].value_counts()).values()
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# In[ ]:


print(f'metadata.json has the ground truth for all the {metadata_df.shape[0]} training video samples.')


# ## Check if we have corresponding original videos of fakes

# for all fake videos,```metadata.json``` has a reference to its corresponding original video.  
# Lets check if we have those original videos with us(included in the public validation set)

# In[ ]:


reference_to_original_list=[item for item in metadata_df['original'].tolist() if item]
reference_to_original_set=set(reference_to_original_list)
train_videos_list=set(metadata_df.index)
intersect_list=list(reference_to_original_set.intersection(train_videos_list))
print(f'train_videos_list:{len(train_videos_list)}, reference_to_original_list:{len(reference_to_original_list)}, reference_to_original_set:{len(reference_to_original_set)}, intersect_list:{len(intersect_list)}')


# Here, ```train_videos_list``` is the list of all the videos in public validation set,  
# ```reference_to_original_set``` is a list of all the unique original videos used to create the fake ones,  
# and ```intersect_list``` is a list of videos found in ```reference_to_original_set``` which exists in ```train_videos_list```

# In[ ]:


orig_to_fake = metadata_df[metadata_df["original"].isin(intersect_list)].reset_index().set_index('original').rename(columns={'index':'fakes'})["fakes"]
display(orig_to_fake.groupby('original').apply(list).to_frame().head())
display(orig_to_fake.groupby('original').apply(list).apply(lambda x : len(x)).to_frame().rename(columns={'fakes':'length(fakes)'}).head())


# lets try to see the original video and their fake counterparts side by side maybe also zooming in on the faces as done in [this notebook](https://www.kaggle.com/aleksandradeis/deepfake-challenge-eda/notebook) by [aleksandradeis](https://www.kaggle.com/aleksandradeis)

# ## Explore the Differences/Similaries b/w fake and real videos

# ### Understanding Haar CascadeClassifier (Viola Jones Face detection Algorithm)  
# 
# Its better to know firsthand how the face detection works in general since it will be a major part of our overall workflow leading to the detection of deepfakes.  
# I recommend reading/watching below contents mainly because its absolute beauty IMHO.  
# [Face Detection using Haar Cascades](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html)  
# [Detecting Faces (Viola Jones Algorithm) - Computerphile](https://www.youtube.com/watch?v=uEJ71VlUmMQ)   
# [Viola Jones face detection and tracking explained](https://www.youtube.com/watch?v=WfdYYNamHZ8)  

# In[ ]:


def get_label(filename):
    return metadata_df.loc[filename.split('/')[-1]].label

def get_videoid(filename):
    return filename.split('/')[-1]

def get_first_frame(filename):
    fig,ax = plt.subplots(1,3,figsize=(20,7))
    
    cap = cv2.VideoCapture(filename)
    ret,frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    cv2.destroyAllWindows()
    ax[0].axis('off')
    ax[0].set_title(f'{get_videoid(filename)} - {get_label(filename)}')
    ax[0].imshow(image)
    
    hcascade = cv2.CascadeClassifier('/kaggle/input/haarcascades/haarcascade_frontalface_default.xml')
    face = hcascade.detectMultiScale(image,1.2,3)
    
    img_copy = image.copy()
    for (x,y,w,h) in face:
        cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),3)
        break;
    
    ax[1].axis('off')
    ax[1].set_title(f'highlight face')
    ax[1].imshow(img_copy)
    
    face_crop = image.copy()
    for (x,y,w,h) in face:
        face_crop = image[y:y+h,x:x+w]
        break; #to get just the first detection
    
    ax[2].axis('off')
    ax[2].set_title(f'face cropped')
    ax[2].imshow(face_crop)


# ### Viewing first frame of a few videos (do note the image label(real/fake) in the title)

# In[ ]:


get_first_frame(train_files[0])


# In[ ]:


get_first_frame(train_files[4])


# In[ ]:


get_first_frame(train_files[11])


# In[ ]:


get_first_frame(train_files[14])


# till now we seen samples of fake videos, below one is of a real one

# In[ ]:


get_first_frame(train_files[13])


# In[ ]:


def get_filename(video_id,train=True):
    if train:
        return f'/kaggle/input/deepfake-detection-challenge/train_sample_videos/{video_id}'
    else:
        return f'/kaggle/input/deepfake-detection-challenge/test_videos/{video_id}'

def get_face_crop(filename):
    cap = cv2.VideoCapture(filename)
    ret,frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    cv2.destroyAllWindows()
    hcascade = cv2.CascadeClassifier('/kaggle/input/haarcascades/haarcascade_frontalface_default.xml')
    face = hcascade.detectMultiScale(image,1.2,3)
    face_crop = image.copy()
    for (x,y,w,h) in face:
        face_crop = image[y:y+h,x:x+w]
        break; #to get just the first detection
    return face_crop

def compare_orig_to_fakes(orig,fake_files):
    if(len(fake_files)<=2):
        fig,ax = plt.subplots(1,len(fake_files)+1,figsize=(20,7))
        face_crop = get_face_crop(get_filename(orig))
        ax[0].axis('off')
        ax[0].set_title(f'face cropped(real) - {orig}')
        ax[0].imshow(face_crop)
    
        for i in range(len(fake_files)):
            face_crop = get_face_crop(get_filename(fake_files[i]))
            ax[i+1].axis('off')
            ax[i+1].set_title(f'face cropped (fake) - {fake_files[i]}')
            ax[i+1].imshow(face_crop)
    else:
        fig,ax = plt.subplots(int(len(fake_files)/2)+1,2,figsize=(20,7*int(len(fake_files)/2)))
        face_crop = get_face_crop(get_filename(orig))
        ax[0,0].axis('off')
        ax[0,0].set_title(f'face cropped(real) - {orig}')
        ax[0,0].imshow(face_crop)
    
        for i in range(1,len(fake_files)+1):
            face_crop = get_face_crop(get_filename(fake_files[i-1]))
            ax[int(i-(i/2)),i%2].axis('off')
            ax[int(i-(i/2)),i%2].set_title(f'face cropped (fake) - {fake_files[i-1]}')
            ax[int(i-(i/2)),i%2].imshow(face_crop)
        
        if(len(fake_files)%2==0):
            ax[int(len(fake_files)/2),1].axis('off')


# ### Viewing Original and their corresponsing Fake videos side by side

# In[ ]:


orig_to_fake.groupby('original').apply(list).to_frame().iloc[:10].reset_index().apply(lambda row : compare_orig_to_fakes(row['original'],row['fakes']),axis=1);


# as we can see above some faces are not being recognized by haar cascadeclassifier(since we didnt get a zoomed version - see 1st and last set above) and some are misidentified as faces(see 5th set).  
# need to find some other method to detect faces.  lets try mtcnn method as suggested [here](https://www.kaggle.com/aleksandradeis/deepfake-challenge-eda/notebook).  

# In[ ]:


def get_first_frame_mtcnn(filename):
    fig,ax = plt.subplots(1,3,figsize=(20,7))
    
    cap = cv2.VideoCapture(filename)
    ret,frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    cv2.destroyAllWindows()
    ax[0].axis('off')
    ax[0].set_title(f'{get_videoid(filename)} - {get_label(filename)}')
    ax[0].imshow(image)
    
    detector = MTCNN()
    mtcnn_op = detector.detect_faces(image)
    
    img_copy = image.copy()
    for boxes in mtcnn_op:
        x,y,w,h = boxes['box']
        cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),3)
    
    ax[1].axis('off')
    ax[1].set_title(f'highlight face')
    ax[1].imshow(img_copy)
    
    face_crop = image.copy()
    for boxes in mtcnn_op:
        x,y,w,h = boxes['box']
        face_crop = image[y:y+h,x:x+w]
        break; #to get just the first detection
    
    ax[2].axis('off')
    ax[2].set_title(f'face cropped')
    ax[2].imshow(face_crop)


# In[ ]:


get_first_frame_mtcnn(train_files[0])


# In[ ]:


get_first_frame_mtcnn(train_files[4])


# In[ ]:


get_first_frame_mtcnn(train_files[11])


# In[ ]:


get_first_frame_mtcnn(train_files[14])


# In[ ]:


get_first_frame_mtcnn(train_files[13])


# In[ ]:


def get_face_crop_mtcnn(filename):
    cap = cv2.VideoCapture(filename)
    ret,frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()
    cv2.destroyAllWindows()
    
    detector = MTCNN()
    mtcnn_op = detector.detect_faces(image)    
        
    face_crop = image.copy()
    for boxes in mtcnn_op:
        x,y,w,h = boxes['box']
        face_crop = image[y:y+h,x:x+w]
        break; #to get just the first detection
    return face_crop

def compare_orig_to_fakes_mtcnn(orig,fake_files):
    if(len(fake_files)<=2):
        fig,ax = plt.subplots(1,len(fake_files)+1,figsize=(20,7))
        face_crop = get_face_crop_mtcnn(get_filename(orig))
        ax[0].axis('off')
        ax[0].set_title(f'face cropped(real) - {orig}')
        ax[0].imshow(face_crop)
    
        for i in range(len(fake_files)):
            face_crop = get_face_crop_mtcnn(get_filename(fake_files[i]))
            ax[i+1].axis('off')
            ax[i+1].set_title(f'face cropped (fake) - {fake_files[i]}')
            ax[i+1].imshow(face_crop)
    else:
        fig,ax = plt.subplots(int(len(fake_files)/2)+1,2,figsize=(20,7*int(len(fake_files)/2)))
        face_crop = get_face_crop_mtcnn(get_filename(orig))
        ax[0,0].axis('off')
        ax[0,0].set_title(f'face cropped(real) - {orig}')
        ax[0,0].imshow(face_crop)
    
        for i in range(1,len(fake_files)+1):
            face_crop = get_face_crop_mtcnn(get_filename(fake_files[i-1]))
            ax[int(i-(i/2)),i%2].axis('off')
            ax[int(i-(i/2)),i%2].set_title(f'face cropped (fake) - {fake_files[i-1]}')
            ax[int(i-(i/2)),i%2].imshow(face_crop)
        
        if(len(fake_files)%2==0):
            ax[int(len(fake_files)/2),1].axis('off')


# In[ ]:


orig_to_fake.groupby('original').apply(list).to_frame().iloc[:10].reset_index().apply(lambda row : compare_orig_to_fakes_mtcnn(row['original'],row['fakes']),axis=1);


# as you can see mtcnn is able to fill the gaps in haarcascade classifier by detecting the faces in 1st and the last set.  
# The face in the 5th set is somehow identifiable as a face(as a human) which was missed by haarcascade classifier.  
# Although it fails for the 4th set as before.  
# Maybe we can try even more face detection methods, possibly dlib.  
# More on that [here](https://www.kaggle.com/timesler/comparison-of-face-detection-packages)

# In[ ]:


def get_frames(filename,zoomed=False,interval=100):
    frames = []
    cap = cv2.VideoCapture(filename)
    detector = MTCNN()
    frame_n = 0
    while(cap.isOpened()):
        ret,frame = cap.read() #ret is a boolean variable that returns true if the frame is available
        
        if not frame_n%interval:
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if zoomed:
                mtcnn_op = detector.detect_faces(image)
                face_crop = image.copy()
                for boxes in mtcnn_op:
                    x,y,w,h = boxes['box']
                    face_crop = image[y:y+h,x:x+w]
                    frames.append(face_crop)
                    break; #to get just the first detection
            else:
                frames.append(image)

        frame_n += 1
        
    cap.release()
    cv2.destroyAllWindows()
    return frames

def visualize_frames(filename, zoomed=False, interval=100, cols=2, title=''):
    frames = get_frames(filename, zoomed=zoomed, interval=interval)
    n_frames = len(frames)
    rows = n_frames // cols
    if n_frames % cols:
        rows = rows + 1
    fig,axis = plt.subplots(rows,cols,figsize=(20,7*rows))
    for i in range(n_frames):
        r = i // cols
        c = i % cols
        if n_frames <= cols:
            axis[c].imshow(frames[i])
            axis[c].axis('off')
            axis[c].set_title(str(i))
        else:
            axis[r,c].imshow(frames[i])
            axis[r,c].axis('off')
            axis[r,c].set_title(str(i))
    
    if(n_frames%cols):
        for i in range(n_frames%cols,cols):
            for i in range(n_frames%cols,cols):
                if n_frames <= cols:
                    axis[i].axis('off')
                else:
                    axis[n_frames//cols,i].axis('off')
    
    plt.suptitle(f'{get_videoid(filename)} {("(zoomed)") if zoomed else ""}' if title=='' else title)
    plt.show()


# ## Visualizing sequences of frames of a few videos  
# having explored the first frame of each video, lets explore the sequential frames

# In[ ]:


visualize_frames(train_files[0],interval=50)
visualize_frames(train_files[0],interval=50,zoomed=True)


# In[ ]:


def get_frames_alongwith_faces(filename, interval=100):
    frames = []
    frames_no = []
    cap = cv2.VideoCapture(filename)
    detector = MTCNN()
    frame_n = 0
    while(cap.isOpened()):
        ret,frame = cap.read() #ret is a boolean variable that returns true if the frame is available
        
        if not frame_n%interval:
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(image)
            frames_no.append(frame_n)
            mtcnn_op = detector.detect_faces(image)
            face_crop = image.copy()
            for boxes in mtcnn_op:
                x,y,w,h = boxes['box']
                face_crop = image[y:y+h,x:x+w]
                frames.append(face_crop)
                frames_no.append(frame_n)
                break; #to get just the first detection
        frame_n += 1
        
    cap.release()
    cv2.destroyAllWindows()
    return frames,frames_no

def visualize_frames_alongside_faces(filename, interval=100, cols=2, title=''):
    frames,frames_no = get_frames_alongwith_faces(filename, interval=interval)
    n_frames = len(frames)
    rows = n_frames // cols
    if n_frames % cols:
        rows = rows + 1
    fig,axis = plt.subplots(rows,cols,figsize=(20,6*rows))
    for i in range(n_frames):
        r = i // cols
        c = i % cols
        axis[r,c].imshow(frames[i])
        axis[r,c].axis('off')
        axis[r,c].set_title(f'frame #{frames_no[i]}' if c==0 else f'frame #{frames_no[i]} (zoomed)')
    
    if(n_frames%cols):
        for i in range(n_frames%cols,cols):
            axis[n_frames//cols,i].axis('off')
    
    plt.suptitle(f'{get_videoid(filename)}' if title=='' else title)
    plt.show()


# In[ ]:


visualize_frames_alongside_faces(train_files[0],interval=50)


# In[ ]:


def get_faces(filename):
    frames = []
    frames_no = []
    cap = cv2.VideoCapture(filename)
    detector = MTCNN()
    frame_n = 0
    while(cap.isOpened()):
        ret,frame = cap.read() #ret is a boolean variable that returns true if the frame is available
        
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mtcnn_op = detector.detect_faces(image)
        face_crop = image.copy()
        for boxes in mtcnn_op:
            x,y,w,h = boxes['box']
            face_crop = image[y:y+h,x:x+w]
            frames.append(face_crop)
            frames_no.append(frame_n)
            break; #to get just the first detection
        frame_n += 1
        
    cap.release()
    cv2.destroyAllWindows()
    return frames,frames_no

def animate_frames(filename):
    frames,_ = get_faces(filename)
    fig = plt.figure(figsize=(16,9))
    
    def update(frame_number):
        plt.axis('off')
        plt.imshow(frames[frame_number])

    return FuncAnimation(fig, update, interval=30, repeat=True)


# ## Animating the sequences of frames (with just faces extracted)

# In[ ]:


animation = animate_frames(train_files[0])
HTML(animation.to_jshtml())


# In[ ]:


def get_ssim_score(frame_a,frame_b,get_str_sim_image=False):
    """
    Compute the mean structural similarity index between two images.
    """
    if frame_a.shape[0] != frame_b.shape[0]: #resizing height on mismatch
        if frame_a.shape[0] < frame_b.shape[0]:
            frame_b = frame_b[:frame_a.shape[0],:,:]
        else:
            frame_a = frame_a[:frame_b.shape[0],:,:]

    if frame_a.shape[1] != frame_b.shape[1]: #resizing width on mismatch
        if frame_a.shape[1] < frame_b.shape[1]:
            frame_b = frame_b[:,:frame_a.shape[1],:]
        else:
            frame_a = frame_a[:,:frame_b.shape[1],:]
    
    if get_str_sim_image:
        (score,image)=structural_similarity(frame_a,frame_b,multichannel=True, full=True) #image has full structural similarity image
        return score,image
    else:
        return structural_similarity(frame_a,frame_b,multichannel=True)

def get_frames_similarity_scores(filename, zoomed=False, interval=10):
    frames = get_frames(filename, zoomed=zoomed, interval=interval)
    print(len(frames),"frames")
    scores = []
    for i in range(1,len(frames)):
        frame = frames[i]
        prev_frame = frames[i-1]
        score = get_ssim_score(frame,prev_frame)
        # score,image=get_ssim_score(frame,prev_frame,get_str_sim_image=True) #image has full structural similarity image
        scores.append(score)
    return scores,frames

def plot_scores(scores,title=""):
    plt.figure(figsize=(12,7))
    plt.plot(scores)
    plt.title(f"Similarity Scores ({title})")
    plt.show()


# ## Plotting the structural similarity scores of 2 consecutive frames for all the frames of the video  
# lets plot the scores of just the face part zoomed in first. 

# In[ ]:


(scores_fake_face,frames_fake_face) = get_frames_similarity_scores(get_filename(orig_to_fake.reset_index().iloc[5]['fakes']), zoomed=True, interval=2)
plot_scores(scores_fake_face,"fake face")


# since it doesn't give a clear picture of the similarities b/w frame as there is noise in it (a possible explanation of this noise is because if we play the face extracted parts as a video it's not stabilized meaning the face parts extracted by mtcnn from each frame has some irregularities as far as the location from where it extracted is concerned and is not consistent - eg. tip of the left eye may be a few pixels off in the next consecutive frame), lets try plotting for the images as is(without face extraction).

# In[ ]:


(scores_fake,frames_fake) = get_frames_similarity_scores(get_filename(orig_to_fake.reset_index().iloc[5]['fakes']), interval=1)
plot_scores(scores_fake,"fake")


# In[ ]:


(scores_real,frames_real) = get_frames_similarity_scores(get_filename(orig_to_fake.reset_index().iloc[5]['original']), interval=1)
plot_scores(scores_real,"real")


# In[ ]:


plt.figure(figsize=(12,7))
plt.plot(scores_fake, label = 'fake', color='red')
plt.plot(scores_real, label = 'real', color='g')
plt.title("Similarity Scores (fake vs real)")
plt.legend()
plt.show()


# Comparing them there's hardly any major difference probably because "fake" part is just on the face and face constitutes a very small area in the entire image. But remember if we just take the face part, it adds to the noise due to unstabilized aspect of extracted frames?

# ## Visualizing the frames where there is a drop in the similarity score

# In[ ]:


def visualize_faces(frames, cols=3):
    n_frames = len(frames)
    rows = n_frames // cols
    if n_frames % cols:
        rows = rows + 1
    fig,axis = plt.subplots(rows,cols,figsize=(20,7*rows))
    for i in range(n_frames):
        r = i // cols
        c = i % cols
        if n_frames <= cols:
            axis[c].imshow(frames[i])
            axis[c].axis('off')
        else:
            axis[r,c].imshow(frames[i])
            axis[r,c].axis('off')
    
    if(n_frames%cols):
        for i in range(n_frames%cols,cols):
            if n_frames <= cols:
                axis[i].axis('off')
            else:
                axis[n_frames//cols,i].axis('off')
    
    plt.show()


# ## Credits where its due:
# [Aleksandra Deis](https://www.kaggle.com/aleksandradeis) for [this notebook](https://www.kaggle.com/aleksandradeis/deepfake-challenge-eda/notebook) : took most of the idea and references from here, added upon it things like face detection using mtcnn where it lacked.
