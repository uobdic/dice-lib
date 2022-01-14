from typing import Dict, List

HDFS_FUSE_MOUNT: str = "/hdfs"
STORAGE_MOUNT: str = "/storage"
SCRATCH_MOUNT: str = "/scratch"
SOFTWARE_MOUNT: str = "/software"

STORAGE_ELEMENT: str = "lcgse01.phy.bris.ac.uk"
SE_ENDPOINTS: Dict[str, str] = {
    "gsiftp": "gsiftp://lcgse01.phy.bris.ac.uk:2811",
    "xrootd": "root://lcgse01.phy.bris.ac.uk/",
    "webdav": "davs://lcgse01.phy.bris.ac.uk:443",
}
SE_MOUNT_POINT: str = "/dpm/phy.bris.ac.uk/home"

STORAGE_ELEMENT_2: str = "xrootd.phy.bris.ac.uk"
SE_ENDPOINTS_2: Dict[str, str] = {
    "xrootd": "root://xrootd.phy.bris.ac.uk:1094/",
    "webdav": "davs://xrootd.phy.bris.ac.uk:1094",
}
SE_MOUNT_POINT_2: str = "/xrootd"

FTS_SERVERS: List[str] = [
    "fts3-pilot.cern.ch:8446",
]

GLOSSARY: Dict[str, str] = {
    "CE": "Computing Element",
    "DICE": "Data Intensive Computing Environment",
    "FTS": "File Transfer Service",
    "HDFS": "Hadoop Distributed File System",
    "SE": "Storage Element",
}
