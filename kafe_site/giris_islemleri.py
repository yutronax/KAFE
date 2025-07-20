
from flask import Flask, render_template, request, redirect, url_for, session, flash
import App
from veri_tabanı import Kullanici,kullanıcı_siparisleri,GREEN_MONEY
musteri=Kullanici()
siparisler=kullanıcı_siparisleri()
money=GREEN_MONEY()
app=App.app
#gizli anahtar ayarla
app.secret_key="elazığ"
#template klasörünü ayarla
app.template_folder = 'templates'
#üyelik sayfası yapıcağız ilk önce kayıt sayfasını yapalım


@app.route('/kayıt', methods=['GET', 'POST'])
def Kayit():
    if request.method == 'POST':
        Kullanici_Adi=request.form['Kullanici_Adi']
        Kullanici_Soyadi=request.form['Kullanici_Soyadi']
        Sifre=request.form['Sifre']
        Sifre_Tekrar=request.form['Sifre_Tekrar']
        if Sifre != Sifre_Tekrar:
            flash('Şifreler eşleşmiyor!', 'danger')
            return redirect(url_for('Kayit'))
        kullanici_ismi= musteri.kullanici_var_mi(Kullanici_Adi, Sifre)
        if kullanici_ismi:
            flash('Bu kullanıcı adı zaten alınmış!', 'danger')
            return redirect(url_for('Kayit'))
        musteri.kaydet(Kullanici_Adi, Kullanici_Soyadi, Sifre)
        
        flash('Kayıt başarılı!', 'success')
        return redirect(url_for('Giriş'))
    return render_template('kayit.html')



# Giriş sayfasını yapalım
@app.route('/giriş', methods=['GET', 'POST'])
def Giriş(): 
    if request.method == 'POST':
        Kullanici_Adi = request.form['Kullanici_Adi']
        Sifre = request.form['Sifre']
        session["sifre"]=Sifre
        if musteri.kullanici_var_mi(Kullanici_Adi, Sifre):
            session['kullanici_id'] = Kullanici_Adi
            flash('Giriş başarılı!', 'success')
            money.user_insert(kullanici_adi=Kullanici_Adi,sifre=Sifre)
            return redirect(url_for('Anasayfa'))
        else:
            flash('Kullanıcı adı veya şifre yanlış!', 'danger')
    

        
    return render_template('giris.html')
@app.route('/')
def anasayfa():
    session.clear()
    return redirect(url_for('Anasayfa'))
@app.route('/anasayfa', methods=['GET', 'POST'])
def Anasayfa():
    if 'kullanici_id' not in session:
        flash('Lütfen giriş yapın!', 'warning')
        return redirect(url_for('Giriş'))
    if request.method == 'GET':
        href = request.args.get('href')
        if href:           
            return redirect(url_for(f'{href}'))
    
    return render_template('anasayfa.html')
@app.route('/cikis')
def Cikis():
    session.pop('kullanici_id', None)
    flash('Çıkış başarılı!', 'success')
    return redirect(url_for('Giriş'))
@app.route('/profil')
def Profil():
    if 'kullanici_id' not in session:
        flash('Lütfen giriş yapın!', 'warning')
        return redirect(url_for('Giriş'))    
    kullanici_adi = session['kullanici_id']
    kullanici_bilgileri=musteri.kullanici_bilgileri_getir(kullanici_adi)
    if not kullanici_bilgileri:
        flash('Kullanıcı bilgileri bulunamadı!', 'danger')
        return redirect(url_for('Giriş'))
    harcama=siparisler.toplam_harcama()
    beklenen,tamamlanan,tumu=siparisler.bekleyen()    
    return render_template('profil.html',harcama=harcama,beklenen=beklenen,tamamlanan=tamamlanan,tumu=tumu)

