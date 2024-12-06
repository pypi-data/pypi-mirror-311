# Written by Dr Daniel Buscombe, Marda Science LLC
# for  the USGS Coastal Change Hazards Program
#
# MIT License
#
# Copyright (c) 2021-23, Marda Science LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE zSOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .imports import standardize, label_to_colors, fromhex

import os,gc 
import numpy as np
import matplotlib.pyplot as plt
from scipy import io
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import json
from skimage.io import imsave, imread
from numpy.lib.stride_tricks import as_strided as ast
from glob import glob
from skimage.transform import resize
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

import tensorflow as tf  # numerical operations on gpu
import tensorflow.keras.backend as K


SEED = 42
np.random.seed(SEED)
AUTO = tf.data.experimental.AUTOTUNE  # used in tf.data.Dataset API

tf.random.set_seed(SEED)

##========================================================
def rescale(dat,
    mn,
    mx):
    '''
    rescales an input dat between mn and mx
    '''
    m = min(dat.flatten())
    M = max(dat.flatten())
    return (mx-mn)*(dat-m)/(M-m)+mn

# #-----------------------------------
def seg_file2tensor_ND(f, TARGET_SIZE):  
    """
    "seg_file2tensor(f)"
    This function reads a NPZ image from file into a cropped and resized tensor,
    for use in prediction with a trained segmentation model
    INPUTS:
        * f [string] file name of npz
    OPTIONAL INPUTS: None
    OUTPUTS:
        * image [tensor array]: unstandardized image
    GLOBAL INPUTS: TARGET_SIZE
    """

    with np.load(f) as data:
        bigimage = data["arr_0"].astype("uint8")

    smallimage = resize(
        bigimage, (TARGET_SIZE[0], TARGET_SIZE[1]), preserve_range=True, clip=True
    )
    smallimage = np.array(smallimage)
    smallimage = tf.cast(smallimage, tf.uint8)

    w = tf.shape(bigimage)[0]
    h = tf.shape(bigimage)[1]

    return smallimage, w, h, bigimage


# #-----------------------------------
def seg_file2tensor_3band(f, TARGET_SIZE):  
    """
    "seg_file2tensor(f)"
    This function reads a jpeg image from file into a cropped and resized tensor,
    for use in prediction with a trained segmentation model
    INPUTS:
        * f [string] file name of jpeg
    OPTIONAL INPUTS: None
    OUTPUTS:
        * image [tensor array]: unstandardized image
    GLOBAL INPUTS: TARGET_SIZE
    """

    bigimage = imread(f)  
    smallimage = resize(
        bigimage, (TARGET_SIZE[0], TARGET_SIZE[1]), preserve_range=True, clip=True
    )
    smallimage = np.array(smallimage)
    smallimage = tf.cast(smallimage, tf.uint8)

    w = tf.shape(bigimage)[0]
    h = tf.shape(bigimage)[1]

    return smallimage, w, h, bigimage

# =========================================================
def compile_models(M, MODEL):
    Mc = []
    for m in M:
        if MODEL=='segformer':
            m.compile(optimizer='adam', loss=None)
        else:
            m.compile(optimizer='adam')
        Mc.append(m)
    return Mc


# #-----------------------------------
def get_image(f,N_DATA_BANDS,TARGET_SIZE,MODEL):
    if N_DATA_BANDS <= 3:
        image, w, h, bigimage = seg_file2tensor_3band(f, TARGET_SIZE)
    else:
        image, w, h, bigimage = seg_file2tensor_ND(f, TARGET_SIZE)

    try: ##>3 bands
        if N_DATA_BANDS<=3:
            if image.shape[-1]>3:
                image = image[:,:,:3]

            if bigimage.shape[-1]>3:
                bigimage = bigimage[:,:,:3]
    except:
        pass

    image = standardize(image.numpy()).squeeze()

    if MODEL=='segformer':
        if np.ndim(image)==2:
            image = np.dstack((image, image, image))
        image = tf.transpose(image, (2, 0, 1))

    return image, w, h, bigimage 


