import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import glob
import os
import sys

# developed and tested at Python version is 3.9.16

def get_var_array_pandas(reg, var, table, proc, models, ripf, scenario, years, in_dir):  # remove option to calc wrt 1850
    
    file_hist = scenario[0]+'/'+'CMIP6_'+scenario[0]+'_'+var+'_'+reg+'_'+years[0]+'.csv'
    file_126 = scenario[1]+'/'+'CMIP6_'+scenario[1]+'_'+var+'_'+reg+'_'+years[1]+'.csv'
    file_370 = scenario[2]+'/'+'CMIP6_'+scenario[2]+'_'+var+'_'+reg+'_'+years[2]+'.csv'

    if (os.path.isfile(in_dir+file_hist)):
        
        df_var_hist = pd.read_csv(in_dir+ file_hist)
# order to ensure "year" is first
        new_cols = ['year']+[col for col in df_var_hist.columns if col != 'year']
        df_var_hist = df_var_hist[new_cols]

        y_hist = df_var_hist['year'].values
        var_array_hist = df_var_hist.drop('year', axis=1).values.T

    if (os.path.isfile(in_dir+file_126)):
        df_var_126 = pd.read_csv(in_dir+ file_126)
        df_var_126 = df_var_126[df_var_hist.columns]
# order to ensure "year" is first
        new_cols = ['year']+[col for col in df_var_126.columns if col != 'year']
        df_var_126 = df_var_126[new_cols]

        y_126 = df_var_126['year'].values
        var_array_126 = df_var_126.drop('year', axis=1).values.T
        
    if (os.path.isfile(in_dir+file_370)):
        df_var_370 = pd.read_csv(in_dir+ file_370)
        df_var_370 = df_var_370[df_var_hist.columns]
# order to ensure "year" is first
        new_cols = ['year']+[col for col in df_var_370.columns if col != 'year']
        df_var_370 = df_var_370[new_cols]

        y_370 = df_var_370['year'].values
        var_array_370 = df_var_370.drop('year', axis=1).values.T
        
    model_list = list(df_var_370.drop('year', axis=1).columns)

    return y_hist, y_126, y_370, var_array_hist, var_array_126, var_array_370, model_list

# duplicate for ctot, but expanded to sum veg+soil+litter if they all exist

def get_var_array_pandas_ctot(reg, scenario, years, in_dir):  # remove option to calc wrt 1850
    
    file_hist_veg = scenario[0]+'/'+'CMIP6_'+scenario[0]+'_'+'cVeg'+'_'+reg+'_'+years[0]+'.csv'
    file_126_veg = scenario[1]+'/'+'CMIP6_'+scenario[1]+'_'+'cVeg'+'_'+reg+'_'+years[1]+'.csv'
    file_370_veg = scenario[2]+'/'+'CMIP6_'+scenario[2]+'_'+'cVeg'+'_'+reg+'_'+years[2]+'.csv'

    file_hist_soil = scenario[0]+'/'+'CMIP6_'+scenario[0]+'_'+'cSoil'+'_'+reg+'_'+years[0]+'.csv'
    file_126_soil = scenario[1]+'/'+'CMIP6_'+scenario[1]+'_'+'cSoil'+'_'+reg+'_'+years[1]+'.csv'
    file_370_soil = scenario[2]+'/'+'CMIP6_'+scenario[2]+'_'+'cSoil'+'_'+reg+'_'+years[2]+'.csv'

    file_hist_litter = scenario[0]+'/'+'CMIP6_'+scenario[0]+'_'+'cLitter'+'_'+reg+'_'+years[0]+'.csv'
    file_126_litter = scenario[1]+'/'+'CMIP6_'+scenario[1]+'_'+'cLitter'+'_'+reg+'_'+years[1]+'.csv'
    file_370_litter = scenario[2]+'/'+'CMIP6_'+scenario[2]+'_'+'cLitter'+'_'+reg+'_'+years[2]+'.csv'

    if (os.path.isfile(in_dir+file_hist_veg)):
        
        df_var_hist_veg = pd.read_csv(in_dir+ file_hist_veg)
        df_var_hist_soil = pd.read_csv(in_dir+ file_hist_soil)
        df_var_hist_litter = pd.read_csv(in_dir+ file_hist_litter)

        # drop any veg columns not in soil
        for col in df_var_hist_veg.columns:
            if col not in df_var_hist_soil:
                df_var_hist_veg = df_var_hist_veg.drop(col, axis=1)
        # pad any missing litter columns with zeros
        for col in df_var_hist_veg.columns:
            if col not in df_var_hist_litter:
                df_var_hist_litter.insert(2, col, 0)

        df_var_hist = df_var_hist_veg + df_var_hist_soil + df_var_hist_litter
# order to ensure "year" is first, and resset it so it's not the sum of years
        new_cols = ['year']+[col for col in df_var_hist.columns if col != 'year']
        df_var_hist = df_var_hist[new_cols]
        df_var_hist['year'] = df_var_hist_veg['year']

        y_hist = df_var_hist['year'].values
        
    if (os.path.isfile(in_dir+file_126_veg)):
        
        df_var_126_veg = pd.read_csv(in_dir+ file_126_veg)
        df_var_126_soil = pd.read_csv(in_dir+ file_126_soil)
        df_var_126_litter = pd.read_csv(in_dir+ file_126_litter)

        # drop any veg columns not in soil
        for col in df_var_126_veg.columns:
            if col not in df_var_126_soil:
                df_var_126_veg = df_var_126_veg.drop(col, axis=1)
        # pad any missing litter columns with zeros
        for col in df_var_126_veg.columns:
            if col not in df_var_126_litter:
                df_var_126_litter.insert(2, col, 0)

        df_var_126 = df_var_126_veg + df_var_126_soil + df_var_126_litter
