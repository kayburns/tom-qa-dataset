# ToM QA Dataset

This repository includes the code to generate data from our EMNLP 2018 paper "Evaluating Theory of Mind in Question Answering". You can read the paper [here](https://arxiv.org/abs/1808.09352).

You can find the dataset used in the paper in the directory `data`. To start running the code, jump to [getting started](https://github.com/kayburns/tom-qa-dataset/blob/master/README.md#getting-started).

## Motivation

We proposed a dataset to evaluate question-answering models with respect to their capacity to reason about beliefs. We took inspiration from theory-of-mind experiments in developmental psychology (for example, the Sally-Anne task); these experiments are designed to test whether children can understand beliefs of others, and also reason about inconsistent states of the world -- for example, when someone's belief is different from the reality of a situation.

## Details of the Dataset

The data consists of a set of 3 *task types* and 4 *question types*, creating 12 total scenarios. The tasks are grouped into stories, which are denoted by the numbering at the start of each line. Here is an example of each *task type*:

<img src=media/tom_task_types.png>

We use four *question types* for each task:
- **First-order belief**: Where will Sally look for the milk?
- **Second-order belief**: Where does Anne think that Sally searches for the milk?
- **Memory**: Where was the milk at the beginning?
- **Reality**: Where is the milk really?
         
The first two questions test a model's ability to reason about beliefs and second-order beliefs (beliefs about beliefs).
The reality and memory questions are used to confirm that a model's correct answer to the belief question is not due to chance, but because it has a correct understanding of the state of the world and the state of others' beliefs. 

Each split contains 1000 examples of each task-question combination: 12 000 examples total per split.

There are four versions of the dataset: `easy with noise`, `easy without noise`, `hard with noise`, and `hard without noise`. Noised datasets include a distractor sentence in the test and validation sets that occurs randomly with 10% probability. The easy dataset a single scenario per story, while the the hard dataset has mutliple. Path names for test and validation files are of the form `{tom or tom_easy}/world_large_nex_1000_{noise: 0 or 10}/{task type}_{question type}_{split}_test`. Training files are available in the same directories and have the name `qa21_task_AB_train.txt`.

The format of the data is similar to the [bAbi](https://research.fb.com/downloads/babi/) tasks. The bAbi dataset additionally labels which sentences in a story are relevant to the given question as *supporting sentences*. We do not use these supporting setences, so an arbitrary number (`1`) is added at the end of each question in our dataset to ensure that the formatting of our questions are consistent with that of bAbi. 

The participants in our stories can have different views of the state of the world. We allow models access to information about who has observed what actions: each sentence is followed by a series of IDs, indicating which agents in the story were present for that action. IDs are constant within stories but not across stories.

## Getting Started

### Data Generation

Data generation code is written in `python3` and requires `NumPy`.

Running the script `generate_tom.sh` will recreate the entire dataset. The data used in the paper is also available directly in the data folder. Note that because actors and objects are sampled randomly, the script and the data will differ slightly.

The data consists of a set of 3 task templates and 4 question types, creating 12 total task-question combinations. Several of these task-question scenarios are grouped into stories, which are delimited by the numbering prepended to each line.

In our dataset, it is assumed that the supporting sentence used to infer the answer to each question is unused, so a 1 is added at the end of each question.

- [ ] Add: why this supervision is useful
We do allow models access to information about who has observed what actions: each sentence is followed by a series of IDs, indicating which agents in the story were present for that action. IDs are constant within stories but not across stories.

### Training: MemN2N

Be sure to install the requirements
- Tensorflow 1.0
- GNU Parallel

Start training by running `run_tasks.sh`.
- [ ] TODO: rerun on cluster to make sure everything works properly

Analysis code is available in `tom_experiments.py`.
- [ ] TODO: add endpoints to generate plots from paper automatically

### Training: EntNet

Be sure to install the requirements.
- [ ] TODO: lua, torch, etc

- [ ] TODO: create script that automatically copies/formats data for EntNet

```
cd models/MemNN/EntNet-babi/
./format_tom_data.sh <-- TODO!
th main.lua -task 21
```

### Training: RelNet

- [ ] TODO: add details on training and eval
