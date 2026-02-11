from isaaclab.utils import configclass
from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoAlgorithmCfg

@configclass
class UnitreeGo2RoughPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 1500
    save_interval = 50
    experiment_name = "unitree_go2_rough"
    empirical_normalization = False

    # ==========================================================
    # 核心配置区域
    # ==========================================================
    actor = {
        # 使用新版类名 MLPModel
        "class_name": "rsl_rl.models.MLPModel",
        "hidden_dims": [512, 256, 128],
        "activation": "elu",
        "init_noise_std": 1.0,
        # !!! 这一行是解决你当前报错的关键 !!!
        "stochastic": True, 
    }

    critic = {
        # Critic 不需要随机性，所以不用加 stochastic
        "class_name": "rsl_rl.models.MLPModel",
        "hidden_dims": [512, 256, 128],
        "activation": "elu",
    }
    # ==========================================================

    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )