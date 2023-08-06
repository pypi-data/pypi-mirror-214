from ..subclass.path.s_c_setgetlocal import *
from ..subclass.path.s_c_setgetdestination import *
from ..subclass.path.s_c_setgetrecovery import *
from ..subclass.file.s_c_file import *
from ..subclass.process.s_c_process_package_1 import *
from ..subclass.alert.s_c_alert import *
from ..subclass.recovery.s_c_recovery import *
from datetime import date, datetime
from ..subclass.input.s_c_input import *
from ..method.mail import *
from ..method.debug import *
from ..method.checkpath import *
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

class RECOVERY():
    def __init__(self,myPath="None",sftpPath="None",custPath="None",payloadData="None",userSftp="None",groupSftp ="None"):
        self.myPath = myPath
        self.sftpPath = sftpPath
        self.custPath = custPath
        self.userSftp = userSftp
        self.groupSftp = groupSftp
        self.dateNow = datetime.now().strftime("%Y%m%d")
        self.timeNow = datetime.now().strftime("%H%M%S")
        self.process_now = str(self.dateNow + self.timeNow)
        self.payloadData = payloadData
        ### Local
        self.local = setgetlocal(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Destination
        self.destination = setgetdestination(self.custPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Recovery
        self.recovery = setgetrecovery(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        self.recovery_process = ProcessRecovery(payloadData)
        ### alert
        self.alert = alert()

    def check(self):
        try:
            ### Get List Folder To Recovery
            pending_folder_check = [icd for icd in listdir(self.recovery.recoveryPathCheck) if isdir(join(self.recovery.recoveryPathCheck, icd))]
            if len(pending_folder_check) > 0:
                ### Loop To do All List Recovery Folder
                for folder_check in pending_folder_check:

                    ### Folder to do now in this round
                    recovery_pathcheck_now = self.recovery.recoveryPathCheck + folder_check + '/'
                    print("recovery_pathcheck_now -> " , recovery_pathcheck_now)
                    ### List File to do in this round
                    pending_check = [icf for icf in listdir(recovery_pathcheck_now) if isfile(join(recovery_pathcheck_now, icf))]
                    print("List File to do in this round -> " , pending_check)
                    if len(pending_check) > 0:
                        ### SetPath To Use
                        local_path_output = self.local.localOutputPath + pending_check + '/'
                        remote_path_output = self.destination.getDestinationPath()
                        check_path(local_path_output)
                        path_history = self.local.localHistoryPath + folder_check + "/"
                        check_path(path_history)
                        path_recover_check_now = self.recovery.recoveryPathCheck + folder_check + "/" + self.process_now + "/"
                        check_path(path_recover_check_now)

                        ### Move File To Recovery Temp Now
                        for file_check in pending_check:
                            shutil.move(recovery_pathcheck_now + file_check , path_recover_check_now+file_check)

                        ### Get List File To Recovery Now
                        all_check = [ac for ac in listdir(path_recover_check_now) if isfile(join(path_recover_check_now, ac))]

                        ### Thread Process Reovery
                        pool = ThreadPool(3)
                        func = partial(self.recovery_process.recover_check , 
                                       recovery_pathcheck_now,
                                       self.recovery.recoveryPath , 
                                       path_recover_check_now , local_path_output , 
                                       remote_path_output , folder_check , self.timeNow , path_history)
                        pool.map(func, all_check)
                        pool.close()
                        pool.join()

                        ### Delete Folder Temp Recovery After finish
                        shutil.rmtree(path_recover_check_now)

                        check_recheck_folder = [crcd for crcd in listdir(recovery_pathcheck_now) if isdir(join(recovery_pathcheck_now, crcd))]
                        check_recheck_file = [crcf for crcf in listdir(recovery_pathcheck_now) if isfile(join(recovery_pathcheck_now, crcf))]
                        print("Total File in folder -> " , len(check_recheck_folder) , " : " , len(check_recheck_file))
                        if len(check_recheck_folder) == 0 and len(check_recheck_file) == 0:
                            shutil.rmtree(recovery_pathcheck_now)
                        check_folder = [ch for ch in listdir(self.recovery.recoveryPathCheck) if isdir(join(self.recovery.recoveryPathCheck, ch))]
                        if len(check_folder) == 0:
                            shutil.rmtree(self.recovery.recoveryPathCheck)
            print(str(self.dateNow + self.timeNow) + '>> API Recovery : Process Recovery done.')
            result = {"status": "OK", "message": "Process Recovery done."}
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>> API Recovery error : ' + str(debug_row(e)))
            result = {"status": "ER","errorCode":"PR999", "errorMessage": 'API Recovery error : '+str(debug_row(e))}

    def sign(self):
        try:
            ### Get List Folder To Recovery
            pending_folder_sign = [jsd for jsd in listdir(self.recovery.recoveryPathSign) if isdir(join(self.recovery.recoveryPathSign, jsd))]
            if len(pending_folder_sign) > 0:
                for folder_sign in pending_folder_sign:
                    ### Folder to do now in this round
                    recovery_pathsign_now = self.recovery.recoveryPathSign + folder_sign + '/'
                    print("recovery_pathsign_now -> " , recovery_pathsign_now)
                    ### List File to do in this round
                    pending_send = [jsf for jsf in listdir(recovery_pathsign_now) if isfile(join(recovery_pathsign_now, jsf))]
                    print("List File to do in this round -> " , pending_send)
                    if len(pending_send) > 0:
                        ### SetPath To Use
                        local_path_output = self.local.localOutputPath + pending_send + '/'
                        remote_path_output = self.destination.getDestinationPath()
                        check_path(local_path_output)
                        path_history = self.local.localHistoryPath + folder_sign + "/"
                        check_path(path_history)
                        path_recover_sign_now = self.recovery.recoveryPathSign + folder_sign + "/" + self.process_now + "/"
                        check_path(path_recover_sign_now)

                        ### Move File To Recovery Temp Now
                        for file_check in pending_send:
                            shutil.move(recovery_pathsign_now + file_check , path_recover_sign_now+file_check)

                        ### Get List File To Recovery Now
                        all_check = [ac for ac in listdir(path_recover_sign_now) if isfile(join(path_recover_sign_now, ac))]

                        ### Thread Process Reovery
                        pool = ThreadPool(3)
                        func = partial(self.recovery_process.recover_check , 
                                       recovery_pathsign_now,
                                       self.recovery.recoveryPath , 
                                       path_recover_sign_now , local_path_output , 
                                       remote_path_output , folder_sign , self.timeNow , path_history)
                        pool.map(func, all_check)
                        pool.close()
                        pool.join()
                        
            print(str(self.dateNow + self.timeNow) + '>> API Recovery : Process Recovery done.')
            result = {"status": "OK", "message": "Process Recovery done."}
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>> API Recovery error : ' + str(debug_row(e)))
            result = {"status": "ER","errorCode":"PR999", "errorMessage": 'API Recovery error : '+str(debug_row(e))}

    def save(self):
        try:
            ### Get List Folder To Recovery
            pending_folder_save = [jsd for jsd in listdir(self.recovery.recoveryPathSave) if isdir(join(self.recovery.recoveryPathSave, jsd))]
            if len(pending_folder_save) > 0:
                for folder_save in pending_folder_save:
                    ### Folder to do now in this round
                    recovery_pathsave_now = self.recovery.recoveryPathSave + folder_save + '/'
                    print("recovery_pathsave_now -> " , recovery_pathsave_now)
                    ### List File to do in this round
                    pending_save = [jsf for jsf in listdir(recovery_pathsave_now) if isfile(join(recovery_pathsave_now, jsf))]
                    print("List File to do in this round -> " , pending_save)
                    if len(pending_save) > 0:
                        ### SetPath To Use
                        local_path_output = self.local.localOutputPath + pending_save + '/'
                        remote_path_output = self.destination.getDestinationPath()
                        check_path(local_path_output)
                        path_history = self.local.localHistoryPath + folder_save + "/"
                        check_path(path_history)
                        path_recover_save_now = self.recovery.recoveryPathSave + folder_save + "/" + self.process_now + "/"
                        check_path(path_recover_save_now)

                        ### Move File To Recovery Temp Now
                        for file_check in pending_save:
                            shutil.move(recovery_pathsave_now + file_check , path_recover_save_now+file_check)

                        ### Get List File To Recovery Now
                        all_check = [ac for ac in listdir(path_recover_save_now) if isfile(join(path_recover_save_now, ac))]

                        ### Thread Process Reovery
                        pool = ThreadPool(3)
                        func = partial(self.recovery_process.recover_save , 
                                       recovery_pathsave_now,
                                       self.recovery.recoveryPath , 
                                       path_recover_save_now , local_path_output , 
                                       remote_path_output , folder_save , self.timeNow , path_history)
                        pool.map(func, all_check)
                        pool.close()
                        pool.join()
                        
            print(str(self.dateNow + self.timeNow) + '>> API Recovery : Process Recovery done.')
            result = {"status": "OK", "message": "Process Recovery done."}
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>> API Recovery error : ' + str(debug_row(e)))
            result = {"status": "ER","errorCode":"PR999", "errorMessage": 'API Recovery error : '+str(debug_row(e))}
