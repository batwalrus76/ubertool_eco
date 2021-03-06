"""
.. module:: rice_batchoutput
   :synopsis: A useful module indeed.
"""

from django.views.decorators.http import require_POST

from StringIO import StringIO

import terrplant_model,terrplant_tables

import logging
import csv
from threading import Thread
import Queue
from collections import OrderedDict

logger = logging.getLogger("RiceBatchPage")

chemical_name=[]
mai=[]
a=[]
dsed=[]
pb=[]
dw=[]
osed=[]
kd=[]

######Pre-defined outputs########
msed=[]
vw=[]
mai1=[]
cw=[]

jid_all = []
jid_batch = []
rice_all = []
all_threads = []
out_html_all = {}
job_q = Queue.Queue()
thread_count = 10


def html_table(row_inp_all):
    while True:
        row_inp_temp_all = row_inp_all.get()
        if row_inp_temp_all is None:
            break
        else:
            row_inp = row_inp_temp_all[0]
            iter = row_inp_temp_all[1]

            logger.info("iteration: " + str(iter))

            chemical_name_temp=str(row_inp[0])
            chemical_name.append(chemical_name_temp)
            mai_temp=float(row_inp[1])
            mai.append(mai_temp)
            a_temp=float(row_inp[2])
            a.append(a_temp)
            dsed_temp= float(row_inp[3])
            dsed.append(dsed_temp)
            pb_temp=float(row_inp[4])
            pb.append(pb_temp)
            dw_temp=float(row_inp[5])
            dw.append(dw_temp)
            osed_temp=float(row_inp[6])
            osed.append(osed_temp)
            kd_temp=float(row_inp[7])       
            kd.append(kd_temp) 

            rice_obj = rice_model.rice(True,True,"batch",chemical_name_temp, mai_temp, dsed_temp, a_temp, pb_temp, dw_temp, osed_temp, kd_temp)
            logger.info("===============")
            msed.append(rice_obj.msed)
            vw.append(rice_obj.vw)
            mai1.append(rice_obj.mai1)
            cw.append(rice_obj.cw)

            jid_all.append(rice_obj.jid)
            rice_all.append(rice_obj)    
            if iter == 1:
                jid_batch.append(rice_obj.jid)

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(iter)
                
            html_temp = rice_tables.table_all(rice_obj)
            out_html_temp = batch_header + html_temp
            out_html_all[iter]=out_html_temp

                
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    # logger.info(header)
    i=1
    ####Create a job queue and add each row of batch temeplate file as a task into it
    for row in reader:
        job_q.put([row, i])
        i=i+1

    all_threads = [Thread(target=html_table, args=(job_q, )) for j in range(thread_count)]
    for x in all_threads:
        x.start()
    for x in all_threads:
        job_q.put(None)
    for x in all_threads:
        x.join()

    html_timestamp = rice_tables.timestamp("", jid_batch[0])
    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))
    sum_output_cw="""<table border="1" style="display: none"><tr>
                    <td id="cw_out_raw" data-val='%s' style="display: none"></td>                                                                              
                    <td>&microg/L</td>
                </tr></table><br>""" %(cw)             
    sum_fig="""<H3>Historgram</H3><br>
               <div id="calculate">
                   <div class="block">
                        <label>How many buckets (Default is based on Sturgis rule):</label>
                        <input type="text" id="buckets" value=%s></div><br>
                        <button type="submit" id="calc">Calculate Historgram</button></div><br>
                <div id="chart1"></div><br>"""%(int(1+3.3*np.log10(len(cw)))) #number of bins coming from Sturgis rule         
    sum_html = rice_tables.table_sum_all(rice_tables.sumheadings, rice_tables.tmpl, mai, dsed, a, pb, dw, osed, kd, msed, vw, mai1, cw)
    return  html_timestamp + sum_html+sum_output_cw+sum_fig + "".join(out_html_all_sort.values())

@require_POST              
def RiceBatchOutputPage(request):
    thefile = request.FILES['upfile']
    iter_html=loop_html(thefile)

    return iter_html, terr_all, jid_batch

