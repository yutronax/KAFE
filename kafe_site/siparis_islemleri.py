import App,datetime
from flask import Flask, json, render_template, request, redirect, url_for, session, flash
from veri_tabanı import Kullanici, kullanıcı_siparisleri

app=App.app
siparisler = kullanıcı_siparisleri()
haftalık_satis_path=r"haftalık_satıs.json"
urunler_path=r'urunler.json'
with open(urunler_path, 'r', encoding="utf-8") as file:
    urunler = json.load(file)


@app.route('/siparis', methods=['GET', 'POST'])
def Siparis():
    if 'kullanici_id' not in session:
        flash('Lütfen giriş yapın!', 'warning')
        return redirect(url_for('Giriş'))

    if request.method == 'POST':
        kullanici_adi = session['kullanici_id']
        secilen_urunler = request.form.getlist('urunler')
        print(secilen_urunler)  

        if not secilen_urunler:
            flash('Lütfen en az bir ürün seçin!', 'warning')
            return redirect(url_for('Siparis'))

        toplam_fiyat = sum(
            urun["fiyat"] for urun in urunler if urun["isim"] in secilen_urunler
        )

        
        siparis_str = ','.join(secilen_urunler)
        if "onay" in request.form: 
            beklenen,_,_= siparisler.bekleyen() 
            if beklenen>0:
                flash("Tamamlanmamış Siparişiniz var.")
                return redirect(url_for("Siparis"))

            with open(haftalık_satis_path,"r",encoding="utf-8") as file:
                veri=json.load(file)
            for i in secilen_urunler:
                for j in veri:
                    if i==j["isim"]:
                        j["toplam_satıs"]+=1

            with open(haftalık_satis_path,"w",encoding="utf-8") as file:
                json.dump(veri,file,indent=4,ensure_ascii=False)
            tarih=datetime.datetime.now()
            durum="beklemede"
                  
            siparisler.siparis_ekle(kullanici_adi, siparis_str,tarih,durum,toplam_fiyat)
            
           
            return redirect(url_for('Odeme'))
        

    return render_template('siparis.html', urunler=urunler) 

    
@app.route('/odeme')
def Odeme():
     toplam_fiyat=siparisler.toplam_fiyat()
     flash(f'Siparişiniz başarıyla alındı! Toplam tutar: {toplam_fiyat} TL', 'success')
     return render_template("odeme.html",toplam_fiyat=toplam_fiyat)


@app.route('/siparislerim',methods=["GET","POST"])
def Siparislerim():
    if 'kullanici_id' not in session:
        flash('Lütfen giriş yapın!', 'warning')
        return redirect(url_for('Giriş'))
    if request.method=="POST":
        if "iptal" in request.form:
          uyarı=siparisler.siparis_sil()
          if uyarı==0:
              flash("siparisiniz bulunmamaktadır!")
    kullanici_adi = session['kullanici_id']
    veriler = siparisler.siparisleri_getir(kullanici_adi)

    siparis_listesi = [satir[0] for satir in veriler]
    tarih_listesi = [satir[1] for satir in veriler]
    durum_listesi = [satir[2] for satir in veriler]
    birlesik_liste=zip(siparis_listesi,tarih_listesi,durum_listesi)
  

    
    return render_template('siparislerim.html',tum_liste = birlesik_liste, urunler=urunler)

  

