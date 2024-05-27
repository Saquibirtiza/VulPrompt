# VulPrompt

Repository for "VulPrompt: Prompt-based Vulnerability Detection using Few-shot Graph Learning" published in the proceedings of DBSec 2024. 

Abstract: Vulprompt is a new approach for detecting software vulnerabilities from source code by employing a prompt-based graph learning technique within a few-shot learning framework. Rather than adopting the \emph{Pretrain-Finetune} paradigm typical of prior works, it is the first to adopt the more recent \emph{Pretrain-Prompt} paradigm in this domain, which affords the creation of a smaller, lightweight model that outperforms larger models within other baseline methods. Evaluations conducted in a few-shot setting reflect the scarcity of large, high-quality labeled datasets for vulnerability detection in large software products---a prevalent issue in cybersecurity. Results show that the reduced number of trainable parameters for prompt-based learning models make them well-suited for this learning scenario, requiring only $n$ instances to train efficiently. The learnable prompt reduces the gap between the pretrain and downstream objectives for a particular task by adjusting the input data for the downstream task to fit the pretrained model. Comparative analyses between \sysname{} and other baseline methods demonstrate the model's robust performance across all datasets tested, consistently achieving notable results. 

![alt text](./proposedmethod.png?raw=true)

## Requirements
The packages used to run this repository along with their version numbers are mentioned in the `package versions.txt` file.

## Step 1: Convert code to graph:
First extract the data inside `data.zip` to get a json file containing information about the C code snippets. Then run the following scripts in this order to generate the corresponding pdgs for those snippets:

```
python json_to_c_convertor+normalizer.py
python pdg_generator.p
python graph_data_reformatter.py
```

The functionalities of the scripts are as follows:
* `json_to_c_convertor+normalizer.py` file converts the json file contained within the `data.zip` into individual .c files containing function-level code snippets. It also normalizes the .c files by removing any user defined function or variable names in the snippets. 
* `pdg_generator.py` file generates the pdgs using Joern. It works on the .c files extracted by the previous script. 
* `graph_data_reformatter.py` file reformats the pdgs into a format suitable for our pipeline. This gives us multiple files containing information such as the adjacency matrix, node labels, graph labels, etc. 

## Step 2: Generate .gml files for our data:
Run the `gml file extractor.py` file to get the .gml files necessary to run our program. Please make sure the input directory paths are changed accordingly before running. 

## Step 3: Train Vulprompt:
Run `pre_train.py` to pretrain the a GNN model. Then use **prompt_fewshot_gpf.py** to run the prompt tuning script. 


