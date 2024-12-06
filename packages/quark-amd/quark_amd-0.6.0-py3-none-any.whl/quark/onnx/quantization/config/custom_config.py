#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import copy
from typing import Dict, Any

from quark.onnx.quantization.config.config import QuantizationConfig

from onnxruntime.quantization.calibrate import CalibrationMethod
from onnxruntime.quantization.quant_utils import QuantType, QuantFormat

from quark.onnx.quant_utils import PowerOfTwoMethod, VitisQuantType, VitisQuantFormat

DEFAULT_ADAROUND_PARAMS = {
    'DataSize': 1000,
    'FixedSeed': 1705472343,
    'BatchSize': 2,
    'NumIterations': 1000,
    'LearningRate': 0.1,
    'OptimAlgorithm': 'adaround',
    'OptimDevice': 'cpu',
    'EarlyStop': True,
}

DEFAULT_ADAQUANT_PARAMS = {
    'DataSize': 1000,
    'FixedSeed': 1705472343,
    'BatchSize': 2,
    'NumIterations': 1000,
    'LearningRate': 0.00001,
    'OptimAlgorithm': 'adaquant',
    'OptimDevice': 'cpu',
    'EarlyStop': True,
}

# configs for pro
UINT8_DYNAMIC_QUANT_CONFIG = QuantizationConfig(weight_type=QuantType.QUInt8, use_dynamic_quant=True)

XINT8_CONFIG = QuantizationConfig(calibrate_method=PowerOfTwoMethod.MinMSE,
                                  activation_type=QuantType.QUInt8,
                                  weight_type=QuantType.QInt8,
                                  enable_npu_cnn=True,
                                  extra_options={'ActivationSymmetric': True})

XINT8_WEIGHTSONLY_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=PowerOfTwoMethod.MinMSE,
                                                       activation_type=QuantType.QUInt8,
                                                       weight_type=QuantType.QInt8,
                                                       enable_npu_cnn=True,
                                                       include_fast_ft=True,
                                                       extra_options={
                                                           'ActivationSymmetric': True,
                                                           'WeightsOnly': True,
                                                           'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                                       })

XINT8_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=PowerOfTwoMethod.MinMSE,
                                           activation_type=QuantType.QUInt8,
                                           weight_type=QuantType.QInt8,
                                           enable_npu_cnn=True,
                                           include_fast_ft=True,
                                           extra_options={
                                               'ActivationSymmetric': True,
                                               'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                           })

XINT8_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=PowerOfTwoMethod.MinMSE,
                                           activation_type=QuantType.QUInt8,
                                           weight_type=QuantType.QInt8,
                                           enable_npu_cnn=True,
                                           include_fast_ft=True,
                                           extra_options={
                                               'ActivationSymmetric': True,
                                               'FastFinetune': DEFAULT_ADAQUANT_PARAMS
                                           })

S8S8_AAWS_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                      quant_format=QuantFormat.QDQ,
                                      activation_type=QuantType.QInt8,
                                      weight_type=QuantType.QInt8,
                                      extra_options={'Percentile': 99.9999})

S8S8_AAWS_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                               quant_format=QuantFormat.QDQ,
                                               activation_type=QuantType.QInt8,
                                               weight_type=QuantType.QInt8,
                                               include_fast_ft=True,
                                               extra_options={
                                                   'Percentile': 99.9999,
                                                   'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                               })

S8S8_AAWS_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                               quant_format=QuantFormat.QDQ,
                                               activation_type=QuantType.QInt8,
                                               weight_type=QuantType.QInt8,
                                               include_fast_ft=True,
                                               extra_options={
                                                   'Percentile': 99.9999,
                                                   'FastFinetune': DEFAULT_ADAQUANT_PARAMS
                                               })

U8S8_AAWS_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                      quant_format=QuantFormat.QDQ,
                                      activation_type=QuantType.QUInt8,
                                      weight_type=QuantType.QInt8)

