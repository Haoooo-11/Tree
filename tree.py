import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgba
import random
from matplotlib.font_manager import FontProperties
import os

CURRENT_STYLE_ID = "6"

# GIF保存配置
SAVE_GIF = True
GIF_FILENAME = "C:/Users/Hao/Desktop/Tree/christmas_tree.gif"
GIF_FPS = 15
GIF_DURATION = 10

# 样式配置
STYLES = {
    "1": {  # 经典绿色
        "bg_col": "#050505",
        "tree_cols": ["#0f3d0f", "#144514", "#006400", "#2E8B57", "#228B22"],
        "trunk_col": "#3e2723",
        "decor_cols": ["#FFD700", "#FF0000", "#FFFFFF", "#FFA500"],
        "star_col": "#FFD700",
        "text_col": "#FFD700",
        "ribbon_col": "#D4AF37",
        "snow_col": "white",
        "has_ribbon": True,
        "ribbon_width": 2.2
    },
    "2": {  # 冰雪蓝
        "bg_col": "#0a1014",
        "tree_cols": ["#2F4F4F", "#5F9EA0", "#708090"],
        "trunk_col": "#404040",
        "decor_cols": ["#E0FFFF", "#FFFFFF", "#B0C4DE"],
        "star_col": "#E0FFFF",
        "text_col": "#B0C4DE",
        "ribbon_col": "#F0FFFF",
        "snow_col": "#F0FFFF",
        "has_ribbon": True,
        "ribbon_width": 1.5
    },
    "3": {  # 橄榄绿
        "bg_col": "#1a1a1a",
        "tree_cols": ["#556B2F", "#6B8E23", "#808000"],
        "trunk_col": "#5D4037",
        "decor_cols": ["#CD853F", "#FFCC00"],
        "star_col": "#FFCC00",
        "text_col": "#DEB887",
        "ribbon_col": "#000000",
        "snow_col": "white",
        "has_ribbon": False,
        "ribbon_width": 0
    },
    "4": {  # 彩色装饰
        "bg_col": "#000000",
        "tree_cols": ["#006400", "#228B22"],
        "trunk_col": "#4E342E",
        "decor_cols": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"],
        "star_col": "#FFD700",
        "text_col": "#FF6347",
        "ribbon_col": "#C0C0C0",
        "snow_col": "white",
        "has_ribbon": True,
        "ribbon_width": 1.5
    },
    "5": {  # 黑白
        "bg_col": "#000000",
        "tree_cols": ["#1a1a1a", "#222222", "#333333"],
        "trunk_col": "#111111",
        "decor_cols": ["#FFFFFF", "#DDDDDD"],
        "star_col": "#FFFFFF",
        "text_col": "#FFFFFF",
        "ribbon_col": "#FFFFFF",
        "snow_col": "#808080",
        "has_ribbon": True,
        "ribbon_width": 1.2
    },
    "6": {  # 粉色浪漫
        "bg_col": "#120508",
        "tree_cols": ["#D87093", "#FF69B4", "#C71585"],
        "trunk_col": "#5D4037",
        "decor_cols": ["#FFFFFF", "#FFD700", "#FF1493"],
        "star_col": "#FFD700",
        "text_col": "#FFC0CB",
        "ribbon_col": "#FFB6C1",
        "snow_col": "#FFF0F5",
        "has_ribbon": True,
        "ribbon_width": 1.5
    }
}

CFG = STYLES.get(str(CURRENT_STYLE_ID), STYLES["1"])


