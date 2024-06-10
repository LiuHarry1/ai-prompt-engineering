# The link to access it 
https://ai-service-ui.apps.namicggtd51d.ecs.dyn.nsroot.net/examples

# Prerequiste to setup env locally 
1. Anaconda 
2. Python
3. Pycharm

# The steps of launch it locally 
## 1. create conda env with Anaconda Prompt
conda create --name aspen-prompt-engineering python=3.9
## 2. enter conda env you created
conda activate aspen-prompt-engineering
## 3. install all python package 
pip install -r requirements.txt


## launch llama2

cd C:\Users\Harry\PycharmProjects\llama.cpp

./server -m ./models/llama-2-7b-chat.Q4_0.gguf

or 
./main -m ./models/llama-2-7b-chat.Q4_0.gguf --color --ctx_size 2048 -n -1 -ins -b 256 --top_k 10000 --temp 0.2 --repeat_penalty 1.1 -t 8

./main -m ./models3/Meta-Llama-3-8B-Instruct.Q4_0.gguf --color --ctx_size 2048 -n -1 -ins -b 256 --top_k 10000 --temp 0.2 --repeat_penalty 1.1 -t 8


./main -m ./models3/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf --color --ctx_size 2048 -n -1 -ins -b 256 --top_k 10000 --temp 0.2 --repeat_penalty 1.1 -t 8

./server -m ./models3/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf -b 2256 --ctx_size 2048

server -m ./models3/Meta-Llama-3-8B-Instruct.Q4_0.gguf -b 2256 --ctx_size 2048


