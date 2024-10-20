## Database autoverification tool
Auto verification for updates to clinvar database when used in bioinfomatics pipeline. 

## Usage Guidelines
1. input file should be a compressed VCF file (gzipped) x 2
2. first VCF - database annotated VCF file from laboratory's pipeline
3. second VCF - original database
4. code for result txt files
```Bash
python3 db_auto_ver.py ~/Downloads/clinvar_20240909.vcf.gz ~/Downloads/clinvar_20240909_processed_cincseq_roi_echtvar_annotated.vcf.gz
```