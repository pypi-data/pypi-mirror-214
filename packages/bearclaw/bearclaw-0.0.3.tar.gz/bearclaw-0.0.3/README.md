# Bearclaw
Components to help extract features from variants, to be used as part of a pipeline.

## Installation
```bash
pip3 install bearclaw
```

## Usage
```python
from bearclaw.preprocessing import VariantDataGenerator
from bearclaw.transforms import spectrum


# Dataframe containing locations of VCF files and labels.
dataframe = DataFrame({
    "vcf": [
        "src/test/resources/GRCh37/sample1.vcf",
        "src/test/resources/GRCh37/sample2.vcf",
    ],
    "class": [1, 0],
})
# Transform VCF files into features using `spectrum`, which counts the number of variants by flanking context.
dg = VariantDataGenerator(transform=spectrum)

# Convert dataframe to label `y` and features `X_spectrum` using `spectrum`.
X_spectrum, y = dg.flow_from_dataframe(dataframe, x_col="vcf")
```

## Reference documentation
https://hylkedonker.gitlab.io/bearclaw/


## License
For open source projects, say how it is licensed.
