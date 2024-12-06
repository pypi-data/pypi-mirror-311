# General imports
import os
import sys
import click
import scipy
import numpy as np
import pandas as pd
import networkx as nx
from pathlib import Path
from collections import Counter
from typing import List, Set

# Pheval phenopacket utils
from pheval.utils.phenopacket_utils import phenopacket_reader
from pheval.utils.phenopacket_utils import PhenopacketUtil


@click.group()
def main():
    """
    Main entry point for the CLI tool.
    """
    pass


def gather_input_output_info(input_path, output_path, results_suffix="_results.tsv"):
    """
    Input is allowed to be a directory containing .json phenopacket files
    Or input is allowed to be a filepath specifying a .json phenopacket
    """
    
    if os.path.isdir(input_path):
        process_data = [os.path.join(input_path, fname) for fname in os.listdir(input_path) if fname.endswith(".json")]
        
    elif os.path.isfile(input_path) and input_path.endswith(".json"):
        process_data = [input_path]
    
    else:
        return None, None
    
    # Format output file names
    out_data = [os.path.join(output_path, pname.split('/')[-1].replace(".json", results_suffix)) for pname in process_data]
    
    return process_data, out_data


def get_entities_from_file(infile_path: str, select_data: set, match_column: str ='category') -> list[dict]:
    """
    Expects a tabular file with the header as the first line. Will pull rows from the file where
    where the column whos name matches match_column are found within the select_data 
    (ie we only want rows where column-xyz matches a name within the select_data argument)
    
    Allows one to pull specific node and edge types from the monarch knowledge graph
    """
    
    # Instead of using pandas to load into memory, we will be memory conscious and load in only select nodes
    return_data = []
    with open(infile_path) as infile:
        header_info = {v:i for i,v in enumerate(infile.readline().strip('\r').strip('\n').split('\t'))}
        
        # Ensure relevant columns exist in header before we proceed
        if (match_column not in header_info) or ("id" not in header_info):
            print("- ERROR Header line is expected to be first line of file with columns 'category' and 'id'")
            return None
        
        # Loop through file and pull nodes
        for line in infile:
            cols = line.strip('\r').strip('\n').split('\t')
            entity = cols[header_info[match_column]]
            if entity not in select_data:
                continue
            
            # Convert row into dictionary and append to list
            return_data.append({k:cols[v] for k,v in header_info.items()})
            
    print("- Entities returned {} of types...".format(format(len(return_data), ',')))
    for k, v in Counter([c[match_column] for c in return_data]).items():
        print("- {} {}".format(k, format(v, ',')))
                                                   
    return return_data


def make_graph(nodes, edges):
    """
    Creates a networkx graph from a list of nodes [{'id':id, attribute1:'xyz',...}] and edges of the same formatting.
    The 'id' for each node is used as the node id within the graph and the rest is added in as attributes.
    Edges are only added if both nodes exist in the graph and all other information is added as an edge attribute
    """
    
    # Record keeping
    node_attr_count = 0
    edge_attr_count = 0
    dangling_edges = 0
    repeat_edges = 0
    
    # Initiate graph and add nodes
    kg_graph = nx.Graph()
    for node in nodes:
        
        # Add node
        kg_graph.add_node(node["id"])
        
        # Add attributes
        attributes = {node["id"]:{k:v for k,v in node.items() if k != "id"}}
        
        nx.set_node_attributes(kg_graph, attributes)
        node_attr_count += len(attributes[node["id"]])
    

    # Add edges
    for edge in edges:
        
        # Ensure both nodes of edge exist in graph
        e1, e2 = (edge["subject"], edge["object"])
        eid, eid_rev = (e1, e2), (e2, e1)
        if (not kg_graph.has_node(e1)) or (not kg_graph.has_node(e2)):
            dangling_edges += 1
            continue
        
        # Check for potential repeat edge
        elif kg_graph.has_edge(e1, e2):
            repeat_edges += 1
            
            #repeat_edges[eid].append(edge)
            #repeat_edges[eid_rev].append(edge)
            
            # The "repeat_edges" (subject, object) demonstrate the consolodation of different ontologies --> mondo
            #for r in repeat_edges[eid]:
            #    print(r["object"], r["subject"], r["predicate"], r["category"])
            #print("################")
            #print("################")
        
        else:
            ##repeat_edges.update({eid:[edge]})
            ##repeat_edges.update({eid_rev:[edge]})
            #print(repeat_edges[eid])
            
            # Add edge along with attributes
            kg_graph.add_edge(e1, e2)
            attributes = {eid:{k:v for k,v in edge.items()}}
            nx.set_edge_attributes(kg_graph, attributes)
            edge_attr_count += len(attributes[eid])
    
    
    # Remove any nodes with zero neighbors
    keep_nodes = set([node_id for node_id in kg_graph.nodes() if len(set(kg_graph.neighbors(node_id))) > 0])
    nsubgraph = kg_graph.subgraph(keep_nodes)
    
    print("- Graph created with {} nodes, and {} edges".format(format(nsubgraph.number_of_nodes(), ','),
                                                               format(nsubgraph.number_of_edges(), ',')))
    print("- Dangling edges found {}".format(format(dangling_edges, ',')))
    
    return nsubgraph


