'''
Function:
    Implementation of ADE20kDataset
Author:
    Zhenchao Jin
'''
import os
import pandas as pd
from .base import _BaseDataset, BaseDataset


'''_ADE20kDataset'''
class _ADE20kDataset(BaseDataset):
    num_classes = 151
    classnames = [
        '__background__', 'wall', 'building, edifice', 'sky', 'floor, flooring', 'tree', 'ceiling', 'road, route', 'bed', 'windowpane, window', 'grass',
        'cabinet', 'sidewalk, pavement', 'person, individual, someone, somebody, mortal, soul', 'earth, ground', 'door, double door', 'table', 'mountain, mount',
        'plant, flora, plant life', 'curtain, drape, drapery, mantle, pall', 'chair', 'car, auto, automobile, machine, motorcar', 'water', 'painting, picture', 
        'sofa, couch, lounge', 'shelf', 'house', 'sea', 'mirror', 'rug, carpet, carpeting', 'field', 'armchair', 'seat', 'fence, fencing', 'desk', 'rock, stone', 
        'wardrobe, closet, press', 'lamp', 'bathtub, bathing tub, bath, tub', 'railing, rail', 'cushion', 'base, pedestal, stand', 'box', 'column, pillar', 'signboard, sign',
        'chest of drawers, chest, bureau, dresser', 'counter', 'sand', 'sink', 'skyscraper', 'fireplace, hearth, open fireplace', 'refrigerator, icebox',
        'grandstand, covered stand', 'path', 'stairs, steps', 'runway', 'case, display case, showcase, vitrine', 'pool table, billiard table, snooker table', 'pillow',
        'screen door, screen', 'stairway, staircase', 'river', 'bridge, span', 'bookcase', 'blind, screen', 'coffee table, cocktail table', 'toilet, can, commode, crapper, pot, potty, stool, throne',
        'flower', 'book', 'hill', 'bench', 'countertop', 'stove, kitchen stove, range, kitchen range, cooking stove', 'palm, palm tree', 'kitchen island',
        'computer, computing machine, computing device, data processor, electronic computer, information processing system', 'swivel chair', 'boat', 'bar', 'arcade machine',
        'hovel, hut, hutch, shack, shanty', 'bus, autobus, coach, charabanc, double-decker, jitney, motorbus, motorcoach, omnibus, passenger vehicle',
        'towel', 'light, light source', 'truck, motortruck', 'tower', 'chandelier, pendant, pendent', 'awning, sunshade, sunblind', 'streetlight, street lamp', 'booth, cubicle, stall, kiosk',
        'television receiver, television, television set, tv, tv set, idiot box, boob tube, telly, goggle box', 'airplane, aeroplane, plane', 'dirt track',
        'apparel, wearing apparel, dress, clothes', 'pole', 'land, ground, soil', 'bannister, banister, balustrade, balusters, handrail', 'escalator, moving staircase, moving stairway',
        'ottoman, pouf, pouffe, puff, hassock', 'bottle', 'buffet, counter, sideboard', 'poster, posting, placard, notice, bill, card', 'stage', 'van', 'ship', 'fountain',
        'conveyer belt, conveyor belt, conveyer, conveyor, transporter', 'canopy', 'washer, automatic washer, washing machine', 'plaything, toy', 'swimming pool, swimming bath, natatorium',
        'stool', 'barrel, cask', 'basket, handbasket', 'waterfall, falls', 'tent, collapsible shelter', 'bag', 'minibike, motorbike', 'cradle', 'oven', 'ball', 'food, solid food', 'step, stair', 'tank, storage tank',
        'trade name, brand name, brand, marque', 'microwave, microwave oven', 'pot, flowerpot', 'animal, animate being, beast, brute, creature, fauna', 'bicycle, bike, wheel, cycle', 'lake',
        'dishwasher, dish washer, dishwashing machine', 'screen, silver screen, projection screen', 'blanket, cover', 'sculpture', 'hood, exhaust hood', 'sconce', 'vase',
        'traffic light, traffic signal, stoplight', 'tray', 'ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin',
        'fan', 'pier, wharf, wharfage, dock', 'crt screen', 'plate', 'monitor, monitoring device', 'bulletin board, notice board', 'shower', 'radiator', 'glass, drinking glass', 'clock', 'flag'
    ]
    assert num_classes == len(classnames)
    def __init__(self, mode, dataset_cfg):
        super(_ADE20kDataset, self).__init__(mode=mode, dataset_cfg=dataset_cfg)
        # set directory
        rootdir = dataset_cfg['rootdir']
        setmap_dict = {'train': 'training', 'val': 'validation', 'test': 'testing'}
        self.image_dir = os.path.join(rootdir, 'ADEChallengeData2016/images', setmap_dict[dataset_cfg['set']])
        self.ann_dir = os.path.join(rootdir, 'ADEChallengeData2016/annotations', setmap_dict[dataset_cfg['set']])
        # obatin imageids
        df = pd.read_csv(os.path.join(rootdir, 'ADEChallengeData2016', dataset_cfg['set']+'.txt'), names=['imageids'])
        self.imageids = df['imageids'].values
        self.imageids = [str(_id) for _id in self.imageids]


'''ADE20kDataset'''
class ADE20kDataset(BaseDataset):
    tasks = {
        'offline': {
            0: [x for x in range(151)]
        },
        '100-50': {
            0: [x for x in range(0, 101)], 1: [x for x in range(101, 151)]
        },
        '100-10': {
            0: [x for x in range(0, 101)], 1: [x for x in range(101, 111)], 2: [x for x in range(111, 121)],
            3: [x for x in range(121, 131)], 4: [x for x in range(131, 141)], 5: [x for x in range(141, 151)]
        },
        '100-5': {
            0: [x for x in range(0, 101)], 1: [x for x in range(101, 106)], 2: [x for x in range(106, 111)],
            3: [x for x in range(111, 116)], 4: [x for x in range(116, 121)], 5: [x for x in range(121, 126)],
            6: [x for x in range(126, 131)], 7: [x for x in range(131, 136)], 8: [x for x in range(136, 141)],
            9: [x for x in range(141, 146)], 10: [x for x in range(146, 151)]
        },
        '50': {
            0: [x for x in range(0, 51)], 1: [x for x in range(51, 101)], 2: [x for x in range(101, 151)]
        },
    }
    def __init__(self, mode, task_name, task_id, dataset_cfg):
        super(ADE20kDataset, self).__init__(
            mode=mode, task_name=task_name, task_id=task_id, dataset_cfg=dataset_cfg
        )
    '''builddatagenerator'''
    def builddatagenerator(self, mode, dataset_cfg):
        data_generator = _ADE20kDataset(mode, dataset_cfg)
        return data_generator