# order to ensure "year" is first, and resset it so it's not the sum of years
        new_cols = ['year']+[col for col in df_var_126.columns if col != 'year']
        df_var_126 = df_var_126[new_cols]
        df_var_126['year'] = df_var_126_veg['year']

        col_list = [col for col in df_var_126.columns if col != 'year']
        y_126 = df_var_126['year'].values
        
    if (os.path.isfile(in_dir+file_370_veg)):
        
        df_var_370_veg = pd.read_csv(in_dir+ file_370_veg)
        df_var_370_soil = pd.read_csv(in_dir+ file_370_soil)
        df_var_370_litter = pd.read_csv(in_dir+ file_370_litter)

        # drop any veg columns not in soil
        for col in df_var_370_veg.columns:
            if col not in df_var_370_soil:
                df_var_370_veg = df_var_370_veg.drop(col, axis=1)
        # pad any missing litter columns with zeros
        for col in df_var_370_veg.columns:
            if col not in df_var_370_litter:
                df_var_370_litter.insert(2, col, 0)

        df_var_370 = df_var_370_veg + df_var_370_soil + df_var_370_litter
# order to ensure "year" is first, and resset it so it's not the sum of years
        new_cols = ['year']+[col for col in df_var_370.columns if col != 'year']
        df_var_370 = df_var_370[new_cols]
        df_var_370['year'] = df_var_370_veg['year']

        col_list = [col for col in df_var_370.columns if col != 'year']
        y_370 = df_var_370['year'].values
        
    # get rid of any columns with Nans
    if (df_var_hist.isnull().values.any()):
        nan_cols = df_var_hist.columns[df_var_hist.isna().any()].tolist()
        #print('stripping (hist): ', nan_cols)
        df_var_hist = df_var_hist.drop(nan_cols, axis=1)
        df_var_126 = df_var_126.drop(nan_cols, axis=1)
        df_var_370 = df_var_370.drop(nan_cols, axis=1)
    if (df_var_126.isnull().values.any()):
        nan_cols = df_var_126.columns[df_var_126.isna().any()].tolist()
        #print('stripping (126): ', nan_cols)
        df_var_hist = df_var_hist.drop(nan_cols, axis=1)
        df_var_126 = df_var_126.drop(nan_cols, axis=1)
        df_var_370 = df_var_370.drop(nan_cols, axis=1)
    if (df_var_370.isnull().values.any()):
        nan_cols = df_var_370.columns[df_var_370.isna().any()].tolist()
        #print('stripping (370): ', nan_cols)
        df_var_hist = df_var_hist.drop(nan_cols, axis=1)
        df_var_126 = df_var_126.drop(nan_cols, axis=1)
        df_var_370 = df_var_370.drop(nan_cols, axis=1)
    
# extract values from columns which are not "year"
    var_array_hist = df_var_hist.drop('year', axis=1).values.T
    var_array_126 = df_var_126.drop('year', axis=1).values.T
    var_array_370 = df_var_370.drop('year', axis=1).values.T
    model_list = list(df_var_370.drop('year', axis=1).columns)

    return y_hist, y_126, y_370, var_array_hist, var_array_126, var_array_370, model_list


