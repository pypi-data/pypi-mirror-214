from ...method.callservice import *
from ...method.checkpath import *
import json , shutil

class ProcessRecovery():
    def __init__(self,payload):
        self.success = 0  ####จำนวนที่สำเร็จใน
        self.fail = 0  ####จำนวนที่ไม่สำเร็จใน
        self.losemessage = []  ####ข้อความทีไม่่สำเร็จใน
        self.recover_count = 0
        self.recover = []
        self.payload = payload
        ### เก็บข้อมูลการทำงานรอบ recover
        self.success_recovery_message = []
        self.success_recovery = 0
        self.fail_recovery_message = []
        self.fail_recovery = 0

    def recover_check(self, path_recover_check , path_recover , path_check_now , output_local_path , output_remote_path , date_now , time_now , path_history , file):
        try:
            filename = str(file.split('.')[0])
            recover_data = json.loads(open(path_check_now + '/' + file, 'r',encoding='UTF-8').read())
            transactionCode = str(recover_data["transactionCode"])
            recheck_trans = checkStatus(self.payload,transactionCode,0)
            if recheck_trans["status"] == "OK":
                self.success_recovery += 1
                self.success_recovery_message.append({
                    "inputDate": date_now,
                    "batchName": filename,
                    "invoiceNo": filename,
                    "message": "การทำงานสำเร็จ"
                })
                save_pdf = saveFile(recheck_trans['pdfURL'], output_local_path + '/PDF/', filename+'.pdf', 0)
                if save_pdf["status"] == "OK":
                    print(str(date_now + time_now) + '>> ' + filename + ' Save PDF success.')
                    shutil.copy(output_local_path + '/PDF/' + filename + '.pdf', output_remote_path + '/PDF/' + filename + '.pdf')
                    print(str(date_now + time_now) + '>> ' + str(filename) + ' Put file.pdf success.')
                    output_pdf = True
                else:
                    output_pdf = False
                    print(str(date_now + time_now) + '>> ' + filename + ' Save PDF fail. : ' + str(save_pdf["errorMessage"]))
                save_xml = saveFile(recheck_trans['xmlURL'], output_local_path + '/XML/', filename+'.xml', 0)
                if save_xml["status"] == "OK":
                    print(str(date_now + time_now) + '>> ' + filename + ' Save XML success.')
                    shutil.copy(output_local_path + '/XML/' + filename + '.xml', output_remote_path + '/XML/' + filename + '.xml')
                    print(str(date_now + time_now) + '>> ' + str(filename) + ' Put file.pdf success.')
                    output_xml = True
                else:
                    output_xml = False
                    print(str(date_now + time_now) + '>> ' + filename + ' Save XML fail. : ' + str(save_xml["errorMessage"]))
                if not output_pdf or not output_xml:
                    check_path(path_recover + '/save/' + date_now + '/')
                    with open(path_recover + '/save/'+ date_now + '/' + str(file), 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover save
                        recover_file.write(json.dumps({"transactionCode": transactionCode}, indent=4, sort_keys=False,ensure_ascii=False))
                try:
                    os.remove(path_check_now+"/"+file)
                    os.remove(path_recover_check + "/" + file)
                except:
                    pass
            elif recheck_trans['errorCode'] == "ER021" or recheck_trans['errorCode'] == "EX01" or recheck_trans['errorCode'] == "PC010" or recheck_trans['errorCode'] == "ERC001" or recheck_trans['errorCode'] == "ER004" or (recheck_trans['errorCode'] == "ER400" and recheck_trans['errorMessage'] == "Not found this transactionCode") or recheck_trans['errorCode'] == "PC001" or recheck_trans['errorCode'] == "ERPC002":
                shutil.move(path_check_now + file, path_recover_check + file)
            elif recheck_trans['errorCode'] == "ER019" or (recheck_trans['errorCode'] == "ER999" and payload['SellerTaxid'] not in recheck_trans['errorMessage']) or recheck_trans['errorCode'] == "ER001" or recheck_trans['errorCode'] == "AU045":
                check_path(path_recover+ '/sign/'+ date_now + '/')
                try:
                    shutil.copy(path_history + filename + '.csv', path_recover+ '/sign/'+ date_now + '/' + filename + '.csv')
                except:
                    try:
                        shutil.copy(path_history + filename + '.CSV', path_recover+ '/sign/'+ date_now + '/' + filename + '.CSV')
                    except:
                        pass
                os.remove(path_check_now+"/"+file)
            else:
                self.fail_recovery += 1
                self.fail_recovery_message.append({
                    "inputDate": date_now,
                    "batchName": filename,
                    "invoiceNo": filename,
                    "errorCode": str(recheck_trans['errorCode']),
                    "errorMessage": str(recheck_trans['errorMessage'])
                })
                os.remove(path_check_now+"/"+file)
        except Exception as e:
            shutil.move(path_check_now + file, path_recover_check + file)

    def recover_sign(self, split_data_one_to_one , local_pdf_output , remote_pdf_output , local_xml_output , remote_xml_output , path_single_file , payload_user , date_now , time_now , path_recover):
        for fullname in split_data_one_to_one:
            name = str(fullname).split('.')[0]
            try:
                ServiceCode = "S06"
                service = serviceSigningS06(self.payload, fullname, name + '.pdf' ,  path_single_file, 0, ServiceCode)
                if service['status'] == 'OK':
                    print(str(date_now + time_now) + '>> ' + str(name) + ' Service signing success.')
                    save_pdf = saveFile(service['pdfURL'], local_pdf_output, name + '.pdf', 0)
                    if save_pdf['status'] == 'OK':
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.pdf success.')
                        shutil.copy(local_pdf_output + '/' + name + '.pdf', remote_pdf_output + '/' + name + '.pdf')
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Put file.pdf success.')
                        pdf_result = 'OK'  ### เก็บ สถานะการทำงานในส่วน PDF
                    else:
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.pdf failed. : ' + str(save_pdf['errorMessage']))
                        pdf_result = 'ER'  ### เก็บ สถานะการทำงานในส่วน PDF
                    save_xml = saveFile(service['xmlURL'], local_xml_output, name + '.xml', 0)
                    if save_xml['status'] == 'OK':
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.xml success.')
                        shutil.copy(local_xml_output + '/' + name + '.xml', remote_xml_output + '/' + name + '.xml')
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Put file.xml success.')
                        xml_result = 'OK'  ### เก็บ สถานะการทำงานในส่วน XML
                    else:
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.xml failed. : ' + str(save_xml['errorMessage']))
                        xml_result = 'ER'  ### เก็บ สถานะการทำงานในส่วน XML
                    ##########นับว่า สำเร็จ หรือ ไม่สำเร็จ #######
                    if pdf_result == 'OK' and xml_result == 'OK':  ### ถ้าสถานะของทั้ง xml และ pdf สำเร็จทั้งคู่จึงจะนับว่า invoice นั้นสำเร็จ
                        self.success = self.success + 1
                        self.success_recovery += 1
                        self.success_recovery_message.append({
                            "inputDate": date_now,
                            "batchName": name,
                            "invoiceNo": name,
                            "message": "การทำงานสำเร็จ"
                        })
                    else:
                        check_path(path_recover + '/save/' + date_now + '/')
                        with open(path_recover + '/save/' + date_now + '/' + name + '.txt', 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover save
                            recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                elif service['status'] == 'PC':
                    pc_result = checkStatus(payload_user, service['transactionCode'], 0)
                    if pc_result['status'] == 'OK':
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Service signing success.')
                        save_pdf_pc = saveFile(pc_result['pdfURL'], local_pdf_output, name + '.pdf', 0)
                        if save_pdf_pc['status'] == 'OK':
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.pdf success.')
                            shutil.copy(local_pdf_output + '/' + name + '.pdf',remote_pdf_output + '/' + name + '.pdf')
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Put file.pdf success.')
                            pc_pdf_result = 'OK'  ### เก็บสถานะการทำงานในส่วน PDF
                        else:
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.pdf failed. : ' + str(save_pdf_pc['errorMessage']))
                            pc_pdf_result = 'ER'  ### เก็บสถานะการทำงานในส่วน PDF
                        save_xml_pc = saveFile(pc_result['xmlURL'], local_xml_output, name + '.xml', 0)
                        if save_xml_pc['status'] == 'OK':
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.xml success.')
                            shutil.copy(local_xml_output + '/' + name + '.xml',remote_xml_output + '/' + name + '.xml')
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Put file.xml success.')
                            pc_xml_result = 'OK'  ### เก็บสถานะการทำงานในส่วน XML
                        else:
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Save file.xml failed. : ' + str(save_pdf_pc['errorMessage']))
                            pc_xml_result = 'ER'  ### เก็บสถานะการทำงานในส่วน XML
                        ##########นับว่า สำเร็จ หรือ ไม่สำเร็จ #######
                        if pc_pdf_result == 'OK' and pc_xml_result == 'OK':  ### ถ้าสถานะของทั้ง xml และ pdf สำเร็จทั้งคู่จึงจะนับว่า invoice นั้นสำเร็จ
                            self.success = self.success + 1
                            self.success_recovery += 1
                            self.success_recovery_message.append({
                                "inputDate": date_now,
                                "batchName": name,
                                "invoiceNo": name,
                                "message": "การทำงานสำเร็จ"
                            })
                        else:
                            check_path(path_recover + '/save/' + date_now + '/')
                            with open(path_recover + '/save/' + date_now + '/' + name + '.txt', 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover save
                                recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                    else:
                        if (pc_result['errorCode'] == "ER999" and payload_user['SellerTaxid'] not in pc_result['errorMessage']) or pc_result['errorCode'] == "ER001" or pc_result['errorCode'] == "ER019" or pc_result['errorCode'] == "AU045":
                            self.recover_count += 1
                            self.recover.append({
                                "invoiceNo": name,
                                "errorCode": str(pc_result["errorCode"]),
                                "errorMessage": str(pc_result["errorMessage"])
                            })
                            check_path(path_recover + '/sign/' + date_now + '/')
                            shutil.move(path_single_file + '/' + fullname, path_recover + '/sign/' + date_now + '/'+ fullname)
                        elif pc_result['errorCode'] == "ER021" or pc_result['errorCode'] == "EX01" or pc_result['errorCode'] == "PC010" or pc_result['errorCode'] == "ERC001" or pc_result['errorCode'] == "ER004" or (pc_result['errorCode'] == "ER400" and pc_result['errorMessage'] == "Not found this transactionCode") or pc_result['errorCode'] == "PC001" or pc_result['errorCode'] == "ERPC002":
                            self.recover_count += 1
                            self.recover.append({
                                "invoiceNo": name,
                                "errorCode": str(pc_result["errorCode"]),
                                "errorMessage": str(pc_result["errorMessage"])
                            })
                            check_path(path_recover + '/check/' + date_now + '/')
                            with open(path_recover + '/check/' + date_now + '/'+ name +'.txt','w',encoding='UTF-8') as recover_file:### สร้างไฟล์เพื่อ recover check
                                recover_file.write(json.dumps({"transactionCode":service['transactionCode']}, indent=4, sort_keys=False, ensure_ascii=False))
                        else:
                            self.fail = self.fail + 1
                            print(str(date_now + time_now) + '>> ' + str(name) + ' Service singning failed. : ' + str(pc_result['errorMessage']))
                            self.losemessage.append({
                                'InvoiceName': str(name),
                                'Process DTM': str(date_now + time_now),
                                'errorCode': pc_result['errorCode'],
                                'errorMessage': pc_result['errorMessage']
                            })
                            self.fail_recovery += 1
                            self.fail_recovery_message.append({
                                "inputDate": date_now,
                                "batchName": name,
                                "invoiceNo": name,
                                "errorCode": str(pc_result['errorCode']),
                                "errorMessage": str(pc_result['errorMessage'])
                            })
                else:
                    if (service['errorCode'] == "ER999" and payload_user['SellerTaxid'] not in service['errorMessage']) or service['errorCode'] == "ER001" or service['errorCode'] == "ERC001":
                        self.recover_count += 1
                        self.recover.append({
                            "invoiceNo": name,
                            "errorCode": str(service["errorCode"]),
                            "errorMessage": str(service["errorMessage"])
                        })
                        check_path(path_recover + '/sign/' + date_now + '/')
                        shutil.move(path_single_file + '/' + fullname, path_recover + '/sign/' + date_now + '/' + fullname)
                    elif service['errorCode'] == "ER021" or service['errorCode'] == "EX01" or service['errorCode'] == "ER004" or service['errorCode'] == "PC001" or service['errorCode'] == "ERPC002":
                        self.recover_count += 1
                        self.recover.append({
                            "invoiceNo": name,
                            "errorCode": str(service["errorCode"]),
                            "errorMessage": str(service["errorMessage"])
                        })
                        check_path(path_recover + '/check/' + date_now + '/')
                        with open(path_recover + '/check/' + date_now + '/' + name + '.txt', 'w',encoding='UTF-8') as recover_file: ### สร้างไฟล์เพื่อ recover check
                            recover_file.write(json.dumps({"transactionCode": service['transactionCode']}, indent=4, sort_keys=False,ensure_ascii=False))
                    else:
                        self.fail = self.fail + 1
                        print(str(date_now + time_now) + '>> ' + str(name) + ' Service singning failed. : ' + str(service['errorMessage']))
                        self.losemessage.append({
                            'InvoiceName': str(name),
                            'Process DTM': str(date_now + time_now),
                            'errorCode': service['errorCode'],
                            'errorMessage': service['errorMessage']
                        })
                        self.fail_recovery += 1
                        self.fail_recovery_message.append({
                            "inputDate": date_now,
                            "batchName": name,
                            "invoiceNo": name,
                            "errorCode": str(service['errorCode']),
                            "errorMessage": str(service['errorMessage'])
                        })
            except KeyError as ke:
                self.recover_count += 1
                self.recover.append({
                    "invoiceNo": name,
                    "errorCode": "PS901",
                    "errorMessage": str(ke)
                })
                check_path(path_recover + '/sign/' + date_now + '/')
                shutil.move(path_single_file + '/' + fullname, path_recover + '/sign/' + date_now + '/'+ fullname) ### ย้ายไป input รอ recover
            except Exception as e:
                self.fail = self.fail + 1
                print(str(date_now + time_now) + ">> Failed to Generate Invoice " + str(name) + " : " + str(e))
                self.losemessage.append({
                    'InvoiceName': str(name),
                    'Process DTM': str(date_now + time_now),
                    'errorCode': 'ER888',
                    'errorMessage': 'Failed to Generate Invoice. : ' + str(e)
                })

    def recover_save(self, path_recover_save, path_save_now, output_local_path, output_remote_path, date_now, time_now, file):
        try:
            filename = str(file.split('.')[0])
            recover_data = json.loads(open(path_save_now + '/' + file, 'r', encoding='UTF-8').read())
            transactionCode = str(recover_data["transactionCode"])
            recheck_trans = checkStatus(self.payload,transactionCode, 0)
            if recheck_trans["status"] == "OK":
                save_pdf = saveFile(recheck_trans['pdfURL'], output_local_path + '/PDF/', filename+'.pdf', 0)
                if save_pdf["status"] == "OK":
                    print(str(date_now + time_now) + '>> ' + filename + ' Save PDF success.')
                    shutil.copy(output_local_path + '/PDF/' + filename + '.pdf', output_remote_path + '/PDF/' + filename + '.pdf')
                    print(str(date_now + time_now) + '>> ' + str(filename) + ' Put file.pdf success.')
                    output_pdf = True
                else:
                    output_pdf = False
                    print(str(date_now + time_now) + '>> ' + filename + ' Save PDF fail. : ' + str(save_pdf["errorMessage"]))
                save_xml = saveFile(recheck_trans['xmlURL'], output_local_path + '/XML/', filename+'.xml', 0)
                if save_xml["status"] == "OK":
                    print(str(date_now + time_now) + '>> ' + filename + ' Save XML success.')
                    shutil.copy(output_local_path + '/XML/' + filename + '.xml', output_remote_path + '/XML/' + filename + '.xml')
                    print(str(date_now + time_now) + '>> ' + str(filename) + ' Put file.pdf success.')
                    output_xml = True
                else:
                    output_xml = False
                    print(str(date_now + time_now) + '>> ' + filename + ' Save XML fail. : ' + str(save_xml["errorMessage"]))
                if not output_pdf or not output_xml:
                    shutil.move(path_save_now + file, path_recover_save + file)
                else:
                    os.remove(path_save_now+'/'+file)
            else:
                shutil.move(path_save_now + file, path_recover_save + file)
        except Exception:
            shutil.move(path_save_now + file, path_recover_save + file)
