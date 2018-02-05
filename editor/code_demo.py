# -*- coding=utf-8 -*-
123456whatthefuck
import Tkinter as tk
yes
import Tkinter as tk
import Tkinter as tk
whatthefuck



import Tkinter as tk
import ttk
from tkMessageBox import showwarning, showinfo

#( sdkflsflaf
#kdsldfsf
#sdlfsdf
#sldflsf
#sldfsldf)


#[sdflsfl
#sldfsf]

#{sdflsdflsfds}


#sdlfsdf"sdlfsldfwieiowr   slfdslfd"


 #sjdflsdflsf'sdflsldflsdfsdfd'

import os
import re
from collections import OrderedDict

import control
import constant
import util


ctrl = control.Control()


class Data(object):
    def __init__(self):
        #保存选中的服务器列表
        self._selected_servers = OrderedDict()
        #保存发放进度
        self._act_server_ids = set()
        #发放成功服务器列表
        self._success = []
        #发放失败服务器列表
        self._fail = []

    def add_select_server(self, company_id, server_ids):
        if server_ids:
            self._selected_servers[company_id] = server_ids
        else:
            if company_id in self._selected_servers:
                self._selected_servers.pop(company_id)
    
    # 发活动时获取选中的服务器列表时调用
    def get_act_server_ids(self):
        self._act_server_ids = set()
        for server_ids in self._selected_servers.values():
            self._act_server_ids.update(server_ids)
        return list(self._act_server_ids)

    def _pop_server_id(self, server_id):
        if server_id in self._act_server_ids:
            self._act_server_ids.remove(server_id)

    def clear_selected_servers(self):
        self._selected_servers = OrderedDict()

    def dump_progress_info(self):
        if not self._act_server_ids:
            return "无"
        return "\n".join(["%s --- %s" % (server_info['name'], 
                                   server_info['ip']) for server_info in 
                                   [ctrl.get_server_info(server_id) for 
                                    server_id in self._act_server_ids]])

    def dump_selected_servers_info(self):
        return ["%s:(%d/%d)" % (ctrl.get_company_name(company_id),
                               len(server_ids), ctrl.get_company_servers_num(company_id))
               for company_id, server_ids in self._selected_servers.iteritems()]

    def is_select_company(self):
        return bool(self._selected_servers)

    def get_left(self):
        return len(self._act_server_ids)

    def add_success(self, server_id):
        self._success.append(server_id)
        self._pop_server_id(server_id)


    def add_fail(self, server_id):
        self._fail.append(server_id)
        self._pop_server_id(server_id)

    def get_result_info(self):
        result_info = '成功 : %d, 失败 : %d' % (len(self._success), len(self._fail))
        fail_info = self._dump_fail_servers_info()
        if fail_info:
            result_info = "%s\n失败列表 :\n%s" % (result_info, fail_info)
        self._reset_count()
        return result_info

    def _dump_fail_servers_info(self):
        return "\n".join(["%s --- %s" % (server_info['name'], 
                                   server_info['ip']) for server_info in 
                                   [ctrl.get_server_info(server_id) for 
                                    server_id in self._fail]])

    def _reset_count(self):
        self._success = []
        self._fail = []


root = None

