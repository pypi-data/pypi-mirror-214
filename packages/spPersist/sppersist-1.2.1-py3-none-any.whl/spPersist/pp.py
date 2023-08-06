import cell2location
import scanpy as sc
import pandas as pd
import os

def quality_control_metrics(adata):
  '''
  quality_control_metrics takes an annotated data object adata
  produced in the data processing module and performs 
  quality control calculation as recommended in Scanpy
  preprocessing tutorials.
  '''

  sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)


def quality_control(adata):
  '''
  quality_control takes an annotated data object adata,
  prompts the user to enter quality control parameters,
  and filters the expression matrix.
  '''
  
  # setting scanpy verbosity for filtering notice
  sc.settings.verbosity = 3

  print('Filtering cells...\nPress Enter to skip a parameter.')
  p = input('Enter min_counts:')
  print('min_counts: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_cells(adata, min_counts=p)
  
  p = input('Enter min_genes:')
  print('min_genes: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_cells(adata, min_genes=p)
  
  p = input('Enter max_counts:')
  print('max_counts: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_cells(adata, max_counts=p)

  p = input('Enter max_genes:')
  print('max_genes: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_cells(adata, max_genes=p)

  print('Filtering genes...\nPress Enter to skip a parameter.')
  p = input('Enter min_counts:')
  print('min_counts: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_genes(adata, min_counts=p)

  p = input('Enter min_cells:')
  print('min_cells: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_genes(adata, min_counts=p)

  p = input('Enter max_counts:')
  print('max_counts: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_genes(adata, max_counts=p)

  p = input('Enter max_cells:')
  print('max_cells: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    sc.pp.filter_genes(adata, max_cells=p)

  print('Mitochondrial filtering...\nPress Enter to skip the parameter.')
  p = input('Enter min_pct_counts_mt:')
  print('min_pct_counts_mt: ' + p)
  try:
    int(p)
  except:
    p = None
    print('Empty entry or the parameter is invalid.')
  else:
    p = int(p)
    adata = adata[adata.obs["pct_counts_mt"] < p]
    print(f"#cells after MT filter: {adata.n_obs}")


def extract_mouse_brain_reference():
  '''
  extract_mouse_brain_reference returns the median gene expression by
  cluster, as a pandas dataframe, from the Yao Z et al.
  '''

  url = 'https://idk-etl-prod-download-bucket.s3.amazonaws.com/aibs_mouse_ctx-hpf_10x/medians.csv'
  filename = 'medians.csv'
  os.system('wget '+url)
  df = pd.read_csv(filename,index_col='feature')

  return df


def extract_reference_data(adata_ref):
  '''
  extract_reference_data takes a single-cell reference data adata_ref
  as annotated data object, and returns the estimated reference expression
  as a pandas dataframe.
  '''

  # prepare anndata for the regression model
  cell2location.models.RegressionModel.setup_anndata(adata=adata_ref)
  
  from cell2location.models import RegressionModel
  mod = RegressionModel(adata_ref) 

  mod.train(max_epochs=250, use_gpu=True)

  adata_ref = mod.export_posterior(
      adata_ref, sample_kwargs={'num_samples': 1000, 'batch_size': 2500, 'use_gpu': True}
  )

  # export estimated expression in each cluster
  if 'means_per_cluster_mu_fg' in adata_ref.varm.keys():
      inf_aver = adata_ref.varm['means_per_cluster_mu_fg'][[f'means_per_cluster_mu_fg_{i}' 
                                      for i in adata_ref.uns['mod']['factor_names']]].copy()
  else:
      inf_aver = adata_ref.var[[f'means_per_cluster_mu_fg_{i}' 
                                      for i in adata_ref.uns['mod']['factor_names']]].copy()
  inf_aver.columns = adata_ref.uns['mod']['factor_names']
  inf_aver.iloc[0:5, 0:5]

  return inf_aver


def deconvolute(adata, ref):
  '''
  deconvolute takes an annotated data object adata produced
  in the data processing module and a single-cell reference 
  data ref as a pandas dataframe, and performs deconvolution 
  methods as demonstrated in the cell2location tutorial with 
  human lymph node. The cell abundance is stored in obsm and
  the deconvolution model is stored in uns['mod']. 
  '''

  cell2location.models.Cell2location.setup_anndata(adata=adata)

  # create and train the model
  mod = cell2location.models.Cell2location(
      adata, cell_state_df=ref, 
      # the expected average cell abundance: tissue-dependent 
      # hyper-prior which can be estimated from paired histology:
      N_cells_per_location=30,
      # hyperparameter controlling normalisation of
      # within-experiment variation in RNA detection:
      detection_alpha=20
  ) 

  mod.train(max_epochs=30000, 
            # train using full data (batch_size=None)
            batch_size=None, 
            # use all data points in training because 
            # we need to estimate cell abundance at all locations
            train_size=1,
            use_gpu=True,
          )

  # In this section, we export the estimated cell abundance (summary of the posterior distribution).
  adata = mod.export_posterior(
      adata, sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs, 'use_gpu': True}
  )

  # Compute expected expression per cell type
  expected_dict = mod.module.model.compute_expected_per_cell_type(
      mod.samples["post_sample_q05"], mod.adata_manager
  )

  # Add to anndata layers
  for i, n in enumerate(mod.factor_names_):
      adata.layers[n] = expected_dict['mu'][i]


def cell_type_identification(adata):
  '''
  cell_type_identification takes an annotated data object adata, and
  identifies cell types in adata via KNN and Leiden clustering, as 
  recommended in the cell2location tutorial.
  '''

  # compute KNN using the cell2location output stored in adata.obsm
  sc.pp.neighbors(adata, use_rep='q05_cell_abundance_w_sf',
                  n_neighbors = 15)

  # Cluster spots into regions using scanpy
  sc.tl.leiden(adata, resolution=1.1)

  # add region as categorical variable
  adata.obs["region_cluster"] = adata.obs["leiden"].astype("category")

