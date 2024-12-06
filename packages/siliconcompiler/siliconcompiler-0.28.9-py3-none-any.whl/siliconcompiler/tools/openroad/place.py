
from siliconcompiler.tools.openroad.openroad import setup as setup_tool
from siliconcompiler.tools.openroad.openroad import build_pex_corners
from siliconcompiler.tools.openroad.openroad import post_process as or_post_process
from siliconcompiler.tools.openroad.openroad import pre_process as or_pre_process
from siliconcompiler.tools.openroad.openroad import _set_reports, set_pnr_inputs, set_pnr_outputs


def setup(chip):
    '''
    Perform global and detail placements along with design violation repairs
    '''

    # Generic tool setup.
    setup_tool(chip)

    set_pnr_inputs(chip)
    set_pnr_outputs(chip)

    _set_reports(chip, [
        'setup',
        'unconstrained',
        'power',
        'drv_violations',
        'fmax',

        # Images
        'placement_density',
        'routing_congestion',
        'power_density',
        'optimization_placement'
    ])


def pre_process(chip):
    or_pre_process(chip)
    build_pex_corners(chip)


def post_process(chip):
    or_post_process(chip)