# #-----------------------------------
def est_label_multiclass(image,M,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE):

    est_label = np.zeros((TARGET_SIZE[0], TARGET_SIZE[1], NCLASSES))
    
    for counter, model in enumerate(M):
        # heatmap = make_gradcam_heatmap(tf.expand_dims(image, 0) , model)
        try:
            if MODEL=='segformer':
                est_label = model(tf.expand_dims(image, 0)).logits
            else:
                est_label = tf.squeeze(model(tf.expand_dims(image, 0)))
        except:
            if MODEL=='segformer':
                est_label = model(tf.expand_dims(image[:,:,:3], 0)).logits
            else:
                est_label = tf.squeeze(model(tf.expand_dims(image[:,:,:3], 0)))

        if TESTTIMEAUG == True:
            # return the flipped prediction
            if MODEL=='segformer':
                est_label2 = np.flipud(
                    model(tf.expand_dims(np.flipud(image), 0)).logits
                    )                
            else:
                est_label2 = np.flipud(
                    tf.squeeze(model(tf.expand_dims(np.flipud(image), 0)))
                    )
            if MODEL=='segformer':

                est_label3 = np.fliplr(
                    model(
                        tf.expand_dims(np.fliplr(image), 0)).logits
                        )                
            else:
                est_label3 = np.fliplr(
                    tf.squeeze(model(tf.expand_dims(np.fliplr(image), 0)))
                )                
            if MODEL=='segformer':
                est_label4 = np.flipud(
                    np.fliplr(
                        tf.squeeze(model(tf.expand_dims(np.flipud(np.fliplr(image)), 0)).logits))
                )                
            else:
                est_label4 = np.flipud(
                    np.fliplr(
                        tf.squeeze(model(
                            tf.expand_dims(np.flipud(np.fliplr(image)), 0)))
                            ))
                
            # soft voting - sum the softmax scores to return the new TTA estimated softmax scores
            est_label = est_label + est_label2 + est_label3 + est_label4

        K.clear_session()

    # heatmap = resize(heatmap,(w,h), preserve_range=True, clip=True)
    return est_label, counter


# #-----------------------------------
def est_label_binary(image,M,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE,w,h):

    E0 = []
    E1 = []

    for counter, model in enumerate(M):
        # heatmap = make_gradcam_heatmap(tf.expand_dims(image, 0) , model)
        try:
            if MODEL=='segformer':
                # est_label = model.predict(tf.expand_dims(image, 0), batch_size=1).logits
                est_label = model(tf.expand_dims(image, 0)).logits
            else:
                est_label = tf.squeeze(model.predict(tf.expand_dims(image, 0), batch_size=1))

        except:
            if MODEL=='segformer':
                est_label = model.predict(tf.expand_dims(image[:,:,:3], 0), batch_size=1).logits

            else:
                est_label = tf.squeeze(model.predict(tf.expand_dims(image[:,:,:3], 0), batch_size=1))

        if TESTTIMEAUG == True:
            # return the flipped prediction
            if MODEL=='segformer':
                est_label2 = np.flipud(
                    model.predict(tf.expand_dims(np.flipud(image), 0), batch_size=1).logits
                    )
            else:
                est_label2 = np.flipud(
                    tf.squeeze(model.predict(tf.expand_dims(np.flipud(image), 0), batch_size=1))
                    )

            if MODEL=='segformer':
                est_label3 = np.fliplr(
                    model.predict(
                        tf.expand_dims(np.fliplr(image), 0), batch_size=1).logits
                        )
            else:
                est_label3 = np.fliplr(
                    tf.squeeze(model.predict(
                        tf.expand_dims(np.fliplr(image), 0), batch_size=1))
                        )
                
            if MODEL=='segformer':
                est_label4 = np.flipud(
                    np.fliplr(
                        model.predict(
                            tf.expand_dims(np.flipud(np.fliplr(image)), 0), batch_size=1).logits)
                            )
            else:
                est_label4 = np.flipud(
                    np.fliplr(
                        tf.squeeze(model.predict(
                            tf.expand_dims(np.flipud(np.fliplr(image)), 0), batch_size=1)))
                            )
                
            # soft voting - sum the softmax scores to return the new TTA estimated softmax scores
            est_label = est_label + est_label2 + est_label3 + est_label4
            # del est_label2, est_label3, est_label4
        
        # est_label = est_label.numpy().astype('float32')

        if not isinstance(est_label, np.ndarray):
            # If not, convert it to a numpy array
            est_label = est_label.numpy()
        # Now, convert to 'float32'
        est_label = est_label.astype('float32')

        if MODEL=='segformer':
            est_label = resize(est_label, (1, NCLASSES, TARGET_SIZE[0],TARGET_SIZE[1]), preserve_range=True, clip=True).squeeze()
            est_label = np.transpose(est_label, (1,2,0))

        E0.append(
            resize(est_label[:, :, 0], (w, h), preserve_range=True, clip=True)
        )
        E1.append(
            resize(est_label[:, :, 1], (w, h), preserve_range=True, clip=True)
        )
        # del est_label
    # heatmap = resize(heatmap,(w,h), preserve_range=True, clip=True)
    K.clear_session()

    return E0, E1 


