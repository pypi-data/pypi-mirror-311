# PhEval Runner for AMELIE

This is the AMELIE plugin for PhEval. With this plugin, you can leverage the gene prioritisation tool, AMELIE, to run the PhEval pipeline seamlessly. The setup process for running the full PhEval Makefile pipeline differs from setting up for a single run. The Makefile pipeline creates directory structures for corpora and configurations to handle multiple run configurations. Detailed instructions on setting up the appropriate directory layout, including the input directory and test data directory, can be found here.

## Installation

Clone the pheval.amelie repo and set up the poetry environment:

```sh
git clone https://github.com/yaseminbridges/pheval.amelie.git

cd pheval.amelie

poetry shell

poetry install

```

Alternatively, install with pip:

```shell
pip install pheval_amelie
```

## Configuring a *single* run

### Setting up the input directory

A config.yaml should be located in the input directory and formatted like so:

```yaml
tool: AMELIE
tool_version: 3.1.0
variant_analysis: False
gene_analysis: True
disease_analysis: False
tool_specific_configuration_options:
```

The bare minimum fields are filled to give an idea on the requirements, as AMELIE is gene prioritisation tool, only `gene_analysis` should be set to `True` in the config. An example config has been provided pheval.amelie/config.yaml.


The overall structure of the input directory should look something like so:
```tree
.
└── config.yaml
```

### Setting up the testdata directory

The AMELIE plugin for PhEval accepts phenopackets and gzipped VCF files as an input for running AMELIE. 

The testdata directory should include a subdirectory named phenopackets and a subdirectory named vcf:

```tree
├── testdata_dir
   ├── phenopackets
   └── vcf
```

## Run command

Once the testdata and input directories are correctly configured for the run, the pheval run command can be executed.

```sh
pheval run --input-dir /path/to/input_dir \
--testdata-dir /path/to/testdata_dir \
--runner ameliephevalrunner \
--output-dir /path/to/output_dir \
--version 3.1.0
```



# Docs

https://yaseminbridges.github.io/pheval.amelie/

# Acknowledgements

This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [pheval-runner-template](https://github.com/yaseminbridges/pheval-runner-template.git) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).
