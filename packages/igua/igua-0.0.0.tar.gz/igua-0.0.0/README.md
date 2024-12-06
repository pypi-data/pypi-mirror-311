# 🦎 IGUA 

*Iterative Gene clUster Analysis*.

## 🗺️  Overview

IGUA is a novel method for high-throughput content-agnostic identification
of Gene Cluster Families. It was designed to assist in complementary 
downstream analyses of the results of our Biosynthetic Gene Cluster 
detection tool, [GECCO](https://pypi.org/project/gecco-tool).

**📝 An actual release will be made once the method has been described in a 
scientific manuscript, currently in preparation. Until then, individual 
access may be granted on e-mail request.**


## 🔧 Installing

IGUA will ultimately be available directly from PyPI and Bioconda, but for
now you can only install it through GitHub, provided you have access. 
Clone the private repository and then install the package with:

```console
$ git clone https://github.com/althonos/IGUA
$ pip install --user ./IGUA
```

## 💡 Running

### 📥 Inputs

The gene clusters to pass to IGUA must be in GenBank format, with one gene
cluster per record, and gene annotations inside `CDS` features, as typically
produced by gene calling tools. Several GenBank files can be passed
to the same pipeline run.

```console
$ igua -i clusters1.gbk -i clusters2.gbk ...
```

The GenBank locus identifier will be used as the name of each gene cluster. This
may cause problems with gene clusters obtained with some tools, such as antiSMASH.
If the input contains duplicate identifiers, the first gene cluster with a given
identifier will be used, and a warning will be displayed.


### 📤 Outputs

The main output of IGUA is a TSV file which assigns a Gene Cluster Family to
each gene cluster found in the input. The GCF identifiers are arbitrary, and
the prefix can be changed with the `--prefix` flag. The table will also record
the original file from which each record was obtained to facilitate resource
management. The table is written to the filename given with the `--output`
flag.


## 💭 Feedback

### ⚠️ Issue Tracker

Found a bug ? Have an enhancement request ? Head over to the [GitHub issue
tracker](https://github.com/althonos/IGUA/issues) if you need to report
or ask something. If you are filing in on a bug, please include as much
information as you can about the issue, and try to recreate the same bug
in a simple, easily reproducible situation.

### 🏗️ Contributing

Contributions are more than welcome! See
[`CONTRIBUTING.md`](https://github.com/althonos/IGUA/blob/main/CONTRIBUTING.md)
for more details.


## 📋 Changelog

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html)
and provides a [changelog](https://github.com/althonos/IGUA/blob/main/CHANGELOG.md)
in the [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) format


## ⚖️ License

IGUA is provided under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/).

*This project was developed by [Martin Larralde](https://github.com/althonos/)
during his PhD project at the [European Molecular Biology Laboratory](https://www.embl.de/)
and the [Leiden University Medical Center](https://lumc.nl/en/)
in the [Zeller team](https://github.com/zellerlab).*
