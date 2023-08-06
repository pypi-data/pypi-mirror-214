import warnings
warnings.simplefilter(action='ignore')

import os, sys, time, random
from loguru import logger

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

import scanpy as sc
import anndata as an

from pymoo.core.problem import Problem
from pymoo.core.sampling import Sampling
from pymoo.core.mutation import Mutation
from pymoo.core.repair import Repair

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.algorithms.moo.age2 import AGEMOEA2
from pymoo.algorithms.moo.sms import SMSEMOA

from pymoo.operators.crossover.expx import ExponentialCrossover
from pymoo.optimize import minimize

from sklearn.cluster import KMeans

import multiprocessing as mp

from _version import __version__

#************************************************************* Problem definition class *************************************************************
class ProblemDefinition(Problem):


	def __init__(self, max_genes, cl_of_interest, other_cls, alpha):
				
		self.__max_genes      = max_genes
		self.__cl_of_interest = cl_of_interest
		self.__other_cls      = other_cls
		self.__alpha          = alpha

		xl = -cl_of_interest.shape[1]
		xu = cl_of_interest.shape[1]
		
		super().__init__(n_var=self.__max_genes,
						 n_obj=2,
						 n_constr=2,
						 xl=xl,
						 xu=xu,
						 var_type=int)


	def __inner_fitness(self, set_positive, set_negative, cluster):

		selected  = cluster[:, set_positive].all(axis=1)
		discarded = np.logical_not(cluster[:, set_negative].any(axis=1))

		cells = np.where(np.logical_and(selected, discarded))[0]

		return len(cells)/len(cluster)


	def __fitness(self, set_positive, set_negative):

		if self.__alpha is None:
			value = self.__inner_fitness(set_positive, set_negative, self.__cl_of_interest) - \
					self.__inner_fitness(set_positive, set_negative, self.__other_cls)
		else:
			value = (1-self.__alpha)*self.__inner_fitness(set_positive, set_negative, self.__cl_of_interest) - \
					self.__alpha*self.__inner_fitness(set_positive, set_negative, self.__other_cls)
		
		return value
	

	def __extract_genes(self, individual):
		
		dictionary = {} 
			
		individual   = np.array(individual, dtype=np.int64)
		set_positive = individual[individual>0] - 1
		set_negative = np.absolute(individual[individual<0]) - 1
		
		dictionary["set_positive"] = set_positive
		dictionary["set_negative"] = set_negative

		return dictionary


	def _evaluate(self, X, out, *args, **kwargs):

		f1 = []
		f2 = []
		g1 = []
		g2 = []            

		for x in X:
			selected_genes = self.__extract_genes(x)
			
			set_positive = selected_genes["set_positive"]
			set_negative = selected_genes["set_negative"]
			
			n_positive   = len(set_positive>0)
			n_negative   = len(set_negative>0)

			f1.append(-1*self.__fitness(set_positive, set_negative))
			f2.append(n_positive + n_negative)
			g1.append(1-(n_positive+n_negative))
			g2.append(len(set(set_positive).intersection(set(set_negative))))

		f1 = np.array(f1)
		f2 = np.array(f2)       
		g1 = np.array(g1)
		g2 = np.array(g2)

		out["F"] = np.column_stack([f1,f2])
		out["G"] = np.column_stack([g1, g2])



#************************************************************* Sampling definition class ************************************************************
class SamplingDefinition(Sampling):


	def __init__(self, n_genes, max_genes):
		super().__init__()

		self.__n_genes   = n_genes
		self.__max_genes = max_genes


	def _do(self, problem, n_samples, **kwargs):
	
		X = np.full((n_samples, self.__max_genes), 0, dtype=np.int64)
		for i in range(n_samples):
			X[i] = np.sort(np.random.randint(-self.__n_genes, self.__n_genes+1, self.__max_genes))
				
		return X



#************************************************************* Mutation definition class ************************************************************
class MutationDefinition(Mutation):


	def __init__(self, n_genes, prob):
		super().__init__()

		self.__n_genes = n_genes
		self.__prob    = prob


	def _do(self, problem, X, **kwargs):

		do_mutation = np.random.random(X.shape) < self.__prob
		
		mutated = []
		for idx,x in enumerate(X[do_mutation]):
			choices = list(set(range(-self.__n_genes, self.__n_genes+1)).difference(set([x])))
			new_x = np.random.choice(choices)
			mutated.append(new_x)
		
		X[do_mutation] = mutated
		
		return X



