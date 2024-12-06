
import json
import networkx as nx
import numpy as np
import copy
import re

from .outils_graph import *

class Graph():
    def __init__(self, nextflow_file):
        self.workflow = nextflow_file
        self.full_dico = nextflow_file.get_structure()
        with open(f"{self.get_output_dir()}/graphs/specification_graph.json", 'w') as output_file :
            json.dump(self.full_dico, output_file, indent=4)
        #This dico give for the nodes its sister nodes
        self.link_dico = None
        #Dico to graph without operations
        self.dico_process_dependency_graph = {}
        self.user_view_with_subworkflows = {}
        self.new_nodes_user_view = []
        self.dico_wo_branch_operation = {}

        #Dictionaries for metadata
        #Dico flattened (without any subworkflows)
        self.dico_flattened = {}
        self.initialised = False


    

    def initialise(self, processes_2_remove = []):
        if(not self.is_initialised()):
            def get_node_id(dico, process):
                for node in dico["nodes"]:
                    if(node['name']==process):
                        return node['id']
                for sub in dico['subworkflows']:
                    res = get_node_id(dico['subworkflows'][sub], process)
                    if(res!=-1):
                        return res
                return -1

            #This function removes the process -> by the simpliest way -> it doesn't create new links
            def remove_node(dico, node_id):
                #Remove nodes
                nodes_to_remove = []
                for node in dico["nodes"]:
                    if(node['id']==node_id):
                        nodes_to_remove.append(node)
                for node in nodes_to_remove:
                    dico["nodes"].remove(node)

                #Remove edges
                edges_to_remove = []
                for edge in dico["edges"]:
                    if(edge['A']==node_id):
                        edges_to_remove.append(edge)
                    if(edge['B']==node_id):
                        edges_to_remove.append(edge)
                for edge in edges_to_remove:
                    dico["edges"].remove(edge)

                for sub in dico['subworkflows']:
                    remove_node(dico['subworkflows'][sub], node_id)

            for process in processes_2_remove:
                node_id = get_node_id(self.full_dico, process)
                remove_node(self.full_dico, node_id)


            self.get_dependency_graph()
            self.get_process_dependency_graph()

            
            #self.networkX_wo_operations = self.get_networkx_graph(self.dico_process_dependency_graph, self.networkX_wo_operations)
            self.dico_flattened["nodes"] = []
            self.dico_flattened["edges"] = []
            #This will stay empty -> it's just so we can use the same function
            self.dico_flattened["subworkflows"] = []
            self.initialised = True
    
    def is_initialised(self):
        return self.initialised

    def get_output_dir(self):
        return self.workflow.get_output_dir()  

    #Creates the networkX graph
    def get_networkx_graph(self, graph, networkX, first_call=True):
        if(first_call):
            networkX = nx.MultiDiGraph()
        for node in graph['nodes']:
            #Case node is process
            if(is_process(node['id'])):
                networkX.add_node(node['id'], type='Process', code=node['name'])
            #Case node is operation
            elif(is_operation(node['id'])):
                networkX.add_node(node['id'], type='Operation', code=node['xlabel'])
            elif(node['id']=="source"):
                networkX.add_node("source", type='source', code="source")
            elif(node['id']=="sink"):
                networkX.add_node("sink", type='sink', code="sink")
            else:
                raise Exception("This shoudn't happen!")
        
        for edge in graph['edges']:
            if(is_process(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_process')
            elif(is_process(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_operation')
            elif(is_operation(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_process')
            elif(is_operation(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_operation')
            else:
                networkX.add_edge(edge['A'], edge['B'], label = "", edge_type='')      
        for subworkflow in graph['subworkflows']:
            networkX = self.get_networkx_graph(graph['subworkflows'][subworkflow], networkX, first_call=False)
        return networkX



    #Method that initalisise the link dico
    def intia_link_dico(self):
        if(self.link_dico==None):
            self.link_dico = initia_link_dico_rec(self.full_dico)

    def get_specification_graph(self, filename = "specification_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.full_dico, render_graphs = render_graphs)

    def get_specification_graph_wo_labels(self, filename = "specification_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.full_dico, label_edge=False, label_node=False, render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations(self, filename = "specification_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations_wo_labels(self, filename = "specification_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), label_edge=False, label_node=False, render_graphs = render_graphs)

    def get_process_dependency_graph_dico(self):
        return self.dico_process_dependency_graph

    def get_process_dependency_graph(self):
        self.intia_link_dico()

        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico_process_dependency_graphs(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(is_process(node['id'])):
                    dico['nodes'].append(node)
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico_process_dependency_graphs(dico_struct['subworkflows'][sub])
            return dico

        dico = replicate_dico_process_dependency_graphs(self.full_dico)

        #This is a dictionnary which links every node to it's connected process
        node_2_processes = copy.deepcopy(self.link_dico)
        already_searched = {}
        for node in node_2_processes:
            already_searched[node] = [node]
        changed = True
        while(changed):
            changed = False
            for node in node_2_processes:
                temp = node_2_processes[node].copy()
                for give in node_2_processes[node]:
                    if(is_operation(give)):
                        temp.remove(give)
                        if(node!=give and give not in already_searched[node]):
                            already_searched[node] += give
                            temp_temp = node_2_processes[give]
                            for node_temp in already_searched[node]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_processes[node] = list(set(temp))

 
        links_added = []
        def add_edges(dico):
            for node in dico['nodes']:
                edges = node_2_processes[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    if(link not in links_added):
                        dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                        links_added.append(link)   
            for sub in dico['subworkflows']:
                add_edges(dico["subworkflows"][sub]) 
            
        
        add_edges(dico)


        self.dico_process_dependency_graph = dico

        with open(f"{self.get_output_dir()}/graphs/process_dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_process_dependency_graph, output_file, indent=4)

    
    def render_graph_wo_operations(self, filename = "process_dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_process_dependency_graph, render_graphs = render_graphs, label_edge=False, label_node=False)
    

    def get_dependency_graph(self):
        self.intia_link_dico()
        nodes_in_graph = []
        branch_operation_ids = []
        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(get_type_node(node)!="Branch Operation"):
                    dico['nodes'].append(node)
                    nodes_in_graph.append(node['id'])
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico(dico_struct['subworkflows'][sub])
            return dico
        
        dico = replicate_dico(self.full_dico)

        #This is a dictionnary which links every node to it's connected process
        node_2_none_branch = copy.deepcopy(self.link_dico)
        already_searched = {}
        for node in node_2_none_branch:
            already_searched[node] = [node]
        changed = True
        while(changed):
            changed = False
            for node in node_2_none_branch:
                temp = node_2_none_branch[node].copy()
                for give in node_2_none_branch[node]:
                    if(is_operation(give) and give not in nodes_in_graph):
                        temp.remove(give)
                        if(node!=give and give not in already_searched[node]):
                            already_searched[node] += give
                            temp_temp = node_2_none_branch[give]
                            for node_temp in already_searched[node]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_none_branch[node] = list(set(temp))

 
        links_added = []
        def add_edges(dico):
            for node in dico['nodes']:
                edges = node_2_none_branch[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    if(link not in links_added):
                        dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                        links_added.append(link)   
            for sub in dico['subworkflows']:
                add_edges(dico["subworkflows"][sub]) 
            
        add_edges(dico)
        self.dico_wo_branch_operation = dico

        with open(f"{self.get_output_dir()}/graphs/dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_wo_branch_operation, output_file, indent=4)
    

    def render_dependency_graph(self, filename = "dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, render_graphs = render_graphs)
    
    def get_dependency_graph_wo_labels(self, filename = "dependency_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, label_edge=False, label_node=False, render_graphs = render_graphs)

    def get_dependency_graph_wo_orphan_operations(self, filename = "dependency_graph_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), render_graphs = render_graphs)
    
    def get_dependency_graph_wo_orphan_operations_wo_labels(self, filename = "dependency_graph_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), label_edge=False, label_node=False, render_graphs = render_graphs)


    #============================
    #GENERATE USER VIEW
    #============================

    def get_user_view_graph(self, relevant_processes = []):
        #For now i'm only gonna work from the flattened dico
        self.initialise_flattened_dico(self.dico_process_dependency_graph)
        #self.initialise_flattened_dico(self.full_dico)
        dico = self.dico_flattened

        user_view, self.new_nodes_user_view = relev_user_view_builder(dico, relevant_modules=relevant_processes)
        
        with open(self.get_output_dir()/ "graphs/user_view.json", 'w') as output_file :
            json.dump(user_view, output_file, indent=4)
        

        user_view_with_subworkflows = add_subworkflows_2_dico(self.dico_process_dependency_graph, user_view)
        with open(self.get_output_dir()/ "graphs/user_view_with_subworkflows.json", 'w') as output_file :
            json.dump(user_view_with_subworkflows, output_file, indent=4)

        return user_view, user_view_with_subworkflows
    
    def generate_user_view(self, relevant_processes = [], render_graphs = True):
        user_view, user_view_with_subworkflows = self.get_user_view_graph(relevant_processes = relevant_processes)
        self.user_view_with_subworkflows = user_view_with_subworkflows
        generate_graph(self.get_output_dir()/'graphs'/"user_view", user_view, label_edge=True, label_node=True, render_graphs = render_graphs, root = False, relevant_nodes = copy.deepcopy(relevant_processes))
        generate_graph(self.get_output_dir()/'graphs'/"user_view_with_subworkflows", user_view_with_subworkflows, label_edge=True, label_node=True, render_graphs = render_graphs, root = False, relevant_nodes = copy.deepcopy(relevant_processes))

    #============================
    #GENERATE LEVEL GRAPHS
    #============================
    def generate_level_graphs(self, render_graphs = True, label_edge=True, label_node=True):
        dico = self.dico_process_dependency_graph
        #dico = self.full_dico
        max_level = get_max_level(dico)
        for l in range(max_level+1):
            new_dico = get_graph_level_l(dico, l)
            #print(new_dico)
            generate_graph(self.get_output_dir()/'graphs'/f"level_{l}", new_dico, label_edge=label_edge, label_node=label_node, render_graphs = render_graphs)
            
    #============================
    #GET NUMBER OF SUBWORKFLOWS
    #============================

    def get_number_subworkflows_process_dependency_graph(self):
        return get_number_of_subworkflows(self.dico_process_dependency_graph)
    
    def get_number_subworkflows_user_view(self):
        return get_number_of_subworkflows(self.user_view_with_subworkflows )
        
    #============================
    #GET node_2_subworkflows
    #============================
    def node_2_subworkflows_process_dependency_graph(self):
        node_2_subworkflows = {}
        fill_node_2_subworkflows(self.dico_process_dependency_graph, node_2_subworkflows)
        return node_2_subworkflows
    
    #This methods returns the nodes to subworkflow dico but for the OG processes
    def node_2_subworkflows_user_view(self):
        node_2_subworkflows = {}
        fill_node_2_subworkflows(self.user_view_with_subworkflows, node_2_subworkflows)
        new_node_2_subworkflows = {}
        for group in self.new_nodes_user_view:
            for node in group:
                for id in node_2_subworkflows: 
                    if(node.replace('<', '').replace('>', '') in id):
                        new_node_2_subworkflows[node] = node_2_subworkflows[id]
        return new_node_2_subworkflows 

    #==========================================================
    #Check if fake dependency is created when created user view
    #==========================================================
    #Here to check if a fake dependency is created, I'm gonna compare the edges 
    #of the level graphs between the user view and the process dependency 
    #Each of the user view edges (with subworkflo) should be in the process dependency edges
    def check_fake_dependency_user_view(self):
        #This function removes the "<>" from the node name
        #And the same for the subworkflows
        def clean_node(node):
            #Case the node is a process
            if(node[0]=="<"):
                #We just remove the '<>' around the name
                node = node[1:-1]
            else:#it's a subworkflow
                for match in re.finditer(r"id_\d+\.\d+\_(.+)", node):
                    node = match.group(1)
            return node

        #First by checking if the node_2_subworkflows are the same, if it's the case i don't need to compare
        if(self.node_2_subworkflows_process_dependency_graph!=self.node_2_subworkflows_user_view):
            dico_process_dependency_graph = self.dico_process_dependency_graph
            user_view_with_subworkflows = self.user_view_with_subworkflows
            user_view_subworkflows = get_subworkflows_names(user_view_with_subworkflows)
            #Get the level workflows for the process dependency graph
            max_level = get_max_level(dico_process_dependency_graph)
            dependency_levels = []
            for l in range(max_level+1):
                new_dico = get_graph_level_l(dico_process_dependency_graph, l)
                dependency_levels.append(new_dico)
            #Get the level workflows for the user view
            max_level = get_max_level(user_view_with_subworkflows)
            user_view_levels = []
            for l in range(max_level+1):
                new_dico = get_graph_level_l(user_view_with_subworkflows, l)
                user_view_levels.append(new_dico)
            #For each level, i'm gonna check the edges
            for i in range(len(user_view_levels)):
                user_view_level = user_view_levels[i]
                dependency_level = dependency_levels[i]
                for sub in user_view_subworkflows:
                    for edge_user in user_view_level["edges"]:
                        if(f"_{sub}" in edge_user["A"] or f"_{sub}" in edge_user["B"]):
                            if(edge_user["A"]!="input" and edge_user["A"]!="output" and edge_user["B"]!="input" and edge_user["B"]!="output"):
                                #This boolean if is to check if the edge 'edge_user' has equivalence in the process dependency graph
                                has_matching_user_dependency = False
                                
                                for edge_process in get_edges(dependency_level):
                                    if(f"_{sub}" in edge_process["A"] or f"_{sub}" in edge_process["B"]):
                                        node = ""
                                        side = ""
                                        #Determine if it's A or B
                                        if(f"_{sub}" in edge_process["A"]):
                                            node = edge_process["B"]
                                            side = "B"
                                        if(f"_{sub}" in edge_process["B"]):
                                            node = edge_process["A"]
                                            side = "A"
                                        node = clean_node(node)
                                        if(node in edge_user[side]):
                                            has_matching_user_dependency = True
                                        
                                if(not has_matching_user_dependency):
                                    #Check if there is an indirect path that exist
                                    node_A = clean_node(edge_user["A"])
                                    node_B = clean_node(edge_user["B"])
                                    nodes_level = get_nodes_from_edges(get_edges(dependency_level))
                                    node_A_temp, node_B_temp = "", ""
                                    for A in node_A.split("_$$_"):
                                        for tmp in nodes_level:
                                            if A in tmp:
                                                node_A_temp = tmp
                                    for B in node_B.split("_$$_"):
                                        for tmp in nodes_level:
                                            if B in tmp:
                                                node_B_temp = tmp
        
                                    if(not exist_path_dico(node_A_temp, node_B_temp, dependency_level)):
                                        print("False dependency", edge_user)
                                        return True     
                                

            
            return False
        else:
            return False

    #============================
    #METADATA FROM GRAPH
    #============================

    def initialise_flattened_dico(self, dico):
        self.dico_flattened = {}
        self.dico_flattened["nodes"] = []
        self.dico_flattened["edges"] = []
        #This will stay empty -> it's just so we can use the same function
        self.dico_flattened["subworkflows"] = []
        flatten_dico(dico, self.dico_flattened)
        #for node in dico["nodes"]:
        #    self.dico_flattened["nodes"].append(node)
        #for edge in dico["edges"]:
        #    self.dico_flattened["edges"].append(edge)
        #for subworkflow in dico["subworkflows"]:
        #    self.initialise_flattened_dico(dico["subworkflows"][subworkflow])

    def get_metadata(self, graph):
        G = self.get_networkx_graph(graph, None)
        dico = {}
        for node in G.nodes(data=True):
            if(node[1]=={}):
                print(node)
        process_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Process']
        operation_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Operation']

        dico['number_of_processes'] =  len(process_nodes)
        dico['number_of_operations'] =  len(operation_nodes)
        dico['number_of_nodes'] = dico['number_of_processes']+dico['number_of_operations']

        dico['number_of_edges_process_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_process")
        dico['number_of_edges_process_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_operation")
        dico['number_of_edges_operation_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_process")
        dico['number_of_edges_operation_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_operation")
        
        dico['number_of_edges_source_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation']
        dico['number_of_edges_source_operation'] = dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges_sink_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_operation_2_process']
        dico['number_of_edges_sink_operation'] = dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        
        dico["number_of_simple_loops"] = nx.number_of_selfloops(G)

        distribution_in_degrees_for_processes = list(dict(G.in_degree(process_nodes)).values())
        distribution_out_degrees_for_processes = list(dict(G.out_degree(process_nodes)).values())
        distribution_in_degrees_for_operations= list(dict(G.in_degree(operation_nodes)).values())
        distribution_out_degrees_for_operations= list(dict(G.out_degree(operation_nodes)).values())

        dico["distribution_in_degrees_for_processes"] = distribution_in_degrees_for_processes
        dico["distribution_out_degrees_for_processes"] = distribution_out_degrees_for_processes
        dico["distribution_in_degrees_for_operations"] = distribution_in_degrees_for_operations
        dico["distribution_out_degrees_for_operations"] = distribution_out_degrees_for_operations

        dico["distribution_in_degrees_for_all"] = dico["distribution_in_degrees_for_processes"]+dico["distribution_in_degrees_for_operations"]
        dico["distribution_out_degrees_for_all"] = dico["distribution_out_degrees_for_processes"]+dico["distribution_out_degrees_for_operations"]

        dico["average_in_degrees_for_processes"]   = np.array(distribution_in_degrees_for_processes).mean()
        dico["average_out_degrees_for_processes"]  = np.array(distribution_out_degrees_for_processes).mean()
        dico["average_in_degrees_for_operations"]  = np.array(distribution_in_degrees_for_operations).mean()
        dico["average_out_degrees_for_operations"] = np.array(distribution_out_degrees_for_operations).mean()
        dico["average_in_degrees_for_all"] = np.array(dico["distribution_in_degrees_for_all"] ).mean()
        dico["average_out_degrees_for_all"] = np.array(dico["distribution_out_degrees_for_all"] ).mean()


        dico["median_in_degrees_for_processes"]   = np.median(np.array(distribution_in_degrees_for_processes))
        dico["median_out_degrees_for_processes"]  = np.median(np.array(distribution_out_degrees_for_processes))
        dico["median_in_degrees_for_operations"]  = np.median(np.array(distribution_in_degrees_for_operations))
        dico["median_out_degrees_for_operations"] = np.median(np.array(distribution_out_degrees_for_operations))
        dico["median_in_degrees_for_all"] =  np.median(np.array(dico["distribution_in_degrees_for_all"]))
        dico["median_out_degrees_for_all"] = np.median(np.array(dico["distribution_out_degrees_for_all"]))

        #DEsnity = m/n(n-1), where n is the number of nodes and m is the number of edges
        dico['density'] = nx.density(G)
        weakly_connected_components = list(nx.weakly_connected_components(G))
        dico['number_of_weakly_connected_components'] = len(weakly_connected_components)
        
        components_with_over_2_nodes = [comp for comp in weakly_connected_components if len(comp) >= 2]
        dico['number_of_weakly_connected_components_with_2_or_more_nodes'] = len(components_with_over_2_nodes)

        #Getting the number of cycles
        self.initialise_flattened_dico(graph)
        links_flattened = initia_link_dico_rec(self.dico_flattened)
        not_source_2_sink = []
        node_2_sink = []
        for node in links_flattened:
            if(links_flattened[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink = links_flattened.copy()
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")
 
        #The simple loops are included in this
        dico['number_of_cycles'], edges_create_cycles = get_number_cycles(links_flattened_source_sink)
        
        #Remove the edges which create the cycles
        #Since the number of paths from Source 2 sink and the longest path depend on the 
        #Topological ordering 
        #A topological ordering is possible if and only if the graph has no directed cycles, that is, if it is a directed acyclic graph (DAG)
        #We turn the CDG (cyclic directed graphs) into a DAG (directed acyclic graph)
        for A, B in edges_create_cycles:
            links_flattened_source_sink[A].remove(B)


        #Here we need to update the sink source since some edges have been removed
        #See phyloplace worklfow (all nodes have an output channel) -> none connected to sink
        #TODO clean this cause it's just a copy of what is above
        not_source_2_sink = []
        node_2_sink = []
        for node in links_flattened:
            if(links_flattened_source_sink[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened_source_sink[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")    
        

        structure_type = ""
        if(len(edges_create_cycles)==0):
            structure_type = "DAG"
        else:
            structure_type = "CDG"
        
        dico['structure_type'] = structure_type

        dico['number_of_paths_source_2_sink'] = get_number_paths_source_2_sink(links_flattened_source_sink)
        dico['shortest_path'] = dijkstra(links_flattened_source_sink)
        dico['longest_path'] = get_longest_distance(links_flattened_source_sink)

        
        """#Check that the values calculated are the same than what gives networkX
        dico_check = {}
        dico_check['nodes'] = []
        dico_check['edges'] = []
        dico_check['subworkflows'] = {}
        for node in links_flattened_source_sink:
            dico_check["nodes"].append({'id':node, 'xlabel':"", 'name':""})
            for B in links_flattened_source_sink[node]:
                dico_check["edges"].append({'A':node, "B":B, "label":""})

        G_DAG = self.get_networkx_graph(dico_check, None)
        #=====================================
        #ADDING SINK AND SOURCE TO THE GRAPH
        #=====================================
        source_node = "source"
        sink_node = "sink"
        
        if(dico['shortest_path']!=nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)):
            raise Exception(f"{dico['shortest_path']}, {nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)}")
        #print("test1")
        if(dico['longest_path']+1!=len(nx.dag_longest_path(G_DAG))):
            raise Exception(f"{dico['longest_path']}, {len(nx.dag_longest_path(G_DAG))}")
        #print("test2")
        
        #if(len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))!=dico['number_of_paths_source_2_sink']):
        #    raise Exception(f"{len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))}, {dico['number_of_paths_source_2_sink']}")
        #print("test3")"""
        
        return dico


    def get_metadata_specification_graph(self):
        
        dico = self.get_metadata(self.full_dico)
        with open(self.get_output_dir()/ "graphs/metadata_specification_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_dependency_graph(self):

        dico = self.get_metadata(self.dico_wo_branch_operation)
        with open(self.get_output_dir()/ "graphs/metadata_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_process_dependency_graph(self):
        
        dico = self.get_metadata(self.dico_process_dependency_graph)
        with open(self.get_output_dir()/ "graphs/metadata_process_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_user_view(self):
        dico = self.get_metadata(self.user_view_with_subworkflows )
        with open(self.get_output_dir()/ "graphs/metadata_user_view.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    #def get_metadata_graph_wo_operations(self):
    #    G = self.networkX_wo_operations
    #    dico = self.get_metadata(G)
    #    with open(self.get_output_dir() / "graphs/metadata_graph_wo_operations.json", 'w') as output_file :
    #        json.dump(dico, output_file, indent=4)
