from2=[1,2,3]
to2=[1,2,3]
mediatype=[4,4,4]
i=len(from2)
kk=[]
for j in range(i):
   a= from2[j]

   kk.append(a)
jj=','.join(str(i) for i in kk)

print jj
    # json_mail={
    #                             "operationtype": 0,
    #                             "esc_period": 0,
    #                             "esc_step_from": i[0],
    #                             "esc_step_to": i[0],
    #                             "evaltype": 0,
    #                             "opmessage_grp": [
    #                                 {
    #                                     "usrgrpid": "7"
    #                                 }
    #                             ],
    #                             "opmessage": {
    #                                 "default_msg": 1,
    #                                 "mediatypeid":i[0],
    #                             }
    #                         }

