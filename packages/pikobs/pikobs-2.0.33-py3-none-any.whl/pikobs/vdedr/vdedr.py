"""

Generating Verification of Radiance Spacing
===========================================

This script is designed to generate charts that analyze the residual bias and raw bias for each
channel of a specific satellite. These charts provide detailed information on the performance of
the radiance verification system and are essential for assessing the accuracy and consistency
of satellite observations for example:
  

    .. image:: ../../../docs/source/_static/vdedr.png
      :alt: vdedr

The script generates two main types of charts for each channel of the selected satellite:

1. **Residual Bias** This chart compares the residual bias (the differences between observations and adjustments,(O-A) for each channel across both experiments. Importance: Comparing residual bias between experiments allows the user to assess how well bias corrections are performing in each setup and to identify any remaining bias differences that may impact prediction accuracy.


2. **Raw Bias** This chart compares the raw bias (the differences between observations and predictions, O-P, before any corrections) for each channel across both experiments. Importance: Raw bias comparisons reveal systematic differences between experiments in the uncorrected observational data. This helps to detect variations in the initial biases and understand the error patterns in each experimental setup.

*******************************************************
Generate Verification of Radiance Spacing
*******************************************************

To start an interactive session for generating cardiograms, use the following qsub command:
::
    qsub -I -X -l select=4:ncpus=80:mpiprocs=80:ompthreads=1:mem=185gb -l place=scatter -l walltime=6:0:0

Generating Verification of Radiance Spacing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To generate cardiograms using pikobs, use the following command format:
::

   python -c 'import pikobs; pikobs.vdedr.arg_call()' \

         --path_control_files  /home/sprj700/data_maestro/ppp6/maestro_archives/G2FC900V2E22/monitoring/banco/postalt/ \

         --control_name  G2FC900V2E22 \

         --path_experience_files  /home/sprj700/data_maestro/ppp6/maestro_archives/G2FC900V2E22/monitoring/banco/postalt/ \

         --experience_name  G2FC900V2E33 \

         --pathwork   work_to_amsua_allsky \

         --datestart  2022061500 \

         --dateend    2022061700 \

         --region     Monde \

         --family     cris to_amsua_allsky \

         --flags_criteria assimilee \

         --id_stn     all \

         --n_cpu      40

Parameter Explanation
^^^^^^^^^^^^^^^^^^^^^
- **path_control_files:** Path to the directory where the control data is stored.
- **control_name:**  Name of the specific control
- **path_experience_files:** Path to the directory where the experiment data is stored.
- **experience_name:**  Name of the specific experiment.
- **pathwork:**  Path to the working directory for the script.
- **datestart:**  Start date and time of the analysis (format: YYYYMMDDHH).
- **dateend:**  End date and time of the analysis (format: YYYYMMDDHH).
- **region:**  Geographic region of interest (e.g., Global, Northern Hemisphere, Southern Hemisphere).
- **family:**  Family of observation (e.g., mwhs2, mwhs2_qc, to_amsua_qc, to_amsua, to_amsua_allsky, to_amsua_allsky_qc, to_amsub_qc, to_amsub, ssmis_qc, ssmis, iasi, iasi_qc, crisfsr1_qc, crisfsr2_qc, cris, atms_allsky, atms_qc and csr, csr_qc)
- **id_stn:**  Name of the satellite for whichis analyzed (e.g., METOP-1, NOAA-20, all).
- **n_cpu:**   Number of CPU cores to use for parallel processing.

Additional Notes
^^^^^^^^^^^^^^^^

- The residual and raw bias charts provide visual information on each satellite channel’s performance in radiance verification.
- Modify --satellite and --channel parameters as needed to analyze specific satellites and channels.
- Ensure paths (path_experience, pathwork) are correctly set to point to your data directories.
- The script utilizes parallel processing (--n_cpu) to optimize performance. Adjust this value according to your system capabilities.
"""




#!/usr/bin/python3
import sqlite3
import pikobs
import re
import os
from  dask.distributed import Client
import numpy as np
import sqlite3
import os
import re
import sqlite3
from  datetime import datetime, timedelta


