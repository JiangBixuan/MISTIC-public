import collections
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

# competitors = ['Eigen', 'PrimateAI', 'FATHMM-XF', 'ClinPred', 'REVEL', 'M-CAP', 'MISTIC']
competitors = ['InMeRF', 'ClinPred', 'REVEL', 'MISTIC']

def violin_plot_scores(dir, logger):
	logger.info('Plotting violin plots distribution')

	dict_names = {
		'ID': 'ID',
		'True_Label': 'True_Label',
		'M-CAP_flag': 'M-CAP',
		'ClinPred_flag': 'ClinPred',
		'REVEL_flag': 'REVEL',
		'PrimateAI_flag': 'PrimateAI',
		'Eigen-raw_coding_flag': 'Eigen',
		'fathmm-XF_coding_flag': 'FATHMM-XF',
		'VotingClassifier_proba': 'MISTIC',

	}

	y_dict = {
		'M-CAP': 0.025,
		'ClinPred': 0.5,
		'REVEL': 0.5,
		'PrimateAI': 0.803,
		'Eigen': 0,
		'FATHMM-XF': 0.5,
		'MISTIC': 0.5,
		'MISTIC_LR': 0.5,
		'GradientBoostingClassifier': 0.5,
		'LogisticRegression': 0.5,
		'RandomForestClassifier': 0.5,
		'MLPClassifier': 0.5,
		'GaussianNB': 0.5,

	}
	thresholds_sup = {
		"ClinPred": 0.298126307851977,
		"Eigen": -0.353569576359789,
		"M-CAP": 0.026337,
		"REVEL": 0.235,
		"FATHMM-XF": 0.22374,
		"PrimateAI": 0.358395427465,
		"MISTIC": 0.277,
		# "MISTIC"    :   0.198003954007379,
	}

	classifiers = ['Eigen', 'PrimateAI', 'FATHMM-XF', 'ClinPred', 'REVEL', 'M-CAP', 'MISTIC']

	pool_df_0 = pd.DataFrame()
	pool_df = pd.DataFrame()
	selected_columns = ['ID', 'True_Label', 'M-CAP_flag', 'ClinPred_flag', 'REVEL_flag', 'Eigen-raw_coding_flag',
	                    'fathmm-XF_coding_flag', 'PrimateAI_flag', 'VotingClassifier_proba']
	for d in tqdm(list(sorted(os.listdir(dir)))):
		if 'RESULTS_' in d and '_0_' not in d:
			tmp_df = pd.read_csv(dir + '/' + d + '/TEST/Complete_matrix_with_predictions.csv.gz', sep='\t',
			                     compression='gzip')
			tmp_df = tmp_df[selected_columns]
			pool_df = pd.concat([pool_df, tmp_df], axis=0)
		if 'RESULTS_' in d and '_0_' in d:
			tmp_df = pd.read_csv(dir + '/' + d + '/TEST/Complete_matrix_with_predictions.csv.gz', sep='\t',
			                     compression='gzip')
			tmp_df = tmp_df[selected_columns]
			pool_df_0 = pd.concat([pool_df, tmp_df], axis=0)

	pool_df['True_Label'] = pool_df['True_Label'].map({-1: 'Benign', 1: 'Pathogenic'})
	pool_df = pool_df[['ID', 'True_Label', 'M-CAP_flag', 'ClinPred_flag', 'REVEL_flag', 'Eigen-raw_coding_flag',
	                   'fathmm-XF_coding_flag', 'PrimateAI_flag', 'VotingClassifier_proba']]
	pool_df.rename(columns=dict_names, inplace=True)



	pool_df_0['True_Label'] = pool_df_0['True_Label'].map({-1: 'Benign', 1: 'Pathogenic'})
	pool_df_0 = pool_df_0[['ID', 'True_Label', 'M-CAP_flag', 'ClinPred_flag', 'REVEL_flag', 'Eigen-raw_coding_flag',
	                       'fathmm-XF_coding_flag', 'PrimateAI_flag']]
	pool_df_0.rename(columns=dict_names, inplace=True)

	# VIOLIN SCORES

	# SANS MAF

	fig, ax = plt.subplots(1, len(classifiers), figsize=(15, 12))

	for j, clf in enumerate(classifiers):
		tmp_df = pool_df_0[['True_Label', clf]]
		tmp_df = pd.melt(tmp_df, id_vars=['True_Label'], value_vars=[clf], var_name='Classifier', value_name='Score')
		tmp_df = tmp_df.sort_values(by='True_Label', ascending=False)
		sns.violinplot(x="Classifier", y="Score", hue='True_Label', data=tmp_df, palette=["#ff7675", "#55efc4"],
		               showfliers=True, linewidth=1.5, scale="width", split=True, cut=0.1, ax=ax[j], )

		ax[j].axhline(y=y_dict[clf], color='grey', linestyle='-', lw=3)
		ax[j].axhline(y=thresholds_sup[clf], color='#4bcffa', linestyle='-', lw=3)
		ax[j].get_legend().remove()
		ax[j].xaxis.set_tick_params(rotation=90, )
		ax[j].set_ylabel('')
		ax[j].set_xlabel('')
		ax[j].tick_params(labelsize=20)

	plt.subplots_adjust(wspace=1, bottom=0.2, top=0.95)

	plt.savefig(dir + '/PLOTS_AND_MEAN_TABLE/Score_distribution_MAF_0.png', dpi=600)

	plt.close()

	# WITH MAF

	fig, ax = plt.subplots(1, len(classifiers), figsize=(15, 12))

	# violin_df = pd.DataFrame()
	for j, clf in enumerate(classifiers):
		tmp_df = pool_df[['True_Label', clf]]
		tmp_df = pd.melt(tmp_df, id_vars=['True_Label'], value_vars=[clf], var_name='Classifier', value_name='Score')
		# violin_df = pd.concat([violin_df, tmp_df], axis=0)
		tmp_df = tmp_df.sort_values(by='True_Label', ascending=False)

		sns.violinplot(x="Classifier", y="Score", hue='True_Label', data=tmp_df, palette=["#ff7675", "#55efc4"],
		               showfliers=True, linewidth=1.5, scale="width", split=True, cut=0.1, ax=ax[j], )

		ax[j].axhline(y=y_dict[clf], color='grey', linestyle='-', lw=3)
		ax[j].axhline(y=thresholds_sup[clf], color='#4bcffa', linestyle='-', lw=3)
		ax[j].get_legend().remove()
		ax[j].xaxis.set_tick_params(rotation=90)
		ax[j].tick_params(labelsize=20)
		ax[j].set_ylabel('')
		ax[j].set_xlabel('')

	plt.subplots_adjust(wspace=1, bottom=0.2, top=0.95)

	plt.savefig(dir + '/PLOTS_AND_MEAN_TABLE/Score_distribution_WITH_MAF.png', dpi=600)

	plt.close()