class Gui(tk.Tk, Data):
    def __init__(self):
        tk.Tk.__init__(self)
        
        # 放到global里面，方便子控件引用，当然，子控件也可以通过 self.winfo_toplevel() 来获取root
        global root
        root = self

        self.iconbitmap(constant.ICON)
        self.title('脚本活动执行')
        self.resizable(False, False)
        #去掉菜单项开头的一横杆
        self.option_add("*tearOff", False)

        self.data = Data()

        # 菜单栏
        self._menu = None
        self._create_menu_bar()
        # 控制面板
        self.act_frm = ActivityFrm(self)
        # 服务器列表面板
        self.server_frm = None
        # 发放进度条
        self.progress_frm = None

        # 开始处理消息
        self._process_cmd()


    def _create_menu_bar(self):
        if self._menu:
            self._menu.pack_forget()

        self._menu = tk.Menu(self)

        menu_company = tk.Menu(self._menu)
        for company_id, company_name in ctrl.get_companys():
            menu_company.add_command(label = company_name, 
                 command= lambda _ = company_id: self._create_server_frm(_))

        menu_sys = tk.Menu(self._menu)
        menu_sys.add_command(label = '同步更新gm', command = self.update_gm)

        menu_log = tk.Menu(self._menu)
        menu_log.add_command(label = '查看执行日志', 
             command = self._check_log(constant.LOG_FILE))
        menu_log.add_command(label='查看执行进度', command = self._see_progress)

        self._menu.add_cascade(label='选择运营商', menu = menu_company)
        self._menu.add_cascade(label='系统设置', menu = menu_sys)
        self._menu.add_cascade(label='查看', menu = menu_log)
        
        self['menu'] = self._menu

    def update_gm(self):
        self.set_act_state()
        ctrl.update_gm()
        self.act_frm.add_msg("[完成]同步更新服务器列表")
        self.set_normal_state()
        self._create_menu_bar()
        
    def set_act_state(self):
        self.act_frm.set_act_state()
        
    def set_normal_state(self):
        self.act_frm.set_nomal_state()

    def _see_progress(self):
        showinfo('发放进度', "未完成:\n%s" % self.data.dump_progress_info())

    def _check_log(self, file_path):
        def _():
            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                showinfo('记录不存在', '%s 不存在' % abs_path)
                return
            os.startfile(abs_path)
        return _
    
    def _rm_server_frm(self):
        if self.server_frm:
            self.server_frm.pack_forget()
            self.server_frm = None
            

    def _create_server_frm(self, company_id):
        self._rm_server_frm()
        self.server_frm = ServersFrm(self, company_id,
                                  *ctrl.get_servers(company_id))
    
    def _rm_progress_frm(self):
        if self.progress_frm:
            self.progress_frm.pack_forget()
            self.progress_frm = None

    def _create_progress_frm(self, total_num):
        self._rm_server_frm()
        self._rm_progress_frm()
        self.progress_frm = ProgressFrm(self, total_num)

    def show_add_servers(self):
        self.act_frm.show_add_servers()
        
    def _process_cmd(self):
        self._process()
        _ = self.after(100, self._process_cmd)
    
    # 检查活动是否发完
    def _check_act_done(self):
        if 0 == self.data.get_left():
            self._rm_progress_frm()
            self.set_normal_state()
            self.show_add_servers()
            showinfo('结束', self.data.get_result_info())


    def _process(self):
        cmd = ctrl.get_cmd()
        if cmd:
            code, server_id, msg = cmd

            if code == constant.SUCCESS:
                self.data.add_success(server_id)

            if code == constant.FAIL:
                self.data.add_fail(server_id)

            self.act_frm.add_msg(msg)
            self.progress_frm.step()

            self._check_act_done()
        

    def do_active(self):
        # 检查服务器列表选择情况
        if not self.data.is_select_company():
            showwarning('注意', '请选择运营商和服务器！')
            return

        act_name, act_type, file_name = self.act_frm.get_act_info()
        act_name = util.encode_str(act_name)
        act_type = util.encode_str(act_type)
        file_name = util.encode_str(file_name)

        if not (act_name and act_type and file_name):
            showwarning('注意', '请完善活动信息！')
            return

        # 检查活动类型
        for item in act_type:
            if (not item.isalpha()) and item != "_":
                showwarning('注意', "活动类型只能由字母和下划线组成！")
                return
        
        # 检查文件名
        if not file_name.endswith('.py'):
            showwarning('注意', "脚本文件必须是.py文件！")
            return
        basename, ext = file_name.split('.')
        if ext.upper() != "PY":
            showwarning('注意', "脚本文件必须是.py文件！")
            return

        # 只能是字母数字下划线组成
        if re.search(r"\W", basename) is not None:
            showwarning('注意', "文件名只能由字母数字下划线组成！")
            return

        # 限制发放按钮
        self.act_frm.set_act_state()
        
        # 增加历史记录
        ctrl.add_history(act_name, act_type, file_name)

        selected_servers_info = "**".join(self.data.dump_selected_servers_info())        
        act_server_ids = self.data.get_act_server_ids()
        total_num = len(act_server_ids)
      
        # 显示进度条
        self._create_progress_frm(total_num)
        
        # 异步执行活动
        ctrl.do_active(act_server_ids, act_name, act_type, file_name, 
                       selected_servers_info, total_num)

        # 活动发出立刻清空服务器列表，防止误发
        self.data.clear_selected_servers()
        
    def choose_item(self):
        self.act_frm.choose_item()

    def add_selected_servers(self, company_id, server_ids):
        self.data.add_select_server(company_id, server_ids)
        self.show_add_servers()

    def start(self):
        self.mainloop()

