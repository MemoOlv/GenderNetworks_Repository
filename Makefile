all: reports/figures/ValoresNulos2016.pdf \
	reports/figures/ValoresNulos2018.pdf \
	reports/figures/ValoresNulos2020.pdf \
	data/cov_matrix_CH2016.csv \
	data/cov_matrix_CH2018.csv \
	data/cov_matrix_CH2020.csv

.PHONY: \
		all \
		check \
		clean \
		format

define checkDirectories
mkdir --parents $(@D)
endef

check:
	black --check --line-length 100 *.py
	flake8 --max-line-length 100 *.py

clean:
	rm --force --recursive .*_cache
	rm --force --recursive data/ENIGH2016
	rm --force --recursive data/ENIGH2018
	rm --force --recursive data/ENIGH*.csv
	rm --force --recursive data/cov*.csv
	rm --force --recursive reports/figures/*.pdf
	rm --force --recursive reports/figures/*.png

format:
	black --line-length 100 *.py

define download_enigh_data_by_year =
	@echo "downloading $(2) data for the $(1) ENIGH"
	@echo "https://www.inegi.org.mx/contenidos/programas/enigh/nc/$(1)/microdatos/enigh$(1)_ns_$(2)_csv.zip"
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/$(1)/microdatos/enigh$(1)_ns_$(2)_csv.zip \
	--output data/ENIGH$(1)/$(2).zip
	unzip -o data/ENIGH$(1)/$(2).zip -d data/ENIGH$(1)
endef

data/ENIGH2016/viviendas.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2016","viviendas")

data/ENIGH2018/viviendas.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2018","viviendas")

data/ENIGH2020/viviendas.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2020","viviendas")

data/ENIGH2022/viviendas.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2022","viviendas")

data/ENIGH2016/hogares.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2016","hogares")

data/ENIGH2018/hogares.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2018","hogares")

data/ENIGH2020/hogares.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2020","hogares")

data/ENIGH2022/hogares.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2022","hogares")

data/ENIGH2016/concentradohogar.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2016","concentradohogar")

data/ENIGH2018/concentradohogar.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2018","concentradohogar")

data/ENIGH2020/concentradohogar.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2020","concentradohogar")

data/ENIGH2022/concentradohogar.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2022","concentradohogar")

data/ENIGH2016/poblacion.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2016","poblacion")

data/ENIGH2018/poblacion.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2018","poblacion")

data/ENIGH2020/poblacion.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2020","poblacion")

data/ENIGH2022/poblacion.csv:
	$(checkDirectories)
	@$(call download_enigh_data_by_year,"2022","poblacion")

reports/figures/ValoresNulos2016.pdf reports/figures/ValoresNulosRemoval2016.pdf data/ENIGH2016_clean.csv: \
	data/ENIGH2016/viviendas.csv \
	data/ENIGH2016/hogares.csv \
	data/ENIGH2016/concentradohogar.csv \
	data/ENIGH2016/poblacion.csv
	$(checkDirectories)
	python data_cleaning.py 2016

reports/figures/ValoresNulos2018.pdf reports/figures/ValoresNulosRemoval2018.pdf data/ENIGH2018_clean.csv: \
	data/ENIGH2018/viviendas.csv \
	data/ENIGH2018/hogares.csv \
	data/ENIGH2018/concentradohogar.csv \
	data/ENIGH2018/poblacion.csv
	$(checkDirectories)
	python data_cleaning.py 2018

reports/figures/ValoresNulos2020.pdf reports/figures/ValoresNulosRemoval2020.pdf data/ENIGH2020_clean.csv: \
	data/ENIGH2020/viviendas.csv \
	data/ENIGH2020/hogares.csv \
	data/ENIGH2020/concentradohogar.csv \
	data/ENIGH2020/poblacion.csv
	$(checkDirectories)
	python data_cleaning.py 2020

reports/figures/ValoresNulos2022.pdf reports/figures/ValoresNulosRemoval2022.pdf data/ENIGH2022_clean.csv: \
	data/ENIGH2022/viviendas.csv \
	data/ENIGH2022/hogares.csv \
	data/ENIGH2022/concentradohogar.csv \
	data/ENIGH2022/poblacion.csv
	$(checkDirectories)
	python data_cleaning.py 2022

reports/figures/CH_NumPersonas2016.pdf data/ENIGH_CH2016.csv reports/figures/Energia_Corriente_Zscore.png reports/figures/Energia_Alfabetismo_Zscore.png reports/figures/Energia_Alfabetismo_Diferencias.png reports/figures/Energia_Alfabetismo_Diferencias_Zscore.png reports/figures/CovMatrix_Heatmap2016.pdf data/cov_matrix_CH2016.csv: \
	data/ENIGH2016_clean.csv
	$(checkDirectories)
	python data_classification.py 2016

reports/figures/CH_NumPersonas2018.pdf data/ENIGH_CH2018.csv reports/figures/CovMatrix_Heatmap2018.pdf data/cov_matrix_CH2018.csv: \
	data/ENIGH2018_clean.csv
	$(checkDirectories)
	python data_classification.py 2018

reports/figures/CH_NumPersonas2020.pdf data/ENIGH_CH2020.csv reports/figures/CovMatrix_Heatmap2020.pdf data/cov_matrix_CH2020.csv: \
	data/ENIGH2020_clean.csv
	$(checkDirectories)
	python data_classification.py 2020

reports/figures/RepCov_HAdultos2016.pdf reports/figures/Representatividad_HAdultos2016.pdf reports/figures/Rep_Pob_Hogares2016.pdf reports/figures/CovMatrixCut2016.pdf data/cov_matrix_CH2016_cut.csv: \
	data/ENIGH2016_clean.csv \
	data/cov_matrix_CH2016.csv
	$(checkDirectories)
	python variable_selection.py 2016
