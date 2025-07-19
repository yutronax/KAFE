import json
import App
from flask import Flask, render_template, request, redirect, url_for, session, flash
from veri_tabanı import Kullanici, kullanıcı_siparisleri
kullanici=Kullanici()
toplam_fiyat=0
app=App.app
ortak_sifre = "elazığ"
haftalık_satis_path=r"haftalık_satıs.json"
yetkili_path=r'yetkili.json'
def json_dosya_oku(dosya_adi):
    with open(dosya_adi,"r",encoding="utf-8") as file:
      veri=json.load(file)
    return veri
def json_dosyası_yaz(dosya_adi,veri):
    with open(dosya_adi,"w",encoding="utf-8") as file:
        json.dump(veri,file,indent=4,ensure_ascii=False)
@app.route('/dashboard', methods=['GET', 'POST'])
def Dashboard():
    global toplam_fiyat
    if 'yetkili' not in session:
        flash('Lütfen yetkili olarak giriş yapın!', 'warning')
        return redirect(url_for('DashboardGiris'))
        
    haftalık_satıs = json_dosya_oku(haftalık_satis_path)
   
    toplam_satıs=0
    for i in haftalık_satıs:
            toplam_satıs+=i["toplam_satıs"]
    toplam_uye=kullanici.toplam_uye_sayisi()
    if session['yetki_düzeyi'] == 'patron':
        if request.method == 'POST':
         if request.args.get('action') == 'ekle':
            yeni_yetkili = request.form['yeni_yetkili']
            yeni_yetki_düzeyi = request.form['yeni_yetki_düzeyi']
            if yeni_yetkili and yeni_yetki_düzeyi:
                   
                    veri=json_dosya_oku(yetkili_path)
                    veri.append({
                        "isim": yeni_yetkili,
                        "yetki düzeyi": yeni_yetki_düzeyi
                    })
                    
                    json_dosyası_yaz(yetkili_path,veri)
                    flash('Yeni yetkili eklendi!', 'success')
            else:
                flash('Lütfen tüm alanları doldurun!', 'danger')
         elif request.args.get('action') == 'sil':
            yetkili_sil = request.form['yetkili_sil']
            yetkililer=json_dosya_oku(yetkili_path)
            yetkili_sil=[isim["isim"] for isim in yetkililer if isim["isim"]==yetkili_sil ]
            if yetkili_sil :
                    
                yetkililer = [y for y in yetkililer if y['isim'] != yetkili_sil]
                json_dosyası_yaz(yetkili_path,yetkililer)    
                flash(f'{yetkili_sil} yetkilisi silindi!', 'success')
            else:
                flash('Yetkili bulunamadı!', 'danger')
            
        
    
    return render_template('dashboard.html', urunler=haftalık_satıs,uye=toplam_uye,toplam_satıs=toplam_satıs)
@app.route('/dashboard/giris', methods=['GET', 'POST'])
def DashboardGiris():

    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        yetkililer = json_dosya_oku(yetkili_path)
        for kisi in yetkililer:
         if kisi["isim"]==kullanici_adi and sifre == ortak_sifre:
            session['yetkili'] = True
            session['yetki_düzeyi'] = kisi['yetki düzeyi']
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('Dashboard'))
        else:
            flash('Kullanıcı adı veya şifre yanlış!', 'danger')
    
    return render_template('dashboard_giris.html')
@app.route('/dashboard/Cikis')
def DashboardCikis():
    session.pop('yetkili', None)
    session.pop('yetki_düzeyi', None)
    flash('Çıkış başarılı!', 'success')
    return redirect(url_for('DashboardGiris'))
