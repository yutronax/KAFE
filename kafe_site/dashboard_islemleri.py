import datetime
import json
import os
import App
from flask import Flask, render_template, request, redirect, url_for, session, flash
from veri_tabanı import Kullanici, kullanıcı_siparisleri
from werkzeug.utils import secure_filename
kullanici=Kullanici()
toplam_fiyat=0
app=App.app
ortak_sifre = "elazığ"
<<<<<<< HEAD
haftalık_satis_path=r"haftalık_satıs.json"
yetkili_path=r'yetkili.json'
=======
haftalık_satis_path=r"C:\Users\MONSTER\3D Objects\yazprojeler\KAFE\kafe_site\json\haftalık_satıs.json"
yetkili_path=r'C:\Users\MONSTER\3D Objects\yazprojeler\KAFE\kafe_site\json\yetkili.json'
kampanya_path=r'C:\Users\MONSTER\3D Objects\yazprojeler\KAFE\kafe_site\json\kampanya.json'
>>>>>>> 148cac1 (Değişiklikler yapıldı)
def json_dosya_oku(dosya_adi):
      try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            return json.load(f)
      except FileNotFoundError:
        return []
      except json.JSONDecodeError:
        return []
def json_dosyası_yaz(dosya_adi,veri):
    with open(dosya_adi,"w",encoding="utf-8") as file:
        json.dump(veri,file,indent=2,ensure_ascii=False)

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
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # sadece resim uzantıları
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/dashboard/kampanya_ekle",methods=["GET","POST"])


@app.route("/dashboard/kampanya_ekle", methods=["GET", "POST"])
def kampanya_ekle():

    if request.method == "POST":
        if "ekle" in request.form:
            # DÜZELTME: request.form kullan (request.args değil)
            kampanya_aciklamasi = request.form.get("aciklama")
            kampanya_adi = request.form.get("kampanya_adi")
            kampanya_suresi = request.form.get("kampanya_suresi")
            indirim_orani = request.form.get("indirim_orani") 
            
            print(f"DEBUG - Form verileri:")
            print(f"Kampanya Adı: {kampanya_adi}")
            print(f"Açıklama: {kampanya_aciklamasi}")
            print(f"Süre: {kampanya_suresi}")
            print(f"İndirim Oranı: {indirim_orani}")
            
          
            if not all([kampanya_aciklamasi, kampanya_adi, kampanya_suresi]):
                flash('Lütfen tüm zorunlu alanları doldurun.')
                return render_template("kampanya_ekle.html")
            
            # Dosya kontrolü
            if 'file' not in request.files:
                flash('Dosya bulunamadı.')
                return render_template("kampanya_ekle.html")
            
            file = request.files['file']
            print(f"DEBUG - Dosya: {file.filename}")
            
            if file.filename == '':
                flash('Dosya seçilmedi.')
                return render_template("kampanya_ekle.html")
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Aynı isimde dosya varsa benzersiz isim oluştur
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    filename = f"{base_name}_{counter}{extension}"
                    counter += 1
                
                # Dosyayı kaydet
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(f"DEBUG - Dosya kaydedildi: {file_path}")
                
                # Kampanya verilerini JSON'a kaydet
                veri = json_dosya_oku(kampanya_path)
                
                yeni_kampanya = {
                    "img": filename,
                    "isim": kampanya_adi,
                    "aciklama": kampanya_aciklamasi,
                    "sure": kampanya_suresi,
                    "indirim_orani": indirim_orani if indirim_orani else "0"
                }
                
                veri.append(yeni_kampanya)
                print(veri)
                json_dosyası_yaz(kampanya_path, veri)
                print(f"DEBUG - JSON'a kaydedildi: {yeni_kampanya}")
                
                flash('Kampanya başarıyla eklendi!')
                
                # DÜZELTME: ekle.html yerine başarı mesajıyla aynı sayfada kal
                return redirect(url_for('kampanya_ekle'))
            
            else:
                flash('Geçersiz dosya türü. Sadece resim dosyaları yüklenebilir.')
                return render_template("kampanya_ekle.html")
    
    return render_template("kampanya_ekle.html")

# Test route - kampanyaları görmek için
@app.route("/kampanyalar")
def kampanyalar_listele():
    kampanyalar = json_dosya_oku(kampanya_path)
   
    return render_template("kampanyalar.html",kampanyalar=kampanyalar)