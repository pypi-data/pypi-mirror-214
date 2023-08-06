"""Module for spiral arm functions."""

import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u


def _getSpiralParameters(model):
    # Spiral arm params from Reid et al. (2014)
    reid2014 = {'perseus': {'R_ref': 9.9,  # kpc
                            'beta_ref': 14.2,  # deg (from Galactic center to sun =0)
                            'beta_min': -110.0,  # deg
                            'beta_max': 270.0,  # deg
                            'pitch': 9.9,  # deg
                            'width': 0.38},  # kpc
                'sagittarius': {'R_ref': 6.6,  # kpc
                                'beta_ref': 25.6,  # deg (from Galactic center to sun =0)
                                'beta_min': -110.0,  # deg
                                'beta_max': 270.0,  # deg
                                'pitch': 6.9,  # deg
                                'width': 0.26},  # kpc
                'scutum': {'R_ref': 5.0,  # kpc
                           'beta_ref': 27.6,  # deg (from Galactic center to sun =0)
                           'beta_min': -110.0,  # deg
                           'beta_max': 270.0,  # deg
                           'pitch': 19.8,  # deg
                           'width': 0.17},  # kpc
                'local': {'R_ref': 8.4,  # kpc
                          'beta_ref': 8.9,  # deg (from Galactic center to sun =0)
                          'beta_min': -110.0,  # deg
                          'beta_max': 270.0,  # deg
                          'pitch': 12.8,  # deg
                          'width': 0.33},  # kpc
                'outer': {'R_ref': 13.0,  # kpc
                          'beta_ref': 18.6,  # deg (from Galactic center to sun =0)
                          'beta_min': -110.0,  # deg
                          'beta_max': 270.0,  # deg
                          'pitch': 13.8,  # deg
                          'width': 0.63}}  # kpc


    # Spiral arm params combined from Reid et al. (2019), CK
    custom2019 = {
        'norma1': {'R_ref': 4.46,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': -1.,  # deg
                   'width': 0.14},  # kpc
        'norma0': {'R_ref': 4.46,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 19.5,  # deg
                   'width': 0.14},  # kpc
        'scutum1': {'R_ref': 4.91,  # kpc
                    'beta_ref': 23.,  # deg (from Galactic center to sun =0)
                    'pitch': 14.1,  # deg
                    'width': 0.23},  # kpc
        'scutum1ck': {'R_ref': 4.91,  # kpc
                      'beta_ref': 23.,  # deg (from Galactic center to sun =0)
                      'pitch': 11.1,  # deg
                      'width': 0.23},  # kpc
        'scutum0': {'R_ref': 4.91,  # kpc
                    'beta_ref': 23.,  # deg (from Galactic center to sun =0)
                    'pitch': 12.1,  # deg
                    'width': 0.23},  # kpc
        'sagittarius1': {'R_ref': 6.04,  # kpc
                         'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                         'pitch': 17.1,  # deg
                         'width': 0.27},  # kpc
        'sagittarius1ck': {'R_ref': 6.9,  # kpc
                           'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                           'pitch': 10.,  # deg
                           'width': 0.27},  # kpc
        'sagittarius0': {'R_ref': 6.04,  # kpc
                         'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                         'pitch': 1.0,  # deg
                         'width': 0.27},  # kpc
        'sagittarius0ck': {'R_ref': 6.04,  # kpc
                           'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                           'pitch': 7.0,  # deg
                           'width': 0.27},  # kpc
        'perseus1': {'R_ref': 8.87,  # kpc
                     'beta_ref': 40.0,  # deg (from Galactic center to sun =0)
                     'pitch': 10.3,  # deg
                     'width': 0.35},  # kpc
        'perseus0': {'R_ref': 8.87,  # kpc
                     'beta_ref': 40.0,  # deg (from Galactic center to sun =0)
                     'pitch': 8.7,  # deg
                     'width': 0.35},  # kpc
        'perseus0ck': {'R_ref': 8.87,  # kpc
                       'beta_ref': 40.0,  # deg (from Galactic center to sun =0)
                       'pitch': 12.7,  # deg
                       'width': 0.35},  # kpc
        'local': {'R_ref': 8.26,  # kpc
                  'beta_ref': 9.,  # deg (from Galactic center to sun =0)
                  'pitch': 11.4,  # deg
                  'width': 0.31},  # kpc
        'outer1': {'R_ref': 12.24,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 3.0,  # deg
                   'width': 0.65},  # kpc
        'outer1ck': {'R_ref': 12.24,  # kpc
                     'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                     'pitch': 5.0,  # deg
                     'width': 0.65},  # kpc
        'outer0': {'R_ref': 12.24,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 9.4,  # deg
                   'width': 0.65},  # kpc
        'outer0ck': {'R_ref': 12.24,  # kpc
                     'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                     'pitch': 11.4,  # deg
                     'width': 0.65}}  # kpc

    # Spiral arm params from Reid et al. (2019)
    # TODO: crosscheck with paper and add correct beta bounds
    reid2019 = {
        'norma1': {'R_ref': 4.46,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': -1.,  # deg
                   'width': 0.14},  # kpc
        'norma0': {'R_ref': 4.46,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 19.5,  # deg
                   'width': 0.14},  # kpc
        'scutum1': {'R_ref': 4.91,  # kpc
                    'beta_ref': 23.,  # deg (from Galactic center to sun =0)
                    'pitch': 14.1,  # deg
                    'width': 0.23},  # kpc
        'scutum0': {'R_ref': 4.91,  # kpc
                    'beta_ref': 23.,  # deg (from Galactic center to sun =0)
                    'pitch': 12.1,  # deg
                    'width': 0.23},  # kpc
        'sagittarius1': {'R_ref': 6.04,  # kpc
                         'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                         'pitch': 17.1,  # deg
                         'width': 0.27},  # kpc
        'sagittarius0': {'R_ref': 6.04,  # kpc
                         'beta_ref': 24.0,  # deg (from Galactic center to sun =0)
                         'pitch': 1.0,  # deg
                         'width': 0.27},  # kpc
        'perseus1': {'R_ref': 8.87,  # kpc
                     'beta_ref': 40.0,  # deg (from Galactic center to sun =0)
                     'pitch': 10.3,  # deg
                     'width': 0.35},  # kpc
        'perseus0': {'R_ref': 8.87,  # kpc
                     'beta_ref': 40.0,  # deg (from Galactic center to sun =0)
                     'pitch': 8.7,  # deg
                     'width': 0.35},  # kpc
        'local': {'R_ref': 8.26,  # kpc
                  'beta_ref': 9.,  # deg (from Galactic center to sun =0)
                  'pitch': 11.4,  # deg
                  'width': 0.31},  # kpc
        'outer1': {'R_ref': 12.24,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 3.0,  # deg
                   'width': 0.65},  # kpc
        'outer0': {'R_ref': 12.24,  # kpc
                   'beta_ref': 18.,  # deg (from Galactic center to sun =0)
                   'pitch': 9.4,  # deg
                   'width': 0.65}}  # kpc

    ck = {'perseus': {'R_ref': 10.9,  # kpc
                      'beta_ref': -16.6,  # deg (from Galactic center to sun =0)
                      'beta_min': 180.0,  # deg
                      'beta_max': 280.0,  # deg
                      'pitch': 5.7,  # deg
                      'width': 0.38},  # kpc
          'local': {'R_ref': 9.8,  # kpc
                    'beta_ref': -0.5,  # deg (from Galactic center to sun =0)
                    'beta_min': 180.0,  # deg
                    'beta_max': 280.0,  # deg
                    'pitch': -24,  # deg
                    'width': 0.33},  # kpc
          'outer': {'R_ref': 14.4,  # kpc
                    'beta_ref': -23.5,  # deg (from Galactic center to sun =0)
                    'beta_min': 180.0,  # deg
                    'beta_max': 280.0,  # deg
                    'pitch': 15.8,  # deg
                    'width': 0.63}}  # kpc

    xinyu2016 = {'outer': {'R_ref': 13.6,  # kpc
                           'beta_ref': 26.9,  # deg (from Galactic center to sun =0)
                           'beta_min': -110.0,  # deg
                           'beta_max': 270.0,  # deg
                           'pitch': 13.1,  # deg
                           'width': np.nan}}  # kpc

    vallee2015 = {'perseus': {'R_ref': 7.0,  # kpc
                              'beta_ref': 90.,  # deg (from Galactic center to sun =0)
                              'beta_min': -110.0,  # deg
                              'beta_max': 270.0,  # deg
                              'pitch': 13.,  # deg
                              'width': 0.38},  # kpc
                  'sagittarius': {'R_ref': 7.0,  # kpc
                                  'beta_ref': 0.,  # deg (from Galactic center to sun =0)
                                  'beta_min': -110.0,  # deg
                                  'beta_max': 270.0,  # deg
                                  'pitch': 13.,  # deg
                                  'width': 0.33},  # kpc
                  'scutum': {'R_ref': 7.0,  # kpc
                             'beta_ref': 270.,  # deg (from Galactic center to sun =0)
                             'beta_min': -110.0,  # deg
                             'beta_max': 270.0,  # deg
                             'pitch': 13.,  # deg
                             'width': 0.33},  # kpc
                  'outer': {'R_ref': 7.0,  # kpc
                            'beta_ref': 180.,  # deg (from Galactic center to sun =0)
                            'beta_min': -110.0,  # deg
                            'beta_max': 270.0,  # deg
                            'pitch': 12.5,  # deg
                            'width': 0.63}}  # kpc

    if model == 'reid2014':
        spiral_arm_params = reid2014
    elif model == 'reid2019':
        spiral_arm_params = reid2019
    elif model == 'xinyu2016':
        spiral_arm_params = xinyu2016
    elif model == 'vallee2015':
        spiral_arm_params = vallee2015
    elif model == 'ck':
        spiral_arm_params = ck

    return spiral_arm_params


