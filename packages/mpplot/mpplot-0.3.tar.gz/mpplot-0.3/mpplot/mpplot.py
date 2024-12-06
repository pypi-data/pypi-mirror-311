import matplotlib.pyplot as plt
import h5py

import matplotlib.animation as animation
import numpy as np
class RealTimePlot:
    def __init__(self, num_lines=3, x_range=(0, 10), y_range=(0, 1)):
        self.num_lines = num_lines
        # self.x = np.linspace(x_range[0], x_range[1], 100)
        self.lines = [[] for _ in range(num_lines)]  # 存储每条线的数据
        self.timestamps = []  # 存储时间戳
        self.xmax=x_range[1]
        # 设置图形
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(x_range)
        self.ax.set_ylim(y_range)
        self.line_objects = [self.ax.plot([], [])[0] for _ in range(num_lines)]

        # 动画更新
        self.ani = animation.FuncAnimation(self.fig, self.update,  blit=False,interval=10,cache_frame_data=False)

    def add_point(self, t, x):
        """ 添加数据点到指定的线条 """
        if len(self.timestamps) == 0 or t > self.timestamps[-1]:
            self.timestamps.append(t)
            for i in range(self.num_lines):
                # 在每条线中添加数据点
                if len(self.lines[i]) < len(self.timestamps):
                    self.lines[i].append(x[i])  # 假设 x 是一个列表
                else:
                    self.lines[i][t] = x[i]  # 更新已有点
        if(max(self.timestamps)>self.xmax):
            self.xmax=self.xmax*2+1
        self.ax.set_xlim(min(self.timestamps), self.xmax)
        self.ax.set_ylim(min(min(line) for line in self.lines), 1+max(max(line) for line in self.lines))
        plt.pause(1.0/1000)

    def update(self, frame):
        # 更新每条线的y值
        for i in range(self.num_lines):
            self.line_objects[i].set_data(self.timestamps, self.lines[i])
        
        return self.line_objects
    def show(self):
        plt.show(block=False)
# matlab python 图形交换格式:matlab python graphics interchange format(mpgif)
class MatAxes:
    def __init__(self, ax,fig):
        self.ax = ax
        self.data = []
        self.title_text = ""
        self.xlabel_text = ""
        self.ylabel_text = ""
        self.zlabel_text = ""
        self.is3d = 0
        self.legend_kwargs = {}
        self.parent=fig

    def plot(self, x, y, *args, **kwargs):
        self.ax.plot(x, y, *args, **kwargs)
        self.data.append((x, y, args,'plot', kwargs))
    def plotc(self, x, y, *args, **kwargs):
        self.ax.plot(x, y, *args, **kwargs)
        self.data.append((x, y, args,'plotc', kwargs))
    def plot3(self, x, y, *args, **kwargs):
        self.ax.plot(x, y, *args, **kwargs)
        self.data.append((x, y, args,'plot3', kwargs))

    def scatter(self, x, y, *args, **kwargs):
        self.ax.scatter(x, y, *args, **kwargs)
        self.data.append((x, y,args, 'scatter', kwargs))

    def bar(self, x, height, *args, **kwargs):
        self.ax.bar(x, height, *args, **kwargs)
        self.data.append((x, height,args, 'bar', kwargs))

    def quiver(self, x, y, *args, **kwargs):
        self.ax.quiver(x, y,*args, **kwargs)
        self.data.append((x, y, args,'quiver', kwargs))
    def quiver3(self, x, y, *args, **kwargs):
        self.ax.quiver(x, y, *args, **kwargs)
        self.data.append((x, y,args, 'quiver3', kwargs))
        self.is3d=1

    def set_title(self, title):
        self.ax.set_title(title)
        self.title_text = title

    def set_xlabel(self, label):
        self.ax.set_xlabel(label)
        self.xlabel_text = label

    def set_ylabel(self, label):
        self.ax.set_ylabel(label)
        self.ylabel_text = label

    def set_zlabel(self, label):
        self.ax.set_zlabel(label)
        self.zlabel_text = label

    def legend(self, **kwargs):
        self.ax.legend(**kwargs)
        self.legend_kwargs = kwargs

    def get_axes(self):
        return self.ax
    def get_fig(self):
        return self.parent

    def save_data(self, hdf5_group,k):
        # 保存坐标区的相关数据
        group = hdf5_group.create_group("axes_" + str(k))
        group.attrs['title'] = self.title_text
        group.attrs['xlabel'] = self.xlabel_text
        group.attrs['ylabel'] = self.ylabel_text
        group.attrs['zlabel'] = self.zlabel_text
        group.attrs['is3d'] = self.is3d
        if self.legend_kwargs is not None:
            group.attrs['legend_kwargs'] = str(self.legend_kwargs)
        # 保存绘制的数据
        for idx, (x, y, args, plot_type, kwargs) in enumerate(self.data):
            plot_group = group.create_group(f"plot_{idx}")
            plot_group.attrs['plot_type']=plot_type
            plot_group.create_dataset("x", data=x)
            plot_group.create_dataset("y", data=y)
            # if len(args)>0:
            plot_group_param = plot_group.create_group(f"params")
            for id,arg in enumerate(args):
                plot_group_param.create_dataset(f"p_{id}", data=arg)
            # 这里可以保存其他参数
            # 将 kwargs 参数保存为属性
            for key, value in kwargs.items():
                plot_group.attrs[key] = value  # 转换为字符串保存

