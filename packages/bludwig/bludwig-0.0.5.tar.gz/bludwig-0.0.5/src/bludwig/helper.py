import importlib, yaml, pkg_resources, os, warnings
import torch 
import bpyth as bpy
import pandas as pd
import pandasklar as pak

    
#############################################################################################################
###
### Helper for Ludwig
###
#############################################################################################################    


def gpu_info():
    # GPU und CUDA
    if torch.cuda.is_available():
        print('CUDA is available on ' + torch.cuda.get_device_name(torch.cuda.current_device()))
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.cuda.empty_cache() # Cache leeren
        print('max_memory_allocated: {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_allocated(device=device)) )  )
        print('max_memory_reserved:  {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_reserved( device=device)) )  )  

    else:
        print('no CUDA!')    



def entwirre_test_stat(test_stats):
    result = []
    for config_no, test_stat in enumerate(test_stats):
        print(config_no)
        for output_feature_name, stat in test_stat.items():
            if output_feature_name == 'combined':
                continue
            for key, value in stat.items():
                if isinstance(value, (int, float)):
                    result += [[config_no, key, bpy.human_readable_number(value,3) ]]    
                    
    result = pak.dataframe(result)
    result.columns = ['config_no','name','value']
    return result




def prepare_train_log(train_log_raw, size='small'):

    result = pd.pivot_table( train_log_raw, 
                              index='name',
                              columns='config_no',
                              values='value', 
                              aggfunc='first')
    result = pak.drop_multiindex(result).reset_index() 
    
    # Namen korrigieren
    mask = result.name.str.startswith('average')
    result.loc[mask,'name'] = result[mask].name.str.replace('average_','') + '_avg'   

    # validation_metric ganz nach vorne
    mask = result.name == 'validation_metric'
    zeilen_ganzvorne = list(set(result[mask].iloc[0]))    
    #print(zeilen_ganzvorne)


    # Zeilen sortieren
    if size == 'small':
        zeilen_vorne =  ['accuracy','recall','specificity','precision','roc_auc','loss',]
        zeilen_hinten = ['epochs','time/epoch','train_time',]    
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )
        result = pak.move_cols( result, zeilen_ganzvorne )        
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()

        # Zeilen löschen
        zeilen_verboten = ['validation_metric']
        zeilen_erlaubt = [z for z in (zeilen_ganzvorne + zeilen_vorne + zeilen_hinten) if not z in zeilen_verboten ]
        mask = result.name.isin( zeilen_erlaubt )
        result = result[mask]
        
    else: # size == 'big'
        result = result.sort_values('name')
        zeilen_vorne =  ['validation_metric',]
        zeilen_hinten = ['experiment_path','output_feature_type','output_feature_name','epochs','train_secs','time/epoch','train_time',]     
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )         
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()        

    result = pak.reset_index(result)
    result.columns = [c if isinstance(c,str) else 'model_' + str(c) for c in result.columns ]
    return result



def list_datasets():

    datasets = [
#                                                       
#        dataset_name                    input_field_types   output_field_type    
#                                    size                                  note
        ['adult_census_income',      4,  'category, number', 'binary',     'many category fields'], 
        ['agnews',                   5,  'text',             'category',   ''   ],
        ['amazon_review_polarity',   6,  'text',             'binary',     '',  ],
        ['amazon_reviews',           6,  'text',             'category',   '',  ],
        ['dbpedia',                  5,  'text',             'category',   '',  ],
        ['electricity',              4,  'number',           'number',     '',  ],
        ['ethos_binary',             2,  'text',             'binary',     '',  ],
        ['flickr8k',                 3,  'image',            'text',       '',  ],
        ['goemotions',               4,  'text',             'category',   '',  ],
        ['irony',                    3,  'text',             'binary',     '',  ],
        ['mnist',                    4,  'image',            'category',   'Hello world',  ],
        ['mushroom_edibility',       3,  'category',         'binary',     '',  ],
        ['poker_hand',               6,  'category',         'category',   '',  ],
        ['sarcos',                   4,  'number',           'number',     '',  ],
        ['sst2',                     3,  'text',             'binary',     '',  ],
        ['sst3',                     4,  'text',             'category',   '',  ],        
        ['sst4',                     4,  'text',             'category',   '',  ],       
        ['yahoo_answers',            6,  'text',             'category',   '',  ],
        ['yelp_review_polarity',     5,  'text',             'binary',     '',  ],
        ['yelp_reviews',             5,  'text',             'category',   '',  ],
        ['yosemite',                 4,  'time',             'number',     '',  ],
        ['ae_price_prediction',      4,  'category',         'number',     '',  ],     
        ['bookprice_prediction',     3,  'text,category',    'number',     '',  ],    


        
        ]
    result = pak.dataframe(datasets)
    result.columns = ['dataset_name','size','input_field_types','output_field_type','note',]
    return result