#************************************************************** Repair definition class *************************************************************
class RepairDefinition(Repair):
	

	def __init__(self):
		super().__init__()
		

	def _do(self, problem, Z, **kwargs):
		
		Y = np.zeros(Z.shape, dtype=np.int64)
		for i in range(len(Z)):
			Y[i] = np.sort(Z[i])
		
		return Y



#**************************************************************** MAGNETO main class ****************************************************************
class MAGNETO(object):

	def __init__(self,
				 n_individuals=200,
				 n_generations=100,
				 cr=0.90,
				 mr=0.05,
				 outdir=".",
				 verbose=0):

		self.__n_individuals = n_individuals
		self.__n_generations = n_generations
		self.__cr            = cr
		self.__mr            = mr
		self.__outdir        = outdir
		self.__verbose       = verbose

		logger.add(os.path.join(self.__outdir,"magneto_{time}.log"), level="INFO")

		if n_individuals < 0:
			logger.warning("Warning! 'n_individuals' must be greater than 0, setting it to the default value (i.e., 200)")
			self.__n_individuals = 200

		if n_generations < 0:
			logger.warning("Warning! 'n_generations' must be greater than 0, setting it to the default value (i.e., 100)")
			self.__n_generations = 100

		if cr < 0 or cr > 1:
			logger.warning("Warning! 'cr' must be in the range [0, 1], setting it to the default value (i.e., 0.95)")
			self.__cr  = 0.95

		if mr is not None:
			if mr < 0 or mr > 1:
				logger.warning("Warning! 'mr' must be in the range [0, 1] or None, setting it to the default value (i.e., None)")
				self.__mr  = None            

	def __pct_cluter(self, set_positive, set_negative, cluster):

		selected  = cluster[:, set_positive].all(axis=1)
		discarded = np.logical_not(cluster[:, set_negative].any(axis=1))

		cells = np.where(np.logical_and(selected, discarded))[0]

		return len(cells)/len(cluster)


	def __generate_ranking(self, population, gene_expression, clusters, cl_of_interest, other_cls):

		results = {}
		
		dataframe = pd.DataFrame(index   = range(len(population)),
								 columns = ["Positive genes", "Negative genes", "F1", "F2"]+list(np.unique(clusters)))
		
		genes = np.array(gene_expression.columns)
		for i,idx in enumerate(population):

			individual = population[idx][2:][0]

			set_positive = individual[individual>0] - 1
			set_negative = np.absolute(individual[individual<0]) - 1

			n_positive   = len(set_positive>0)
			n_negative   = len(set_negative>0)

			f1 = self.__pct_cluter(set_positive, set_negative, cl_of_interest) - \
			     self.__pct_cluter(set_positive, set_negative, other_cls)
			
			f2 = n_positive + n_negative

			results = []
			for cl in np.unique(clusters):
				indeces = clusters[clusters == cl].index.tolist()
				cluster = np.array(gene_expression[gene_expression.index.isin(indeces)])
				results.append(100*self.__pct_cluter(set_positive, set_negative, cluster))

			positive_genes = ", ".join(list(genes[set_positive]))
			negative_genes = ", ".join(list(genes[set_negative]))

			values =  [positive_genes] + [negative_genes] + ["%5.2f"%f1] + ["%d"%f2] + ["%6.2f%%"%r for r in results]
			
			dataframe.iloc[i] = values

		return dataframe


	def __subset_genes(self, adata, list_genes):
	
		genes = adata.var.index.isin(list_genes)

		indeces = adata.obs.index
		columns = adata.var[genes].index
		data    = adata.X[:, genes]

		genes = adata.var.index.isin(list_genes)

		df = pd.DataFrame(index=indeces, columns=columns, data=data)

		adata1 = sc.AnnData(df)
		adata1.obs = adata.obs
		
		return adata1

	
	def __filter_genes(self, adata, path_genes):
		
		if type(path_genes) is str:
			if path_genes.split(".")[-1] == "txt":
				list_genes = np.genfromtxt(path_genes, dtype="str", delimiter="\n")
				adata = self.__subset_genes(adata, list_genes)   
				return adata
			
			else:
				logger.error("%s is a string but it is not a 'txt' file."%path_genes)
				# print(" * Error! %s is a string but it is not a 'txt' file"%path_genes)
				sys.exit(-6)
		
		elif type(path_genes) is list:
			adata = self.__subset_genes(adata, path_genes)
			return adata
		
		else:
			logger.error("'path_genes' must be a 'txt' file or a list object.")
			# print(" * Error! 'path_genes' must be a 'txt' file or a list object")
			sys.exit(-7)

	def __append_clusters(self, adata, clusters):
		
		clusters = clusters.rename(columns={clusters.columns[0]:"User annotation"})
		
		if len(set(adata.obs.index).difference(set(clusters.index))) != 0:

			if not set(clusters.index).issubset(set(adata.obs.index)):
				logger.error("The cell IDs in the cell annotation file must be equal to or a subset of the cell IDs of the gene expression matrix")
				sys.exit(-5)

			else:
				adata = adata[adata.obs.index.isin(clusters.index)]

		adata.obs = adata.obs.join(clusters)    
		
		return adata
		

	def __add_clusters(self, adata, path_clusters):
		
		if type(path_clusters) is str:
			splitted = path_clusters.split(".")[-1]
			if splitted in ["csv", "tsv"]:
				sep = ","
				if splitted == "tsv":
					sep = "\t"

				clusters = pd.read_csv(path_clusters, sep=sep).astype(str)
				clusters.set_index(clusters.columns[0], drop=True, inplace=True)
				clusters.index.name = None
				
				adata = self.__append_clusters(adata, clusters)
				return adata
			
			elif path_clusters in adata.obs.columns.tolist():
				adata.obs["User annotation"] = adata.obs[path_clusters]
				return adata

			else:
				logger.error("%s is a string but it is neither a 'csv' file, or 'tsv' file, or a valid column of '.obs' of the AnnData object"%path_clusters)
				#print(" * Error! %s is a string but it is neither a 'csv' file, or 'tsv' file, or a valid column of '.obs' of the AnnData object"%path_clusters)
				sys.exit(-3)
		
		elif type(path_clusters) is pd.core.frame.DataFrame:
			adata = self.__append_clusters(adata, path_clusters)
			return adata
		
		else:
			logger.error("'path_clusters' must be a pandas DataFrame, a 'csv' or 'tsv' file,, or a valid column of '.obs' of the AnnData object")
			# print(" * Error! 'path_clusters' must be a 'csv' or 'tsv' file, a pandas DataFrame, or a valid column of '.obs' of the AnnData object")
			sys.exit(-4)


	def __create_structure(self, path_data, path_clusters):

		if type(path_data) is str:
			
			splitted = path_data.split(".")[-1]
			
			if splitted == "h5ad":
				adata = sc.read_h5ad(path_data)
			
			elif splitted in ["csv", "tsv"]:
				sep = ","
				if splitted == "tsv":
					sep = "\t"
				
				data = pd.read_csv(path_data, sep=sep)
				data.set_index(data.columns[0], drop=True, inplace=True)
				data.index.name = None
				adata = sc.AnnData(data)
			
			else:
				logger.error("%s is a string but it is neither a 'csv' file, or 'tsv' file, or a 'h5ad' file"%path_data)
				# print(" * Error! %s is a string but it is neither a 'csv' file, or 'tsv' file, or a 'h5ad' file"%path_data)
				sys.exit(-2)
			
			adata = self.__add_clusters(adata, path_clusters)
			return adata

		elif type(path_data) is pd.core.frame.DataFrame:
			adata = sc.AnnData(path_data)
			adata = self.__add_clusters(adata, path_clusters)
			return adata

		elif type(path_data) is an._core.anndata.AnnData:
			adata = self.__add_clusters(path_data, path_clusters)
			return adata

		else:
			logger.error("'path_data' must be a pandas DataFrame, a 'h5ad', 'csv' or 'tsv' file, or a Scanpy (AnnData) object")
			# print(" * Error! 'path_data' must be a 'h5ad', 'csv' or 'tsv' file, or a Scanpy (AnnData) object")
			sys.exit(-1)
	
	def __solve(self, gene_expression, clusters, cl_of_interest):

		if self.__algorithm.upper() in ["NSGA2", "NSGA-2", "NSGAII", "NSGA-II"]:
			self.__algorithm = "NSGA2"
		
		elif self.__algorithm.upper() in ["AGEMOEA", "AGE-MOEA"]:
			self.__algorithm = "AGEMOEA"
		
		elif self.__algorithm.upper() in ["AGEMOEA2", "AGE-MOEA2"]:
			self.__algorithm = "AGEMOEA2"

		elif self.__algorithm.upper() in ["SMSEMOA", "SMS-EMOA"]:
			self.__algorithm = "SMSEMOA"
		
		else:
			logger.warning("'algorithm' must be equal to 'NSGA2', 'AGEMOEA', 'AGEMOEA2', or SMSEMOA setting it to the default value (i.e., 'AGEMOEA')")
			self.__algorithm = "AGEMOEA"

		if self.__max_genes < 0:
			logger.warning("'max_genes' must be greater than 0, setting it to the default value (i.e., 5)")
			self.__max_genes = 5

		if self.__alpha is not None:
			if self.__alpha < 0 or self.__alpha > 1:
				logger.warning("'alpha' must be in the range [0, 1] or None, setting it to the default value (i.e., 0.8)")
				self.__alpha = 0.8

		# Create the matrices cl_of_interest and other clusters
		indeces = clusters[clusters == cl_of_interest].index.tolist()
		C = np.array(gene_expression[gene_expression.index.isin(indeces)])

		indeces = clusters[clusters != cl_of_interest].index.tolist()
		S = np.array(gene_expression[gene_expression.index.isin(indeces)])

		if self.__verbose > 0:
			logger.info("There are %d cells in cluster '%s'"%(C.shape[0], cl_of_interest))
			logger.info("There are %d cells in the other clusters\n"%(S.shape[0]))

		self.__path_out = self.__outdir+os.sep+str(cl_of_interest)

		try:
			Path(self.__path_out).mkdir(parents=True, exist_ok=True) # python >= 3.5
		except:
			pass
		
		problem   = ProblemDefinition(self.__max_genes, C, S, self.__alpha)
		
		if self.__mr is None:
			self.__mr = 1.0 / problem.n_var
			
		sampling  = SamplingDefinition(C.shape[1], self.__max_genes)
		mutation  = MutationDefinition(C.shape[1], self.__mr)
		# crossover = get_crossover("int_exp", prob=self.__cr)
		crossover = ExponentialCrossover(prob=self.__cr)
		repair    = RepairDefinition()

		if self.__verbose > 0:
			if self.__alpha is not None:
				logger.info("Weighted fitness function (alpha=%5.2f)"%self.__alpha)

			if self.__seed is not None:
				logger.info("Setting seed to %d"%self.__seed)

			logger.info("Initialising MAGNETO settings ...")

			offset = max(5, len(str(self.__n_individuals)), len(str(self.__n_generations)), len(str(self.__max_genes)))

			logger.info("* {0:>{1}} individuals (n_individuals)".format(self.__n_individuals, offset))
			logger.info("* {0:>{1}} maximum number of generations (n_generations)".format(self.__n_generations, offset))
			logger.info("* {0:>{1}} crossover rate (cr)".format(self.__cr, offset+0.2))
			logger.info("* {0:>{1}} mutation rate (mr)".format(self.__mr, offset+0.2))
			logger.info("* {0:>{1}} allowed genes (max_genes)\n".format(self.__max_genes, offset))
		
		if self.__seed is not None:
			random.seed(self.__seed)
			np.random.seed(self.__seed)
			
		if self.__algorithm == "AGEMOEA2":
			algorithm = AGEMOEA2(pop_size=self.__n_individuals,
								 sampling=sampling,
								 crossover=crossover,
								 mutation=mutation,
								 repair=repair,
								 eliminate_duplicates=True)

		elif self.__algorithm == "AGEMOEA":
			algorithm = AGEMOEA(pop_size=self.__n_individuals,
								sampling=sampling,
								crossover=crossover,
								mutation=mutation,
								repair=repair,
								eliminate_duplicates=True)

		elif self.__algorithm == "SMSEMOA":
			algorithm = SMSEMOA(pop_size=self.__n_individuals,
								sampling=sampling,
								crossover=crossover,
								mutation=mutation,
								repair=repair,
								eliminate_duplicates=True)

		else:
			algorithm = NSGA2(pop_size=self.__n_individuals,
							  sampling=sampling,
							  crossover=crossover,
							  mutation=mutation,
							  repair=repair,
							  eliminate_duplicates=True)

		if self.__verbose > 0:
			if self.__repetition is not None:
				logger.info("Starting the optimization number %d using %s ...\n"%(self.__repetition, self.__algorithm))

			else:
				logger.info("Starting the optimization using %s ...\n"%self.__algorithm)

		result = minimize(problem,
						  algorithm,
						  ('n_gen', self.__n_generations),
						  seed=self.__seed,
						  save_history=True)
		
		if self.__verbose > 0:
			logger.info("Ranking the calculated panels ...")
		
		if self.__verbose > 0:
			logger.info("Retrieving the %d Pareto front solution(s) ..."%result.F.shape[0])

		population = {}
		for idx,fitnesses in enumerate(result.F):
			population[idx] = [-1*fitnesses[0], fitnesses[1], result.X[idx]] 
			
		population = dict(sorted(population.items(), key=lambda item: item[1][0], reverse=True))
		panels = self.__generate_ranking(population, gene_expression, clusters, C, S)

		if self.__verbose > 0:
			logger.info("Saving the results to: %s"%self.__path_out)

		if self.__repetition is None:
			if self.__alpha is None:
				path_csv = self.__path_out+os.sep+"%s_marker_panels.csv"%self.__algorithm
			else:
				path_csv = self.__path_out+os.sep+"%s_marker_panels_alpha=%.3f.csv"%(self.__algorithm, self.__alpha)
		else:
			if self.__alpha is None:
				path_csv = self.__path_out+os.sep+"%s_marker_panels_repetition%d.csv"%(self.__algorithm, self.__repetition)
			else:
				path_csv = self.__path_out+os.sep+"%s_marker_panels_repetition%d_alpha=%.3f.csv"%(self.__algorithm, self.__repetition, self.__alpha)
		
		
		panels.to_csv(path_csv, index=False)
				
		idx = panels.index[0]

		if self.__verbose > 1:
			S_BOLD = '\033[1m'
			E_BOLD = '\033[0m'

			logger.info("Analysing the best panel found for {0}{1}{2} ...".format(S_BOLD, cl_of_interest, E_BOLD))
			logger.info("Best F1: %s"%panels["F1"][idx])
			logger.info("Best set of positive genes: " + "|".join(panels["Positive genes"][idx].split(", ")))
			logger.info("Best set of negative genes: " + "|".join(panels["Negative genes"][idx].split(", ")))

			results = dict(zip(np.unique(clusters), panels[np.unique(clusters)].iloc[idx]))

			offset = max(list(map(len, clusters)))
			for r in sorted(results.items(), key=lambda item: item[1], reverse=True):
				if r[0] == cl_of_interest:
					logger.info("* Cluster {0}{1:>{2}}{3}: {4:>{5}} of cells express this combination of genes".format(S_BOLD, r[0], offset, E_BOLD, r[1], 4))
				else:
					logger.info("* Cluster {0:>{1}}: {2:>{3}} of cells express this combination of genes".format(r[0], offset, r[1], 4))


	def __iterativeKmeans(self, data_in, n_clusters=2):  
		
		data = np.array(data_in)    

		while n_clusters > 0:  
			data = np.reshape(data, (-1,1)) #reshape to array with one feature  

			clusters = pow(2, n_clusters) 
			kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data)   
			data = kmeans.cluster_centers_[kmeans.labels_] 
			n_clusters = n_clusters - 1  
		
		#binarize
		boolVal = kmeans.cluster_centers_[0,0] > kmeans.cluster_centers_[1,0] 
		centers = np.array([int(boolVal), int(not boolVal)])     

		result = pd.Series(index=data_in.index, data=centers[kmeans.labels_].tolist())

		return result

	def __read_parameters(self, adata=None, annotation=None, pos_genes=None, neg_genes=None, cluster=None):

		if adata is None:
			local_adata = self.__adata.copy()

			if annotation is None:
				annotation = "User annotation"
			
		else:
			local_adata = adata.copy()

		if adata is None:
			local_adata = self.__adata.copy()

			if annotation is None:
				annotation = "User annotation"
			
		else:
			local_adata = adata.copy()

		local_adata.obs[annotation] = local_adata.obs[annotation].astype("category")

		if pos_genes is None and neg_genes is None:

			if cluster is None:
				logger.error("Please provide a valid cluster or the lists of positive and negative genes.")
				sys.exit(-11)

			self.__path_out = self.__outdir+os.sep+str(cluster)

			if self.__repetition is None:
				if self.__alpha is None:
					path_csv = self.__path_out+os.sep+"%s_marker_panels.csv"%self.__algorithm
				else:
					path_csv = self.__path_out+os.sep+"%s_marker_panels_alpha=%.3f.csv"%(self.__algorithm, self.__alpha)
			else:
				if self.__alpha is None:
					path_csv = self.__path_out+os.sep+"%s_marker_panels_repetition%d.csv"%(self.__algorithm, self.__repetition)
				else:
					path_csv = self.__path_out+os.sep+"%s_marker_panels_repetition%d_alpha=%.3f.csv"%(self.__algorithm, self.__repetition, self.__alpha)
			
			
			df = pd.read_csv(path_csv)

			try:
				pos_genes = df.iloc[0][0].split(", ")
			except:
				pass

			try:
				neg_genes = df.iloc[0][1].split(", ")
			except:
				pass

		return local_adata, annotation, pos_genes, neg_genes


	def evaluate_panel(self, adata=None, annotation=None, pos_genes=None, neg_genes=None, cluster=None):

		local_adata, annotation, pos_genes, neg_genes = self.__read_parameters(adata, annotation, pos_genes, neg_genes, cluster)


		df = pd.DataFrame(index=local_adata.obs[annotation].cat.categories,
			              columns=["Positive genes", "Negative genes", "Marker panel"])

		cells  = local_adata.X[:, local_adata.var.index.isin(pos_genes)].all(axis=1)
		local_adata.obs["positive"] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, "positive"] = True
		local_adata.obs["positive"] = local_adata.obs["positive"].astype("category")

		cells  = local_adata.X[:, local_adata.var.index.isin(neg_genes)].any(axis=1)
		local_adata.obs["negative"] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, "negative"] = True
		local_adata.obs["negative"] = local_adata.obs["negative"].astype("category")

		selected  = local_adata.X[:, local_adata.var.index.isin(pos_genes)].all(axis=1)
		discarded = np.logical_not(local_adata.X[:, local_adata.var.index.isin(neg_genes)].any(axis=1))
		cells = np.where(np.logical_and(selected, discarded))[0]
		local_adata.obs["panel"] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, "panel"] = True
		local_adata.obs["panel"] = local_adata.obs["panel"].astype("category")

		for cl in local_adata.obs[annotation].cat.categories:

			subset = local_adata[local_adata.obs[annotation] == cl]

			try:
				values = subset.obs["positive"].value_counts()  
				df.loc[cl, "Positive genes"] = "%3.2f%%"%(100*values[True]/subset.n_obs)
			except:
				df.loc[cl, "Positive genes"] = "%3.2f%%"%(0)

			try:
				values = subset.obs["negative"].value_counts()
				df.loc[cl, "Negative genes"] = "%3.2f%%"%(100*values[True]/subset.n_obs)
			except:
				df.loc[cl, "Negative genes"] = "%3.2f%%"%(0)

			try:
				values = subset.obs["panel"].value_counts()
				df.loc[cl, "Marker panel"] = "%3.2f%%"%(100*values[True]/subset.n_obs)
			except:
				df.loc[cl, "Marker panel"] = "%3.2f%%"%(0)

		return df


	def plot_charts(self, cluster=None, adata=None, annotation=None, pos_genes=None, neg_genes=None, filename=None):

		local_adata, annotation, pos_genes, neg_genes = self.__read_parameters(adata, annotation, pos_genes, neg_genes, cluster)

		local_adata.obs[cluster] = "Others"
		indeces = local_adata[local_adata.obs[annotation] == cluster].obs.index
		local_adata.obs.loc[indeces, cluster] = cluster
		local_adata.obs[cluster] = local_adata.obs[cluster].astype("category")
		
		name_pos = "".join([g+"$^+$" for g in pos_genes])
		name_neg = "".join([g+"$^-$" for g in neg_genes])
		name_pan = "".join([g+"$^+$" for g in pos_genes] + [g+"$^-$" for g in neg_genes])

		cells  = local_adata.X[:, local_adata.var.index.isin(pos_genes)].all(axis=1)
		local_adata.obs[name_pos] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, name_pos] = True
		local_adata.obs[name_pos] = local_adata.obs[name_pos].astype("category")

		cells = local_adata.X[:, local_adata.var.index.isin(neg_genes)].any(axis=1)
		local_adata.obs[name_neg] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, name_neg] = True
		local_adata.obs[name_neg] = local_adata.obs[name_neg].astype("category")

		selected  = local_adata.X[:, local_adata.var.index.isin(pos_genes)].all(axis=1)
		discarded = np.logical_not(local_adata.X[:, local_adata.var.index.isin(neg_genes)].any(axis=1))
		cells = np.where(np.logical_and(selected, discarded))[0]
		local_adata.obs[name_pan] = False
		indeces = local_adata.obs.index[cells]
		local_adata.obs.loc[indeces, name_pan] = True
		local_adata.obs[name_pan] = local_adata.obs[name_pan].astype("category")

		f, axs = plt.subplots(2,3,figsize=(24,16))
		sns.despine(offset=10, trim=False)

		sns.set(font_scale=1.5)
		sns.set_style("white")

		values = local_adata[local_adata.obs[cluster] == cluster].obs[name_pos].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[0,0].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#800000", "#cecece"])
		m[0].set_color('white')
		axs[0,0].set_title(str(cluster) + " (" + name_pos + ")", y=0.96)

		values = local_adata[local_adata.obs[cluster] == cluster].obs[name_neg].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[0,1].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#03396c", "#cecece"])
		m[0].set_color('white')
		axs[0,1].set_title(str(cluster) + " (" + name_neg + ")", y=0.96)

		values = local_adata[local_adata.obs[cluster] == cluster].obs[name_pan].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[0,2].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#295f48", "#cecece"])
		m[0].set_color('white')
		axs[0,2].set_title(str(cluster) + " (" + name_pan + ")", y=0.96)


		values = local_adata[local_adata.obs[cluster] != cluster].obs[name_pos].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[1,0].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#800000", "#cecece"])
		m[0].set_color('white')
		axs[1,0].set_title("Others (" + name_pos + ")", y=0.96)

		values = local_adata[local_adata.obs[cluster] != cluster].obs[name_neg].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[1,1].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#03396c", "#cecece"])
		m[0].set_color('white')
		axs[1,1].set_title("Others (" + name_neg + ")", y=0.96)

		values = local_adata[local_adata.obs[cluster] != cluster].obs[name_pan].value_counts()
		labels = [True, False]
		sizes  = [values[l] for l in labels]
		_,_,m = axs[1,2].pie(sizes, labels=None, autopct='%1.1f%%', colors=["#295f48", "#cecece"])
		m[0].set_color('white')
		axs[1,2].set_title("Others (" + name_pan + ")", y=0.96)

		plt.tight_layout()
		plt.show()
		plt.close("All")

		if filename is not None:
			f.savefig(filename, bbox_inches='tight')


	def solve(self, path_data, path_clusters, cl_of_interest=None, list_genes=None, algorithm="AGEMOEA", max_genes=5, alpha=0.8,
		      binarization="Q1", theta=None, d_kmeans=None, parallel=True, repetition=None, seed=42):

		start = time.time()

		self.__algorithm      = algorithm
		self.__max_genes      = max_genes
		self.__alpha          = alpha
		self.__repetition     = repetition
		self.__seed           = seed

		self.__adata = self.__create_structure(path_data, path_clusters)

		if type(self.__adata) is int:
			logger.error("It is impossible to create a Scanpy (AnnData) object. Please check the log to identify the error.")
			# print(" * It is impossible to create a Scanpy (AnnData) object. Please check the log to identify the error.")
			sys.exit(-8)


		if list_genes is not None:
			self.__adata = self.__filter_genes(self.__adata, list_genes)

		if np.sum(self.__adata.X < 0) > 0:
			logger.error("There are negative values in the gene espression, please provide raw counts or normalized values")
			# print(" * Error! 'path_data' must be a 'h5ad', 'csv' or 'tsv' file, or a Scanpy (AnnData) object")
			sys.exit(-9)

		gene_expression = pd.DataFrame(index=self.__adata.obs.index, columns=self.__adata.var.index, data=self.__adata.X)

		# Binarization of the gene expression matrix
		if binarization not in ["Q1", "k-means", "threshold"]:
			logger.warning("Warning! %s' is not among the the implemented binarization strategies, which are 'Q1', 'k-means', 'threshold'. Setting it to the default one (i.e., 'Q1')"%binarization)
			# print("Warning! %s' is not among the the implemented binarization strategies, which are 'Q1', 'k-means', 'threshold'. Setting it to the default one (i.e., 'Q1')"%binarization)
			binarization = "Q1"

		if binarization == "Q1":
			gene_expression = gene_expression.copy()

			gene_expression = gene_expression > gene_expression.quantile(0.25, axis=0)
			gene_expression = gene_expression.astype(np.int64)

		elif binarization == "k-means":
			if d_kmeans is None:
				logger.warning("Warning! 'k-means' binarization strategy is selected but 'd_kmeans' is equal to None, setting it to the default value (i.e., 2)")
				# print("Warning! 'k-means' binarization strategy is selected but 'd_kmeans' is equal to None, setting it to the default value (i.e., 2)")
				d_kmeans = 2
			
			elif d_kmeans <= 0:
				logger.warning("Warning! 'k-means' binarization strategy is selected but 'd_kmeans' is negative, setting it to the default value (i.e., 2)")
				# print("Warning! 'k-means' binarization strategy is selected but 'd_kmeans' is negative, setting it to the default value (i.e., 2)")
				d_kmeans = 2

			gene_expression = gene_expression.apply(self.__iterativeKmeans, n_clusters=d_kmeans, axis=0)
			gene_expression = gene_expression.astype(np.int64)

		elif binarization == "threshold":

			if theta is None:
				logger.warning("Warning! 'threshold' binarization strategy is selected but 'theta' is equal to None, setting it to the default value (i.e., 0)")
				# print("Warning! 'threshold' binarization strategy is selected but 'theta' is equal to None, setting it to the default value (i.e., 0)")
				theta = 0.0
			
			elif theta < 0:
				logger.warning("Warning! 'threshold' binarization strategy is selected but 'theta' is negative, setting it to the default value (i.e., 0)")
				# print("Warning! 'threshold' binarization strategy is selected but 'theta' is negative, setting it to the default value (i.e., 0)")
				theta = 0.0

			gene_expression = (gene_expression > theta).astype(np.int64)

		clusters = self.__adata.obs["User annotation"]

		if cl_of_interest is None:

			import platform
			plt = platform.system()

			if plt == "Linux" and parallel:
				logger.info("Parallelization required! %s OS detected, parallelization activated..."%plt)
				logger.info("Starting MAGNETO using %s..."%self.__algorithm)

				jobs = []
				for cl in list(np.unique(clusters)):
					logger.info("Analysing cluster %s..."%cl)
					p = mp.Process(target=self.__solve, args=(gene_expression, clusters, cl,))
					jobs.append(p)
					p.start()				
				for proc in jobs:
					proc.join()

			else:
				logger.info("%s OS detected, parallelization deactivated..."%plt)
				logger.info("Starting MAGNETO using %s..."%self.__algorithm)

				for cl in list(np.unique(clusters)):
					logger.info("Analysing cluster %s..."%cl)
					self.__solve(gene_expression, clusters, cl)

		elif cl_of_interest in list(np.unique(clusters)):
			logger.info("Analysing cluster %s as required..."%cl_of_interest)
			self.__solve(gene_expression, clusters, cl_of_interest)

		else:
			logger.error("The provided 'cl_of_interest' is not a valid cluster.")
			logger.error("Provide either None or one cluster among the following: " + "|".join(list(np.unique(clusters))))
			sys.exit(-10)

		end = time.time()
		end_start = [end - start]

		logger.info("Elapsed time %5.2f seconds\n"%end_start[0])

		if self.__repetition is None:
			if self.__alpha is None:
				path_txt = self.__outdir+os.sep+"%s_time.txt"%self.__algorithm
			else:
				path_txt = self.__outdir+os.sep+"%s_time_alpha=%.3f.txt"%(self.__algorithm, self.__alpha)
		else:
			if self.__alpha is None:
				path_txt = self.__outdir+os.sep+"%s_time_repetition%d.txt"%(self.__algorithm, self.__repetition)
			else:
				path_txt = self.__outdir+os.sep+"%s_time_repetition%d_alpha=%.3f.txt"%(self.__algorithm, self.__repetition, self.__alpha)

		np.savetxt(path_txt, end_start)