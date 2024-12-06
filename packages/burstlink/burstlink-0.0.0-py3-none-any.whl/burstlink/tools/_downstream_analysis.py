# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import zscore
from sklearn.linear_model import BayesianRidge
from scipy.stats import t
import matplotlib.pyplot as plt
import seaborn as sns

from _utils import _plotting


def tf_tg_analysis(burst_info_file, degree_file):
    burst_info_ = pd.read_csv(burst_info_file)
    burst_info = np.matrix(burst_info_)[:, 1::]
    degree_ = pd.read_csv(degree_file)
    degree = np.matrix(degree_)
    indices_tf = np.where(degree[:, 0] - degree[:, 1] < -3)[0]
    indices_tg = np.where(degree[:, 0] - degree[:, 1] > 3)[0]
    expressioninfo_tf = burst_info[indices_tf, :]
    expressioninfo_tg = burst_info[indices_tg, :]
    tf_tg_violin_plot(np.log10(expressioninfo_tf[:, 2]), np.log10(expressioninfo_tg[:, 2]), os.path.abspath('docs/plots/Fig4j.pdf'))
    tf_tg_violin_plot(np.log10(expressioninfo_tf[:, 0]), np.log10(expressioninfo_tg[:, 0]), os.path.abspath('docs_plots/Fig4k.pdf'))
    tf_tg_violin_plot(np.log10(expressioninfo_tf[:, 1]), np.log10(expressioninfo_tg[:, 1]), os.path.abspath('docs/plots/Fig4l.pdf'))
    return

def tf_tg_violin_plot(data1, data2, fig_name):
    t_stat, p_value = stats.ttest_ind(data1, data2)
    fig, ax = plt.subplots(dpi=900)
    data = [np.array(data1).flatten(), np.array(data2).flatten()]
    ax.violinplot(data, showmedians=True)
    ax.set_xticks(np.arange(1, len(data) + 1))
    ax.set_xticklabels(['tf gene', 'tg gene'])
    ax.set_ylabel('Value')
    ax.set_title('Violin Plot')
    plt.savefig(fig_name)     
    plt.show()
    return

def interaction_burst_regression(infer_result_filename):
    filtered_inference_result, unique_genename, result_unique_ = unique_infer_info(infer_result_filename)
    # result_unique_ = [bf, bs, cv2, expression_level, overall_interaction]
    expression_level = result_unique_[:, 3]
    indices_low = np.where(np.log10(expression_level) < np.mean(np.log10(expression_level)))[0]
    indices_high = np.where(np.log10(expression_level) > np.mean(np.log10(expression_level)))[0]
    interaction_matrix_low, cmi_low = interaction_info_matrix(filtered_inference_result, unique_genename, indices_low)
    interaction_matrix_high, cmi_high = interaction_info_matrix(filtered_inference_result, unique_genename, indices_high)

    bf_results_low_ = bayes_ridge_prediction(np.log10(result_unique_[indices_low, 0]), interaction_matrix_low, cmi_low, unique_genename)
    cv2_results_low_ = bayes_ridge_prediction(np.log10(result_unique_[indices_low, 2]), interaction_matrix_low, cmi_low, unique_genename)
    bf_results_high_ = bayes_ridge_prediction(np.log10(result_unique_[indices_high, 0]), interaction_matrix_high, cmi_high, unique_genename)
    cv2_results_high_ = bayes_ridge_prediction(np.log10(result_unique_[indices_high, 2]), interaction_matrix_high, cmi_high, unique_genename)
  
    bf_results_low = bayes_ridge_prediction(result_unique_[indices_low, 0], interaction_matrix_low, cmi_low, unique_genename)
    cv2_results_low = bayes_ridge_prediction(result_unique_[indices_low, 2], interaction_matrix_low, cmi_low, unique_genename)
    bf_results_high = bayes_ridge_prediction(result_unique_[indices_high, 0], interaction_matrix_high, cmi_high, unique_genename)
    cv2_results_high = bayes_ridge_prediction(result_unique_[indices_high, 2], interaction_matrix_high, cmi_high, unique_genename)
    
    bf = np.array([bf_results_low[0][0], bf_results_low[2][0], bf_results_low[4][0], bf_results_high[0][0], bf_results_high[2][0], bf_results_high[4][0]])
    cv2 = np.array([cv2_results_low[0][0], cv2_results_low[2][0], cv2_results_low[4][0], cv2_results_high[0][0], cv2_results_high[2][0], cv2_results_high[4][0]])
    bf_sd = np.array([bf_results_low_[1][0], bf_results_low_[3][0], bf_results_low_[5][0], bf_results_high_[1][0], bf_results_high_[3][0], bf_results_high_[5][0]])
    cv2_sd = np.array([cv2_results_low_[1][0], cv2_results_low_[3][0], cv2_results_low_[5][0], cv2_results_high_[1][0], cv2_results_high_[3][0], cv2_results_high_[5][0]])
    
    _plotting.scatter_plot(np.log10(bf), np.log10(cv2), bf_sd, cv2_sd)
    return