class ActivityFrm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self._create_act_info_panel()
        self._create_selected_server_panel()
        self._create_msg_panel()

        self.set_nomal_state()

        self.pack(side = 'top', fill = 'y')


    def _create_act_info_panel(self):
        self.act_info_panel = ActInfoFrm(self)
        self.act_info_panel.pack(side = 'left')
        

    def _create_selected_server_panel(self):
        self.selected_server_panel = MessagePanel(self, '已选择：')
        self.selected_server_panel.pack(side = 'left', padx = 3)
    
    def _create_msg_panel(self):
        self.msg_panel = MessagePanel(self, '执行结果：')
        self.msg_panel.pack(side = 'left', padx = 3)


    def set_act_state(self):
        self.act_info_panel.set_act_state()

    def set_nomal_state(self):
        self.act_info_panel.set_nomal_state()
    
    def show_add_servers(self):
        global root
        self.selected_server_panel.set_v(root.data.dump_selected_servers_info())

    def get_act_info(self):
        return self.act_info_panel.get_act_info()

    def choose_item(self):
        history = ctrl.get_history(self.act_info_panel.get_act_name())
        if not history:
            return
        self.act_info_panel.set_act_type(history[0])
        self.act_info_panel.set_file_name(history[1])

    def add_msg(self, msg):
        self.msg_panel.add_msg(msg)


class ActInfoFrm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.entry_act_name = ActCombobox(self, '活动名称', '(如"春节送好礼")')
        self.entry_act_type = ActEntry(self, '活动类型', '(自定义，如"open_box"，"daily_recharge")')
        self.entry_file_name = ActEntry(self, '脚本名称', '(py文件，如"mingcheng.py")')
        self.btn_send = tk.Button(self, command = self.do_active)
        self.btn_send.pack(side = 'top', fill = 'x')
    
    def get_act_name(self):
        return self.entry_act_name.get_v().strip()
    
    def set_act_type(self, v):
        self.entry_act_type.set_v(v)
    
    def set_file_name(self, v):
        self.entry_file_name.set_v(v)

    def set_nomal_state(self):
        self.btn_send.config(state = 'normal', bg = 'grey', text = "执行".center(90, ' '))
    
    def set_act_state(self):
        self.btn_send.config(state = 'disabled', bg = 'red', 
                 text = '执行中，请稍等，注意千万不能关闭本应用！'.center(90, ' '))

    def get_act_info(self):
        return (self.entry_act_name.get_v().strip(),
                self.entry_act_type.get_v().strip(),
                self.entry_file_name.get_v().strip())

    def do_active(self):
        global root
        root.do_active()


class ProgressFrm(tk.Frame):
    def __init__(self, parent, num):
        tk.Frame.__init__(self, parent)
        self._num = num
        self.progressbar = ttk.Progressbar(self, length = 500,
                                       mode = 'indeterminate')
        self.label = tk.Label(self, text = "处理中")
        self.label.pack(side = 'left')
        self.progressbar.pack(side = 'left')
        self.progressbar.start()
        self._progressing = False
        self.pack(side = 'top', fill = 'y')

    def step(self):
        if not self._progressing:
            self.progressbar.stop()
            self.progressbar.config(maximum = self._num,
                                    mode = 'determinate')
            self.label.config(text = "执行进度：")
            self._progressing = True
        self.progressbar.step()

