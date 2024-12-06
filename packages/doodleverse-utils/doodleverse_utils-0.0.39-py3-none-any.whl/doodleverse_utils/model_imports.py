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

import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K

# keras functions for early stopping and model weights saving
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

try:
    from transformers import TFSegformerForSemanticSegmentation
except:
    print("Transformers library did not load")

SEED = 42
np.random.seed(SEED)
AUTO = tf.data.experimental.AUTOTUNE  # used in tf.data.Dataset API

tf.random.set_seed(SEED)

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())


###############################################################
### MODEL ARCHITECTURES
###############################################################
def segformer(
    id2label,
    num_classes=2,
):
    """
    https://keras.io/examples/vision/segformer/
    https://huggingface.co/nvidia/mit-b0
    """

    label2id = {label: id for id, label in id2label.items()}
    model_checkpoint = "nvidia/mit-b0"

    model = TFSegformerForSemanticSegmentation.from_pretrained(
        model_checkpoint,
        num_labels=num_classes,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )
    return model


# -----------------------------------
def simple_resunet(
    input_shape,
    kernel=(2, 2),
    num_classes=2,
    activation="relu",
    use_batch_norm=True,
    dropout=0.1,
    dropout_change_per_layer=0.0,
    dropout_type="standard",
    use_dropout_on_upsampling=False,
    filters=8,
    num_layers=4,
    strides=(1, 1),
):

    """
    Customisable UNet architecture (Ronneberger et al. 2015 https://arxiv.org/abs/1505.04597)

    input_shape: shape (x, y, num_channels)

    num_classes (int): 2 for binary segmentation

    activation (str): A keras.activations.Activation to use. ReLu by default.

    use_batch_norm (bool): Whether to use Batch Normalisation across the channel axis between convolutions

    dropout (float , 0. and 1.): dropout after the first convolutional block. 0. = no dropout

    dropout_change_per_layer (float , 0. and 1.): Factor to add to the Dropout after each convolutional block

    dropout_type (one of "spatial" or "standard"): Spatial is recommended  by  https://arxiv.org/pdf/1411.4280.pdf

    use_dropout_on_upsampling (bool): Whether to use dropout in the decoder part of the network

    filters (int): Convolutional filters in the initial convolutional block. Will be doubled every block

    num_layers (int): Number of total layers in the encoder not including the bottleneck layer

    """
    # Build U-Net model
    inputs = tf.keras.layers.Input(input_shape)
    x = inputs

    # x = bottleneck_block(inputs, filters)

    down_layers = []
    for l in range(num_layers):
        x = res_conv2d_block(
            inputs=x,
            filters=filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
            strides=strides,  # (1,1),
        )
        down_layers.append(x)
        x = tf.keras.layers.MaxPooling2D(kernel)(x)
        dropout += dropout_change_per_layer
        filters = filters * 2  # double the number of filters with each layer

    x = conv2d_block(
        inputs=x,
        filters=filters,
        use_batch_norm=use_batch_norm,
        dropout=dropout,
        dropout_type=dropout_type,
        activation=activation,
        strides=strides,  # (1,1),
    )

    if not use_dropout_on_upsampling:
        dropout = 0.0
        dropout_change_per_layer = 0.0

    for conv in reversed(down_layers):
        filters //= 2  # decreasing number of filters with each layer
        dropout -= dropout_change_per_layer
        # x = upsample(filters, kernel, strides=(2,2), padding="same")(x)#(2, 2)
        x = tf.keras.layers.UpSampling2D(kernel)(x)
        x = tf.keras.layers.concatenate([x, conv])
        x = res_conv2d_block(
            inputs=x,
            filters=filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
            strides=strides,
        )  # (1,1))

    outputs = tf.keras.layers.Conv2D(
        num_classes, (1, 1), padding="same", activation="softmax"#, dtype='float32'
    )(
        x
    )  # (1, 1)

    model = tf.keras.models.Model(inputs=[inputs], outputs=[outputs])
    return model


