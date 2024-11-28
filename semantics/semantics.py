import math
import matplotlib.pyplot as plt


class Semantics:
    def __init__(self):
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.rot_ang = 0.0
        self.scale_x = 1
        self.scale_y = 1
        self.points = []  # 用于保存所有的绘制点
        self.t_values = []  # 保存T的值用于绘制

    def eval(self, ast_node):
        """根据语法树执行语义分析"""
        if ast_node.node_type == "Program":
            for child in ast_node.children:
                self.eval(child)
        elif ast_node.node_type == "OriginStatement":
            self.origin_x, self.origin_y = self.get_expr_value(ast_node.children[0]), self.get_expr_value(
                ast_node.children[1])
        elif ast_node.node_type == "ScaleStatement":
            self.scale_x, self.scale_y = self.get_expr_value(ast_node.children[0]), self.get_expr_value(
                ast_node.children[1])
        elif ast_node.node_type == "RotStatement":
            self.rot_ang = self.get_expr_value(ast_node.children[0])
        elif ast_node.node_type == "ForStatement":
            start = self.get_expr_value(ast_node.children[1])
            end = self.get_expr_value(ast_node.children[2])
            step = self.get_expr_value(ast_node.children[3])
            self.draw_loop(start, end, step, ast_node.children[4])  # 传递绘制点的表达式
        elif ast_node.node_type == "BinaryOp" or ast_node.node_type == "UnaryOp":
            return self.get_expr_value(ast_node)
        elif ast_node.node_type == "Constant":
            return float(ast_node.value)
        elif ast_node.node_type == "Variable":
            if ast_node.value == "T":
                return self.t_values[-1]  # 返回当前的T值
        else:
            print(f"Error: Unknown node type: {ast_node.node_type}")

    def get_expr_value(self, ast_node):
        """计算表达式的值"""
        if ast_node.node_type == "BinaryOp":
            left = self.get_expr_value(ast_node.children[0])
            right = self.get_expr_value(ast_node.children[1])
            if ast_node.value == '+':
                return left + right
            elif ast_node.value == '-':
                return left - right
            elif ast_node.value == '*':
                return left * right
            elif ast_node.value == '/':
                return left / right
            elif ast_node.value == '^':
                return left ** right
        elif ast_node.node_type == "UnaryOp":
            value = self.get_expr_value(ast_node.children[0])
            if ast_node.value == '+':
                return value
            elif ast_node.value == '-':
                return -value
        elif ast_node.node_type == "Constant":
            return float(ast_node.value)
        elif ast_node.node_type == "Variable":
            if ast_node.value == "T":
                return self.t_values[-1]

    def calc_coord(self, t_value, draw_x, draw_y):
        """计算点的坐标（进行平移、缩放、旋转）"""
        # 缩放
        scaled_x = self.origin_x + draw_x * self.scale_x
        scaled_y = self.origin_y + draw_y * self.scale_y

        # 旋转
        angle_rad = math.radians(self.rot_ang)
        rotated_x = scaled_x * math.cos(angle_rad) - scaled_y * math.sin(angle_rad)
        rotated_y = scaled_x * math.sin(angle_rad) + scaled_y * math.cos(angle_rad)

        return rotated_x, rotated_y

    def draw_pixel(self, t_value, draw_x, draw_y):
        """绘制一个点（使用matplotlib绘制）"""
        rotated_x, rotated_y = self.calc_coord(t_value, draw_x, draw_y)
        self.points.append((rotated_x, rotated_y))

    def draw_loop(self, start, end, step, draw_expr):
        """循环绘制所有的点"""
        print(f"start: {start}, end: {end}, step: {step}")  # Debugging print to check values
        t = start
        while t <= end:
            self.t_values.append(t)
            draw_x = draw_expr.children[0].value(t)  # 获取 X 坐标的表达式值
            draw_y = draw_expr.children[1].value(t)  # 获取 Y 坐标的表达式值
            print(f"Drawing point ({draw_x}, {draw_y})")
            self.draw_pixel(t, draw_x, draw_y)
            t += step

    def show_plot(self):
        """显示绘图"""
        x_vals, y_vals = zip(*self.points)
        plt.plot(x_vals, y_vals, marker='o')
        plt.title('Plot of Points')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.show()