class ServersFrm(tk.Frame):
    def __init__(self, parent, c_id, server_list, c_name):
        tk.Frame.__init__(self, parent)
        self.c_id = c_id
        self.c_name = c_name
        self.servers = {}
        self._create_btn_frm()
        self._create_servers_frm(server_list)
        self.pack(side = 'top', fill = 'y')

    def _create_btn_frm(self):
        self.frm_btn = tk.Frame(self)
        self.btn_choose_all = tk.Button(self.frm_btn, text = '%s：全选' % self.c_name, command = self.select_all)
        self.btn_add = tk.Button(self.frm_btn, text = '添加', command = self._confirm_select)
        self.btn_choose_all.pack(side = 'left')
        self.btn_add.pack(side = 'left')
        self.frm_btn.pack(side = 'top', fill = 'x')

    def _create_servers_frm(self, server_list):
        self.frm_servers = tk.Frame(self)
        for index, (s_id, s_name) in enumerate(server_list):
            server = Server(self.frm_servers, s_name)
            server.grid(row = index%16, column = index/16, sticky = 'w')
            self.servers.setdefault(s_id, server)
        self.frm_servers.pack(side = 'top', fill = 'x')

    def _get_select_servers(self):
        ser_list = []
        for s_id, server in self.servers.iteritems():
            if server.is_selected():
                ser_list.append(s_id)
        return ser_list

    def _confirm_select(self):
        global root
        root.add_selected_servers(self.c_id, self._get_select_servers())

    def select_all(self):
        for server in self.servers.values():
            server.select()
        self.btn_choose_all.config(text = '%s：取消' % self.c_name, command = self.cancel_all)
            
    def cancel_all(self):
        for server in self.servers.values():
            server.cancel_select()
        self.btn_choose_all.config(text = '%s：全选' % self.c_name, command = self.select_all)

class Server(tk.Frame):
    def __init__(self, root, s_name):
        tk.Frame.__init__(self, root)
        self.v = tk.BooleanVar()
        self.check_btn = tk.Checkbutton(self, text = s_name, variable = self.v)
        self.check_btn.pack()
        
    def is_selected(self):
        return bool(self.v.get())
    
    def select(self):
        self.v.set(True)

    def cancel_select(self):
        self.v.set(False)


class Scrollbar(ttk.Scrollbar):
    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, first, last)

class MessagePanel(tk.LabelFrame):
    def __init__(self, parent, label):
        tk.LabelFrame.__init__(self, parent, text = label)
        self.v = tk.StringVar()
        self.list_box = tk.Listbox(self, height = 5, width = 25, activestyle = 'none', listvariable = self.v)

        self.y_scroll = Scrollbar(self, orient = tk.VERTICAL)
        self.x_scroll = Scrollbar(self, orient = tk.HORIZONTAL)
        self.list_box['yscrollcommand'] = self.y_scroll.set
        self.list_box['xscrollcommand'] = self.x_scroll.set
        self.y_scroll['command'] = self.list_box.yview
        self.x_scroll['command'] = self.list_box.xview
        self.y_scroll.grid(row = 0, column = 1, sticky = tk.N+tk.S, rowspan = 2)
        self.x_scroll.grid(row = 1, column = 0, sticky = tk.E+tk.W)
        self.list_box.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)

    def add_msg(self, msg):
        self.list_box.insert('end', msg)
        self.list_box.see('end')

    def set_v(self, l):
        self.v.set(tuple(l))
        self.list_box.see('end')
        
    def get_v(self):
        return eval(self.v.get())
        
           
class ActInput(tk.Frame):
    def __init__(self, parent, lable, tip = ""):
        tk.Frame.__init__(self, parent)
        self.name = tk.Label(self, text = '%s：' % lable, padx = 3)
        self.v = tk.StringVar()
        self.tip = tk.Label(self, text = tip, padx = 3)
        self.name.pack(side = 'left')
        self.init_input()
        self.tip.pack(side = 'left')
        self.pack(side = 'top', fill = 'x')

    def init_input(self):
        pass
        
    def get_v(self):
        return util.encode_str(self.v.get())

    def set_v(self, val):
        self.v.set(val)

    def clear(self):
        self.v.set('')

class ActCombobox(ActInput):
    def init_input(self):
        self.combobox = ttk.Combobox(self, textvariable = self.v,
                                     width = 50, postcommand = self._init_items)
        self.combobox.bind('<<ComboboxSelected>>', self._choose_item)
        self.combobox.pack(side = 'left')

    def _init_items(self):
        items = ctrl.get_history_items()
        if not items:
            return
        self.combobox.configure(values = items)

    def _choose_item(self, event):
        global root
        root.choose_item()


class ActEntry(ActInput):
    def init_input(self):
        self.entry = tk.Entry(self, textvariable = self.v,
                              width = 30)
        self.entry.pack(side = 'left')
