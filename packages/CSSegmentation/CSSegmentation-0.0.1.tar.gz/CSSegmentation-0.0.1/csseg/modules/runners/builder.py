'''
Function:
    Implementation of BuildRunner
Author:
    Zhenchao Jin
'''
import copy
from .mib import MIBRunner
from .plop import PLOPRunner
from .rcil import RCILRunner


'''BuildRunner'''
def BuildRunner(mode, cmd_args, runner_cfg):
    runner_cfg = copy.deepcopy(runner_cfg)
    # supported runners
    supported_runners = {
        'MIBRunner': MIBRunner,
        'PLOPRunner': PLOPRunner,
        'RCILRunner': RCILRunner,
    }
    # parse
    runner_type = runner_cfg.pop('type')
    runner = supported_runners[runner_type](mode=mode, cmd_args=cmd_args, runner_cfg=runner_cfg)
    # return
    return runner