def create_serie_cardio(family, 
                        new_db_filename, 
                        existing_db_filename,
                        region_seleccionada,
                        selected_flags, 
                        id_stn,
                       # vcoord, 
                        varno):
    """
    Create a new SQLite database with a 'moyenne' table and populate it with data from an existing database.

    Args:
        new_db_filename (str): Filename of the new database to be created.
        
        existing_db_filename (str): Filename of the existing database to be attached.
  
        region_seleccionada (str): Region selection criteria.
   
        selected_flags (str): Selected flags criteria.
   

    Returns:
     
        None
    """

 
    pattern = r'(\d{10})'
    match = re.search(pattern, existing_db_filename)
    if match:
        date = match.group(1)
       
    else:
        print("No 10 digits found in the string.")
    
    # Connect to the new database
  
    new_db_conn = sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=99999)
    new_db_cursor = new_db_conn.cursor()
    FAM, VCOORD, VCOCRIT, STATB, VCOORD, VCOTYP = pikobs.family(family)
    LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
    LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
    flag_criteria = pikobs.flag_criteria(selected_flags)

    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
    # load extension CMC 
    new_db_conn.enable_load_extension(True)
    extension_dir = f'{os.path.dirname(pikobs.__file__)}/extension/libudfsqlite-shared.so'
    new_db_conn.execute(f"SELECT load_extension('{extension_dir}')")
    if id_stn =='all':
      criteria_id_stn= ' '
    else:
      criteria_id_stn= f" and id_stn='{id_stn}' "
    query = """
           CREATE TABLE IF NOT EXISTS serie_cardio ( 
            DATE INTEGER,
            sumx FLOAT, 
            sumy FLOAT,
            sumz FLOAT,
            sumx2 FLOAT,
            sumy2 float,
            sumz2 float,
            sumStat float,
            Ntot INTEGER,
            vcoord float,
            varno INTEGER,
            id_stn  TEXT
        );
    """
   # print (query)
    new_db_cursor.execute(query)

    query=f"""INSERT INTO serie_cardio (

            DATE,
            sumx, 
            sumy,
            sumz,
            sumx2,
            sumy2,
            sumz2,
            sumStat,
            Ntot,
            vcoord,
            varno,
            id_stn
        )
    
    
             SELECT 
                 isodatetime({date}) ,  
                 sum(oma),
                 sum(omp),
                 sum(obsvalue),
                 sum(oma*oma),
                 sum(omp*omp),
                 sum(obsvalue*obsvalue),
                 sum( {STATB} ),
                 count(*),
                 vcoord,
                 varno,
                 id_stn
            FROM 
                 header
             NATURAL JOIN 
                 data
             WHERE 
                 VARNO = {int(varno)}
                 and obsvalue is not null
                 {criteria_id_stn}
              --   AND ID_STN LIKE 'id_stn'
              --   AND vcoord IN (vcoord)
                 {flag_criteria}
                 {LATLONCRIT}
                 {VCOCRIT}
             GROUP BY 
                 VCOORD, ID_STN, vcoord """
    #print (query)
    new_db_cursor.execute(query)

    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")
    new_db_conn.commit()




    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()

def create_data_list_cardio(datestart1, 
                            dateend1,
                            families,
                            pathin, 
                            name,
                            pathwork,
                            flag_criteria,
                            region,
                            id_stn):
   data_list_cardio = []
   for family in families:
       # Convert datestart and dateend to datetime objects
       datestart = datetime.strptime(datestart1, '%Y%m%d%H')
       dateend = datetime.strptime(dateend1, '%Y%m%d%H')
   
       # Initialize the current_date to datestart
       current_date = datestart
   
       # Define a timedelta of 6 hours
       delta = timedelta(hours=6)
       FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
       
       #flag_criteria = generate_flag_criteria(flag_criteria)
   
       element_array = np.array([float(x) for x in element.split(',')])
       for varno in element_array:
        # Iterate through the date range in 6-hour intervals
        while current_date <= dateend:
           # Format the current date as a string
           formatted_date = current_date.strftime('%Y%m%d%H')
   
           # Build the file name using the date and family
           filename = f'{formatted_date}_{family}'
   
           file_path_name = f'{pathin}/{filename}'
           conn = sqlite3.connect(file_path_name)
           # Create a cursor to execute SQL queries
           cursor = conn.cursor()
   
           channel ='all'
           for ii in id_stn:
              #  Create a new dictionary and append it to the list
              data_dict = {'family': family,
                             'filein': f'{pathin}/{filename}',
                             'db_new': f'{pathwork}/vdedr_{name}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db',
                             'region': region,
                             'flag_criteria': flag_criteria,
                             'varno':  varno,
                             'vcoord': channel,
                             'id_stn': ii}
              data_list_cardio.append(data_dict)
           conn.close()
           # Update the current_date in the loop by adding 6 hours
           current_date += delta
   return data_list_cardio





