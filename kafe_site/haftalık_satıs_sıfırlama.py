import json,time,datetime
def haftalık_satıs_sıfırlama():
    simdi=datetime.datetime.now()
    if simdi.weekday()==6 and simdi.hour==0:

        haftalık_satis_path=r"C:\Users\MONSTER\3D Objects\yazprojeler\KAFE\kafe_site\json\haftalık_satıs.json"

        with open(haftalık_satis_path,"r",encoding="utf-8") as file:
            veri=json.load(file)
        for i in veri:
            i["toplam_satıs"]=0
        print("satışlar sıfırlanıd")
        with open(haftalık_satis_path,"w",encoding="utf-8") as file:
            json.dump(veri,file,indent=4,ensure_ascii=False)
        print("sıfırlama kaydedildi.")

            
