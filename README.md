Hi! Here is my version of the Turmerik ML/SWE take-home coding assignment. 

Disclaimer: I used a very small sample size for the final output due to the large amount of time
it takes for each call to the OpenAI API. The final patient_trial_matches.csv file only considers 
5 patients and 8 trials for the sake of time. 

Brainstorm process:

First, I knew I had to get the data into readable files, so I knew I needed to scrape data off
of the clinical trials website. After obtaining this information, I also knew I needed patient 
data to use with the trial data, so I merged various pieces of data from each csv file in the 
datasets to create one master set with all of each patient's attributes. I will say that the 
datasets I downloaded appeared to be of low quality, with corrupted data in some places, mismatched
columns and rows, and some were shorter or longer than others, making it hard to analyze data
efficiently. As such, some of the data I used is actually not matched up properly, but for the sake
of time I used it as an arbitrary dataset just for the demonstration of the code. 

After obtaining the data, I decided to use the OpenAI API because of its simplicity and easy 
accessibility to analyze this data, taking inspiration from a provided research paper recommending 
the use of LLMs to match patients. Finally, after matching the patients with their prospective trials,
I generated an xlsx file as per the assignment instructions and also added an extra program to convert this 
into a csv file. 


SETUP AND USAGE INSTRUCTIONS:

First, download the repository. 
Make sure you have your own OpenAI API key, and make sure you have pandas installed. If not, use pip install
pandas in the terminal. 

Then, run ScrapeClinicalTrials.py, adjusting line 27 (for i in range(1)) to whatever suits your purposes, where
this for loop describes how many pages you will scrape for data. After running this program, you will have your
clinical_trials.csv file. 

Now, run CleanData.py, where you similarly adjust the value of rows and i >= (some number) on lines 7, 22, 49, 
65, 81, and 99. MAKE SURE ALL OF THESE VALUES ARE THE SAME. 

Once you have both sets of data, run Clinical_Trials_Matching.py, where on line 7 you replace the placeholder
statement YOUR-OWN-KEY with your actual OpenAI API key. 

This will output an xlsx file, which may already suit your purposes. However, in case you want the data in a 
different format, I included a small program named OutputToCSV.py, where you can convert this file into a csv
file. 

Have fun matching patients to trials!