def create_data_list_plot(datestart1,
                          dateend1, 
                          families, 
                          pathwork, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          channel,
                          files_in,
                          names_in):
   for family in families:                       
       data_list_plot = []
       filedb_control = f'{pathwork}/vdedr_{names_in[0]}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db'
       filedb_experience = f'{pathwork}/vdedr_{names_in[1]}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db'
       conn = sqlite3.connect(filedb_control)
       cursor = conn.cursor()
       if id_stn[0]=='all':
           
           query = "SELECT DISTINCT id_stn, varno  FROM serie_cardio;"
           cursor.execute(query)
           id_stns = cursor.fetchall()
       else:
           stn_str = f"({', '.join(repr(stn) for stn in tuple(id_stn))})"
           query = f"SELECT DISTINCT id_stn, varno  FROM serie_cardio where id_stn in {stn_str};"
           cursor.execute(query)
           id_stns = cursor.fetchall()
   
       for idstn, varno in id_stns:
              
          #if id_stn=='alone':
           #  criter =f'where id_stn = "{idstn[0]}"'
          
          #elif id_stn=='all':
   
          #  criter =' '
   
         # query = f"SELECT DISTINCT chan, varno  FROM serie_cardio {criter} ORDER BY chan ASC;"
         # cursor.execute(query)
         # vcoords = cursor.fetchall()
          #for vcoord, varno in vcoords:
              data_dict_plot = {
               'files_in': [filedb_control,filedb_experience],
               'names_in': names_in,
               'id_stn': idstn,
               'family':family,
               'varno': varno}
              data_list_plot.append(data_dict_plot)
   
   return data_list_plot


def make_cardio( files_in,
                 names_in,
                 pathwork, 
                 datestart,
                 dateend,
                 region, 
                 family, 
                 flag_criteria, 
                 id_stn,
                 channel,
                 n_cpu):

   
   pikobs.delete_create_folder(pathwork)
   for file_in, name_in in zip(files_in,names_in):
       

       data_list_cardio = create_data_list_cardio(datestart,
                                           dateend, 
                                           family, 
                                           file_in,
                                           name_in,
                                           pathwork,
                                           flag_criteria, 
                                           region,
                                           id_stn)
       import time 
       import dask
       t0 = time.time()
       #n_cpu=1
       if n_cpu==1:
        for  data_ in data_list_cardio:  
            print ("Serie for {filein}:")
            create_serie_cardio(data_['family'], 
                                data_['db_new'], 
                                data_['filein'],
                                data_['region'],
                                data_['flag_criteria'],
                                data_['id_stn'],
                                data_['varno'])
    
    
    
    
       else:
        print (f'in Paralle for {name_in}: {len(data_list_cardio)} files ')
        with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(create_serie_cardio)(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['id_stn'],
                                              data_['varno'])for data_ in data_list_cardio]
            results = dask.compute(*delayed_funcs)
        
       tn= time.time()
       print (f'Total time =',round(tn-t0,2) ) 

   data_list_plot = create_data_list_plot(datestart,
                                dateend, 
                                family, 
                                pathwork,
                                flag_criteria, 
                                region,
                                id_stn,
                                channel,
                                files_in,
                                names_in)



  # exit()   
   os.makedirs(f'{pathwork}/vdedr')
   #print (data_list_plot )
   tn= time.time()
   mode='bias'

   if n_cpu==1: 
      print (f'Serie = {len(data_list_plot)}')
      for  data_ in data_list_plot:  
          pikobs.vdedr_plot(pathwork,
                            datestart,
                            dateend,
                            flag_criteria,
                            data_['family'],
                            region,
                            data_['files_in'],
                            data_['names_in'],
                            data_['id_stn'], 
                            data_['varno'],
                            mode)
   else:
      print (f'in Paralle = {len(data_list_plot)} plots')
      with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(pikobs.vdedr_plot)(
                           pathwork,
                            datestart,
                            dateend,
                            flag_criteria,
                            data_['family'],
                            region,
                            data_['files_in'],
                            data_['names_in'],
                            data_['id_stn'], 
                            data_['varno'],
                            mode) for data_ in data_list_plot]

        results = dask.compute(*delayed_funcs)
   print ('Total time for plotting =',round(tn-t0,2) ) 

 



def arg_call():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_control_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--control_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--path_experience_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--experience_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', default='undefined', type=str, help="Region")
    parser.add_argument('--family', nargs="+",default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--id_stn', nargs="+",  default='all', type=str, help="id_stn") 
    parser.add_argument('--channel', nargs="+", default='all', type=str, help="channel") 
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()
    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.path_control_files == 'undefined':
        raise ValueError('You must specify --path_control_files')
    elif args.control_name == 'undefined':
        raise ValueError('You must specify --control_name')
    else:    
      
      if args.path_experience_files == 'undefined':
          raise ValueError('You must specify --path_experience_files')
      if args.experience_name == 'undefined':
          raise ValueError('You must specify --experience_name')
      else:

          files_in = [args.path_control_files, args.path_experience_files]
          names_in = [args.control_name, args.experience_name]

    if args.pathwork == 'undefined':
        raise ValueError('You must specify --pathwork')
    if args.datestart == 'undefined':
        raise ValueError('You must specify --datestart')
    if args.dateend == 'undefined':
        raise ValueError('You must specify --dateend')
    if args.region == 'undefined':
        raise ValueError('You must specify --region')
    if args.family == 'undefined':
        raise ValueError('You must specify --family')
    if args.flags_criteria == 'undefined':
        raise ValueError('You must specify --flags_criteria')


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_cardio (files_in,
                          names_in,
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.id_stn,
                          args.channel,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()




