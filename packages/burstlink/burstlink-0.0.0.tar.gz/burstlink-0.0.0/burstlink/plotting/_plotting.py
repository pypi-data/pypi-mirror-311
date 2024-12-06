# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import rpy2.robjects as ro

from _utils import _plotting


def network_visualization(counts_file, gene_interactions_file, burst_info_file, degree_data_file):
    r_script_path = "plotting/_network_plotting.R"
    ro.r.source(r_script_path)
    gene_umap = ro.globalenv['gene_umap']
    network_plot = ro.globalenv['network_plot']
    umap_df = gene_umap(counts_file)
    network_plot(gene_interactions_file, burst_info_file, degree_data_file, umap_df)
    return

def TFs_interactiontype_network(readfile_name):
    filtered_inference_result = filter_inference_results(readfile_name, [-3.5, 2.5, -2.5, 5.0])
    feedback_matrix__ = filtered_inference_result[:, np.array([0, 1, 23, 22])]
    unique_genename = sorted(list(set(np.asarray(np.vstack([filtered_inference_result[:, 0], filtered_inference_result[:, 1]])).flatten())))     
    feedback_matrix = np.zeros([len(unique_genename), len(unique_genename)]) - 10
    index = 0
    for genename in unique_genename:
        indices_ = np.where(feedback_matrix__[:, 0] == genename)[0]
        indices__ = np.where(np.isin(unique_genename, feedback_matrix__[indices_, 1]))[0]
        feedback_matrix[indices__, index] = 5 * np.array(feedback_matrix__[indices_, 2].astype(float)).flatten()
        feedback_matrix[index, indices__] = 5 * np.array(feedback_matrix__[indices_, 3].astype(float)).flatten()
        feedback_matrix[index, index] = - 10
        index = index + 1
    feedback_matrix_new = feedback_matrix.copy()
    for index in np.arange(len(unique_genename)):
        feedback_matrix_new[index, :] = sorted(feedback_matrix[index, :], reverse=True)
    feedback_matrix_new = np.hstack([np.arange(len(unique_genename)).reshape([len(unique_genename), 1]), feedback_matrix_new])
    sorted_feedback_matrix =  np.matrix(sorted(feedback_matrix_new.tolist(), key=lambda x: tuple(x[1::])))
    sorted_feedback_matrix_ = np.flipud(sorted_feedback_matrix)
    plt.figure(dpi=900)
    sns.heatmap(sorted_feedback_matrix_[:, 1::], annot=False, cmap=plt.cm.Blues, annot_kws={'size': 100}, linewidths=0.08, linecolor='w')
    plt.title('Inference GRN Heatmap')
    plt.show()
    return

def scatterplot_burst(readfile_name):
    filtered_inference_result = filter_inference_results(readfile_name, [-2.5, 3.0, -1.2, 2.5])
    bs = np.array(np.vstack([filtered_inference_result[:, 13], filtered_inference_result[:, 14]]).astype(float))
    bf = np.array(np.vstack([filtered_inference_result[:, 11], filtered_inference_result[:, 12]]).astype(float))
    cv2 = np.array(np.vstack([filtered_inference_result[:, 15], filtered_inference_result[:, 16]]).astype(float))
    expression_level = bs * bf
    fig, ax = plt.subplots(dpi=900)
    sc = plt.scatter(np.log10(bf), np.log10(bs), s=cv2*1.5, c=np.log10(expression_level), cmap=plt.cm.viridis)
    plt.colorbar(sc)
    plt.xlabel('log10(bf)', fontsize=17)
    plt.ylabel('log10(bs)', fontsize=17) 
    x = np.linspace(min(np.log10(bf)), max(np.log10(bf)), 100) 
    y = 0.3449 - x  
    ax.plot(x, y, color='red', linestyle='--', linewidth=2)
    plt.xlim([-2.8, 2.6]) 
    plt.ylim([-1.6, 2.6])               
    plt.show()
    return

def filter_inference_results(readfile_name, thresholds):
    inference_result_ = pd.read_csv(readfile_name)
    inference_result = np.matrix(inference_result_)[:, 1::]
    indices_infer = np.where(inference_result[:, 17].astype(float) == 0)[0]
    for index in np.arange(4):
        indices_ = np.where(inference_result[:, index+4].astype(float) == 1e-4)[0]
        indices__ = np.where(inference_result[:, index+4].astype(float) == 1e4)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+11].astype(float)) < thresholds[0])[0]
        indices__ = np.where(np.log10(inference_result[:, index+11].astype(float)) > thresholds[1])[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+13].astype(float)) < thresholds[2])[0]
        indices__ = np.where(np.log10(inference_result[:, index+13].astype(float)) > thresholds[3])[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    filtered_inference_result = np.delete(inference_result, indices_infer, axis = 0)
    return(filtered_inference_result)
