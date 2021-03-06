# -*- coding: utf-8 -*-
"""Vehicle-Insurance Datasets Classification Using K-Nearest-Neighbor Algorithm

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SKpQqOfbvy6HH4AsA7g9zQ5ytGYi9qAb

#SUPERVISED LEARNING - CLASSIFICATION : DATASET KENDARAAN
oleh:	MUHAMMAD SHULHANNUR mshulhannur@gmail.com

Algoritma = k-Nearest Neighbor    
Banyak tetangga (k) = 13 {1,3,5,...,25}   
banyak data train = 5000   
banyak data test = 1000   
Penghitungan jarak = Euclidean Distance   
Kolom yg dipakaI = Jenis_Kelamin, Umur, Kendaraan_Rusak, Sudah_Asuransi, Premi, Lama_Berlangganan

#LAKUKAN IMPORT LIBRARIES
"""

#untuk data analysis and manipulation
import pandas as pd

#untuk matematika
import numpy as np

#untuk matematika
import math

#untuk grafik 2D
import matplotlib.pyplot as plt

#untuk url
import io

#untuk request file from url
import requests

#untuk request file from url
import time

"""#DATA PREPROCESSING

##READ FILES INTO DATASETS
"""

# Read kendaraan_train.csv file into DataFrame
url_datatraining = "https://cdn.discordapp.com/attachments/756550576640360469/833533583331164190/kendaraan_train.csv"
training = requests.get(url_datatraining).content
train = pd.read_csv(io.StringIO(training.decode('utf-8')), nrows=5000)
train = train.drop(columns = ['id','Kode_Daerah','Umur_Kendaraan','Kanal_Penjualan','SIM'])
train

# Read kendaraan_test.csv file into DataFrame
url_datatesting="https://cdn.discordapp.com/attachments/756550576640360469/833533558941024266/kendaraan_test.csv"
testing=requests.get(url_datatesting).content
test = pd.read_csv(io.StringIO(testing.decode('utf-8')), nrows=1000)
test = test.drop(columns = ['Kode_Daerah','Umur_Kendaraan','Kanal_Penjualan','SIM'])
test

"""##TENTUKAN NILAI K"""

K_VALUES = [1,3,5,7,9,11,13,15,17,19,21,23,25]

test.head()

"""##LAKUKAN DATA CLEANSING"""

# method untuk cleansing data, untuk data non numerik yaitu Jenis_Kelamin dan Kendaraan_Rusak juga mengisi data yang kosong dengan nilai means kolom
def preprocess(dataset):
  gender = []
  broken = []
  for idx, node in dataset.iterrows():
    gender.append(1 if node['Jenis_Kelamin'] == 'Pria' else 0)
    broken.append(1 if node['Kendaraan_Rusak'] == 'Pernah' else 0)
  dataset["Jenis_Kelamin"] = gender
  dataset["Kendaraan_Rusak"] = broken
  # proses pengisian data yang kosong di kolom numerik
  for key in dataset.columns:
    # data kosong di isi dengan nilai mean dari kolom
    dataset[key].fillna(dataset[key].mean(), inplace=True)

"""##NORMALISASIKAN TABEL"""

# menormalisasikan seluruh field
def normalizeAllNumericFields(dataset):
  numeric_field = dataset._get_numeric_data().columns
  for key in numeric_field:
      dataset[key] = (dataset[key] - dataset[key].min()) / (dataset[key].max() - dataset[key].min())

"""#OBSERVASI

##TENTUKAN NILAI EUCLEDIAN DISTANCE
"""

# menghitung jarak eucledian
def eucledian(train, test):
  keys = ['Jenis_Kelamin','Umur','Kendaraan_Rusak','Sudah_Asuransi','Premi','Lama_Berlangganan']
  total = 0
  for key in keys:
    total = total + math.pow(test[key] - train[key], 2)
  return math.sqrt(total)

"""##HITUNG NILAI KNN"""

# menentukan hasil knn berdasarkan jarak eucledian terdekat
def define_outcome(dataset, k):
  datas = dataset[0:k]
  # menghitung banyak case dengan output 1
  totalPositive = [1 for case in datas.iterrows() if case[1]['Tertarik'] == 1]
  # menghitung banyak case dengan output 0
  totalNegative = [0 for case in datas.iterrows() if case[1]['Tertarik'] == 0]
  # jika lebih banyak case dengan output 1 maka hasil knn adalah 1 dan sebaliknya
  if len(totalPositive) > len(totalNegative):
      return 1
  else:
      return 0

"""##HITUNG NILAI AKURASI"""

# menghitung akurasi
def calc_accurracy(miss_outcome, pass_outcome):
  total = miss_outcome + pass_outcome
  return float(pass_outcome) * 100 / total

"""#EKSEKUSI

##PEMANGGILAN FUNGSI
"""

# proses utama KNN
def k_nn(train, test, k):
  temp_outcome = []
  for test_case in test.iterrows():
    temp = []
    for train_case in train.iterrows():
      temp.append(eucledian(train_case[1], test_case[1]))
    train['eucledian'] = temp
    sorted_by_eucledian = train.sort_values('eucledian')
    temp_outcome.append(define_outcome(sorted_by_eucledian, k))
  test['outcome'] = temp_outcome
  return(test)

"""##READ DATASETS INTO FILES"""

# export hasil ke csv
def exportCSV(hasil,k):
  df = hasil[['outcome','Tertarik','status']]
  nama = 'tetangga '+str(k)+' | k-NN.csv'
  df.to_csv(nama)
  print("\nexport file ",nama,'selesai')

"""##MAIN"""

start_time = time.time()
preprocess(train)
preprocess(test)
normalizeAllNumericFields(train)
normalizeAllNumericFields(test)
# tinggal proses k-nn nya aja
res = []
start_knn = time.time()
for k in K_VALUES:
  start = time.time()
  output = k_nn(train,test,k)
  miss_outcome = 0
  pass_outcome = 0
  status = []
  for test_case in output.iterrows():
    if test_case[1]['outcome'] != test_case[1]['Tertarik']:
      miss_outcome = miss_outcome + 1
      status.append('SALAH')
    else:
      pass_outcome = pass_outcome + 1
      status.append('benar')
  acc = calc_accurracy(miss_outcome, pass_outcome)
  output['status'] = status
  exportCSV(output,k)
  res.append(acc)
  stop = time.time()
  print('akurasi ',k,'- NearestNeighbor :',acc)
  print('Runtime :',stop - start)
stop_knn = time.time()
print('Total Runtime : ',stop_knn - start_knn)
plt.plot(K_VALUES, res, 'bx-')
plt.ylabel('Akurasi')
plt.xlabel('Nilai K')
plt.title('K-NN')
plt.show()
print("--- Running for %s seconds ---" % (time.time() - start_time))
