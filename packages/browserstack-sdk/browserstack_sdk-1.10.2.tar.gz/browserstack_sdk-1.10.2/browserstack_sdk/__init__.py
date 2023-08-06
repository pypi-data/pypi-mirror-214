# coding: UTF-8
import sys
bstack1l_opy_ = sys.version_info [0] == 2
bstack111_opy_ = 2048
bstack11_opy_ = 7
def bstack1l1l_opy_ (bstack1_opy_):
    global bstack11l_opy_
    stringNr = ord (bstack1_opy_ [-1])
    bstack1ll1_opy_ = bstack1_opy_ [:-1]
    bstack1lll_opy_ = stringNr % len (bstack1ll1_opy_)
    bstackl_opy_ = bstack1ll1_opy_ [:bstack1lll_opy_] + bstack1ll1_opy_ [bstack1lll_opy_:]
    if bstack1l_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack1l1_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1llll111_opy_ = {
	bstack1l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1l1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1l1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1l1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1l1l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1l1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1l1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1l1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1l1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1l1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1l1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1l1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1l1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1l1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1l1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1l1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack11l1ll11_opy_ = [
  bstack1l1l_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1111l_opy_ = {
  bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack1l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack1l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack1l1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack1l1l_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstack1l1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1ll1l1l1_opy_ = {
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1l1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1l1l_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1ll1ll11_opy_ = {
  bstack1l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1l1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1l1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1l1l_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1l1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1l1l11lll_opy_ = [
  bstack1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1l1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1l1l_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1l1l_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1l1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11lllll_opy_ = [
  bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1l1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1l1l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack111l1111_opy_ = [
  bstack1l1l_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1l1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1l1l_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1l1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1l1l_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1l1l_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1l1l_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1l1l_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1l1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1l1l_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1l1l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1l1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1l1l_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1l1l_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1l1l_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1l1l_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1l1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1l1l_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1l1l_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1l1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1l1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1l1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1l1l_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1l1l_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1l1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1l1l_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1l1l_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1l1l_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1l1l_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1l1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1l1l_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1l1l_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1l1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1l1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1l1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1l1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1l1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1l1l_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1l1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1l1l_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1l1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1l1l_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1l1l_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1l1l_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1l1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1l1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1l1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1l1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1l1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1l1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1l1l_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1l1l_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1l1l_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1l1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1l1l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1l1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1l1l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1l1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1111l1l1_opy_ = {
  bstack1l1l_opy_ (u"࠭ࡶࠨच"): bstack1l1l_opy_ (u"ࠧࡷࠩछ"),
  bstack1l1l_opy_ (u"ࠨࡨࠪज"): bstack1l1l_opy_ (u"ࠩࡩࠫझ"),
  bstack1l1l_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1l1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1l1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1l1l_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1l1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1l1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1l1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1l1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1l1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1l1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1l1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1l1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1l1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1l1l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1l1l_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1l1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1l1l_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1l1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1l1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1l1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1l1l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1l11ll11l_opy_ = bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l11l1_opy_ = bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack11111l1_opy_ = bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1l111ll11_opy_ = {
  bstack1l1l_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l1l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack11ll11l_opy_ = bstack1l111ll11_opy_[bstack1l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1l11l1l_opy_ = bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack11l11l11_opy_ = bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1111lll1_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack11llll11_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1l1l1lll_opy_ = [bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1lllll1ll_opy_ = [bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1llll1ll_opy_ = [
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1l1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1l1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1l1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1l1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1l1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1l1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1l1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1l1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1l1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1l1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1l1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1l1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1l1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1l1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1l1l_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1l1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1l1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1l1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1l1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1l1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1l1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1l1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1l1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1l1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1l1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1l1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1l1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1l1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1l1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1l1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1l1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1l1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1l1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1l1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1l1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1l1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1l1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1l1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1l1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1l1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1l1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1l1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1l1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1l1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1l1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1l1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1l1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1l1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1l1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1l1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1l1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1l1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1l1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1l1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1l1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1l1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1l1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1l1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1l1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1l1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1l1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1l1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1l1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1l1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1l1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1l1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1l1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1l1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1l1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1l1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1l1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1l1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1l1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1l1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1l1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1l1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1l1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l111111_opy_ = bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack11l11ll_opy_ = [bstack1l1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1ll11l111_opy_ = [bstack1l1l_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1lll1111_opy_ = {
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1l1lll1ll_opy_ = [
  bstack1l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack11lll1l1_opy_ = bstack11lllll_opy_ + bstack111l1111_opy_ + bstack1llll1ll_opy_
bstack1l1l1l11_opy_ = [
  bstack1l1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack11llll_opy_ = bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1l11l11_opy_ = bstack1l1l_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1llllllll_opy_ = [ bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1ll1ll1l1_opy_ = [ bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1l11111_opy_ = [ bstack1l1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11l1lll_opy_ = bstack1l1l_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1111l1ll_opy_ = bstack1l1l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack111l1ll1_opy_ = bstack1l1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1ll1llll1_opy_ = bstack1l1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1ll1l11ll_opy_ = [
  bstack1l1l_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1l1l_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1l1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1l1l_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1l1l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1l1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1l1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1l1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1l1l_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1l1l_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1l1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1l1l_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1l1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1l1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1l1l_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1l1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1l1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1l1l_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
def bstack1l1llll_opy_():
  global CONFIG
  headers = {
        bstack1l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਧ"): bstack1l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਨ"),
      }
  proxy = bstack11l111l1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ਩")) or CONFIG.get(bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩਪ")):
    proxies = {
      bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬਫ"): proxy
    }
  try:
    response = requests.get(bstack11111l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11llllll1_opy_ = response.json()[bstack1l1l_opy_ (u"ࠧࡩࡷࡥࡷࠬਬ")]
      logger.debug(bstack1lll111l1_opy_.format(response.json()))
      return bstack11llllll1_opy_
    else:
      logger.debug(bstack1l111lll_opy_.format(bstack1l1l_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢਭ")))
  except Exception as e:
    logger.debug(bstack1l111lll_opy_.format(e))
def bstack1llll111l_opy_(hub_url):
  global CONFIG
  url = bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਮ")+  hub_url + bstack1l1l_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥਯ")
  headers = {
        bstack1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪਰ"): bstack1l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ਱"),
      }
  proxy = bstack11l111l1_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩਲ")) or CONFIG.get(bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫਲ਼")):
    proxies = {
      bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ਴"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11ll111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1llll1l11_opy_.format(hub_url, e))
def bstack11l11l_opy_():
  try:
    global bstack1lll111_opy_
    bstack11llllll1_opy_ = bstack1l1llll_opy_()
    with Pool() as pool:
      results = pool.map(bstack1llll111l_opy_, bstack11llllll1_opy_)
    bstack1lll11l_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1l_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪਵ")]
      latency = item[bstack1l1l_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫਸ਼")]
      bstack1lll11l_opy_[hub_url] = latency
    bstack1ll11lll_opy_ = min(bstack1lll11l_opy_, key= lambda x: bstack1lll11l_opy_[x])
    bstack1lll111_opy_ = bstack1ll11lll_opy_
    logger.debug(bstack1l1l1l1l1_opy_.format(bstack1ll11lll_opy_))
  except Exception as e:
    logger.debug(bstack111l11ll_opy_.format(e))
bstack1l1l1l11l_opy_ = bstack1l1l_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫ਷")
bstack11l11l1l_opy_ = bstack1l1l_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨਸ")
bstack1l11l1l1l_opy_ = bstack1l1l_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਹ")
bstack1111111l_opy_ = bstack1l1l_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ਺")
bstack11lllllll_opy_ = bstack1l1l_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ਻")
bstack111l11l1_opy_ = bstack1l1l_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾ਼ࠩ")
bstack1l1111l11_opy_ = bstack1l1l_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ਽")
bstack1ll11_opy_ = bstack1l1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩਾ")
bstack1llll1111_opy_ = bstack1l1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack11ll1_opy_ = bstack1l1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨੀ")
bstack1ll11l_opy_ = bstack1l1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨੁ")
bstack1l1l1lll1_opy_ = bstack1l1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩੂ")
bstack111lll11_opy_ = bstack1l1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠫ੃")
bstack1l11ll111_opy_ = bstack1l1l_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡦࡪࡰࡧࠤࡪ࡯ࡴࡩࡧࡵࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡶࡤࡰࡱࠦࡴࡩࡧࠣࡶࡪࡲࡥࡷࡣࡱࡸࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡪࡲࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠪ੄")
bstack1ll111_opy_ = bstack1l1l_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭੅")
bstack1l11lll_opy_ = bstack1l1l_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨ੆")
bstack11l11111_opy_ = bstack1l1l_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࡣࡱࡽࠥࡶࡡࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡩࠤࠧࢁࡽࠣ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡥࡴࡶࡶ࠲ࠬੇ")
bstack1l1l1ll11_opy_ = bstack1l1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭ੈ")
bstack1lll1111l_opy_ = bstack1l1l_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧ੉")
bstack1lll1_opy_ = bstack1l1l_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧ੊")
bstack1l1ll1l11_opy_ = bstack1l1l_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪੋ")
bstack11ll111_opy_ = bstack1l1l_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11ll_opy_ = bstack1l1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪ੍ࠥࠬ")
bstack111l11_opy_ = bstack1l1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪ੎")
bstack11111l_opy_ = bstack1l1l_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫ੏")
bstack11111l11_opy_ = bstack1l1l_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩ੐")
bstack11l11l1_opy_ = bstack1l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨੑ")
bstack1l111l1_opy_ = bstack1l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧ੒")
bstack1l1lll11l_opy_ = bstack1l1l_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧ੓")
bstack1111llll_opy_ = bstack1l1l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬ੔")
bstack1l1lll11_opy_ = bstack1l1l_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫ੕")
bstack1lll111ll_opy_ = bstack1l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪ੖")
bstack1lllll111_opy_ = bstack1l1l_opy_ (u"ࠨࡇࡻࡴࡪࡩࡴࡦࡦࠣࡥࡹࠦ࡬ࡦࡣࡶࡸࠥ࠷ࠠࡪࡰࡳࡹࡹ࠲ࠠࡳࡧࡦࡩ࡮ࡼࡥࡥࠢ࠳ࠫ੗")
bstack1l1l1l1_opy_ = bstack1l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡳࡴࠥࡻࡰ࡭ࡱࡤࡨ࠳ࠦࡻࡾࠩ੘")
bstack1l11l1l11_opy_ = bstack1l1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡁࡱࡲ࠱ࠤࡎࡴࡶࡢ࡮࡬ࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡿࢂ࠴ࠧਖ਼")
bstack1l11ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡐ࡫ࡹࡴࠢࡦࡥࡳࡴ࡯ࡵࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡦࡹࠠࡢࡲࡳࠤࡻࡧ࡬ࡶࡧࡶ࠰ࠥࡻࡳࡦࠢࡤࡲࡾࠦ࡯࡯ࡧࠣࡴࡷࡵࡰࡦࡴࡷࡽࠥ࡬ࡲࡰ࡯ࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠭ࠢࡲࡲࡱࡿࠠࠣࡲࡤࡸ࡭ࠨࠠࡢࡰࡧࠤࠧࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠣࠢࡦࡥࡳࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡶࡲ࡫ࡪࡺࡨࡦࡴ࠱ࠫਗ਼")
bstack11l1l111_opy_ = bstack1l1l_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠠࡢࡴࡨࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧਜ਼")
bstack1l11l1ll1_opy_ = bstack1l1l_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡕࡸࡴࡵࡵࡲࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࡶࠤࡴ࡬ࠠࡢࡲࡳࠤࡦࡸࡥࠡࡱࡩࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧੜ")
bstack1l1ll11ll_opy_ = bstack1l1l_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡳࡴࠥ࡯ࡤࠡࡽࢀࠤ࡫ࡵࡲࠡࡪࡤࡷ࡭ࠦ࠺ࠡࡽࢀ࠲ࠬ੝")
bstack1l11ll_opy_ = bstack1l1l_opy_ (u"ࠨࡃࡳࡴ࡛ࠥࡰ࡭ࡱࡤࡨࡪࡪࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠠࡊࡆࠣ࠾ࠥࢁࡽࠨਫ਼")
bstack111ll1_opy_ = bstack1l1l_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡃࡳࡴࠥࡀࠠࡼࡿ࠱ࠫ੟")
bstack1l1l1ll1_opy_ = bstack1l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡵࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠯ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡸࡡ࡭࡮ࡨࡰࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡀࠤ࠶࠭੠")
bstack1lll11ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࠽ࠤࢀࢃࠧ੡")
bstack1111ll11_opy_ = bstack1l1l_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡾࢁࠬ੢")
bstack1l1l111l1_opy_ = bstack1l1l_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡲࡦࡣࡶࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡻࡾࠩ੣")
bstack1l1ll111l_opy_ = bstack1l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡡࡱ࡫ࠣࡧࡦࡲ࡬࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ੤")
bstack1l11ll1l1_opy_ = bstack1l1l_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡮࡯ࡸࠢࡥࡹ࡮ࡲࡤࠡࡗࡕࡐ࠱ࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡻࡳࡦࡦ࠱ࠫ੥")
bstack1ll1111l1_opy_ = bstack1l1l_opy_ (u"ࠩࡖࡩࡷࡼࡥࡳࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠠࡪࡵࠣࡲࡴࡺࠠࡴࡣࡰࡩࠥࡧࡳࠡࡥ࡯࡭ࡪࡴࡴࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮࠭੦")
bstack1l111l11l_opy_ = bstack1l1l_opy_ (u"࡚ࠪ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠿ࠦࡻࡾࠩ੧")
bstack1l1l1l1ll_opy_ = bstack1l1l_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡢࡥࡦࡩࡸࡹࠠࡢࠢࡳࡶ࡮ࡼࡡࡵࡧࠣࡨࡴࡳࡡࡪࡰ࠽ࠤࢀࢃࠠ࠯ࠢࡖࡩࡹࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡣࡰࡰࡩ࡭࡬ࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠻ࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠢ࡟ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭࠼ࠣࡸࡷࡻࡥࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠨ੨")
bstack1l111ll_opy_ = bstack1l1l_opy_ (u"࡙ࠬ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࡡࡨࡶࡷࡵࡲࠡ࠼ࠣࡿࢂ࠭੩")
bstack11ll1ll_opy_ = bstack1l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡲࡩࡥࡡ࡮ࡲ࡯࡭ࡹࡻࡤࡦࡡࡨࡺࡪࡴࡴࠡࡨࡲࡶ࡙ࠥࡄࡌࡕࡨࡸࡺࡶࠠࡼࡿࠥ੪")
bstack1ll11111_opy_ = bstack1l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡾࢁࠧ੫")
bstack1l1lll111_opy_ = bstack1l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠤࢀࢃࠢ੬")
bstack1lllll1l_opy_ = bstack1l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯ࡲࡦࡡࡵࡩࡶࡻࡥࡴࡶࠣࡿࢂࠨ੭")
bstack1lllll1l1_opy_ = bstack1l1l_opy_ (u"ࠥࡔࡔ࡙ࡔࠡࡇࡹࡩࡳࡺࠠࡼࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡀࠠࡼࡿࠥ੮")
bstack111ll1l_opy_ = bstack1l1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡴࡷࡵࡸࡺࠢࡶࡩࡹࡺࡩ࡯ࡩࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੯")
bstack1lll111l1_opy_ = bstack1l1l_opy_ (u"ࠬࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠢࡾࢁࠬੰ")
bstack1l111lll_opy_ = bstack1l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢ࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸࡀࠠࡼࡿࠪੱ")
bstack1l1l1l1l1_opy_ = bstack1l1l_opy_ (u"ࠧࡏࡧࡤࡶࡪࡹࡴࠡࡪࡸࡦࠥࡧ࡬࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡶ࠾ࠥࢁࡽࠨੲ")
bstack111l11ll_opy_ = bstack1l1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠠࡊࡐࠣࡅࡑࡒࡏࡄࡃࡗࡉࠥࡎࡕࡃࠢࡾࢁࠬੳ")
bstack11ll111l_opy_ = bstack1l1l_opy_ (u"ࠩࡏࡥࡹ࡫࡮ࡤࡻࠣࡳ࡫ࠦࡨࡶࡤ࠽ࠤࢀࢃࠠࡪࡵ࠽ࠤࢀࢃࠧੴ")
bstack1llll1l11_opy_ = bstack1l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦ࡬ࡢࡶࡨࡲࡨࡿࠠࡧࡱࡵࠤࢀࢃࠠࡩࡷࡥ࠾ࠥࢁࡽࠨੵ")
bstack1l1111ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡍࡻࡢࠡࡷࡵࡰࠥࡩࡨࡢࡰࡪࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥ࠾ࠥࢁࡽࠨ੶")
bstack1l1llll1_opy_ = bstack1l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡱࡳࡸ࡮ࡳࡡ࡭ࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ੷")
bstack1ll1l1ll_opy_ = bstack1l1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭੸")
bstack1l11111l_opy_ = bstack1l1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭੹")
from ._version import __version__
bstack1ll11l11l_opy_ = None
CONFIG = {}
bstack11l111l_opy_ = {}
bstack1l111ll1_opy_ = {}
bstack1ll111ll_opy_ = None
bstack1llllll11_opy_ = None
bstack11ll1l11_opy_ = None
bstack1111_opy_ = -1
bstack1ll1l1l11_opy_ = bstack11ll11l_opy_
bstack1l1l1l_opy_ = 1
bstack1lllll_opy_ = False
bstack1l1ll1111_opy_ = bstack1l1l_opy_ (u"ࠨࠩ੺")
bstack11llll1_opy_ = bstack1l1l_opy_ (u"ࠩࠪ੻")
bstack111l1_opy_ = False
bstack1l1lllll_opy_ = True
bstack1lllll11l_opy_ = bstack1l1l_opy_ (u"ࠪࠫ੼")
bstack1lll11111_opy_ = []
bstack1lll111_opy_ = bstack1l1l_opy_ (u"ࠫࠬ੽")
bstack1ll1111l_opy_ = False
bstack1ll1ll1l_opy_ = False
bstack1l1l111_opy_ = None
bstack1l1l1111_opy_ = None
bstack11l111_opy_ = None
bstack111l1lll_opy_ = None
bstack111ll111_opy_ = None
bstack1lll1ll_opy_ = None
bstack11ll1l_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1ll1l1_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack11111_opy_ = None
bstack1lll1ll1l_opy_ = None
bstack1l1l1ll_opy_ = bstack1l1l_opy_ (u"ࠧࠨ੾")
class bstack1l1l11l1l_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l1l11l1l_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l1l11_opy_,
                    format=bstack1l1l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ੿"),
                    datefmt=bstack1l1l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ઀"))
def bstack11lll_opy_():
  global CONFIG
  global bstack1ll1l1l11_opy_
  if bstack1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઁ") in CONFIG:
    bstack1ll1l1l11_opy_ = bstack1l111ll11_opy_[CONFIG[bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫં")]]
    logging.getLogger().setLevel(bstack1ll1l1l11_opy_)
def bstack1l11l1ll_opy_():
  global CONFIG
  global bstack1ll1ll1l_opy_
  bstack1lll1ll1_opy_ = bstack1lll1ll11_opy_(CONFIG)
  if(bstack1l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઃ") in bstack1lll1ll1_opy_ and str(bstack1lll1ll1_opy_[bstack1l1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭઄")]).lower() == bstack1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪઅ")):
    bstack1ll1ll1l_opy_ = True
def bstack1l111lll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11ll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡣࡰࡰࡩ࡭࡬࡬ࡩ࡭ࡧࠥઆ") == args[i].lower() or bstack1l1l_opy_ (u"ࠢ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡲ࡫࡯ࡧࠣઇ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lllll11l_opy_
      bstack1lllll11l_opy_ += bstack1l1l_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠥ࠭ઈ") + path
      return path
  return None
def bstack111l1ll_opy_():
  bstack11lllll11_opy_ = bstack1l11l1111_opy_()
  if bstack11lllll11_opy_ and os.path.exists(os.path.abspath(bstack11lllll11_opy_)):
    fileName = bstack11lllll11_opy_
  if bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઉ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઊ")])) and not bstack1l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭ઋ") in locals():
    fileName = os.environ[bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")]
  if bstack1l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    bstack11lllll1_opy_ = os.path.abspath(fileName)
  else:
    bstack11lllll1_opy_ = bstack1l1l_opy_ (u"ࠧࠨ઎")
  bstack11111l1l_opy_ = os.getcwd()
  bstack11ll1111_opy_ = bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫએ")
  bstack1ll1l11l1_opy_ = bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭ઐ")
  while (not os.path.exists(bstack11lllll1_opy_)) and bstack11111l1l_opy_ != bstack1l1l_opy_ (u"ࠥࠦઑ"):
    bstack11lllll1_opy_ = os.path.join(bstack11111l1l_opy_, bstack11ll1111_opy_)
    if not os.path.exists(bstack11lllll1_opy_):
      bstack11lllll1_opy_ = os.path.join(bstack11111l1l_opy_, bstack1ll1l11l1_opy_)
    if bstack11111l1l_opy_ != os.path.dirname(bstack11111l1l_opy_):
      bstack11111l1l_opy_ = os.path.dirname(bstack11111l1l_opy_)
    else:
      bstack11111l1l_opy_ = bstack1l1l_opy_ (u"ࠦࠧ઒")
  if not os.path.exists(bstack11lllll1_opy_):
    bstack1ll1l1l_opy_(
      bstack11l11111_opy_.format(os.getcwd()))
  with open(bstack11lllll1_opy_, bstack1l1l_opy_ (u"ࠬࡸࠧઓ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1ll1l1l_opy_(bstack1lll1111l_opy_.format(str(exc)))
def bstack1l1l1_opy_(config):
  bstack11l1111l_opy_ = bstack1l1111lll_opy_(config)
  for option in list(bstack11l1111l_opy_):
    if option.lower() in bstack1111l1l1_opy_ and option != bstack1111l1l1_opy_[option.lower()]:
      bstack11l1111l_opy_[bstack1111l1l1_opy_[option.lower()]] = bstack11l1111l_opy_[option]
      del bstack11l1111l_opy_[option]
  return config
def bstack11111lll_opy_():
  global bstack1l111ll1_opy_
  for key, bstack1ll111l1l_opy_ in bstack1l1111l_opy_.items():
    if isinstance(bstack1ll111l1l_opy_, list):
      for var in bstack1ll111l1l_opy_:
        if var in os.environ:
          bstack1l111ll1_opy_[key] = os.environ[var]
          break
    elif bstack1ll111l1l_opy_ in os.environ:
      bstack1l111ll1_opy_[key] = os.environ[bstack1ll111l1l_opy_]
  if bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨઔ") in os.environ:
    bstack1l111ll1_opy_[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫક")] = {}
    bstack1l111ll1_opy_[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬખ")][bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫગ")] = os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬઘ")]
def bstack11lll1l_opy_():
  global bstack11l111l_opy_
  global bstack1lllll11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l1l_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઙ").lower() == val.lower():
      bstack11l111l_opy_[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩચ")] = {}
      bstack11l111l_opy_[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")][bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩજ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1lll1l1l1_opy_ in bstack1ll1l1l1_opy_.items():
    if isinstance(bstack1lll1l1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll1l1l1_opy_:
          if idx<len(sys.argv) and bstack1l1l_opy_ (u"ࠨ࠯࠰ࠫઝ") + var.lower() == val.lower() and not key in bstack11l111l_opy_:
            bstack11l111l_opy_[key] = sys.argv[idx+1]
            bstack1lllll11l_opy_ += bstack1l1l_opy_ (u"ࠩࠣ࠱࠲࠭ઞ") + var + bstack1l1l_opy_ (u"ࠪࠤࠬટ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l1l_opy_ (u"ࠫ࠲࠳ࠧઠ") + bstack1lll1l1l1_opy_.lower() == val.lower() and not key in bstack11l111l_opy_:
          bstack11l111l_opy_[key] = sys.argv[idx+1]
          bstack1lllll11l_opy_ += bstack1l1l_opy_ (u"ࠬࠦ࠭࠮ࠩડ") + bstack1lll1l1l1_opy_ + bstack1l1l_opy_ (u"࠭ࠠࠨઢ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1lll1lll1_opy_(config):
  bstack1llll1ll1_opy_ = config.keys()
  for bstack1l11llll1_opy_, bstack1111l1l_opy_ in bstack1llll111_opy_.items():
    if bstack1111l1l_opy_ in bstack1llll1ll1_opy_:
      config[bstack1l11llll1_opy_] = config[bstack1111l1l_opy_]
      del config[bstack1111l1l_opy_]
  for bstack1l11llll1_opy_, bstack1111l1l_opy_ in bstack1ll1ll11_opy_.items():
    if isinstance(bstack1111l1l_opy_, list):
      for bstack11lllll1l_opy_ in bstack1111l1l_opy_:
        if bstack11lllll1l_opy_ in bstack1llll1ll1_opy_:
          config[bstack1l11llll1_opy_] = config[bstack11lllll1l_opy_]
          del config[bstack11lllll1l_opy_]
          break
    elif bstack1111l1l_opy_ in bstack1llll1ll1_opy_:
        config[bstack1l11llll1_opy_] = config[bstack1111l1l_opy_]
        del config[bstack1111l1l_opy_]
  for bstack11lllll1l_opy_ in list(config):
    for bstack1111lll_opy_ in bstack11lll1l1_opy_:
      if bstack11lllll1l_opy_.lower() == bstack1111lll_opy_.lower() and bstack11lllll1l_opy_ != bstack1111lll_opy_:
        config[bstack1111lll_opy_] = config[bstack11lllll1l_opy_]
        del config[bstack11lllll1l_opy_]
  bstack1l1lll1l1_opy_ = []
  if bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪણ") in config:
    bstack1l1lll1l1_opy_ = config[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત")]
  for platform in bstack1l1lll1l1_opy_:
    for bstack11lllll1l_opy_ in list(platform):
      for bstack1111lll_opy_ in bstack11lll1l1_opy_:
        if bstack11lllll1l_opy_.lower() == bstack1111lll_opy_.lower() and bstack11lllll1l_opy_ != bstack1111lll_opy_:
          platform[bstack1111lll_opy_] = platform[bstack11lllll1l_opy_]
          del platform[bstack11lllll1l_opy_]
  for bstack1l11llll1_opy_, bstack1111l1l_opy_ in bstack1ll1ll11_opy_.items():
    for platform in bstack1l1lll1l1_opy_:
      if isinstance(bstack1111l1l_opy_, list):
        for bstack11lllll1l_opy_ in bstack1111l1l_opy_:
          if bstack11lllll1l_opy_ in platform:
            platform[bstack1l11llll1_opy_] = platform[bstack11lllll1l_opy_]
            del platform[bstack11lllll1l_opy_]
            break
      elif bstack1111l1l_opy_ in platform:
        platform[bstack1l11llll1_opy_] = platform[bstack1111l1l_opy_]
        del platform[bstack1111l1l_opy_]
  for bstack1l1l1llll_opy_ in bstack1lll1111_opy_:
    if bstack1l1l1llll_opy_ in config:
      if not bstack1lll1111_opy_[bstack1l1l1llll_opy_] in config:
        config[bstack1lll1111_opy_[bstack1l1l1llll_opy_]] = {}
      config[bstack1lll1111_opy_[bstack1l1l1llll_opy_]].update(config[bstack1l1l1llll_opy_])
      del config[bstack1l1l1llll_opy_]
  for platform in bstack1l1lll1l1_opy_:
    for bstack1l1l1llll_opy_ in bstack1lll1111_opy_:
      if bstack1l1l1llll_opy_ in list(platform):
        if not bstack1lll1111_opy_[bstack1l1l1llll_opy_] in platform:
          platform[bstack1lll1111_opy_[bstack1l1l1llll_opy_]] = {}
        platform[bstack1lll1111_opy_[bstack1l1l1llll_opy_]].update(platform[bstack1l1l1llll_opy_])
        del platform[bstack1l1l1llll_opy_]
  config = bstack1l1l1_opy_(config)
  return config
def bstack111lll1_opy_(config):
  global bstack11llll1_opy_
  if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭થ") in config and str(config[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧદ")]).lower() != bstack1l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪધ"):
    if not bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩન") in config:
      config[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ઩")] = {}
    if not bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩપ") in config[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")]:
      bstack111ll1ll_opy_ = datetime.datetime.now()
      bstack1l111l111_opy_ = bstack111ll1ll_opy_.strftime(bstack1l1l_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭બ"))
      hostname = socket.gethostname()
      bstack1111ll_opy_ = bstack1l1l_opy_ (u"ࠪࠫભ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1l_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭મ").format(bstack1l111l111_opy_, hostname, bstack1111ll_opy_)
      config[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")][bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર")] = identifier
    bstack11llll1_opy_ = config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")]
  return config
def bstack1lll11l1l_opy_():
  if (
    isinstance(os.getenv(bstack1l1l_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧળ")), str) and len(os.getenv(bstack1l1l_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઴"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l1l_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠪવ")), str) and len(os.getenv(bstack1l1l_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫશ"))) > 0
  ):
    return os.getenv(bstack1l1l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬષ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠧࡄࡋࠪસ"))).lower() == bstack1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭હ") and str(os.getenv(bstack1l1l_opy_ (u"ࠩࡆࡍࡗࡉࡌࡆࡅࡌࠫ઺"))).lower() == bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻"):
    return os.getenv(bstack1l1l_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓ઼ࠧ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠬࡉࡉࠨઽ"))).lower() == bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫા") and str(os.getenv(bstack1l1l_opy_ (u"ࠧࡕࡔࡄ࡚ࡎ࡙ࠧિ"))).lower() == bstack1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી"):
    return os.getenv(bstack1l1l_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨુ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠪࡇࡎ࠭ૂ"))).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ") and str(os.getenv(bstack1l1l_opy_ (u"ࠬࡉࡉࡠࡐࡄࡑࡊ࠭ૄ"))).lower() == bstack1l1l_opy_ (u"࠭ࡣࡰࡦࡨࡷ࡭࡯ࡰࠨૅ"):
    return 0 # bstack1l1llllll_opy_ bstack11l1ll1l_opy_ not set build number env
  if os.getenv(bstack1l1l_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠪ૆")) and os.getenv(bstack1l1l_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠫે")):
    return os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫૈ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠪࡇࡎ࠭ૉ"))).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ૊") and str(os.getenv(bstack1l1l_opy_ (u"ࠬࡊࡒࡐࡐࡈࠫો"))).lower() == bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ"):
    return os.getenv(bstack1l1l_opy_ (u"ࠧࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ્ࠬ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠨࡅࡌࠫ૎"))).lower() == bstack1l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૏") and str(os.getenv(bstack1l1l_opy_ (u"ࠪࡗࡊࡓࡁࡑࡊࡒࡖࡊ࠭ૐ"))).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑"):
    return os.getenv(bstack1l1l_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠨ૒"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"࠭ࡃࡊࠩ૓"))).lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔") and str(os.getenv(bstack1l1l_opy_ (u"ࠨࡉࡌࡘࡑࡇࡂࡠࡅࡌࠫ૕"))).lower() == bstack1l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖"):
    return os.getenv(bstack1l1l_opy_ (u"ࠪࡇࡎࡥࡊࡐࡄࡢࡍࡉ࠭૗"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠫࡈࡏࠧ૘"))).lower() == bstack1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙") and str(os.getenv(bstack1l1l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡐࡏࡔࡆࠩ૚"))).lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛"):
    return os.getenv(bstack1l1l_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ૜"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠩࡗࡊࡤࡈࡕࡊࡎࡇࠫ૝"))).lower() == bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstack1l1l_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ૟"), 0)
  return -1
def bstack11lll1_opy_(bstack1l1lll1_opy_):
  global CONFIG
  if not bstack1l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧૠ") in CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨૡ")]:
    return
  CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩૢ")] = CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")].replace(
    bstack1l1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૤"),
    str(bstack1l1lll1_opy_)
  )
def bstack1l1ll1_opy_():
  global CONFIG
  if not bstack1l1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૥") in CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૦")]:
    return
  bstack111ll1ll_opy_ = datetime.datetime.now()
  bstack1l111l111_opy_ = bstack111ll1ll_opy_.strftime(bstack1l1l_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪ૧"))
  CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstack1l1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૪"),
    bstack1l111l111_opy_
  )
def bstack1l11ll11_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫") in CONFIG and not bool(CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]):
    del CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭")]
    return
  if not bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮") in CONFIG:
    CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")] = bstack1l1l_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૰")
  if bstack1l1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧ૱") in CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]:
    bstack1l1ll1_opy_()
    os.environ[bstack1l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ૳")] = CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]
  if not bstack1l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ૵") in CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]:
    return
  bstack1l1lll1_opy_ = bstack1l1l_opy_ (u"ࠧࠨ૷")
  bstack11l1llll_opy_ = bstack1lll11l1l_opy_()
  if bstack11l1llll_opy_ != -1:
    bstack1l1lll1_opy_ = bstack1l1l_opy_ (u"ࠨࡅࡌࠤࠬ૸") + str(bstack11l1llll_opy_)
  if bstack1l1lll1_opy_ == bstack1l1l_opy_ (u"ࠩࠪૹ"):
    bstack1l1llll11_opy_ = bstack1lll1l1l_opy_(CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ૺ")])
    if bstack1l1llll11_opy_ != -1:
      bstack1l1lll1_opy_ = str(bstack1l1llll11_opy_)
  if bstack1l1lll1_opy_:
    bstack11lll1_opy_(bstack1l1lll1_opy_)
    os.environ[bstack1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨૻ")] = CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]
def bstack111ll1l1_opy_(bstack1l11lll1l_opy_, bstack1l1l1l1l_opy_, path):
  bstack1l1l11_opy_ = {
    bstack1l1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૽"): bstack1l1l1l1l_opy_
  }
  if os.path.exists(path):
    bstack1l111llll_opy_ = json.load(open(path, bstack1l1l_opy_ (u"ࠧࡳࡤࠪ૾")))
  else:
    bstack1l111llll_opy_ = {}
  bstack1l111llll_opy_[bstack1l11lll1l_opy_] = bstack1l1l11_opy_
  with open(path, bstack1l1l_opy_ (u"ࠣࡹ࠮ࠦ૿")) as outfile:
    json.dump(bstack1l111llll_opy_, outfile)
def bstack1lll1l1l_opy_(bstack1l11lll1l_opy_):
  bstack1l11lll1l_opy_ = str(bstack1l11lll1l_opy_)
  bstack1lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠩࢁࠫ଀")), bstack1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪଁ"))
  try:
    if not os.path.exists(bstack1lll11ll_opy_):
      os.makedirs(bstack1lll11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠫࢃ࠭ଂ")), bstack1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"), bstack1l1l_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨ଄"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1l_opy_ (u"ࠧࡸࠩଅ")):
        pass
      with open(file_path, bstack1l1l_opy_ (u"ࠣࡹ࠮ࠦଆ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1l_opy_ (u"ࠩࡵࠫଇ")) as bstack111l1l1l_opy_:
      bstack1lllll11_opy_ = json.load(bstack111l1l1l_opy_)
    if bstack1l11lll1l_opy_ in bstack1lllll11_opy_:
      bstack1l1l111ll_opy_ = bstack1lllll11_opy_[bstack1l11lll1l_opy_][bstack1l1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧଈ")]
      bstack1lll1l11l_opy_ = int(bstack1l1l111ll_opy_) + 1
      bstack111ll1l1_opy_(bstack1l11lll1l_opy_, bstack1lll1l11l_opy_, file_path)
      return bstack1lll1l11l_opy_
    else:
      bstack111ll1l1_opy_(bstack1l11lll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll11ll1_opy_.format(str(e)))
    return -1
def bstack111llll_opy_(config):
  if not config[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ଉ")] or not config[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨଊ")]:
    return True
  else:
    return False
def bstack111l_opy_(config):
  if bstack1l1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬଋ") in config:
    del(config[bstack1l1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଌ")])
    return False
  if bstack11ll1l1_opy_() < version.parse(bstack1l1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ଍")):
    return False
  if bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ଎")):
    return True
  if bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଏ") in config and config[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଐ")] == False:
    return False
  else:
    return True
def bstack11l1l_opy_(config, index = 0):
  global bstack111l1_opy_
  bstack1l1lllll1_opy_ = {}
  caps = bstack11lllll_opy_ + bstack1l1l11lll_opy_
  if bstack111l1_opy_:
    caps += bstack1llll1ll_opy_
  for key in config:
    if key in caps + [bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଑")]:
      continue
    bstack1l1lllll1_opy_[key] = config[key]
  if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒") in config:
    for bstack1l111l1l_opy_ in config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")][index]:
      if bstack1l111l1l_opy_ in caps + [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଔ"), bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪକ")]:
        continue
      bstack1l1lllll1_opy_[bstack1l111l1l_opy_] = config[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ")][index][bstack1l111l1l_opy_]
  bstack1l1lllll1_opy_[bstack1l1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ଗ")] = socket.gethostname()
  if bstack1l1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଘ") in bstack1l1lllll1_opy_:
    del(bstack1l1lllll1_opy_[bstack1l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଙ")])
  return bstack1l1lllll1_opy_
def bstack11ll1lll_opy_(config):
  global bstack111l1_opy_
  bstack1l1l111l_opy_ = {}
  caps = bstack1l1l11lll_opy_
  if bstack111l1_opy_:
    caps+= bstack1llll1ll_opy_
  for key in caps:
    if key in config:
      bstack1l1l111l_opy_[key] = config[key]
  return bstack1l1l111l_opy_
def bstack1ll1ll_opy_(bstack1l1lllll1_opy_, bstack1l1l111l_opy_):
  bstack1l1l1111l_opy_ = {}
  for key in bstack1l1lllll1_opy_.keys():
    if key in bstack1llll111_opy_:
      bstack1l1l1111l_opy_[bstack1llll111_opy_[key]] = bstack1l1lllll1_opy_[key]
    else:
      bstack1l1l1111l_opy_[key] = bstack1l1lllll1_opy_[key]
  for key in bstack1l1l111l_opy_:
    if key in bstack1llll111_opy_:
      bstack1l1l1111l_opy_[bstack1llll111_opy_[key]] = bstack1l1l111l_opy_[key]
    else:
      bstack1l1l1111l_opy_[key] = bstack1l1l111l_opy_[key]
  return bstack1l1l1111l_opy_
def bstack1l1ll1l_opy_(config, index = 0):
  global bstack111l1_opy_
  caps = {}
  bstack1l1l111l_opy_ = bstack11ll1lll_opy_(config)
  bstack1ll1l1111_opy_ = bstack1l1l11lll_opy_
  bstack1ll1l1111_opy_ += bstack1l1lll1ll_opy_
  if bstack111l1_opy_:
    bstack1ll1l1111_opy_ += bstack1llll1ll_opy_
  if bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଚ") in config:
    if bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଛ") in config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index]:
      caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ")] = config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index][bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")]
    if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଠ") in config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][index]:
      caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ")] = str(config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index][bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")])
    bstack1llllll_opy_ = {}
    for bstack1llllll1_opy_ in bstack1ll1l1111_opy_:
      if bstack1llllll1_opy_ in config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index]:
        if bstack1llllll1_opy_ == bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧଦ"):
          bstack1llllll_opy_[bstack1llllll1_opy_] = str(config[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index][bstack1llllll1_opy_] * 1.0)
        else:
          bstack1llllll_opy_[bstack1llllll1_opy_] = config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][index][bstack1llllll1_opy_]
        del(config[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1llllll1_opy_])
    bstack1l1l111l_opy_ = update(bstack1l1l111l_opy_, bstack1llllll_opy_)
  bstack1l1lllll1_opy_ = bstack11l1l_opy_(config, index)
  for bstack11lllll1l_opy_ in bstack1l1l11lll_opy_ + [bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧପ"), bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଫ")]:
    if bstack11lllll1l_opy_ in bstack1l1lllll1_opy_:
      bstack1l1l111l_opy_[bstack11lllll1l_opy_] = bstack1l1lllll1_opy_[bstack11lllll1l_opy_]
      del(bstack1l1lllll1_opy_[bstack11lllll1l_opy_])
  if bstack111l_opy_(config):
    bstack1l1lllll1_opy_[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫବ")] = True
    caps.update(bstack1l1l111l_opy_)
    caps[bstack1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଭ")] = bstack1l1lllll1_opy_
  else:
    bstack1l1lllll1_opy_[bstack1l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = False
    caps.update(bstack1ll1ll_opy_(bstack1l1lllll1_opy_, bstack1l1l111l_opy_))
    if bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଯ") in caps:
      caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩର")] = caps[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱")]
      del(caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ")])
    if bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ") in caps:
      caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ଴")] = caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ")]
      del(caps[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଶ")])
  return caps
def bstack1l1111ll_opy_():
  global bstack1lll111_opy_
  if bstack11ll1l1_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨଷ")):
    if bstack1lll111_opy_ != bstack1l1l_opy_ (u"ࠩࠪସ"):
      return bstack1l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦହ") + bstack1lll111_opy_ + bstack1l1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ଺")
    return bstack1l11l1_opy_
  if  bstack1lll111_opy_ != bstack1l1l_opy_ (u"ࠬ࠭଻"):
    return bstack1l1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯଼ࠣ") + bstack1lll111_opy_ + bstack1l1l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣଽ")
  return bstack1l11ll11l_opy_
def bstack11lll111_opy_(options):
  return hasattr(options, bstack1l1l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩା"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l1l1l1_opy_(options, bstack111l111l_opy_):
  for bstack11111ll1_opy_ in bstack111l111l_opy_:
    if bstack11111ll1_opy_ in [bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧି"), bstack1l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧୀ")]:
      next
    if bstack11111ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack11111ll1_opy_]= update(options._experimental_options[bstack11111ll1_opy_], bstack111l111l_opy_[bstack11111ll1_opy_])
    else:
      options.add_experimental_option(bstack11111ll1_opy_, bstack111l111l_opy_[bstack11111ll1_opy_])
  if bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ") in bstack111l111l_opy_:
    for arg in bstack111l111l_opy_[bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪୂ")]:
      options.add_argument(arg)
    del(bstack111l111l_opy_[bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ")])
  if bstack1l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୄ") in bstack111l111l_opy_:
    for ext in bstack111l111l_opy_[bstack1l1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ୅")]:
      options.add_extension(ext)
    del(bstack111l111l_opy_[bstack1l1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")])
def bstack1ll11lll1_opy_(options, bstack1ll111lll_opy_):
  if bstack1l1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩେ") in bstack1ll111lll_opy_:
    for bstack1111l111_opy_ in bstack1ll111lll_opy_[bstack1l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪୈ")]:
      if bstack1111l111_opy_ in options._preferences:
        options._preferences[bstack1111l111_opy_] = update(options._preferences[bstack1111l111_opy_], bstack1ll111lll_opy_[bstack1l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉")][bstack1111l111_opy_])
      else:
        options.set_preference(bstack1111l111_opy_, bstack1ll111lll_opy_[bstack1l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")][bstack1111l111_opy_])
  if bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ") in bstack1ll111lll_opy_:
    for arg in bstack1ll111lll_opy_[bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୌ")]:
      options.add_argument(arg)
def bstack1l11l11ll_opy_(options, bstack1l1111_opy_):
  if bstack1l1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹ୍ࠪ") in bstack1l1111_opy_:
    options.use_webview(bool(bstack1l1111_opy_[bstack1l1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୎")]))
  bstack11l1l1l1_opy_(options, bstack1l1111_opy_)
def bstack1l11ll1ll_opy_(options, bstack1l1ll1ll_opy_):
  for bstack1ll11l1_opy_ in bstack1l1ll1ll_opy_:
    if bstack1ll11l1_opy_ in [bstack1l1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ୏"), bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ୐")]:
      next
    options.set_capability(bstack1ll11l1_opy_, bstack1l1ll1ll_opy_[bstack1ll11l1_opy_])
  if bstack1l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack1l1ll1ll_opy_:
    for arg in bstack1l1ll1ll_opy_[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
  if bstack1l1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୓") in bstack1l1ll1ll_opy_:
    options.use_technology_preview(bool(bstack1l1ll1ll_opy_[bstack1l1l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୔")]))
def bstack11ll11l1_opy_(options, bstack111ll11_opy_):
  for bstack11llll1l_opy_ in bstack111ll11_opy_:
    if bstack11llll1l_opy_ in [bstack1l1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ୕"), bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options._options[bstack11llll1l_opy_] = bstack111ll11_opy_[bstack11llll1l_opy_]
  if bstack1l1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ") in bstack111ll11_opy_:
    for bstack1l1ll11l1_opy_ in bstack111ll11_opy_[bstack1l1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୘")]:
      options.add_additional_option(
          bstack1l1ll11l1_opy_, bstack111ll11_opy_[bstack1l1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙")][bstack1l1ll11l1_opy_])
  if bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୚") in bstack111ll11_opy_:
    for arg in bstack111ll11_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୛")]:
      options.add_argument(arg)
def bstack1ll11ll1l_opy_(options, caps):
  if not hasattr(options, bstack1l1l_opy_ (u"ࠪࡏࡊ࡟ࠧଡ଼")):
    return
  if options.KEY == bstack1l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩଢ଼") and options.KEY in caps:
    bstack11l1l1l1_opy_(options, caps[bstack1l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୞")])
  elif options.KEY == bstack1l1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack1ll11lll1_opy_(options, caps[bstack1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩୡ") and options.KEY in caps:
    bstack1l11ll1ll_opy_(options, caps[bstack1l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪୢ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack1l11l11ll_opy_(options, caps[bstack1l1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୥") and options.KEY in caps:
    bstack11ll11l1_opy_(options, caps[bstack1l1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୦")])
def bstack1111111_opy_(caps):
  global bstack111l1_opy_
  if bstack111l1_opy_:
    if bstack1l111lll1_opy_() < version.parse(bstack1l1l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭୧")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ୨")
    if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୩") in caps:
      browser = caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ୪")]
    elif bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୫") in caps:
      browser = caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୬")]
    browser = str(browser).lower()
    if browser == bstack1l1l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭୭") or browser == bstack1l1l_opy_ (u"ࠧࡪࡲࡤࡨࠬ୮"):
      browser = bstack1l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୯")
    if browser == bstack1l1l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪ୰"):
      browser = bstack1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪୱ")
    if browser not in [bstack1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୲"), bstack1l1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ୳"), bstack1l1l_opy_ (u"࠭ࡩࡦࠩ୴"), bstack1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ୵"), bstack1l1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ୶")]:
      return None
    try:
      package = bstack1l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫ୷").format(browser)
      name = bstack1l1l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫ୸")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lll111_opy_(options):
        return None
      for bstack11lllll1l_opy_ in caps.keys():
        options.set_capability(bstack11lllll1l_opy_, caps[bstack11lllll1l_opy_])
      bstack1ll11ll1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l111l11_opy_(options, bstack111111ll_opy_):
  if not bstack11lll111_opy_(options):
    return
  for bstack11lllll1l_opy_ in bstack111111ll_opy_.keys():
    if bstack11lllll1l_opy_ in bstack1l1lll1ll_opy_:
      next
    if bstack11lllll1l_opy_ in options._caps and type(options._caps[bstack11lllll1l_opy_]) in [dict, list]:
      options._caps[bstack11lllll1l_opy_] = update(options._caps[bstack11lllll1l_opy_], bstack111111ll_opy_[bstack11lllll1l_opy_])
    else:
      options.set_capability(bstack11lllll1l_opy_, bstack111111ll_opy_[bstack11lllll1l_opy_])
  bstack1ll11ll1l_opy_(options, bstack111111ll_opy_)
  if bstack1l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ୹") in options._caps:
    if options._caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୺")] and options._caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୻")].lower() != bstack1l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ୼"):
      del options._caps[bstack1l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧ୽")]
def bstack11111111_opy_(proxy_config):
  if bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୾") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ୿")] = proxy_config[bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀")]
    del(proxy_config[bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஁")])
  if bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஂ") in proxy_config and proxy_config[bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஃ")].lower() != bstack1l1l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ஄"):
    proxy_config[bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")] = bstack1l1l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪஆ")
  if bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩஇ") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ")] = bstack1l1l_opy_ (u"࠭ࡰࡢࡥࠪஉ")
  return proxy_config
def bstack111l1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ஊ") in config:
    return proxy
  config[bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ஋")] = bstack11111111_opy_(config[bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")])
  return proxy
def bstack111lll_opy_(self):
  global CONFIG
  global bstack1ll111ll1_opy_
  if bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஎ") in CONFIG:
    return CONFIG[bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨஏ")]
  elif bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஐ") in CONFIG:
    return CONFIG[bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஑")]
  else:
    return bstack1ll111ll1_opy_(self)
def bstack11l11_opy_():
  global CONFIG
  return bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫஒ") in CONFIG or bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ஓ") in CONFIG
def bstack11l111l1_opy_(config):
  if not bstack11l11_opy_():
    return
  if config.get(bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ")):
    return config.get(bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக"))
  if config.get(bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖")):
    return config.get(bstack1l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗"))
def bstack1ll1111ll_opy_():
  return bstack11l11_opy_() and bstack11ll1l1_opy_() >= version.parse(bstack1ll1llll1_opy_)
def bstack1l1111lll_opy_(config):
  if bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ஘") in config:
    return config[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬங")]
  if bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨச") in config:
    return config[bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஛")]
  return {}
def bstack1lll1ll11_opy_(config):
  if bstack1l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩஜ") in config:
    return config[bstack1l1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ஝")]
  return {}
def bstack1lll11lll_opy_(caps):
  global bstack11llll1_opy_
  if bstack1l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧஞ") in caps:
    caps[bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨட")][bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ஠")] = True
    if bstack11llll1_opy_:
      caps[bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ஡")][bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ஢")] = bstack11llll1_opy_
  else:
    caps[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩண")] = True
    if bstack11llll1_opy_:
      caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭த")] = bstack11llll1_opy_
def bstack111llll1_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஥") in CONFIG and CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ஦")]:
    bstack11l1111l_opy_ = bstack1l1111lll_opy_(CONFIG)
    bstack1ll1l11l_opy_(CONFIG[bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஧")], bstack11l1111l_opy_)
def bstack1ll1l11l_opy_(key, bstack11l1111l_opy_):
  global bstack1ll11l11l_opy_
  logger.info(bstack1l1ll1l11_opy_)
  try:
    bstack1ll11l11l_opy_ = Local()
    bstack1l11111l1_opy_ = {bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ந"): key}
    bstack1l11111l1_opy_.update(bstack11l1111l_opy_)
    logger.debug(bstack11111l_opy_.format(str(bstack1l11111l1_opy_)))
    bstack1ll11l11l_opy_.start(**bstack1l11111l1_opy_)
    if bstack1ll11l11l_opy_.isRunning():
      logger.info(bstack11ll_opy_)
  except Exception as e:
    bstack1ll1l1l_opy_(bstack111l11_opy_.format(str(e)))
def bstack1l1l11l11_opy_():
  global bstack1ll11l11l_opy_
  if bstack1ll11l11l_opy_.isRunning():
    logger.info(bstack11ll111_opy_)
    bstack1ll11l11l_opy_.stop()
  bstack1ll11l11l_opy_ = None
def bstack1ll1l1l1l_opy_():
  global bstack1l1l1ll_opy_
  global bstack1lll11111_opy_
  if bstack1l1l1ll_opy_:
    logger.warning(bstack1l1l1l1ll_opy_.format(str(bstack1l1l1ll_opy_)))
  logger.info(bstack1ll111_opy_)
  global bstack1ll11l11l_opy_
  if bstack1ll11l11l_opy_:
    bstack1l1l11l11_opy_()
  try:
    for driver in bstack1lll11111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11lll_opy_)
  bstack1ll1lll_opy_()
def bstack1l1ll_opy_(self, *args):
  logger.error(bstack1l1111l11_opy_)
  bstack1ll1l1l1l_opy_()
  sys.exit(1)
def bstack1ll1l1l_opy_(err):
  logger.critical(bstack1lll1_opy_.format(str(err)))
  bstack1ll1lll_opy_(bstack1lll1_opy_.format(str(err)))
  atexit.unregister(bstack1ll1l1l1l_opy_)
  sys.exit(1)
def bstack11lll11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1lll_opy_(message)
  atexit.unregister(bstack1ll1l1l1l_opy_)
  sys.exit(1)
def bstack1ll1l111_opy_():
  global CONFIG
  global bstack11l111l_opy_
  global bstack1l111ll1_opy_
  global bstack1l1lllll_opy_
  CONFIG = bstack111l1ll_opy_()
  bstack11111lll_opy_()
  bstack11lll1l_opy_()
  CONFIG = bstack1lll1lll1_opy_(CONFIG)
  update(CONFIG, bstack1l111ll1_opy_)
  update(CONFIG, bstack11l111l_opy_)
  CONFIG = bstack111lll1_opy_(CONFIG)
  if bstack1l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧன") in CONFIG and str(CONFIG[bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨப")]).lower() == bstack1l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ஫"):
    bstack1l1lllll_opy_ = False
  if (bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஬") in CONFIG and bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭") in bstack11l111l_opy_) or (bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫம") in CONFIG and bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய") not in bstack1l111ll1_opy_):
    if os.getenv(bstack1l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧர")):
      CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற")] = os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩல"))
    else:
      bstack1l11ll11_opy_()
  elif (bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩள") not in CONFIG and bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩழ") in CONFIG) or (bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫவ") in bstack1l111ll1_opy_ and bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬஶ") not in bstack11l111l_opy_):
    del(CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ")])
  if bstack111llll_opy_(CONFIG):
    bstack1ll1l1l_opy_(bstack1l1l1ll11_opy_)
  bstack1111l1_opy_()
  bstack1l111ll1l_opy_()
  if bstack111l1_opy_:
    CONFIG[bstack1l1l_opy_ (u"ࠫࡦࡶࡰࠨஸ")] = bstack1llll11l1_opy_(CONFIG)
    logger.info(bstack111ll1_opy_.format(CONFIG[bstack1l1l_opy_ (u"ࠬࡧࡰࡱࠩஹ")]))
def bstack1l111ll1l_opy_():
  global CONFIG
  global bstack111l1_opy_
  if bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪ஺") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11lll11_opy_(e, bstack1l1l1lll1_opy_)
    bstack111l1_opy_ = True
def bstack1llll11l1_opy_(config):
  bstack1111l11_opy_ = bstack1l1l_opy_ (u"ࠧࠨ஻")
  app = config[bstack1l1l_opy_ (u"ࠨࡣࡳࡴࠬ஼")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l11ll_opy_:
      if os.path.exists(app):
        bstack1111l11_opy_ = bstack1llll11ll_opy_(config, app)
      elif bstack1l111111l_opy_(app):
        bstack1111l11_opy_ = app
      else:
        bstack1ll1l1l_opy_(bstack1l11l1l11_opy_.format(app))
    else:
      if bstack1l111111l_opy_(app):
        bstack1111l11_opy_ = app
      elif os.path.exists(app):
        bstack1111l11_opy_ = bstack1llll11ll_opy_(app)
      else:
        bstack1ll1l1l_opy_(bstack1l11l1ll1_opy_)
  else:
    if len(app) > 2:
      bstack1ll1l1l_opy_(bstack1l11ll1_opy_)
    elif len(app) == 2:
      if bstack1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ஽") in app and bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ா") in app:
        if os.path.exists(app[bstack1l1l_opy_ (u"ࠫࡵࡧࡴࡩࠩி")]):
          bstack1111l11_opy_ = bstack1llll11ll_opy_(config, app[bstack1l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪீ")], app[bstack1l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩு")])
        else:
          bstack1ll1l1l_opy_(bstack1l11l1l11_opy_.format(app))
      else:
        bstack1ll1l1l_opy_(bstack1l11ll1_opy_)
    else:
      for key in app:
        if key in bstack1ll11l111_opy_:
          if key == bstack1l1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬூ"):
            if os.path.exists(app[key]):
              bstack1111l11_opy_ = bstack1llll11ll_opy_(config, app[key])
            else:
              bstack1ll1l1l_opy_(bstack1l11l1l11_opy_.format(app))
          else:
            bstack1111l11_opy_ = app[key]
        else:
          bstack1ll1l1l_opy_(bstack11l1l111_opy_)
  return bstack1111l11_opy_
def bstack1l111111l_opy_(bstack1111l11_opy_):
  import re
  bstack1ll111l1_opy_ = re.compile(bstack1l1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ௃"))
  bstack111l1l1_opy_ = re.compile(bstack1l1l_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪ࠰࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ௄"))
  if bstack1l1l_opy_ (u"ࠪࡦࡸࡀ࠯࠰ࠩ௅") in bstack1111l11_opy_ or re.fullmatch(bstack1ll111l1_opy_, bstack1111l11_opy_) or re.fullmatch(bstack111l1l1_opy_, bstack1111l11_opy_):
    return True
  else:
    return False
def bstack1llll11ll_opy_(config, path, bstack1l1l11ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1l_opy_ (u"ࠫࡷࡨࠧெ")).read()).hexdigest()
  bstack1ll1ll1ll_opy_ = bstack1l11llll_opy_(md5_hash)
  bstack1111l11_opy_ = None
  if bstack1ll1ll1ll_opy_:
    logger.info(bstack1l1ll11ll_opy_.format(bstack1ll1ll1ll_opy_, md5_hash))
    return bstack1ll1ll1ll_opy_
  bstack11l1l11l_opy_ = MultipartEncoder(
    fields={
        bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࠪே"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1l_opy_ (u"࠭ࡲࡣࠩை")), bstack1l1l_opy_ (u"ࠧࡵࡧࡻࡸ࠴ࡶ࡬ࡢ࡫ࡱࠫ௉")),
        bstack1l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫொ"): bstack1l1l11ll_opy_
    }
  )
  response = requests.post(bstack1l111111_opy_, data=bstack11l1l11l_opy_,
                         headers={bstack1l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨோ"): bstack11l1l11l_opy_.content_type}, auth=(config[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬௌ")], config[bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ்ࠧ")]))
  try:
    res = json.loads(response.text)
    bstack1111l11_opy_ = res[bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ࠭௎")]
    logger.info(bstack1l11ll_opy_.format(bstack1111l11_opy_))
    bstack111lllll_opy_(md5_hash, bstack1111l11_opy_)
  except ValueError as err:
    bstack1ll1l1l_opy_(bstack1l1l1l1_opy_.format(str(err)))
  return bstack1111l11_opy_
def bstack1111l1_opy_():
  global CONFIG
  global bstack1l1l1l_opy_
  bstack1111l11l_opy_ = 0
  bstack11111ll_opy_ = 1
  if bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௏") in CONFIG:
    bstack11111ll_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧௐ")]
  if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑") in CONFIG:
    bstack1111l11l_opy_ = len(CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")])
  bstack1l1l1l_opy_ = int(bstack11111ll_opy_) * int(bstack1111l11l_opy_)
def bstack1l11llll_opy_(md5_hash):
  bstack111l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠪࢂࠬ௓")), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௔"), bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭௕"))
  if os.path.exists(bstack111l111_opy_):
    bstack1ll11l11_opy_ = json.load(open(bstack111l111_opy_,bstack1l1l_opy_ (u"࠭ࡲࡣࠩ௖")))
    if md5_hash in bstack1ll11l11_opy_:
      bstack1111ll1l_opy_ = bstack1ll11l11_opy_[md5_hash]
      bstack111111l_opy_ = datetime.datetime.now()
      bstack1111l_opy_ = datetime.datetime.strptime(bstack1111ll1l_opy_[bstack1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪௗ")], bstack1l1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ௘"))
      if (bstack111111l_opy_ - bstack1111l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1111ll1l_opy_[bstack1l1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௙")]):
        return None
      return bstack1111ll1l_opy_[bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭௚")]
  else:
    return None
def bstack111lllll_opy_(md5_hash, bstack1111l11_opy_):
  bstack1lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠫࢃ࠭௛")), bstack1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ௜"))
  if not os.path.exists(bstack1lll11ll_opy_):
    os.makedirs(bstack1lll11ll_opy_)
  bstack111l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"࠭ࡾࠨ௝")), bstack1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ௞"), bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ௟"))
  bstack1lll11_opy_ = {
    bstack1l1l_opy_ (u"ࠩ࡬ࡨࠬ௠"): bstack1111l11_opy_,
    bstack1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭௡"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௢")),
    bstack1l1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௣"): str(__version__)
  }
  if os.path.exists(bstack111l111_opy_):
    bstack1ll11l11_opy_ = json.load(open(bstack111l111_opy_,bstack1l1l_opy_ (u"࠭ࡲࡣࠩ௤")))
  else:
    bstack1ll11l11_opy_ = {}
  bstack1ll11l11_opy_[md5_hash] = bstack1lll11_opy_
  with open(bstack111l111_opy_, bstack1l1l_opy_ (u"ࠢࡸ࠭ࠥ௥")) as outfile:
    json.dump(bstack1ll11l11_opy_, outfile)
def bstack111111_opy_(self):
  return
def bstack1ll1111_opy_(self):
  return
def bstack1ll1l1lll_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1lll1l11_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll111ll_opy_
  global bstack1111_opy_
  global bstack11ll1l11_opy_
  global bstack1lllll_opy_
  global bstack1l1ll1111_opy_
  global bstack1l1l111_opy_
  global bstack1lll11111_opy_
  CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ௦")] = str(bstack1l1ll1111_opy_) + str(__version__)
  command_executor = bstack1l1111ll_opy_()
  logger.debug(bstack11lllllll_opy_.format(command_executor))
  proxy = bstack111l1l_opy_(CONFIG, proxy)
  bstack1lll11l1_opy_ = 0 if bstack1111_opy_ < 0 else bstack1111_opy_
  if bstack1lllll_opy_ is True:
    bstack1lll11l1_opy_ = int(threading.current_thread().getName())
  bstack111111ll_opy_ = bstack1l1ll1l_opy_(CONFIG, bstack1lll11l1_opy_)
  logger.debug(bstack1l11l1l1l_opy_.format(str(bstack111111ll_opy_)))
  if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭௧") in CONFIG and CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ௨")]:
    bstack1lll11lll_opy_(bstack111111ll_opy_)
  if desired_capabilities:
    bstack1lll1l1_opy_ = bstack1lll1lll1_opy_(desired_capabilities)
    bstack1lll1l1_opy_[bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ௩")] = bstack111l_opy_(CONFIG)
    bstack1l1l11ll1_opy_ = bstack1l1ll1l_opy_(bstack1lll1l1_opy_)
    if bstack1l1l11ll1_opy_:
      bstack111111ll_opy_ = update(bstack1l1l11ll1_opy_, bstack111111ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l111l11_opy_(options, bstack111111ll_opy_)
  if not options:
    options = bstack1111111_opy_(bstack111111ll_opy_)
  if proxy and bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ௪")):
    options.proxy(proxy)
  if options and bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ௫")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11ll1l1_opy_() < version.parse(bstack1l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭௬")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack111111ll_opy_)
  logger.info(bstack11l11l1l_opy_)
  if bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ௭")):
    bstack1l1l111_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ௮")):
    bstack1l1l111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ௯")):
    bstack1l1l111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack111ll11l_opy_ = bstack1l1l_opy_ (u"ࠫࠬ௰")
    if bstack11ll1l1_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭௱")):
      bstack111ll11l_opy_ = self.caps.get(bstack1l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ௲"))
    else:
      bstack111ll11l_opy_ = self.capabilities.get(bstack1l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ௳"))
    if bstack111ll11l_opy_:
      if bstack11ll1l1_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ௴")):
        self.command_executor._url = bstack1l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ௵") + bstack1lll111_opy_ + bstack1l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ௶")
      else:
        self.command_executor._url = bstack1l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ௷") + bstack111ll11l_opy_ + bstack1l1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ௸")
      logger.debug(bstack1l1111ll1_opy_.format(bstack111ll11l_opy_))
    else:
      logger.debug(bstack1l1llll1_opy_.format(bstack1l1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ௹")))
  except Exception as e:
    logger.debug(bstack1l1llll1_opy_.format(e))
  bstack1ll111ll_opy_ = self.session_id
  bstack1lll11111_opy_.append(self)
  if bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௺") in CONFIG and bstack1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭௻") in CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௼")][bstack1lll11l1_opy_]:
    bstack11ll1l11_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௽")][bstack1lll11l1_opy_][bstack1l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௾")]
  logger.debug(bstack111l11l1_opy_.format(bstack1ll111ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11lll11l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1111l_opy_
      if(bstack1l1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ௿") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"࠭ࡾࠨఀ")), bstack1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఁ"), bstack1l1l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪం")), bstack1l1l_opy_ (u"ࠩࡺࠫః")) as fp:
          fp.write(bstack1l1l_opy_ (u"ࠥࠦఄ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨఅ")))):
          with open(args[1], bstack1l1l_opy_ (u"ࠬࡸࠧఆ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1l_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬఇ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1l1ll_opy_)
            lines.insert(1, bstack1l11111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤఈ")), bstack1l1l_opy_ (u"ࠨࡹࠪఉ")) as bstack1llll1l1_opy_:
              bstack1llll1l1_opy_.writelines(lines)
        CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫఊ")] = str(bstack1l1ll1111_opy_) + str(__version__)
        bstack1lll11l1_opy_ = 0 if bstack1111_opy_ < 0 else bstack1111_opy_
        if bstack1lllll_opy_ is True:
          bstack1lll11l1_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l1l_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥఋ")] = False
        CONFIG[bstack1l1l_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥఌ")] = True
        bstack111111ll_opy_ = bstack1l1ll1l_opy_(CONFIG, bstack1lll11l1_opy_)
        logger.debug(bstack1l11l1l1l_opy_.format(str(bstack111111ll_opy_)))
        if CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ఍")]:
          bstack1lll11lll_opy_(bstack111111ll_opy_)
        if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఎ") in CONFIG and bstack1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఏ") in CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఐ")][bstack1lll11l1_opy_]:
          bstack11ll1l11_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ఑")][bstack1lll11l1_opy_][bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఒ")]
        args.append(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠫࢃ࠭ఓ")), bstack1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬఔ"), bstack1l1l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨక")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack111111ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤఖ"))
      bstack1ll1111l_opy_ = True
      return bstack11111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11llll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll111ll_opy_
    global bstack1111_opy_
    global bstack11ll1l11_opy_
    global bstack1lllll_opy_
    global bstack1l1ll1111_opy_
    global bstack1l1l111_opy_
    CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪగ")] = str(bstack1l1ll1111_opy_) + str(__version__)
    bstack1lll11l1_opy_ = 0 if bstack1111_opy_ < 0 else bstack1111_opy_
    if bstack1lllll_opy_ is True:
      bstack1lll11l1_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣఘ")] = True
    bstack111111ll_opy_ = bstack1l1ll1l_opy_(CONFIG, bstack1lll11l1_opy_)
    logger.debug(bstack1l11l1l1l_opy_.format(str(bstack111111ll_opy_)))
    if CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧఙ")]:
      bstack1lll11lll_opy_(bstack111111ll_opy_)
    if bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧచ") in CONFIG and bstack1l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఛ") in CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩజ")][bstack1lll11l1_opy_]:
      bstack11ll1l11_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఝ")][bstack1lll11l1_opy_][bstack1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఞ")]
    import urllib
    import json
    bstack1l11l_opy_ = bstack1l1l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫట") + urllib.parse.quote(json.dumps(bstack111111ll_opy_))
    browser = self.connect(bstack1l11l_opy_)
    return browser
except Exception as e:
    pass
def bstack1lll1l111_opy_():
    global bstack1ll1111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll11llll_opy_
        bstack1ll1111l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11lll11l_opy_
      bstack1ll1111l_opy_ = True
    except Exception as e:
      pass
def bstack11l11ll1_opy_(context, bstack1l1111111_opy_):
  try:
    context.page.evaluate(bstack1l1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦఠ"), bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨడ")+ json.dumps(bstack1l1111111_opy_) + bstack1l1l_opy_ (u"ࠧࢃࡽࠣఢ"))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦణ"), e)
def bstack1l11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣత"), bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭థ") + json.dumps(message) + bstack1l1l_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬద") + json.dumps(level) + bstack1l1l_opy_ (u"ࠪࢁࢂ࠭ధ"))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢన"), e)
def bstack1lllllll_opy_(context, status, message = bstack1l1l_opy_ (u"ࠧࠨ఩")):
  try:
    if(status == bstack1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨప")):
      context.page.evaluate(bstack1l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣఫ"), bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩబ") + json.dumps(bstack1l1l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦభ") + str(message)) + bstack1l1l_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧమ") + json.dumps(status) + bstack1l1l_opy_ (u"ࠦࢂࢃࠢయ"))
    else:
      context.page.evaluate(bstack1l1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨర"), bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧఱ") + json.dumps(status) + bstack1l1l_opy_ (u"ࠢࡾࡿࠥల"))
  except Exception as e:
    logger.debug(bstack1l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧళ"), e)
def bstack1l1lll_opy_(self, url):
  global bstack1l1ll1l1l_opy_
  try:
    bstack11l1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l111ll_opy_.format(str(err)))
  try:
    bstack1l1ll1l1l_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1111l1l_opy_ = str(e)
      if any(err_msg in bstack1l1111l1l_opy_ for err_msg in bstack1ll1l11ll_opy_):
        bstack11l1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l111ll_opy_.format(str(err)))
    raise e
def bstack1l1ll11l_opy_(self, test):
  global CONFIG
  global bstack1ll111ll_opy_
  global bstack1llllll11_opy_
  global bstack11ll1l11_opy_
  global bstack1l1l1111_opy_
  try:
    if not bstack1ll111ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠩࢁࠫఴ")), bstack1l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪవ"), bstack1l1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭శ"))) as f:
        bstack1l111l1ll_opy_ = json.loads(bstack1l1l_opy_ (u"ࠧࢁࠢష") + f.read().strip() + bstack1l1l_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨస") + bstack1l1l_opy_ (u"ࠢࡾࠤహ"))
        bstack1ll111ll_opy_ = bstack1l111l1ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll111ll_opy_:
    try:
      data = {}
      bstack11l1lll1_opy_ = None
      if test:
        bstack11l1lll1_opy_ = str(test.data)
      if not bstack1ll1ll1l_opy_ and bstack11l1lll1_opy_:
        data[bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭఺")] = bstack11l1lll1_opy_
      if bstack1llllll11_opy_:
        if bstack1llllll11_opy_.status == bstack1l1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ఻"):
          data[bstack1l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ఼ࠪ")] = bstack1l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫఽ")
        elif bstack1llllll11_opy_.status == bstack1l1l_opy_ (u"ࠬࡌࡁࡊࡎࠪా"):
          data[bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ి")] = bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧీ")
          if bstack1llllll11_opy_.message:
            data[bstack1l1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨు")] = str(bstack1llllll11_opy_.message)
      user = CONFIG[bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫూ")]
      key = CONFIG[bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ృ")]
      url = bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩౄ").format(user, key, bstack1ll111ll_opy_)
      headers = {
        bstack1l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ౅"): bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩె"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11l11l1_opy_.format(str(e)))
  bstack1l1l1111_opy_(self, test)
def bstack1l11l1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l111_opy_
  bstack11l111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llllll11_opy_
  bstack1llllll11_opy_ = self._test
def bstack11l1ll_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢే"), bstack1l1l_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧై"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l1l_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶࠧ౉"), bstack1l1l_opy_ (u"ࠥ࠲ࠧొ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l1l_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥో"))))
  if not files:
    pabot._write(bstack1l1l_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧౌ") % outs_dir, pabot.Color.YELLOW)
    return bstack1l1l_opy_ (u"ࠨ్ࠢ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack11l1ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ౎") in options:
    del options[bstack1l1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ౏")]
  if ROBOT_VERSION < bstack1l1l_opy_ (u"ࠤ࠷࠲࠵ࠨ౐"):
    stats = {
      bstack1l1l_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧ౑"): {bstack1l1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥ౒"): 0, bstack1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౓"): 0, bstack1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౔"): 0},
      bstack1l1l_opy_ (u"ࠢࡢ࡮࡯ౕࠦ"): {bstack1l1l_opy_ (u"ࠣࡶࡲࡸࡦࡲౖࠢ"): 0, bstack1l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ౗"): 0, bstack1l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥౘ"): 0},
    }
  else:
    stats = {
      bstack1l1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥౙ"): 0,
      bstack1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧౚ"): 0,
      bstack1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౛"): 0,
      bstack1l1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣ౜"): 0,
    }
  if pabot_args[bstack1l1l_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢౝ")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l1l_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ౞")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l1l_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨ౟")], pabot_args[bstack1l1l_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧౠ")]
      )
      outputs += [
        bstack11l1ll_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l1l_opy_ (u"ࠧ࠵ࠢౡ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l1l_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨౢ"), bstack1l1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨౣ") % index),
        )
      ]
    if bstack1l1l_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣ౤") not in options:
      options[bstack1l1l_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤ౥")] = bstack1l1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢ౦")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1ll1lll_opy_(self, ff_profile_dir):
  global bstack111l1lll_opy_
  if not ff_profile_dir:
    return None
  return bstack111l1lll_opy_(self, ff_profile_dir)
def bstack1ll11ll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11llll1_opy_
  bstack1ll1l1ll1_opy_ = []
  if bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౧") in CONFIG:
    bstack1ll1l1ll1_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౨")]
  bstack11ll11_opy_ = len(suite_group) * len(pabot_args[bstack1l1l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ౩")] or [(bstack1l1l_opy_ (u"ࠢࠣ౪"), None)]) * len(bstack1ll1l1ll1_opy_)
  pabot_args[bstack1l1l_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢ౫")] = []
  for q in range(bstack11ll11_opy_):
    pabot_args[bstack1l1l_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ౬")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ౭")],
      pabot_args[bstack1l1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ౮")],
      argfile,
      pabot_args.get(bstack1l1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ౯")),
      pabot_args[bstack1l1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ౰")],
      platform[0],
      bstack11llll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ౱")] or [(bstack1l1l_opy_ (u"ࠣࠤ౲"), None)]
    for platform in enumerate(bstack1ll1l1ll1_opy_)
  ]
def bstack1llll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1l111_opy_=bstack1l1l_opy_ (u"ࠩࠪ౳")):
  global bstack1lll1ll_opy_
  self.platform_index = platform_index
  self.bstack1lll11l11_opy_ = bstack1l111_opy_
  bstack1lll1ll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1ll111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11ll1l_opy_
  global bstack1lllll11l_opy_
  if not bstack1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౴") in item.options:
    item.options[bstack1l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭౵")] = []
  for v in item.options[bstack1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౶")]:
    if bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ౷") in v:
      item.options[bstack1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ౸")].remove(v)
    if bstack1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ౹") in v:
      item.options[bstack1l1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ౺")].remove(v)
  item.options[bstack1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ౻")].insert(0, bstack1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭౼").format(item.platform_index))
  item.options[bstack1l1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ౽")].insert(0, bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭౾").format(item.bstack1lll11l11_opy_))
  if bstack1lllll11l_opy_:
    item.options[bstack1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ౿")].insert(0, bstack1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫಀ").format(bstack1lllll11l_opy_))
  return bstack11ll1l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll1lll1l_opy_(command):
  global bstack1lllll11l_opy_
  if bstack1lllll11l_opy_:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಁ"), bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠࠨಂ") + bstack1lllll11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಃ"), bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ಄"), 1)
def bstack1l1l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111ll111_opy_
  bstack1ll1lll1l_opy_(command)
  return bstack111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111ll111_opy_
  bstack1ll1lll1l_opy_(command)
  return bstack111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111ll111_opy_
  bstack1ll1lll1l_opy_(command)
  return bstack111ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll1llll_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll111l_opy_
  bstack1l11lll1_opy_ = bstack1lll111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1l_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭ಅ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1l_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫಆ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11lll1_opy_
def bstack1llll11_opy_(self, name, context, *args):
  global bstack1ll1l11_opy_
  if name in [bstack1l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಇ"), bstack1l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಈ")]:
    bstack1ll1l11_opy_(self, name, context, *args)
  if name == bstack1l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫಉ"):
    try:
      if(not bstack1ll1ll1l_opy_):
        bstack1l1111111_opy_ = str(self.feature.name)
        bstack11l11ll1_opy_(context, bstack1l1111111_opy_)
        context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩಊ") + json.dumps(bstack1l1111111_opy_) + bstack1l1l_opy_ (u"ࠬࢃࡽࠨಋ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ಌ").format(str(e)))
  if name == bstack1l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ಍"):
    try:
      if not hasattr(self, bstack1l1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಎ")):
        self.driver_before_scenario = True
      if(not bstack1ll1ll1l_opy_):
        bstack1lll1llll_opy_ = args[0].name
        bstack1l1l11l1_opy_ = bstack1l1111111_opy_ = str(self.feature.name)
        bstack1l1111111_opy_ = bstack1l1l11l1_opy_ + bstack1l1l_opy_ (u"ࠩࠣ࠱ࠥ࠭ಏ") + bstack1lll1llll_opy_
        if self.driver_before_scenario:
          bstack11l11ll1_opy_(context, bstack1l1111111_opy_)
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨಐ") + json.dumps(bstack1l1111111_opy_) + bstack1l1l_opy_ (u"ࠫࢂࢃࠧ಑"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ಒ").format(str(e)))
  if name == bstack1l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಓ"):
    try:
      bstack11ll11ll_opy_ = args[0].status.name
      if str(bstack11ll11ll_opy_).lower() == bstack1l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಔ"):
        bstack11ll1l1l_opy_ = bstack1l1l_opy_ (u"ࠨࠩಕ")
        bstack1l1llll1l_opy_ = bstack1l1l_opy_ (u"ࠩࠪಖ")
        bstack1111ll1_opy_ = bstack1l1l_opy_ (u"ࠪࠫಗ")
        try:
          import traceback
          bstack11ll1l1l_opy_ = self.exception.__class__.__name__
          bstack1l111l1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l1llll1l_opy_ = bstack1l1l_opy_ (u"ࠫࠥ࠭ಘ").join(bstack1l111l1l1_opy_)
          bstack1111ll1_opy_ = bstack1l111l1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l111l1_opy_.format(str(e)))
        bstack11ll1l1l_opy_ += bstack1111ll1_opy_
        bstack1l11_opy_(context, json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦಙ") + str(bstack1l1llll1l_opy_)), bstack1l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧಚ"))
        if self.driver_before_scenario:
          bstack1lllllll_opy_(context, bstack1l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢಛ"), bstack11ll1l1l_opy_)
        context.browser.execute_script(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ಜ") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣಝ") + str(bstack1l1llll1l_opy_)) + bstack1l1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪಞ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫಟ") + json.dumps(bstack1l1l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤಠ") + str(bstack11ll1l1l_opy_)) + bstack1l1l_opy_ (u"࠭ࡽࡾࠩಡ"))
      else:
        bstack1l11_opy_(context, bstack1l1l_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣಢ"), bstack1l1l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨಣ"))
        if self.driver_before_scenario:
          bstack1lllllll_opy_(context, bstack1l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤತ"))
        context.browser.execute_script(bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨಥ") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣದ")) + bstack1l1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫಧ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪನ"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ಩").format(str(e)))
  if name == bstack1l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಪ"):
    try:
      if context.failed is True:
        bstack1ll11l1l1_opy_ = []
        bstack1l1lll1l_opy_ = []
        bstack1lll1lll_opy_ = []
        bstack1lll1l1ll_opy_ = bstack1l1l_opy_ (u"ࠩࠪಫ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll11l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l111l1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1l11l111_opy_ = bstack1l1l_opy_ (u"ࠪࠤࠬಬ").join(bstack1l111l1l1_opy_)
            bstack1l1lll1l_opy_.append(bstack1l11l111_opy_)
            bstack1lll1lll_opy_.append(bstack1l111l1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l111l1_opy_.format(str(e)))
        bstack11ll1l1l_opy_ = bstack1l1l_opy_ (u"ࠫࠬಭ")
        for i in range(len(bstack1ll11l1l1_opy_)):
          bstack11ll1l1l_opy_ += bstack1ll11l1l1_opy_[i] + bstack1lll1lll_opy_[i] + bstack1l1l_opy_ (u"ࠬࡢ࡮ࠨಮ")
        bstack1lll1l1ll_opy_ = bstack1l1l_opy_ (u"࠭ࠠࠨಯ").join(bstack1l1lll1l_opy_)
        if not self.driver_before_scenario:
          bstack1l11_opy_(context, bstack1lll1l1ll_opy_, bstack1l1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨರ"))
          bstack1lllllll_opy_(context, bstack1l1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಱ"), bstack11ll1l1l_opy_)
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧಲ") + json.dumps(bstack1lll1l1ll_opy_) + bstack1l1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪಳ"))
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫ಴") + json.dumps(bstack1l1l_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥವ") + str(bstack11ll1l1l_opy_)) + bstack1l1l_opy_ (u"࠭ࡽࡾࠩಶ"))
      else:
        if not self.driver_before_scenario:
          bstack1l11_opy_(context, bstack1l1l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥಷ") + str(self.feature.name) + bstack1l1l_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥಸ"), bstack1l1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢಹ"))
          bstack1lllllll_opy_(context, bstack1l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ಺"))
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ಻") + json.dumps(bstack1l1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀ಼ࠠࠣ") + str(self.feature.name) + bstack1l1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣಽ")) + bstack1l1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ಾ"))
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬಿ"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫೀ").format(str(e)))
  if name in [bstack1l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪು"), bstack1l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬೂ")]:
    bstack1ll1l11_opy_(self, name, context, *args)
    if (name == bstack1l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ೃ") and self.driver_before_scenario) or (name == bstack1l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ೄ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1l1ll1l1_opy_(config, startdir):
  return bstack1l1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧ೅").format(bstack1l1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢೆ"))
class Notset:
  def __repr__(self):
    return bstack1l1l_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦೇ")
notset = Notset()
def bstack1l11lllll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1ll1l_opy_
  if str(name).lower() == bstack1l1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪೈ"):
    return bstack1l1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ೉")
  else:
    return bstack1lll1ll1l_opy_(self, name, default, skip)
def bstack11l1l1l_opy_(bstack1ll111l11_opy_):
  global bstack1l1ll1111_opy_
  global bstack1ll1111l_opy_
  bstack1l1ll1111_opy_ = bstack1ll111l11_opy_
  logger.info(bstack1l1l1l11l_opy_.format(bstack1l1ll1111_opy_.split(bstack1l1l_opy_ (u"ࠬ࠳ࠧೊ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack111111_opy_
    Service.stop = bstack1ll1111_opy_
    webdriver.Remote.__init__ = bstack1lll1l11_opy_
    webdriver.Remote.get = bstack1l1lll_opy_
    WebDriver.close = bstack1ll1l1lll_opy_
    bstack1ll1111l_opy_ = True
  except Exception as e:
    pass
  bstack1lll1l111_opy_()
  if not bstack1ll1111l_opy_:
    bstack11lll11_opy_(bstack1l1l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣೋ"), bstack1l11ll111_opy_)
  if bstack1ll1111ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111lll_opy_
    except Exception as e:
      logger.error(bstack111ll1l_opy_.format(str(e)))
  if (bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ೌ") in str(bstack1ll111l11_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1ll1lll_opy_
      except Exception as e:
        logger.warn(bstack11ll1_opy_ + str(e))
    except Exception as e:
      bstack11lll11_opy_(e, bstack11ll1_opy_)
    Output.end_test = bstack1l1ll11l_opy_
    TestStatus.__init__ = bstack1l11l1l1_opy_
    QueueItem.__init__ = bstack1llll_opy_
    pabot._create_items = bstack1ll11ll11_opy_
    try:
      from pabot import __version__ as bstack1l11l111l_opy_
      if version.parse(bstack1l11l111l_opy_) >= version.parse(bstack1l1l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ್")):
        pabot._run = bstack1llll11l_opy_
      elif version.parse(bstack1l11l111l_opy_) >= version.parse(bstack1l1l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ೎")):
        pabot._run = bstack1l1l11111_opy_
      else:
        pabot._run = bstack1l1l1l111_opy_
    except Exception as e:
      pabot._run = bstack1l1l1l111_opy_
    pabot._create_command_for_execution = bstack1ll1ll111_opy_
    pabot._report_results = bstack11l1ll1_opy_
  if bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ೏") in str(bstack1ll111l11_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll11_opy_(e, bstack1ll11l_opy_)
    Runner.run_hook = bstack1llll11_opy_
    Step.run = bstack1ll1llll_opy_
  if bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೐") in str(bstack1ll111l11_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1ll1l1_opy_
      Config.getoption = bstack1l11lllll_opy_
    except Exception as e:
      pass
def bstack1llll1_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ೑") in CONFIG and int(CONFIG[bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭೒")]) > 1:
    logger.warn(bstack1l1l1ll1_opy_)
def bstack111l1l11_opy_(bstack1l111l_opy_, index):
  bstack11l1l1l_opy_(bstack1l11l1l_opy_)
  exec(open(bstack1l111l_opy_).read())
def bstack1ll1lllll_opy_(arg):
  global CONFIG
  bstack11l1l1l_opy_(bstack11llll11_opy_)
  os.environ[bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ೓")] = CONFIG[bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ೔")]
  os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬೕ")] = CONFIG[bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೖ")]
  from _pytest.config import main as bstack11l11lll_opy_
  bstack11l11lll_opy_(arg)
def bstack1l11l11l_opy_(arg):
  bstack11l1l1l_opy_(bstack1111lll1_opy_)
  from behave.__main__ import main as bstack1l1ll11_opy_
  bstack1l1ll11_opy_(arg)
def bstack1lll1l_opy_():
  logger.info(bstack1111llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ೗"), help=bstack1l1l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭೘"))
  parser.add_argument(bstack1l1l_opy_ (u"࠭࠭ࡶࠩ೙"), bstack1l1l_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ೚"), help=bstack1l1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ೛"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠩ࠰࡯ࠬ೜"), bstack1l1l_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩೝ"), help=bstack1l1l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬೞ"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠬ࠳ࡦࠨ೟"), bstack1l1l_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೠ"), help=bstack1l1l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ೡ"))
  bstack11lll1ll_opy_ = parser.parse_args()
  try:
    bstack11ll1ll1_opy_ = bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬೢ")
    if bstack11lll1ll_opy_.framework and bstack11lll1ll_opy_.framework not in (bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೣ"), bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ೤")):
      bstack11ll1ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪ೥")
    bstack1lllllll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll1ll1_opy_)
    bstack111l11l_opy_ = open(bstack1lllllll1_opy_, bstack1l1l_opy_ (u"ࠬࡸࠧ೦"))
    bstack1l1ll1ll1_opy_ = bstack111l11l_opy_.read()
    bstack111l11l_opy_.close()
    if bstack11lll1ll_opy_.username:
      bstack1l1ll1ll1_opy_ = bstack1l1ll1ll1_opy_.replace(bstack1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭೧"), bstack11lll1ll_opy_.username)
    if bstack11lll1ll_opy_.key:
      bstack1l1ll1ll1_opy_ = bstack1l1ll1ll1_opy_.replace(bstack1l1l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ೨"), bstack11lll1ll_opy_.key)
    if bstack11lll1ll_opy_.framework:
      bstack1l1ll1ll1_opy_ = bstack1l1ll1ll1_opy_.replace(bstack1l1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೩"), bstack11lll1ll_opy_.framework)
    file_name = bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ೪")
    file_path = os.path.abspath(file_name)
    bstack1l1l1ll1l_opy_ = open(file_path, bstack1l1l_opy_ (u"ࠪࡻࠬ೫"))
    bstack1l1l1ll1l_opy_.write(bstack1l1ll1ll1_opy_)
    bstack1l1l1ll1l_opy_.close()
    logger.info(bstack1l1lll11_opy_)
    try:
      os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೬")] = bstack11lll1ll_opy_.framework if bstack11lll1ll_opy_.framework != None else bstack1l1l_opy_ (u"ࠧࠨ೭")
      config = yaml.safe_load(bstack1l1ll1ll1_opy_)
      config[bstack1l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭೮")] = bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭೯")
      bstack1l11111ll_opy_(bstack11l1lll_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll111ll_opy_.format(str(e)))
def bstack1l11111ll_opy_(bstack1ll11ll_opy_, config, bstack111ll_opy_ = {}):
  global bstack1l1lllll_opy_
  if not config:
    return
  bstack1ll11l1l_opy_ = bstack1l11111_opy_ if not bstack1l1lllll_opy_ else ( bstack1ll1ll1l1_opy_ if bstack1l1l_opy_ (u"ࠨࡣࡳࡴࠬ೰") in config else bstack1llllllll_opy_ )
  data = {
    bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫೱ"): config[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬೲ")],
    bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧೳ"): config[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೴")],
    bstack1l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ೵"): bstack1ll11ll_opy_,
    bstack1l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೶"): {
      bstack1l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೷"): str(config[bstack1l1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ೸")]) if bstack1l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ೹") in config else bstack1l1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ೺"),
      bstack1l1l_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧ೻"): bstack1ll1lll1_opy_(os.getenv(bstack1l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ೼"), bstack1l1l_opy_ (u"ࠢࠣ೽"))),
      bstack1l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ೾"): bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ೿"),
      bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫഀ"): bstack1ll11l1l_opy_,
      bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഁ"): config[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨം")]if config[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩഃ")] else bstack1l1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣഄ"),
      bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഅ"): str(config[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫആ")]) if bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬഇ") in config else bstack1l1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧഈ"),
      bstack1l1l_opy_ (u"ࠬࡵࡳࠨഉ"): sys.platform,
      bstack1l1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨഊ"): socket.gethostname()
    }
  }
  update(data[bstack1l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഋ")], bstack111ll_opy_)
  try:
    response = bstack11l1l1_opy_(bstack1l1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭ഌ"), bstack1l11l11_opy_, data, config)
    if response:
      logger.debug(bstack1lllll1l1_opy_.format(bstack1ll11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_.format(str(e)))
def bstack11l1l1_opy_(type, url, data, config):
  bstack1ll1ll1_opy_ = bstack11llll_opy_.format(url)
  proxy = bstack11l111l1_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ഍")) or config.get(bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧഎ")):
    proxies = {
      bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪഏ"): proxy
    }
  if type == bstack1l1l_opy_ (u"ࠬࡖࡏࡔࡖࠪഐ"):
    response = requests.post(bstack1ll1ll1_opy_, json=data,
                    headers={bstack1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ഑"): bstack1l1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪഒ")}, auth=(config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪഓ")], config[bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬഔ")]), proxies=proxies)
  return response
