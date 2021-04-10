import subprocess
from threading import Thread
import shlex
import sys
import io
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import xlsxwriter
import socket
import struct
import netifaces
import csv
import logging

# import openpyxl
# from openpyxl.chart import (
#    LineChart,
#    Reference,
#    Series,
# )
# from openpyxl.chart.axis import DateAxis

# tshark -i 1 -a duration:60 -d udp.port==%1,rtp -qz rtp,streams >> iptv.log
# tshark -D

# ========================= RTP Streams ========================
#   Start time      End time     Src IP addr  Port    Dest IP addr  Port       SSRC          Payload  Pkts         Lost   Max Delta(ms)  Max Jitter(ms) Mean Jitter(ms) Problems?
#     0.000000     60.475994   192.168.33.11  2002     230.100.1.2  2002 0x1E8F828C  MPEG-II streams 47149     0 (0.0%)            3.20            0.52            0.34
# ==============================================================

# logging setting,10=DEBUG,20=INFO
output_logging = 20


class video_analyzer(tk.Tk):
    total_pkts = 0
    total_loss = 0
    latest_pkts = 0
    latest_loss = 0
    iface = 0
    iface_name = ''
    iface_id = {}
    iface_ipv4 = {}
    port = 0
    channel = ''
    criteria = 0
    pkt_list = []
    card_list = []
    output_list = []
    proc_state = False
    thread = 0
    alive_id = 0
    stop_id = 0
    currentValue = 0
    sock = 0

    def __init__(self, top=None):
        super().__init__()
        # Get tshark interface list

        self.start_logging()
        self.interface()
        self.read_csv('default.txt')

        self.geometry("300x350")
        self.title("IPTV Packet Monitor")

        self.Label0 = tk.Label(top, text='Network Card:', anchor='w', justify='left')
        self.Label0.place(relx=0.05, rely=0.1, height=15, width=150)

        self.Label1 = tk.Label(top, text='Multicast Channel:', anchor='w', justify='left')
        self.Label1.place(relx=0.05, rely=0.2, height=15, width=150)

        self.Label2 = tk.Label(top, text='UDP Port:', anchor='w', justify='left')
        self.Label2.place(relx=0.05, rely=0.3, height=15, width=150)

        self.Label3 = tk.Label(top, text='Total Packets:', anchor='w', justify='left')
        self.Label3.place(relx=0.05, rely=0.4, height=15, width=150)

        self.Label4 = tk.Label(top, text='Total Packets Loss:', anchor='w', justify='left')
        self.Label4.place(relx=0.05, rely=0.5, height=15, width=150)

        self.Label5 = tk.Label(top, text='Criteria:', anchor='w', justify='left')
        self.Label5.place(relx=0.05, rely=0.6, height=15, width=150)

        self.Label5 = tk.Label(top, text='Test Result:', anchor='w', justify='left')
        self.Label5.place(relx=0.05, rely=0.7, height=15, width=150)

        self.NetworkText = ttk.Combobox(top, width=334, values=self.card_list)
        self.NetworkText.current(0)
        self.NetworkText.place(relx=0.55, rely=0.08, relheight=0.1, relwidth=0.4)

        self.ChannelText = tk.Entry(top, width=334)
        self.ChannelText.place(relx=0.55, rely=0.18, relheight=0.1, relwidth=0.4)

        if self.channel=='':
            self.ChannelText.insert(tk.END, '230.100.1.2')
        else:
            self.ChannelText.insert(tk.END, self.channel)

        self.PortText = tk.Entry(top, width=334)
        self.PortText.place(relx=0.55, rely=0.28, relheight=0.1, relwidth=0.4)
        if self.port==0:
            self.PortText.insert(tk.END, '2002')
        else:
            self.PortText.insert(tk.END, self.port)

        self.PacketText = tk.Entry(top, width=334)
        self.PacketText.place(relx=0.55, rely=0.38, relheight=0.1, relwidth=0.4)
        self.PacketText.insert(tk.END, '0')

        self.LossText = tk.Entry(top, width=334)
        self.LossText.place(relx=0.55, rely=0.48, relheight=0.1, relwidth=0.4)
        self.LossText.insert(tk.END, '0')

        self.CriteriaText = tk.Entry(top, width=334)
        self.CriteriaText.place(relx=0.55, rely=0.58, relheight=0.1, relwidth=0.4)

        if self.criteria==0:
            self.CriteriaText.insert(tk.END, '0.0001')
        else:
            self.CriteriaText.insert(tk.END, self.criteria)

        self.ResultText = tk.Entry(top, width=334)
        self.ResultText.place(relx=0.55, rely=0.68, relheight=0.1, relwidth=0.4)
        self.ResultText.insert(tk.END, 'N/A')

        self.StartButton = tk.Button(top, pady="0", text='Start', command=self.start_btn)
        self.StartButton.place(relx=0.15, rely=0.81, height=31, width=47)
        self.StartButton.config(state=tk.NORMAL)

        self.StopButton = tk.Button(top, pady="0", text='Stop', command=self.stop_btn)
        self.StopButton.place(relx=0.4, rely=0.81, height=31, width=47)
        self.StopButton.config(state=tk.DISABLED)

        self.ReportButton = tk.Button(top, pady="0", text='Report', command=self.report_btn)
        self.ReportButton.place(relx=0.7, rely=0.81, height=31, width=55)
        self.ReportButton.config(state=tk.DISABLED)

        self.progressbar = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate")
        self.progressbar.pack(side=tk.BOTTOM)

    def read_csv(self, filename):
        table = []
        try:

            with open(filename) as csvfile:
                reader = csv.reader(csvfile)  # change contents to floats
                for row in reader:  # each row is a list
                    table.append(row)

            self.channel = table[0]
            self.port = table[1]
            self.criteria = table[2]
            logging.info('Read default value')
        except:
            logging.info('No default value found')

    def start_logging(self):
        # Enable the logging to console and file
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=output_logging,
                            format='%(asctime)s: [%(levelname)s] %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='iptv_monitor.log',
                            filemode='w')

        console = logging.StreamHandler()
        console.setLevel(output_logging)
        formatter = logging.Formatter('%(levelname)-4s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def start_btn(self):
        self.output_list = []
        self.total_pkts = 0
        self.total_loss = 0
        self.latest_pkts = 0
        self.latest_loss = 0

        logging.info('Start IPTV Monitor')
        self.PacketText.delete(0, 'end')
        self.PacketText.insert(tk.END, self.total_pkts)
        self.LossText.delete(0, 'end')
        self.LossText.insert(tk.END, self.total_loss)
        self.ResultText.delete(0, 'end')
        self.ResultText.insert(tk.END, 'Ongoing')

        self.StartButton.config(state=tk.DISABLED)
        self.StopButton.config(state=tk.NORMAL)
        self.ReportButton.config(state=tk.NORMAL)
        self.criteria = self.CriteriaText.get()
        self.channel = self.ChannelText.get()
        self.port = self.PortText.get()
        self.iface = self.NetworkText.current() + 1
        self.iface_name = self.NetworkText.get()

        logging.info('iface_name: %s', self.iface_name.replace('\n', ''))
        logging.info('channel: %s', self.channel)
        logging.info('port: %s', self.port)
        logging.info('criteria: %s', self.criteria)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.iface_ipv4[self.iface_name], int(self.port)))

        self.igmp_send('join')
        self.poll_thread()
        self.update_idletasks()

    def poll_thread(self):
        logging.debug('[DEBUG] thread checking: %s', self.thread)
        state = self.StartButton['state']
        if self.proc_state == False and state != tk.NORMAL:
            self.currentValue = 0
            self.progressbar["value"] = self.currentValue
            self.progressbar.update()
            logging.info("Start capture packet for 60s")
            self.proc_state = True
            self.thread = capture(self.iface, self.port)

        if self.thread.is_alive():
            self.currentValue = self.currentValue + 1.6
            self.progressbar["value"] = self.currentValue
            self.progressbar.update()
            self.alive_id = self.after(1000, lambda: self.poll_thread())
        else:
            # print('[DEBUG] thread terminated',self.thread)

            self.currentValue = 100
            self.progressbar["value"] = self.currentValue
            self.progressbar.update()

            self.proc_state = False
            self.latest_pkts = self.thread.now_pkts
            self.latest_loss = self.thread.now_loss
            self.update_data()
            self.update_idletasks()
            app.update()
            # self.igmp_send('join')
            self.stop_id = self.after(1000, lambda: self.poll_thread())

    def update_data(self):
        result = {}

        now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.total_pkts = self.total_pkts + self.latest_pkts
        self.total_loss = self.total_loss + self.latest_loss

        result['time'] = now_time
        result['channel'] = self.channel
        result['port'] = self.port
        result['packets'] = self.latest_pkts
        result['loss'] = self.latest_loss
        result['total_packets'] = self.total_pkts
        result['total_loss'] = self.total_loss
        result['criteria'] = self.criteria

        self.PacketText.delete(0, 'end')
        self.PacketText.insert(tk.END, self.total_pkts)
        self.LossText.delete(0, 'end')
        self.LossText.insert(tk.END, self.total_loss)
        self.ResultText.delete(0, 'end')

        logging.info("New Packet: %s", self.latest_pkts)
        logging.info("New Packet Loss: %s", self.latest_loss)
        logging.info("Total Packet: %s", self.total_pkts)
        logging.info("Total Packet Loss: %s", self.total_loss)
        if self.total_pkts != 0:
            logging.info("Total loss : %s", (self.total_loss / self.total_pkts) * 100)
            pass
        else:
            logging.info("Total loss : 0.0")
            pass

        if self.latest_pkts != 0:
            test = (float(self.latest_pkts) * float(self.criteria))
            if float(self.latest_loss) > float(test):
                result['result'] = "Failed"
            else:
                result['result'] = "Passed"
        else:
            result['result'] = "N/A"

        if self.total_pkts != 0:
            test = (float(self.total_pkts) * float(self.criteria))
            if float(self.total_loss) > float(test):
                self.ResultText.insert(tk.END, 'Failed')
                result['sum_result'] = 'Failed'
            else:
                self.ResultText.insert(tk.END, 'Passed')
                result['sum_result'] = 'Passed'
        else:
            self.ResultText.insert(tk.END, 'N/A')
            result['sum_result'] = 'N/A'

        self.output_list.append(result)

    def report_btn(self):
        self.output_xls()

    def stop_btn(self):
        logging.info('Stop IPTV Monitor')
        self.StartButton.config(state=tk.NORMAL)
        self.StopButton.config(state=tk.DISABLED)
        self.ReportButton.config(state=tk.DISABLED)
        try:
            self.thread.task.terminate()
            self.thread.join()
        except:
            logging.debug('thread cant be terminated')
        try:
            self.after_cancel(self.alive_id)
        except:
            logging.debug('No alive id found: %s', self.alive_id)
        try:
            self.after_cancel(self.stop_id)
        except:
            logging.debug('No stop id found: %s', self.stop_id)

        self.igmp_send('leave')
        self.sock.close()
        self.output_xls()

    def output_xls(self):
        logging.info('Test Report is generated')

        data_row = 0
        data_col = 0

        xls_title = ['time', 'channel', 'port', 'packets', 'loss', 'total_packets', 'total_loss', 'criteria', 'result',
                     'sum_result']
        filename = self.channel + '_' + str(self.port) + '_' + 'realtime_log.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        # workbook = openpyxl.Workbook()

        for name in xls_title:
            worksheet.write(data_row, data_col, name)
            data_col += 1

        data_row += 1
        data_col = 0
        for entry in self.output_list:
            for name in xls_title:
                worksheet.write(data_row, data_col, entry[name])
                data_col += 1
            data_row += 1
            data_col = 0

        chart1 = workbook.add_chart({'type': 'line'})
        chart1.add_series({
            'categories': '=Sheet1!$A$2:$A$' + str(len(self.output_list) + 1),
            'values': '=Sheet1!$E$2:$E$' + str(len(self.output_list) + 1),
            'line': {'color': 'red'},
            'name': 'Packet Loss Chart',
        })
        chart1.set_size({'width': 1200, 'height': 400})
        chart1.set_x_axis({'name': 'Time'})
        chart1.set_y_axis({'name': 'Packet Loss'})
        worksheet.insert_chart('M2', chart1)

        chart2 = workbook.add_chart({'type': 'line'})
        chart2.add_series({
            'categories': '=Sheet1!$A$2:$A$' + str(len(self.output_list) + 1),
            'values': '=Sheet1!$G$2:$G$' + str(len(self.output_list) + 1),
            'line': {'color': 'red'},
            'name': 'Total Packet Loss Chart',
        })
        chart2.set_size({'width': 1200, 'height': 400})
        chart2.set_x_axis({'name': 'Time'})
        chart2.set_y_axis({'name': 'Packet Loss'})
        worksheet.insert_chart('M25', chart2)

        workbook.close()

        # chart = LineChart()
        # chart.title = "Packet Loss vs Time Chart"
        # chart.style = 13
        # chart.y_axis.title = 'Loss Packets'
        # chart.x_axis.title = 'Time'
        # chart.x_axis.crosses = 'min'
        # chart.x_axis.majorTickMark = "out"
        # chart.y_axis.crossAx = 500
        # chart.x_axis = DateAxis()
        # chart.x_axis.number_format = 'yyyy-mm-dd h:mm:ss'
        # hart.x_axis.majorTimeUnit = "days"

        # chart.width = 20
        # chart.height = 10

        # x_data = Reference(worksheet, min_col=1, min_row=2, max_row=worksheet.max_row)
        # x_data = Reference(worksheet, range_string='Sheet!$A$2:$A$100')
        # y_data = Reference(worksheet, min_col=5, min_row=1, max_row=worksheet.max_row)
        # chart.set_categories(x_data)
        # series = Series(y_data,x_data,title_from_data=True)
        # chart.add_data(y_data, titles_from_data=True)
        # chart.series.append(series)
        # worksheet.add_chart(chart, "L3")

        # workbook.save(self.channel + '_' + str(self.port) + '_' + 'realtime_log.xlsx')
        # workbook.close()

    def get_ipv4(self, id):
        # iface_list = netifaces.interfaces()
        try:
            ipv4_addr_set = netifaces.ifaddresses(id)
            if netifaces.AF_INET in ipv4_addr_set:
                ipv4_addr = ipv4_addr_set[netifaces.AF_INET][0]['addr']
            else:
                ipv4_addr = '0.0.0.0'
        except:
            logging.info('network card not found: %s', id)
            ipv4_addr = '0.0.0.0'
        # print(iface_list)
        logging.info('ip address = %s', ipv4_addr)
        return ipv4_addr

    def igmp_send(self, type):

        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.INADDR_ANY)
        mreq = struct.pack("4s4s", socket.inet_aton(self.channel), socket.inet_aton(self.iface_ipv4[self.iface_name]))
        if type == 'join':
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            logging.info('Send IGMP Join to channel: %s', self.channel)
        else:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
            logging.info('Send IGMP Leave to channel: %s', self.channel)

    def interface(self):
        cmd = ".\\\\tshark\\\\tshark.exe -D"
        args = shlex.split(cmd)
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(args, shell=False, startupinfo=si, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        process.wait()
        for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
            logging.info("Network card: %s" % line.rstrip())
            if_name = line.split('(')[1].replace(')', '')
            self.iface_id[if_name] = line.split()[1].split('_')[1]
            self.card_list.append(if_name)
            self.iface_ipv4[if_name] = self.get_ipv4(self.iface_id[if_name])


class capture(Thread):
    def __init__(self, iface, port):
        super().__init__()
        self.iface = iface
        self.port = port
        self.now_pkts = 0
        self.now_loss = 0
        self.daemon = True
        self.start()
        self.task = 0

    def run(self):
        logging.info("Testing if tshark works. Using {}".format(self.iface))
        devnull = open(os.devnull, 'wb')
        cmd = ".\\\\tshark\\\\tshark -i " + str(self.iface) + " -a duration:60 -f \"udp port " + str(
            self.port) + "\" -d udp.port==" + str(self.port) + ",rtp -qz rtp,streams"
        args = shlex.split(cmd)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.task = subprocess.Popen(args, shell=False, startupinfo=si, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
        self.task.wait()
        for line in io.TextIOWrapper(self.task.stdout, encoding="utf-8"):
            # print("test: %s" % line.rstrip())
            if str(self.port) in line:
                tmp = line.split()
                self.now_pkts = int(tmp[9])
                self.now_loss = int(tmp[10])
        self.task.terminate()


if __name__ == '__main__':
    app = video_analyzer()
    app.mainloop()
    sys.exit(0)
