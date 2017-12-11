from Bio import SeqIO


for record in SeqIO.parse("BRCA1.fasta", "fasta"):
    if "Homo sapiens" in record.description:
        brca_hs = record
        break

with open("BRCA1_homo_sapiens.fasta", "w") as outfile:
    SeqIO.write(brca_hs, outfile, "fasta")


    