def load_dataset(dataset_name, verbose=True):
    '''
    Loads a dataset from Ludwig's dataset zoo. 
    * dataset_name: Name of the dataset. Valid names are listed by list_datasets().
    Returns a DataFrame with training data and a ludwig.dataset_loader.
    '''
    module         = importlib.import_module('ludwig.datasets')
    dataset_loader = getattr(module, dataset_name)
    data_df       = dataset_loader.load(split=False)
        
    #katalog = list_datasets()
    #mask = katalog.dataset_name == dataset_name
    #katalogeintrag = katalog[mask].iloc[0]

    output_feature_names = [col['name'] for col in dataset_loader.config.output_features]   
    if dataset_name == 'agnews':
        output_feature_names = ['class']
    data_df = pak.move_cols(data_df, output_feature_names)     
    data_df = pak.move_cols(data_df, 'split',-1) 
    data_df = pak.drop_cols(data_df,['Unnamed: 0','Unnamed: 1'])
    data_df = pak.change_datatype(data_df)

    if verbose:
        print()
        print(dataset_loader.description())    
        print('output_features:', dataset_loader.config.output_features)  
        
    return data_df, dataset_loader



def analyse_cols(data_df, dataset_loader=None, output_features_size=1):
    '''
    Analyses training data. 
    The information whether a column is input_feature or output_feature comes either from
    * dataset_loader (provided by load_dataset), or from
    * output_features_size (then it is the first n columns of the DataFrame).
    If a dataset_loader is provided, output_features_type is taken from config. Otherwise it's guessed.
    '''

    # analyse_cols
    spalten = ['col_name', 'datatype_short', 'datatype_identified','mem_usage','nunique', 'ndups', 'vmin', 'vmax','n']
    
    analyse = pak.analyse_cols(  pak.sample(data_df, 10000), human_readable=False  )[spalten].iloc[1:]
    mask = analyse.col_name == 'split'
    analyse = pak.drop_rows(analyse,mask)
    analyse['is_output_feature'] = False
    analyse['feature_type'] = ''
    analyse = pak.move_cols(analyse,['is_output_feature','feature_type'],'col_name')
    analyse = pak.reset_index(analyse)

    # is_output_feature
    if dataset_loader is not None:
        output_feature_names = [col['name'] for col in dataset_loader.config.output_features]    
    else:
        output_feature_names = list(data_df.columns)[:output_features_size]
    mask = analyse.col_name.isin(output_feature_names)
    analyse.loc[mask,'is_output_feature'] = True

    # binary feature_type
    mask = analyse['nunique'] == 2
    analyse.loc[mask,'feature_type'] = 'binary'

    # category from number feature_type
    mask0 = analyse['datatype_identified'].isin(['int','float'])    
    mask1 = analyse['nunique'] / analyse['ndups'] < 0.05
    mask2 = analyse['nunique'] <= 30    
    mask3 = analyse.feature_type == ''
    mask = mask0  &  mask1  &  mask2  &  mask3
    analyse.loc[mask,'feature_type'] = 'category'

    # category from text feature_type
    mask0 = analyse['datatype_identified'].isin(['string']) 
    mask1 = analyse['nunique'] / analyse['ndups'] < 0.1
    mask2 = analyse['nunique'] <= 50    
    mask3 = analyse.feature_type == ''
    mask = mask0  &  mask1  &  mask2  &  mask3
    analyse.loc[mask,'feature_type'] = 'category'    

    # numeric feature_type
    mask1 = analyse['datatype_identified'].isin(['int','float'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'number'

    # text feature_type
    mask1 = analyse['datatype_identified'].isin(['string'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'text'

    
    # image feature_type  
    try:
        mask1 = analyse['feature_type'] == 'text'
        mask2 = analyse['vmin'].str.endswith(('jpg','png'))
        mask = mask1 & mask2
        analyse.loc[mask,'feature_type'] = 'image'
    except:
        pass

    # date feature_type  
    mask1 = analyse['datatype_identified'].isin(['datetime'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'date'

    # sequence feature_type  
    mask1 = analyse['datatype_identified'].isin(['list'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'sequence'    

    # feature_type_guess
    #analyse['feature_type_guess'] = analyse.feature_type.copy()
    #analyse = pak.move_cols(analyse, 'feature_type_guess', 'feature_type')
    
    # überschreibe feature_type_real
    if dataset_loader is not None:
        output_features_real = pak.dataframe(dataset_loader.config.output_features)
        analyse = pak.update_col(analyse, output_features_real, left_on='col_name', right_on='name', col='type', col_rename='feature_type')    
    
    return analyse 





def config0(data_df, dataset_loader=None, output_features_size=1, use_yaml=True):
    '''
    Creates a default config for a given DataFrame. To identify the output_features, use
    * dataset_loader or 
    * output_features_size as in analyse_cols().
    '''
    analyse = analyse_cols(data_df, dataset_loader, output_features_size)
    mask = analyse.is_output_feature
    output_features_size = analyse[mask].shape[0]
    
    # input_features
    spalten = ['col_name','feature_type']
    input_features = analyse[output_features_size:][spalten]
    input_features.columns = ['name','type']
    input_features = input_features.to_dict(orient='records')  

    # output_features
    output_features = analyse[:output_features_size][spalten]
    output_features.columns = ['name','type']
    output_features = output_features.to_dict(orient='records')

    # config
    config = {'input_features':  input_features,
              'output_features': output_features }

    if use_yaml:
        return yaml.dump(config)
    return config



def config1(dataset_loader, use_yaml=True):
    '''
    Wrapper for default_model_config from dataset_loader
    '''
    result = dataset_loader.default_model_config

    if use_yaml:
        result = yaml.dump(result)
        result = result.replace( 'null\n...\n', '' )
        
    return result    



def get_datasets(remove_failed=True):
    '''
    List all datasets available in Ludwig.
    '''
    library_location = pkg_resources.get_distribution('ludwig').location
    directory_within_library = 'ludwig/datasets/configs'
    directory_path = os.path.join(library_location, directory_within_library)
    file_list = os.listdir(directory_path)
    
    elements_to_remove = ['__pycache__','__init__.py']
    result = [x.replace('.yaml','') for x in file_list if x not in elements_to_remove]
    result = sorted(result)

    if not remove_failed:
        return result

    failed =    ['allstate_claims_severity',
                 'amazon_employee_access_challenge',
                 'ames_housing',
                 'bbcnews',
                 'bnp_claims_management',
                 'connect4',
                 'creditcard_fraud',
                 'customer_churn_prediction',
                 'higgs',
                 'ieee_fraud',
                 'imbalanced_insurance',
                 'imdb',
                 'insurance_lite',
                 'jigsaw_unintended_bias100k',
                 'mercedes_benz_greener',
                 'noshow_appointments',
                 'numerai28pt6',
                 'ohsumed_7400',
                 'otto_group_product',
                 'porto_seguro_safe_driver',
                 'reuters_r8',
                 'rossman_store_sales',
                 'santander_customer_satisfaction',
                 'santander_customer_transaction',
                 'santander_value_prediction',
                 'sarcastic_headlines',
                 'synthetic_fraud',
                 'talkingdata_adtrack_fraud',
                 'telco_customer_churn',
                 'temperature',
                 'titanic',
                 'twitter_bots',
                 'walmart_recruiting',
                 'wmt15',
                 'fever',
                 'forest_cover',
                 'google_quest_qa',
                 'imdb_genre_prediction',
                 'kdd_appetency',
                 'kdd_churn',
                 'kdd_upselling']    

    result = [x for x in result if x not in failed]
    return result





def scan_datasets(dataset_names, get_elements_to_remove=False):
    '''
    Scan and analyse Ludwig's database zoo. 
    '''
    result = []
    for dataset in dataset_names:
        
        # load_dataset
        print('loading',dataset)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")            
                data_df, dataset_loader = load_dataset(dataset, verbose=False)  
        except:
            elements_to_remove += [dataset]

        # analysieren 
        analyse = analyse_cols(data_df, dataset_loader) 
        mask = analyse.is_output_feature
        output_features_size = analyse[mask].shape[0]        

        # output_features and input_features 
        spalten = ['col_name','feature_type','mem_usage']
        output_features = analyse[:output_features_size][spalten]           
        input_features = analyse[output_features_size:][spalten]        

        # Ausgabewerte berechnen
        input_features_type  = ', '.join(pak.group_and_agg( input_features,  ['feature_type','mem_usage'], ['','sum']).sort_values('mem_usage_sum', ascending=False).feature_type)
        output_features_type = ', '.join(pak.group_and_agg( output_features, ['feature_type','mem_usage'], ['','sum']).sort_values('mem_usage_sum', ascending=False).feature_type)        
        config1 = yaml.dump(dataset_loader.default_model_config)
        config1 = config1.replace('null\n...\n','')

        # Ausgabe
        result += [{'dataset_name': dataset, 
                    'rows': bpy.human_readable_number(data_df.shape[0]) ,
                    'in_size'  : input_features.shape[0],                        
                    'out_size' : output_features.shape[0],

                    'in_name'  : ', '.join(input_features.col_name),                    
                    'out_name' : ', '.join(output_features.col_name),                    

                    'in_type'  : input_features_type,  # ', '.join(input_features.feature_type),                      
                    'out_type' : output_features_type, # ', '.join(output_features.feature_type),                    
                                 
                    'description': dataset_loader.description(),
                    'config1': config1(dataset_loader),

                   }]
    

    result = pak.dataframe(result) 

    if get_elements_to_remove:
        return result, elements_to_remove
    return result