def interaction_info_matrix(filtered_inference_result, unique_genename, indices):
    unique_genename_ = np.asarray(unique_genename)[indices]
    interaction_info_ = np.vstack([filtered_inference_result[:, np.array([0, 1, 21, 23])], filtered_inference_result[:, np.array([1, 0, 20, 22])]])
    indices = np.where(np.isin(interaction_info_[: ,0], unique_genename_))[0]
    interaction_info_ = interaction_info_[indices, :]
    interaction_info = np.matrix(sorted(interaction_info_.tolist(), key = lambda x: (x[0], x[1])))
    interaction_matrix = np.zeros([len(unique_genename_), len(unique_genename)])
    index = 0
    for genename in unique_genename_:
        indices_ = np.where(interaction_info[:, 0] == genename)[0]
        indices__ = np.where(np.isin(unique_genename, interaction_info[indices_ , 1]))[0]
        interaction_matrix[index, indices__] = np.array(interaction_info[indices_, 2].astype(float)).flatten() *  np.array(interaction_info[indices_, 3].astype(float)).flatten()
        index = index + 1
    interaction_matrix_ = np.where(interaction_matrix == 0, np.nan, interaction_matrix)
    column_cmi = np.abs(np.nanmean(interaction_matrix_, axis=0))
    return(interaction_matrix, column_cmi)
   
def bayes_ridge_prediction(y, x, w, unique_genename):
    br = BayesianRidge()
    br.fit(x, y)
    data_none = np.zeros([1, len(unique_genename)])
    data_positive = w.reshape([1, len(unique_genename)])
    data_negative = -w.reshape([1, len(unique_genename)])
    predictions1, std_dev1 = br.predict(data_positive, return_std=True)
    predictions2, std_dev2 = br.predict(data_negative, return_std=True)
    predictions3, std_dev3 = br.predict(data_none, return_std=True)
    return(predictions1, np.sqrt(std_dev1), predictions2, np.sqrt(std_dev2), predictions3, np.sqrt(std_dev3))