def hyper_geom(x, M, n, N):
    """
    x = How many specific objects we want to sample (or more)
    M = How many objects are in the bag
    n = Number of objects matching specification in the bag
    N = How many times we draw from the bag

    https://alexlenail.medium.com/understanding-and-implementing-the-hypergeometric-test-in-python-a7db688a7458
    """

    # Frozen distribution
    rv = scipy.stats.hypergeom(M, n, N)

    # Inverse of the Cumulitive distribution function to get the probability (survival function)
    prob = scipy.stats.hypergeom.sf(x-1, M, n, N)
    return prob


def phen_to_disease_hg_tests(dis_to_hp: dict[str:set], hp_to_dis: dict[str:set], lookup_terms: set, M: int) -> list:
    
    # Preformat lookup terms
    if type(lookup_terms) != type(set()):
        lookup_terms = set(lookup_terms)
    
    # Hyper geometric param
    N = len(lookup_terms)
    
    
    # Pull out only diseases that have a chance of being associated (i.e. minimum overlap of 1 hp term)
    pdis = set()
    for p in lookup_terms:
        if p not in hp_to_dis:
            continue
        pdis = pdis | hp_to_dis[p]
    
    # Loop through smaller subset rather than the whole possible world
    dis_associations = []
    for d in pdis:
        hp_dis = dis_to_hp[d]
        overlap = lookup_terms & hp_dis
        x = len(overlap)
        n = len(hp_dis)
        pval = hyper_geom(x=x, M=M, n=n, N=N)
        dis_associations.append([d, pval, x, M, n, N])
    
    # Sort by lowest pvalue first
    return sorted(dis_associations, key=lambda x: x[1])


@click.command()
@click.option("--input-path",
              "-i",
              required=True,
              type=str,
              help="Input path to directory of .json phenopacket files OR a path to a single .json phenopacket file",
)
@click.option("--output-path",
              "-o",
              required=True,
              type=str,
              help="Output file path to a directory "
)
@click.option("--nodes-path",
              "-n",
              required=True,
              type=str,
              help="Path to monarch-kg_nodes.tsv file"
)
@click.option("--edges-path",
              "-e",
              required=True,
              type=str,
              help="Path to monarch-kg_edges.tsv file")
