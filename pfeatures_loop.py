import Pfeature
import pandas as pd
import os
import requests

#Assign the positive and negative files
pos_file_url = "https://raw.githubusercontent.com/dataprofessor/AMP/main/train_po.fasta"
negative_file_url = "https://raw.githubusercontent.com/dataprofessor/AMP/main/train_ne.fasta"

#Create a vairbale:filename dictionary
url_dict = {pos_file_url:'train_po.fasta', negative_file_url:'train_ne.fasta'}

#Loop through the variables in the dictionary and save the contents as filenames in the dictionary
for url, filename in url_dict.items():
  r = requests.get(url)
  with open (f'{filename}', 'wb') as f:
    f.write(r.content)
 
#Process the files with cd-hit
os.system("cd-hit -i train_po.fasta -o train_po_cdhit.txt -c 0.99")
os.system("cd-hit -i train_ne.fasta -o train_ne_cdhit.txt -c 0.99")

############### COPY AND PASTE THIS PART INTO THE NOTEBOOK BY CHANIN AT THE POINT OF PROCESSING THE FILES WITH PFEATURE (DON'T FORGET TO IMPORT Pfeature * ########################

#Create a dictionary of the functions and their names to iterate through so as to get the right description for looping through and automating the functions
pfeatures = {
      "aac": Pfeature.pfeature.aac_wp,
      "dpc":	Pfeature.pfeature.dpc_wp,
      "tpc":	Pfeature.pfeature.tpc_wp,
      "atc": Pfeature.pfeature.atc_wp, 
      "btc": Pfeature.pfeature.btc_wp,
      "pcp": Pfeature.pfeature.pcp_wp,
      "aai": Pfeature.pfeature.aai_wp,
      "rri": Pfeature.pfeature.rri_wp,
      "ddr": Pfeature.pfeature.ddr_wp,
      "pri": Pfeature.pfeature.pri_wp,
      "sep":Pfeature.pfeature.sep_wp,
      "ser":Pfeature.pfeature.ser_wp,
      "spc":Pfeature.pfeature.spc_wp,
      "acr":Pfeature.pfeature.acr_wp,
      "ctc":Pfeature.pfeature.ctc_wp,
      "ctd":Pfeature.pfeature.ctd_wp,
      "paac":Pfeature.pfeature.paac_wp,
      "apaac":Pfeature.pfeature.apaac_wp,
      "qos":Pfeature.pfeature.qos_wp,
      "soc":Pfeature.pfeature.soc_wp
}


# Create a dictionary of the training files to iterate through with the functions
train_files = {'train_po_cdhit.txt':'pos', 'train_ne_cdhit.txt':'neg'}

#empty list to append processed dataframes to
dataframes = []

#This loops through each function, and then each file for each function
for funcname,function in pfeatures.items(): 
  #pfeatures is a dictionary that contains the function name abbreviation, e.g 'dpc' as the key and the actual function from pfeatures as the value e.g Pfeature.pfeature.dpc_wp
  for filename, pclass in train_files.items():
    #train files is a dictionary that contains the filename as a key e.g 'train_po_cdhit.txt' and the value is it's classification e.g 'pos'
    train_file = filename.rstrip('.txt')
    #this strips the txt extension from the file and creates a new filename specifying the function name (funcname), the file processed (train_file) and the class (pos) with csv appended
    output = f'{funcname}_{train_file}_{pclass}.csv'

    #The following logic checks for the function name and calls the function slightly differently dependent on the arguments the functions take
    if funcname in ['dpc','acr']: # dpc and acr take in (filename, output, order). Change the order to figures desired
      order = 1
      df_out = function(filename,output, order)
    elif funcname in ['paac', 'apaac']: # paac and apaac take in (filename, output, lamba, weight). Change the lambda and weight to figures desired
      lamb_da = 1
      weight = 1
      df_out = function(filename, output, lamb_da, weight)
    elif funcname == 'qos': #qos takes in (filename, output, gap, weight). Change the gap and weight to figures desired
      gap = 1
      weight = 1
      df_out = function(filename, output, gap, weight)
    elif funcname == 'soc':# soc takes in (filename, output, gap). Change the gap to figures desired
      df_out = function(filename, output, gap) 
    else: # all the rest take in (filename, output)
      df_out = function(filename,output)
    df_in = pd.read_csv(output)
    #append to dataframes list if using in the same script/notebook
    dataframes.append(df_in)
    
    #Dataframes saved to folder and can be looped through to read them into another script.