# =========================================================
def do_seg(
    f, M, metadatadict, MODEL, sample_direc, 
    NCLASSES, N_DATA_BANDS, TARGET_SIZE, TESTTIMEAUG, WRITE_MODELMETADATA,
    OTSU_THRESHOLD,
    out_dir_name='out',
    profile='minimal'
):
    
    if profile=='meta':
        WRITE_MODELMETADATA = True
    if profile=='full':
        WRITE_MODELMETADATA = True

    # Mc = compile_models(M, MODEL)

    if f.endswith("jpg"):
        segfile = f.replace(".jpg", "_predseg.png")
    elif f.endswith("png"):
        segfile = f.replace(".png", "_predseg.png")
    elif f.endswith("tif"):
        segfile = f.replace(".tif", "_predseg.png")        
    elif f.endswith("npz"):  # in f:
        segfile = f.replace(".npz", "_predseg.png")

    if WRITE_MODELMETADATA:
        metadatadict["input_file"] = f
        
    # directory to hold the outputs of the models is named 'out' by default
    # create a directory to hold the outputs of the models, by default name it 'out' or the model name if it exists in metadatadict
    out_dir_path = os.path.normpath(sample_direc + os.sep + out_dir_name)
    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)

    segfile = os.path.normpath(segfile)
    segfile = segfile.replace(
        os.path.normpath(sample_direc), os.path.normpath(sample_direc + os.sep + out_dir_name)
    )

    if WRITE_MODELMETADATA:
        metadatadict["nclasses"] = NCLASSES
        metadatadict["n_data_bands"] = N_DATA_BANDS

    if NCLASSES == 2:

        image, w, h, bigimage = get_image(f,N_DATA_BANDS,TARGET_SIZE,MODEL)

        if np.std(image)==0:

            print("Image {} is empty".format(f))
            e0 = np.zeros((w,h))
            e1 = np.zeros((w,h))

        else:

            E0, E1 = est_label_binary(image,M,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE,w,h)

            e0 = np.average(np.dstack(E0), axis=-1)  

            # del E0

            e1 = np.average(np.dstack(E1), axis=-1) 
            # del E1

        est_label = (e1 + (1 - e0)) / 2

        if WRITE_MODELMETADATA:
            metadatadict["av_prob_stack"] = est_label

        softmax_scores = np.dstack((e0,e1))
        # del e0, e1

        if WRITE_MODELMETADATA:
            metadatadict["av_softmax_scores"] = softmax_scores

        if OTSU_THRESHOLD:
            thres = threshold_otsu(est_label)
            # print("Class threshold: %f" % (thres))
            est_label = (est_label > thres).astype("uint8")
            if WRITE_MODELMETADATA:
                metadatadict["otsu_threshold"] = thres

        else:
            est_label = (est_label > 0.5).astype("uint8")
            if WRITE_MODELMETADATA:
                metadatadict["otsu_threshold"] = 0.5            

    else:  ###NCLASSES>2

        image, w, h, bigimage = get_image(f,N_DATA_BANDS,TARGET_SIZE,MODEL)

        if np.std(image)==0:

            print("Image {} is empty".format(f))
            est_label = np.zeros((w,h))

        else:
                
            est_label, counter = est_label_multiclass(image,M,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE)

            est_label /= counter + 1
            # est_label cannot be float16 so convert to float32
            # est_label = est_label.numpy().astype('float32')

            if not isinstance(est_label, np.ndarray):
                # If not, convert it to a numpy array
                est_label = est_label.numpy()
            # Now, convert to 'float32'
            est_label = est_label.astype('float32')

            if MODEL=='segformer':
                est_label = resize(est_label, (1, NCLASSES, TARGET_SIZE[0],TARGET_SIZE[1]), preserve_range=True, clip=True).squeeze()
                est_label = np.transpose(est_label, (1,2,0))
                est_label = resize(est_label, (w, h))
            else:
                est_label = resize(est_label, (w, h))


        if WRITE_MODELMETADATA:
            metadatadict["av_prob_stack"] = est_label

        softmax_scores = est_label.copy() #np.dstack((e0,e1))

        if WRITE_MODELMETADATA:
            metadatadict["av_softmax_scores"] = softmax_scores

        if np.std(image)>0:
            est_label = np.argmax(softmax_scores, -1)
        else:
            est_label = est_label.astype('uint8')


    class_label_colormap = [
        "#3366CC",
        "#DC3912",
        "#FF9900",
        "#109618",
        "#990099",
        "#0099C6",
        "#DD4477",
        "#66AA00",
        "#B82E2E",
        "#316395",
        "#ffe4e1",
        "#ff7373",
        "#666666",
        "#c0c0c0",
        "#66cdaa",
        "#afeeee",
        "#0e2f44",
        "#420420",
        "#794044",
        "#3399ff",
    ]

    class_label_colormap = class_label_colormap[:NCLASSES]

    if WRITE_MODELMETADATA:
        metadatadict["color_segmentation_output"] = segfile

    try:
        color_label = label_to_colors(
            est_label,
            bigimage.numpy()[:, :, 0] == 0,
            alpha=128,
            colormap=class_label_colormap,
            color_class_offset=0,
            do_alpha=False,
        )
    except:
        try:
            color_label = label_to_colors(
                est_label,
                bigimage[:, :, 0] == 0,
                alpha=128,
                colormap=class_label_colormap,
                color_class_offset=0,
                do_alpha=False,
            )
        except:
            color_label = label_to_colors(
                est_label,
                bigimage == 0,
                alpha=128,
                colormap=class_label_colormap,
                color_class_offset=0,
                do_alpha=False,
            )        

    imsave(segfile, (color_label).astype(np.uint8), check_contrast=False)
    
    if WRITE_MODELMETADATA:
        metadatadict["color_segmentation_output"] = segfile

    segfile = segfile.replace("_predseg.png", "_res.npz")

    if WRITE_MODELMETADATA:
        metadatadict["grey_label"] = est_label
        np.savez_compressed(segfile, **metadatadict)

    if profile == 'full': #(profile !='minimal') and (profile !='meta'):
        #### plot overlay
        segfile = segfile.replace("_res.npz", "_overlay.png")

        if N_DATA_BANDS <= 3:
            plt.imshow(bigimage, cmap='gray')
        else:
            plt.imshow(bigimage[:, :, :3])

        plt.imshow(color_label, alpha=0.5)
        plt.axis("off")
        plt.savefig(segfile, dpi=200, bbox_inches="tight")
        plt.close("all")

        #### image - overlay side by side
        segfile = segfile.replace("_res.npz", "_image_overlay.png")

        plt.subplot(121)
        if N_DATA_BANDS <= 3:
            plt.imshow(bigimage, cmap='gray')
        else:
            plt.imshow(bigimage[:, :, :3])
        plt.axis("off")

        plt.subplot(122)
        if N_DATA_BANDS <= 3:
            plt.imshow(bigimage, cmap='gray')
        else:
            plt.imshow(bigimage[:, :, :3])
        plt.imshow(color_label, alpha=0.5)
        plt.axis("off")
        plt.savefig(segfile, dpi=200, bbox_inches="tight")
        plt.close("all")

    if profile == 'full': #(profile !='minimal') and (profile !='meta'):

        #### plot overlay of per-class probabilities
        for kclass in range(softmax_scores.shape[-1]):
            tmpfile = segfile.replace("_overlay.png", "_overlay_"+str(kclass)+"prob.png")

            if N_DATA_BANDS <= 3:
                plt.imshow(bigimage, cmap='gray')
            else:
                plt.imshow(bigimage[:, :, :3])

            plt.imshow(softmax_scores[:,:,kclass], alpha=0.5, vmax=1, vmin=0)
            plt.axis("off")
            plt.colorbar()
            plt.savefig(tmpfile, dpi=200, bbox_inches="tight")
            plt.close("all")