def bstack1ll1lll1_opy_(framework):
  return bstack1l1l_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢക").format(str(framework), __version__) if framework else bstack1l1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧഖ").format(__version__)
def bstack1llllll1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1ll1l111_opy_()
    logger.debug(bstack1111111l_opy_.format(str(CONFIG)))
    bstack11lll_opy_()
    bstack1l11l1ll_opy_()
  except Exception as e:
    logger.error(bstack1l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤഗ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll111l_opy_
  atexit.register(bstack1ll1l1l1l_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll_opy_)
def bstack1ll111l_opy_(exctype, value, traceback):
  global bstack1lll11111_opy_
  try:
    for driver in bstack1lll11111_opy_:
      driver.execute_script(
        bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ഘ") + json.dumps(bstack1l1l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥങ") + str(value)) + bstack1l1l_opy_ (u"ࠨࡿࢀࠫച"))
  except Exception:
    pass
  bstack1ll1lll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1lll_opy_(message = bstack1l1l_opy_ (u"ࠩࠪഛ")):
  global CONFIG
  try:
    if message:
      bstack111ll_opy_ = {
        bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩജ"): str(message)
      }
      bstack1l11111ll_opy_(bstack111l1ll1_opy_, CONFIG, bstack111ll_opy_)
    else:
      bstack1l11111ll_opy_(bstack111l1ll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1lll111_opy_.format(str(e)))
