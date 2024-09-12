import requests
import gzip
from sys import argv

# filename = input('Enter file location (VCF): ')
filename1 = argv[1]
filename2 = argv[2]

vcf_data1 = {}

print('Reading clinvar VCF file...')

with gzip.open(filename1, 'r') as file_n:
    for bline in file_n:
        line = bline.decode('UTF-8')
        if not line.startswith('#'):
            columns = line.strip('\n').split('\t')
            database_id = columns[2]
            col8 = columns[7]
            info = col8.split(';')

            cln_sig = ''
            cln_revstat = ''

            for item in info:
                if 'CLNSIG' in item:
                    cln_sig = item.split('=')[1]
                if 'CLNREVSTAT' in item:
                    cln_revstat = item.split('=')[1]

            vcf_data1[database_id] = [cln_sig, cln_revstat]

vcf_data2 = {}

print('Reading pipeline output VCF file...')

with gzip.open(filename2, 'r') as file_n:
    for bline in file_n:
        line =  bline.decode('UTF-8')
        if not line.startswith('#'):
            columns = line.strip('\n').split('\t')
            col8 = columns[7]
            info = col8.split(';')
            cln_sig = ''
            cln_revstat = ''
            database_id = ''

            for item in info:
                if 'clinvar_sig' in item and not 'MISSING' in item:
                    cln_sig = item.split('=')[1]
                if 'clinvar_review' in item and not 'MISSING' in item:
                    cln_revstat = item.split('=')[1]
                if 'clinvar_id' in item and not 'MISSING' in item:
                    database_id = item.split('=')[1]

            vcf_data2[database_id] = [cln_sig, cln_revstat]

match_f_count = 0
match_nf_count = 0

print('Analyzing results...')

for database_id, values in vcf_data2.items():
    sig2 = values[0]
    rating2 = values[1]
    if database_id in vcf_data1:
        vals = vcf_data1[database_id]
        sig1 = vals[0]
        rating1 = vals[1]
        if sig1 == sig2 and rating1 == rating2:
            match_f_count += 1
        else:
            match_nf_count += 1
            print(f'Match not found.\nDatabase id: {database_id}\nSignificance observed: {sig2}\nSignificane expected: {sig1}\nRating observed: {rating2}\nRating expected: {rating1}')


print(f'Matches found: {match_f_count}\nMatches not found: {match_nf_count}\nTotal variants: {match_nf_count + match_f_count}')