# # =========================================================
# def do_seg(
#     f, M, metadatadict, MODEL, sample_direc, 
#     NCLASSES, N_DATA_BANDS, TARGET_SIZE, TESTTIMEAUG, WRITE_MODELMETADATA,
#     OTSU_THRESHOLD,
#     out_dir_name='out',
#     profile='minimal'
# ):
    
#     if profile=='meta':
#         WRITE_MODELMETADATA = True
#     if profile=='full':
#         WRITE_MODELMETADATA = True

#     Mc = compile_models(M, MODEL)

#     if f.endswith("jpg"):
#         segfile = f.replace(".jpg", "_predseg.png")
#     elif f.endswith("png"):
#         segfile = f.replace(".png", "_predseg.png")
#     elif f.endswith("npz"):  # in f:
#         segfile = f.replace(".npz", "_predseg.png")

#     if WRITE_MODELMETADATA:
#         metadatadict["input_file"] = f
        
#     # directory to hold the outputs of the models is named 'out' by default
#     # create a directory to hold the outputs of the models, by default name it 'out' or the model name if it exists in metadatadict
#     out_dir_path = os.path.normpath(sample_direc + os.sep + out_dir_name)
#     if not os.path.exists(out_dir_path):
#         os.mkdir(out_dir_path)

#     segfile = os.path.normpath(segfile)
#     segfile = segfile.replace(
#         os.path.normpath(sample_direc), os.path.normpath(sample_direc + os.sep + out_dir_name)
#     )