# -----------------------------------
def simple_unet(
    input_shape,
    kernel=(2, 2),
    num_classes=2,
    activation="relu",
    use_batch_norm=True,
    dropout=0.1,
    dropout_change_per_layer=0.0,
    dropout_type="standard",
    use_dropout_on_upsampling=False,
    filters=8,
    num_layers=4,
    strides=(1, 1),
):

    """
    Customisable UNet architecture (Ronneberger et al. 2015 https://arxiv.org/abs/1505.04597)

    input_shape: shape (x, y, num_channels)

    num_classes (int): 2 for binary segmentation

    activation (str): A keras.activations.Activation to use. ReLu by default.

    use_batch_norm (bool): Whether to use Batch Normalisation across the channel axis between convolutions

    dropout (float , 0. and 1.): dropout after the first convolutional block. 0. = no dropout

    dropout_change_per_layer (float , 0. and 1.): Factor to add to the Dropout after each convolutional block

    dropout_type (one of "spatial" or "standard"): Spatial is recommended  by  https://arxiv.org/pdf/1411.4280.pdf

    use_dropout_on_upsampling (bool): Whether to use dropout in the decoder part of the network

    filters (int): Convolutional filters in the initial convolutional block. Will be doubled every block

    num_layers (int): Number of total layers in the encoder not including the bottleneck layer

    """

    # Build U-Net model
    inputs = tf.keras.layers.Input(input_shape)
    x = inputs

    down_layers = []
    for l in range(num_layers):
        x = conv2d_block(
            inputs=x,
            filters=filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
            strides=strides,  # (1,1),
        )
        down_layers.append(x)
        # if use_pooling:
        x = tf.keras.layers.MaxPooling2D(kernel)(x)
        dropout += dropout_change_per_layer
        filters = filters * 2  # double the number of filters with each layer

    x = conv2d_block(
        inputs=x,
        filters=filters,
        use_batch_norm=use_batch_norm,
        dropout=dropout,
        dropout_type=dropout_type,
        activation=activation,
        strides=strides,  # (1,1),
    )

    if not use_dropout_on_upsampling:
        dropout = 0.0
        dropout_change_per_layer = 0.0

    for conv in reversed(down_layers):
        filters //= 2  # decreasing number of filters with each layer
        dropout -= dropout_change_per_layer
        # x = upsample(filters, kernel, strides=(2,2), padding="same")(x)#(2, 2)
        x = tf.keras.layers.UpSampling2D(kernel)(x)
        x = tf.keras.layers.concatenate([x, conv])
        x = conv2d_block(
            inputs=x,
            filters=filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
        )

    outputs = tf.keras.layers.Conv2D(
        num_classes, (1, 1), padding="same", activation="softmax"#, dtype='float32'
    )(x)

    model = tf.keras.models.Model(inputs=[inputs], outputs=[outputs])
    return model


##========================================================================


