# Copyright 2011 Hugo Larochelle. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Hugo Larochelle ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Hugo Larochelle OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Hugo Larochelle.

"""
Module ``datasets.face_completion_lfw`` gives access to the Labeled
Faces in the Wild, occluded faces dataset.

This is a multi-dimensional regression dataset, with outputs in [0,1].
The task is to remove occlusions from images of faces. The occlusions
were generated by overlapping random characters on the image. The
characters were obtained from the OCR letters dataset (see
``datasets.ocr_letters``).

The original dataset, Labeled Faces in the Wild comes from
http://vis-www.cs.umass.edu/lfw/. 

| **References:**
| Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments.
| Huang, Ramesh, Berg and Learned-Miller
| http://vis-www.cs.umass.edu/lfw/

"""

import mlpython.misc.io as mlio
import numpy as np
import os
from gzip import GzipFile as gfile

def load(dir_path,load_to_memory=False):
    """
    Labeled Faces in the Wild, occluded faces dataset.

    The data is given by a dictionary mapping from strings
    ``'train'``, ``'valid'`` and ``'test'`` to the associated pair of data and metadata.
    
    The inputs and targets have been converted to be in the [0,1] interval.

    **Defined metadata:**

    * ``'input_size'``
    * ``'target_size'``
    * ``'length'``

    """
    
    input_size=1024
    target_size=1024
    dir_path = os.path.expanduser(dir_path)

    def load_line(line):
        tokens = line.split()
        return (np.array([float(i)/255 for i in tokens[:input_size]]), np.array([float(i)/255 for i in tokens[input_size:]]))

    train_file,valid_file,test_file = [os.path.join(dir_path, 'occluded_faces_lfw_' + ds + '.txt') for ds in ['train','valid','test']]
    # Get data
    train,valid,test = [mlio.load_from_file(f,load_line) for f in [train_file,valid_file,test_file]]

    lengths = [11089,1149,1117]
    if load_to_memory:
        train,valid,test = [mlio.MemoryDataset(d,[(input_size,),(target_size,)],[np.float64,np.float64],l) for d,l in zip([train,valid,test],lengths)]
        
    # Get metadata
    train_meta,valid_meta,test_meta = [{'input_size':input_size,'target_size':target_size,
                                        'length':l} for l in lengths]
    
    return {'train':(train,train_meta),'valid':(valid,valid_meta),'test':(test,test_meta)}


def obtain(dir_path):
    """
    Downloads the dataset to ``dir_path``.
    """

    dir_path = os.path.expanduser(dir_path)
    print 'Downloading the dataset'
    import urllib
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/occluded_faces_train.mat',os.path.join(dir_path,'occluded_faces_train.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/faces_train.mat',os.path.join(dir_path,'faces_train.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/occluded_faces_valid.mat',os.path.join(dir_path,'occluded_faces_valid.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/faces_valid.mat',os.path.join(dir_path,'faces_valid.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/occluded_faces_test.mat',os.path.join(dir_path,'occluded_faces_test.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/occluded_faces_lfw/faces_test.mat',os.path.join(dir_path,'faces_test.mat'))

    # Writing everything into text files, to allow for not loading the data into memory
    def write_to_txt_file(u,v,filename):
        f = open(filename,'w')
        for u_t,v_t in zip(u,v):
            for i in range(len(u_t)):
                f.write(str(int(u_t[i]))+' ')
            for i in range(len(v_t)-1):
                f.write(str(int(v_t[i]))+' ')
            f.write(str(int(v_t[-1]))+'\n')
        f.close()

    import scipy.io
    u = scipy.io.loadmat(os.path.join(dir_path,'occluded_faces_train.mat'))['mat']
    v = scipy.io.loadmat(os.path.join(dir_path,'faces_train.mat'))['mat']
    write_to_txt_file(u,v,os.path.join(dir_path,'occluded_faces_lfw_train.txt'))

    u = scipy.io.loadmat(os.path.join(dir_path,'occluded_faces_valid.mat'))['mat']
    v = scipy.io.loadmat(os.path.join(dir_path,'faces_valid.mat'))['mat']
    write_to_txt_file(u,v,os.path.join(dir_path,'occluded_faces_lfw_valid.txt'))

    u = scipy.io.loadmat(os.path.join(dir_path,'occluded_faces_test.mat'))['mat']
    v = scipy.io.loadmat(os.path.join(dir_path,'faces_test.mat'))['mat']
    write_to_txt_file(u,v,os.path.join(dir_path,'occluded_faces_lfw_test.txt'))

    print 'Done                     '
