#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# David Yambay <yambayda@gmail.com>
# Fri March 14 14:57:28 CET 2014

"""
The Livdet 2013 Fingerprint Liveness Database is a fingerprint liveness database which consists of four sub-sets, which contain live and fake fingerprint images from four capture devices. Images have been collected by a consensual approach and using different materials for the artificial reproduction of the fingerprint (gelatine, silicone, play-doh, ecoflex, body double, wood glue).

DATA SET
 	Scanner 	Model 	        Res (dpi) 	Image size 	Live samples 	Fake samples
1 	Biometrika 	FX2000       	569 	    312X372 	2000 	        2000
2 	Italdata 	ET10 	        500 	    640X480 	2000 	        2000
3 	Crossmatch 	L SCAN GUARDIAN 500 	    640X480 	2500 	        2000
4 	Swipe 		                96 		                2374 	        1979


The actual raw data for the database should be downloaded from the original
URL. This package only contains the `Bob <http://www.idiap.ch/software/bob/>`_
accessor methods to use the DB directly from python, with our certified
protocols.

References::

1. L. Ghiani, D. Yambay, V. Mura, S. Tocco, G.L. Marcialis, F. Roli, and S. Schuckers, LivDet 2013 -  Fingerprint Liveness Detection Competition 2013, 6th IAPR/IEEE Int. Conf. on Biometrics, June, 4-7, 2013, Madrid (Spain).
""""

import os
import six
from .models import *

class Database(object):

  protocols = ('Biometrika','CrossMatch','Italdata','Swipe')
  groups = ('train', 'test')
  classes = ('live', 'spoof')

  def __init__(self):
    from .driver import Interface
    from pkg_resources import resource_filename
    self.info = Interface()
    self.location = resource_filename(__name__, '')


  def objects(self, protocols=None, groups=None, classes=None):
    """Returns a list of unique :py:class:`.File` objects for the specific query by the user.

    Keyword Parameters:

    protocols
      The '

    groups
      One of the protocolar subgroups of data as specified in the tuple groups,
      or a tuple with several of them.  If you set this parameter to an empty
      string or the value None, we use reset it to the default which is to get
      all.

    classes
      Either "spoof", "live" or any combination of those (in a tuple). Defines
      the class of data to be retrieved.  If you set this parameter to an empty
      string or the value None, we use reset it to the default, ("live",
      "spoof").




    Returns: A list of :py:class:`.File` objects.

    """

    def check_validity(l, obj, valid, default):
      """Checks validity of user input data against a set of valid values"""
      if not l: return default
      elif isinstance(l, six.string_types): return check_validity((l,), obj, valid, default)
      for k in l:
        if k not in valid:
          raise RuntimeError('Invalid %s "%s". Valid values are %s, or lists/tuples of those' % (obj, k, valid))
      return l

    # check if protocols are valid
    VALID_PROTOCOLS = Database.protocols
    protocols = check_validity(protocols, "protocol", VALID_PROTOCOLS, VALID_PROTOCOLS)

    # check if groups set are valid
    VALID_GROUPS = Database.groups
    groups = check_validity(groups, "group", VALID_GROUPS, VALID_GROUPS)

    # 
    VALID_CLASSES = Database.classes
    classes = check_validity(classes, "class", VALID_CLASSES, VALID_CLASSES)

    retval = []

    for p in protocols:
      for g in groups:
        for c in classes:
          file_list = os.path.join(self.location,p,g,c+'.txt')
          retval += [File(k.strip()) for k in open(file_list, 'r').readlines() if k.strip()]

    return retval

