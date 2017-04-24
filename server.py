
from flask import Flask
from flask import render_template
import json
import csv
from flask import request
from config import files
from config import constants
from sampling import random_sample
from sampling import stratified_sample
from sampling import find_pca
from sampling import plot_elbow
from sklearn.metrics import euclidean_distances
from sklearn import metrics as SK_Metrics
from sklearn.metrics import pairwise
import numpy as np
from sampling import find_pca
from sklearn.decomposition import  PCA
from sklearn.manifold import MDS
import memcache
from sklearn import preprocessing

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/euclidean_template")
def euclidean_template():
    return render_template("euclidean.html")

@app.route("/correlation_template")
def correlation_template():
    return render_template("correlation.html")

@app.route("/intrinsic_template")
def intrinsic_template():
    return render_template("intrinsic.html")

@app.route("/scree_template")
def scree_template():
    return render_template("scree.html")

@app.route("/elbow_template")
def elbow_template():
    return render_template("elbow.html")


@app.route("/matrix_template")
def scatter_template():
    return render_template("scatter_matrix.html")

@app.route("/geo_template")
def geo_template():
    return render_template("geo_plot.html")

@app.route("/stacked_bars")
def stacked_bars():
    return render_template("stacked_bars.html")

def get_geo_vals():

    #Check if data is cached
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    if mc.get('random_samples') is not None:
        geo_vals = mc.get('geo_vals')

    return geo_vals


def get_samples():

    #Check if data is cached
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    if mc.get('random_samples') is not None:
        random_samples = mc.get('random_samples')
        stratified_samples = mc.get('stratified_samples')
        geo_vals = mc.get('geo_vals')
        
    else:
        geo_vals = {}
        
        row_list = []
        col_dict = {}
        with open(files.csv_file, 'rt') as f:
            reader = csv.reader(f)
            firstRow = next(reader)


            print(firstRow)


            for i,rowName in enumerate(firstRow[:-1]):
                col_dict[rowName] = []

            for row in reader:
                row_list.append(row[:-1])
                
                if row[20] not in geo_vals.keys():
                    geo_vals[row[20]] = {}
                    geo_vals[row[20]]["male"] = 0
                    geo_vals[row[20]]["female"] = 0
                    geo_vals[row[20]]["a1"] = 0
                    geo_vals[row[20]]["a2"] = 0
                    geo_vals[row[20]]["a3"] = 0



                if row[2] == '1':
                    geo_vals[row[20]]["male"] += 1
                elif row[2] == '2':
                    geo_vals[row[20]]["female"] += 1
                

                if int(row[3]) >= 18 and int(row[3]) <= 30:
                    geo_vals[row[20]]['a1'] += 1
                if int(row[3]) >= 31 and int(row[3]) <= 40:
                    geo_vals[row[20]]['a2'] += 1
                if int(row[3]) >= 42 and int(row[3]) <= 50:
                    geo_vals[row[20]]['a3'] += 1


                for i,rowName in enumerate(firstRow[:-1]):
                    col_dict[rowName].append(row[i])



        # Perform random sampling
        random_samples = random_sample(row_list, constants.sample_fraction*len(row_list))
        print("Random sampling - Num_sampled : "+str(len(random_samples)))


        print(random_samples[0])
        #Normalize data
        random_samples = preprocessing.scale(random_samples)


        print(random_samples[0])
        #Find optimal k value with elbow
        elbow_vals = plot_elbow(row_list)



        #Perform stratified sampling


        stratified_samples = stratified_sample(row_list)
        #Normalize data

        print("STTTTTTT")
        stratified_samples = preprocessing.scale(stratified_samples)

        print("STTTTTTT2")

        mc.set('first_row',firstRow)
        mc.set('random_samples',random_samples)
        mc.set('stratified_samples',stratified_samples)
        mc.set('elbow_vals',elbow_vals)
        mc.set('geo_vals',geo_vals)

    print(random_samples[0])
    return random_samples,stratified_samples

def get_pca_values():

    random_samples,stratified_samples = get_samples()

    # Get correlation matrix
    random_correlation_matrix =  np.corrcoef(random_samples,rowvar=False)
    stratified_correlation_matrix =  np.corrcoef(stratified_samples,rowvar=False)

    dict = {}
    pca =  PCA(n_components = 2)

    random_pca_values = pca.fit_transform(random_correlation_matrix)
    

    stratified_pca_values = pca.fit_transform(stratified_correlation_matrix)
    print(stratified_pca_values.shape)


    random_pca_values = np.dot(random_samples,random_pca_values)
    random_pca_values = np.array(random_pca_values,np.float32)
    random_pca_values = random_pca_values.tolist()


    stratified_pca_values = np.dot(stratified_samples,stratified_pca_values)
    stratified_pca_values = np.array(stratified_pca_values,np.float32)

    stratified_pca_values = stratified_pca_values.tolist()

    return random_pca_values,stratified_pca_values

@app.route("/pca_data")
def get_pca_data():

    dict = {}
    random_pca_values,stratified_pca_values = get_pca_values()

    dict['pca_random'] = random_pca_values
    dict['pca_stratified'] = stratified_pca_values

    print("sending data.....")
    return app.response_class(json.dumps(dict), content_type='application/json')



