# VulPrompt

Repository for "VulPrompt: Prompt-based Vulnerability Detection using Few-shot Graph Learning" published in the proceedings of DBSec 2024. 

Abstract: Vulprompt is a new approach for detecting software vulnerabilities from source code by employing a prompt-based graph learning technique within a few-shot learning framework. Rather than adopting the \emph{Pretrain-Finetune} paradigm typical of prior works, it is the first to adopt the more recent \emph{Pretrain-Prompt} paradigm in this domain, which affords the creation of a smaller, lightweight model that outperforms larger models within other baseline methods. Evaluations conducted in a few-shot setting reflect the scarcity of large, high-quality labeled datasets for vulnerability detection in large software products---a prevalent issue in cybersecurity. Results show that the reduced number of trainable parameters for prompt-based learning models make them well-suited for this learning scenario, requiring only $n$ instances to train efficiently. The learnable prompt reduces the gap between the pretrain and downstream objectives for a particular task by adjusting the input data for the downstream task to fit the pretrained model. Comparative analyses between \sysname{} and other baseline methods demonstrate the model's robust performance across all datasets tested, consistently achieving notable results. 

![alt text](./proposedmethod.png?raw=true)



## Requirements
The packages used to run this repository along with their version numbers are mentioned in the `package versions.txt` file.

## Step 1: Convert code to graph:
First run the **json_to_c_convertor+normalizer.py** file using the data in the data.zip folder.
Next, run the **pdg_generator.py** file on the files generator by the previous script. This generates the pdgs using Joern. 
Finally run the **graph_data_reformatter.py** file on the output from the previous step. This reformats the pdgs into a format suitable for our pipeline. 

## Step 2: Generate .gml files for our data:
Run the **gml file extractor.py** file to get the .gml files necessary to run our program.

## Step 3: Train Vulprompt:
Run **pre_train.py** to pretrain the a GNN model. Then use **prompt_fewshot_gpf.py** to run the prompt tuning script. 


