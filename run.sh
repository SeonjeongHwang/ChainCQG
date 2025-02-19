#python data_preprocess.py --dataset-name coqa_two_gpt \
#                          --model-name gpt2 \
#                          --max-seq-length 512

CUDA_VISIBLE_DEVICES=1 python main_coqa_two_gpt.py --random-seed 1111 \
                                 --warmup-steps 100 \
                                 --learning-rate 1e-5 \
                                 --batch-size 1 \
                                 --gradient-accumulation-steps 1 \
                                 --num-train-epochs 10 \
                                 --do-train \
                                 --do-valid \
                                 --do-predict \
                                 --model-size small \
                                 --dataset-name coqa_two_gpt

#CUDA_VISIBLE_DEVICES=0 python main_coqa_two_gpt.py --batch-size 1 \
#                                                   --do-predict \
#                                                   --model-size small \
#                                                   --dataset-name coqa_two_gpt \
#                                                   --checkpoint-dir coqa_two_gpt_small_Checkpoint_3
