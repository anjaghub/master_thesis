# The Interplay of Decision Agency, Outcome Value and Outcome Ownership When Interacting with Robots
## Data Wrangling for My Master Thesis Project

## 🌈 Project Description
My researach project sets up an online experiment that measures the conflict of participants when being situated in different kinds of decision-action scenarios together with robots. This repository is used to analyse the data of the online experiment. In the testing phase participants are asked to choose between two colorful boxes on the screen. The boxes are each associated with a different outcome value, one of the boxes means winning an amount of money while the second stands for losing money. The study setting further manipulates decision-making authority by varying whether the participants can make the choice themselves or whether the cooperating robot chooses, which then only has to be confirmed by the participant. 
Additionally, outcome ownership is manipulated by attributing the outcome value either to the participant herself or again to the cooperating robot. 
This means that the study varies three different variables all with two factors: the authority level in decision process (low and high agency), the outcome value (winning and losing) and the outcome ownership (self-attributed or attributed to non-human agent) ending in a total number of eight experimental settings. The data collection will happen as a within study design where all participants are faced with each of the eight experimental condition pairs.
The primary measure of interest is the participants' reaction time to the outcome attribution, which represents the degree of conflict they face with outcome of the action-decision situation. Additional questionnaires or specific question items may be integrated into the study design to assess factors such as personality traits or depression scales, which could potentially elucidate the research findings concerning self-agency.

## 🧬 Structure of this Repository
There are several files, solving different purposes:
1. The data_prep.py script wich prepares data for analysis by merging, renaming, deleting, etc...
2. The survey_data.py script to preproccess the data of the questionnaires in the beginning and end of the experiment
3. The data_check.py file which helped us understand the data before starting the testing; we checked distribution of our variables for counterbalancing and so on
4. Last but not least the analysis.ipynb script where the real collected data will be analysed