# -----------------------------------
def simple_satunet(
    input_shape,
    kernel=(2, 2),
    num_classes=2,
    activation="relu",
    use_batch_norm=True,
    dropout=0.1,
    dropout_change_per_layer=0.0,
    dropout_type="standard",
    use_dropout_on_upsampling=False,
    filters=8,
    num_layers=4,
    strides=(1, 1),
):

    """
    Customisable UNet architecture (Ronneberger et al. 2015 https://arxiv.org/abs/1505.04597)

    input_shape: shape (x, y, num_channels)

    num_classes (int): 2 for binary segmentation

    activation (str): A keras.activations.Activation to use. ReLu by default.

    use_batch_norm (bool): Whether to use Batch Normalisation across the channel axis between convolutions

    dropout (float , 0. and 1.): dropout after the first convolutional block. 0. = no dropout

    dropout_change_per_layer (float , 0. and 1.): Factor to add to the Dropout after each convolutional block

    dropout_type (one of "spatial" or "standard"): Spatial is recommended  by  https://arxiv.org/pdf/1411.4280.pdf

    use_dropout_on_upsampling (bool): Whether to use dropout in the decoder part of the network

    filters (int): Convolutional filters in the initial convolutional block. Will be doubled every block

    num_layers (int): Number of total layers in the encoder not including the bottleneck layer

    """

    upconv_filters = int(1.5 * filters)

    # Build U-Net model
    inputs = tf.keras.layers.Input(input_shape)
    x = inputs

    down_layers = []
    for l in range(num_layers):
        x = conv2d_block(
            inputs=x,
            filters=filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
            strides=strides,  # (1,1),
        )
        down_layers.append(x)
        x = tf.keras.layers.MaxPooling2D(kernel)(x)
        dropout += dropout_change_per_layer
        # filters = filters * 2  # double the number of filters with each layer

    x = conv2d_block(
        inputs=x,
        filters=filters,
        use_batch_norm=use_batch_norm,
        dropout=dropout,
        dropout_type=dropout_type,
        activation=activation,
        strides=strides,  # (1,1),
    )

    if not use_dropout_on_upsampling:
        dropout = 0.0
        dropout_change_per_layer = 0.0

    for conv in reversed(down_layers):
        filters //= 2  # decreasing number of filters with each layer
        dropout -= dropout_change_per_layer
        # x = upsample(filters, kernel, strides=(2,2), padding="same")(x)#(2, 2)
        x = tf.keras.layers.UpSampling2D(kernel)(x)
        x = tf.keras.layers.concatenate([x, conv])
        x = conv2d_block(
            inputs=x,
            filters=upconv_filters,
            use_batch_norm=use_batch_norm,
            dropout=dropout,
            dropout_type=dropout_type,
            activation=activation,
        )

    outputs = tf.keras.layers.Conv2D(
        num_classes, (1, 1), padding="same", activation="softmax"#, dtype='float32'
    )(x)

    model = tf.keras.models.Model(inputs=[inputs], outputs=[outputs])
    return model


##========================================================================


# -----------------------------------
def custom_resunet(
    sz,
    f,
    nclasses=2,
    kernel_size=(7, 7),
    strides=2,
    dropout=0.1,
    dropout_change_per_layer=0.0,
    dropout_type="standard",
    use_dropout_on_upsampling=False,
):
    """
    res_unet(sz, f, nclasses=1)
    This function creates a custom residual U-Net model for image segmentation
    INPUTS:
        * `sz`: [tuple] size of input image
        * `f`: [int] number of filters in the convolutional block
        * flag: [string] if 'binary', the model will expect 2D masks and uses sigmoid. If 'multiclass', the model will expect 3D masks and uses softmax
        * nclasses [int]: number of classes
        dropout (float , 0. and 1.): dropout after the first convolutional block. 0. = no dropout

        dropout_change_per_layer (float , 0. and 1.): Factor to add to the Dropout after each convolutional block

        dropout_type (one of "spatial" or "standard"): Spatial is recommended  by  https://arxiv.org/pdf/1411.4280.pdf

        use_dropout_on_upsampling (bool): Whether to use dropout in the decoder part of the network

        filters (int): Convolutional filters in the initial convolutional block. Will be doubled every block
    OPTIONAL INPUTS:
        * `kernel_size`=(7, 7): tuple of kernel size (x, y) - this is the size in pixels of the kernel to be convolved with the image
        * `padding`="same":  see tf.keras.layers.Conv2D
        * `strides`=1: see tf.keras.layers.Conv2D
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras model
    """
    inputs = tf.keras.layers.Input(sz)

    ## downsample
    e1 = bottleneck_block(inputs, f)
    f = int(f * 2)
    e2 = res_block(
        e1,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    e3 = res_block(
        e2,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    e4 = res_block(
        e3,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    _ = res_block(
        e4,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )

    ## bottleneck
    b0 = conv_block(
        _,
        f,
        strides=1,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    _ = conv_block(
        b0,
        f,
        strides=1,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )

    if not use_dropout_on_upsampling:
        dropout = 0.0
        dropout_change_per_layer = 0.0

    ## upsample
    _ = upsamp_concat_block(_, e4)
    _ = res_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e3)
    _ = res_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e2)
    _ = res_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e1)
    _ = res_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )

    outputs = tf.keras.layers.Conv2D(
        nclasses, (1, 1), padding="same", activation="softmax"#, dtype='float32'
    )(_)

    # model creation
    model = tf.keras.models.Model(inputs=[inputs], outputs=[outputs])
    return model


