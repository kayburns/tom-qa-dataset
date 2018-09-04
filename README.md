# ToM QA Dataset

This repository includes the code to generate data from our EMNLP 2018 Paper "Evaluating Theory of Mind in Question Answering". You can read the paper here: https://arxiv.org/abs/1808.09352

You can find the dataset used in the paper in the directory data. To start running the code jump to [getting started](https://github.com/kayburns/tom-qa-dataset/blob/master/README.md#getting-started).

## Motivation

We propose a dataset to evaluate question-answering models with respect to their capacity to reason about beliefs. We took inspiration from theory-of-mind experiments in developmental psychology (for example, the Sally-Anne task); these experiments are designed to test whether children can understand beliefs of others, and also represent inconsistent states of the world -- for example, when someone’s belief is different from the reality of a situation.

## Details of the Dataset

The data consists of a set of 3 task and 4 question types, creating 12 total tasks. The tasks are grouped into stories, which are denoted by the numbering at the start of each line. Here is an example of each task type:

<img src=media/tom_task_types.png>

We use for question types for each task:
- **First-order belief**: Where will Sally look for the milk?
- **Second-order belief**: Where does Anne think that Sally searches for the milk?
- **Memory**: Where was the milk at the beginning?
- **Reality**: Where is the milk really?
         
The first two question tests a model's ability to reason about beliefs and beliefs about beliefs.
The reality and memory questions are used to confirm that a model's correct answer to the belief question is not due to chance; but because it has a correct understanding of the state of world and others' beliefs. 


Add: Size of the training, test, and validation datasets.

The format of the data is inspired by the <a href=https://research.fb.com/downloads/babi/> bAbi </a> tasks. 

Add: what is the supporting sentence
In our dataset, it is assumed that the supporting sentence is unused, so a 1 is added at the end of each question. 

Add: why this supervision is useful
We do allow models access to information about who has observed what actions: each sentence is followed by a series of ids, indicating which agents in the story were present for that action. Ids are constant within stories but not across stories.

## Getting Started

Running the script `generate_tom.sh` will recreate the entire dataset. The data used in the paper is also available directly in the data folder. Note that because actors and objects are sampled randomly, the script and the data will differ slightly.

The data consists of a set of 3 story templates and 4 question types, creating 12 total tasks. The tasks are grouped into stories, which are denoted by the numbering at the start of each line.

Add: Size of the training, test, and validation datasets.

Add: what is the supporting sentence
In our dataset, it is assumed that the supporting sentence is unused, so a 1 is added at the end of each question. 

Add: why this supervision is useful
We do allow models access to information about who has observed what actions: each sentence is followed by a series of ids, indicating which agents in the story were present for that action. Ids are constant within stories but not across stories.