#     if WRITE_MODELMETADATA:
#         metadatadict["nclasses"] = NCLASSES
#         metadatadict["n_data_bands"] = N_DATA_BANDS

#     if NCLASSES == 2:

#         image, w, h, bigimage = get_image(f,N_DATA_BANDS,TARGET_SIZE,MODEL)

#         E0, E1 = est_label_binary(image,Mc,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE,w,h)

#         e0 = np.average(np.dstack(E0), axis=-1)  

#         # del E0

#         e1 = np.average(np.dstack(E1), axis=-1) 
#         # del E1

#         est_label = (e1 + (1 - e0)) / 2

#         if WRITE_MODELMETADATA:
#             metadatadict["av_prob_stack"] = est_label

#         softmax_scores = np.dstack((e0,e1))
#         # del e0, e1

#         if WRITE_MODELMETADATA:
#             metadatadict["av_softmax_scores"] = softmax_scores

#         if OTSU_THRESHOLD:
#             thres = threshold_otsu(est_label)
#             # print("Class threshold: %f" % (thres))
#             est_label = (est_label > thres).astype("uint8")
#             if WRITE_MODELMETADATA:
#                 metadatadict["otsu_threshold"] = thres

#         else:
#             est_label = (est_label > 0.5).astype("uint8")
#             if WRITE_MODELMETADATA:
#                 metadatadict["otsu_threshold"] = 0.5            

#     else:  ###NCLASSES>2

#         image, w, h, bigimage = get_image(f,N_DATA_BANDS,TARGET_SIZE,MODEL)

#         est_label, counter = est_label_multiclass(image,Mc,MODEL,TESTTIMEAUG,NCLASSES,TARGET_SIZE)

#         est_label /= counter + 1
#         # est_label cannot be float16 so convert to float32
#         est_label = est_label.numpy().astype('float32')

#         if MODEL=='segformer':
#             est_label = resize(est_label, (1, NCLASSES, TARGET_SIZE[0],TARGET_SIZE[1]), preserve_range=True, clip=True).squeeze()
#             est_label = np.transpose(est_label, (1,2,0))
#             est_label = resize(est_label, (w, h))
#         else:
#             est_label = resize(est_label, (w, h))


#         if WRITE_MODELMETADATA:
#             metadatadict["av_prob_stack"] = est_label

#         softmax_scores = est_label.copy() #np.dstack((e0,e1))

#         if WRITE_MODELMETADATA:
#             metadatadict["av_softmax_scores"] = softmax_scores

#         est_label = np.argmax(softmax_scores, -1)


#     class_label_colormap = [
#         "#3366CC",
#         "#DC3912",
#         "#FF9900",
#         "#109618",
#         "#990099",
#         "#0099C6",
#         "#DD4477",
#         "#66AA00",
#         "#B82E2E",
#         "#316395",
#         "#ffe4e1",
#         "#ff7373",
#         "#666666",
#         "#c0c0c0",
#         "#66cdaa",
#         "#afeeee",
#         "#0e2f44",
#         "#420420",
#         "#794044",
#         "#3399ff",
#     ]

#     class_label_colormap = class_label_colormap[:NCLASSES]

#     if WRITE_MODELMETADATA:
#         metadatadict["color_segmentation_output"] = segfile

#     try:
#         color_label = label_to_colors(
#             est_label,
#             bigimage.numpy()[:, :, 0] == 0,
#             alpha=128,
#             colormap=class_label_colormap,
#             color_class_offset=0,
#             do_alpha=False,
#         )
#     except:
#         try:
#             color_label = label_to_colors(
#                 est_label,
#                 bigimage[:, :, 0] == 0,
#                 alpha=128,
#                 colormap=class_label_colormap,
#                 color_class_offset=0,
#                 do_alpha=False,
#             )
#         except:
#             color_label = label_to_colors(
#                 est_label,
#                 bigimage == 0,
#                 alpha=128,
#                 colormap=class_label_colormap,
#                 color_class_offset=0,
#                 do_alpha=False,
#             )        

#     imsave(segfile, (color_label).astype(np.uint8), check_contrast=False)
    
#     if WRITE_MODELMETADATA:
#         metadatadict["color_segmentation_output"] = segfile

#     segfile = segfile.replace("_predseg.png", "_res.npz")