U8S8_AAWS_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                               quant_format=QuantFormat.QDQ,
                                               activation_type=QuantType.QUInt8,
                                               weight_type=QuantType.QInt8,
                                               include_fast_ft=True,
                                               extra_options={'FastFinetune': DEFAULT_ADAROUND_PARAMS})

U8S8_AAWS_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                               quant_format=QuantFormat.QDQ,
                                               activation_type=QuantType.QUInt8,
                                               weight_type=QuantType.QInt8,
                                               include_fast_ft=True,
                                               extra_options={'FastFinetune': DEFAULT_ADAQUANT_PARAMS})

S16S8_ASWS_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                       quant_format=VitisQuantFormat.QDQ,
                                       activation_type=VitisQuantType.QInt16,
                                       weight_type=QuantType.QInt8,
                                       extra_options={'ActivationSymmetric': True})

S16S8_ASWS_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                quant_format=VitisQuantFormat.QDQ,
                                                activation_type=VitisQuantType.QInt16,
                                                weight_type=QuantType.QInt8,
                                                include_fast_ft=True,
                                                extra_options={
                                                    'ActivationSymmetric': True,
                                                    'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                                })

S16S8_ASWS_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                quant_format=VitisQuantFormat.QDQ,
                                                activation_type=VitisQuantType.QInt16,
                                                weight_type=QuantType.QInt8,
                                                include_fast_ft=True,
                                                extra_options={
                                                    'ActivationSymmetric': True,
                                                    'FastFinetune': DEFAULT_ADAQUANT_PARAMS
                                                })

U16S8_AAWS_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                       quant_format=VitisQuantFormat.QDQ,
                                       activation_type=VitisQuantType.QUInt16,
                                       weight_type=QuantType.QInt8)

U16S8_AAWS_ADAROUND_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                quant_format=VitisQuantFormat.QDQ,
                                                activation_type=VitisQuantType.QUInt16,
                                                weight_type=QuantType.QInt8,
                                                include_fast_ft=True,
                                                extra_options={'FastFinetune': DEFAULT_ADAROUND_PARAMS})

U16S8_AAWS_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                quant_format=VitisQuantFormat.QDQ,
                                                activation_type=VitisQuantType.QUInt16,
                                                weight_type=QuantType.QInt8,
                                                include_fast_ft=True,
                                                extra_options={'FastFinetune': DEFAULT_ADAQUANT_PARAMS})

BF16_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                 quant_format=VitisQuantFormat.QDQ,
                                 activation_type=VitisQuantType.QBFloat16,
                                 weight_type=VitisQuantType.QBFloat16)

BFP16_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                  quant_format=VitisQuantFormat.BFPFixNeuron,
                                  extra_options={
                                      'BFPAttributes': {
                                          'bfp_method': "to_bfp",
                                          'axis': 1,
                                          'bit_width': 16,
                                          'block_size': 8,
                                          'rounding_mode': 0,
                                      }
                                  })

BFP16_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                           quant_format=VitisQuantFormat.BFPFixNeuron,
                                           include_fast_ft=True,
                                           extra_options={
                                               'BFPAttributes': {
                                                   'bfp_method': "to_bfp",
                                                   'axis': 1,
                                                   'bit_width': 16,
                                                   'block_size': 8,
                                                   'rounding_mode': 0,
                                               },
                                               'FastFinetune': {
                                                   'DataSize': 100,
                                                   'FixedSeed': 1705472343,
                                                   'BatchSize': 5,
                                                   'NumIterations': 100,
                                                   'LearningRate': 0.000001,
                                                   'OptimAlgorithm': 'adaquant',
                                                   'OptimDevice': 'cuda:0',
                                                   'InferDevice': 'cuda:0',
                                                   'EarlyStop': True,
                                               }
                                           })

