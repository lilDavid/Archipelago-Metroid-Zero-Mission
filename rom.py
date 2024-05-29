"""
Classes and functions related to creating a ROM patch
"""
import hashlib

from worlds.Files import APDeltaPatch

MD5_MZMUS = "EBBCE58109988B6DA61EBB06C7A432D5"


class MZMDeltaPatch(APDeltaPatch):
    game = "Metroid Zero Mission"
    hash = MD5_MZMUS
    patch_file_ending = ".apmzm"
    result_file_ending = ".gba"
