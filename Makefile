all: reports/figures/ValoresNulos2016.pdf \
	data/cov_matrix_CH2016.csv

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
	rm --force --recursive reports/figures/*.pdf

format:
	black --line-length 100 *.py

data/ENIGH2016/viviendas.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2016/microdatos/enigh2016_ns_viviendas_csv.zip \
	--output data/ENIGH2016/vivienda.zip
	unzip -o data/ENIGH2016/vivienda.zip -d data/ENIGH2016

data/ENIGH2016/hogares.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2016/microdatos/enigh2016_ns_hogares_csv.zip \
	--output data/ENIGH2016/hogares.zip
	unzip data/ENIGH2016/hogares.zip -d data/ENIGH2016

data/ENIGH2016/concentradohogar.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2016/microdatos/enigh2016_ns_concentradohogar_csv.zip \
	--output data/ENIGH2016/concentradohogar.zip
	unzip -o data/ENIGH2016/concentradohogar.zip -d data/ENIGH2016

data/ENIGH2016/poblacion.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2016/microdatos/enigh2016_ns_poblacion_csv.zip \
	--output data/ENIGH2016/poblacion.zip
	unzip data/ENIGH2016/poblacion.zip -d data/ENIGH2016

data/ENIGH2018/viviendas.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2018/microdatos/enigh2018_ns_viviendas_csv.zip \
	--output data/ENIGH2018/viviendas.zip
	unzip -o data/ENIGH2018/viviendas.zip -d data/ENIGH2018

data/ENIGH2018/hogares.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2018/microdatos/enigh2018_ns_hogares_csv.zip \
	--output data/ENIGH2018/hogares.zip
	unzip data/ENIGH2018/hogares.zip -d data/ENIGH2018

data/ENIGH2018/concentradohogar.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2018/microdatos/enigh2018_ns_concentradohogar_csv.zip \
	--output data/ENIGH2018/concentradohogar.zip
	unzip -o data/ENIGH2018/concentradohogar.zip -d data/ENIGH2018

data/ENIGH2018/poblacion.csv:
	$(checkDirectories)
	curl https://www.inegi.org.mx/contenidos/programas/enigh/nc/2018/microdatos/enigh2018_ns_poblacion_csv.zip \
	--output data/ENIGH2018/poblacion.zip
	unzip data/ENIGH2018/poblacion.zip -d data/ENIGH2018

reports/figures/ValoresNulos2016.pdf reports/figures/ValoresNulosRemoval2016.pdf data/ENIGH2016_clean.csv: \
	data/ENIGH2016/viviendas.csv \
	data/ENIGH2016/hogares.csv \
	data/ENIGH2016/concentradohogar.csv \
	data/ENIGH2016/poblacion.csv
	$(checkDirectories)
	python data_cleaning.py

reports/figures/CH_NumPersonas2016.pdf data/ENIGH_CH2016.csv reports/figures/Energia_Corriente_Zscore.png reports/figures/Energia_Alfabetismo_Zscore.png reports/figures/Energia_Alfabetismo_Diferencias.png reports/figures/Energia_Alfabetismp_Diferencias_Zscore.png reports/figures/CovMatrix_Heatmap data/cov_matrix_CH2016.csv: \
	data/ENIGH2016_clean.csv
	$(checkDirectories)
	python data_classification.py

