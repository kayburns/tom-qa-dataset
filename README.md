# python-bAbi-tasks

This repository includes the code to generate data from our EMNLP Paper Evaluating Theory of Mind in Question Answering (link coming soon).

## Getting Started

Running the script `generate_tom.sh` will recreate the entire dataset. The data used in the paper is also available directly in the data folder. Note that because actors and objects are sampled randomly, the script and the data will differ slightly.

## Details of the Dataset

The data consists of a set of 3 story templates and 4 question types, creating 12 total tasks. The tasks are grouped into stories, which are denoted by the numbering at the start of each line.

The format of the data is adopted from the original bAbi[https://research.fb.com/downloads/babi/] tasks. In our dataset, it is assumed that the supporting sentence is unused, so a 1 is added at the end of each question. We do allow models access to information about who has observed what actions: each sentence is followed by a series of ids, indicating which agents in the story were present for that action. Ids are constant within stories but not across stories.
