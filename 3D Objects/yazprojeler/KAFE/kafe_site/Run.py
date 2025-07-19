import App,giris_islemleri, siparis_islemleri, dashboard_islemleri,haftalık_satıs_sıfırlama,threading
from flask import session
hafta=haftalık_satıs_sıfırlama
threading.Thread(target=hafta.haftalık_satıs_sıfırlama).start()

app=App.app

    
if __name__ == '__main__':
    app.run(debug=True)