def getSpiralArmXY(spiral_name, beta_min=-110, beta_max=270., model='reid2014',
                   resolution=0.0001, R_0=8.34):
    spiral_arm_params = _getSpiralParameters(model)

    R_ref = spiral_arm_params[spiral_name]['R_ref']
    beta_ref = spiral_arm_params[spiral_name]['beta_ref']
    pitch = spiral_arm_params[spiral_name]['pitch']
    if beta_min is None:
        beta_min = spiral_arm_params[spiral_name]['beta_min']
    if beta_max is None:
        beta_max = spiral_arm_params[spiral_name]['beta_max']

    beta = np.arange(beta_max, beta_min, -1. * resolution)  # [deg]

    R_gal = R_ref * np.exp(-1 * (beta - beta_ref) * np.pi / 180. * np.tan(np.pi / 180. * pitch))  # kpc

    #     x = R_gal * -1. * np.cos(beta * np.pi/180.)
    #     y = R_gal * np.sin(beta * np.pi/180.)
    x = -1 * R_gal * np.sin((90 - beta) * np.pi / 180.)
    y = R_gal * np.cos((90 - beta) * np.pi / 180.)

    arm = SkyCoord(frame='galactocentric', x=x*u.kpc, y=y*u.kpc, z=0.0*u.kpc,
                   galcen_distance=R_0*u.kpc,
                   galcen_coord=SkyCoord(frame='galactic', l=0*u.deg, b=0*u.deg).icrs,
                   z_sun=0.*u.kpc,
                   roll=0.).galactocentric
    return arm