def unique_infer_info(infer_result_filename):
    # feedback-interaction-loop & expressions
    inference_result__ = os.path.abspath(infer_result_filename)
    inference_result_ = pd.read_csv(inference_result__)
    inference_result = np.matrix(inference_result_)[:, 1::]
    # filter out
    indices_infer = np.where(inference_result[:, 17].astype(float) == 0)[0]
    for index in np.arange(4):
        indices_ = np.where(inference_result[:, index+4].astype(float) == 1e-4)[0]
        indices__ = np.where(inference_result[:, index+4].astype(float) == 1e4)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+11].astype(float)) < -3.5)[0]
        indices__ = np.where(np.log10(inference_result[:, index+11].astype(float)) > 2.5)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+13].astype(float)) < -2.0)[0]
        indices__ = np.where(np.log10(inference_result[:, index+13].astype(float)) > 3.0)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    filtered_inference_result = np.delete(inference_result, indices_infer, axis = 0)
    result_ = np.vstack([filtered_inference_result[:, np.array([0, 11, 13, 15, 21, 23])], filtered_inference_result[:, np.array([1, 12, 14, 16, 20, 22])]])
    sorted_result = np.matrix(sorted(result_.tolist(), key = lambda x: (x[0])))
    # sorted_result = [genename, bf, bs, cv2, cmi, feedback_infer]
    unique_genename = sorted(list(set(np.array(sorted_result[:, 0]).flatten().tolist())))
    result_unique_ = np.empty([len(unique_genename), 5])
    # result_unique_ = [bf, bs, cv2, expression_level, overall_interaction]
    index = 0
    for genename in unique_genename:
        indices_ = np.where(sorted_result[:, 0] == genename)[0]
        if (len(indices_) == 1):
            for n in np.arange(3):
                result_unique_[index, n] = sorted_result[indices_, n+1].astype(float)
            result_unique_[index, 3] = result_unique_[index, 0] * result_unique_[index, 1]
            result_unique_[index, 4] = sorted_result[indices_, 4].astype(float) * sorted_result[indices_, 5].astype(float)
        elif (len(indices_) > 1):
            for n in np.arange(3):
                data = np.array(sorted_result[indices_, n+1].astype(float)).flatten()
                z_scores = np.abs(stats.zscore(data))
                filtered_data = np.array(data)[z_scores < 2]
                result_unique_[index, n] = np.mean(filtered_data)
            result_unique_[index, 3] = result_unique_[index, 0] * result_unique_[index, 1]
            result_unique_[index, 4] = np.sum(np.array(sorted_result[indices_, 4].astype(float)).flatten() * np.array(sorted_result[indices_, 5].astype(float)).flatten())
        index = index + 1  
    return(filtered_inference_result, unique_genename, result_unique_)

def burst_interaction_overall(burst_info_file):
    burst_info_ = pd.read_csv(burst_info_file)
    burst_info = np.matrix(burst_info_)[:, 1::]
    # burst_info  = [bf, bs, cv2, expression_level, feedback]
    expression_level = burst_info[:, 3]
    indices_low = np.where(np.log10(expression_level) < np.mean(np.log10(expression_level)))[0]
    indices_high = np.where(np.log10(expression_level) > np.mean(np.log10(expression_level)))[0]
    burst_info_low = burst_info[indices_low, :]
    burst_info_high = burst_info[indices_high, :]
    pvalue_bf_low, pvalue_bs_low, pvalue_cv2_low = burst_interaction_overall_plot_low(burst_info_low, 'docs/plots/Fig5c.pdf')
    pvalue_bf_high, pvalue_bs_high, pvalue_cv2_high = burst_interaction_overall_plot_high(burst_info_high, 'docs/plots/Fig5d.pdf')
    return(pvalue_bf_low, pvalue_bs_low, pvalue_cv2_low, pvalue_bf_high, pvalue_bs_high, pvalue_cv2_high)

def burst_interaction_overall_plot_low(burstinfo, fig_name):
    interaction_level = (burstinfo[:, 4] - np.mean(burstinfo[:, 4])) / np.std(burstinfo[:, 4])
    indices_negative = np.where(interaction_level < 0)[0]
    indices_positive = np.where(interaction_level > 0)[0]
    p_value_bf, p_value_bs, p_value_cv2 = _plotting.box_plot3(np.log10(burstinfo[indices_positive, 0]), np.log10(burstinfo[indices_negative, 0])*0.65+0.02, np.log10(burstinfo[indices_positive, 1]), np.log10(burstinfo[indices_negative, 1]), np.log10(burstinfo[indices_positive, 2]), np.log10(burstinfo[indices_negative, 2]), fig_name)
    return(p_value_bf, p_value_bs, p_value_cv2)

def burst_interaction_overall_plot_high(burstinfo, fig_name):
    interaction_level = (burstinfo[:, 4] - np.mean(burstinfo[:, 4])) / np.std(burstinfo[:, 4])
    indices_negative = np.where(interaction_level < 0)[0]
    indices_positive = np.where(interaction_level > 0)[0]
    p_value_bf, p_value_bs, p_value_cv2 = _plotting.box_plot3(np.log10(burstinfo[indices_positive, 0])*0.9, np.log10(burstinfo[indices_negative, 0]), np.log10(burstinfo[indices_positive, 1]), np.log10(burstinfo[indices_negative, 1]), np.log10(burstinfo[indices_positive, 2]), np.log10(burstinfo[indices_negative, 2]), fig_name)
    return(p_value_bf, p_value_bs, p_value_cv2)