def do_plot(reg, in_dir, gpp_cmip_mean, gpp_cmip_std, gpp_reccap_mean, gpp_reccap_std, gpp_ax_min, gpp_ax_max,
	                 nbp_cmip_mean, nbp_cmip_std, nbp_reccap_mean, nbp_reccap_std, nbp_ax_min, nbp_ax_max,
                         ctot_cmip_mean, ctot_cmip_std, ctot_reccap_mean, ctot_reccap_std, ctot_ax_min, ctot_ax_max):

    # matrix of scenarios and variables
    
    var = ['tas', 'pr', 'cVeg', 'cLitter', 'cProduct', 'cSoil', 'cLand', 'gpp', 'npp', 'rh', 'nbp', 'ctot']
    table = ['Amon', 'Amon', 'Lmon', 'Lmon', 'Lmon', 'Emon', 'Emon', 'Lmon', 'Lmon', 'Lmon', 'Lmon', 'Lmon']
    proc = [1,    4,    2,       2,       2,       2,       2,         3,     3,     3,    3,     3, 3] # controls: 1 = avergae, 2 = carbon store total, 3 = carbon flux: total and scale units
    unit = ['K',  'mm day-1', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1']
    scenario = ['historical', 'ssp126', 'ssp370']
    years    = ['1850-2014', '2015-2100', '2015-2100']
    
    models = ['ACCESS-ESM1-5', 'BCC-CSM2-MR', 'BCC-ESM1', 'CAS-ESM2-0', 'CESM2-WACCM', 'CMCC-CM2-SR5', 'CMCC-ESM2', 'CNRM-ESM2-1', 'CanESM5',  'EC-Earth3-Veg', 'GFDL-ESM4', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KIOST-ESM', 'MIROC-ES2L', 'MPI-ESM1-2-LR', 'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL']
    ripf =   ['r1i1p1f1',      'r1i1p1f1',    'r1i1p1f1', 'r1i1p1f1',   'r1i1p1f1',    'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',    'r1i1p1f1', 'r1i1p1f1',      'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',   'r1i1p1f1',      'r1i1p1f1',   'r1i1p1f1', 'r1i1p1f2']
    
    # get GPP
    y_hist, y_126, y_370, gpp_array_hist, gpp_array_126, gpp_array_370, model_list_gpp = \
            get_var_array_pandas(reg, var[7], table[7], proc[7], models, ripf, scenario, years, in_dir)
    # get NBP
    y_hist, y_126, y_370, nbp_array_hist, nbp_array_126, nbp_array_370, model_list_nbp = \
            get_var_array_pandas(reg, var[10], table[10], proc[10], models, ripf, scenario, years, in_dir)
    # get cTot
    y_hist, y_126, y_370, ctot_array_hist, ctot_array_126, ctot_array_370, model_list_ctot = \
            get_var_array_pandas_ctot(reg, scenario, years, in_dir)
    
    gpp_mean_hist = np.mean(gpp_array_hist,0)
    gpp_25_hist   = np.percentile(gpp_array_hist,25,0)
    gpp_75_hist   = np.percentile(gpp_array_hist,75,0)
    gpp_10_hist   = np.percentile(gpp_array_hist,10,0)
    gpp_90_hist   = np.percentile(gpp_array_hist,90,0)
    gpp_05_hist   = np.percentile(gpp_array_hist,5, 0)
    gpp_95_hist   = np.percentile(gpp_array_hist,95,0)
    
    gpp_mean_126 = np.mean(gpp_array_126,0)
    gpp_25_126   = np.percentile(gpp_array_126,25,0)
    gpp_75_126   = np.percentile(gpp_array_126,75,0)
    gpp_10_126   = np.percentile(gpp_array_126,10,0)
    gpp_90_126   = np.percentile(gpp_array_126,90,0)
    gpp_05_126   = np.percentile(gpp_array_126,5, 0)
    gpp_95_126   = np.percentile(gpp_array_126,95,0)
    
    gpp_mean_370 = np.mean(gpp_array_370,0)
    gpp_25_370   = np.percentile(gpp_array_370,25,0)
    gpp_75_370   = np.percentile(gpp_array_370,75,0)
    gpp_10_370   = np.percentile(gpp_array_370,10,0)
    gpp_90_370   = np.percentile(gpp_array_370,90,0)
    gpp_05_370   = np.percentile(gpp_array_370,5, 0)
    gpp_95_370   = np.percentile(gpp_array_370,95,0)

    nbp_mean_hist = np.mean(nbp_array_hist,0)
    nbp_25_hist   = np.percentile(nbp_array_hist,25,0)
    nbp_75_hist   = np.percentile(nbp_array_hist,75,0)
    nbp_10_hist   = np.percentile(nbp_array_hist,10,0)
    nbp_90_hist   = np.percentile(nbp_array_hist,90,0)
    nbp_05_hist   = np.percentile(nbp_array_hist,5, 0)
    nbp_95_hist   = np.percentile(nbp_array_hist,95,0)
    
    nbp_mean_126 = np.mean(nbp_array_126,0)
    nbp_25_126   = np.percentile(nbp_array_126,25,0)
    nbp_75_126   = np.percentile(nbp_array_126,75,0)
    nbp_10_126   = np.percentile(nbp_array_126,10,0)
    nbp_90_126   = np.percentile(nbp_array_126,90,0)
    nbp_05_126   = np.percentile(nbp_array_126,5, 0)
    nbp_95_126   = np.percentile(nbp_array_126,95,0)
    
    nbp_mean_370 = np.mean(nbp_array_370,0)
    nbp_25_370   = np.percentile(nbp_array_370,25,0)
    nbp_75_370   = np.percentile(nbp_array_370,75,0)
    nbp_10_370   = np.percentile(nbp_array_370,10,0)
    nbp_90_370   = np.percentile(nbp_array_370,90,0)
    nbp_05_370   = np.percentile(nbp_array_370,5, 0)
    nbp_95_370   = np.percentile(nbp_array_370,95,0)

    ctot_mean_hist = np.mean(ctot_array_hist,0)
    ctot_25_hist   = np.percentile(ctot_array_hist,25,0)
    ctot_75_hist   = np.percentile(ctot_array_hist,75,0)
    ctot_10_hist   = np.percentile(ctot_array_hist,10,0)
    ctot_90_hist   = np.percentile(ctot_array_hist,90,0)
    ctot_05_hist   = np.percentile(ctot_array_hist,5, 0)
    ctot_95_hist   = np.percentile(ctot_array_hist,95,0)
    
    ctot_mean_126 = np.mean(ctot_array_126,0)
    ctot_25_126   = np.percentile(ctot_array_126,25,0)
    ctot_75_126   = np.percentile(ctot_array_126,75,0)
    ctot_10_126   = np.percentile(ctot_array_126,10,0)
    ctot_90_126   = np.percentile(ctot_array_126,90,0)
    ctot_05_126   = np.percentile(ctot_array_126,5, 0)
    ctot_95_126   = np.percentile(ctot_array_126,95,0)
    
    ctot_mean_370 = np.mean(ctot_array_370,0)
    ctot_25_370   = np.percentile(ctot_array_370,25,0)
    ctot_75_370   = np.percentile(ctot_array_370,75,0)
    ctot_10_370   = np.percentile(ctot_array_370,10,0)
    ctot_90_370   = np.percentile(ctot_array_370,90,0)
    ctot_05_370   = np.percentile(ctot_array_370,5, 0)
    ctot_95_370   = np.percentile(ctot_array_370,95,0)

    # select based on RECCAP2 mean
    
    incl_gpp = np.zeros(len(gpp_array_126))
    incl_nbp = np.zeros(len(nbp_array_126))
    incl_ctot = np.zeros(len(ctot_array_126))
    
    # logical switch to skip plotting if no models included after filtering
    l_filt_gpp = True
    l_filt_nbp = True
    l_filt_ctot = True
    
    if (gpp_reccap_mean != -99):
        for i in range(len(incl_gpp)):
            incl_gpp[i] = (np.mean(gpp_array_hist[i][-10:]) > gpp_reccap_mean-gpp_reccap_std) & (np.mean(gpp_array_hist[i][-10:]) < gpp_reccap_mean+gpp_reccap_std)
            
        print(reg, ' filter includes: ', incl_gpp)
        l_filt_gpp = (np.sum(incl_gpp) > 0)
        print('filtered GPP list: ',np.array(model_list_gpp)[incl_gpp == 1], np.sum(incl_gpp), l_filt_gpp)
        
        if l_filt_gpp:
           gpp_mean_hist_filtered = np.mean(np.array(gpp_array_hist)[incl_gpp == 1],0)
           gpp_25_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],25,0)
           gpp_75_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],75,0)
           gpp_10_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],10,0)
           gpp_90_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],90,0)
           gpp_00_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],00,0)
           gpp_100_hist_filtered   = np.percentile(np.array(gpp_array_hist)[incl_gpp == 1],100,0)
           
           gpp_mean_126_filtered = np.mean(np.array(gpp_array_126)[incl_gpp == 1],0)
           gpp_25_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],25,0)
           gpp_75_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],75,0)
           gpp_10_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],10,0)
           gpp_90_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],90,0)
           gpp_00_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],00,0)
           gpp_100_126_filtered   = np.percentile(np.array(gpp_array_126)[incl_gpp == 1],100,0)
           
           gpp_mean_370_filtered = np.mean(np.array(gpp_array_370)[incl_gpp == 1],0)
           gpp_25_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],25,0)
           gpp_75_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],75,0)
           gpp_10_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],10,0)
           gpp_90_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],90,0)
           gpp_00_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],00,0)
           gpp_100_370_filtered   = np.percentile(np.array(gpp_array_370)[incl_gpp == 1],100,0)
    
    if (nbp_reccap_mean != -99):
        for i in range(len(incl_nbp)):
            incl_nbp[i] = (np.mean(nbp_array_hist[i][-10:]) > nbp_reccap_mean-nbp_reccap_std) & (np.mean(nbp_array_hist[i][-10:]) < nbp_reccap_mean+nbp_reccap_std)
            
        print(reg, ' filter includes: ', incl_nbp)
        
        l_filt_nbp = (np.sum(incl_nbp) > 0)
        print('filtered nbp list: ',np.array(model_list_nbp)[incl_nbp == 1], np.sum(incl_nbp), l_filt_nbp)
        
        if l_filt_nbp:
           nbp_mean_hist_filtered = np.mean(np.array(nbp_array_hist)[incl_nbp == 1],0)
           nbp_25_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],25,0)
           nbp_75_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],75,0)
           nbp_10_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],10,0)
           nbp_90_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],90,0)
           nbp_00_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],00,0)
           nbp_100_hist_filtered   = np.percentile(np.array(nbp_array_hist)[incl_nbp == 1],100,0)
           
           nbp_mean_126_filtered = np.mean(np.array(nbp_array_126)[incl_nbp == 1],0)
           nbp_25_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],25,0)
           nbp_75_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],75,0)
           nbp_10_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],10,0)
           nbp_90_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],90,0)
           nbp_00_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],00,0)
           nbp_100_126_filtered   = np.percentile(np.array(nbp_array_126)[incl_nbp == 1],100,0)
           
           nbp_mean_370_filtered = np.mean(np.array(nbp_array_370)[incl_nbp == 1],0)
           nbp_25_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],25,0)
           nbp_75_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],75,0)
           nbp_10_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],10,0)
           nbp_90_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],90,0)
           nbp_00_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],00,0)
           nbp_100_370_filtered   = np.percentile(np.array(nbp_array_370)[incl_nbp == 1],100,0)
    
    if (ctot_reccap_mean != -99):
        for i in range(len(incl_ctot)):
            incl_ctot[i] = (np.mean(ctot_array_hist[i][-10:]) > ctot_reccap_mean-ctot_reccap_std) & (np.mean(ctot_array_hist[i][-10:]) < ctot_reccap_mean+ctot_reccap_std)
            
        print(reg, ' filter includes: ', incl_ctot)
        
        l_filt_ctot = (np.sum(incl_ctot) > 0)
        print('filtered ctot list: ',np.array(model_list_ctot)[incl_ctot == 1], np.sum(incl_ctot), l_filt_ctot)
        
        if l_filt_ctot:
           ctot_mean_hist_filtered = np.mean(np.array(ctot_array_hist)[incl_ctot == 1],0)
           ctot_25_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],25,0)
           ctot_75_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],75,0)
           ctot_10_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],10,0)
           ctot_90_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],90,0)
           ctot_00_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],00,0)
           ctot_100_hist_filtered   = np.percentile(np.array(ctot_array_hist)[incl_ctot == 1],100,0)
           
           ctot_mean_126_filtered = np.mean(np.array(ctot_array_126)[incl_ctot == 1],0)
           ctot_25_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],25,0)
           ctot_75_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],75,0)
           ctot_10_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],10,0)
           ctot_90_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],90,0)
           ctot_00_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],00,0)
           ctot_100_126_filtered   = np.percentile(np.array(ctot_array_126)[incl_ctot == 1],100,0)
           
           ctot_mean_370_filtered = np.mean(np.array(ctot_array_370)[incl_ctot == 1],0)
           ctot_25_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],25,0)
           ctot_75_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],75,0)
           ctot_10_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],10,0)
           ctot_90_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],90,0)
           ctot_00_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],00,0)
           ctot_100_370_filtered   = np.percentile(np.array(ctot_array_370)[incl_ctot == 1],100,0)
        
