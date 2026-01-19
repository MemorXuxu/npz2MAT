import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import scipy.io as io
import numpy as np
import os

class NPZtoMATConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("NPZ to MAT 文件转换器")
        self.root.geometry("650x640")
        
        # 设置样式
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", font=("Arial", 10))
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="NPZ 到 MAT 文件转换器", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 输入文件选择
        input_frame = ttk.LabelFrame(main_frame, text="选择输入文件 (.npz)", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.input_path = tk.StringVar()
        ttk.Label(input_frame, text="NPZ 文件路径:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, sticky="ew")
        ttk.Button(input_frame, text="浏览", command=self.browse_input_file).grid(row=0, column=2, padx=(10, 0))
        
        # 输出文件选择
        output_frame = ttk.LabelFrame(main_frame, text="选择输出文件 (.mat)", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path = tk.StringVar()
        ttk.Label(output_frame, text="MAT 文件路径:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, sticky="ew")
        ttk.Button(output_frame, text="浏览", command=self.browse_output_file).grid(row=0, column=2, padx=(10, 0))
        
        # 文件信息显示
        info_frame = ttk.LabelFrame(main_frame, text="文件信息", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.info_text = tk.Text(info_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="加载 NPZ 文件信息", 
                  command=self.load_npz_info).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="转换到 MAT", 
                  command=self.convert_to_mat).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="退出", 
                  command=self.root.quit).pack(side=tk.RIGHT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X)
        
    def browse_input_file(self):
        """浏览并选择输入文件"""
        file_path = filedialog.askopenfilename(
            title="选择 NPZ 文件",
            filetypes=[("NPZ files", "*.npz"), ("All files", "*.*")]
        )
        if file_path:
            self.input_path.set(file_path)
            self.status_var.set(f"已选择输入文件: {os.path.basename(file_path)}")
    
    def browse_output_file(self):
        """浏览并选择输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存 MAT 文件",
            defaultextension=".mat",
            filetypes=[("MAT files", "*.mat"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
            self.status_var.set(f"已选择输出文件: {os.path.basename(file_path)}")
    
    def load_npz_info(self):
        """加载 NPZ 文件信息并显示"""
        input_file = self.input_path.get()
        
        if not input_file:
            messagebox.showerror("错误", "请先选择 NPZ 文件")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("错误", "NPZ 文件不存在")
            return
        
        try:
            self.progress.start()
            self.status_var.set("正在加载 NPZ 文件信息...")
            
            # 加载 NPZ 文件
            data = np.load(input_file)
            
            # 清空信息显示
            self.info_text.delete(1.0, tk.END)
            
            # 显示文件信息
            info = f"NPZ 文件信息:\n"
            info += f"文件路径: {input_file}\n"
            info += f"文件大小: {os.path.getsize(input_file) / 1024:.2f} KB\n"
            info += f"\n包含的数组:\n"
            
            for key in data.files:
                array = data[key]
                info += f"\n数组名: {key}\n"
                info += f"  形状: {array.shape}\n"
                info += f"  数据类型: {array.dtype}\n"
                info += f"  大小: {array.size} 个元素\n"
                
                # 显示前几个元素（如果是小数组）
                if array.size <= 10:
                    info += f"  数据: {array}\n"
                else:
                    info += f"  前5个元素: {array.flat[:5]}\n"
            
            self.info_text.insert(tk.END, info)
            self.status_var.set("NPZ 文件信息加载完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载 NPZ 文件时出错:\n{str(e)}")
            self.status_var.set("加载失败")
        finally:
            self.progress.stop()
    
    def convert_to_mat(self):
        """执行转换操作"""
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        
        if not input_file:
            messagebox.showerror("错误", "请先选择 NPZ 文件")
            return
        
        if not output_file:
            messagebox.showerror("错误", "请先选择输出 MAT 文件路径")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("错误", "NPZ 文件不存在")
            return
        
        try:
            self.progress.start()
            self.status_var.set("正在转换文件...")
            
            # 执行核心转换操作
            data = np.load(input_file)
            io.savemat(output_file, mdict=dict(data))
            
            # 显示转换结果
            self.info_text.insert(tk.END, f"\n\n转换完成!\n")
            self.info_text.insert(tk.END, f"输入文件: {input_file}\n")
            self.info_text.insert(tk.END, f"输出文件: {output_file}\n")
            self.info_text.insert(tk.END, f"文件大小: {os.path.getsize(output_file) / 1024:.2f} KB\n")
            
            messagebox.showinfo("成功", f"文件转换完成!\n输出文件: {output_file}")
            self.status_var.set("转换完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出错:\n{str(e)}")
            self.status_var.set("转换失败")
        finally:
            self.progress.stop()
    
    def clear_all(self):
        """清空所有内容"""
        self.input_path.set("")
        self.output_path.set("")
        self.info_text.delete(1.0, tk.END)
        self.status_var.set("已清空")

def main():
    root = tk.Tk()
    app = NPZtoMATConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()