# -----------------------------------
def custom_unet(
    sz,
    f,
    nclasses=2,
    kernel_size=(7, 7),
    strides=2,
    dropout=0.1,
    dropout_change_per_layer=0.0,
    dropout_type="standard",
    use_dropout_on_upsampling=False,
):
    """
    unet(sz, f, nclasses=2)
    This function creates a custom U-Net model for image segmentation
    INPUTS:
        * `sz`: [tuple] size of input image
        * `f`: [int] number of filters in the convolutional block
        * flag: [string] if 'binary', the model will expect 2D masks and uses sigmoid. If 'multiclass', the model will expect 3D masks and uses softmax
        * nclasses [int]: number of classes
        dropout (float , 0. and 1.): dropout after the first convolutional block. 0. = no dropout

        dropout_change_per_layer (float , 0. and 1.): Factor to add to the Dropout after each convolutional block

        dropout_type (one of "spatial" or "standard"): Spatial is recommended  by  https://arxiv.org/pdf/1411.4280.pdf

        use_dropout_on_upsampling (bool): Whether to use dropout in the decoder part of the network

        filters (int): Convolutional filters in the initial convolutional block. Will be doubled every block
    OPTIONAL INPUTS:
        * `kernel_size`=(7, 7): tuple of kernel size (x, y) - this is the size in pixels of the kernel to be convolved with the image
        * `padding`="same":  see tf.keras.layers.Conv2D
        * `strides`=1: see tf.keras.layers.Conv2D
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras model
    """
    inputs = tf.keras.layers.Input(sz)

    ## downsample
    e1 = bottleneck_block(inputs, f)
    f = int(f * 2)
    e2 = conv_block(
        e1,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    e3 = conv_block(
        e2,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    e4 = conv_block(
        e3,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    f = int(f * 2)
    dropout += dropout_change_per_layer
    _ = conv_block(
        e4,
        f,
        strides=strides,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )

    ## bottleneck
    b0 = conv_block(
        _,
        f,
        strides=1,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    _ = conv_block(
        b0,
        f,
        strides=1,
        kernel_size=kernel_size,
        dropout=dropout,
        dropout_type=dropout_type,
    )

    if not use_dropout_on_upsampling:
        dropout = 0.0
        dropout_change_per_layer = 0.0

    ## upsample
    _ = upsamp_concat_block(_, e4)
    _ = conv_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e3)
    _ = conv_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e2)
    _ = conv_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )
    f = int(f / 2)
    dropout -= dropout_change_per_layer

    _ = upsamp_concat_block(_, e1)
    _ = conv_block(
        _, f, kernel_size=kernel_size, dropout=dropout, dropout_type=dropout_type
    )

    outputs = tf.keras.layers.Conv2D(
        nclasses, (1, 1), padding="same", activation="softmax"#, dtype='float32'
    )(_)

    # model creation
    model = tf.keras.models.Model(inputs=[inputs], outputs=[outputs])
    return model


###############################################################
### MODEL SUBFUNCTIONS
###############################################################

# -----------------------------------
def upsamp_concat_block(x, xskip):
    """
    upsamp_concat_block(x, xskip)
    This function takes an input layer and creates a concatenation of an upsampled version and a residual or 'skip' connection
    INPUTS:
        * `xskip`: input keras layer (skip connection)
        * `x`: input keras layer
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras layer, output of the addition between residual convolutional and bottleneck layers
    """
    u = tf.keras.layers.UpSampling2D((2, 2))(x)

    return tf.keras.layers.Concatenate()([u, xskip])


# -----------------------------------
def conv_block(
    x,
    filters,
    kernel_size=(7, 7),
    padding="same",
    strides=1,
    dropout=0.1,
    dropout_type="standard",
):
    """
    conv_block(x, filters, kernel_size = (7,7), padding="same", strides=1)
    This function applies batch normalization to an input layer, then convolves with a 2D convol layer
    The two actions combined is called a convolutional block

    INPUTS:
        * `filters`: number of filters in the convolutional block
        * `x`:input keras layer to be convolved by the block
    OPTIONAL INPUTS:
        * `kernel_size`=(3, 3): tuple of kernel size (x, y) - this is the size in pixels of the kernel to be convolved with the image
        * `padding`="same":  see tf.keras.layers.Conv2D
        * `strides`=1: see tf.keras.layers.Conv2D
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras layer, output of the batch normalized convolution
    """

    if dropout_type == "spatial":
        DO = tf.keras.layers.SpatialDropout2D
    elif dropout_type == "standard":
        DO = tf.keras.layers.Dropout
    else:
        raise ValueError(
            f"dropout_type must be one of ['spatial', 'standard'], got {dropout_type}"
        )

    if dropout > 0.0:
        x = DO(dropout)(x)

    conv = batchnorm_act(x)
    return tf.keras.layers.Conv2D(
        filters, kernel_size, padding=padding, strides=strides
    )(conv)


# -----------------------------------
def bottleneck_block(x, filters, kernel_size=(2, 2), padding="same", strides=1):
    """
    bottleneck_block(x, filters, kernel_size = (7,7), padding="same", strides=1)

    This function creates a bottleneck block layer, which is the addition of a convolution block and a batch normalized/activated block
    INPUTS:
        * `filters`: number of filters in the convolutional block
        * `x`: input keras layer
    OPTIONAL INPUTS:
        * `kernel_size`=(3, 3): tuple of kernel size (x, y) - this is the size in pixels of the kernel to be convolved with the image
        * `padding`="same":  see tf.keras.layers.Conv2D
        * `strides`=1: see tf.keras.layers.Conv2D
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras layer, output of the addition between convolutional and bottleneck layers
    """
    conv = tf.keras.layers.Conv2D(
        filters, kernel_size, padding=padding, strides=strides
    )(x)
    conv = conv_block(
        conv,
        filters,
        kernel_size=kernel_size,
        padding=padding,
        strides=strides,
        dropout=0.0,
        dropout_type="standard",
    )

    bottleneck = tf.keras.layers.Conv2D(
        filters, kernel_size=(1, 1), padding=padding, strides=strides
    )(x)
    bottleneck = batchnorm_act(bottleneck)

    return tf.keras.layers.Add()([conv, bottleneck])


def res_block(
    x,
    filters,
    kernel_size=(7, 7),
    padding="same",
    strides=1,
    dropout=0.1,
    dropout_type="standard",
):
    """
    res_block(x, filters, kernel_size = (7,7), padding="same", strides=1)
    This function creates a residual block layer, which is the addition of a residual convolution block and a batch normalized/activated block
    INPUTS:
        * `filters`: number of filters in the convolutional block
        * `x`: input keras layer
    OPTIONAL INPUTS:
        * `kernel_size`=(3, 3): tuple of kernel size (x, y) - this is the size in pixels of the kernel to be convolved with the image
        * `padding`="same":  see tf.keras.layers.Conv2D
        * `strides`=1: see tf.keras.layers.Conv2D
    GLOBAL INPUTS: None
    OUTPUTS:
        * keras layer, output of the addition between residual convolutional and bottleneck layers
    """
    res = conv_block(
        x,
        filters,
        kernel_size=kernel_size,
        padding=padding,
        strides=strides,
        dropout=dropout,
        dropout_type=dropout_type,
    )
    res = conv_block(
        res,
        filters,
        kernel_size=kernel_size,
        padding=padding,
        strides=1,
        dropout=dropout,
        dropout_type=dropout_type,
    )

    bottleneck = tf.keras.layers.Conv2D(
        filters, kernel_size=(1, 1), padding=padding, strides=strides
    )(x)
    bottleneck = batchnorm_act(bottleneck)

    return tf.keras.layers.Add()([bottleneck, res])


# -----------------------------------
def conv2d_block(
    inputs,
    use_batch_norm=True,
    dropout=0.1,
    dropout_type="standard",
    filters=16,
    kernel_size=(2, 2),
    activation="relu",
    strides=(1, 1),
    kernel_initializer="he_normal",
    padding="same",
):

    if dropout_type == "spatial":
        DO = tf.keras.layers.SpatialDropout2D
    elif dropout_type == "standard":
        DO = tf.keras.layers.Dropout
    else:
        raise ValueError(
            f"dropout_type must be one of ['spatial', 'standard'], got {dropout_type}"
        )

    c = tf.keras.layers.Conv2D(
        filters,
        kernel_size,
        activation=activation,
        kernel_initializer=kernel_initializer,
        padding=padding,
        strides=strides,
        use_bias=not use_batch_norm,
    )(inputs)

    if use_batch_norm:
        c = tf.keras.layers.BatchNormalization()(c)
    if dropout > 0.0:
        c = DO(dropout)(c)

    c = tf.keras.layers.Conv2D(
        filters,
        kernel_size,
        activation=activation,
        kernel_initializer=kernel_initializer,
        padding=padding,
        strides=strides,
        use_bias=not use_batch_norm,
    )(c)

    if use_batch_norm:
        c = tf.keras.layers.BatchNormalization()(c)
    return c


# -----------------------------------
def res_conv2d_block(
    inputs,
    use_batch_norm=True,
    dropout=0.1,
    dropout_type="standard",
    filters=16,
    kernel_size=(2, 2),
    activation="relu",
    strides=(1, 1),
    kernel_initializer="he_normal",
    padding="same",
):

    res = conv2d_block(
        inputs=inputs,
        use_batch_norm=use_batch_norm,
        dropout=dropout,
        dropout_type=dropout_type,
        filters=filters,
        kernel_size=kernel_size,
        activation=activation,
        strides=strides,
        kernel_initializer="he_normal",
        padding="same",
    )

    res = conv2d_block(
        inputs=res,
        use_batch_norm=use_batch_norm,
        dropout=dropout,
        dropout_type=dropout_type,
        filters=filters,
        kernel_size=kernel_size,
        activation=activation,
        strides=(1, 1),
        kernel_initializer="he_normal",
        padding="same",
    )

    bottleneck = tf.keras.layers.Conv2D(
        filters, kernel_size=(1, 1), padding=padding, strides=strides
    )(
        inputs
    )  ##kernel_size
    bottleneck = batchnorm_act(bottleneck)

    return tf.keras.layers.Add()([bottleneck, res])


# -----------------------------------
def batchnorm_act(x):
    """
    batchnorm_act(x)
    This function applies batch normalization to a keras model layer, `x`, then a relu activation function
    INPUTS:
        * `z` : keras model layer (should be the output of a convolution or an input layer)
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * batch normalized and relu-activated `x`
    """
    x = tf.keras.layers.BatchNormalization()(x)
    return tf.keras.layers.Activation("relu")(x)


###############################################################
### LOSSES AND METRICS
###############################################################

# -----------------------------------

#define the basic IOU formula. 
def basic_iou(y_true, y_pred):
    smooth = 10e-6
    y_true_f = tf.reshape(tf.dtypes.cast(y_true, tf.float32), [-1])
    y_pred_f = tf.reshape(tf.dtypes.cast(y_pred, tf.float32), [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    union =  tf.reduce_sum(y_true_f + y_pred_f) - intersection
    return (intersection+smooth)/(union+ smooth)

#define the IoU metric for nclasses
def iou_multi(nclasses):
    """
    mean_iou(y_true, y_pred)
    This function computes the mean IoU between `y_true` and `y_pred`: this version is tensorflow (not numpy) and is used by tensorflow training and evaluation functions

    INPUTS:
        * y_true: true masks, one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
        * y_pred: predicted masks, either softmax outputs, or one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * IoU score [tensor]
    """
    def mean_iou(y_true, y_pred):
        iousum = 0
        y_pred = tf.one_hot(tf.argmax(y_pred, -1), nclasses)
        for index in range(nclasses):
            iousum += basic_iou(y_true[:,:,:,index], y_pred[:,:,:,index])
        return iousum/nclasses

    return mean_iou

# -----------------------------------
#define basic Dice formula
# @tf.autograph.experimental.do_not_convert
def basic_dice_coef(y_true, y_pred):
    """
    dice_coef(y_true, y_pred)

    This function computes the mean Dice coefficient between `y_true` and `y_pred`: this version is tensorflow (not numpy) and is used by tensorflow training and evaluation functions

    INPUTS:
        * y_true: true masks, one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
        * y_pred: predicted masks, either softmax outputs, or one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * Dice score [tensor]
    """
    smooth = 10e-6
    y_true_f = tf.reshape(tf.dtypes.cast(y_true, tf.float32), [-1])
    y_pred_f = tf.reshape(tf.dtypes.cast(y_pred, tf.float32), [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    dice = (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)
    return dice

#define Dice formula for multiple classes
# @tf.autograph.experimental.do_not_convert
def dice_multi(nclasses):

    def dice_coef(y_true, y_pred):
        dice = 0
        #can't have an argmax in a loss
        for index in range(nclasses):
            dice += basic_dice_coef(y_true[:,:,:,index], y_pred[:,:,:,index])
        return dice/nclasses

    return dice_coef

# ---------------------------------------------------
#define Dice loss for multiple classes
# @tf.autograph.experimental.do_not_convert
def dice_coef_loss(nclasses):
    """
    dice_coef_loss(y_true, y_pred)

    This function computes the mean Dice loss (1 - Dice coefficient) between `y_true` and `y_pred`: this version is tensorflow (not numpy) and is used by tensorflow training and evaluation functions

    INPUTS:
        * y_true: true masks, one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
        * y_pred: predicted masks, either softmax outputs, or one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * Dice loss [tensor]
    """
    def MC_dice_coef_loss(y_true, y_pred):
        dice = 0
        #can't have an argmax in a loss
        for index in range(nclasses):
            dice += basic_dice_coef(y_true[:,:,:,index], y_pred[:,:,:,index])
        return 1 - (dice/nclasses)

    return MC_dice_coef_loss

#define weighted Dice loss for multiple classes
# @tf.autograph.experimental.do_not_convert
def weighted_dice_coef_loss(nclasses, weights):
    """
    weighted_MC_dice_coef_loss(y_true, y_pred)

    This function computes the mean Dice loss (1 - Dice coefficient) between `y_true` and `y_pred`: this version is tensorflow (not numpy) and is used by tensorflow training and evaluation functions

    INPUTS:
        * y_true: true masks, one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
        * y_pred: predicted masks, either softmax outputs, or one-hot encoded.
            * Inputs are B*W*H*N tensors, with
                B = batch size,
                W = width,
                H = height,
                N = number of classes
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: None
    OUTPUTS:
        * Dice loss [tensor]
    """

    def weighted_MC_dice_coef_loss(y_true, y_pred):
        dice = 0
        #can't have an argmax in a loss
        for index in range(nclasses):
            dice += basic_dice_coef(y_true[:,:,:,index], y_pred[:,:,:,index])*weights[index]
        meandice = (dice/nclasses)
        return 1 - meandice

    return weighted_MC_dice_coef_loss

def mean_iou_np(y_true, y_pred, nclasses):
    iousum = 0
    y_pred = tf.one_hot(tf.argmax(y_pred, -1), nclasses)
    for index in range(nclasses):
        iousum += basic_iou(y_true[:,:,:,index], y_pred[:,:,:,index])
    return (iousum/nclasses).numpy()


def mean_dice_np(y_true, y_pred, nclasses):
    dice = 0
    #can't have an argmax in a loss
    for index in range(nclasses):
        dice += basic_dice_coef(y_true[:,:,:,index], y_pred[:,:,:,index])
    return (dice/nclasses).numpy()