def bstack1ll1ll11l_opy_(bstack1lllll1_opy_, size):
  bstack1ll11l1ll_opy_ = []
  while len(bstack1lllll1_opy_) > size:
    bstack1ll111111_opy_ = bstack1lllll1_opy_[:size]
    bstack1ll11l1ll_opy_.append(bstack1ll111111_opy_)
    bstack1lllll1_opy_   = bstack1lllll1_opy_[size:]
  bstack1ll11l1ll_opy_.append(bstack1lllll1_opy_)
  return bstack1ll11l1ll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1lllll111_opy_)
    return
  if sys.argv[1] == bstack1l1l_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧഝ")  or sys.argv[1] == bstack1l1l_opy_ (u"ࠬ࠳ࡶࠨഞ"):
    logger.info(bstack1l1l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ട").format(__version__))
    return
  if sys.argv[1] == bstack1l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ഠ"):
    bstack1lll1l_opy_()
    return
  args = sys.argv
  bstack1llllll1l_opy_()
  global CONFIG
  global bstack1l1l1l_opy_
  global bstack1lllll_opy_
  global bstack1111_opy_
  global bstack11llll1_opy_
  global bstack1lllll11l_opy_
  bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠨࠩഡ")
  if args[1] == bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഢ") or args[1] == bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫണ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫത")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഥ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬദ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ധ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧന")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪഩ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫപ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫഫ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬബ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ഭ"):
    bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧമ")
    args = args[2:]
  else:
    if not bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫയ") in CONFIG or str(CONFIG[bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬര")]).lower() in [bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪറ"), bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬല")]:
      bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬള")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩഴ")]).lower() == bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭വ"):
      bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧശ")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഷ")]).lower() == bstack1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩസ"):
      bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪഹ")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨഺ")]).lower() == bstack1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ഻࠭"):
      bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ഼ࠧ")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഽ")]).lower() == bstack1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩാ"):
      bstack1llll1l_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪി")
      args = args[1:]
    else:
      os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ീ")] = bstack1llll1l_opy_
      bstack1ll1l1l_opy_(bstack1l111l1_opy_)
  global bstack11111_opy_
  try:
    os.environ[bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧു")] = bstack1llll1l_opy_
    bstack1l11111ll_opy_(bstack1111l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1lll111_opy_.format(str(e)))
  global bstack1l1l111_opy_
  global bstack1l1l1111_opy_
  global bstack11l111_opy_
  global bstack111l1lll_opy_
  global bstack111ll111_opy_
  global bstack1lll1ll_opy_
  global bstack11ll1l_opy_
  global bstack1ll1l1_opy_
  global bstack1ll1l11_opy_
  global bstack1lll111l_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll111ll1_opy_
  global bstack1lll1ll1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l111_opy_ = webdriver.Remote.__init__
    bstack1ll1l1_opy_ = WebDriver.close
    bstack1l1ll1l1l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11111_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11l11_opy_():
    if bstack11ll1l1_opy_() < version.parse(bstack1ll1llll1_opy_):
      logger.error(bstack1l1lll11l_opy_.format(bstack11ll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll111ll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack111ll1l_opy_.format(str(e)))
  bstack11l11l_opy_()
  if (bstack1llll1l_opy_ in [bstack1l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬൂ"), bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൃ"), bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩൄ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1ll1lll_opy_
      except Exception as e:
        logger.warn(bstack11ll1_opy_ + str(e))
    except Exception as e:
      bstack11lll11_opy_(e, bstack11ll1_opy_)
    bstack1l1l1111_opy_ = Output.end_test
    bstack11l111_opy_ = TestStatus.__init__
    bstack111ll111_opy_ = pabot._run
    bstack1lll1ll_opy_ = QueueItem.__init__
    bstack11ll1l_opy_ = pabot._create_command_for_execution
  if bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൅"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll11_opy_(e, bstack1ll11l_opy_)
    bstack1ll1l11_opy_ = Runner.run_hook
    bstack1lll111l_opy_ = Step.run
  if bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪെ"):
    try:
      from _pytest.config import Config
      bstack1lll1ll1l_opy_ = Config.getoption
    except Exception as e:
      logger.warn(e, bstack1llll1111_opy_)
  if bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫേ"):
    bstack111llll1_opy_()
    bstack1llll1_opy_()
    if bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨൈ") in CONFIG:
      bstack1lllll_opy_ = True
      bstack11l111ll_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൉")]):
        bstack11l111ll_opy_.append(bstack1l1l11l1l_opy_(name=str(index),
                                      target=bstack111l1l11_opy_, args=(args[0], index)))
      for t in bstack11l111ll_opy_:
        t.start()
      for t in bstack11l111ll_opy_:
        t.join()
    else:
      bstack11l1l1l_opy_(bstack1l11l1l_opy_)
      exec(open(args[0]).read())
  elif bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൊ") or bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧോ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11lll11_opy_(e, bstack11ll1_opy_)
    bstack111llll1_opy_()
    bstack11l1l1l_opy_(bstack11l11l11_opy_)
    if bstack1l1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧൌ") in args:
      i = args.index(bstack1l1l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ്"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1l1l_opy_))
    args.insert(0, str(bstack1l1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩൎ")))
    pabot.main(args)
  elif bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൏"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11lll11_opy_(e, bstack11ll1_opy_)
    for a in args:
      if bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ൐") in a:
        bstack1111_opy_ = int(a.split(bstack1l1l_opy_ (u"ࠧ࠻ࠩ൑"))[1])
      if bstack1l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ൒") in a:
        bstack11llll1_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠩ࠽ࠫ൓"))[1])
      if bstack1l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪൔ") in a:
        bstack1lllll11l_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠫ࠿࠭ൕ"))[1])
    bstack11l1l1l_opy_(bstack11l11l11_opy_)
    run_cli(args)
  elif bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬൖ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      import importlib
      bstack1l1ll111_opy_ = importlib.find_loader(bstack1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨൗ"))
    except Exception as e:
      logger.warn(e, bstack1llll1111_opy_)
    bstack111llll1_opy_()
    try:
      if bstack1l1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ൘") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ൙"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬ൚") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭൛"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"ࠫ࠲ࡶࠧ൜") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠬ࠳ࡰࠨ൝"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ൞") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨൟ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"ࠨ࠯ࡱࠫൠ") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠩ࠰ࡲࠬൡ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack111lll1l_opy_ = config.args
    bstack1ll11111l_opy_ = config.invocation_params.args
    bstack1ll11111l_opy_ = list(bstack1ll11111l_opy_)
    bstack1ll1lll11_opy_ = []
    for arg in bstack1ll11111l_opy_:
      for spec in bstack111lll1l_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1ll1lll11_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1l_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫൢ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111lll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11ll1_opy_)))
                    for bstack1ll11ll1_opy_ in bstack111lll1l_opy_]
    if (bstack1ll1ll1l_opy_):
      bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨൣ"))
      bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"࡚ࠬࡲࡶࡧࠪ൤"))
    bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"࠭࠭ࡱࠩ൥"))
    bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬ൦"))
    bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ൧"))
    bstack1ll1lll11_opy_.append(bstack1l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ൨"))
    bstack1l11l11l1_opy_ = []
    for spec in bstack111lll1l_opy_:
      bstack1l11ll1l_opy_ = []
      bstack1l11ll1l_opy_.append(spec)
      bstack1l11ll1l_opy_ += bstack1ll1lll11_opy_
      bstack1l11l11l1_opy_.append(bstack1l11ll1l_opy_)
    bstack1lllll_opy_ = True
    bstack11llllll_opy_ = 1
    if bstack1l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ൩") in CONFIG:
      bstack11llllll_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ൪")]
    bstack1l1111l1_opy_ = int(bstack11llllll_opy_)*int(len(CONFIG[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൫")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൬")]):
      for bstack1l11ll1l_opy_ in bstack1l11l11l1_opy_:
        item = {}
        item[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࠫ൭")] = bstack1l11ll1l_opy_
        item[bstack1l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ൮")] = index
        execution_items.append(item)
    bstack1llll1lll_opy_ = bstack1ll1ll11l_opy_(execution_items, bstack1l1111l1_opy_)
    for execution_item in bstack1llll1lll_opy_:
      bstack11l111ll_opy_ = []
      for item in execution_item:
        bstack11l111ll_opy_.append(bstack1l1l11l1l_opy_(name=str(item[bstack1l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ൯")]),
                                            target=bstack1ll1lllll_opy_,
                                            args=(item[bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࠧ൰")],)))
      for t in bstack11l111ll_opy_:
        t.start()
      for t in bstack11l111ll_opy_:
        t.join()
  elif bstack1llll1l_opy_ == bstack1l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൱"):
    try:
      from behave.__main__ import main as bstack1l1ll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11lll11_opy_(e, bstack1ll11l_opy_)
    bstack111llll1_opy_()
    bstack1lllll_opy_ = True
    bstack11llllll_opy_ = 1
    if bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ൲") in CONFIG:
      bstack11llllll_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭൳")]
    bstack1l1111l1_opy_ = int(bstack11llllll_opy_)*int(len(CONFIG[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൴")]))
    config = Configuration(args)
    bstack111lll1l_opy_ = config.paths
    bstack11l1111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack111lll1l_opy_:
        bstack11l1111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1l_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ൵"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111lll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll11ll1_opy_)))
                    for bstack1ll11ll1_opy_ in bstack111lll1l_opy_]
    bstack1l11l11l1_opy_ = []
    for spec in bstack111lll1l_opy_:
      bstack1l11ll1l_opy_ = []
      bstack1l11ll1l_opy_ += bstack11l1111_opy_
      bstack1l11ll1l_opy_.append(spec)
      bstack1l11l11l1_opy_.append(bstack1l11ll1l_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ൶")]):
      for bstack1l11ll1l_opy_ in bstack1l11l11l1_opy_:
        item = {}
        item[bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࠧ൷")] = bstack1l1l_opy_ (u"ࠫࠥ࠭൸").join(bstack1l11ll1l_opy_)
        item[bstack1l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ൹")] = index
        execution_items.append(item)
    bstack1llll1lll_opy_ = bstack1ll1ll11l_opy_(execution_items, bstack1l1111l1_opy_)
    for execution_item in bstack1llll1lll_opy_:
      bstack11l111ll_opy_ = []
      for item in execution_item:
        bstack11l111ll_opy_.append(bstack1l1l11l1l_opy_(name=str(item[bstack1l1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬൺ")]),
                                            target=bstack1l11l11l_opy_,
                                            args=(item[bstack1l1l_opy_ (u"ࠧࡢࡴࡪࠫൻ")],)))
      for t in bstack11l111ll_opy_:
        t.start()
      for t in bstack11l111ll_opy_:
        t.join()
  else:
    bstack1ll1l1l_opy_(bstack1l111l1_opy_)
  bstack1l11l1lll_opy_()
def bstack1l11l1lll_opy_():
  global CONFIG
  try:
    if bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫർ") in CONFIG:
      host = bstack1l1l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬൽ") if bstack1l1l_opy_ (u"ࠪࡥࡵࡶࠧൾ") in CONFIG else bstack1l1l_opy_ (u"ࠫࡦࡶࡩࠨൿ")
      user = CONFIG[bstack1l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ඀")]
      key = CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩඁ")]
      bstack1l1l11l_opy_ = bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ං") if bstack1l1l_opy_ (u"ࠨࡣࡳࡴࠬඃ") in CONFIG else bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ඄")
      url = bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪඅ").format(user, key, host, bstack1l1l11l_opy_)
      headers = {
        bstack1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪආ"): bstack1l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨඇ"),
      }
      if bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඈ") in CONFIG:
        params = {bstack1l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬඉ"):CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫඊ")], bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඋ"):CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඌ")]}
      else:
        params = {bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩඍ"):CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඎ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1ll1l_opy_ = response.json()[0][bstack1l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩඏ")]
        if bstack1ll1l_opy_:
          bstack1llll1l1l_opy_ = bstack1ll1l_opy_[bstack1l1l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫඐ")].split(bstack1l1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧඑ"))[0] + bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪඒ") + bstack1ll1l_opy_[bstack1l1l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ඓ")]
          logger.info(bstack1l111l11l_opy_.format(bstack1llll1l1l_opy_))
          bstack111111l1_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧඔ")]
          if bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ") in CONFIG:
            bstack111111l1_opy_ += bstack1l1l_opy_ (u"࠭ࠠࠨඖ") + CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ඗")]
          if bstack111111l1_opy_!= bstack1ll1l_opy_[bstack1l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭඘")]:
            logger.debug(bstack1ll1111l1_opy_.format(bstack1ll1l_opy_[bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඙")], bstack111111l1_opy_))
    else:
      logger.warn(bstack1l11ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll111l_opy_.format(str(e)))
def bstack11l1l11_opy_(url, bstack11l1l1ll_opy_=False):
  global CONFIG
  global bstack1l1l1ll_opy_
  if not bstack1l1l1ll_opy_:
    hostname = bstack1ll1l111l_opy_(url)
    is_private = bstack1l11lll11_opy_(hostname)
    if (bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧක") in CONFIG and not CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨඛ")]) and (is_private or bstack11l1l1ll_opy_):
      bstack1l1l1ll_opy_ = hostname
def bstack1ll1l111l_opy_(url):
  return urlparse(url).hostname
def bstack1l11lll11_opy_(hostname):
  for bstack11l1_opy_ in bstack1l1l1l11_opy_:
    regex = re.compile(bstack11l1_opy_)
    if regex.match(hostname):
      return True
  return False