class ChristmasTree:
    def __init__(self, cfg):
        self.cfg = cfg
        self.particles = []
        self.snow = []
        self.build_scene()
        self.init_snow()

    def build_scene(self):
        data = []
        n_layers = 8
        layer_gap = 0.04

        n_trunk = 2500
        for _ in range(n_trunk):
            h = np.random.uniform(-0.8, -0.2)
            r = np.random.uniform(0, 0.28)
            theta = np.random.uniform(0, 2 * np.pi)
            data.append({
                "x": r * np.cos(theta), "y": h, "z": r * np.sin(theta),
                "color": self.cfg["trunk_col"], "size": 18, "alpha": 1.0
            })

        total_leaves = 8000

        layer_heights = np.linspace(-0.5, 1.25, n_layers + 1)

        for layer_idx in range(n_layers):
            h_min_raw = layer_heights[layer_idx]
            h_max_raw = layer_heights[layer_idx + 1]

            if layer_idx == n_layers - 1:
                h_min = h_min_raw + layer_gap * 0.3
                star_target_h = layer_heights[-1] + 0.28
                h_max = star_target_h - 0.02
            else:
                h_min = h_min_raw + layer_gap
                h_max = h_max_raw - layer_gap

            layer_center_h = (h_min + h_max) / 2.0

            rel_h_layer = layer_idx / (n_layers - 1)

            if layer_idx == n_layers - 1:
                layer_type = "cone"
                layer_below_idx = layer_idx - 1
                rel_h_below = layer_below_idx / (n_layers - 1)
                max_radius_below = 1.6 * (1.0 - rel_h_below * 0.8)
                radius_at_top_below = max_radius_below * 0.7
                max_layer_radius = radius_at_top_below
                leaves_in_this_layer = int(total_leaves // n_layers * 1.2)
            else:
                layer_type = "cylinder"
                max_layer_radius = 1.6 * (1.0 - rel_h_layer * 0.8)
                leaves_in_this_layer = total_leaves // n_layers

            for _ in range(leaves_in_this_layer):
                h = np.random.uniform(h_min, h_max)
                rel_h_in_layer = (h - h_min) / (h_max - h_min) if (h_max - h_min) > 0 else 0

                if layer_type == "cone":
                    base_r = max_layer_radius * (1.0 - rel_h_in_layer)
                    r = base_r * np.sqrt(np.random.uniform(0.05, 1.0))
                    if rel_h_in_layer > 0.85:
                        blend_factor = (rel_h_in_layer - 0.85) / 0.15
                        if np.random.random() < blend_factor * 0.3:
                            particle_color = self.cfg["star_col"]
                        else:
                            particle_color = random.choice(self.cfg["tree_cols"])
                    else:
                        particle_color = random.choice(self.cfg["tree_cols"])
                else:
                    dist_to_center = abs(h - layer_center_h) / (h_max - h_min) * 2.0 if (h_max - h_min) > 0 else 0
                    base_r = max_layer_radius * (1.0 - dist_to_center ** 2 * 0.3)
                    r = base_r * np.sqrt(np.random.uniform(0.1, 1.0))
                    particle_color = random.choice(self.cfg["tree_cols"])

                theta = np.random.uniform(0, 2 * np.pi)

                data.append({
                    "x": r * np.cos(theta), "y": h, "z": r * np.sin(theta),
                    "color": particle_color,
                    "size": np.random.uniform(5, 15), "alpha": 0.9
                })

        total_decor = 600
        decor_per_layer = total_decor // n_layers

        for layer_idx in range(n_layers):
            h_min_raw = layer_heights[layer_idx]
            h_max_raw = layer_heights[layer_idx + 1]

            if layer_idx == n_layers - 1:
                h_min = h_min_raw + layer_gap * 0.3 + 0.01
                star_target_h = layer_heights[-1] + 0.28
                h_max = star_target_h - 0.02 - 0.01
            else:
                h_min = h_min_raw + layer_gap + 0.01
                h_max = h_max_raw - layer_gap - 0.01

            layer_center_h = (h_min + h_max) / 2.0
            rel_h_layer = layer_idx / (n_layers - 1)

            if layer_idx == n_layers - 1:
                layer_type = "cone"
                layer_below_idx = layer_idx - 1
                rel_h_below = layer_below_idx / (n_layers - 1)
                max_radius_below = 1.6 * (1.0 - rel_h_below * 0.8)
                radius_at_top_below = max_radius_below * 0.7
                max_layer_radius = radius_at_top_below
            else:
                layer_type = "cylinder"
                max_layer_radius = 1.6 * (1.0 - rel_h_layer * 0.8)

            for _ in range(decor_per_layer):
                h = np.random.uniform(h_min, h_max)
                rel_h_in_layer = (h - h_min) / (h_max - h_min) if (h_max - h_min) > 0 else 0

                if layer_type == "cone":
                    base_r = max_layer_radius * (1.0 - rel_h_in_layer)
                else:
                    dist_to_center = abs(h - layer_center_h) / (h_max - h_min) * 2.0 if (h_max - h_min) > 0 else 0
                    base_r = max_layer_radius * (1.0 - dist_to_center ** 2 * 0.3)

                r = base_r * 0.98
                theta = np.random.uniform(0, 2 * np.pi)
                data.append({
                    "x": r * np.cos(theta), "y": h, "z": r * np.sin(theta),
                    "color": random.choice(self.cfg["decor_cols"]),
                    "size": np.random.uniform(22, 45), "alpha": 1.0
                })

        if self.cfg["has_ribbon"]:
            total_ribbon_pts = 1200
            pts_per_layer = total_ribbon_pts // n_layers

            for layer_idx in range(n_layers):
                h_min_raw = layer_heights[layer_idx]
                h_max_raw = layer_heights[layer_idx + 1]

                if layer_idx == n_layers - 1:
                    h_min = h_min_raw + layer_gap * 0.3
                    h_max = h_max_raw - 0.01
                else:
                    h_min = h_min_raw + layer_gap
                    h_max = h_max_raw - layer_gap

                layer_center_h = (h_min + h_max) / 2.0
                rel_h_layer = layer_idx / (n_layers - 1)

                if layer_idx == n_layers - 1:
                    layer_type = "cone"
                    layer_below_idx = layer_idx - 1
                    rel_h_below = layer_below_idx / (n_layers - 1)
                    max_radius_below = 1.6 * (1.0 - rel_h_below * 0.8)
                    radius_at_top_below = max_radius_below * 0.7
                    max_layer_radius = radius_at_top_below
                else:
                    layer_type = "cylinder"
                    max_layer_radius = 1.6 * (1.0 - rel_h_layer * 0.8)

                h_vals = np.linspace(h_max, h_min, pts_per_layer)
                t_vals = np.linspace(0, 1.5 * np.pi, pts_per_layer) + (layer_idx * np.pi * 0.7)

                for i, t in enumerate(t_vals):
                    h = h_vals[i]
                    rel_h_in_layer = (h - h_min) / (h_max - h_min) if (h_max - h_min) > 0 else 0

                    if layer_type == "cone":
                        base_r = max_layer_radius * (1.0 - rel_h_in_layer)
                    else:
                        dist_to_center = abs(h - layer_center_h) / (h_max - h_min) * 2.0 if (h_max - h_min) > 0 else 0
                        base_r = max_layer_radius * (1.0 - dist_to_center ** 2 * 0.3)

                    r = base_r + 0.08
                    data.append({
                        "x": r * np.cos(t), "y": h, "z": r * np.sin(t),
                        "color": self.cfg["ribbon_col"],
                        "size": 8 * self.cfg["ribbon_width"], "alpha": 0.6
                    })

        star_h = layer_heights[-1] + 0.28

        n_transition = 50
        transition_h_range = (star_h - 0.02, star_h - 0.005)
        for _ in range(n_transition):
            h_trans = np.random.uniform(transition_h_range[0], transition_h_range[1])
            rel_trans = (h_trans - transition_h_range[0]) / (transition_h_range[1] - transition_h_range[0])
            r_trans = 0.02 * (1.0 - rel_trans) * np.sqrt(np.random.uniform(0.1, 1.0))
            theta_trans = np.random.uniform(0, 2 * np.pi)
            blend_ratio = rel_trans
            if np.random.random() < blend_ratio:
                trans_color = self.cfg["star_col"]
            else:
                trans_color = random.choice(self.cfg["tree_cols"])
            data.append({
                "x": r_trans * np.cos(theta_trans), "y": h_trans, "z": r_trans * np.sin(theta_trans),
                "color": trans_color,
                "size": np.random.uniform(3, 8), "alpha": 0.7 + rel_trans * 0.3
            })

        data.append({
            "x": 0, "y": star_h, "z": 0,
            "color": self.cfg["star_col"], "size": 500, "alpha": 1.0, "marker": "*"
        })
        for size, alpha in [(800, 0.2), (500, 0.3), (300, 0.4)]:
            data.append({
                "x": 0, "y": star_h, "z": 0,
                "color": self.cfg["star_col"], "size": size, "alpha": alpha
            })

        self.particles = self._process_data(data)

    def init_snow(self):
        n_snow = 500
        data = []
        for _ in range(n_snow):
            data.append({
                "x": np.random.uniform(-2.5, 2.5),
                "y": np.random.uniform(-1.0, 1.5),
                "z": np.random.uniform(-2.5, 2.5),
                "vx": 0, "vy": np.random.uniform(0.02, 0.05), "vz": 0,
                "color": self.cfg["snow_col"],
                "size": np.random.uniform(4, 9), "alpha": np.random.uniform(0.4, 0.8)
            })
        self.snow = data

    def _process_data(self, data_list):
        processed = []
        for p in data_list:
            rgba = to_rgba(p["color"])
            marker_type = 1.0 if p.get("marker") == "*" else 0.0
            processed.append([
                p["x"], p["y"], p["z"],
                rgba[0], rgba[1], rgba[2], p["alpha"],
                p["size"], marker_type
            ])
        return np.array(processed)


def update(frame, tree, ax, custom_font_prop):
    ax.clear()
    ax.set_facecolor(tree.cfg["bg_col"])
    ax.set_axis_off()

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-0.9, 1.65)

    camera_dist = 2.4

    angle = frame * 0.08
    cos_a, sin_a = np.cos(angle), np.sin(angle)

    P = tree.particles.copy()
    x, y, z = P[:, 0], P[:, 1], P[:, 2]

    x_rot = x * cos_a - z * sin_a
    z_rot = x * sin_a + z * cos_a

    depth_factor = 1.0 / (camera_dist - z_rot)
    x_2d = x_rot * depth_factor
    y_2d = y * depth_factor
    sizes = P[:, 7] * depth_factor * 1000 * 0.002

    snow_data = []
    for s in tree.snow:
        s["y"] -= s["vy"]
        if s["y"] < -1.2: s["y"] = 1.6

        sx_rot = s["x"] * cos_a - s["z"] * sin_a
        sz_rot = s["x"] * sin_a + s["z"] * cos_a

        s_depth = 1.0 / (camera_dist - sz_rot)
        rgba = to_rgba(s["color"])

        if s_depth > 0:
            snow_data.append([
                sx_rot * s_depth, s["y"] * s_depth, sz_rot,
                rgba[0], rgba[1], rgba[2], s["alpha"],
                s["size"] * s_depth * 1000 * 0.002, 0.0
            ])

    snow_arr = np.array(snow_data) if len(snow_data) > 0 else np.zeros((0, 9))

    tree_render_data = np.zeros((len(P), 9))
    tree_render_data[:, 0] = x_2d
    tree_render_data[:, 1] = y_2d
    tree_render_data[:, 2] = z_rot
    tree_render_data[:, 3:7] = P[:, 3:7]
    tree_render_data[:, 7] = sizes
    tree_render_data[:, 8] = P[:, 8]

    all_points = np.vstack((tree_render_data, snow_arr))
    sorted_points = all_points[np.argsort(all_points[:, 2])]

    is_star = sorted_points[:, 8] > 0.5
    normal_pts = sorted_points[~is_star]
    star_pts = sorted_points[is_star]

    if len(normal_pts) > 0:
        ax.scatter(normal_pts[:, 0], normal_pts[:, 1],
                   s=normal_pts[:, 7], c=normal_pts[:, 3:7],
                   marker='o', edgecolors='none', zorder=1)

    if len(star_pts) > 0:
        ax.scatter(star_pts[:, 0], star_pts[:, 1],
                   s=star_pts[:, 7], c=star_pts[:, 3:7],
                   marker='*', edgecolors='none', zorder=100)

    text_y = 1.05
    if custom_font_prop:
        ax.text(0, text_y, "Merry Christmas", color=tree.cfg["text_col"],
                fontsize=45, ha='center', fontproperties=custom_font_prop, zorder=200)
    else:
        font_options = ['Brush Script MT', 'Comic Sans MS', 'Segoe Print', 'Ink Free']
        chosen_font = next((f for f in font_options if FontProperties(family=f).get_name() == f), 'serif')
        style = 'italic' if chosen_font == 'serif' else 'normal'
        weight = 'bold' if chosen_font == 'serif' else 'normal'
        ax.text(0, text_y, "Merry Christmas", color=tree.cfg["text_col"],
                fontsize=42, ha='center', fontname=chosen_font, style=style, fontweight=weight, zorder=200)


if __name__ == "__main__":
    tree = ChristmasTree(CFG)

    fig = plt.figure(figsize=(10, 8), facecolor=CFG["bg_col"])
    ax = fig.add_axes([0, 0, 1, 1])

    font_path = "GreatVibes-Regular.ttf"
    custom_font = None
    if os.path.exists(font_path):
        try:
            custom_font = FontProperties(fname=font_path)
        except:
            pass

    if GIF_DURATION is not None:
        total_frames = int(GIF_FPS * GIF_DURATION)
    else:
        total_frames = 300

    ani = animation.FuncAnimation(
        fig, update, fargs=(tree, ax, custom_font),
        frames=total_frames, interval=30, blit=False
    )

    if SAVE_GIF:
        ani.save(GIF_FILENAME, writer='pillow', fps=GIF_FPS)
        print(f"✓ GIF文件已成功保存: {GIF_FILENAME}")
        plt.show()
    else:
        plt.show()