#     if WRITE_MODELMETADATA:
#         metadatadict["grey_label"] = est_label
#         np.savez_compressed(segfile, **metadatadict)

#     if profile == 'full': #(profile !='minimal') and (profile !='meta'):
#         #### plot overlay
#         segfile = segfile.replace("_res.npz", "_overlay.png")

#         if N_DATA_BANDS <= 3:
#             plt.imshow(bigimage, cmap='gray')
#         else:
#             plt.imshow(bigimage[:, :, :3])

#         plt.imshow(color_label, alpha=0.5)
#         plt.axis("off")
#         plt.savefig(segfile, dpi=200, bbox_inches="tight")
#         plt.close("all")

#         #### image - overlay side by side
#         segfile = segfile.replace("_res.npz", "_image_overlay.png")

#         plt.subplot(121)
#         if N_DATA_BANDS <= 3:
#             plt.imshow(bigimage, cmap='gray')
#         else:
#             plt.imshow(bigimage[:, :, :3])
#         plt.axis("off")

#         plt.subplot(122)
#         if N_DATA_BANDS <= 3:
#             plt.imshow(bigimage, cmap='gray')
#         else:
#             plt.imshow(bigimage[:, :, :3])
#         plt.imshow(color_label, alpha=0.5)
#         plt.axis("off")
#         plt.savefig(segfile, dpi=200, bbox_inches="tight")
#         plt.close("all")

#     if profile == 'full': #(profile !='minimal') and (profile !='meta'):

#         #### plot overlay of per-class probabilities
#         for kclass in range(softmax_scores.shape[-1]):
#             tmpfile = segfile.replace("_overlay.png", "_overlay_"+str(kclass)+"prob.png")

#             if N_DATA_BANDS <= 3:
#                 plt.imshow(bigimage, cmap='gray')
#             else:
#                 plt.imshow(bigimage[:, :, :3])

#             plt.imshow(softmax_scores[:,:,kclass], alpha=0.5, vmax=1, vmin=0)
#             plt.axis("off")
#             plt.colorbar()
#             plt.savefig(tmpfile, dpi=200, bbox_inches="tight")
#             plt.close("all")

#     gc.collect()



# --------------------------------------------------------
def make_gradcam_heatmap(image, model):

    # Remove last layer's softmax
    model.layers[-2].activation = None

    last_conv_layer_name = model.layers[-39].name
    # print(last_conv_layer_name)

    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output],
        trainable=False,
    )

    # then gradient of the output with respect to the output feature map of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(image)

        grads = tape.gradient(preds, last_conv_layer_output)
    # mean intensity of the gradient
    # importance of each channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    heatmap = heatmap.numpy().squeeze()

    # plt.imshow(image.numpy().squeeze()); plt.imshow(heatmap, cmap='bwr',alpha=0.5); plt.savefig('tmp.png')

    return heatmap


###### for patches-based segmentation 


def window2d(window_func, window_size, **kwargs):
    """
    Generates a 2D square image (of size window_size) containing a 2D user-defined
    window with values ranging from 0 to 1.
    It is possible to pass arguments to the window function by setting kwargs.
    All available windows: https://docs.scipy.org/doc/scipy/reference/signal.windows.html
    """
    window = np.matrix(window_func(M=window_size, sym=False, **kwargs))
    return window.T.dot(window)


def generate_corner_windows(window_func, window_size, **kwargs):
    step = window_size >> 1
    window = window2d(window_func, window_size, **kwargs)
    window_u = np.vstack(
        [np.tile(window[step : step + 1, :], (step, 1)), window[step:, :]]
    )
    window_b = np.vstack(
        [window[:step, :], np.tile(window[step : step + 1, :], (step, 1))]
    )
    window_l = np.hstack(
        [np.tile(window[:, step : step + 1], (1, step)), window[:, step:]]
    )
    window_r = np.hstack(
        [window[:, :step], np.tile(window[:, step : step + 1], (1, step))]
    )
    window_ul = np.block(
        [
            [np.ones((step, step)), window_u[:step, step:]],
            [window_l[step:, :step], window_l[step:, step:]],
        ]
    )
    window_ur = np.block(
        [
            [window_u[:step, :step], np.ones((step, step))],
            [window_r[step:, :step], window_r[step:, step:]],
        ]
    )
    window_bl = np.block(
        [
            [window_l[:step, :step], window_l[:step, step:]],
            [np.ones((step, step)), window_b[step:, step:]],
        ]
    )
    window_br = np.block(
        [
            [window_r[:step, :step], window_r[:step, step:]],
            [window_b[step:, :step], np.ones((step, step))],
        ]
    )
    return np.array(
        [
            [window_ul, window_u, window_ur],
            [window_l, window, window_r],
            [window_bl, window_b, window_br],
        ]
    )