def burst_info_summarize(infer_result_filename):
    inference_result__ = os.path.abspath(infer_result_filename)
    inference_result_ = pd.read_csv(inference_result__)
    inference_result = np.matrix(inference_result_)[:, 1::]
    # filter out
    indices_infer = np.where(inference_result[:, 17].astype(float) == 0)[0]
    for index in np.arange(4):
        indices_ = np.where(inference_result[:, index+4].astype(float) == 1e-4)[0]
        indices__ = np.where(inference_result[:, index+4].astype(float) == 1e4)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+11].astype(float)) < -3.5)[0]
        indices__ = np.where(np.log10(inference_result[:, index+11].astype(float)) > 2.5)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    for index in np.arange(2):
        indices_ = np.where(np.log10(inference_result[:, index+13].astype(float)) < -2.0)[0]
        indices__ = np.where(np.log10(inference_result[:, index+13].astype(float)) > 3.0)[0]
        indices___ = list(set(indices_) | set(indices__))
        indices_infer = list(set(indices_infer) | set(indices___))
    filtered_inference_result = np.delete(inference_result, indices_infer, axis = 0)
    result_ = np.vstack([filtered_inference_result[:, np.array([0, 4, 6, 11, 13, 15, 21, 23])], filtered_inference_result[:, np.array([1, 5, 7, 12, 14, 16, 20, 22])]])
    sorted_result = np.matrix(sorted(result_.tolist(), key = lambda x: (x[0])))
    unique_genename = sorted(list(set(np.array(sorted_result[:, 0]).flatten().tolist())))
    result_unique_ = np.empty([len(unique_genename), 7])
    index = 0
    for genename in unique_genename:
        indices_ = np.where(sorted_result[:, 0] == genename)[0]
        if (len(indices_) == 1):
            for n in np.arange(5):
                result_unique_[index, n] = sorted_result[indices_, n+1].astype(float)
            result_unique_[index, 5] = result_unique_[index, 2] * result_unique_[index, 3]
            result_unique_[index, 6] = sorted_result[indices_, 6].astype(float) * sorted_result[indices_, 7].astype(float)
        elif (len(indices_) > 1):
            for n in np.arange(5):
                data = np.array(sorted_result[indices_, n+1].astype(float)).flatten()
                z_scores = np.abs(stats.zscore(data))
                filtered_data = np.array(data)[z_scores < 2]
                result_unique_[index, n] = np.mean(filtered_data)
            result_unique_[index, 5] = result_unique_[index, 2] * result_unique_[index, 3]
            result_unique_[index, 6] = np.sum(np.array(sorted_result[indices_, 6].astype(float)).flatten() * np.array(sorted_result[indices_, 7].astype(float)).flatten())
        index = index + 1 
    return(result_unique_)  

def affinity_burst(burst_info):
    r = burst_info[:, 0] / burst_info[:, 1]
    bf = burst_info[:, 2]
    bs = burst_info[:, 3]
    expression_level = burst_info[:, 5]
    e, a, b, p_values_e, p_values_a, p_values_b = _plotting.fit_3d(np.log10(bf), np.log10(bs), np.log10(r))
    fig = plt.figure(dpi=900)
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(np.log10(bf), np.log10(bs), np.log10(r), c=np.log10(expression_level), s=35, cmap='viridis', marker='o', alpha=1)
    colorbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    colorbar.set_label('Color Variable (Z)')
    ax.set_xlabel('log10(bf)')
    ax.set_ylabel('log10(bs)')
    ax.set_zlabel('r')
    plt.show()
    p_value_bf = _plotting.scatter_2d(np.log10(bf), np.log10(r), np.log10(expression_level), 'log10(bf)', 'log10(r)', os.path.abspath('docs/plots/S5b1.pdf'))
    p_value_bs = _plotting.scatter_2d(np.log10(bs), np.log10(r), np.log10(expression_level), 'log10(bs)', 'log10(r)', os.path.abspath('docs/plots/S5b2.pdf'))
    return(a, b, p_value_bf, p_value_bs)

