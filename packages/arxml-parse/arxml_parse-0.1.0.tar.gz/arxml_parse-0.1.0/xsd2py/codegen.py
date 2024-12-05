import re
import subprocess
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

CODEGEN_DIR = Path(__file__).parent
PROJECT_DIR = CODEGEN_DIR.parent
LIBRARY_DIR = PROJECT_DIR / "src" / "arxml_parse"
URL_MAP = {
    "AUTOSAR_00042.xsd": "https://www.autosar.org/fileadmin/standards/R17-03_R1.1.0/AP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00043.xsd": "https://www.autosar.org/fileadmin/standards/R17-10_R1.2.0/AP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00044.xsd": "https://www.autosar.org/fileadmin/standards/R4.3.1/CP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00045.xsd": "https://www.autosar.org/fileadmin/standards/R18-03_R1.4.0/AP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00046.xsd": "https://www.autosar.org/fileadmin/standards/R18-10_R4.4.0_R1.5.0/CP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00047.xsd": "https://www.autosar.org/fileadmin/standards/R19-03/AP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00048.xsd": "https://www.autosar.org/fileadmin/standards/R19-11/AP/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00049.xsd": "https://www.autosar.org/fileadmin/standards/R20-11/FO/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00050.xsd": "https://www.autosar.org/fileadmin/standards/R21-11/FO/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00051.xsd": "https://www.autosar.org/fileadmin/standards/R22-11/FO/AUTOSAR_MMOD_XMLSchema.zip",
    "AUTOSAR_00052.xsd": "https://www.autosar.org/fileadmin/standards/R23-11/FO/AUTOSAR_FO_MMOD_XMLSchema.zip",
}


def download_xsd(zipfile_url: str) -> tuple[str, bytes]:
    resp = urlopen(zipfile_url)
    myzip = ZipFile(BytesIO(resp.read()))
    for zip_member in myzip.namelist():
        if not re.match(r"AUTOSAR_\d+\.xsd$", zip_member):
            continue
        return zip_member, myzip.read(zip_member)
    raise FileNotFoundError


if __name__ == "__main__":
    xsd_directories: list[Path] = []
    for xsd_name, xsd_zip_url in URL_MAP.items():
        xsd_dir = CODEGEN_DIR / Path(xsd_name).stem.lower().replace("-", "_")
        xsd_directories.append(xsd_dir)
        if not xsd_dir.exists():
            xsd_dir.mkdir()
        xsd_path = xsd_dir / xsd_name
        if not xsd_path.exists():
            download_name, xsd_bytes = download_xsd(xsd_zip_url)
            assert download_name == xsd_name
            xsd_path.write_bytes(xsd_bytes)

    for xsd_dir in xsd_directories:
        target_dir = LIBRARY_DIR / xsd_dir.name
        subprocess.run(
            [
                "xsdata",
                "generate",
                "--config",
                CODEGEN_DIR / ".xsdata.xml",
                "--package",
                target_dir.name,
                xsd_dir,
            ],
            cwd=LIBRARY_DIR,
            check=False,
        )
        subprocess.run(
            [
                "ruff",
                "check",
                "--config",
                PROJECT_DIR / "pyproject.toml",
                "--fix",
                target_dir,
            ],
            cwd=PROJECT_DIR,
            check=False,
        )
        subprocess.run(
            [
                "ruff",
                "format",
                "--config",
                PROJECT_DIR / "pyproject.toml",
                target_dir,
            ],
            cwd=PROJECT_DIR,
            check=False,
        )
