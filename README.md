## Predictor Cal Poly Senior Project
The goal of this project is given a list of available developers and open issues
in a Github repository to predict which issue is best suited for each developer to 
work on next.

This project accomplishes this by data-mining the previous contributions by each
developer and finding patterns in what they other issues they have succesfully completed.
The idea is that someone who has worked on similar features in the past will 
complete the new issues more quickly and with fewer defects.

## Techniques 
This project uses a few different techniques to determine similarity between two texts:

1. Transform each text into a set of words and find how many words are shared between the texts
2. The Levenshtein edit distance between the texts
3. Cosine similarity between the raw texts
4. Cosine similarity between the texts after they have been stemmed and tokenized 

## Validation
The Statistics page steps through time to make a guess with only the data available
at the time that the issue was available to work on. It outputs the amount of correct 
guesses that it made and can give an indication of confidence for predicting the current
dataset. 

## Data Issues
Not all projects remeber to include the issue number in each pull request so many projects
are missing significant amounts of data that could help build the prediction model.

## Getting Started
This project uses vagrant for testing and developing

Change the secret key in predictor.wsgi
Change the MySQL password in the `vagrant/provision-app.sh` script
Change the GitHub user and password in the `views.py` file
Change the MySQL password in the `Database.py` file

Go to the vagrant folder and run:
`./prepare-vagrant.sh`
`vagrant up`

After the virtual machine is up:
`vagrant ssh`
Get the machines IP from `ifconfig`
Change the IP in `/etc/apache2/sites-available/Predictor.conf` from `127.0.0.1` to your IP
`sudo service apache2 restart`

Congrats, you are running the predictor

## Usage

### Import Project
Under this tab, you can import a project by its full Github name. IE: `bbeck13/RhythmRunner`
This step takes a long time for large projects

### Analyze Project
Under this tab, you can pick from available developers, and available issues and it will
produce in order the most relevent issues for the developer to work on.

### Generate CSV Data
This tab will produce a CSV file of the confidence ratings from each prediction model for each issue that
has already been completed.

### Statistics
This tab will produce the number of correct predictions the predictor has made on the project

### Delete Project
Delete the current project

### Switch Project
Switch between already imported projects

![screen shot 2017-03-15 at 12 27 55 am](https://cloud.githubusercontent.com/assets/2614746/23937934/3497efe0-0917-11e7-8f51-aeac5b38010d.png)
![screen shot 2017-03-15 at 12 28 16 am](https://cloud.githubusercontent.com/assets/2614746/23937935/34ada1d2-0917-11e7-86c6-806d1c556ad7.png)
![screen shot 2017-03-15 at 12 29 49 am](https://cloud.githubusercontent.com/assets/2614746/23937936/34af82e0-0917-11e7-9e97-ac9c0c3d5282.png)
