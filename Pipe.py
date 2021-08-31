# ----------------------------------------
# Thick-Wall Pipe with 4 members-6 nodes
# ----------------------------------------


# Gerekli kütüphaneler import ediliyor.
import openseespy.opensees as ops
import openseespy.postprocessing.Get_Rendering as opsplt

# Çağırılan opensees komutları ile oluşturulan her şeyi temizle.
ops.wipe()

# Model oluşturacağımız uzayı tanımlıyoruz.
ops.model('basic','-ndm',2,'-ndf',2) # 2 yönde yer değiştirme, düzlem dışı yer değiştirmeler ve dönmeler kısıtlı.

# Düğüm noktaları koordinatları
ops.node(1, 200.0,  0.0)
ops.node(2, 300.0,  0.0)
ops.node(3, 141.42, 141.42)
ops.node(4, 212.13, 212.13)
ops.node(5, 0.0, 200.0)
ops.node(6, 0.0, 300.0)

# Mesnet bilgileri
# Sistemde 4 adet kayıcı mesnet bulunmakta.
ops.fix(1, 0, 1)
ops.fix(2, 0, 1)
ops.fix(5, 1, 0)
ops.fix(6, 1, 0)

# Malzeme tanımlama
ops.nDMaterial('ElasticIsotropic', 1, 100000.0, 0.25)

# Eleman tanımlama
# Elemanlarımız üçgen eleman, düzlem-şekil değiştirme sistemi
ops.element('Tri31', 1, 1, 2, 4, 1.0, 'PlaneStrain', 1)
ops.element('Tri31', 2, 1, 4, 3, 1.0, 'PlaneStrain', 1)
ops.element('Tri31', 3, 3, 4, 5, 1.0, 'PlaneStrain', 1)
ops.element('Tri31', 4, 5, 4, 6, 1.0, 'PlaneStrain', 1)

# Zaman serisi tanımlama
ops.timeSeries("Linear", 1)

# Yük sınıfı tanımlama
# Tek tip yükümüz var.
ops.pattern("Plain", 1, 1)

# Yükler tanımlanır.
ops.load(1, 7654.0, 0.0)
ops.load(3, 10824.0, 10824.0)
ops.load(5, 0.0 , 7654.0)

ops.system('BandSPD')
ops.numberer('RCM')
ops.constraints('Plain')
ops.integrator('LoadControl', 1.0)

# Çözüm algoritması
ops.algorithm('Linear')
 
# Analiz türü
ops.analysis('Static')
ops.analyze(1) # Analizin kaç kez yapılacağını belirtir.

# ---------------------------------
# Çıktı
# ---------------------------------

# Yer değiştirmeler
for i in range(1,7):
    print(i,"numaralı düğüm x=",ops.nodeDisp(i,1),"mm  -  y=",ops.nodeDisp(i,2),"mm")
    
# Modeli çizdir
opsplt.plot_model("nodes","elements")


































