#VLM-RL-Mobile_manipulation
Based on Unitree Go2 & NVIDIA Isaac Lab. Intergrating VLM for semantic navigation.

## 🚀 Environment Setup & Verification (已验证)

### Prerequisites
- **System**: Ubuntu 22.04 + RTX 3060
- **Environment**: Isaac Sim 4.5+ / Isaac Lab (Flat Layout)
- **Python**: 3.10 / 3.11

### 🛠️ How to Run the "Hello Go2" Demo

由于 Isaac Lab 采用 Flat Layout 结构，运行前必须设置 `PYTHONPATH` 以加载源码和资产。

1. **设置环境变量 (关键步骤)**
   ```bash
   # 临时设置 (当前终端有效)
   export PYTHONPATH=$HOME/workspace/IsaacLab/source:$HOME/workspace/IsaacLab/source/isaaclab_assets:$PYTHONPATH
   export DISPLAY=:0
2. **运行脚本 使用 Isaac Lab 内置的 python 解释器运行：**
   ```bash
   # 确保在项目根目录下
   ../IsaacLab/isaaclab.sh -p src/hello_go2.py

---

## 🎮 Phase 2: Basic Control & Physics Verification (已验证)

**Goal**: Verify the control loop by sending PD commands to the robot's actuators.

### 🕹️ How to Run
运行运动控制演示脚本，观察机器狗在物理地面上进行原地关节运动（Sine Wave Control）：

```bash
# 1. 设置环境变量
export PYTHONPATH=$HOME/workspace/IsaacLab/source:$HOME/workspace/IsaacLab/source/isaaclab_assets:$PYTHONPATH
export DISPLAY=:0

# 2. 运行脚本
../IsaacLab/isaaclab.sh -p src/move_go2.py

---

## 🧠 Phase 3: AI Control & Reinforcement Learning (已验证)

**Goal**: Train a neural network policy (Brain) to control the Unitree Go2 robot using **PPO (Proximal Policy Optimization)** via the `rsl_rl` library.
**目标**: 使用 PPO 算法训练神经网络策略，接管机器狗的 12 个电机控制，实现复杂地形上的鲁棒行走。

### 🏋️‍♂️ Training the Agent (训练)

使用 `rsl_rl` 库进行训练。建议使用无头模式 (`--headless`) 以加快训练速度。

**Run Training Command:**
```bash
# 确保环境变量已设置 (PYTHONPATH & DISPLAY)
export PYTHONPATH=$HOME/workspace/IsaacLab/source:$HOME/workspace/IsaacLab/source/isaaclab_assets:$PYTHONPATH
export DISPLAY=:0

# 启动训练 (Headless mode for speed)
# Task: Isaac-Velocity-Rough-Unitree-Go2-v0
../IsaacLab/isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Rough-Unitree-Go2-v0 --headless

🎮 Running the Trained Policy (推理/可视化)
加载训练好的 checkpoint 模型并在仿真器中查看效果。

⚠️ Critical Note for RTX 3060 (6GB VRAM): 由于显存限制，必须添加 --num_envs 1 参数。默认的 50 个环境会导致 PhysX OOM (Out of Memory) 崩溃。

Run Play Command:

Bash
# --num_envs 1 is required to prevent VRAM crash on Laptop GPUs
../IsaacLab/isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py --task Isaac-Velocity-Rough-Unitree-Go2-v0 --num_envs 1