class Matfig:
    def __init__(self, *args, **kwargs):
        self.fig = plt.figure(*args, **kwargs)
        self.axes_list = []

    def add_subplot(self, *args, **kwargs):
        ax = self.fig.add_subplot(*args, **kwargs)
        mat_axes = MatAxes(ax,self)
        self.axes_list.append(mat_axes)
        return mat_axes
    def subplots(self, nrows, ncols, **kwargs):
        """ 创建多个子图并返回 figure 和 MatAxes 对象列表 """
        fig, axes = plt.subplots(nrows, ncols, **kwargs)
        mat_axes_list = []
        
        for ax in np.ravel(axes):  # 将多维数组展平
            mat_axes = MatAxes(ax, self)
            mat_axes_list.append(mat_axes)
            self.axes_list.append(mat_axes)
        
        return fig, mat_axes_list  # 返回 figure 和 MatAxes 列表

    # def show(self):
    #     plt.show()
    
    def current(self):
        if(len(self.axes_list)==0):
            return None
        else:
            return self.axes_list[-1]
    # def current(self):
    #     if(len(self.axes_list)==0):
    #         return None
    #     else:
    #         return self.axes_list[-1]
    def set_current(self,ma):
        if ma in self.axes_list:
            self.axes_list.remove(ma)
            self.axes_list.append(ma)
        else:
            raise ValueError("try to set a axis not there!")


    def savefig(self, filename, **kwargs):
        # 保存图形到文件
        self.fig.savefig(filename, **kwargs)

        # 保存数据到 HDF5
        with h5py.File(filename +'.mpif.h5', 'w') as h5file:
            h5file.attrs['axes'] = len(self.axes_list)
            h5file.attrs['version'] = "Matfig-v0.1"
            h5file.attrs['author'] =  "LiJun"
            # h5file.attrs['is3d'] =  self.is3d
            for k,mat_axes in enumerate(self.axes_list):
                mat_axes.save_data(h5file,k)
            print("metafile save to {path}, use plotmutihdf5('{path}') to reproduce it in matlab".format(path= filename +'.mpif.h5'))


# 全局变量
_self_figures = {}
def _get_current_fig_id():
    current_fig = plt.gcf()
    if current_fig.number in _self_figures:
        return current_fig.number
    else:
        return _initfigure(current_fig)

def _initfigure(fig):
    fig_id = fig.number
    _self_figures[fig_id] = Matfig(fig)
    return fig_id

def figure(*args, **kwargs):
    fig = plt.figure(*args, **kwargs)
    mf=Matfig(fig)
    fig_id = fig.number
    _self_figures[fig_id] = mf
    return mf
def plot(x, y, *args, **kwargs):
    ax=gca()
    return ax.plot(x, y, *args, **kwargs)
def subplot(*args, **kwargs):
    fig_id = _get_current_fig_id()
    return _self_figures[fig_id].add_subplot(*args, **kwargs)

# 全局函数
def subplots(nrows, ncols, **kwargs):
    fig_id = _get_current_fig_id()
    return _self_figures[fig_id].subplots(nrows, ncols, **kwargs)


def gcf():
    fig_id=_get_current_fig_id()
    return _self_figures[fig_id]
    
def gca():
    fig=gcf()
    ma0=fig.current()
    if ma0 is None:
        ma0=fig.add_subplot()
        
    return ma0

# MatAxes
def sca(ma):
    ma.get_fig().set_current(ma)
    plt.sca(ma.get_axes())
    return ma


    
def show():
    plt.show()

def savefig(filename, **kwargs):
    fig_id = _get_current_fig_id()
    _self_figures[fig_id].savefig(filename, **kwargs)



