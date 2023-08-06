from . import models
from . import pipelines

from .models.ann import configuration_ann
from .models.ann import feature_extraction_ann
from .models.ann import modeling_ann

from .models.cnn import configuration_cnn
from .models.cnn import modeling_cnn
from .models.cnn import image_processing_cnn

from .models.custom_bert import configuration_custom_bert
from .models.custom_bert import modeling_custom_bert

from .models.custom_wav2vec2 import feature_extraction_custom_wav2vec2

from .models.embedded_1dcnn import configuration_embedded_1dcnn
from .models.embedded_1dcnn import modeling_embedded_1dcnn

from .models.embedded_rnn import configuration_embedded_rnn
from .models.embedded_rnn import modeling_embedded_rnn
from .models.embedded_rnn import tokenization_embedded_rnn

from .models.faster_rcnn import configuration_faster_rcnn
from .models.faster_rcnn import modeling_faster_rcnn
from .models.faster_rcnn import image_processing_faster_rcnn

from .models.rnn import configuration_rnn
from .models.rnn import modeling_rnn

from .pipelines import tabular_regression_pipeline
from .pipelines import tabular_binary_classification_pipeline
from .pipelines import tabular_classification_pipeline
from .pipelines import custom_image_classification_pipeline
from .pipelines import fixed_length_translation_pipeline

def register_auto():
    configuration_ann.register_auto()
    modeling_ann.register_auto()
    feature_extraction_ann.register_auto()

    configuration_cnn.register_auto()
    modeling_cnn.register_auto()
    image_processing_cnn.register_auto()

    configuration_custom_bert.register_auto()
    modeling_custom_bert.register_auto()

    feature_extraction_custom_wav2vec2.register_auto()

    configuration_embedded_1dcnn.register_auto()
    modeling_embedded_1dcnn.register_auto()

    configuration_embedded_rnn.register_auto()
    modeling_embedded_rnn.register_auto()
    tokenization_embedded_rnn.register_auto()

    configuration_faster_rcnn.register_auto()
    modeling_faster_rcnn.register_auto()
    image_processing_faster_rcnn.register_auto()

    configuration_rnn.register_auto()
    modeling_rnn.register_auto()

    tabular_regression_pipeline.register_pipeline()
    tabular_binary_classification_pipeline.register_pipeline()
    tabular_classification_pipeline.register_pipeline()
    custom_image_classification_pipeline.register_pipeline()
    fixed_length_translation_pipeline.register_pipeline()
