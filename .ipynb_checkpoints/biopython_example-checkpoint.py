"""
Using BioPython to search sequences and parse files
"""
from Bio import Entrez

search_term = 'shh'
Entrez.email = 'tuc12093@temple.edu'
search_handle = Entrez.esearch(db="nucleotide",
                               term=search_term,
                               usehistory="y",
                               idtype="acc")
search_results = Entrez.read(search_handle)
search_handle.close()

acc_list = search_results["IdList"]
count = int(search_results["Count"])
print(count == len(acc_list))

webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]

try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2

batch_size = 3
outfile = search_term + ".fasta"
out_handle = open(outfile, "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    while attempt < 3:
        attempt += 1
        try:
            fetch_handle = Entrez.efetch(db="nucleotide",
                                         rettype="fasta", retmode="text",
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key,
                                         idtype="acc")
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                time.sleep(15)
            else:
                raise
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
out_handle.close()
