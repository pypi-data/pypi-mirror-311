"""Run functions."""

import json
from pathlib import Path
from typing import List

import requests

from pheval_amelie.constants import AMELIE_URL
from pheval_amelie.run.prepare_requests import AmelieParameters, write_parameters


def read_parameters(parameters_file: Path) -> List[AmelieParameters]:
    """
    Read parameters from JSON.

    Args:
        parameters_file (Path): Path to JSON parameters file.

    Returns:
        List[AmelieParameters]: List of parameters.

    """
    with open(parameters_file, "r") as file:
        data = json.load(file)
    file.close()
    return [AmelieParameters(**entry) for entry in data]


def save_response_to_file(response_data: dict, output_path: Path) -> None:
    """
    Save the JSON response data to a file.

    Args:
        response_data (dict): The response.
        output_path (Path): Path to write response.

    """
    with open(output_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4)
    output_file.close()


def post_request(data: dict, files: dict) -> dict:
    """
    Send a POST request and returns the JSON response.

    Args:
        data (dict): The data to pass to the request.
        files (Optional[dict]): The files to pass to the request.

    Returns:
        dict: The response.

    """
    response = requests.post(AMELIE_URL, verify=False, data=data, files=files, timeout=600)
    response.raise_for_status()
    return response.json()


def run_requests(parameters: List[AmelieParameters], raw_results_dir: Path) -> None:
    """
    Run the requests for a corpus.

    Args:
       parameters (List[AmelieParameters]): List of parameters.
       raw_results_dir (Path): Path to the raw results directory.

    """
    for parameter in parameters:
        data = {
            "dominantAlfqCutoff": 0.1,
            "alfqCutoff": 0.5,
            "filterByCount": False,
            "hmctCutoff": 1,
            "alctCutoff": 3,
            "patientName": parameter.patient_name,
            "patientSex": parameter.patient_sex,
            "onlyPassVariants": True,
            "filterRelativesOnlyHom": False,
            "phenotypes": ",".join(parameter.phenotypes),
        }
        files = {"vcfFile": open(parameter.vcf_file, "rb")}
        try:
            response_data = post_request(data, files)
            output_filename = raw_results_dir.joinpath(f"{parameter.phenopacket_path_stem}.json")
            save_response_to_file(response_data, output_filename)
        finally:
            if files:
                files["vcfFile"].close()


def run(testdata_dir: Path, tool_input_commands_dir: Path, raw_results_dir: Path) -> None:
    """
    Run AMELIE on the corpus.

    Args:
        testdata_dir(Path): Path to the test data directory.
        tool_input_commands_dir(Path): Path to the tool input command directory.
        raw_results_dir (bool): Path to raw results directory.

    """
    write_parameters(testdata_dir.joinpath("phenopackets"), testdata_dir, tool_input_commands_dir)
    parameters_file = tool_input_commands_dir.joinpath(testdata_dir.name + "_parameters.json")
    parameters = read_parameters(parameters_file)
    run_requests(parameters, raw_results_dir)
