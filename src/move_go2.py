"""
Move Go2 - 最终版 (物理地面修复 + API修复)
"""
import argparse
import sys
import math

# 1. 启动仿真
import isaacsim
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Move Go2")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# 2. 导入核心库
import torch
from isaaclab.sim import SimulationContext, SimulationCfg
from isaaclab.assets import Articulation
# 引入 UsdPhysics 用来添加碰撞属性
from pxr import UsdGeom, UsdLux, UsdPhysics, Sdf, Gf

# 导入资产
try:
    from isaaclab_assets.robots.unitree import UNITREE_GO2_CFG
except ImportError:
    from isaaclab.assets import UNITREE_GO2_CFG

def main():
    # 初始化仿真
    sim = SimulationContext(SimulationCfg(dt=0.01))
    sim.set_camera_view([1.5, 1.5, 0.8], [0.0, 0.0, 0.4])

    # 获取舞台
    stage = sim.stage

    # --- 创建场景 ---
    # 1. 灯光
    UsdLux.DistantLight.Define(stage, "/World/Light").CreateIntensityAttr(1000.0)

    # 2. 创建物理地面 (修复了这里！)
    plane_path = "/World/GroundPlane"
    physics_ground = UsdGeom.Plane.Define(stage, plane_path)
    
    # OLD (Error): physics_ground.AddAxisAttr("Z")
    # NEW (Fixed): Use CreateAxisAttr
    physics_ground.CreateAxisAttr("Z") # Z轴朝上
    
    # 添加碰撞 API (CollisionAPI)，让它变“实心”
    UsdPhysics.CollisionAPI.Apply(physics_ground.GetPrim())
    
    # ----------------

    # --- 机器狗配置 ---
    robot_cfg = UNITREE_GO2_CFG.replace(prim_path="/World/Go2")
    # 初始位置：Z=0.45 (保证脚在地面上方，不要卡进地里)
    robot_cfg.init_state.pos = (0.0, 0.0, 0.45)
    
    # 增加刚度
    for key in robot_cfg.actuators.keys():
        robot_cfg.actuators[key].stiffness = 40.0
        robot_cfg.actuators[key].damping = 5.0

    robot = Articulation(robot_cfg)
    
    sim.reset()
    print("[INFO] 仿真开始！Go2 应该能站住了！")

    default_joints = robot.data.default_joint_pos.clone()

    sim_time = 0.0
    
    while simulation_app.is_running():
        # 1. 计算指令
        offset = 0.3 * math.sin(sim_time * 3.0) 
        joint_targets = default_joints + offset

        # 2. 应用指令
        robot.set_joint_position_target(joint_targets)
        
        # 3. 写入数据
        robot.write_data_to_sim()

        # 4. 物理步进
        sim.step()
        
        # 5. 更新状态
        robot.update(sim.cfg.dt)
        sim_time += sim.cfg.dt

        pos = robot.data.root_pos_w[0]
        # 打印高度
        print(f"\r🐶 Height: {pos[2]:.3f} m | Cmd: {offset:.3f}", end="")

    simulation_app.close()

if __name__ == "__main__":
    main()