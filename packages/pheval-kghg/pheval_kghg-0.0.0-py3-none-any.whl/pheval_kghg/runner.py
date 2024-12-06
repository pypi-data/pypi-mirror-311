"""Custom Pheval Runner."""
# General imports
import os
import subprocess
import pandas as pd
from pathlib import Path
from packaging import version
from dataclasses import dataclass
from typing import Optional, List
from pydantic import (BaseModel, 
                      Field)

# Pheval imports
from pheval.runners.runner import PhEvalRunner
from pheval.utils.file_utils import (all_files,
                                     files_with_suffix)
from pheval.post_processing.post_processing import (PhEvalDiseaseResult,
                                                    generate_pheval_result)



class KgHgConfigurations(BaseModel):
    """
    Class for defining the kghg configurations in tool_specific_configurations field,
    within the input_dir config.yaml
    Args:
        environment (str): Environment to run kghg, i.e., local/docker (only local supported)
        path_to_kghg (str): File path to kghg.py 
        path_to_nodes (str): File path to monarch-kg_nodes.tsv
        path_to_edges (str): File path to monarch-kg_edges.tsv
    """

    environment: str = Field(...)
    path_to_nodes: str = Field(...)
    path_to_edges: str = Field(...)
    path_to_kghg: Optional[str] = None


@dataclass
class KgHgPhevalRunner(PhEvalRunner):
    """
    CustomPhevalRunner Class.
    """

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """
        prepare method (Currently un-used for this runner)
        """
        dummy_variable = 0


    def run(self):
        """
        Generates kghg command line call and writes to file, then runs the command through subprocess
        """

        # Gather tool config options and create output path to write command to 
        config = KgHgConfigurations.model_validate(self.input_dir_config.tool_specific_configuration_options)
        tool_command_outpath = str(self.tool_input_commands_dir.joinpath("kghg_commands.txt"))
        
        # outputd_dir is the top level directory for the results for this run.
        # So we pass in self.raw_results_dir instead so that the tool will output there instead to work with pheval
        self.run_kghg_local(input_dir=self.testdata_dir,
                            output_dir=self.raw_results_dir,
                            tool_input_commands_path=tool_command_outpath,
                            config=config)
    

    # Run (main function  with arguments expanded for readability called b)
    def run_kghg_local(self,
                       input_dir: Path,
                       output_dir: Path,
                       tool_input_commands_path: str,
                       config: KgHgConfigurations) -> None:
        """
        Run kghg locally and write command to a file for record keeping
        """

        # Combine arguments into subprocess friendly command format
        if config.path_to_kghg != None:
            subp_command = ["python", config.path_to_kghg]
        else:
            subp_command = ["pheval-kghg"]

        # Add the rest of our command options
        subp_command += ["rank-associations",
                         "-i", input_dir,
                         "-o", output_dir,
                         "-n", config.path_to_nodes,
                         "-e", config.path_to_edges]
        
        # Write command to file
        with open(tool_input_commands_path, 'w') as outfile:
            outfile.write(' '.join([str(v) for v in subp_command])) # Must convert Path objects to strings

        # Run kghg through subprocss
        subprocess.run(subp_command, shell=False)


    def post_process(self):
        """
        Converts disease results file from kghg to a pheval benchmarking compatible version across all files in the
        raw_results_dir. Results are then written to the pheval_disease_results directory
        """

        # Disease results
        if self.input_dir_config.disease_analysis == True:
            for fname in files_with_suffix(self.raw_results_dir, suffix='.tsv'):
                self.convert_to_pheval_disease_results(str(fname), self.output_dir)
        
        ## self.input_dir_config.disease_analysis
        ## self.input_dir_config.gene_analysis
        ## self.input_dir_config.variant_analysis

        # TO DO: Potentially 
        ##if gene_analysis == True:
        ##if variant_analysis == True:


    # Post process (sub function)
    def convert_to_pheval_disease_results(self, res_path: str, output_dir: str):
        """
        Opens raw results file as dataframe, converts to lists, and uses phevals built in results formatting to
        convert and write disease results to relevant pheval_disease_results directory
        """

        # Open and convert to lists
        analysis_df = pd.read_csv(res_path, sep='\t', header=0)
        ranks = list(analysis_df["rank"])
        pvals = list(analysis_df["pvalue"]) 
        names = list(analysis_df["disease_name"]) 
        ids = list(analysis_df["disease_identifier"])

        # Convert data to pheval results
        results = [PhEvalDiseaseResult(disease_name=d[2],
                                       disease_identifier=d[3],
                                       score=float(d[1])) for d in zip(ranks, pvals, names, ids)]
            
        # Now leverage pheval to write disease results to disease results directory with accompanying filename suffixs
        # Note, that we need to format samplename_results.tsv --> samplename.tsv so that the pheval post_processing .stem
        # function will pull in the appropriate sample name
        tool_res_path = Path(res_path.replace("_results", ''))
        pheval_res = generate_pheval_result(pheval_result=results,
                                            sort_order_str='ascending', # We want lowest pvalue to highest
                                            output_dir=output_dir,
                                            tool_result_path=tool_res_path)



