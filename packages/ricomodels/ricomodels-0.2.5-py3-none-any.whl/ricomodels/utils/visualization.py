#! /usr/bin/env python3

import gc
import os
import shutil
import time

import matplotlib.pyplot as plt
import torch
import wandb

RESULTS_DIR = "/tmp/results/"

#############################################################################
# Logging
#############################################################################


def wandb_weight_histogram_logging(model, epoch):
    for name, param in model.named_parameters():
        if param.grad is not None:
            wandb.log(
                {
                    f"grad_hist/{name}": wandb.Histogram(param.grad.cpu().numpy()),
                    "epoch": epoch,
                }
            )


def get_total_weight_norm(model):
    """
    Returns mean square root norm of params
    """
    total_norm = 0
    for _, param in model.named_parameters():
        if param.grad is not None:
            param_norm = param.norm(2)
            total_norm += param_norm**2
    return total_norm**0.5


def setup_results_dir_once():
    if not hasattr(setup_results_dir_once, "called"):
        if os.path.exists(RESULTS_DIR):
            shutil.rmtree(RESULTS_DIR)
        os.mkdir(RESULTS_DIR)
        setup_results_dir_once.called = True


class TrainingTimer:
    def __init__(self):
        gc.collect()
        torch.cuda.empty_cache()
        # torch.cuda.reset_max_memory_allocated()
        # torch.cuda.synchronize()
        self.start_time = time.perf_counter()

    def lapse_time(self) -> int:
        # torch.cuda.synchronize()
        end_time = time.perf_counter()
        return end_time - self.start_time


#############################################################################
# Images
#############################################################################

def binary_label_to_name(binary_label,class_names):
    return [class_names[i] for i, val in enumerate(binary_label) if val]    

def visualize_image_class_names(image, pred_cat_ids, ground_truth_cat_ids, class_names):
    """
    class_names: {cat_id: class name}
    """
    setup_results_dir_once()

    # Making channels the last dimension
    plt.imshow(image.permute(1, 2, 0))
    plt.title("image")

    gt = binary_label_to_name(ground_truth_cat_ids, class_names)
    pred = binary_label_to_name(pred_cat_ids, class_names)

    label_text = "Ground truth: "+", ".join(gt) + "\n"
    label_text += "Predictions: "+", ".join(pred) + "\n"
    plt.title(label_text, fontsize=10)
    # plt.gcf().text(0.5, 0.95, label_text, fontsize=12, ha='center',
    #             bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')) 
    tiempo = int(time.time() * 1000)
    plt.savefig(RESULTS_DIR + str(tiempo) + ".png")
    plt.show()
    
def visualize_image_target_mask(image, target=None, labels=None):
    # See torch.Size([3, 281, 500]) torch.Size([1, 281, 500])
    setup_results_dir_once()

    plt.subplot(1, 3, 1)
    # Making channels the last dimension
    plt.imshow(image.permute(1, 2, 0))
    plt.title("image")

    if target is not None:
        plt.subplot(1, 3, 2)
        # Making channels the last dimension
        plt.imshow(target)
        plt.title("prediction")

    if labels is not None:
        plt.subplot(1, 3, 3)
        # Making channels the last dimension
        plt.imshow(labels)
        plt.title("labels")

    # See tensor([  0,   1,  15, 255], dtype=torch.uint8)
    tiempo = int(time.time() * 1000)

    plt.savefig(RESULTS_DIR + str(tiempo) + ".png")
    plt.show()