def maf_plot_maf_0(dir, cv, logger):
	dict_names_0 = {
		'ID': 'ID',
		'True_Label': 'True_Label',
		'M-CAP_flag': 'M-CAP',
		'InMeRF_flag' : 'InMeRF',
		'ClinPred_flag': 'ClinPred',
		'REVEL_flag': 'REVEL',
		'PrimateAI_flag': 'PrimateAI',
		'Eigen-raw_coding_flag': 'Eigen',
		'fathmm-XF_coding_flag': 'FATHMM-XF',
		'VotingClassifier': 'MISTIC',
	}

	logger.info('Plotting results for variants without MAF ...')

	tmp_list = list()
	i = 0
	# reversed_competitors = ['Eigen', 'PrimateAI', 'FATHMM-XF', 'ClinPred', 'REVEL', 'M-CAP']
	reversed_competitors = ['InMeRF', 'ClinPred', 'REVEL', 'MISTIC']

	reversed_competitors.reverse()

	tmp_df_cv = pd.DataFrame()
	final_plot_df = pd.DataFrame()
	for d in list(sorted(os.listdir(dir))):
		if 'RESULTS_' in d and 'gnom' not in d and 'swiss' not in d:
			d = d.split('_')
			if d[-2] == '0':
				d = "_".join(d)
				tmp_name = d.replace('RESULTS_', '')
				tmp_name = tmp_name.replace('_filtered', '')
				tmp_name = tmp_name.replace('filtered_vep', '')
				tmp_name = tmp_name.replace('filter_', '')
				tmp_name = tmp_name.replace('_path', '')
				tmp_name = tmp_name.replace('_vep', '')
				tmp_name = tmp_name.split('_')
				combi_name = tmp_name[1]
				if 'clinvar' in tmp_name:
					combi_name = '_'.join(tmp_name[1:3])
					combi_name = combi_name.replace('clinvar_new', 'ClinVar_NEW')
				if 'Arabic' in combi_name:
					combi_name = combi_name.replace('Arabic', 'WesternAsia')
				df = pd.read_csv(dir + '/' + d + '/TEST/Classification_summary.csv', sep='\t')
				df.replace(dict_names_0, inplace=True)

				df = df.loc[df['Classifier'].isin(reversed_competitors)]
				tmp_df_cv = pd.concat([tmp_df_cv, df], axis=0)

				i += 1
				if i % cv == 0:
					tmp_plot_df = tmp_df_cv.copy()
					tmp_plot_df['Combination'] = combi_name
					final_plot_df = pd.concat([final_plot_df, tmp_plot_df], axis=0)
					tmp_d = dict()
					tmp_d['combi_name'] = combi_name
					combi_name = combi_name.replace('|', ' - ')
					tmp_group = tmp_df_cv.groupby(['Classifier'], as_index=False)
					tmp_std = pd.DataFrame()
					for gr in tmp_group:
						tmp_std = pd.concat([tmp_std, gr[1].groupby(['Classifier']).std()], axis=0)
					tmp_std.columns = ['STD ' + t for t in list(tmp_std.columns)]
					tmp_std = tmp_std.reset_index()
					tmp_std['Classifier'] = tmp_std['Classifier'].astype('category')
					tmp_std['Classifier'].cat.set_categories(reversed_competitors, inplace=True)
					combi_name = combi_name.split(' - ')
					combi_name = combi_name[1] + ' - ' + combi_name[0]
					combi_name = combi_name.lower()
					tmp_std.sort_values('Classifier').to_csv(
						dir + '/PLOTS_AND_MEAN_TABLE/std_results_' + str(combi_name) + '_specific.csv', sep='\t',
						index=False)

					tmp_df_cv = tmp_df_cv.groupby(['Classifier'], as_index=False).mean().sort_values(by='Classifier',
					                                                                                 ascending=False)

					tmp_df_cv.columns = ['Classifier'] + ['MEAN ' + t for t in list(tmp_df_cv.columns) if
					                                      'Classifier' not in t]
					tmp_d['df'] = tmp_df_cv
					tmp_df_cv['Classifier'] = tmp_df_cv['Classifier'].astype('category')
					tmp_df_cv['Classifier'].cat.set_categories(reversed_competitors, inplace=True)
					tmp_df_cv.sort_values('Classifier').to_csv(
						dir + '/PLOTS_AND_MEAN_TABLE/mean_results_' + str(combi_name) + '_specific.csv', sep='\t',
						index=False)
					tmp_list.append(tmp_d)
					tmp_df_cv = pd.DataFrame()

	complete_results = list()
	for file in list(sorted(os.listdir(dir + '/PLOTS_AND_MEAN_TABLE/'))):
		if 'mean' in file and 'specific' in file:
			file_df = pd.read_csv(dir + '/PLOTS_AND_MEAN_TABLE/' + file, sep='\t')
			file_df['Source'] = file
			complete_results.append(file_df)
	pd.concat(complete_results).to_csv(dir + '/PLOTS_AND_MEAN_TABLE/' + 'complete_results_specific.csv', sep='\t',
	                                   index=False)

	d = dict()
	scores = ['AUC Score', 'F1 Score', 'Log Loss']

	final_plot_df.replace(dict_names_0, inplace=True)
	final_plot_df = final_plot_df[['Classifier', 'Combination'] + scores]
	final_plot_df = final_plot_df[final_plot_df['Classifier'].isin(competitors)]

	final_df = final_plot_df

	sorter = ["ClinVar_NEW - uk10k", "DoCM - uk10k", "ClinVar_NEW - SweGen", "DoCM - SweGen",
	          "ClinVar_NEW - WesternAsia", "DoCM - WesternAsia", ]

	final_df.reset_index(drop=True, inplace=True)

	final_df['Combination'] = final_df['Combination'].str.replace('|', ' - ')
	final_df['Combination'] = final_df['Combination'].str.replace('Sweden', 'SweGen')
	final_df['Combination'] = final_df['Combination'].str.replace('Arabic', 'WesternAsia')
	final_df.Combination = final_df.Combination.astype('category')
	final_df.Combination.cat.set_categories(sorter, inplace=True)
	final_df.Classifier = final_df.Classifier.str.replace('-raw', '')
	final_df.Classifier = final_df.Classifier.astype('category')
	final_df.Classifier.cat.set_categories(competitors, inplace=True)
	final_df.sort_values(by=['Combination', 'Classifier'], inplace=True)

	sns.set(style="whitegrid")
	sns.set_context("paper")
	sns.set(font_scale=1.7)

	fig, ax = plt.subplots(1, 3, figsize=(18, 9))

	i = 0
	for score in scores:
		p = sns.pointplot(
			x='Combination',
			y=score,
			hue='Classifier',
			data=final_df,
			join=True,
			ax=ax[i],
			# markers=['o', "2", 'v', 's', 'X', '*', "D", "+"],
			scale=0.7,
			fontsize=20,
			# palette=sns.color_palette(["#0c2461", "#22a6b3", "#9b59b6", "#2196F3", "#4CAF50", "#FF9800", "#f44336"]),
			palette=sns.color_palette(["#FF9800", "#2196F3", "#4CAF50", "#f44336"]),
		)

		ax[i].grid(True)
		ax[i].get_legend().remove()
		if score != 'Log Loss':
			ax[i].set_ylim(ymax=1)

		ax[i].set_xlabel('')
		i += 1

	handles, labels = ax[i - 1].get_legend_handles_labels()
	for ax in fig.axes:
		matplotlib.pyplot.sca(ax)
		plt.xticks(rotation=90)
	fig.legend(handles, labels, ncol=1,
	           loc='center right',
	           title='Predictors',

	           )
	fig.suptitle('Population specific variants', fontsize=20, y=0.95)
	plt.subplots_adjust(wspace=0.35, bottom=0.45, right=0.8)

	plt.savefig(dir + '/PLOTS_AND_MEAN_TABLE/Specific - MAF_0.png', dpi=600)
	plt.close(fig)


