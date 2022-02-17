#!/usr/bin/env python3
# from __future__ import annotations
from GCore import GCoreBase, GCoreAuth, GCoreCloudRegion, GCoreCloudProject


class GCoreInstance(GCoreBase):
    def __init__(self, creds: GCoreAuth, project: GCoreCloudRegion, region: GCoreCloudProject):
        super().__init__(creds)
        self.region = region
        self.project = project