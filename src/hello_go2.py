import argparse
import sys

# 1. 启动仿真 (The Launch)
print("[INFO] 正在唤醒 Isaac Sim...")
import isaacsim
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Hello Go2")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

print("[INFO] 引擎启动成功！正在加载资产...")

# -----------------------------------------------------------
# 2. 导入核心库 (The Logic)
# -----------------------------------------------------------
import torch
from isaaclab.sim import SimulationContext, SimulationCfg
from isaaclab.assets import Articulation

# 导入 USD 库 (用来代替 omni.isaac.core 画地面)
from pxr import UsdGeom, Gf, UsdLux

# 动态加载 Go2 配置
try:
    from isaaclab_assets.robots.unitree import UNITREE_GO2_CFG
except ImportError:
    # 备选路径
    from isaaclab.assets import UNITREE_GO2_CFG

def main():
    # 初始化仿真
    sim = SimulationContext(SimulationCfg(dt=0.01))
    sim.set_camera_view([2.0, 2.0, 2.0], [0.0, 0.0, 0.0])

    # 获取当前舞台 (Stage)
    stage = sim.stage

    # --- 使用 PXR 原生命令创建地面和灯光 ---
    print("[INFO] 创建场景 (使用 USD)...")
    
    # 1. 创建灯光
    light = UsdLux.DistantLight.Define(stage, "/World/Light")
    light.CreateIntensityAttr(1000.0)

    # 2. 创建地面 (用一个巨大的 Xform 代表地面位置)
    ground = UsdGeom.Xform.Define(stage, "/World/Ground")
    
    # ------------------------------------------------

    # 创建机器狗
    print("[INFO] 生成 Unitree Go2...")
    robot_cfg = UNITREE_GO2_CFG.replace(prim_path="/World/Go2")
    robot_cfg.init_state.pos = (0.0, 0.0, 0.5)
    go2_robot = Articulation(robot_cfg)

    sim.reset()
    print("[INFO] 仿真开始！注意看屏幕！")

    while simulation_app.is_running():
        sim.step()
        
        # --- 核心修改：直接更新，去掉 is_valid 检查 ---
        go2_robot.update(0.01)
        
        # 获取位置
        pos = go2_robot.data.root_pos_w[0]
        
        # 打印高度 (如果数字在变，说明物理引擎在工作！)
        print(f"\r🐶 Go2 Height: {pos[2]:.3f} m", end="")

    simulation_app.close()

if __name__ == "__main__":
    main()