def get_phenotype_associations(input_path: str, output_path: str, nodes_path: str, edges_path: str):
    """
    This algorithm leverages a subgraph of the monarch knowledge graph + hyper geometric test to find the disease(s) 
    that are most associated with a patients phenotypes. A single .json phenopacket file can be passed in or
    a directory containing multiple .json phenopacket files. The patients observed phenotype terms are pulled
    from the data and the number of terms that overlap for any given disease are counted. The hypergeometric test 
    parameters are as follows:
    
    M = Total number of unique HP terms within the subgraph
    N = How many patient phenotypes (HP) are being input into the test (how many times we sample from the "bag")
    x = How many patient phenotypes (HP) are an exact match to a disease nodes neighboring HP terms
    n = Total number of HP terms neighboring the disease node in question
    
    Note, this is a first pass algorithm. Properly adjusting for the total number of times any given 
    HP term occurs in the graph could alter results along with adding additional information
    """
    
    
    # Initiate the biolink model categories we wish to pull for our nodes and edges
    valid_nodes = set(["biolink:Gene", 
                       "biolink:Disease", 
                       "biolink:PhenotypicFeature"])

    valid_edges = set(["biolink:DiseaseToPhenotypicFeatureAssociation", 
                       "biolink:CausalGeneToDiseaseAssociation"])

    
    # Preformat our input and output paths
    infiles, outfiles = gather_input_output_info(input_path, output_path, results_suffix="_results.tsv")
    
    # Initiate our graph from monarch nodes and edges .tsv files
    nodes = get_entities_from_file(nodes_path, select_data=valid_nodes, match_column='category')
    edges = get_entities_from_file(edges_path, select_data=valid_edges, match_column='category')
    graph = make_graph(nodes, edges)
    
    # Read graph data to get hypergeom testing params and datastructures
    dis_nodes = [n for n in graph.nodes() if graph.nodes[n]['category'] == 'biolink:Disease']
    phen_nodes = [n for n in graph.nodes() if graph.nodes[n]['category'] == 'biolink:PhenotypicFeature']
    
    # Sanity check to ensure only HP (human phenotype) terms have been pulled into the graph
    if len([ppp for ppp in phen_nodes if not ppp.startswith("HP:")]) > 0:
        sys.exit("- ERROR, Non HP terms found in graph associated with diseases. Exiting...")
    
    # Generate disease --> phenotype mapping 
    # Note, graph building process could be skipped by just selecting 
    dis_to_hp = {d:set([nn for nn in list(graph.neighbors(d)) 
                        if graph.nodes[nn]['category'] == "biolink:PhenotypicFeature"]) for d in dis_nodes}
    
    hp_to_dis = {p:set([nn for nn in list(graph.neighbors(p)) 
                    if graph.nodes[nn]['category'] == "biolink:Disease"]) for p in phen_nodes}
    
    # Generate disease --> gene mapping (currently not unused)
    #dis_to_gene = {d:set([graph.nodes[nn]['name'] for nn in list(graph.neighbors(d)) 
    #                    if graph.nodes[nn]['category'] == "biolink:Gene"]) for d in dis_nodes}
    
    
    # Progress statement
    print("- Disease nodes present {}".format(format(len(dis_nodes), ',')))
    print("- Phenotype nodes present {}".format(format(len(phen_nodes), ',')))
    print("- Found {} file(s) to process...".format(format(len(infiles), ',')))
    print("- Preprocessing complete...")
    
    # Hyper geometric param
    M = len(phen_nodes)
    
    # Loop through data and perform hypergeoemtric test against disease hp terms
    processed = 0
    for fname, outname in zip(infiles, outfiles):
        
        # Open phenopacket file and pull relevant information (we want observed phenotypes)
        phenopacket = phenopacket_reader(str(fname))
        phenopacket_util = PhenopacketUtil(phenopacket)
        observed_phenotypes = phenopacket_util.observed_phenotypic_features()
        phenotype_ids = [observed_phenotype.type.id for observed_phenotype in observed_phenotypes]
        
        # Generate sorted list (ranked) set of disease ids based on lowest pvalue
        results = phen_to_disease_hg_tests(dis_to_hp=dis_to_hp,
                                           hp_to_dis=hp_to_dis, 
                                           lookup_terms=set(phenotype_ids),
                                           M=M)

        # Results are originally in form of [[disease_id, pval, x, M, n, N], ...]
        results = np.asarray(results).T
        
        # Convert to dataframe and write data. 
        # TO DO: potentially need to map disease_identifier to something else, and bring in disease_name through sssom file...
        # This will currently output data in a pheval friendly way so that there is no postprocessing necessary EXCEPT for simply
        # copying the files over to the pheval_results directory.
        pd.DataFrame({"rank":np.arange(1, len(results[0])+1),
                      "pvalue":results[1],
                      "disease_name":".",
                      "disease_identifier":results[0]} 
                     ).to_csv(outname, sep='\t', header=True, index=False)
        
        processed += 1
        if processed % 20 == 0:
            print("- Processed {}/{} samples...".format(format(processed, ','), format(len(infiles), ',')))

    
    print("- Successfully processed {}/{} samples".format(format(processed, ','), format(len(infiles), ',')))


main.add_command(get_phenotype_associations, name="rank-associations")


if __name__ == '__main__':
    main()