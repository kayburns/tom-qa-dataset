# ToM QA Dataset

This repository includes the code to generate data from our EMNLP Paper "Evaluating Theory of Mind in Question Answering" (link coming soon).

## Getting Started

Running the script `generate_tom.sh` will recreate the entire dataset. The data used in the paper is also available directly in the data folder. Note that because actors and objects are sampled randomly, the script and the data will differ slightly.

## Details of the Dataset

Add: intro about the goal of the templates and question types -- what is the dataset evaluating?

The data consists of a set of 3 story templates and 4 question types, creating 12 total tasks. The tasks are grouped into stories, which are denoted by the numbering at the start of each line.

Add: Size of the training, test, and validation datasets.

The format of the data is inspired by the original bAbi[https://research.fb.com/downloads/babi/] tasks. 

Add: what is the supporting sentence
In our dataset, it is assumed that the supporting sentence is unused, so a 1 is added at the end of each question. 

Add: why this supervision is useful
We do allow models access to information about who has observed what actions: each sentence is followed by a series of ids, indicating which agents in the story were present for that action. Ids are constant within stories but not across stories.