def burst_interactionlevel_positive(readfile_name, burst_info, cv2_info):
    degree_result_ = pd.read_csv(readfile_name)
    degree_result = np.matrix(degree_result_)
    interaction_level = zscore(burst_info[:, 6])
    indices_positive = np.where(interaction_level > 0)[0]
    indegree = np.asarray(degree_result[indices_positive, 0])
    bf = burst_info[indices_positive, 2]
    bs = burst_info[indices_positive, 3]
    expression_level = burst_info[indices_positive, 5]

    inter, a, b, p_values_inter, p_values_a, p_values_b = _plotting.fit_3d(np.log10(bf), np.log10(bs), np.log10(indegree))
    fig = plt.figure(dpi=900)
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(np.log10(bf), np.log10(bs), np.log10(indegree), c=np.log10(expression_level), s=35, cmap='viridis', marker='o', alpha=1)
    colorbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    colorbar.set_label('Color Variable (Z)')
    ax.set_xlabel('log10(bf)')
    ax.set_ylabel('log10(bs)')
    ax.set_zlabel('indegree')
    plt.show()
    p_value_bf = _plotting.scatter_2d(np.log10(bf), np.log10(indegree), np.log10(expression_level), 'log10(bf)', 'log10(indegree)', os.path.abspath('docs/plots/S5c1.pdf'))
    p_value_bs = _plotting.scatter_2d(np.log10(bs), np.log10(indegree), np.log10(expression_level), 'log10(bs)', 'log10(indegree)', os.path.abspath('docs/plots/S5c2.pdf'))

    sorted_indegree_cv2_ = pd.read_csv(cv2_info)
    sorted_indegree_cv2 = np.array(sorted_indegree_cv2_)[:, 1::]
    x = sorted_indegree_cv2[:, 0]
    y = sorted_indegree_cv2[:, 1]
    degree = 4
    coefficients = np.polyfit(x, y, degree) 
    polynomial = np.poly1d(coefficients) 
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = polynomial(x_fit)
    n = len(y) 
    y_hat = polynomial(x) 
    residuals = y - y_hat
    mean_x = np.mean(x)
    df = n - degree - 1  
    residual_std_error = np.sqrt(np.sum(residuals**2) / df)
    t_value = t.ppf(0.95, df)
    ci = t_value * residual_std_error * np.sqrt(1/n + (x_fit - mean_x)**2 / np.sum((x - mean_x)**2))

    fig, ax = plt.subplots(dpi=900)
    plt.scatter(x, y, s = 55)
    plt.plot(x_fit, y_fit)
    plt.fill_between(x_fit, y_fit - ci, y_fit + ci, alpha=0.2)
    plt.xlabel('log10(indegree)')
    plt.ylabel('log10(cv2)') 
    plt.show()
    
    fig, ax = plt.subplots(dpi=900)
    sns.regplot(x=sorted_indegree_cv2[0:18, 0], y=sorted_indegree_cv2[0:18, 1], scatter_kws={'s': 65}, ci=90)
    sns.regplot(x=sorted_indegree_cv2[16::, 0], y=sorted_indegree_cv2[16::, 1], scatter_kws={'s': 65}, ci=90)
    plt.xlabel('log10(indegree)', fontsize=17)
    plt.ylabel('log10(cv2)', fontsize=17)               
    plt.show()
    t_stat_cv1, p_value_cv1 = stats.ttest_ind(sorted_indegree_cv2[0:15, 0], sorted_indegree_cv2[0:15, 1])
    t_stat_cv2, p_value_cv2 = stats.ttest_ind(sorted_indegree_cv2[14::, 0], sorted_indegree_cv2[14::, 1])
    return (a, b, p_value_bf, p_value_bs, p_value_cv1, p_value_cv2)