MXINT8_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                   quant_format=VitisQuantFormat.MXFixNeuron,
                                   extra_options={
                                       'MXAttributes': {
                                           'element_dtype': 'MXINT8',
                                           'axis': 1,
                                           'block_size': 8,
                                           'rounding_mode': 0,
                                       },
                                   })

S16S16_MIXED_S8S8_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                              quant_format=VitisQuantFormat.QDQ,
                                              activation_type=VitisQuantType.QInt16,
                                              weight_type=VitisQuantType.QInt16,
                                              include_auto_mp=True,
                                              extra_options={
                                                  'Percentile': 99.9999,
                                                  'Int32Bias': False,
                                                  'AutoMixprecision': {
                                                      'ActTargetQuantType': QuantType.QInt8,
                                                      'WeightTargetQuantType': QuantType.QInt8,
                                                      'OutputIndex': 0,
                                                  }
                                              })

BF16_MIXED_BFP16_ADAQUANT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                                      quant_format=VitisQuantFormat.QDQ,
                                                      activation_type=VitisQuantType.QBFloat16,
                                                      weight_type=VitisQuantType.QBFloat16,
                                                      include_auto_mp=True,
                                                      include_fast_ft=True,
                                                      extra_options={
                                                          'ActivationSymmetric': True,
                                                          'QuantizeBias': False,
                                                          'DedicateDQNode': True,
                                                          'CalibDataSize': 1,
                                                          'AutoMixprecision': {
                                                              'ActTargetQuantType': VitisQuantType.QBFP,
                                                              'WeightTargetQuantType': VitisQuantType.QBFP,
                                                              'OutputIndex': 0,
                                                          },
                                                          'FastFinetune': DEFAULT_ADAQUANT_PARAMS
                                                      })

# configs for amateurs
INT8_CNN_DEFAULT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                             quant_format=QuantFormat.QDQ,
                                             activation_type=QuantType.QUInt8,
                                             weight_type=QuantType.QInt8)

INT16_CNN_DEFAULT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                              quant_format=VitisQuantFormat.QDQ,
                                              activation_type=VitisQuantType.QUInt16,
                                              weight_type=VitisQuantType.QInt16)

INT8_TRANSFORMER_DEFAULT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                                     quant_format=QuantFormat.QDQ,
                                                     activation_type=QuantType.QUInt8,
                                                     weight_type=QuantType.QInt8,
                                                     enable_npu_transformer=True)

INT16_TRANSFORMER_DEFAULT_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.MinMax,
                                                      quant_format=VitisQuantFormat.QDQ,
                                                      activation_type=VitisQuantType.QUInt16,
                                                      weight_type=VitisQuantType.QInt16,
                                                      enable_npu_transformer=True)