def generate_patch_list(
    image_width, image_height, window_func, window_size, overlapping=False
):
    patch_list = []
    if overlapping:
        step = window_size >> 1
        windows = generate_corner_windows(window_func, window_size)
        max_height = int(image_height / step - 1) * step
        max_width = int(image_width / step - 1) * step
    else:
        step = window_size
        windows = np.ones((window_size, window_size))
        max_height = int(image_height / step) * step
        max_width = int(image_width / step) * step
    for i in range(0, max_height, step):
        for j in range(0, max_width, step):
            if overlapping:
                # Close to border and corner cases
                # Default (1, 1) is regular center window
                border_x, border_y = 1, 1
                if i == 0:
                    border_x = 0
                if j == 0:
                    border_y = 0
                if i == max_height - step:
                    border_x = 2
                if j == max_width - step:
                    border_y = 2
                # Selecting the right window
                current_window = windows[border_x, border_y]
            else:
                current_window = windows
            # The patch is cropped when the patch size is not
            # a multiple of the image size.
            patch_height = window_size
            if i + patch_height > image_height:
                patch_height = image_height - i
            patch_width = window_size
            if j + patch_width > image_width:
                patch_width = image_width - j
            # Adding the patch
            patch_list.append(
                (
                    j,
                    i,
                    patch_width,
                    patch_height,
                    current_window[:patch_height, :patch_width],
                )
            )
    return patch_list


# =========================================================
def norm_shape(shap):
    """
    Normalize numpy array shapes so they're always expressed as a tuple,
    even for one-dimensional shapes.
    """
    try:
        i = int(shap)
        return (i,)
    except TypeError:
        # shape was not a number
        pass

    try:
        t = tuple(shap)
        return t
    except TypeError:
        # shape was not iterable
        pass

    raise TypeError("shape must be an int, or a tuple of ints")


