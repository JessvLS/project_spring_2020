#On April 16, 2020:

"Got approval to work on the RAMPART sequencing pipeline for norovirus, a project whose code was laid out by a collaborator, but would be updated for our lab's purposes"

#On April 20, 2020:

" * Original files were uploaded from https://github.com/aineniamh/realtime-noro"
" * README.md was updated to include the project goals we intended to accomplish"

#On April 21, 2020:

" * A new references.fasta was crafted to merge the exisiting reference sequences with a complete set of references for all uncommon noro strains"

#On April 22,2020:

" * genome.json was edited to correct for overlapping ORFs - original file did not have this overlap"
" * genome.json was edited to have correct GI numbering to accommodate mapping noro genomes larger than GI.1"
" * pipelines.json was edited to drop 'min_read' coverage from 50 to 10 to assume complete genome coverage"
" * protocol.json was edited to drop 'min_identity' from 'annotationOptions' from 50 to 10 to assure complete genome coverage"
" * protocol.json was edited to remove 'require_two_barcodes' from 'annotationOptions' to account for poor barcoding during wetlab prep"
" * primer_file.csv was updated to include the primers our lab used to generate amplicon pools spanning each noro genotype"
" * RAN A TEST RUN OF DATA - FAIL"
" * Updated RAMPART and environment.yml used to run the current version of RAMPART"
" * RE-RAN TEST RUN - SUCCESS; Issue 1 fixed; Issues 2, 3, 4 outlined in our goals on the README.md still stand"

#On April 23, 2020:

" * README.md containing our goals and original text was moved to parent folder; new README.md was crafted under project_spring_2020/project_spring_2020"
" * Test fastq files containing sequences from a noro run were added to the 'tests/test-fastq' directory"

#On May 4, 2020:

" * environment.yml was moved to root directory"
" * setup.py was coded for, but unsure of how to finalize packaging - do we need to upload it to pypi?"

#On May 7, 2020:

" * config.yml from circleci folder was deleted; meta.yaml outlining conda config uploaded to root directory"
" * run_test.py changed to run_test.txt as per notation in meta.yaml"

#Current work:

" * Issue 2 - Visualization issues are coded within the RAMPART program and are coded in JavaScript - will need to contact original coder James Hadfield."
" * Issues 3 and 4 - Consensus pipelines have been updated following NCoV2019 work - we are working with original coding team to update python script in Snakemake files accordingly."
