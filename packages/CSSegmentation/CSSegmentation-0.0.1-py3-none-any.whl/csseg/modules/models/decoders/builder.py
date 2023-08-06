'''
Function:
    Implementation of BuildDecoder
Author:
    Zhenchao Jin
'''
import copy
from .aspphead import ASPPHead


'''BuildDecoder'''
def BuildDecoder(decoder_cfg):
    decoder_cfg = copy.deepcopy(decoder_cfg)
    # supported decoders
    supported_decoders = {
        'ASPPHead': ASPPHead,
    }
    # parse
    decoder_type = decoder_cfg.pop('type')
    decoder = supported_decoders[decoder_type](**decoder_cfg)
    # return
    return decoder