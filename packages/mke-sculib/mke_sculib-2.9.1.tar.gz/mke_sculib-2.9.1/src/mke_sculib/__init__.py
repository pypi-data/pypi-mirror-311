__version__ = '2.9.1'

import mke_sculib.scu 
from mke_sculib.scu import scu as scu_api
from mke_sculib.scu import load as _load
from mke_sculib.scu import plot_tt, print_color, colors, log, link_stellarium, activate_logging_mattermost
from mke_sculib.sim import scu_sim
from mke_sculib.stellarium_api import stellarium_api as stellar_api
from mke_sculib.sim import plot_motion_pyplot as plot_motion
from mke_sculib.helpers import get_utcnow, make_zulustr, parse_zulutime

from astropy.time import Time
import astropy.units as u
from astropy.coordinates import EarthLocation, get_sun, AltAz, get_moon

def load(antenna_id='', readonly=False, use_socket=True, debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):

    if not "requests" in locals():
        import requests
    if not "json" in locals():
        import json    

    log(f'INFO you are using mke_sculib version:"{__version__}" @ file_location:"{__file__}"', color=colors.OKBLUE)

    if antenna_id == 'test_antenna' or antenna_id == 'sim':
        return scu_sim(str(antenna_id), debug=debug, **kwargs)
    else:
        return _load(antenna_id, readonly=readonly, use_socket=use_socket, debug=debug, url_qry=url_qry, **kwargs)