def maf_plot_others(dir, cv, logger):
	# cv=5
	logger.info('Plotting results for variants with MAF ...')
	tmp_list = list()
	sec_list = list()

	dict_names_maf = {
		'ID': 'ID',
		'True_Label': 'True_Label',
		'M-CAP_flag': 'M-CAP',
		'InMeRF_flag' : 'InMeRF',
		'ClinPred_flag': 'ClinPred',
		'REVEL_flag': 'REVEL',
		'PrimateAI_flag': 'PrimateAI',
		'Eigen-raw_coding_flag': 'Eigen',
		'fathmm-XF_coding_flag': 'FATHMM-XF',
		# 'VotingClassifier': 'Voting Classifier',
		'VotingClassifier_lr_rf': 'MISTIC',
	}

	sorter = ["Singleton", "<0.0001", "<0.001", "<0.005", "<0.01"]

	i = 0
	tmp_df_cv = pd.DataFrame()

	maf_plot_dict = collections.defaultdict(pd.DataFrame)

	# reversed_competitors = ['Eigen', 'PrimateAI', 'FATHMM-XF', 'ClinPred', 'REVEL', 'M-CAP', 'Voting Classifier']
	reversed_competitors = ['InMeRF', 'ClinPred', 'REVEL', 'MISTIC']
	reversed_competitors.reverse()

	for d in list(sorted(os.listdir(dir))):
		if 'RESULTS_' in d and '_0_' not in d:
			d = d.split('_')
			if d[-2] != ('all.maf' or 0):
				d = "_".join(d)
				tmp_name = d.replace('RESULTS_', '')
				tmp_name = tmp_name.replace('_filtered', '')
				tmp_name = tmp_name.replace('filtered_vep', '')
				tmp_name = tmp_name.replace('filter_', '')
				tmp_name = tmp_name.replace('_path', '')
				tmp_name = tmp_name.replace('_vep', '')
				tmp_name = tmp_name.split('_')
				combi_name = tmp_name[1]
				if 'clinvar' in tmp_name:
					combi_name = '_'.join(tmp_name[1:3])
					combi_name = combi_name.replace('clinvar_new', 'ClinVar_NEW')
				if 'swissvar' in combi_name:
					combi_name = combi_name.replace('swissvar', 'SwissVar')
				maf = tmp_name[-2]
				df = pd.read_csv(dir + '/' + d + '/TEST/Classification_summary.csv', sep='\t')
				df.replace(dict_names_maf, inplace=True)
				print(df)
				df = df.loc[df['Classifier'].isin(reversed_competitors)]
				tmp_df_cv = pd.concat([tmp_df_cv, df], axis=0)
				i += 1
				if i % cv == 0:
					combi_name = combi_name.replace('|', ' - ')
					tmp_plot_df = tmp_df_cv.copy()
					if maf == 'AC1':
						maf = 'Singleton'
					else:
						maf = '<' + maf
					tmp_plot_df['Filter'] = maf
					maf_plot_dict[combi_name] = pd.concat([maf_plot_dict[combi_name], tmp_plot_df], axis=0)

					tmp_group = tmp_df_cv.groupby(['Classifier'], as_index=False)
					tmp_std = pd.DataFrame()
					for gr in tmp_group:
						tmp_std = pd.concat([tmp_std, gr[1].groupby(['Classifier']).std()], axis=0)
					tmp_std.columns = ['STD ' + t for t in list(tmp_std.columns)]
					tmp_std = tmp_std.reset_index()
					tmp_std.to_csv(dir + '/PLOTS_AND_MEAN_TABLE/std_results_' + str(combi_name) + '_' + maf + '.csv',
					               sep='\t', index=False)
					print(tmp_std)
					tmp_df_cv = tmp_df_cv.groupby(['Classifier'], as_index=False).mean().sort_values(by='AUC Score',
					                                                                                 ascending=False)

					tmp_d = dict()
					tmp_d['combi_name'] = combi_name
					tmp_d['maf'] = maf
					tmp_d['df'] = df

					tmp_df_cv['Classifier'] = tmp_df_cv['Classifier'].astype('category')
					tmp_df_cv['Classifier'].cat.set_categories(reversed_competitors, inplace=True)
					tmp_df_cv.sort_values('Classifier').to_csv(
						dir + '/PLOTS_AND_MEAN_TABLE/mean_results_' + str(combi_name) + '_' + maf + '.csv', sep='\t',
						index=False)

					sec_list.append(tmp_d)
					tmp_df_cv = pd.DataFrame()
					if i % (len(sorter) * cv) == 0:
						tmp_list.append(sec_list)
						sec_list = list()

	complete_results = list()
	for file in list(sorted(os.listdir(dir + '/PLOTS_AND_MEAN_TABLE/'))):
		if 'mean' in file and 'specific' not in file:
			file_df = pd.read_csv(dir + '/PLOTS_AND_MEAN_TABLE/' + file, sep='\t')
			file_df['Source'] = file.replace('mean_results_', '').split(' - ')[0]
			file_df['MAF'] = file.split('_')[-1].replace('.csv', '')
			complete_results.append(file_df)
	complete_results = pd.concat(complete_results)
	complete_results['MAF'] = complete_results['MAF'].astype('category')
	complete_results['MAF'].cat.set_categories(sorter, inplace=True)
	complete_results.sort_values(by=['Source', 'MAF'], inplace=True)
	complete_results.to_csv(dir + '/PLOTS_AND_MEAN_TABLE/' + 'complete_results_maf.csv', sep='\t', index=False)

	for l, subdict in tqdm(maf_plot_dict.items()):
		final_plot_df = subdict

		scores = ['AUC Score', 'F1 Score', 'Log Loss']

		final_plot_df.replace(dict_names_maf, inplace=True)

		final_plot_df = final_plot_df[['Classifier', 'Filter'] + scores]
		final_plot_df = final_plot_df[final_plot_df['Classifier'].isin(competitors)]
		final_df = final_plot_df

		final_df.reset_index(drop=True, inplace=True)
		final_df.Filter = final_df.Filter.astype('category')
		final_df.Filter.cat.set_categories(sorter, inplace=True)
		final_df.Classifier = final_df.Classifier.str.replace('-raw', '')
		final_df.Classifier = final_df.Classifier.astype('category')
		final_df.Classifier.cat.set_categories(competitors, inplace=True)
		final_df.sort_values(by=['Filter', 'Classifier'], inplace=True)

		sns.set(style="whitegrid")
		sns.set_context("paper")
		sns.set(font_scale=1.7)

		fig, ax = plt.subplots(1, 3, figsize=(18, 6))

		i = 0
		for score in scores:
			p = sns.pointplot(
				x='Filter',
				y=score,
				hue='Classifier',
				data=final_df,
				join=True,
				ax=ax[i],
				# markers=['o', "2", 'v', 's', 'X', '*', "D", "+"],
				scale=0.7,
				fontsize=20,
				# palette=sns.color_palette(["#0c2461", "#22a6b3", "#9b59b6", "#2196F3", "#4CAF50", "#FF9800", "#f44336"]),
				palette=sns.color_palette(["#FF9800", "#2196F3", "#4CAF50", "#f44336"]),
				)

			if score != 'Log Loss':
				ax[i].set_ylim(ymax=1)
			ax[i].grid(True)
			p.set_xlabel(score, fontsize=13)
			ax[i].get_legend().remove()

			ax[i].set_ylabel(score, fontsize=20)
			ax[i].set_xlabel('Minor Allele Frequency', fontsize=20)
			i += 1

		handles, labels = ax[i - 1].get_legend_handles_labels()
		fig.legend(handles, labels, ncol=1,
		           # bbox_to_anchor=(0.73, 0.97),
		           loc='center right',
		           title='Predictors',
		           )
		title = l
		title = title.replace('|', ' - ')
		title = title.replace('gnomAD', 'gnomAD_EvalSet')

		for ax in fig.axes:
			matplotlib.pyplot.sca(ax)
			plt.xticks(rotation=45)

		fig.suptitle(title, fontsize=20, y=0.95)
		plt.subplots_adjust(wspace=0.45, bottom=0.30, top=0.85, right=0.75)

		plt.savefig(dir + '/PLOTS_AND_MEAN_TABLE/' + title + '_maf_plot.png', dpi=600)
		plt.close(fig)


