import pandas as pd
import numpy as np

data = pd.read_excel(r'data fixx.xlsx')

f1 = pd.DataFrame(data, columns = ['slg'])
f2 = pd.DataFrame(data, columns = ['goa_maria'])
f3 = pd.DataFrame(data, columns = ['kebun_matahari'])
f4 = pd.DataFrame(data, columns = ['goa_selomangleng'])
f5 = pd.DataFrame(data, columns = ['gunung_klotok'])
f6 = pd.DataFrame(data, columns = ['bdi'])
f7 = pd.DataFrame(data, columns = ['alun_kediri'])
f8 = pd.DataFrame(data, columns = ['taman_sekartaji'])
f9 = pd.DataFrame(data, columns = ['klenteng'])

data = np.hstack((f1,f2,f3,f4,f5,f6,f7,f8,f9))

#============== Inisialisasi Variabel ==============#
alpha = 1
beta = 1
p = 0.45
rho = 1
iterasi = 5
t = np.full((9,9),0.021) #set tau awal 0.021
tau_baru = t


def split(arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr   = arr[size:]
        arrs.append(arr)
        return arrs

for i in range(iterasi+1):
    tau_lama = tau_baru
    iterasi = i
    #============== Nilai Visibilitas ==============#
    visibilitas = np.round(np.divide(1,data, out = np.zeros_like(data), where=data!=0),5) #0 tidak dibagi biar ga devide by 0
    n = 0
    mem = []
    #============== Pencarian Rute ==============#
    while True:
        #============== Probabilitas ==============#
        prob = []
        # visibilitas = vis
        w, h = visibilitas.shape
        for i in range (h):
            for j in range (w):
                hasil = (tau_lama[i,j] * visibilitas[i,j]) / np.matmul(tau_lama[i,:],visibilitas[i,:])
                prob.append(hasil)

        probabilitas = np.round(split(prob, len(data)),5)

        #============== Max Probabilitas ==============#
        maks = []
        tujuan = []
        memory = []
        for i in range(len(data)):
            Max = max(probabilitas[i,:])

            if (Max==probabilitas[i,0]):
                Tujuan = 0
            elif (Max==probabilitas[i,1]):
                Tujuan = 1
            elif (Max==probabilitas[i,2]):
                Tujuan = 2
            elif (Max==probabilitas[i,3]):
                Tujuan = 3
            elif (Max==probabilitas[i,4]):
                Tujuan = 4
            elif (Max==probabilitas[i,5]):
                Tujuan = 5
            elif (Max==probabilitas[i,6]):
                Tujuan = 6
            elif (Max==probabilitas[i,7]):
                Tujuan = 7
            elif (Max==probabilitas[i,8]):
                Tujuan = 8
            Memory =  [Tujuan]
        
            maks.append(Max)
            tujuan.append(Tujuan)
            memory.append(Memory)
        #============== End of Max Probabilitas ==============#

        # hasil = np.column_stack((probabilitas, maks, tujuan, memory))
        # print(hasil)

        #============== meng 0 kan nilai yang dikunjungi ==============#
        h,w = np.array(memory).shape

        for i in range (h):
            for j in range(w):
                a = memory[i][j]
                probabilitas[i,a] = 0
        visibilitas = probabilitas
        n = n + 1
        mem.append(memory)
        if(maks[1] == 1):
            break
    #============== End of Pencarian Rute ==============#

    memory = np.transpose(mem)
    memory = memory[0]
    awal_kunjungan = [0,1,2,3,4,5,6,7,8]
    memory = np.column_stack((awal_kunjungan,memory))
    # print(memory)
    # print(data)

    #============== Menghitung jarak total ==============#
    jarak = []
    for i in range(len(memory)):
        Jarak = 0
        for j in range(len(memory)-1):
            Jarak = Jarak + data[i,memory[i,j]] + data[i,memory[i,j+1]]
        jarak.append(Jarak)

    jarak = np.round(jarak,2)
    # print(jarak[1])
    hasil_akhir = np.column_stack((memory, jarak))
    np.set_printoptions(suppress=True) #Biar ga keluar nilai e+ coba comment kalo ga percaya

    #============== Jarak Paling Minimum ==============#
    jarak_minimum = np.argmin(hasil_akhir[:,9])
    print("\n\n#======================== ITERASI KE ",iterasi," ========================#")
    print("HASIL ITERASI KE ", iterasi)
    print(hasil_akhir)
    print("\nRUTE DENGAN JARAK PALING PENDEK " ,iterasi,)
    print(hasil_akhir[jarak_minimum])

    #============== Update Feromon (Tau) ==============#
    tau_baru = []
    for i in range(len(memory)):
        delta_tau = np.round((p / jarak[i]),4)
        Tau = np.full((9,9),0.0) #set 0 biar diisi
        # print(delta_tau)
        for j in range(len(memory)-1):
            Tau[memory[i,j],memory[i,j+1]] = delta_tau
            Tau[memory[i,j+1],memory[i,j]] = delta_tau
        # print(Tau)
        # print("==================================================")
        tau_baru.append(Tau)
    tau_baru = sum(tau_baru)
    tau_baru = np.array(p * np.array(data)) + np.array(tau_lama)
    print("\nUPDATE FEROMON " ,iterasi,)
    print(tau_baru)
