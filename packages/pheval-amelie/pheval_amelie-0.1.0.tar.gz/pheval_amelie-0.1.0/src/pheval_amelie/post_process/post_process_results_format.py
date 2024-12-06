"""Post Process AMELIE result functions."""

import json
from pathlib import Path
from typing import Dict, List

from pheval.post_processing.post_processing import PhEvalGeneResult, generate_pheval_result
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_amelie_result(amelie_result: Path) -> Dict:
    """
    Parse the AMELIE JSON result.

    Args:
        amelie_result (Path): Path to the AMELIE JSON result.

    Returns:
        Dict: Parsed AMELIE result.

    """
    with open(amelie_result, "r") as file:
        result = json.load(file)
    file.close()
    return result


class PhEvalGeneResultFromAmelieCreator:
    """Class for converting AMELIE JSON result to PhEvalGeneResult."""

    def __init__(self, amelie_result: Dict, gene_identifier_updator: GeneIdentifierUpdater):
        """Initialise PhEvalGeneResultFromAmelieCreator class."""
        self.amelie_result = amelie_result
        self.gene_identifier_updater = gene_identifier_updator

    @staticmethod
    def _find_gene_symbol(gene_entry: List) -> str:
        """
        Find the gene symbol.

        Args:
            gene_entry (List): A gene entry from the AMELIE JSON result.

        Returns:
            str: The gene symbol.

        """
        return gene_entry[0]

    def _find_gene_identifier(self, gene_entry: List) -> str:
        """
        Find the gene identifier.

        Args:
            gene_entry (List): A gene entry from the AMELIE JSON result.

        Returns:
            str: The gene identifier.

        """
        return self.gene_identifier_updater.find_identifier(self._find_gene_symbol(gene_entry))

    @staticmethod
    def _find_highest_score(gene_entry: List) -> float:
        """
        Find the highest score for a gene entry.

        Args:
            gene_entry (list): A gene entry from the AMELIE JSON result.

        Returns:
            float: Highest score.

        """
        scores = [result[1] for result in gene_entry[1]]
        return max(scores)

    def extract_pheval_gene_requirements(self) -> List[PhEvalGeneResult]:
        """
        Extract PhEval Gene requirements from AMELIE JSON result.

        Returns:
            List[PhEvalGeneResult]: List of PhEvalGeneResult.

        """
        simplified_amelie_result = []
        for gene_entry in self.amelie_result:
            simplified_amelie_result.append(
                PhEvalGeneResult(
                    gene_symbol=self._find_gene_symbol(gene_entry),
                    gene_identifier=self._find_gene_identifier(gene_entry),
                    score=self._find_highest_score(gene_entry),
                )
            )
        return simplified_amelie_result


def create_standardised_results(results_dir: Path, output_dir: Path) -> None:
    """
    Write standardised gene results from default AMELIE JSON output.

    Args:
        results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.

    """
    hgnc_data = create_hgnc_dict()
    gene_identifier_updator = GeneIdentifierUpdater(hgnc_data=hgnc_data, gene_identifier="ensembl_id")
    for result in all_files(results_dir):
        amelie_result = read_amelie_result(result)
        pheval_gene_result = PhEvalGeneResultFromAmelieCreator(
            amelie_result, gene_identifier_updator
        ).extract_pheval_gene_requirements()
        generate_pheval_result(
            pheval_result=pheval_gene_result,
            sort_order_str="DESCENDING",
            output_dir=output_dir,
            tool_result_path=result,
        )
