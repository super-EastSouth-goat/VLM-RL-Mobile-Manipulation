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