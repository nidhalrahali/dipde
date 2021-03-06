import neuroml as nml
import warnings
from neuroml.utils import validate_neuroml2

def neuroml_internal_population_parameter_dict_adapter(p):
    
    param_dict = p.to_dict()
    
    new_param_dict = {}
    new_param_dict['leak_reversal'] = '%smV' % (param_dict.pop('reversal_potential', 0.)*1000,)
    
    return new_param_dict

def network_to_neuroml(network, output_file_name, **kwargs):
    
    # Unpack neuroml extras from kwargs:
    doc_id = kwargs.get('doc_id', 'default_dipde_network')
    
    # Create neuroml doc:
    nml_doc = nml.NeuroMLDocument(id=doc_id)
    print(nml_doc)
    
    validate_neuroml2(nml_doc)
    
    # Append types:
#     nml_doc.iaf_cells.append(nml.IafCell0)
    
    population_type_list = {}
    for p in network.population_list:
        curr_population_name = p.__class__.__name__
        if curr_population_name == 'InternalPopulation':
            output = neuroml_internal_population_parameter_dict_adapter(p)
        elif curr_population_name == 'ExternalPopulation':
            pass
#             print neuroml_external_population_parameter_dict_adapter(p)
        else:
            raise Exception('Population Type (%s) not recognize when converting to NeuroML' % curr_population_name)


if __name__ == "__main__":
    
    warnings.warn('NeuroML adapter is in prototype stage and not debugged.')
    
    from dipde.examples.singlepop import get_network
    
    network = get_network(tol=1e-14)
    
    network_to_neuroml(network, 'temp.net.nml')
    