INT8_CNN_ACCURATE_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                              quant_format=QuantFormat.QDQ,
                                              activation_type=QuantType.QUInt8,
                                              weight_type=QuantType.QInt8,
                                              include_fast_ft=True,
                                              extra_options={
                                                  'Percentile': 99.9999,
                                                  'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                              })

INT16_CNN_ACCURATE_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                               quant_format=VitisQuantFormat.QDQ,
                                               activation_type=VitisQuantType.QUInt16,
                                               weight_type=VitisQuantType.QInt16,
                                               include_fast_ft=True,
                                               extra_options={
                                                   'Percentile': 99.9999,
                                                   'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                               })

INT8_TRANSFORMER_ACCURATE_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                      quant_format=QuantFormat.QDQ,
                                                      activation_type=QuantType.QUInt8,
                                                      weight_type=QuantType.QInt8,
                                                      enable_npu_transformer=True,
                                                      include_fast_ft=True,
                                                      extra_options={
                                                          'Percentile': 99.9999,
                                                          'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                                      })

INT16_TRANSFORMER_ACCURATE_CONFIG = QuantizationConfig(calibrate_method=CalibrationMethod.Percentile,
                                                       quant_format=VitisQuantFormat.QDQ,
                                                       activation_type=VitisQuantType.QUInt16,
                                                       weight_type=VitisQuantType.QInt16,
                                                       enable_npu_transformer=True,
                                                       include_fast_ft=True,
                                                       extra_options={
                                                           'Percentile': 99.9999,
                                                           'FastFinetune': DEFAULT_ADAROUND_PARAMS
                                                       })

MATMUL_NBITS_CONFIG = QuantizationConfig(extra_options={
    "UseMatMulNBits": True,
    'MatMulNBitsParams': {
        'GroupSize': 128,
        'Symmetric': True,
        'Bits': 4,
        'AccuracyLevel': 1
    }
})
DefaultConfigMapping = {
    # configs for pro
    'UINT8_DYNAMIC_QUANT': UINT8_DYNAMIC_QUANT_CONFIG,
    'XINT8': XINT8_CONFIG,
    'XINT8_ADAROUND': XINT8_ADAROUND_CONFIG,
    'XINT8_ADAQUANT': XINT8_ADAQUANT_CONFIG,
    'S8S8_AAWS': S8S8_AAWS_CONFIG,
    'S8S8_AAWS_ADAROUND': S8S8_AAWS_ADAROUND_CONFIG,
    'S8S8_AAWS_ADAQUANT': S8S8_AAWS_ADAQUANT_CONFIG,
    'U8S8_AAWS': U8S8_AAWS_CONFIG,
    'U8S8_AAWS_ADAROUND': U8S8_AAWS_ADAROUND_CONFIG,
    'U8S8_AAWS_ADAQUANT': U8S8_AAWS_ADAQUANT_CONFIG,
    'S16S8_ASWS': S16S8_ASWS_CONFIG,
    'S16S8_ASWS_ADAROUND': S16S8_ASWS_ADAROUND_CONFIG,
    'S16S8_ASWS_ADAQUANT': S16S8_ASWS_ADAQUANT_CONFIG,
    'U16S8_AAWS': U16S8_AAWS_CONFIG,
    'U16S8_AAWS_ADAROUND': U16S8_AAWS_ADAROUND_CONFIG,
    'U16S8_AAWS_ADAQUANT': U16S8_AAWS_ADAQUANT_CONFIG,
    'BF16': BF16_CONFIG,
    'BFP16': BFP16_CONFIG,
    'BFP16_ADAQUANT': BFP16_ADAQUANT_CONFIG,
    'MXINT8': MXINT8_CONFIG,
    'S16S16_MIXED_S8S8': S16S16_MIXED_S8S8_CONFIG,
    'BF16_MIXED_BFP16_ADAQUANT': BF16_MIXED_BFP16_ADAQUANT_CONFIG,
    # configs for amateur
    'INT8_CNN_DEFAULT': INT8_CNN_DEFAULT_CONFIG,
    'INT16_CNN_DEFAULT': INT16_CNN_DEFAULT_CONFIG,
    'INT8_TRANSFORMER_DEFAULT': INT8_TRANSFORMER_DEFAULT_CONFIG,
    'INT16_TRANSFORMER_DEFAULT': INT16_TRANSFORMER_DEFAULT_CONFIG,
    'INT8_CNN_ACCURATE': INT8_CNN_ACCURATE_CONFIG,
    'INT16_CNN_ACCURATE': INT16_CNN_ACCURATE_CONFIG,
    'INT8_TRANSFORMER_ACCURATE': INT8_TRANSFORMER_ACCURATE_CONFIG,
    'INT16_TRANSFORMER_ACCURATE': INT16_TRANSFORMER_ACCURATE_CONFIG,
    'MATMUL_NBITS': MATMUL_NBITS_CONFIG,
}


def get_default_config_mapping() -> Dict[str, QuantizationConfig]:
    return DefaultConfigMapping


def get_default_config(config_name: str) -> Any:
    if config_name not in DefaultConfigMapping:
        raise ValueError("Unexpected config name: {}".format(config_name))

    return copy.deepcopy(DefaultConfigMapping[config_name])
