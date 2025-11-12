1- Here the main app for Data cleaning is app.py . When you run it, it uses the configuration that has been defined at config.json and executes the type of data cleaning you want. It is possible to arrange the settings and adjust the feature you want to by changing the configurations in config.ini.

After the program is run, new data is created in data/output/ called cleaned data. Additionally, the data profiling has been created before and after cleaning in dataprofiles folder

2- logging.ini, Config.py and config.json are configuration files. These files are implemented in datacleaner.py, which is the main file that executes datacleaning.

3- datacleaner.py is the main function that cleanes the data. Here different type of NA handle options,  feature removal or duplicate removal option can be seen depending on client needs. It choses feature name and type of data handling defined in config.json, therefore depending on the type of operation and the data set given by client, one can only change the config.json and clean any type of data.