@app.route("/scree_data")
def get_scree_data():
  
    
    random_samples,stratified_samples = get_samples()
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    first_row = mc.get('first_row')

    random_correlation_matrix =  np.corrcoef(random_samples,rowvar=False)
    stratified_correlation_matrix =  np.corrcoef(stratified_samples,rowvar=False)

    pca =  PCA(n_components = 3)

    random_pca_values = pca.fit_transform(random_correlation_matrix)
    stratified_pca_values = pca.fit_transform(stratified_correlation_matrix)

    random_scree_values = np.square(random_pca_values)
    stratified_scree_values = np.square(stratified_pca_values)

    random_scree_values = np.sum(random_scree_values, axis=1)
    stratified_scree_values = np.sum(stratified_scree_values, axis=1)


    random_scree_values = np.array(random_scree_values,np.float32)
    random_scree_values = random_scree_values.tolist()

    stratified_scree_values = np.array(stratified_scree_values,np.float32)
    stratified_scree_values = stratified_scree_values.tolist()
    
    dict = {}
    dict['scree_random'] = random_scree_values
    dict['scree_stratified'] = stratified_scree_values
    dict['labels'] = first_row
    print("sending data.....")
    return app.response_class(json.dumps(dict), content_type='application/json')


@app.route("/euclidean_data")
def get_euclidean_data():
   
    dict = {}

    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    if mc.get('random_euclidean') is not None:
        random_euclidean_values = mc.get('random_euclidean')
        stratified_euclidean_values = mc.get('stratified_euclidean')

        
    else:
            random_pca_values,stratified_pca_values = get_pca_values()
            mds = MDS(n_components=2, dissimilarity='precomputed')
            random_euclidean_values = SK_Metrics.pairwise_distances(random_pca_values, metric = 'euclidean')
            stratified_euclidean_values = SK_Metrics.pairwise_distances(stratified_pca_values, metric = 'euclidean')

            random_euclidean_values = mds.fit_transform(random_euclidean_values)
            stratified_euclidean_values = mds.fit_transform(stratified_euclidean_values)

            random_euclidean_values = np.array(random_euclidean_values,np.float32)
            random_euclidean_values = random_euclidean_values.tolist()

            stratified_euclidean_values = np.array(stratified_euclidean_values,np.float32)
            stratified_euclidean_values = stratified_euclidean_values.tolist()
            mc.set('random_euclidean',random_euclidean_values)
            mc.set('stratified_euclidean',stratified_euclidean_values)

    dict['random_euclidean_vals'] = random_euclidean_values
    dict['stratified_euclidean_vals'] = stratified_euclidean_values


    print("sending data.....")
    return app.response_class(json.dumps(dict), content_type='application/json')



@app.route("/correlation_data")
def get_correlation_data():
    # Code from the previous section: Data preparation

    dict = {}
    
    # random_pca_values,stratified_pca_values = get_pca_values()
    random_pca_values,stratified_pca_values = get_samples()
    
    random_corr_values = SK_Metrics.pairwise_distances(random_pca_values, metric = 'correlation')
    stratified_corr_values = SK_Metrics.pairwise_distances(stratified_pca_values, metric = 'correlation')

    mds = MDS(n_components=2, dissimilarity='precomputed')
    
    random_corr_values = mds.fit_transform(random_corr_values)
    random_corr_values = np.array(random_corr_values,np.float32)
    random_corr_values = random_corr_values.tolist()


    stratified_corr_values = mds.fit_transform(stratified_corr_values)
    stratified_corr_values = np.array(stratified_corr_values,np.float32)
    stratified_corr_values = stratified_corr_values.tolist()
    
    dict['random_corr_vals'] = random_corr_values
    dict['stratified_corr_vals'] = stratified_corr_values
    print("sending data.....")

    return app.response_class(json.dumps(dict), content_type='application/json')

@app.route("/eigen_values")
def get_eigen_values():
    random_samples,stratified_samples = get_samples()

    dict = {}

    random_correlation_matrix =  np.corrcoef(random_samples,rowvar=False)
    random_eigen_vals,random_eigen_vector = np.linalg.eigh(random_correlation_matrix)
    random_eigen_values = np.array(random_eigen_vals,np.float32)
    random_eigen_vals = random_eigen_vals.tolist()

    dict['random_eigen_vals'] = random_eigen_vals

    stratified_correlation_matrix =  np.corrcoef(stratified_samples,rowvar=False)
    stratified_eigen_vals,stratified_eigen_vector = np.linalg.eigh(stratified_correlation_matrix)
    stratified_eigen_values = np.array(stratified_eigen_vals,np.float32)
    stratified_eigen_vals = stratified_eigen_vals.tolist()
    dict['stratified_eigen_vals'] = stratified_eigen_vals



    print("sending data.....")
    return app.response_class(json.dumps(dict), content_type='application/json')

@app.route("/elbow_data")
def get_elbow_data():

    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    elbow_points = mc.get('elbow_vals')

    dict = {}
    dict['elbow_vals'] = elbow_points

    return app.response_class(json.dumps(dict), content_type='application/json')

@app.route("/matrix_data")
def get_matrix_data():
      
    random_samples,stratified_samples = get_samples()
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    first_row = mc.get('first_row')

    random_samples = np.array(random_samples,np.float32)
    
    random_samples = random_samples.tolist()    
    
    stratified_samples = np.array(stratified_samples,np.float32)

    stratified_samples = stratified_samples.tolist()

    dict = {}
    dict['matrix_random'] = random_samples
    dict['matrix_stratified'] = stratified_samples

    dict['labels'] = first_row
    print("sending data.....")
    return app.response_class(json.dumps(dict), content_type='application/json')


@app.route("/postalData")
def getPostal():
    postal = request.args.get('val')
    dict = {}



    
    all_vals = get_geo_vals()
    # print(all_vals)    
    dict['res'] = all_vals[postal]

    return  app.response_class(json.dumps(dict), content_type='application/json')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
# 
