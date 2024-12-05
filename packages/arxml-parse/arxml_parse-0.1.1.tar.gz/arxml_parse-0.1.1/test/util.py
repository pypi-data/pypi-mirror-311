import re
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / "data"
URL_MAP = {
    "AUTOSAR_00044.xsd": "https://www.autosar.org/fileadmin/standards/R4.3.1/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00046.xsd": "https://www.autosar.org/fileadmin/standards/R18-10_R4.4.0_R1.5.0/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00048.xsd": "https://www.autosar.org/fileadmin/standards/R19-11/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00049.xsd": "https://www.autosar.org/fileadmin/standards/R20-11/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00050.xsd": "https://www.autosar.org/fileadmin/standards/R21-11/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00051.xsd": "https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_MOD_AISpecificationExamples.zip",
    "AUTOSAR_00052.xsd": "https://www.autosar.org/fileadmin/standards/R23-11/CP/AUTOSAR_CP_MOD_AISpecificationExamples.zip",
}


def download_arxml(zipfile_url: str) -> tuple[str, bytes]:
    resp = urlopen(zipfile_url)
    myzip = ZipFile(BytesIO(resp.read()))
    for zip_member in myzip.namelist():
        if not re.match(r".*\.arxml$", zip_member):
            continue
        return zip_member, myzip.read(zip_member)
    raise FileNotFoundError


def get_example_file(schema_name: str) -> Path:
    """Retrieve cached arxml from data directory or download."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    target_path = DATA_DIR / (Path(schema_name).stem + "_example.arxml")
    if not target_path.exists():
        _name, arxml_bytes = download_arxml(URL_MAP[schema_name])
        target_path.write_bytes(arxml_bytes)
    return target_path
