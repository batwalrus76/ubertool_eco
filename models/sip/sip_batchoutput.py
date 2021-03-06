"""
.. module:: sip_batchoutput
   :synopsis: A useful module indeed.
"""

from django.views.decorators.http import require_POST

import csv
import sip_model,sip_tables

import logging
from threading import Thread
import Queue
from collections import OrderedDict

logger = logging.getLogger("SIPBatchOutput")

chemical_name=[]
species_tested_bird=[]
species_tested_mammal=[]
bodyweight_quail=[]
bodyweight_duck=[]
bodyweight_bird_other=[]
bodyweight_rat=[]
bodyweight_tested_mammal_other=[]
avian_ld50=[]
mammalian_ld50=[]
solubility=[]
bodyweight_assessed_bird=[]
mineau_scaling_factor=[]
bodyweight_assessed_mammal=[]
noaec_d=[]
noaec_q=[]
noaec_o=[]
noael_mammal_water=[]
Species_of_the_bird_NOAEC_CHOICES=[]
noael_avian_water=[]

######Pre-defined outputs########
dose_bird_out = []
dose_mamm_out = []
at_bird_out = []
at_mamm_out = []
det_out = []
act_out = []
acute_bird_out = []
acuconb_out = []
acute_mamm_out = []
acuconm_out = []
chron_bird_out = []
chronconb_out = []
chron_mamm_out = []
chronconm_out = []

jid_all = []
jid_batch = []
sip_all = []
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
            chemical_name.append(str(row_inp[0]))
            species_tested_bird.append(float(row_inp[1]))
            species_tested_mammal.append(float(row_inp[2]))
            bodyweight_quail.append(float(row_inp[3]))
            bodyweight_duck.append(float(row_inp[4]))
            bodyweight_bird_other.append(float(row_inp[5])) 
            bodyweight_rat.append(float(row_inp[6]))
            bodyweight_tested_mammal_other.append(float(row_inp[7]))
            solubility.append(float(row_inp[8]))
            avian_ld50.append(float(row_inp[9])) 
            mammalian_ld50.append(float(row_inp[10]))
            bodyweight_assessed_bird.append(float(row_inp[11]))
            mineau_scaling_factor.append(float(row_inp[12]))
            bodyweight_assessed_mammal.append(float(row_inp[13]))
            noaec_d.append(float(row_inp[14]))
            noaec_q.append(float(row_inp[15]))
            noaec_o.append(float(row_inp[16]))
            noael_mammal_water.append(float(row_inp[17]))
            Species_of_the_bird_NOAEC_CHOICES.append(str(row_inp[18]))
            if Species_of_the_bird_NOAEC_CHOICES[iter] == '1':
                noael_avian_water.append(float(row_inp[14]))
            elif Species_of_the_bird_NOAEC_CHOICES[iter] == '2':
                noael_avian_water.append(float(row_inp[15]))
            elif Species_of_the_bird_NOAEC_CHOICES[iter] == '3':
                noael_avian_water.append(float(row_inp[16]))

            logger.info(chemical_name)
            logger.info(species_tested_bird)
            logger.info(species_tested_mammal)
            logger.info(bodyweight_quail)
            logger.info(bodyweight_duck)
            logger.info(bodyweight_bird_other)
            logger.info(bodyweight_rat)
            logger.info(bodyweight_tested_mammal_other)
            logger.info(solubility)
            logger.info(avian_ld50)
            logger.info(mammalian_ld50)
            logger.info(bodyweight_assessed_bird)
            logger.info(mineau_scaling_factor)
            logger.info(bodyweight_assessed_mammal)
            logger.info(noaec_d)
            logger.info(noaec_q)
            logger.info(noaec_o)
            logger.info(noael_mammal_water)
            logger.info(Species_of_the_bird_NOAEC_CHOICES)

            sip_obj = sip_model.sip(True,True,'batch',chemical_name[iter], species_tested_bird[iter], species_tested_mammal[iter], bodyweight_quail[iter],
                            bodyweight_duck[iter], bodyweight_bird_other[iter], bodyweight_rat[iter], bodyweight_tested_mammal_other[iter], solubility[iter], avian_ld50[iter],
                            mammalian_ld50[iter], bodyweight_assessed_bird[iter], mineau_scaling_factor[iter], bodyweight_assessed_mammal[iter], noaec_d[iter], noaec_q[iter], noaec_o[iter], Species_of_the_bird_NOAEC_CHOICES[iter], noael_mammal_water[iter])

            dose_bird_out.append(sip_obj.dose_bird_out)
            dose_mamm_out.append(sip_obj.dose_mamm_out)
            at_bird_out.append(sip_obj.at_bird_out)
            at_mamm_out.append(sip_obj.at_mamm_out)
            det_out.append(sip_obj.det_out)
            act_out.append(sip_obj.act_out)
            acute_bird_out.append(sip_obj.acute_bird_out)
            acuconb_out.append(sip_obj.acuconb_out)
            acute_mamm_out.append(sip_obj.acute_mamm_out)
            acuconm_out.append(sip_obj.acuconm_out)
            chron_bird_out.append(sip_obj.chron_bird_out)
            chronconb_out.append(sip_obj.chronconb_out)
            chron_mamm_out.append(sip_obj.chron_mamm_out)
            chronconm_out.append(sip_obj.chronconm_out)

            jid_all.append(sip_obj.jid)
            sip_all.append(sip_obj)    
            if iter == 0:
                jid_batch.append(sip_obj.jid)

            batch_header = """
                <div class="out_">
                    <br><H3>Batch Calculation of Iteration %s:</H3>
                </div>
                """%(iter + 1)

            out_html_temp = batch_header + sip_tables.table_all(sip_obj)
            out_html_all[iter]=out_html_temp

def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    header = reader.next()
    # logger.info(header)
    i=0
    iter_html=""
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

    html_timestamp = sip_tables.timestamp("", jid_batch[0])
    out_html_all_sort = OrderedDict(sorted(out_html_all.items()))
    sum_html = sip_tables.table_all_sum(sip_tables.sumheadings, sip_tables.tmpl, bodyweight_quail,bodyweight_duck,bodyweight_bird_other,bodyweight_rat,bodyweight_tested_mammal_other,solubility,
                    avian_ld50,mammalian_ld50,bodyweight_assessed_bird,mineau_scaling_factor,bodyweight_assessed_mammal,noael_avian_water,noael_mammal_water,
                    dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out)

    return html_timestamp + sum_html + "".join(out_html_all_sort.values())


@require_POST
def sipBatchOutputPage(request):
    thefile = request.FILES['upfile']
    iter_html=loop_html(thefile)

    return iter_html, sip_all, jid_batch