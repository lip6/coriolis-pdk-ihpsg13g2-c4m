# SPDX-License-Identifier: GPL-2.0-or-later
from pdkmaster.io.coriolis import export as c4m_export
from c4m.pdk import ihpsg13g2 as c4m_ihpsg13g2


__all__ = ["c4m_ihpsg13g2", "c4m_tech", "c4m_export"]


c4m_tech = c4m_ihpsg13g2.tech
