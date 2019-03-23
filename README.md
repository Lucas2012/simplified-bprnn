# Structure Inference Machines: Recurrent Neural Networks for Analyzing Relations 

This is the official implementation for the paper [Structure Inference Machines: Recurrent Neural Networks for Analyzing Relations in Group Activity Recognition](https://arxiv.org/abs/1511.04196).

Please cite our paper if you find this code helpful:

```
@article{Deng2016StructureIM,
  title={Structure Inference Machines: Recurrent Neural Networks for Analyzing Relations in Group Activity Recognition},
  author={Zhiwei Deng and Arash Vahdat and Hexiang Hu and Greg Mori},
  journal={2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2016},
  pages={4772-4781}
}
```

## Overview

  Rich semantic relations are important in a variety of visual recognition problems. As a concrete example, group
activity recognition involves the interactions and relative spatial relations of a set of people in a scene. State of the art
recognition methods center on deep learning approaches for training highly effective, complex classifiers for interpreting images. However, bridging the relatively low-level concepts output by these methods to interpret higher-level
compositional scenes remains a challenge. Graphical models are a standard tool for this task. In this paper, we
propose a method to integrate graphical models and deep neural networks into a joint framework. Instead of using a
traditional inference method, we use a sequential inference modeled by a recurrent neural network. Beyond this, the
appropriate structure for inference can be learned by imposing gates on edges between nodes. Empirical results on
group activity recognition demonstrate the potential of this model to handle highly structured learning tasks.


