# Robotics-Integration-Group-13

---

## Jetson Orin NX
### 1. System Environment config
| Environment | Version                    |
|-------------|----------------------------|
| JetPack     | 6.2.1                      |
| Ubuntu      | 22.04 Jammy                |
| CUDA        | 12.6.68                    |
| cuDNN       | 9.3.0.75                   |
| VPI         | 3.2.4                      |
| Vulkan      | 1.3.204                    |
| Python      | 3.10.12                    |
| OpenCV      | 4.11.0 with CUDA: YES      |
| PyTorch     | 2.5.0 (torchvision 0.23.0) |
| TensorRT    | 10.3.0                     |

> Suggestion: Use `jtop` to check the system config.

### 2. Compilation Environment config
Before configuring the environement, run `sudo apt-get update` and `sudo apt-get upgrade` at first.
<details>

<summary> 1. Python </summary>

- Use `miniconda` to manage python version. 
- Run `conda create --name xxx python=3.10` to create virtual env

</details>

<details>
<summary> 2. Ultralytics (YOLO) </summary>

- Install ultralytics dependencies: `pip install ultralytics`
- Uninstall `torch` and `torchvision` for they're `cpu` version: `pip uninstall torch torchvision` (See belows)
- Reinstall `numpy` for its too-high version: `pip install "numpy<2" --force-reinstall`

</details>

<details>
<summary> 3. OpenCV </summary>

- Install **nano / orin**: `sudo apt-get install nano`
    > Don't worry it's also compatible with `orin nx`
- Install **dphys-swapfile**: `sudo apt-get install dphys-swapfile`
- Enlarge the boundary of **CONF_MAXSWAP**: `sudo nano /sbin/dphys-swapfile`
- Restart the **nano / orin**: `sudo reboot`
- Check memory: `free -m`
- Run automator script [OpenCV-4-11-0.sh](./doc/guide/OpenCV-4-11-0.sh):
  - Grant permissions: `sudo chmod 755 ./OpenCV-4-11-0.sh`
  - Run: `./OpenCV-4-11-0.sh`
- Then check the installation of `opencv-cuda-version` is okay

    > Thanks to [Q-engineering](https://qengineering.eu/install-opencv-on-jetson-nano.html) I finally did it!

</details>

<details>
<summary> 4. Pytorch </summary>

- Uninstall **cpu-pytorch**: `sudo apt-get uninstall pytorch`  
- Install **gpu-pytorch** from a prebuild wheel:
```
pip install https://github.com/ultralytics/assets/releases/download/v0.0.0/torch-2.5.0a0+872d972e41.nv24.08-cp310-cp310-linux_aarch64.whl
```
> See Resources [Pytorch for Jetson](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#overview)

</details>

<details>
<summary> 5. TensorRT </summary>

- Install **tensorrt** from a prebuild wheel:
```
pip install https://github.com/ultralytics/assets/releases/download/v0.0.0/torchvision-0.20.0a0+afc54f7-cp310-cp310-linux_aarch64.whl
```
> See Resources [TensorRT for Jetson](https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/installing.html)

</details>

<details>
<summary> 6. ONNX </summary>

- The onnxruntime-gpu package hosted in PyPI does not have `aarch64` binaries for the Jetson. So we need to manually install this package.
- Install `onnxruntime-gpu`: With Python3.10 on our `jetson orin nx`, here we install [onnxruntime-gpu 1.20.0](https://pypi.org/project/onnxruntime-gpu/) by:
```
pip install https://github.com/ultralytics/assets/releases/download/v0.0.0/onnxruntime_gpu-1.20.0-cp310-cp310-linux_aarch64.whl
```

</details>

---

## Reference
[1] YOLO Official Web: [Ultralytics YOLO Docs](https://docs.ultralytics.com) \
[2] Robomaster Support: [Robomaster SDK Ultra](https://github.com/RamessesN/Robomaster-SDK-Ultra) \
[3] Training on Intel Arc GPU: [intel-extension-for-pytorch](https://github.com/intel/intel-extension-for-pytorch) & [ultralytics issue #19821](https://github.com/ultralytics/ultralytics/issues/19821)

---

#### ⚠️ License: This project isn't open-source. See Details [LICENSE](LICENSE).