# =========================================================
# Return a sliding window over a in any number of dimensions
# version with no memory mapping
def sliding_window(a, ws, ss=None, flatten=True):
    """
    Return a sliding window over a in any number of dimensions
    """
    if None is ss:
        # ss was not provided. the windows will not overlap in any direction.
        ss = ws
    ws = norm_shape(ws)
    ss = norm_shape(ss)
    # convert ws, ss, and a.shape to numpy arrays
    ws = np.array(ws)
    ss = np.array(ss)
    shap = np.array(a.shape)
    # ensure that ws, ss, and a.shape all have the same number of dimensions
    ls = [len(shap), len(ws), len(ss)]
    if 1 != len(set(ls)):
        raise ValueError(
            "a.shape, ws and ss must all have the same length. They were %s" % str(ls)
        )

    # ensure that ws is smaller than a in every dimension
    if np.any(ws > shap):
        raise ValueError(
            "ws cannot be larger than a in any dimension.\
 a.shape was %s and ws was %s"
            % (str(a.shape), str(ws))
        )
    # how many slices will there be in each dimension?
    newshape = norm_shape(((shap - ws) // ss) + 1)
    # the shape of the strided array will be the number of slices in each dimension
    # plus the shape of the window (tuple addition)
    newshape += norm_shape(ws)
    # the strides tuple will be the array's strides multiplied by step size, plus
    # the array's strides (tuple addition)
    newstrides = norm_shape(np.array(a.strides) * ss) + a.strides
    a = ast(a, shape=newshape, strides=newstrides)
    if not flatten:
        return a
    # Collapse strided so that it has one more dimension than the window.  I.e.,
    # the new array is a flat list of slices.
    meat = len(ws) if ws.shape else 0
    firstdim = (np.product(newshape[:-meat]),) if ws.shape else ()
    dim = firstdim + (newshape[-meat:])
    # remove any dimensions with size 1
    # dim = filter(lambda i : i != 1,dim)

    return a.reshape(dim), newshape



# #-----------------------------------
# def crf_refine_from_integer_labels(label, img, nclasses = 2, theta_col=100, theta_spat=3, compat=120):
#     """
#     "crf_refine(label, img)"
#     This function refines a label image based on an input label image and the associated image
#     Uses a conditional random field algorithm using spatial and image features
#     INPUTS:
#         * label [ndarray]: label image 2D matrix of integers
#         * image [ndarray]: image 3D matrix of integers
#     OPTIONAL INPUTS: None
#     GLOBAL INPUTS: None
#     OUTPUTS: label [ndarray]: label image 2D matrix of integers
#     """

#     gx,gy = np.meshgrid(np.arange(img.shape[1]), np.arange(img.shape[0]))
#     # print(gx.shape)
#     img = np.dstack((img,gx,gy))

#     H = label.shape[0]
#     W = label.shape[1]
#     U = unary_from_labels(1+label,nclasses,gt_prob=0.51)
#     d = dcrf.DenseCRF2D(H, W, nclasses)
#     d.setUnaryEnergy(U)

#     # to add the color-independent term, where features are the locations only:
#     d.addPairwiseGaussian(sxy=(theta_spat, theta_spat),
#                  compat=3,
#                  kernel=dcrf.DIAG_KERNEL,
#                  normalization=dcrf.NORMALIZE_SYMMETRIC)
#     feats = create_pairwise_bilateral(
#                           sdims=(theta_col, theta_col),
#                           schan=(2,2,2),
#                           img=img,
#                           chdim=2)

#     d.addPairwiseEnergy(feats, compat=compat,kernel=dcrf.DIAG_KERNEL,normalization=dcrf.NORMALIZE_SYMMETRIC)
#     Q = d.inference(20)
#     kl1 = d.klDivergence(Q)
#     return np.argmax(Q, axis=0).reshape((H, W)).astype(np.uint8), kl1



# ##========================================================
# def crf_refine(label,
#     img,n,
#     crf_theta_slider_value,
#     crf_mu_slider_value,
#     crf_downsample_factor): #gt_prob
#     """
#     "crf_refine(label, img)"
#     This function refines a label image based on an input label image and the associated image
#     Uses a conditional random field algorithm using spatial and image features
#     INPUTS:
#         * label [ndarray]: label image 2D matrix of integers
#         * image [ndarray]: image 3D matrix of integers
#     OPTIONAL INPUTS: None
#     GLOBAL INPUTS: None
#     OUTPUTS: label [ndarray]: label image 2D matrix of integers
#     """

#     Horig = img.shape[0]
#     Worig = img.shape[1]
#     l_unique = label.shape[-1]

#     label = label.reshape(Horig,Worig,l_unique)

#     scale = 1+(5 * (np.array(img.shape).max() / 3000))

#     # decimate by factor by taking only every other row and column
#     try:
#         img = img[::crf_downsample_factor,::crf_downsample_factor, :]
#     except:
#         img = img[::crf_downsample_factor,::crf_downsample_factor]

#     # do the same for the label image
#     label = label[::crf_downsample_factor,::crf_downsample_factor]
#     # yes, I know this aliases, but considering the task, it is ok; the objective is to
#     # make fast inference and resize the output

#     H = img.shape[0]
#     W = img.shape[1]
#     # U = unary_from_labels(np.argmax(label,-1).astype('int'), n, gt_prob=gt_prob)
#     # d = dcrf.DenseCRF2D(H, W, n)

#     U = unary_from_softmax(np.ascontiguousarray(np.rollaxis(label,-1,0)))
#     d = dcrf.DenseCRF2D(H, W, l_unique)

#     d.setUnaryEnergy(U)

#     # to add the color-independent term, where features are the locations only:
#     d.addPairwiseGaussian(sxy=(3, 3),
#                  compat=3,
#                  kernel=dcrf.DIAG_KERNEL,
#                  normalization=dcrf.NORMALIZE_SYMMETRIC)

#     try:
#         feats = create_pairwise_bilateral(
#                             sdims=(crf_theta_slider_value, crf_theta_slider_value),
#                             schan=(scale,scale,scale),
#                             img=img,
#                             chdim=2)

#         d.addPairwiseEnergy(feats, compat=crf_mu_slider_value, kernel=dcrf.DIAG_KERNEL,normalization=dcrf.NORMALIZE_SYMMETRIC)
#     except:
#         feats = create_pairwise_bilateral(
#                             sdims=(crf_theta_slider_value, crf_theta_slider_value),
#                             schan=(scale,scale, scale),
#                             img=np.dstack((img,img,img)),
#                             chdim=2)

#         d.addPairwiseEnergy(feats, compat=crf_mu_slider_value, kernel=dcrf.DIAG_KERNEL,normalization=dcrf.NORMALIZE_SYMMETRIC)

#     Q = d.inference(10)
#     result = np.argmax(Q, axis=0).reshape((H, W)).astype(np.uint8) +1

#     # uniq = np.unique(result.flatten())

#     result = resize(result, (Horig, Worig), order=0, anti_aliasing=False) #True)
#     result = rescale(result, 1, l_unique).astype(np.uint8)

#     return result, l_unique