def getSpiralArmsDetail(model='reid2019'):

    # if model=='optimized':
    #     # SAGITTARIUS arm
    #     svx1, svy1 = getSpiralArmXY('sagittarius', beta_min=-245., beta_max=-2, model='vallee2015')
    #     sx, sy = getSpiralArmXY('sagittarius', beta_min=-2, beta_max=68, model='reid2014')
    #     svx2, svy2 = getSpiralArmXY('sagittarius', beta_min=68, beta_max=225, model='vallee2015')
    #
    #     # SCUTUM arm
    #     scx, scy = getSpiralArmXY('scutum', beta_min=3, beta_max=101)
    #     scvx, scvy = getSpiralArmXY('scutum', beta_min=35, beta_max=363, model='vallee2015')
    #     scvx2, scvy2 = getSpiralArmXY('scutum', beta_min=461, beta_max=560, model='vallee2015')
    #
    #     # OUTER arm
    #     ox, oy = getSpiralArmXY('outer', beta_min=-6, beta_max=56)
    #     ovx, ovy = getSpiralArmXY('outer', beta_min=56, beta_max=410, model='vallee2015')
    #     ockx, ocky = getSpiralArmXY('outer', beta_min=-70, beta_max=-6, model='ck')
    #
    #     # PERSEUS spiral arm
    #     px, py = getSpiralArmXY('perseus', beta_min=-21, beta_max=88)
    #     pvx, pvy = getSpiralArmXY('perseus', beta_min=90, beta_max=390, model='vallee2015')
    #     pckx, pcky = getSpiralArmXY('perseus', beta_min=-40, beta_max=-10, model='ck')
    #     pvx2, pvy2 = getSpiralArmXY('perseus', beta_min=-160, beta_max=-40, model='vallee2015')
    #
    #     return sy, sx, svy1, svx1, svy2, svx2, scy, scx, scvy, scvx, scvy2, scvx2, oy, ox, ovy, ovx, ocky, ockx, py, px, pvy, pvx, pvy2, pvx2, pcky, pckx
    # else:

    # SAGITTARIUS arm
    # svx1, svy1 = getSpiralArmXY('sagittarius', beta_min=-245., beta_max=-2, model=model)
    # sx, sy = getSpiralArmXY('sagittarius', beta_min=-2, beta_max=68, model=model)
    # svx2, svy2 = getSpiralArmXY('sagittarius', beta_min=68, beta_max=225, model=model)
    # sag_x = list(svx1)+list(sx)+list(svx2)
    # sag_y = list(svy1)+list(sy)+list(svy2)
    sagittarius = getSpiralArmXY('sagittarius', beta_min=-245., beta_max=225, model=model)

    # SCUTUM arm
    # scx, scy = getSpiralArmXY('scutum', beta_min=3, beta_max=101, model=model)
    # scvx, scvy = getSpiralArmXY('scutum', beta_min=101, beta_max=363, model=model)
    # scvx2, scvy2 = getSpiralArmXY('scutum', beta_min=363, beta_max=560, model=model)
    # scutum_x = list(scx)+list(scvx)+list(scvx2)
    # scutum_y = list(scy)+list(scvy)+list(scvy2)
    scutum = getSpiralArmXY('scutum', beta_min=3, beta_max=560, model=model)

    # OUTER arm
    # ockx, ocky = getSpiralArmXY('outer', beta_min=-70, beta_max=-6, model=model)
    # ox, oy = getSpiralArmXY('outer', beta_min=-6, beta_max=56, model=model)
    # ovx, ovy = getSpiralArmXY('outer', beta_min=56, beta_max=410, model=model)
    # outer_x = list(ockx) + list(ox) + list(ovx)
    # outer_y = list(ocky) + list(oy) + list(ovy)
    outer = getSpiralArmXY('outer', beta_min=-70, beta_max=410, model=model)

    # PERSEUS spiral arm
    # pvx2, pvy2 = getSpiralArmXY('perseus', beta_min=-160, beta_max=-40, model=model)
    # pckx, pcky = getSpiralArmXY('perseus', beta_min=-40, beta_max=-10, model=model)
    # px, py = getSpiralArmXY('perseus', beta_min=-10, beta_max=90, model=model)
    # pvx, pvy = getSpiralArmXY('perseus', beta_min=90, beta_max=390, model=model)
    # per_x = list(pckx) + list(pvx2) + list(px) + list(pvx)
    # per_y = list(pcky) + list(pvy2) + list(py) + list(pvy)
    perseus = getSpiralArmXY('perseus', beta_min=-160, beta_max=390, model=model)

    return sagittarius, scutum, outer, perseus


def getSpiralArms(model='vallee2015'):
    sagittarius, scutum, outer, perseus = getSpiralArmsDetail(model=model)

    return {'sagittarius': sagittarius,
            'scutum': scutum,
            'perseus': perseus,
            'outer': outer}
    #
    # return {'sagittarius': {'x': list(svx1) + list(sx) + list(svx2),
    #                         'y': list(svy1) + list(sy) + list(svy2)},
    #         'scutum': {'x': list(scvx) + list(scx) + list(scvx2),
    #                    'y': list(scvy) + list(scy) + list(scvy2)},
    #         'perseus': {'x': list(pvx) + list(px) + list(pckx) + list(pvx2),
    #                     'y': list(pvy) + list(py) + list(pcky) + list(pvy2)},
    #         'outer': {'x': list(ovx) + list(ox) + list(ockx),
    #                   'y': list(ovy) + list(oy) + list(ocky)}}
