"""Prepare requests functions."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Union

from phenopackets import Sex
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class AmelieParameters:
    """Class to store AMELIE parameters."""

    phenopacket_path_stem: str
    phenotypes: List[str]
    patient_name: str
    patient_sex: str
    vcf_file: str


def _return_hpo_list(phenopacket_util: PhenopacketUtil) -> List[str]:
    """
    Return HPO list from Phenopacket file.

    Args:
        phenopacket_util: Phenopacket Util object.

    Returns:
        List[str]: HPO list from Phenopacket Util object.

    """
    return [hpo.type.id for hpo in phenopacket_util.observed_phenotypic_features()]


def _return_patient_name(phenopacket_util: PhenopacketUtil) -> str:
    """
    Return the Sample ID from a phenopacket.

    Args:
        phenopacket_util (PhenopacketUtil): Phenopacket Util object.

    Returns:
        str: Sample ID.

    """
    return phenopacket_util.sample_id()


def _return_vcf_file(phenopacket_path: Path, phenopacket_util: PhenopacketUtil, testdata_dir: Path) -> str:
    """
    Return the path to the VCF file.

    Args:
        phenopacket_path (Path): Path to the Phenopacket file.
        phenopacket_util (PhenopacketUtil): PhenopacketUtil object.
        testdata_dir (Path): Path to the test data directory.

    Returns:
        str: Path to the VCF directory

    """
    return phenopacket_util.vcf_file_data(phenopacket_path, testdata_dir.joinpath("vcf")).uri


def _return_patient_sex(phenopacket_util: PhenopacketUtil) -> Union[str, None]:
    """
    Return the patient sex.

    Args:
        phenopacket_util (PhenopacketUtil): PhenopacketUtil object.

    Returns:
        Union[str,None]: Patient sex if there is one.

    """
    patient_sex = Sex.Name(phenopacket_util.phenopacket_contents.subject.sex)
    if patient_sex == "UNKNOWN_SEX":
        return None
    else:
        return patient_sex.upper()


def get_parameters(phenopacket_dir: Path, testdata_dir: Path) -> List[AmelieParameters]:
    """
    Get parameters for a corpus.

    Args:
        phenopacket_dir (Path): Path to Phenopacket directory.
        testdata_dir (Path): Path to testdata directory.

    Returns:
        List[AmelieParameters]: List of parameters for the corpus

    """
    parameters = []
    for phenopacket_path in all_files(phenopacket_dir):
        phenopacket_util = PhenopacketUtil(phenopacket_reader(phenopacket_path))
        parameters.append(
            AmelieParameters(
                phenopacket_path_stem=phenopacket_path.stem,
                phenotypes=_return_hpo_list(phenopacket_util),
                patient_name=_return_patient_name(phenopacket_util),
                patient_sex=_return_patient_sex((phenopacket_util)),
                vcf_file=_return_vcf_file(phenopacket_path, phenopacket_util, testdata_dir),
            )
        )
    return parameters


def write_parameters(phenopacket_dir: Path, testdata_dir: Path, tool_input_commands_dir: Path) -> None:
    """
    Write the parameters to a JSON file.

    Args:
        phenopacket_dir (Path): Path to Phenopacket directory.
        testdata_dir (Path): Path to testdata directory.
        tool_input_commands_dir (Path): Path to tool input commands dir.

    """
    output_file = tool_input_commands_dir.joinpath(testdata_dir.name + "_parameters.json")
    patients = get_parameters(phenopacket_dir, testdata_dir)
    with open(output_file, "w") as file:
        json.dump([asdict(patient) for patient in patients], file, indent=4)
    file.close()