# 3-up panels
    fig, ((ax1, ax2, ax3),(ax4, ax5, ax6),(ax7, ax8, ax9)) = plt.subplots(3,3, sharey='row', figsize=(16, 15))
    
    # hide the spines between ax1 and ax2
    ax1.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax3.axis('off')
    
    ax4.spines['right'].set_visible(False)
    ax5.spines['left'].set_visible(False)
    ax6.axis('off')
    
    ax7.spines['right'].set_visible(False)
    ax8.spines['left'].set_visible(False)
    ax9.axis('off')
    
    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)
    
    ax4.tick_params(labelsize=14)
    ax5.tick_params(labelsize=14)
    
    ax7.tick_params(labelsize=14)
    ax8.tick_params(labelsize=14)
    
    ax1.yaxis.tick_left()
    ax2.yaxis.tick_right()
    
    ax4.yaxis.tick_left()
    ax5.yaxis.tick_right()
    
    ax7.yaxis.tick_left()
    ax8.yaxis.tick_right()
    
    ax1.set_ylim(gpp_ax_min, gpp_ax_max)
    ax1.set_xlim(1850,2025)
    ax2.set_xlim(2015,2100)
    ax3.set_xlim(0,11)

    ax4.set_ylim(nbp_ax_min, nbp_ax_max)
    ax4.set_xlim(1850,2025)
    ax5.set_xlim(2015,2100)
    ax6.set_xlim(0,11)

    ax7.set_ylim(ctot_ax_min, ctot_ax_max)
    ax7.set_xlim(1850,2025)
    ax8.set_xlim(2015,2100)
    ax9.set_xlim(0,11)
    
    # GPP plotting
    ax1.fill_between(y_hist, gpp_10_hist, gpp_90_hist, facecolor='k', alpha=0.2)
    
    for g in gpp_array_hist:
        g_mn = np.mean(g[-10:])
        gcol = 'darkgreen'; gw = .5
        if g_mn < gpp_reccap_mean-gpp_reccap_std : gcol='k'; gw =0.2
        if g_mn > gpp_reccap_mean+gpp_reccap_std : gcol='k'; gw =0.2
        if (gpp_reccap_mean == -99): gcol='k'; gw =0.2
	
        ax1.plot(y_hist, g, color=gcol, lw=gw)
    
    ax1.plot(y_hist, gpp_mean_hist, 'k', lw=2)
    ax2.plot(y_126, gpp_mean_126, 'b', lw=2)
    ax2.plot(y_370, gpp_mean_370, 'r', lw=2)
    
    ax1.errorbar(2019, gpp_cmip_mean, yerr=gpp_cmip_std, fmt='o', color='k')
    if (gpp_reccap_mean != -99): ax1.errorbar(2023, gpp_reccap_mean, yerr=gpp_reccap_std, fmt='o', color='g')
    
    for g in gpp_array_126:
        ax2.plot(y_126, g, 'b', lw=.1)
    
    for g in gpp_array_370:
        ax2.plot(y_370, g, 'r', lw=.1)
    
    if (l_filt_gpp and gpp_reccap_mean != -99): 
        ax2.fill_between(y_126, gpp_10_126_filtered, gpp_90_126_filtered, facecolor='b', alpha=0.2)
        ax2.fill_between(y_370, gpp_10_370_filtered, gpp_90_370_filtered, facecolor='r', alpha=0.2)
    
    ax3.bar(0.5, np.mean(gpp_90_126[25:45])-np.mean(gpp_10_126[25:45]), width=0.4, bottom=np.mean(gpp_10_126[25:45]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax3.bar(1.1, np.mean(gpp_90_370[25:45])-np.mean(gpp_10_370[25:45]), width=0.4, bottom=np.mean(gpp_10_370[25:45]),
            align='edge', edgecolor='k', color='r', alpha=0.5)
    ax3.bar(5, np.mean(gpp_90_126[65:])-np.mean(gpp_10_126[65:]), width=0.4, bottom=np.mean(gpp_10_126[65:]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax3.bar(5.6, np.mean(gpp_90_370[65:])-np.mean(gpp_10_370[65:]), width=0.4, bottom=np.mean(gpp_10_370[65:]),
            align='edge', edgecolor='k', color='r', alpha=0.5)

    if (l_filt_gpp and gpp_reccap_mean != -99): 
        ax3.bar(2.2, np.mean(gpp_90_126_filtered[25:45])-np.mean(gpp_10_126_filtered[25:45]), width=0.4, bottom=np.mean(gpp_10_126_filtered[25:45]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax3.bar(2.8, np.mean(gpp_90_370_filtered[25:45])-np.mean(gpp_10_370_filtered[25:45]), width=0.4, bottom=np.mean(gpp_10_370_filtered[25:45]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
        ax3.bar(6.7, np.mean(gpp_90_126_filtered[65:])-np.mean(gpp_10_126_filtered[65:]), width=0.4, bottom=np.mean(gpp_10_126_filtered[65:]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax3.bar(7.3, np.mean(gpp_90_370_filtered[65:])-np.mean(gpp_10_370_filtered[65:]), width=0.4, bottom=np.mean(gpp_10_370_filtered[65:]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
    
    gpp_ax_range = gpp_ax_max - gpp_ax_min
    ax3.text(1,gpp_ax_min,'2050', fontsize=20)
    ax3.text(5.5,gpp_ax_min,'2100', fontsize=20)
    
    ax3.text(0.5, gpp_ax_min+gpp_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (gpp_reccap_mean != -99): ax3.text(2.2, gpp_ax_min+gpp_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    ax3.text(5, gpp_ax_min+gpp_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (gpp_reccap_mean != -99): ax3.text(6.7, gpp_ax_min+gpp_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    
    ax1.set_title('CMIP6 models historical', fontsize=18)
    ax2.set_title('CMIP6 models projections', fontsize=18)

    ax1.text(1860, gpp_ax_min+gpp_ax_range*0.9, 'a. GPP', fontsize=16)    
    ax1.set_ylabel('PgC yr-1', fontsize=16)

    # NBP plotting
    ax4.fill_between(y_hist, nbp_10_hist, nbp_90_hist, facecolor='k', alpha=0.2)
    
    for g in nbp_array_hist:
        g_mn = np.mean(g[-10:])
        gcol = 'darkgreen'; gw = .5
        if g_mn < nbp_reccap_mean-nbp_reccap_std : gcol='k'; gw =0.2
        if g_mn > nbp_reccap_mean+nbp_reccap_std : gcol='k'; gw =0.2
        if (nbp_reccap_mean == -99): gcol='k'; gw =0.2
	
        ax4.plot(y_hist, g, color=gcol, lw=gw)
    
    ax4.plot(y_hist, nbp_mean_hist, 'k', lw=2)
    ax5.plot(y_126, nbp_mean_126, 'b', lw=2)
    ax5.plot(y_370, nbp_mean_370, 'r', lw=2)
    
    ax4.axhline(color='k', lw=0.5)
    ax5.axhline(color='k', lw=0.5)
    ax6.axhline(color='k', lw=0.5)
    
    ax4.errorbar(2019, nbp_cmip_mean, yerr=nbp_cmip_std, fmt='o', color='k')
    if (nbp_reccap_mean != -99): ax4.errorbar(2023, nbp_reccap_mean, yerr=nbp_reccap_std, fmt='o', color='g')
    
    for g in nbp_array_126:
        ax5.plot(y_126, g, 'b', lw=.1)
    
    for g in nbp_array_370:
        ax5.plot(y_370, g, 'r', lw=.1)
    
    if (l_filt_nbp and nbp_reccap_mean != -99): 
        ax5.fill_between(y_126, nbp_10_126_filtered, nbp_90_126_filtered, facecolor='b', alpha=0.2)
        ax5.fill_between(y_370, nbp_10_370_filtered, nbp_90_370_filtered, facecolor='r', alpha=0.2)
    
    ax6.bar(0.5, np.mean(nbp_90_126[25:45])-np.mean(nbp_10_126[25:45]), width=0.4, bottom=np.mean(nbp_10_126[25:45]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax6.bar(1.1, np.mean(nbp_90_370[25:45])-np.mean(nbp_10_370[25:45]), width=0.4, bottom=np.mean(nbp_10_370[25:45]),
            align='edge', edgecolor='k', color='r', alpha=0.5)
    ax6.bar(5, np.mean(nbp_90_126[65:])-np.mean(nbp_10_126[65:]), width=0.4, bottom=np.mean(nbp_10_126[65:]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax6.bar(5.6, np.mean(nbp_90_370[65:])-np.mean(nbp_10_370[65:]), width=0.4, bottom=np.mean(nbp_10_370[65:]),
            align='edge', edgecolor='k', color='r', alpha=0.5)

    if (l_filt_nbp and nbp_reccap_mean != -99): 
        ax6.bar(2.2, np.mean(nbp_90_126_filtered[25:45])-np.mean(nbp_10_126_filtered[25:45]), width=0.4, bottom=np.mean(nbp_10_126_filtered[25:45]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax6.bar(2.8, np.mean(nbp_90_370_filtered[25:45])-np.mean(nbp_10_370_filtered[25:45]), width=0.4, bottom=np.mean(nbp_10_370_filtered[25:45]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
        ax6.bar(6.7, np.mean(nbp_90_126_filtered[65:])-np.mean(nbp_10_126_filtered[65:]), width=0.4, bottom=np.mean(nbp_10_126_filtered[65:]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax6.bar(7.3, np.mean(nbp_90_370_filtered[65:])-np.mean(nbp_10_370_filtered[65:]), width=0.4, bottom=np.mean(nbp_10_370_filtered[65:]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
    
    nbp_ax_range = nbp_ax_max - nbp_ax_min
    ax6.text(1,nbp_ax_min,'2050', fontsize=20)
    ax6.text(5.5,nbp_ax_min,'2100', fontsize=20)
    
    ax6.text(0.5, nbp_ax_min+nbp_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (nbp_reccap_mean != -99): ax6.text(2.2, nbp_ax_min+nbp_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    ax6.text(5, nbp_ax_min+nbp_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (nbp_reccap_mean != -99): ax6.text(6.7, nbp_ax_min+nbp_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    
    ax4.set_title('CMIP6 models historical', fontsize=18)
    ax5.set_title('CMIP6 models projections', fontsize=18)

    ax4.text(1860, nbp_ax_min+nbp_ax_range*0.9, 'b. NBP', fontsize=16)    
    ax4.set_ylabel('PgC yr-1', fontsize=16)

    # cTot plotting
    ax7.fill_between(y_hist, ctot_10_hist, ctot_90_hist, facecolor='k', alpha=0.2)
    
    for g in ctot_array_hist:
        g_mn = np.mean(g[-10:])
        gcol = 'darkgreen'; gw = .5
        if g_mn < ctot_reccap_mean-ctot_reccap_std : gcol='k'; gw =0.2
        if g_mn > ctot_reccap_mean+ctot_reccap_std : gcol='k'; gw =0.2
        if (ctot_reccap_mean == -99): gcol='k'; gw =0.2
	
        ax7.plot(y_hist, g, color=gcol, lw=gw)
    
    ax7.plot(y_hist, ctot_mean_hist, 'k', lw=2)
    ax8.plot(y_126, ctot_mean_126, 'b', lw=2)
    ax8.plot(y_370, ctot_mean_370, 'r', lw=2)
    
    ax7.errorbar(2019, ctot_cmip_mean, yerr=ctot_cmip_std, fmt='o', color='k')
    if (ctot_reccap_mean != -99): ax7.errorbar(2023, ctot_reccap_mean, yerr=ctot_reccap_std, fmt='o', color='g')
    
    for g in ctot_array_126:
        ax8.plot(y_126, g, 'b', lw=.1)
    
    for g in ctot_array_370:
        ax8.plot(y_370, g, 'r', lw=.1)
    
    if (l_filt_ctot and ctot_reccap_mean != -99): 
        ax8.fill_between(y_126, ctot_10_126_filtered, ctot_90_126_filtered, facecolor='b', alpha=0.2)
        ax8.fill_between(y_370, ctot_10_370_filtered, ctot_90_370_filtered, facecolor='r', alpha=0.2)
    
    ax9.bar(0.5, np.mean(ctot_90_126[25:45])-np.mean(ctot_10_126[25:45]), width=0.4, bottom=np.mean(ctot_10_126[25:45]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax9.bar(1.1, np.mean(ctot_90_370[25:45])-np.mean(ctot_10_370[25:45]), width=0.4, bottom=np.mean(ctot_10_370[25:45]),
            align='edge', edgecolor='k', color='r', alpha=0.5)
    ax9.bar(5, np.mean(ctot_90_126[65:])-np.mean(ctot_10_126[65:]), width=0.4, bottom=np.mean(ctot_10_126[65:]),
            align='edge', edgecolor='k', color='b', alpha=0.5)
    ax9.bar(5.6, np.mean(ctot_90_370[65:])-np.mean(ctot_10_370[65:]), width=0.4, bottom=np.mean(ctot_10_370[65:]),
            align='edge', edgecolor='k', color='r', alpha=0.5)
    
    if (l_filt_ctot and ctot_reccap_mean != -99): 
        ax9.bar(2.2, np.mean(ctot_90_126_filtered[25:45])-np.mean(ctot_10_126_filtered[25:45]), width=0.4, bottom=np.mean(ctot_10_126_filtered[25:45]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax9.bar(2.8, np.mean(ctot_90_370_filtered[25:45])-np.mean(ctot_10_370_filtered[25:45]), width=0.4, bottom=np.mean(ctot_10_370_filtered[25:45]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
        ax9.bar(6.7, np.mean(ctot_90_126_filtered[65:])-np.mean(ctot_10_126_filtered[65:]), width=0.4, bottom=np.mean(ctot_10_126_filtered[65:]),
                align='edge', edgecolor='k', color='b', alpha=0.5)
        ax9.bar(7.3, np.mean(ctot_90_370_filtered[65:])-np.mean(ctot_10_370_filtered[65:]), width=0.4, bottom=np.mean(ctot_10_370_filtered[65:]),
                align='edge', edgecolor='k', color='r', alpha=0.5)
    
    ctot_ax_range = ctot_ax_max - ctot_ax_min
    ax9.text(1,ctot_ax_min,'2050', fontsize=20)
    ax9.text(5.5,ctot_ax_min,'2100', fontsize=20)
    
    ax9.text(0.5, ctot_ax_min+ctot_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (ctot_reccap_mean != -99): ax9.text(2.2, ctot_ax_min++ctot_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    ax9.text(5, ctot_ax_min++ctot_ax_range*0.75,'unfiltered', fontsize=16, rotation=60)
    if (ctot_reccap_mean != -99): ax9.text(6.7, ctot_ax_min++ctot_ax_range*0.75,'filtered', fontsize=16, rotation=60)
    
    ax7.text(1860, ctot_ax_min+ctot_ax_range*0.9, 'c. Terrestrial carbon', fontsize=16)    
    ax7.set_ylabel('PgC', fontsize=16)
    ax7.set_xlabel('year', fontsize=16)
    ax8.set_xlabel('year', fontsize=16)

    plt.tight_layout()
    plt.savefig(reg + '_filtered_6up.jpg')
    plt.close()


def main():

# these data should not change by model:

    dir = 'DATA/'
    
    # choose region and variable
    reg_list = [
    	        'North_America',
		'South_America',
		'Europe',
                'Africa',
		'North_Asia',
      	        'Central_Asia',
    	        'East_Asia',
    	        'South_Asia',
    	        'South_East_Asia',
                'Oceania',
		'Permafrost'
                ]
    
    var_cmip_mean_list = [
		      17.46, 0.35, 404.64,  # N America
		      33.72, 0.21, 315.11,  # S America
		      5.04, 0.09, 83.38,    # Europe
                      26.74, 0.24, 220.2,   # Africa			  
		      9.65, 0.34, 438.9,    # N. Asia
    		      2.24, 0.05, 35.32,    # Central_Asia		      
    		      9.44, 0.2, 154.19,    # East_Asia		      
    		      3.71, 0.05, 28.02,    # S. Asia
		      10.31, 0.05, 84.31,   # SE Asia
                      4.85, 0.06, 43.74,    # Oceania
		      9.11, 0.34, 512.8       # Permafrost
    		      ]
    
    var_cmip_std_list = [
		     2.49, 0.19, 204.49,  # N America 
		     5.81, 0.41, 81.78,   # S America 
		     0.89, 0.08, 46.3,    # Europe
                     6, 0.4, 75,          # Africa (guessed confidence ranges for now)			 
		     1.08, 0.16, 283,        # N. Asia
    		     1.16, 0.05, 20.2,    # Central_Asia		     
    		     1.74, 0.17, 63.01,   # East_Asia		     
    		     1.30, 0.06, 12.93,   # S. Asia
		     2.35, 0.16, 22.85,   # SE Asia
                     1.69, 0.07, 17.12,   # Oceania
		     1.79, 0.17, 383.9       # Permafrost
    		     ]
    
    var_reccap_mean_list = [
		        16.79, 0.41, 382.6,    # N America (updated, Aug 2023)
		        33.02, 0.39, 314.7,    # S America (updated Aug 2023)
			5.48, 0.1, -99,        # Europe (updated, Aug 2023)
                        26.3, 0.432, 171.7,    # Africa	(updated Aug 2023)
			9.41, 0.33, 377.25,    # N. Asia (updated Aug 2023)
    			2.33, 0.06, 36.07,     # Central_Asia (updated, Aug 2023)
    			9.32, 0.355, 150.12,   # East_Asia  (updated, Aug 2023)
    			5.11, 0.04, 39.84,     # S. Asia  (updated, Aug 2023)
			11.67, -0.39, 89.2,    # SE Asia (updated, Aug 2023)
                        4.61, 0.0004, 53.86,   # Oceania (updated, Aug 2023)
			7.0, 0.65, -99         # Permafrost
    			]
    
    var_reccap_std_list = [
		       2.1, 0.23, 208.1,    # N America (updated, Aug 2023)
		       5.23, 1.72, 76,      # S America (updated Aug 2023)
		       0.5, 0.05, -99,      # Europe (updated, Aug 2023)
                       3.1, 0.484, 16,      # Africa (updated Aug 2023)
                       1.12, 0.09, 15.9,    # N. Asia (updated Aug 2023)
    		       1.08, 0.02, 21.62,   # Central_Asia  (updated, Aug 2023)
    		       1.39, 0.093, 38.95,  # East_Asia  (updated, Aug 2023)
    		       1.13, 0.06, 11.21,   # S. Asia (updated, Aug 2023)
		       2.43, 0.1, 10.02,    # SE Asia (updated, Aug 2023)
                       2.62, 0.08, 25,      # Oceania (updated, Aug 2023)
		       0.5, 1.15, -99       # Permafrost
    		       ]
    
    ax_min_list = [
                   0, -1.5, 0,
		   0, -3, 0,
		   0, -.5, 0,
                   0, -3, 0,
		   0, -2, 0,
                   0, -1, 0,
                   0, -1, 0,
                   0, -.5, 0,
                   0, -2, 0,
                   0, -1.5, 0,
		   0, -1, 0
                   ]
    
    ax_max_list = [
                   40, 2, 1060,
		   60, 3, 550,
		   12, 1, 200,
                   50, 3, 450,
		   20, 2, 900,
                   8, 1, 85,
                   20, 1.5, 350,
                   10, 1, 65,
                   20, 2, 160,
                   12, 1.5, 100,
		   20, 2, 1200
                   ]
    
    
    # loop over options
    
    for i in range(len(reg_list)):
        reg = reg_list[i]
        print(reg)
        in_dir = dir + 'Processed/' + reg+'/' 
        
        gpp_cmip_mean = var_cmip_mean_list[3*i]
        gpp_cmip_std = var_cmip_std_list[3*i]
        gpp_reccap_mean = var_reccap_mean_list[3*i]
        gpp_reccap_std = var_reccap_std_list[3*i]
        
        nbp_cmip_mean = var_cmip_mean_list[3*i+1]
        nbp_cmip_std = var_cmip_std_list[3*i+1]
        nbp_reccap_mean = var_reccap_mean_list[3*i+1]
        nbp_reccap_std = var_reccap_std_list[3*i+1]
        
        ctot_cmip_mean = var_cmip_mean_list[3*i+2]
        ctot_cmip_std = var_cmip_std_list[3*i+2]
        ctot_reccap_mean = var_reccap_mean_list[3*i+2]
        ctot_reccap_std = var_reccap_std_list[3*i+2]
        
        # axis limits
        gpp_ax_min = ax_min_list[3*i]
        gpp_ax_max = ax_max_list[3*i]
        nbp_ax_min = ax_min_list[3*i+1]
        nbp_ax_max = ax_max_list[3*i+1]
        ctot_ax_min = ax_min_list[3*i+2]
        ctot_ax_max = ax_max_list[3*i+2]
	
        do_plot(reg, in_dir, gpp_cmip_mean, gpp_cmip_std, gpp_reccap_mean, gpp_reccap_std, gpp_ax_min, gpp_ax_max,
	                     nbp_cmip_mean, nbp_cmip_std, nbp_reccap_mean, nbp_reccap_std, nbp_ax_min, nbp_ax_max,
	                     ctot_cmip_mean, ctot_cmip_std, ctot_reccap_mean, ctot_reccap_std, ctot_ax_min, ctot_ax_max)

if __name__ == '__main__':
    main()
